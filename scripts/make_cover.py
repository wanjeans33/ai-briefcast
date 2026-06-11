#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""小红书封面生成器（HTML → Playwright 截图，3:4 / 1080×1440）。

用法：python scripts/make_cover.py   # 默认出 6/7 封面到 assets/cover/cover.png
"""
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

W, H = 1080, 1440   # 小红书封面 3:4
ACC = "#d6431f"     # 主点缀色（暖橙红）

CSS = f"""
*{{margin:0;box-sizing:border-box}}
body{{font-family:'Microsoft YaHei','Noto Sans SC','PingFang SC',sans-serif;-webkit-font-smoothing:antialiased}}
.cover{{width:{W}px;height:{H}px;position:relative;overflow:hidden;display:flex;flex-direction:column;
       padding:76px 72px 64px;color:#3a1d10;
       background:linear-gradient(155deg,#fbe3d3 0%,#f3a98a 100%)}}
.deco{{position:absolute;right:-90px;top:-70px;font-size:520px;opacity:0.16;transform:rotate(12deg);z-index:0}}
.deco2{{position:absolute;right:60px;bottom:30px;font-size:230px;opacity:0.22;z-index:0}}
.brand{{display:inline-flex;align-items:center;gap:12px;align-self:flex-start;z-index:2;
       padding:16px 32px;border-radius:999px;background:rgba(255,255,255,0.6);
       font-size:30px;font-weight:800}}
.hook{{z-index:2;margin-top:54px}}
.hook .k{{font-size:40px;font-weight:800;opacity:0.66}}
.hook .big{{font-size:150px;font-weight:900;line-height:0.98;letter-spacing:-0.02em;margin-top:8px}}
.hook .big em{{color:{ACC};font-style:normal}}
.list{{z-index:2;margin-top:60px;display:flex;flex-direction:column;gap:30px}}
.row{{display:flex;align-items:flex-start;gap:24px;font-size:46px;font-weight:700;line-height:1.26}}
.row .n{{flex:none;width:62px;height:62px;border-radius:16px;background:{ACC};color:#fff;
        font-size:34px;font-weight:900;display:flex;align-items:center;justify-content:center}}
.row b{{background:{ACC};color:#fff;padding:2px 14px;border-radius:12px;
       -webkit-box-decoration-break:clone;box-decoration-break:clone}}
.foot{{z-index:2;margin-top:auto;display:flex;align-items:center;justify-content:space-between}}
.foot .l{{font-size:34px;font-weight:700;opacity:0.7}}
.foot .save{{font-size:34px;font-weight:900;color:{ACC};padding:16px 30px;border-radius:999px;
            background:rgba(255,255,255,0.7)}}
"""


def hl(t: str) -> str:
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)


# —— 6/11 封面内容 ——
BRAND = "🍊 柿子树下的猫 ｜ AI 速览"
KICKER = "6月11日 · 1分钟追上AI圈"
BIG = '今日 AI<br><em>5</em> 件大事'
ROWS = [
    "马斯克把**数据中心搬上天**，散热遭质疑",
    "双方律师**AI代笔没审**，法官取消庭审",
    "苹果**云端AI免费**，圈住中小开发者",
    "视频多点编辑，**一上强度就翻车**",
    "记忆更新**也能学**，冻结模型拿高分",
]
DATE = "@AI Briefcast · 6/11"


def build_html():
    rows = "".join(
        f'<div class="row"><span class="n">{i+1}</span><span>{hl(t)}</span></div>'
        for i, t in enumerate(ROWS))
    return (f"<!DOCTYPE html><html lang=zh-CN><head><meta charset=UTF-8>"
            f"<style>{CSS}</style></head><body>"
            f'<div class="cover">'
            f'<div class="deco">🍊</div><div class="deco2">😼</div>'
            f'<div class="brand">{BRAND}</div>'
            f'<div class="hook"><div class="k">{KICKER}</div>'
            f'<div class="big">{BIG}</div></div>'
            f'<div class="list">{rows}</div>'
            f'<div class="foot"><span class="l">{DATE}</span>'
            f'<span class="save">建议收藏 ⭐</span></div>'
            f'</div></body></html>')


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("assets/cover/cover.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
        pg.set_content(build_html(), wait_until="load")
        pg.wait_for_timeout(300)
        pg.query_selector(".cover").screenshot(path=str(out))
        b.close()
    print(f"[done] {out}  ({out.stat().st_size/1e6:.2f} MB, {W*2}x{H*2})")


if __name__ == "__main__":
    main()
