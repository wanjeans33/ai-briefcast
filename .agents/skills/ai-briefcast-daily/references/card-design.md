# 卡片设计参考（make_xhs_video_html.py）

竖屏 9:16，HTML 渲染（viewport 1080×1920，dsf=2 → 卡片 PNG 2160×3840），ffmpeg 交叉淡变卡点。
渲染入口 `build_xhs_video(cards, audio, out, date, cards_dir, seg_durations, intro_path)`。

## 文案要点（先记住）
- **内容卡（point）要有干货**：短标题 + **加厚正文（2 个数字/事实）** + 金句。只有标题+金句会显单薄。
- **补充卡（explainer）是科普**：解释新闻/论文里的概念/背景（AI 名词、金融词、旧闻），**不复述新闻**，
  口语"高中生也能懂"，且**联网查证**后再写。标题别加"什么是"前缀，直接 `「概念」`。
- 内容卡文案常按"3 选 1"（观点①/数字②/提问③）让用户挑；补充卡先给候选池让用户多选。

## 卡片类型与字段

所有 `body`/`punch` 支持 `**关键词**` → 渲染成主题色**高亮色块**（不是只加粗）。`title` 自动按字断行。

### cover（封面/目录钩子，第一张）
```python
{"kind":"cover","badge":"建议收藏 · 每日AI速览","subtitle":"6月7日 · AI Briefcast",
 "count":3,"toc":["逐条列中间卡的一句话标题（≤14字）", ...]}
```
渲染为「今日 N 条要闻」+ 编号目录预告。`count` 一般 = 头条数。

### point（新闻卡）
```python
{"kind":"point","grad":"c1","tag":"头条 01 · 行业","icon":"📱","title":"≤10字标题",
 "body":"≤55字，**关键数字/词**高亮","punch":"≤16字金句，可**加粗**，显示在卡片底部"}
```
右上有超大半透明序号（取 `tag` 里的数字），底部金句，正文左侧主题色条。

### explainer（信息补充卡）
```python
{"kind":"explainer","grad":"c1","icon":"📰","rel":"头条01","title":"术语/要点",
 "body":"高中生也能懂的口语解释，**关键事实**高亮（需联网查证）"}
```
顶部描边「信息补充」标签 + 主题角标（用 `icon` 放大）+ `↑ 关联：<rel>`，内容垂直居中。
**与父新闻同色分组**：把同一条新闻的新闻卡和它的补充卡设成相同 `grad`。

### cta（结尾）
```python
{"kind":"cta","title":"明天见","subtitle":"每天三分钟，AI新鲜事不错过","tags":["关注","收藏","分享"]}
```

## 配色（grad）
`c1` 桃、`c2` 米黄、`c3` 灰绿、`c4` 蓝紫、`c5` 粉、`c7` 暗（CTA 固定）。
三条新闻建议用 `c1 / c3 / c4` 区分；不写 `grad` 则按位置自动取色（cover=c1, cta=c7）。

## 卡点（精确对齐音频）
音频按段（intro / 每条新闻 / 收尾）合成，每段有真实时长。把每段时长按组内权重切给该组卡片：
- 新闻卡权重 1.5，每张补充卡 1.0。
- `seg_durations` 传**展开后每张卡的可见时长**（顺序与 `cards` 一致），`build_xhs_video` 会自动 `+XFADE`，
  使每次淡变恰好落在该卡时间结束处。`len(seg_durations) == len(cards)`。

## 可直接改用的驱动脚本

把下面存成 `scripts/_tmp_make_<date>.py`，改 `GROUPS` 内容后运行；用完可删。
**音频复用已合成的 `segs/*.mp3`，不重配音。**

