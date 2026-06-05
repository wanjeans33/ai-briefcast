#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为播报 MP3 配上小红书风格竖屏视频（9:16）。

设计遵循 open-design 的 `card-xiaohongshu` skill + 小红书设计系统 tokens：
  画布柔和、白卡圆角、单一品牌红 #ff2442 accent、PingFang/雅黑大字、大量留白、
  右下角水印；封面 → 每张一个观点 → 结尾 CTA。

因本机无 headless 浏览器 / ffmpeg，这里用 PIL 直接按 1080×1920 精确出图，
再用 PyAV 把多张卡片按音频时间轴拼成 mp4 并混入 MP3 音轨。

用法:
  python scripts/make_xhs_video.py \
      --audio audio_output/broadcast-2026-06-05-concise.mp3 \
      --out   audio_output/xhs-2026-06-05-concise.mp4
"""
from __future__ import annotations

import argparse
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FPS = 15

# ── 小红书 / RED 设计 tokens（取自 open-design design-systems/xiaohongshu）──
ACCENT = (255, 36, 66)          # #ff2442 品牌红，全局唯一强调色
INK = (38, 38, 40)              # 软黑标题
BODY = (70, 70, 74)             # 正文
MUTED = (140, 140, 146)         # 次要/水印
CARD = (255, 255, 255)          # 白卡
GRAD_TOP = (250, 233, 235)      # 顶部柔粉
GRAD_BOT = (244, 244, 245)      # 底部近白

FONT = "C:/Windows/Fonts/msyh.ttc"
FONT_BD = "C:/Windows/Fonts/msyhbd.ttc"


def f(sz, bold=False):
    return ImageFont.truetype(FONT_BD if bold else FONT, sz)


# ── 卡片内容（基于 2026-06-05 简洁版播报）────────────────────────────────
DATE = "2026-06-05"
WATERMARK = "@AI Briefcast · 6/5"
CARDS = [
    {"type": "cover", "kicker": "每日 AI 速览",
     "title": "今天 AI 圈\n发生了什么", "subtitle": "6 月 5 日 · 3 条头条 + 论文速递",
     "tag": "建议收藏"},
    {"type": "point", "kicker": "头条 01 · 行业", "title": "Google 的 AI 有点尴尬",
     "bullets": ["CEO 对外宣称 75% 代码已由 AI 写成",
                 "一线工程师却传梗图：被吹过头了",
                 "还在悄悄收购人类代码训模型，项目自标「机密」"]},
    {"type": "point", "kicker": "头条 02 · 教育 & 司法", "title": "AI 正冲击考场与法庭",
     "bullets": ["伯克利 CS10 挂科率飙到 35.3%（惯例 ≤ 7%）",
                 "教授归因：学生用大模型代写作业",
                 "法官头疼：AI 法律文件塞满编造的判例"]},
    {"type": "point", "kicker": "头条 03 · 前沿争议", "title": "Anthropic 对决科幻作家姜峯楠",
     "bullets": ["Claude 发布 84 页「宪法」，暗示 AI 或有意识",
                 "还想让 Claude「很快乐」、自主构建后继者",
                 "Ted Chiang：他们擅长的不是 AI，是拟人化",
                 "Claude 有意识吗？他只答：不，绝对不"]},
    {"type": "point", "kicker": "论文 · 搜索 Agent", "title": "上下文管理\n正比策略本身更关键",
     "bullets": ["策略身上「记账杂活」太多：候选池 / 证据 / 验证记录",
                 "三篇论文各拆一块，外置给环境或清出上下文",
                 "管好上下文窗口，正成为搜索 Agent 的胜负手"]},
    {"type": "cta", "title": "明天见", "subtitle": "每天一条 · AI 头条 + 论文速递",
     "tag": "关注 + 收藏，不错过明天"},
]
# 各卡时长（秒），按旁白节奏分配，最后一张兜到音频结尾
DURATIONS = [7, 28, 27, 28, 11, 4]


def gradient_bg():
    top = np.array(GRAD_TOP, dtype=np.float32)
    bot = np.array(GRAD_BOT, dtype=np.float32)
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    col = (top[None, :] * (1 - t) + bot[None, :] * t)  # H×3
    return np.repeat(col[:, None, :], W, axis=1).astype(np.uint8)


def wrap(draw, text, font, max_w):
    """按字符断行（中文无空格）。"""
    lines, cur = [], ""
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if draw.textlength(cur + ch, font=font) <= max_w:
            cur += ch
        else:
            lines.append(cur); cur = ch
    if cur:
        lines.append(cur)
    return lines


def draw_card(card, idx, total):
    img = Image.fromarray(gradient_bg())
    d = ImageDraw.Draw(img)

    # 白卡
    m = 60
    cx0, cy0, cx1, cy1 = m, m, W - m, H - m
    d.rounded_rectangle([cx0, cy0, cx1, cy1], radius=56, fill=CARD)
    pad = 84
    ix0, ix1 = cx0 + pad, cx1 - pad
    iw = ix1 - ix0

    # 顶部：页码
    d.text((ix1, cy0 + 64), f"{idx+1:02d} / {total:02d}", font=f(34), fill=MUTED, anchor="ra")

    if card["type"] == "cover":
        y = cy0 + 360
        # kicker 胶囊
        kf = f(40, True)
        kw = d.textlength(card["kicker"], font=kf)
        d.rounded_rectangle([ix0, y, ix0 + kw + 64, y + 84], radius=42, fill=ACCENT)
        d.text((ix0 + 32, y + 42), card["kicker"], font=kf, fill="white", anchor="lm")
        y += 84 + 80
        for ln in card["title"].split("\n"):
            d.text((ix0, y), ln, font=f(108, True), fill=INK)
            y += 132
        y += 36
        d.text((ix0, y), card["subtitle"], font=f(46), fill=BODY)
        y += 120
        d.text((ix0, y), "· " + card["tag"] + " ·", font=f(44, True), fill=ACCENT)

    elif card["type"] == "cta":
        y = cy0 + 520
        d.text((ix0, y), card["title"], font=f(140, True), fill=INK)
        y += 200
        d.text((ix0, y), card["subtitle"], font=f(50), fill=BODY)
        y += 140
        tf = f(50, True)
        tw = d.textlength(card["tag"], font=tf)
        d.rounded_rectangle([ix0, y, ix0 + tw + 80, y + 104], radius=52, fill=ACCENT)
        d.text((ix0 + 40, y + 52), card["tag"], font=tf, fill="white", anchor="lm")

    else:  # point
        y = cy0 + 150
        kf = f(38, True)
        kw = d.textlength(card["kicker"], font=kf)
        d.rounded_rectangle([ix0, y, ix0 + kw + 56, y + 76], radius=38, fill=(255, 236, 239))
        d.text((ix0 + 28, y + 38), card["kicker"], font=kf, fill=ACCENT, anchor="lm")
        y += 76 + 56
        for ln in wrap(d, card["title"], f(82, True), iw):
            d.text((ix0, y), ln, font=f(82, True), fill=INK)
            y += 104
        # accent 下划线
        y += 8
        d.rounded_rectangle([ix0, y, ix0 + 120, y + 10], radius=5, fill=ACCENT)
        y += 80
        bf = f(46)
        for b in card["bullets"]:
            d.ellipse([ix0, y + 18, ix0 + 18, y + 36], fill=ACCENT)
            for j, ln in enumerate(wrap(d, b, bf, iw - 56)):
                d.text((ix0 + 56, y), ln, font=bf, fill=BODY)
                y += 66
            y += 30

    # 水印
    d.text((ix1, cy1 - 56), WATERMARK, font=f(34), fill=MUTED, anchor="rs")
    return img


def build_video(cards, durs, audio_path, out_path):
    out = av.open(str(out_path), "w")
    v = out.add_stream("h264", rate=FPS)
    v.width, v.height, v.pix_fmt = W, H, "yuv420p"
    v.options = {"crf": "20", "preset": "medium"}

    inp = av.open(str(audio_path))
    ain = inp.streams.audio[0]
    a = out.add_stream("aac", rate=ain.rate)
    try:
        a.layout = ain.layout
    except Exception:
        pass

    pts = 0
    for img, dur in zip(cards, durs):
        arr = np.array(img.convert("RGB"))
        frame = av.VideoFrame.from_ndarray(arr, format="rgb24")
        for _ in range(max(1, round(dur * FPS))):
            frame.pts = pts
            pts += 1
            for pkt in v.encode(frame):
                out.mux(pkt)
    for pkt in v.encode():
        out.mux(pkt)

    resampler = av.audio.resampler.AudioResampler(format="fltp", layout=a.layout, rate=ain.rate)
    for fr in inp.decode(ain):
        for rf in resampler.resample(fr):
            rf.pts = None
            for pkt in a.encode(rf):
                out.mux(pkt)
    for pkt in a.encode():
        out.mux(pkt)

    inp.close()
    out.close()


def main():
    ap = argparse.ArgumentParser(description="把播报 MP3 配成小红书竖屏视频")
    ap.add_argument("--audio", default="audio_output/broadcast-2026-06-05-concise.mp3")
    ap.add_argument("--out", default="audio_output/xhs-2026-06-05-concise.mp4")
    args = ap.parse_args()

    audio = av.open(args.audio)
    total_s = audio.duration / 1_000_000.0
    audio.close()

    durs = list(DURATIONS)
    durs[-1] = max(2.0, total_s - sum(durs[:-1]))  # 最后一张兜到音频结尾
    print(f"[plan] 音频 {total_s:.1f}s -> {len(CARDS)} 张卡，时长分配 {['%.1f'%x for x in durs]}")

    imgs = []
    outdir = Path("assets/xhs_cards"); outdir.mkdir(parents=True, exist_ok=True)
    for i, c in enumerate(CARDS):
        im = draw_card(c, i, len(CARDS))
        im.save(outdir / f"card-{i+1}.png")
        imgs.append(im)
    print(f"[render] {len(imgs)} 张卡片 PNG -> {outdir}")

    build_video(imgs, durs, args.audio, args.out)
    sz = Path(args.out).stat().st_size
    print(f"[done] {args.out} ({sz/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
