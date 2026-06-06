#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书竖屏视频（HTML 版，数据驱动）——真·card-xiaohongshu skill 链路。

按 open-design card-xiaohongshu 的视觉签名（莫兰迪渐变 / 徽章 / 大标题 / 水印）
把一组卡片数据渲成 9:16 HTML → Playwright 无头 Chromium 高清截图
→ ffmpeg 交叉淡入淡出 + 混入 MP3 → MP4。

卡片数据可来自 generate_broadcast.make_cards()（LLM 生成）或 --cards JSON 文件。

用法:
  python scripts/make_xhs_video_html.py --cards cards.json \
      --audio audio_output/broadcast-2026-06-05-concise.mp3 \
      --out   audio_output/xhs-2026-06-05-concise.mp4
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import av
from playwright.sync_api import sync_playwright

FFMPEG = r"C:\Users\WANG-\ffmpeg\ffmpeg-8.1.1-essentials_build\bin\ffmpeg.exe"
XFADE = 0.7
WEIGHTS = [7, 28, 27, 28, 11, 5]   # 各卡相对旁白时长（权重），按音频总长等比缩放
GRADS = ["c1", "c2", "c3", "c4", "c5"]   # 莫兰迪渐变循环；cta 固定用暗色 c7

CSS = """
*{margin:0;box-sizing:border-box}
body{font-family:'Microsoft YaHei','Noto Sans SC','PingFang SC',sans-serif;-webkit-font-smoothing:antialiased}
.card{width:1080px;height:1920px;position:relative;padding:120px 88px;display:flex;flex-direction:column}
.c1{background:linear-gradient(160deg,#f7d2c2 0%,#f3a98a 100%);color:#3a1d10}
.c2{background:linear-gradient(160deg,#fff7e6 0%,#ffe4b8 100%);color:#3a2e10}
.c3{background:linear-gradient(160deg,#e8f0e3 0%,#bcd6b3 100%);color:#1f3a1f}
.c4{background:linear-gradient(160deg,#e7e8f5 0%,#bec1e8 100%);color:#1d1f4a}
.c5{background:linear-gradient(160deg,#fce7f0 0%,#f5b3ce 100%);color:#4a1b34}
.c7{background:linear-gradient(160deg,#15140f 0%,#3a2620 100%);color:#fafaf7}
.badge{display:inline-flex;align-items:center;gap:10px;padding:14px 30px;border-radius:999px;
       background:rgba(255,255,255,0.55);font-size:30px;font-weight:600;align-self:flex-start}
.kicker{display:inline-flex;padding:12px 26px;border-radius:999px;background:rgba(0,0,0,0.10);
        font-size:30px;font-weight:700;align-self:flex-start;margin-bottom:40px}
h2{font-size:96px;font-weight:900;line-height:1.08;letter-spacing:-0.01em;margin:0 0 40px}
.body{font-size:46px;font-weight:500;line-height:1.62;opacity:0.88;max-width:23ch}
.body strong{font-weight:800}
.hero{font-size:128px;font-weight:900;line-height:1.05;letter-spacing:-0.02em;margin:0}
.hl{color:#c0392b}
.c7 .hl{color:#e9b94a}
.label{font-size:38px;font-weight:600;opacity:0.7;margin-bottom:28px}
.c7 .label{color:#e9b94a;opacity:1}
.foot{font-size:36px;opacity:0.62;font-weight:500}
.mid{margin:auto 0}
.tags{display:flex;gap:20px;font-size:38px;font-weight:600}
.tags span{padding:18px 40px;border-radius:999px}
.tags .pri{background:#e9b94a;color:#15140f}
.tags .sec{background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.22)}
.watermark{position:absolute;bottom:60px;right:72px;font-size:28px;opacity:0.55;font-weight:500}
.pageno{position:absolute;top:64px;right:80px;font-size:30px;font-weight:600;opacity:0.45;letter-spacing:0.08em}
"""


def _bold(t: str) -> str:
    t = (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)


def _wrap(t: str, n: int) -> str:
    """按 ~n 字断行，尽量不切断连续的 ASCII 词。"""
    out, cur, run = [], "", ""
    for ch in (t or ""):
        cur += ch
        run = run + ch if (ch.isascii() and not ch.isspace()) else ""
        if len(cur) >= n and not run:
            out.append(cur.strip()); cur = ""
    if cur.strip():
        out.append(cur.strip())
    return "<br/>".join(out) or t


def _cls(i: int, n: int, kind: str) -> str:
    if kind == "cta":
        return "c7"
    if i == 0:
        return "c1"
    return GRADS[(i) % len(GRADS)]


