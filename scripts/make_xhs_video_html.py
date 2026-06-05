#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书竖屏视频（HTML 版）——真·card-xiaohongshu skill 链路。

流程：按 open-design card-xiaohongshu 的 HTML/CSS 视觉签名生成 9:16 卡片
（莫兰迪渐变、大号衬线序号、粗标题、徽章、水印）→ Playwright 无头 Chromium
逐张高清截图 → ffmpeg 交叉淡入淡出拼接 + 混入 MP3 → MP4。

用法:
  python scripts/make_xhs_video_html.py \
      --audio audio_output/broadcast-2026-06-05-concise.mp3 \
      --out   audio_output/xhs-2026-06-05-concise-html.mp4
"""
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

import av
from playwright.sync_api import sync_playwright

FFMPEG = r"C:\Users\WANG-\ffmpeg\ffmpeg-8.1.1-essentials_build\bin\ffmpeg.exe"
WM = "@AI Briefcast · 6/5"

# 每张卡：渐变类 + 内容。point 用大号序号；cover/cta 用 hero。
CARDS = [
    {"cls": "c1", "kind": "cover", "badge": "⚡ 建议收藏 · 每日 AI 速览",
     "label": "AI 头条 + 论文速递", "hero": '今天 AI 圈<br/>发生了<br/><span class="hl">什么</span>',
     "foot": "滑动看 →"},
    {"cls": "c2", "kind": "point", "num": "01",
     "title": "Google 的 AI<br/>有点尴尬",
     "body": "CEO 对外宣称 <strong>75% 代码已由 AI 写成</strong>，"
             "一线工程师却传梗图吐槽<strong>被吹过头了</strong>。<br/><br/>"
             "更讽刺的是，Google 还在悄悄收购人类代码训模型 —— 项目自标「机密」。"},
    {"cls": "c3", "kind": "point", "num": "02",
     "title": "AI 冲击<br/>考场与法庭",
     "body": "伯克利 CS10 挂科率飙到 <strong>35.3%</strong>（惯例 ≤ 7%），"
             "教授归因学生<strong>用大模型代写作业</strong>。<br/><br/>"
             "法庭同样头疼：AI 生成的法律文件塞满<strong>编造的判例</strong>。"},
    {"cls": "c4", "kind": "point", "num": "03",
     "title": "Anthropic<br/>对决姜峯楠",
     "body": "Claude 发布 <strong>84 页「宪法」</strong>，暗示 AI 或有意识，"
             "还想让它「很快乐」、自主构建后继者。<br/><br/>"
             "Ted Chiang 泼冷水：他们擅长的不是 AI，<strong>是拟人化</strong>。"
             "Claude 有意识吗？「不，绝对不」。"},
    {"cls": "c5", "kind": "point", "num": "论文",
     "title": "上下文管理<br/>比策略更关键",
     "body": "今天多篇搜索 Agent 论文指向同一处：策略身上<strong>记账杂活太多</strong>"
             " —— 候选池 / 证据链接 / 验证记录。<br/><br/>"
             "三篇各拆一块，<strong>外置给环境或清出上下文</strong>。"},
    {"cls": "c7", "kind": "cta", "label": "看完别走 ✨",
     "hero": '工具不在多，<br/><span class="hl">每天看一条</span><br/>才跟得上。',
     "tags": ["关注", "收藏", "分享"]},
]
WEIGHTS = [7, 28, 27, 28, 11, 5]   # 各卡相对旁白时长（权重），按音频总长等比缩放
XFADE = 0.7

CSS = """
*{margin:0;box-sizing:border-box}
body{font-family:'Microsoft YaHei','Noto Sans SC','PingFang SC',sans-serif;-webkit-font-smoothing:antialiased}
.card{width:1080px;height:1920px;border-radius:0;overflow:hidden;position:relative;
      padding:120px 88px;display:flex;flex-direction:column}
