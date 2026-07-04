# -*- coding: utf-8 -*-
"""0705 出片：16 张卡（无片头 + 圆形猫头片尾）+ 字幕。全量重渲染，片尾坐标按卡片坐标系。"""
import sys, json, shutil
from pathlib import Path
sys.path.insert(0, "scripts")
import make_xhs_video_html as xhs
import run_daily as rd, generate_broadcast as gb
from PIL import Image

ROOT = Path("E:/Github_project/ai-briefcast")
DATE = "2026-07-05"
AUDIO = str(ROOT / f"output/{DATE}/audio/broadcast-{DATE}-spacex.mp3")
seg_durs = json.loads((ROOT / f"output/{DATE}/audio/durs.json").read_text(encoding="utf-8"))
VDIR = ROOT / f"output/{DATE}/video"; VDIR.mkdir(parents=True, exist_ok=True)
MAIN = str(VDIR / "_main.mp4"); OUTRO = str(VDIR / "_outro.mp4")
BASE = str(VDIR / f"xhs-{DATE}-spacex.mp4")
SUB = str(VDIR / f"xhs-{DATE}-spacex-sub.mp4")
PHOTO = str(ROOT / "片头" / "图片_20260606072137.png")
CDIR = ROOT / f"assets/xhs_cards_{DATE}"

c1, c3, c4, c5, c2 = "c1", "c3", "c4", "c5", "c2"
MW = 1.5
def P(g, tag, ic, t, b, pu):
    return {"kind": "point", "grad": g, "tag": tag, "icon": ic, "title": t, "body": b, "punch": pu}
def E(g, ic, rel, t, b):
    return {"kind": "explainer", "grad": g, "icon": ic, "rel": rel, "title": t, "body": b}

GROUPS = [
    ([{"kind": "cover", "badge": "建议收藏 · 每日AI速览", "subtitle": "7月5日 · AI Briefcast", "count": 5,
       "toc": ["阿里全面禁用Claude", "扎克伯格认怂agent", "OpenAI送政府5%股权", "教AI说我不知道", "简单办法打赢花哨"]}], [1]),
    ([P(c1, "头条 01 · 行业", "📱", "阿里全面禁用Claude",
        "**7月3日**发通知、**7月10日**生效。导火索是 Anthropic 指控千问用 **2.5万假账号** 蒸馏，又被曝 Claude Code 藏检测机制", "先封禁，再指控，又设防"),
      E(c1, "🧪", "头条01", "模型蒸馏", "把大模型答过的海量问题当教材，喂给小模型照着学，就能低成本学到它的本事。**阿里被指用假账号问了 Claude 2880万次** 偷师"),
      E(c1, "🕵️", "头条01", "时区检测机制", "Claude Code 偷查你电脑是不是 **中国时区**，再比对一份 **147个域名** 清单，把结果藏进日期格式悄悄回传。原厂称防倒卖，新版已删")], [MW, 1, 1]),
    ([P(c3, "头条 02 · 观察", "🥪", "AI叙事在膨胀",
        "卖三明治的连锁店招股书都郑重写上 AI。可扎克伯格在 Meta 内部会议承认，**agent 进展不及预期**", "外面吹得越响，里面活越没干完"),
      E(c3, "🤖", "头条02", "AI agent", "给个目标就自己拆解、调工具、连续干完的 AI，不用一步步下指令。**扎克伯格说“没跟上预期”的**，正是它"),
      E(c3, "📰", "头条02", "AI取代焦虑史", "这几年头条轮番喊 AI 要 **终结教育、取代作家和工程师、让 SaaS 消失**。SaaS 没消失，可当真的人真亏了钱")], [MW, 1, 1]),
    ([P(c4, "头条 03 · 博弈", "🏛️", "OpenAI递投名状",
        "OpenAI 提出把 **5%股权** 给美国政府换关系缓和。Anthropic 也靠让步换 Fable 5 重新上线", "AI竞争早不只是技术竞争"),
      E(c4, "🤝", "头条03", "股权换监管", "AI 实验室要政府松绑审批，就拿好处换空间。**OpenAI 提议送 5%股权**、Anthropic 靠让步换模型上线，都是递投名状"),
      E(c4, "🌍", "头条03", "主权AI", "一个国家用自己的算力、数据、语言造、自己能管的 AI，不依赖外国。各国抢着建，图的是 **别被卡脖子**")], [MW, 1, 1]),
    ([P(c5, "论文 01 · 安全", "🎓", "教AI说我不知道",
        "对付 AI 胡说，常规做法是外面加核查。耶鲁把“知道自己不知道”直接当 **训练目标**", "敢说不知道的AI更让人放心"),
      E(c5, "📄", "论文01", "预印本", "论文正式发表前的 **公开草稿**，抢时间先放网上交流，**没经过同行评审**。今天两篇论文都是这类，数字好看也要留一分怀疑"),
      E(c5, "🧠", "论文01", "元认知/校准", "AI **“知道自己有几分把握”** 的能力。理想是嘴上说的自信，对得上它真实的水平，而不是高声胡说")], [MW, 1, 1]),
    ([P(c2, "论文 02 · 评测", "🔬", "简单办法打赢花哨",
        "QVal 横评 **21种方法、7个流派**，做了 **1200+次实验**。结论是直接拿提示词问模型，稳定赢过多数复杂监督", "花哨监督不如简单基线"),
      E(c2, "🔁", "论文02", "长程agent", "干一件事要 **连着做几百上千步** 的 AI。只看最后成没成，中间对错太稀疏，才有人想给每步打分")], [MW, 1]),
    ([{"kind": "cta", "title": "明天见", "subtitle": "每天一分钟，AI新鲜事不错过", "tags": ["关注", "收藏", "分享"]}], [1]),
]

assert len(GROUPS) == len(seg_durs)
cards, card_durs = [], []
for (gc, w), sd in zip(GROUPS, seg_durs):
    s = sum(w)
    for cd, wi in zip(gc, w):
        cards.append(cd); card_durs.append(sd * wi / s)
print(f"[plan] {len(cards)} 卡 旁白 {sum(card_durs):.1f}s", flush=True)

pngs = xhs.render_cards(cards, CDIR, "")           # 全量重渲染 → CTA 卡干净
cw, ch = Image.open(pngs[-1]).size
print(f"[cards] {len(pngs)} PNG  card={cw}x{ch}", flush=True)

# —— 片尾参数＝0615/0701–0704 已验证做法（skill 步骤5），别改 ——
photo = xhs.circle_photo(PHOTO, 760)               # 默认裁切参数含住猫头
center = (1080, int(0.24 * 3840))                  # 2160 宽卡片水平居中、24% 高度
plain = str(Path(pngs[-1]).with_suffix(".plain.png"))
shutil.copy(pngs[-1], plain)
xhs.place_photo_on_card(pngs[-1], photo, center)
xhs.composite(pngs, [d + xhs.XFADE for d in card_durs], AUDIO, MAIN)   # 逐卡 +XFADE 补转场
xhs.build_shrink_outro(plain, photo, center, OUTRO, dur=1.0)
xhs.concat_clips([MAIN, OUTRO], BASE)
print(f"[base] {BASE}", flush=True)

md = (ROOT / f"output/{DATE}/scripts/broadcast-0705-B-changed.md").read_text(encoding="utf-8")
segs = gb.split_segments(rd.strip_header(md))
xhs.add_subtitles(segs, seg_durs, AUDIO, BASE, SUB)
print(f"[done] {SUB}", flush=True)
