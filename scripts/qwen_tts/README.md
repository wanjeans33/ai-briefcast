# Qwen3-TTS 本地语音合成脚本

基于阿里通义 [Qwen3-TTS](https://github.com/QwenLM/Qwen3-TTS)(Apache-2.0)的本地 TTS 工具,
作为豆包 TTS 之外的另一套合成方案。支持预置音色、音色克隆、长稿播报导出 MP3。

## 环境准备

需要 NVIDIA GPU(1.7B 模型建议 ≥8GB 显存)。建议用独立虚拟环境:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

# 安装匹配 CUDA 的 PyTorch(以 CUDA 12.4 为例)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu124

# 安装 Qwen3-TTS 及本仓脚本所需依赖
pip install -U qwen-tts faster-whisper lameenc hf_xet
```

> Windows 上 `flash-attn` 难安装,可跳过(脚本默认用 PyTorch 实现);
> `sox` 警告无害(仅 25Hz tokenizer 需要,本脚本用 12Hz 模型)。

## 模型下载

首次运行会自动从 HuggingFace 拉取。若官方源大文件下载不稳定,推荐用魔搭(国内更稳):

```powershell
pip install modelscope
python -c "from modelscope import snapshot_download; snapshot_download('Qwen/Qwen3-TTS-12Hz-1.7B-Base', local_dir='models/Qwen3-TTS-1.7B-Base')"
```

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `test_tts.py` | 用 0.6B-CustomVoice 预置音色合成一段中文(冒烟测试) |
| `clone_voice.py` | 音色克隆(ICL):自动转写参考音频 → 用 1.7B-Base 克隆合成 |
| `broadcast_tts.py` | 长稿播报:读取 markdown 稿,按句切块逐块克隆合成 → 拼接导出 MP3 |
| `recording_script.txt` | 录制自己声音作参考音频的提示稿 + 录制要求 |

## 用自己的声音克隆

1. 按 `recording_script.txt` 录一段 10–20 秒、干净无杂音的参考音频。
2. 在脚本里把参考音频路径指向你的录音,文字稿用录制稿原文(ICL 高保真)。
3. 长稿播报跑 `broadcast_tts.py`,输出 MP3 到 `audio_output/`(已 gitignore,不入库)。

## 注意

- 脚本中的路径目前为作者本机绝对路径,使用前按需调整 `MD` / `OUTDIR` / `MODEL_DIR`。
- 输出音频(`*.mp3`/`*.wav`)与 `audio_output/` 已在 `.gitignore` 中排除。
- ICL 模式偶有参考音频结尾"残留"泄漏;追求完全无泄漏可改用 `x_vector_only_mode=True`(纯音色,不需文字稿)。
