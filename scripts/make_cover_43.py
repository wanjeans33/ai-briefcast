#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""抖音横版封面生成器（HTML → Playwright 截图，4:3 / 1440×1080，@2x=2880×2160）。

读取 output/<date>/episode.yaml 的 cover3x4 数据，排成横版双栏：
左=品牌+kicker+大字钩子+日期，右=5 行速览。

用法：python scripts/make_cover_43.py --date 2026-07-16
     输出 output/<date>/cover/cover-<date>-4x3.png
"""
import argparse
import re
from pathlib import Path

import yaml
from playwright.sync_api import sync_playwright

W, H = 1440, 1080   # 4:3 横版
ACC = "#d6431f"

CSS = f"""
*{{margin:0;box-sizing:border-box}}
body{{font-family:'Microsoft YaHei','Noto Sans SC','PingFang SC',sans-serif;-webkit-font-smoothing:antialiased}}
.cover{{width:{W}px;height:{H}px;position:relative;overflow:hidden;display:flex;
       padding:64px 68px;color:#3a1d10;gap:56px;
       background:linear-gradient(130deg,#fbe3d3 0%,#f3a98a 100%)}}
.deco{{position:absolute;right:-140px;top:-150px;font-size:460px;opacity:0.11;transform:rotate(12deg);z-index:0}}
.deco2{{position:absolute;right:44px;bottom:20px;font-size:180px;opacity:0.22;z-index:0}}
.left{{z-index:2;flex:0 0 46%;display:flex;flex-direction:column}}
.brand{{display:inline-flex;align-items:center;gap:10px;align-self:flex-start;
       padding:14px 28px;border-radius:999px;background:rgba(255,255,255,0.6);
       font-size:27px;font-weight:800}}
.hook{{margin-top:52px}}
.hook .k{{font-size:34px;font-weight:800;opacity:0.66}}
.hook .big{{font-size:96px;font-weight:900;line-height:1.06;letter-spacing:-0.02em;margin-top:10px;
           text-shadow:0 2px 0 rgba(255,255,255,0.5),0 0 28px rgba(251,227,211,0.85)}}
.hook .big em{{color:{ACC};font-style:normal}}
.foot{{margin-top:auto;display:flex;align-items:center;gap:22px}}
.foot .l{{font-size:29px;font-weight:700;opacity:0.7}}
.foot .save{{font-size:29px;font-weight:900;color:{ACC};padding:13px 26px;border-radius:999px;
            background:rgba(255,255,255,0.7)}}
.list{{z-index:2;flex:1;display:flex;flex-direction:column;gap:34px;justify-content:center}}
.row{{display:flex;align-items:flex-start;gap:20px;font-size:40px;font-weight:700;line-height:1.26}}
.row .n{{flex:none;width:54px;height:54px;border-radius:14px;background:#4a2718;color:#fff;
        font-size:30px;font-weight:900;display:flex;align-items:center;justify-content:center}}
.row b{{background:{ACC};color:#fff;padding:2px 12px;border-radius:10px;
       -webkit-box-decoration-break:clone;box-decoration-break:clone}}
"""


def hl(t: str) -> str:
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


def build_html(brand, kicker, big, rows, date):
    row_html = "".join(
        f'<div class="row"><span class="n">{i+1}</span><span>{hl(t)}</span></div>'
        for i, t in enumerate(rows))
    return (f"<!DOCTYPE html><html lang=zh-CN><head><meta charset=UTF-8>"
            f"<style>{CSS}</style></head><body>"
            f'<div class="cover">'
            f'<div class="deco">🍊</div><div class="deco2">😼</div>'
            f'<div class="left">'
            f'<div class="brand">{brand}</div>'
            f'<div class="hook"><div class="k">{kicker}</div>'
            f'<div class="big">{big}</div></div>'
            f'<div class="foot"><span class="l">{date}</span>'
            f'<span class="save">建议收藏 ⭐</span></div>'
            f'</div>'
            f'<div class="list">{row_html}</div>'
            f'</div></body></html>')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    args = ap.parse_args()
    repo = Path(__file__).resolve().parents[1]
    outd = repo / "output" / args.date
    ep = yaml.safe_load((outd / "episode.yaml").read_text(encoding="utf-8"))
    cov = ep["cover3x4"]
    brand = cov.get("brand", "🍊 柿子树下的猫 ｜ AI 速览")
    date = cov.get("date", f"@AI Briefcast · {args.date[5:].lstrip('0').replace('-0', '/').replace('-', '/')}")
    out = outd / "cover" / f"cover-{args.date}-4x3.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.set_content(build_html(brand, cov["kicker"], cov["big"], cov["rows"], date),
                       wait_until="load")
        pg.wait_for_timeout(300)
        pg.query_selector(".cover").screenshot(path=str(out))
        b.close()
    print(f"[done] {out}  ({out.stat().st_size/1e6:.2f} MB, {W*2}x{H*2})")


if __name__ == "__main__":
    main()
