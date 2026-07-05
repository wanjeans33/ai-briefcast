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
import shutil
import subprocess
from pathlib import Path

import av
from playwright.sync_api import sync_playwright

FFMPEG = r"C:\Users\WANG-\ffmpeg\ffmpeg-8.1.1-essentials_build\bin\ffmpeg.exe"
OUT_W, OUT_H = 2160, 3840   # 输出 4K 竖屏 9:16（卡片本就 2160×3840，零放大）
XFADE = 0.7
WEIGHTS = [7, 28, 27, 28, 11, 5]   # 各卡相对旁白时长（权重），按音频总长等比缩放
GRADS = ["c1", "c2", "c3", "c4", "c5"]   # 莫兰迪渐变循环；cta 固定用暗色 c7

CSS = """
*{margin:0;box-sizing:border-box}
body{font-family:'Microsoft YaHei','Noto Sans SC','PingFang SC',sans-serif;-webkit-font-smoothing:antialiased}
.card{width:1080px;height:1920px;position:relative;padding:104px 84px 96px;display:flex;
      flex-direction:column;overflow:hidden;
      background:linear-gradient(160deg,var(--g1) 0%,var(--g2) 100%);color:var(--fg)}
.c1{--g1:#f7d2c2;--g2:#f3a98a;--fg:#3a1d10;--acc:#d6431f}
.c2{--g1:#fff7e6;--g2:#ffe2b0;--fg:#3a2e10;--acc:#c07d00}
.c3{--g1:#e8f0e3;--g2:#b7d3ad;--fg:#1f3a1f;--acc:#2c8a48}
.c4{--g1:#e7e8f5;--g2:#bbbfe8;--fg:#1d1f4a;--acc:#4147c4}
.c5{--g1:#fce7f0;--g2:#f3aecb;--fg:#4a1b34;--acc:#c0397a}
.c7{--g1:#15140f;--g2:#3a2620;--fg:#fafaf7;--acc:#e9b94a}
.bignum{position:absolute;top:-78px;right:-18px;font-size:580px;font-weight:900;line-height:1;
        color:var(--acc);opacity:0.12;letter-spacing:-0.05em;z-index:0;font-style:italic}
.dots{display:flex;gap:14px;z-index:2}
.dots i{width:20px;height:20px;border-radius:999px;background:var(--fg);opacity:0.2}
.dots i.on{opacity:1;background:var(--acc);width:56px}
.head{display:flex;align-items:center;gap:26px;margin-top:62px;z-index:2}
.ico{width:108px;height:108px;border-radius:30px;display:flex;align-items:center;justify-content:center;
     font-size:60px;background:rgba(255,255,255,0.6);box-shadow:0 10px 28px rgba(0,0,0,0.10)}
.kicker{font-size:34px;font-weight:800;letter-spacing:0.02em;padding:16px 34px;border-radius:999px;
        background:var(--acc);color:#fff}
h2{font-size:104px;font-weight:900;line-height:1.06;letter-spacing:-0.01em;margin:50px 0 44px;z-index:2}
.body{font-size:50px;font-weight:500;line-height:1.58;z-index:2;padding-left:38px;
      border-left:10px solid var(--acc);max-width:25ch}
.hl{font-weight:800;background:var(--acc);color:#fff;padding:3px 16px;border-radius:14px;
    -webkit-box-decoration-break:clone;box-decoration-break:clone}
.punch{margin-top:auto;font-size:58px;font-weight:800;line-height:1.32;z-index:2;
       padding-top:46px;border-top:4px solid rgba(0,0,0,0.14)}
.punch .q{color:var(--acc);font-weight:900}
.watermark{position:absolute;bottom:52px;right:72px;font-size:28px;opacity:0.5;font-weight:600;z-index:2}
/* 名词解释卡（与父新闻同色分组，但更柔和、带书签角标） */
.exp{padding-top:104px}
.exp::before{content:"";position:absolute;inset:0;background:rgba(255,255,255,0.34);z-index:0}
.exp>*{position:relative}
.bookmark{position:absolute;top:-30px;right:18px;font-size:300px;opacity:0.14;z-index:0;
          transform:rotate(8deg)}
.expmid{margin:auto 0;z-index:2;display:flex;flex-direction:column;align-items:flex-start}
.kicker.out{background:transparent;color:var(--acc);border:4px solid var(--acc);
            display:inline-flex}
.exptitle{font-size:90px;margin:46px 0 40px}
.body.soft{font-weight:500;line-height:1.62}
.reltag{margin-top:48px;font-size:34px;font-weight:700;opacity:0.78;
        padding:16px 32px;border-radius:999px;background:rgba(0,0,0,0.08)}
/* 封面（目录钩子） */
.brand{align-self:flex-start;padding:18px 38px;border-radius:999px;background:var(--acc);color:#fff;
       font-size:32px;font-weight:800;margin-top:44px;z-index:2}
.coverhead{margin-top:104px;z-index:2}
.coverhead .sub{font-size:42px;font-weight:700;opacity:0.7}
.coverhead .big{font-size:142px;font-weight:900;line-height:1.0;margin-top:16px;letter-spacing:-0.02em}
.coverhead .big em{color:var(--acc);font-style:normal}
.toc{margin-top:78px;display:flex;flex-direction:column;gap:36px;z-index:2}
.toc .row{display:flex;align-items:flex-start;gap:28px;font-size:48px;font-weight:600;line-height:1.25}
.toc .num{flex:none;width:66px;height:66px;border-radius:18px;background:var(--acc);color:#fff;
          font-size:36px;font-weight:900;display:flex;align-items:center;justify-content:center}
.swipe{margin-top:auto;font-size:40px;font-weight:700;opacity:0.65;z-index:2}
/* 结尾 CTA */
.cta-wrap{margin:auto 0;z-index:2}
.cta-kick{font-size:42px;font-weight:800;color:var(--acc);margin-bottom:28px}
.cta-title{font-size:152px;font-weight:900;line-height:1.0;letter-spacing:-0.02em}
.cta-sub{font-size:48px;font-weight:600;opacity:0.85;margin-top:38px}
.tags{display:flex;gap:22px;font-size:40px;font-weight:700;z-index:2;margin-top:64px}
.tags span{padding:22px 46px;border-radius:999px}
.tags .pri{background:var(--acc);color:#15140f}
.tags .sec{background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.28)}
"""

