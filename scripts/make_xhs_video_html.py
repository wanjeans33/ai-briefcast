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
        inner = (f'<div class="brand">{c.get("badge","每日AI速览")}</div>'
                 f'<div class="coverhead"><div class="sub">{c.get("subtitle","")}</div>'
                 f'<div class="big">今日 <em>{cnt}</em> 条要闻</div></div>'
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
