# -*- coding: utf-8 -*-
"""Qwen3-TTS 本地冒烟测试:加载 0.6B CustomVoice 模型,合成一段中文语音。"""
import os
# 默认用 HuggingFace 官方源。若官方源下载慢,可改用国内镜像:
# os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

import torch
import soundfile as sf
from qwen_tts import Qwen3TTSModel

MODEL_ID = "Qwen/Qwen3-TTS-12Hz-0.6B-CustomVoice"
OUT = os.path.join(os.path.dirname(__file__), "output_test.wav")

print(f"[1/4] 加载模型 {MODEL_ID} ...")
model = Qwen3TTSModel.from_pretrained(
    MODEL_ID,
    device_map="cuda:0",
    dtype=torch.bfloat16,
    # Windows 无 flash-attn,使用默认 eager 实现
)

print("[2/4] 支持的语言:", model.get_supported_languages())
speakers = model.get_supported_speakers()
print("[2/4] 支持的音色:", speakers)

spk = speakers[0] if speakers else "Ryan"
text = "你好,这是通义千问 Qwen3 语音合成模型的本地测试。今天天气不错。"

print(f"[3/4] 使用音色 '{spk}' 合成语音 ...")
wavs, sr = model.generate_custom_voice(text=text, language="Chinese", speaker=spk)

sf.write(OUT, wavs[0], sr)
print(f"[4/4] 完成!采样率={sr}Hz,已保存到: {OUT}")