# 分类大图标（C）：先看显式 icon 字段，否则按关键词推断
ICON_MAP = [
    (("安全", "防", "注入", "隐私", "对齐", "攻击"), "🛡️"),
    (("资本", "股", "上市", "IPO", "标普", "投资", "估值", "融资"), "📈"),
    (("机器人", "具身", "Robot"), "🤖"),
    (("芯片", "算力", "显存", "GPU", "加速", "量化"), "⚡"),
    (("论文", "模型", "架构", "推理", "全模态", "训练", "研究"), "🧪"),
    (("苹果", "Apple", "Siri", "手机", "硬件", "产品"), "📱"),
    (("行业", "发布", "公司"), "🏢"),
]


def _icon(c) -> str:
    if c.get("icon"):
        return c["icon"]
    s = (c.get("tag", "") + c.get("title", "") + c.get("body", ""))
    for keys, ic in ICON_MAP:
        if any(k in s for k in keys):
            return ic
    return "📰"


def _hl(t: str) -> str:
    """**关键词** → 高亮色块（B）。"""
    t = (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r'<span class="hl">\1</span>', t)


def _idx(c, fallback: int) -> str:
    """从 tag 里取序号（头条 02 → 02），无则用 fallback。"""
    m = re.search(r"\d+", c.get("tag", ""))
    return f"{int(m.group(0)) if m else fallback:02d}"


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