```python
import sys
from pathlib import Path
import av
sys.path.insert(0, "scripts")
import make_xhs_video_html as xhs

ROOT = Path("E:/Github_project/ai-briefcast")
DATE = "2026-06-07"
SUF  = "-3news"                       # 用哪份音频的 seg 前缀
SEG  = ROOT/"audio_output"/"segs"
AUDIO= ROOT/"audio_output"/f"broadcast-{DATE}-concise{SUF}.mp3"
INTRO= ROOT/"片头"/"小猫片头_1x1_4s.mp4"
OUT  = ROOT/"audio_output"/f"xhs-{DATE}-concise-cards.mp4"
A,B,C = "c1","c3","c4"; MW = 1.5

# (该段音频 seg 名, [组内卡片...], [组内权重...])  —— 顺序 = 音频段顺序
GROUPS = [
  ("seg00", [ {"kind":"cover","badge":"建议收藏 · 每日AI速览","subtitle":f"…","count":3,"toc":["…","…","…"]} ], [1]),
  ("seg01", [ {"kind":"point","grad":A,"tag":"头条 01 · 行业","icon":"📱","title":"…","body":"…**…**…","punch":"…"},
              {"kind":"explainer","grad":A,"icon":"📰","rel":"头条01","title":"…","body":"…**…**…"},
              # …更多补充卡（同 grad）
            ], [MW,1,1]),
  # seg02 / seg03 同理（grad 换 B / C）
  ("seg04", [ {"kind":"cta","title":"明天见","subtitle":"每天三分钟，AI新鲜事不错过","tags":["关注","收藏","分享"]} ], [1]),
]

def secs(name):
    p = SEG/f"broadcast-{DATE}-concise{SUF}-{name}.mp3"
    a = av.open(str(p)); d = a.duration/1e6; a.close(); return d

cards, durs = [], []
for name, gc, w in GROUPS:
    total = secs(name); s = sum(w)
    for cd, wi in zip(gc, w):
        cards.append(cd); durs.append(total*wi/s)
print(f"[plan] {len(cards)} 张卡, ≈{sum(durs):.1f}s + 片头")
xhs.build_xhs_video(cards, AUDIO, OUT, date=DATE, seg_durations=durs,
                    cards_dir=f"assets/xhs_cards_{DATE}", intro_path=INTRO)
print("[done]", OUT)
```

运行：`PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python scripts/_tmp_make_<date>.py`
渲染后用 Read 抽查 `assets/xhs_cards_<date>/card-*.png`；用 ffprobe 确认 2160×3840 与时长。

### 变体：还没配音时（首次出片 / 跨日期精选）
把 GROUPS 改成 `[(cards, weights), ...]`（顺序＝音频段顺序，不带 seg 名），先用
**`run_daily.synth_single_synced`**（整段一次合成、音色统一）拿每段时长，再按权重摊给组内卡片：
```python
import os, sys; sys.path.insert(0, "scripts")
import run_daily as rd, generate_broadcast as gb, make_xhs_video_html as xhs
rd.load_dotenv(rd.REPO_ROOT)
os.environ["VOLC_SPEECH_RATE"] = "50"                       # ≈1.4×（默认）
spk = os.getenv("VOLC_SPEAKER2")
segs = gb.split_segments(rd.strip_header(open("output/<date>/scripts/broadcast-....md",encoding="utf-8").read()))
log = rd.Logger(rd.REPO_ROOT/"logs"/"run-mix.log")
durs_seg = rd.synth_single_synced(segs, AUDIO, log, spk)    # 7 段 → 7 个真实时长（音色统一）
assert len(GROUPS) == len(segs)
cards, durs = [], []
for sd, group in zip(durs_seg, GROUPS):
    s = sum(w for _, w in group)
    for cd, w in group: cards.append(cd); durs.append(sd*w/s)
xhs.build_xhs_video(cards, AUDIO, OUT, seg_durations=durs, cards_dir=..., intro_path=INTRO)
```
要点：`len(GROUPS) == 段数`；段顺序＝ intro / 每条内容 / 收尾；补充卡放在其父内容卡同一组里。