.c1{background:linear-gradient(160deg,#f7d2c2 0%,#f3a98a 100%);color:#3a1d10}
.c2{background:linear-gradient(160deg,#fff7e6 0%,#ffe4b8 100%);color:#3a2e10}
.c3{background:linear-gradient(160deg,#e8f0e3 0%,#bcd6b3 100%);color:#1f3a1f}
.c4{background:linear-gradient(160deg,#e7e8f5 0%,#bec1e8 100%);color:#1d1f4a}
.c5{background:linear-gradient(160deg,#fce7f0 0%,#f5b3ce 100%);color:#4a1b34}
.c7{background:linear-gradient(160deg,#15140f 0%,#3a2620 100%);color:#fafaf7}
.badge{display:inline-flex;align-items:center;gap:10px;padding:14px 28px;border-radius:999px;
       background:rgba(255,255,255,0.55);font-size:30px;font-weight:600;align-self:flex-start}
.num{font-family:Georgia,serif;font-style:italic;font-size:200px;font-weight:700;line-height:0.9;opacity:0.85;margin-bottom:36px}
.numzh{font-size:120px;font-weight:900;line-height:0.95;opacity:0.85;margin-bottom:28px}
h2{font-size:96px;font-weight:900;line-height:1.08;letter-spacing:-0.01em;margin:0 0 44px}
.body{font-size:46px;font-weight:500;line-height:1.6;opacity:0.86;max-width:22ch}
.body strong{font-weight:800}
.hero{font-size:128px;font-weight:900;line-height:1.04;letter-spacing:-0.02em;margin:0}
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
.pageno{position:absolute;top:64px;right:80px;font-family:Inter,sans-serif;font-size:30px;font-weight:600;opacity:0.45;letter-spacing:0.08em}
"""


def card_html(c, i, n):
    page = f'<div class="pageno">{i+1:02d} / {n:02d}</div>'
    wm = f'<div class="watermark">{WM}</div>'
    if c["kind"] == "cover":
        inner = (f'<div class="badge">{c["badge"]}</div>'
                 f'<div class="mid"><div class="label">{c["label"]}</div>'
                 f'<h2 class="hero">{c["hero"]}</h2></div>'
                 f'<div class="foot">{c["foot"]}</div>')
    elif c["kind"] == "cta":
        tags = ('<div class="tags">'
                + ''.join(f'<span class="{"pri" if k==0 else "sec"}">{t}</span>'
                          for k, t in enumerate(c["tags"])) + '</div>')
        inner = (f'<div class="mid"><div class="label">{c["label"]}</div>'
                 f'<h2 class="hero">{c["hero"]}</h2></div>{tags}')
    else:
        numcls = "numzh" if not c["num"].isdigit() else "num"
        inner = (f'<div class="{numcls}">{c["num"]}</div>'
                 f'<h2>{c["title"]}</h2><p class="body">{c["body"]}</p>')
    return f'<div class="card {c["cls"]}" id="card{i}">{page}{inner}{wm}</div>'


def render_cards(outdir: Path):
    n = len(CARDS)
    cards = "".join(card_html(c, i, n) for i, c in enumerate(CARDS))
    html = f"<!DOCTYPE html><html lang=zh-CN><head><meta charset=UTF-8><style>{CSS}</style></head><body>{cards}</body></html>"
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


def build_video(pngs, durs, audio, out):
    n = len(pngs)
    cmd = [FFMPEG, "-y"]
    for p, d in zip(pngs, durs):
        cmd += ["-loop", "1", "-t", f"{d}", "-i", str(p)]
    cmd += ["-i", str(audio)]

    parts, labels = [], []
    for i in range(n):
        parts.append(f"[{i}:v]scale=1080:1920,setsar=1,fps=30,format=yuv420p[v{i}]")
        labels.append(f"[v{i}]")
    chain, prev, cum = "", labels[0], 0.0
    for j in range(1, n):
        cum += durs[j - 1]
        off = cum - j * XFADE
        out_lbl = "[vout]" if j == n - 1 else f"[x{j}]"
        chain += f"{prev}{labels[j]}xfade=transition=fade:duration={XFADE}:offset={off:.3f}{out_lbl};"
        prev = out_lbl
    filt = ";".join(parts) + ";" + chain.rstrip(";")

    cmd += ["-filter_complex", filt, "-map", "[vout]", "-map", f"{n}:a",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k", "-shortest", str(out)]
    print("[ffmpeg] compositing", n, "cards with xfade ...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ffmpeg failed:\n" + r.stderr[-1500:])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", default="audio_output/broadcast-2026-06-05-concise.mp3")
    ap.add_argument("--out", default="audio_output/xhs-2026-06-05-concise-html.mp4")
    args = ap.parse_args()

    a = av.open(args.audio); alen = a.duration / 1e6; a.close()
    total = alen + (len(CARDS) - 1) * XFADE   # xfade 会吃掉重叠，补回来让成片≈音频
    s = sum(WEIGHTS)
    durs = [w / s * total for w in WEIGHTS]
    print(f"[plan] 音频 {alen:.1f}s, xfade {XFADE}s, 时长 {['%.1f'%d for d in durs]}")

    pngs = render_cards(Path("assets/xhs_cards_html"))
    print(f"[render] {len(pngs)} 张 HTML 卡片 -> assets/xhs_cards_html")
    build_video(pngs, durs, args.audio, args.out)
    print(f"[done] {args.out} ({Path(args.out).stat().st_size/1e6:.2f} MB)")


if __name__ == "__main__":
    main()
