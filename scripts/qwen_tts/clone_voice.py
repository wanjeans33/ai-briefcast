# -*- coding: utf-8 -*-
"""音色克隆(ICL 高保真模式):
1. 用 faster-whisper 自动转写参考音频得到文字稿;
2. 用 Qwen3-TTS-12Hz-1.7B-Base 克隆该音色合成新文本。
"""
import os
import torch
import soundfile as sf

HERE = os.path.dirname(__file__)
REF = os.path.join(HERE, "ref_clip.wav")          # 参考音频(15 秒片段)
OUT = os.path.join(HERE, "output_clone.wav")      # 克隆输出

# 想让克隆音色"说"的内容,改这里即可
TARGET_TEXT = "大家好,这是用克隆出来的音色合成的一段语音测试,你觉得像不像?"
TARGET_LANG = "Chinese"   # 目标语言:Chinese / English / Japanese ...

# ---------- 1. 转写参考音频 ----------
print("[1/3] 转写参考音频得到文字稿 ...")
from faster_whisper import WhisperModel
asr = WhisperModel("small", device="cpu", compute_type="int8")
segments, info = asr.transcribe(REF, beam_size=5)
ref_text = "".join(s.text for s in segments).strip()
print(f"      检测语言: {info.language} (置信度 {info.language_probability:.2f})")
print(f"      参考文字稿: {ref_text}")
del asr

# ---------- 2. 加载克隆模型 ----------
print("[2/3] 加载 Qwen3-TTS-12Hz-1.7B-Base ...")
from qwen_tts import Qwen3TTSModel
# 用从魔搭下载到本地的模型目录(避免 HF 大文件下载不稳定)
MODEL_DIR = os.path.join(HERE, "models", "Qwen3-TTS-1.7B-Base")
model = Qwen3TTSModel.from_pretrained(
    MODEL_DIR,
    device_map="cuda:0",
    dtype=torch.bfloat16,
)

# ---------- 3. 克隆合成 ----------
print(f"[3/3] 用克隆音色合成: {TARGET_TEXT}")
wavs, sr = model.generate_voice_clone(
    text=TARGET_TEXT,
    language=TARGET_LANG,
    ref_audio=REF,
    ref_text=ref_text,          # ICL 模式:参考文字稿
)
sf.write(OUT, wavs[0], sr)
print(f"完成!采样率={sr}Hz,已保存到: {OUT}")
