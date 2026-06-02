# -*- coding: utf-8 -*-
"""长稿播报 TTS:把 markdown 播报稿用克隆主播声合成,按句切块拼接,输出 MP3。"""
import os
import re
import numpy as np
import torch
import lameenc

HERE = os.path.dirname(__file__)
REF = os.path.join(HERE, "ref_clip.wav")
MODEL_DIR = os.path.join(HERE, "models", "Qwen3-TTS-1.7B-Base")

MD = r"E:\Github_project\ai-briefcast\.claude\worktrees\upbeat-poincare-c12c19\samples\broadcast-2026-06-02-concise.md"
OUTDIR = r"E:\Github_project\ai-briefcast\audio_output"
SUFFIX = "-qwen"   # 区别于豆包(豆包用 -doubao 或无后缀)
OUT = os.path.join(OUTDIR, os.path.splitext(os.path.basename(MD))[0] + SUFFIX + ".mp3")

LANG = "Chinese"
CHUNK_LIMIT = 120   # 每块最大字数

# ---------- 1. 读取并提取正文(去掉 markdown 头/引用/分隔线) ----------
with open(MD, encoding="utf-8") as f:
    raw = f.read()
body = raw.split("\n---\n", 1)
body = body[1] if len(body) > 1 else raw[0]
paragraphs = []
for ln in body.splitlines():
    s = ln.strip()
    if not s or s.startswith("#") or s.startswith(">") or s == "---":
        continue
    paragraphs.append(s)

# ---------- 2. 按句切块(长段落用 。!? 拆分,合并到 CHUNK_LIMIT) ----------
def chunk_text(paragraphs, limit):
    chunks = []
    for p in paragraphs:
        if len(p) <= limit:
            chunks.append(p)
            continue
        sents = [s for s in re.findall(r'[^。！？]*[。！？]?', p) if s]
        cur = ""
        for s in sents:
            if len(cur) + len(s) <= limit:
                cur += s
            else:
                if cur:
                    chunks.append(cur)
                cur = s
        if cur:
            chunks.append(cur)
    return chunks

chunks = chunk_text(paragraphs, CHUNK_LIMIT)
print(f"正文切成 {len(chunks)} 个文本块")

# ---------- 3. 转写参考音频得到文字稿 ----------
print("[1/4] 转写参考音频 ...")
from faster_whisper import WhisperModel
asr = WhisperModel("small", device="cpu", compute_type="int8")
segs, info = asr.transcribe(REF, beam_size=5)
ref_text = "".join(s.text for s in segs).strip()
del asr
print(f"      参考文字稿: {ref_text}")

# ---------- 4. 加载模型并构建一次克隆 prompt(复用,保证音色一致) ----------
print("[2/4] 加载 1.7B-Base 模型 ...")
from qwen_tts import Qwen3TTSModel
model = Qwen3TTSModel.from_pretrained(MODEL_DIR, device_map="cuda:0", dtype=torch.bfloat16)
clone_prompt = model.create_voice_clone_prompt(ref_audio=REF, ref_text=ref_text)

# ---------- 5. 逐块合成 ----------
print("[3/4] 逐块克隆合成 ...")
sr = 24000
pieces = []
for i, c in enumerate(chunks):
    w, sr = model.generate_voice_clone(text=c, language=LANG, voice_clone_prompt=clone_prompt)
    pieces.append(w[0].astype(np.float32))
    print(f"      [{i+1}/{len(chunks)}] {len(w[0])/sr:5.1f}s  {c[:24]}")

# ---------- 6. 拼接(块间 0.35 秒停顿) ----------
gap = np.zeros(int(0.35 * sr), dtype=np.float32)
audio = []
for i, w in enumerate(pieces):
    audio.append(w)
    if i < len(pieces) - 1:
        audio.append(gap)
audio = np.concatenate(audio)

# ---------- 7. 编码 MP3 ----------
print("[4/4] 编码 MP3 ...")
os.makedirs(OUTDIR, exist_ok=True)
pcm16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
enc = lameenc.Encoder()
enc.set_bit_rate(128)
enc.set_in_sample_rate(sr)
enc.set_channels(1)
enc.set_quality(2)
mp3 = enc.encode(pcm16.tobytes()) + enc.flush()
with open(OUT, "wb") as f:
    f.write(mp3)
print(f"完成!总时长 {len(audio)/sr:.1f} 秒,已保存到: {OUT}")