def _cls(i: int, n: int, kind: str, grad: str | None = None) -> str:
    if grad:                      # 显式指定配色（解释卡跟父新闻同色分组）
        return grad
    if kind == "cta":
        return "c7"
    if i == 0:
        return "c1"
    return GRADS[(i) % len(GRADS)]


def card_html(c, i, n, wm):
    kind = c.get("kind", "point")
    water = f'<div class="watermark">{wm}</div>'
    dots = ('<div class="dots">'
            + "".join(f'<i class="{"on" if k == i else ""}"></i>' for k in range(n))
            + "</div>")
    cls = _cls(i, n, kind, c.get("grad"))

    if kind == "explainer":
        big = f'<div class="bookmark">{c.get("icon", "📖")}</div>'
        rel = c.get("rel", "")
        reltag = f'<div class="reltag">↑ 关联：{rel}</div>' if rel else ""
        inner = (f'<div class="expmid">'
                 f'<div class="kicker out">信息补充</div>'
                 f'<h2 class="exptitle">{_wrap(c.get("title",""), 9)}</h2>'
                 f'<div class="body soft">{_hl(c.get("body",""))}</div>'
                 f'{reltag}</div>')
        return f'<div class="card {cls} exp" id="card{i}">{dots}{big}{inner}{water}</div>'

    if kind == "cover":
        toc = c.get("toc") or []
        rows = "".join(
            f'<div class="row"><span class="num">{k+1}</span>'
            f'<span>{_wrap(t, 13)}</span></div>' for k, t in enumerate(toc))
        cnt = c.get("count") or (len(toc) if toc else 3)
        hook = c.get("hook")  # 头条大字钩子；给定时大字＝钩子，「今日N条要闻」降为副行
        sub = c.get("subtitle", "")
        if hook:
            sub = (sub + " · 今日 " + str(cnt) + " 条要闻").strip(" ·")
            bigline = f'<div class="big">{hook}</div>'
        else:
            bigline = f'<div class="big">今日 <em>{cnt}</em> 条要闻</div>'
        inner = (f'<div class="brand">{c.get("badge","每日AI速览")}</div>'
                 f'<div class="coverhead"><div class="sub">{sub}</div>'
                 f'{bigline}</div>'
                 f'<div class="toc">{rows}</div>')
        return f'<div class="card {cls}" id="card{i}">{dots}{inner}{water}</div>'

    if kind == "cta":
        tags = c.get("tags", ["关注", "收藏", "分享"])
        tg = ('<div class="tags">'
              + "".join(f'<span class="{"pri" if k==0 else "sec"}">{t}</span>'
                        for k, t in enumerate(tags)) + "</div>")
        inner = (f'<div class="cta-wrap"><div class="cta-kick">看完别走 ✨</div>'
                 f'<div class="cta-title">{_wrap(c.get("title","明天见"), 6)}</div>'
                 f'<div class="cta-sub">{c.get("subtitle","")}</div></div>{tg}')
        return f'<div class="card {cls}" id="card{i}">{dots}{inner}{water}</div>'

    # point
    big = f'<div class="bignum">{_idx(c, i)}</div>'
    punch = c.get("punch", "")
    punchdiv = (f'<div class="punch"><span class="q">「</span>{_hl(punch)}'
                f'<span class="q">」</span></div>') if punch else ""
    inner = (f'<div class="head"><div class="ico">{_icon(c)}</div>'
             f'<div class="kicker">{c.get("tag","")}</div></div>'
             f'<h2>{_wrap(c.get("title",""), 8)}</h2>'
             f'<div class="body">{_hl(c.get("body",""))}</div>'
             f'{punchdiv}')
    return f'<div class="card {cls}" id="card{i}">{dots}{big}{inner}{water}</div>'


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
    parts = [f"[{i}:v]scale={OUT_W}:{OUT_H},setsar=1,fps=30,format=yuv420p[v{i}]" for i in range(n)]
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


