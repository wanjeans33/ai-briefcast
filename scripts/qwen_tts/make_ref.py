# -*- coding: utf-8 -*-
"""从一段录音(.m4a/.wav)按静音切分，导出指定段作为音色克隆参考 wav。

用法:
  python make_ref.py <输入音频> <输出wav> [段号(从1起,默认3)]
不依赖 ffmpeg，用 PyAV 解码。会打印各段的 起止/时长/峰值 供核对。
"""
import sys
import numpy as np
import av
import soundfile as sf

SR = 24000


def decode_mono(path: str, sr: int = SR) -> np.ndarray:
    container = av.open(path)
    stream = container.streams.audio[0]
    resampler = av.AudioResampler(format="flt", layout="mono", rate=sr)
    chunks = []
    for frame in container.decode(stream):
        frame.pts = None
        for rf in resampler.resample(frame):
            chunks.append(rf.to_ndarray().reshape(-1))
    container.close()
    return np.concatenate(chunks).astype(np.float32) if chunks else np.zeros(0, np.float32)


def split_on_silence(audio, sr, win=0.02, sil_thresh=0.02, min_gap=0.30, min_len=0.6):
    n = int(win * sr)
    if n <= 0:
        return []
    frames = len(audio) // n
    rms = np.array([np.sqrt(np.mean(audio[i * n:(i + 1) * n] ** 2) + 1e-12)
                    for i in range(frames)])
    voiced = rms > (sil_thresh * max(rms.max(), 1e-6) / sil_thresh if False else sil_thresh)
    # 用绝对阈值 sil_thresh
    voiced = rms > sil_thresh
    segs = []
    i = 0
    gap_frames = int(min_gap / win)
    while i < frames:
        if voiced[i]:
            j = i
            silent_run = 0
            while j < frames and (voiced[j] or silent_run < gap_frames):
                silent_run = 0 if voiced[j] else silent_run + 1
                j += 1
            start, end = i * n, min(len(audio), j * n)
            if (end - start) / sr >= min_len:
                segs.append((start, end))
            i = j
        else:
            i += 1
    return segs


def main():
    inp = sys.argv[1]
    out = sys.argv[2]
    idx = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    audio = decode_mono(inp)
    print(f"输入 {inp}: 总时长 {len(audio) / SR:.2f}s, 峰值 {np.abs(audio).max():.3f}")
    segs = split_on_silence(audio, SR)
    for k, (s, e) in enumerate(segs, 1):
        clip = audio[s:e]
        print(f"  段{k}: {s/SR:6.2f}–{e/SR:6.2f}s  时长 {(e-s)/SR:5.2f}s  峰值 {np.abs(clip).max():.3f}")
    if not segs:
        sys.exit("未切出任何语音段，请调阈值。")
    if idx < 1 or idx > len(segs):
        print(f"段号 {idx} 越界，改用最后一段。")
        idx = len(segs)
    s, e = segs[idx - 1]
    clip = audio[s:e]
    sf.write(out, clip, SR)
    print(f"已导出 段{idx}（{(e-s)/SR:.2f}s, 峰值 {np.abs(clip).max():.3f}）→ {out}")


if __name__ == "__main__":
    main()