def card_html(c, i, n, wm):
    kind = c.get("kind", "point")
    page = f'<div class="pageno">{i+1:02d} / {n:02d}</div>'
    water = f'<div class="watermark">{wm}</div>'
    cls = _cls(i, n, kind)
    if kind == "cover":
        inner = (f'<div class="badge">{c.get("badge","")}</div>'
                 f'<div class="mid"><div class="label">{c.get("subtitle","")}</div>'
                 f'<h2 class="hero">{_wrap(c.get("title",""), 6)}</h2></div>'
                 f'<div class="foot">滑动看 →</div>')
    elif kind == "cta":
        tags = c.get("tags", ["关注", "收藏", "分享"])
        tagsdiv = ('<div class="tags">'
                   + "".join(f'<span class="{"pri" if k==0 else "sec"}">{t}</span>'
                             for k, t in enumerate(tags)) + "</div>")
        inner = (f'<div class="mid"><div class="label">看完别走 ✨</div>'
                 f'<h2 class="hero">{_wrap(c.get("title","明天见"), 6)}</h2>'
                 f'<div class="label" style="margin-top:32px;opacity:.8">{c.get("subtitle","")}</div></div>'
                 f'{tagsdiv}')
    else:
        inner = (f'<div class="kicker">{c.get("tag","")}</div>'
                 f'<h2>{_wrap(c.get("title",""), 8)}</h2>'
                 f'<p class="body">{_bold(c.get("body",""))}</p>')
    return f'<div class="card {cls}" id="card{i}">{page}{inner}{water}</div>'


def render_cards(cards, outdir: Path, wm: str):
    n = len(cards)
    html = ("<!DOCTYPE html><html lang=zh-CN><head><meta charset=UTF-8><style>"
            + CSS + "</style></head><body>"
            + "".join(card_html(c, i, n, wm) for i, c in enumerate(cards))
            + "</body></html>")
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        pg.set_content(html, wait_until="load")
        pg.wait_for_timeout(400)
        for i in range(n):
            fp = outdir / f"card-{i+1}.png"
            pg.query_selector(f"#card{i}").screenshot(path=str(fp))
            paths.append(fp)
        b.close()
    return paths


def composite(pngs, durs, audio, out):
    n = len(pngs)
    cmd = [FFMPEG, "-y"]
    for p, d in zip(pngs, durs):
        cmd += ["-loop", "1", "-t", f"{d}", "-i", str(p)]
    cmd += ["-i", str(audio)]
    parts = [f"[{i}:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[v{i}]" for i in range(n)]
    chain, prev, cum = "", "[v0]", 0.0
    for j in range(1, n):
        cum += durs[j - 1]
        off = cum - j * XFADE
        lbl = "[vout]" if j == n - 1 else f"[x{j}]"
        chain += f"{prev}[v{j}]xfade=transition=fade:duration={XFADE}:offset={off:.3f}{lbl};"
        prev = lbl
    filt = ";".join(parts) + ";" + chain.rstrip(";")
    cmd += ["-filter_complex", filt, "-map", "[vout]", "-map", f"{n}:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k", "-shortest", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ffmpeg failed:\n" + r.stderr[-1500:])


def build_xhs_video(cards, audio_path, out_path, date=None,
                    cards_dir="assets/xhs_cards_html", seg_durations=None):
    """渲染卡片 + 合成视频。cards 为 dict 列表。返回输出路径。

    seg_durations: 每张卡对应那段旁白的真实时长（秒）。给定时按它精确卡点——
    每张卡停留 = 该段旁白时长，交叉淡变恰好从该段结束处开始；否则按 WEIGHTS 估算。
    """
    wm = "@AI Briefcast"
    if date:
        m = re.match(r"\d{4}-(\d{2})-(\d{2})", date)
        if m:
            wm = f"@AI Briefcast · {int(m.group(1))}/{int(m.group(2))}"
    n = len(cards)
    if seg_durations and len(seg_durations) == n:
        durs = [d + XFADE for d in seg_durations]   # 卡点：每次淡变从该段结束处起
    else:
        a = av.open(str(audio_path)); alen = a.duration / 1e6; a.close()
        weights = (WEIGHTS if n == len(WEIGHTS) else [1] * n)
        total = alen + (n - 1) * XFADE
        durs = [w / sum(weights) * total for w in weights]
    pngs = render_cards(cards, Path(cards_dir), wm)
    composite(pngs, durs, audio_path, out_path)
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cards", help="卡片 JSON 文件（{\"cards\":[...]} 或 [...]）")
    ap.add_argument("--audio", default="audio_output/broadcast-2026-06-05-concise.mp3")
    ap.add_argument("--out", default="audio_output/xhs-2026-06-05-concise.mp4")
    ap.add_argument("--date", default="2026-06-05")
    args = ap.parse_args()
    if not args.cards:
        raise SystemExit("请用 --cards 传入卡片 JSON（或经 run_daily 自动生成）")
    data = json.loads(Path(args.cards).read_text(encoding="utf-8"))
    cards = data["cards"] if isinstance(data, dict) else data
    print(f"[plan] {len(cards)} 张卡 + {args.audio}")
    build_xhs_video(cards, args.audio, args.out, date=args.date)
    print(f"[done] {args.out} ({Path(args.out).stat().st_size/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