def prepend_intro(intro_path, main_path, out_path):
    """把片头视频拼到主视频前面，统一到 OUT_W×OUT_H / 30fps / 44100 立体声。

    片头若非 9:16（如 1:1），用「模糊放大铺底 + 居中原图」适配竖屏，不留死黑边。
    片头自带的音频（背景音乐）原样保留，主视频旁白接在其后。
    """
    filt = (
        f"[0:v]split=2[i0][i1];"
        f"[i0]scale={OUT_W}:{OUT_H}:force_original_aspect_ratio=increase,"
        f"crop={OUT_W}:{OUT_H},boxblur=42:1[bg];"
        f"[i1]scale={OUT_W}:-2[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30,format=yuv420p[iv];"
        f"[0:a]aresample=44100,aformat=channel_layouts=stereo[ia];"
        f"[1:v]scale={OUT_W}:{OUT_H},setsar=1,fps=30,format=yuv420p[mv];"
        f"[1:a]aresample=44100,aformat=channel_layouts=stereo[ma];"
        f"[iv][ia][mv][ma]concat=n=2:v=1:a=1[v][a]"
    )
    cmd = [FFMPEG, "-y", "-i", str(intro_path), "-i", str(main_path),
           "-filter_complex", filt, "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
           "-c:a", "aac", "-b:a", "128k", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ffmpeg intro concat failed:\n" + r.stderr[-1500:])
    return out_path


# --------------------------------------------------------------------------- #
# 片尾：品牌圆形照片缩放消失（替代/补充片头）
# --------------------------------------------------------------------------- #
def circle_photo(src, diameter, cx_frac=0.30, cy_frac=0.57, r_frac=0.32):
    """把一张照片裁成圆形 RGBA（自动按中心+半径裁方再套圆罩）。

    cx_frac/cy_frac 圆心在原图的相对位置，r_frac 半径占短边比例（会自动夹到边界内）。
    默认值适配 片头/图片_20260606072137.png 那只猫（头在左中，半径足够含住整头）。
    """
    from PIL import Image, ImageDraw
    img = Image.open(src).convert("RGB")
    W, H = img.size
    cx, cy = int(cx_frac * W), int(cy_frac * H)
    r = min(int(r_frac * min(W, H)), cx, W - cx, cy, H - cy)
    crop = img.crop((cx - r, cy - r, cx + r, cy + r)).resize((diameter, diameter), Image.LANCZOS).convert("RGBA")
    m = Image.new("L", (diameter, diameter), 0)
    ImageDraw.Draw(m).ellipse((0, 0, diameter, diameter), fill=255)
    crop.putalpha(m)
    return crop


def place_photo_on_card(card_png, photo_rgba, center):
    """把圆形照片合到某张卡片 PNG 上（原地覆盖）。center=(x,y) 为照片中心像素。"""
    from PIL import Image
    base = Image.open(card_png).convert("RGBA")
    d = photo_rgba.width
    base.alpha_composite(photo_rgba, (center[0] - d // 2, center[1] - d // 2))
    base.convert("RGB").save(card_png)


def build_shrink_outro(bg_png, photo_rgba, center, out_clip, dur=1.0, fps=30):
    """1 秒片尾：在 bg_png 背景上，圆形照片从满 → 0 原地缩小消失（静音）。"""
    from PIL import Image
    bg = Image.open(bg_png).convert("RGBA")
    d = photo_rgba.width
    n = max(2, int(dur * fps))
    fdir = Path(out_clip).with_suffix("")
    fdir = fdir.parent / ("_frames_" + fdir.name)
    if fdir.exists():
        shutil.rmtree(fdir)
    fdir.mkdir(parents=True)
    for i in range(n):
        s = 1 - i / (n - 1)
        fr = bg.copy()
        sz = int(d * s)
        if sz >= 2:
            c = photo_rgba.resize((sz, sz), Image.LANCZOS)
            fr.alpha_composite(c, (center[0] - sz // 2, center[1] - sz // 2))
        fr.convert("RGB").save(fdir / f"f{i:03d}.png")
    cmd = [FFMPEG, "-y", "-framerate", str(fps), "-i", str(fdir / "f%03d.png"),
           "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=44100:cl=stereo",
           "-vf", f"scale={OUT_W}:{OUT_H},format=yuv420p", "-c:v", "libx264",
           "-pix_fmt", "yuv420p", "-crf", "20", "-c:a", "aac", "-b:a", "128k",
           "-shortest", str(out_clip)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    shutil.rmtree(fdir)
    if r.returncode != 0:
        raise SystemExit("outro failed:\n" + r.stderr[-1200:])
    return out_clip


def concat_clips(clips, out_path):
    """顺序拼接多个同尺寸视频（统一 30fps / 44100 立体声）。"""
    n = len(clips)
    cmd = [FFMPEG, "-y"]
    for c in clips:
        cmd += ["-i", str(c)]
    parts = ";".join(
        f"[{i}:v]fps=30,format=yuv420p[v{i}];"
        f"[{i}:a]aresample=44100,aformat=channel_layouts=stereo[a{i}]" for i in range(n))
    seq = "".join(f"[v{i}][a{i}]" for i in range(n))
    filt = parts + ";" + seq + f"concat=n={n}:v=1:a=1[v][a]"
    cmd += ["-filter_complex", filt, "-map", "[v]", "-map", "[a]",
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
            "-c:a", "aac", "-b:a", "128k", str(out_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("concat failed:\n" + r.stderr[-1200:])
    return out_path


# --------------------------------------------------------------------------- #
# 字幕：脚本原文 + faster-whisper 词级时间戳强制对齐 → ASS → 烧进视频
# 用脚本原文（不用 ASR 文本），避免 Nex/Qwen/CODA-BENCH 等专有名词被转错。
# --------------------------------------------------------------------------- #
SUB_FONT = "Microsoft YaHei"
SUB_FONTSIZE = 96            # 字幕字号（2160 宽空间内）；6/19 起放大 78→96 更醒目
SUB_MARGINV = 820            # 字幕条距底边像素（约 78% 高度，落在正文与金句之间的空白带）
SUB_MAXLEN = 18            # 每行最多“全宽字”（英文/数字/空格按半宽计），在标点处断，绝不切词；放大字号后 22→18 防溢出
SUB_STRONG = set("。！？")  # 句末：必收行
SUB_BREAK_AFTER = set("的了地得和与及或在把对为到从让被并而且也就还又再，、；：")  # 长子句兜底断点


def _sub_spoken(s):
    """只数会被读出的字符（中日韩 + 字母数字），忽略标点空格。"""
    return [c for c in s if c.isalnum()]


def _sub_w(s):
    """显示宽度：全宽中文＝1，英文/数字/空格＝0.5。按视觉宽度而非字数断行。"""
    return sum(0.5 if c.isascii() else 1.0 for c in s)


def _wrap_clause(s, maxlen):
    """单个超宽子句（无内部标点可断）在自然处折：优先助词/连词后，绝不切开英文/数字 token。"""
    out = []
    while _sub_w(s) > maxlen:
        cum, idx = 0.0, len(s)
        for i, ch in enumerate(s):                       # 找累计宽度刚超 maxlen 的位置
            cum += 0.5 if ch.isascii() else 1.0
            if cum > maxlen:
                idx = i
                break
        found = None
        for i in range(idx, max(1, idx - 8) - 1, -1):    # 向左找“可断点之后”
            if i < len(s) and s[i - 1] in SUB_BREAK_AFTER:
                found = i
                break
        if found is None:                                # 没好断点：退到 idx，但别切断英数 token
            cut = idx
            while 1 < cut < len(s) and s[cut - 1].isascii() and s[cut - 1].isalnum() \
                    and s[cut].isascii() and s[cut].isalnum():
                cut -= 1
            found = max(1, cut)
        out.append(s[:found].strip())
        s = s[found:].strip()
    if s:
        out.append(s)
    return out


def subtitle_lines(segments, maxlen=SUB_MAXLEN):
    """切字幕行：只在标点（逗号/顿号/分句）处断，绝不在词或数字中间切；按视觉宽度合并到 ≤maxlen；
    句末（。！？）强制收行；单个子句超宽才在自然处折。返回 [{text,n,seg}]（n＝有声字数，供对齐）。"""
    out = []
    for si, seg in enumerate(segments):
        for q in "「」『』":
            seg = seg.replace(q, "")
        parts = re.split(r"(?<=[。！？；，、：])", seg)
        cur = ""

        def flush():
            nonlocal cur
            core = cur.strip().rstrip("。，、；：！？ ")
            if core:
                for piece in _wrap_clause(core, maxlen):
                    piece = piece.strip()
                    n = len(_sub_spoken(piece))
                    if n:
                        out.append({"text": piece, "n": n, "seg": si})
            cur = ""

        for p in parts:
            p = p.strip()
            if not p:
                continue
            if cur and _sub_w(cur) + _sub_w(p) > maxlen:   # 放不下 → 先在上一个标点处收行
                flush()
            cur += p
            if p[-1] in SUB_STRONG:                        # 句末必收行，不跨句合并
                flush()
        flush()
    return out


def _align_whisper(lines, audio_path, log=print):
    """faster-whisper 词级时间戳 → 按有声字比例映射到字幕行。不可用/失败返回 None。"""
    try:
        from faster_whisper import WhisperModel
    except Exception as e:  # noqa: BLE001
        log(f"[subs] 无 faster-whisper（{e}）"); return None
    try:
        model = WhisperModel("base", device="cpu", compute_type="int8")
        wsegs, _ = model.transcribe(str(audio_path), language="zh", word_timestamps=True)
        cs, ce = [], []
        for ws in wsegs:
            for w in (ws.words or []):
                wc = _sub_spoken(w.word)
                if not wc:
                    continue
                a, b = float(w.start), float(w.end)
                for k in range(len(wc)):
                    cs.append(a + (b - a) * k / len(wc))
                    ce.append(a + (b - a) * (k + 1) / len(wc))
        Nw = len(cs)
        Nm = sum(l["n"] for l in lines)
        if Nw < 10 or Nm == 0:
            return None
        times, cum, prev = [], 0, 0.0
        for l in lines:
            a = cum; b = cum + l["n"]; cum = b
            ia = min(Nw - 1, max(0, round(a * Nw / Nm)))
            ib = min(Nw - 1, max(0, round((b - 1) * Nw / Nm)))
            st = max(prev, cs[ia]); en = max(st + 0.4, ce[ib])
            times.append((st, en)); prev = en
        log(f"[subs] faster-whisper 对齐：whisper {Nw} 字 ↔ 脚本 {Nm} 字")
        return times
    except Exception as e:  # noqa: BLE001
        log(f"[subs] whisper 对齐失败（{str(e)[:80]}）"); return None


def _align_durs(lines, durs):
    """回退：按每段时长 durs、行内有声字比例分配（有段间停顿漂移，精度略低）。"""
    starts = [sum(durs[:i]) for i in range(len(durs))]
    by_seg = {}
    for i, l in enumerate(lines):
        by_seg.setdefault(l["seg"], []).append((i, l))
    times = [None] * len(lines)
    for si, group in by_seg.items():
        tot = sum(g["n"] for _, g in group) or 1
        t0 = starts[si] if si < len(starts) else 0.0
        acc = 0.0
        for i, g in group:
            d = (durs[si] if si < len(durs) else 2.0) * g["n"] / tot
            times[i] = (t0 + acc, t0 + acc + d); acc += d
    return times


def _ass_ts(x):
    cs_ = int(round(x * 100)); h = cs_ // 360000; m = (cs_ // 6000) % 60
    s = (cs_ // 100) % 60; c = cs_ % 100
    return f"{h}:{m:02d}:{s:02d}.{c:02d}"


def write_ass(lines, times, ass_path, marginv=SUB_MARGINV, fontsize=SUB_FONTSIZE, font=SUB_FONT):
    """写 ASS：微软雅黑、半透明黑底(BorderStyle=3)、底部居中、MarginV 控制高度。"""
    head = (
        "[Script Info]\nScriptType: v4.00+\n"
        f"PlayResX: {OUT_W}\nPlayResY: {OUT_H}\nWrapStyle: 2\nScaledBorderAndShadow: yes\n\n"
        "[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, "
        "BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, "
        "BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
        f"Style: Default,{font},{fontsize},&H00FFFFFF,&H00FFFFFF,&H00101010,&H8C000000,"
        f"1,0,0,0,100,100,0,0,3,8,0,2,150,150,{marginv},1\n\n"
        "[Events]\n"
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    )
    ev = "".join(
        f"Dialogue: 0,{_ass_ts(st)},{_ass_ts(en)},Default,,0,0,0,,{l['text']}\n"
        for l, (st, en) in zip(lines, times)
    )
    Path(ass_path).write_text(head + ev, encoding="utf-8")
    return ass_path


def burn_subtitles(video_in, ass_path, video_out):
    """ffmpeg 把 ASS 烧进视频。用 cwd 下相对路径避开 Windows 盘符冒号转义。"""
    ass_path, video_in, video_out = Path(ass_path), Path(video_in), Path(video_out)
    tmp = Path.cwd() / ("_burn_" + ass_path.name)
    shutil.copy(ass_path, tmp)
    try:
        cmd = [FFMPEG, "-y", "-i", str(video_in), "-vf", f"ass={tmp.name}",
               "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20",
               "-c:a", "copy", str(video_out)]
        r = subprocess.run(cmd, cwd=str(Path.cwd()), capture_output=True, text=True)
    finally:
        tmp.unlink(missing_ok=True)
    if r.returncode != 0:
        raise SystemExit("subtitle burn failed:\n" + r.stderr[-1500:])
    return video_out


def add_subtitles(segments, durs, audio_path, video_in, video_out,
                  ass_path=None, marginv=SUB_MARGINV, log=print):
    """一站式字幕：脚本段 → 字幕行 →（whisper 对齐｜durs 回退）→ ASS → 烧进视频。

    segments: 与 durs 等长的「每段旁白文本」（= gb.split_segments(strip_header(md))）。
    durs    : 每段秒数（与卡点同一份 durs.json）。
    """
    lines = subtitle_lines(segments)
    times = _align_whisper(lines, audio_path, log)
    if times is None:
        log("[subs] 回退 durs 按段比例分配")
        times = _align_durs(lines, durs)
    if ass_path is None:
        ass_path = Path(video_out).with_name("subs.ass")
    write_ass(lines, times, ass_path, marginv=marginv)
    log(f"[subs] {len(lines)} 行 → {ass_path}")
    burn_subtitles(video_in, ass_path, video_out)
    log(f"[subs] 烧字幕 → {video_out}")
    return video_out


def build_xhs_video(cards, audio_path, out_path, date=None,
                    cards_dir="assets/xhs_cards_html", seg_durations=None,
                    intro_path=None):
    """渲染卡片 + 合成视频。cards 为 dict 列表。返回输出路径。

    seg_durations: 每张卡对应那段旁白的真实时长（秒）。给定时按它精确卡点——
    每张卡停留 = 该段旁白时长，交叉淡变恰好从该段结束处开始；否则按 WEIGHTS 估算。
    intro_path: 片头视频路径。给定时先合成主视频，再把片头拼到最前面。
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
    if intro_path and Path(intro_path).exists():
        tmp = Path(out_path).with_name(Path(out_path).stem + "_body.mp4")
        composite(pngs, durs, audio_path, tmp)
        prepend_intro(intro_path, tmp, out_path)
        tmp.unlink(missing_ok=True)
    else:
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
