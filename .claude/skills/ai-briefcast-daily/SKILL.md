---
name: ai-briefcast-daily
description: >
  在 ai-briefcast 仓库里生成"每日 AI 速览"的小红书成品：竖屏卡点视频（4K，带片头）+
  3:4 封面 + 标题/话题标签。覆盖抓取(可跨日期混合：某天新闻+另一天论文)→选稿(可出多版让用户挑)→
  固定开场白→分段豆包TTS(克隆音色)→内容卡(标题+加厚正文+金句)+联网查证的科普「信息补充」卡
  (按新闻同色分组)→逐卡精确卡点+1:1片头→make_cover 封面→标题/话题标签。
  只要用户提到"做今天/某天/某几天的（AI）播报/视频/小红书/封面/卡片/briefcast/速览/精选"、
  要为某条音频配视频、要选稿/选卡、要补充卡/封面/标题/tag，就使用本技能；即使没说"skill"也要主动用。
---

# AI Briefcast 每日小红书成品流水线

把 ai-briefcast.liziran 两个来源的当天新闻，做成可直接发小红书的一套成品：
**4K 竖屏卡点视频（带猫片头）+ 3:4 封面 + 标题 + 话题标签**。

仓库根：`E:\Github_project\ai-briefcast`。所有命令在仓库根执行，加 `PYTHONUTF8=1 PYTHONIOENCODING=utf-8`（Windows 中文输出）。

## 关键约定（记住这些，少踩坑）

- **声音**：用户自己的豆包克隆音色 `VOLC_SPEAKER2=S_HHgApOH42`（不是 liziran 的）。
- **开场白固定**：每天用"大家好，这里是柿子树下的猫wanjeans，三分钟带你了解AI圈的新鲜事。…"。
  `generate_broadcast.fixed_intro()` 自动套用（只换日期）；跨日期精选时手写一句不带具体日期的开场即可。
- **可跨日期混合**：常见需求是"某天的新闻 + 另一天的论文"，且按 **N 闻 + M 论文** 选（如 3+2）。
  digest 和 brief 各自按自己的日期抓，再合成一份素材（见步骤 1）。
- **内容卡要有干货**：每张新闻/论文卡 = 短标题(视觉锤) + **加厚正文(塞 2 个数字/事实)** + 金句(观点)，
  只有标题+金句会显单薄。
- **补充卡 = 科普概念**：解释新闻/论文里普通人看不懂的概念（AI 名词、金融词、背景旧闻等），
  **不是复述新闻**。口语"高中生也能懂"，且**必须联网查证**后再写。
- **音频/文稿是基线，不要为了加卡片去改它**：补充卡是静默视觉卡，把某条新闻/论文的音频时长
  切给"内容卡+几张补充卡"，不重新配音。
- **交互式选稿/选卡**：稿子可出 2 版（如 A 轻快网感 / B 沉稳串点）让用户选；卡片文案可"3 选 1"
  （观点/数字/提问三种标题风格，用户可逐卡选如 "22231"）；补充卡先给候选池让用户"多选"。
- **片头 / 片尾**：默认 1:1 片头 `片头/小猫片头_1x1_4s.mp4`（模糊铺底+居中）。也可改成**片尾**——
  最后一张卡放品牌圆形照片，结尾 1 秒圆圈缩小消失（见步骤 5 的片尾做法）；二者按用户要求二选一。
- **语速可调**：`doubao_tts_ws` 读 `VOLC_SPEECH_RATE`（正数更快）。实测 rate 30≈1.19×、**50≈1.4×**、
  60≈1.51×、上限约 1.85×。**默认 1.4×（rate 50）**听感从容。想要更短先调语速，但**只靠语速到不了
  大幅缩短**（~150s 稿拉满也才 ~80s），真要 1 分钟还得删稿。
- **音色优先：整段一次合成**。分段独立调用克隆音色会在段间（尤其 intro/收尾这种短段）**音色漂移**。
  默认用 `run_daily.synth_single_synced`：整段一次合成（音色全程统一）+ 逐段临时测时等比缩放卡点
  （见步骤 3）。silencedetect 找段落边界在快语速下不可靠，已弃用。
- **输出结构**：每天产物归到 **`output/<日期>/{scripts,audio,video,cover,cards}/`**，并写
  **`output/<日期>/CHANGELOG.md`** 记录当天每次调整、MD 版本演化、踩坑与决策（经验沉淀，别只堆 `audio_output`）。
- **先音频后视频**：用户常要先听音频确认，再出视频——分步做，别一口气跑完。
- **突发新闻可当头条**：当天有大新闻（如新模型发布）可替换掉抓取的某条头条；<24h 的发布抓取源可能没收录，
  用 deep-research / 官方页核实，必要时让用户给权威链接。
- **ffmpeg 绝对路径**写在 `make_xhs_video_html.FFMPEG`；输出 4K = `OUT_W,OUT_H=2160,3840`。
- **每一步产出后，先让用户审，再继续**：选稿 → 选卡文案/补充卡 → 终审卡片 → 音频确认 → 出片，逐步停。

## 前置检查

- `.env`（仓库根）含：`VOLC_APP_ID/VOLC_API_KEY/VOLC_SPEAKER2/VOLC_RESOURCE_ID`，
  改写用 `DEEPSEEK_API_KEY`（pi 后端）。注意 DeepSeek key 易手滑多打字符，401 时先核对尾号。
- ffmpeg：`make_xhs_video_html.FFMPEG` 指向的 exe 存在。
- Playwright Chromium 已装（`playwright install chromium`）。
- 改写后端：`--llm pi`（pi agent + DeepSeek）或 `--llm api`（OpenAI 兼容直连 DeepSeek）。
  pi 在 Windows 要走 `node dist/cli.js`（已在 `_pi_command()` 处理）。

## 流水线（按顺序，逐步暂停给用户审）

### 1) 抓素材 + 选稿（先和用户对齐范围与风格）
**a. 抓取**。同日：`generate_broadcast.py --date YYYY-MM-DD --dump-raw` 出 `samples/source-<date>.md`。
跨日期混合（某天新闻 + 另一天论文）用内联脚本分别抓：
```python
import generate_broadcast as gb
du = gb.latest_article_url(gb.DIGEST_HOME, "digest", "2026-06-03")   # 新闻那天
bu = gb.latest_article_url(gb.BRIEF_HOME, "daily",  "2026-06-08")    # 论文那天
digest = gb.parse_digest(du); brief = gb.parse_brief(bu)
open("samples/source-mix.md","w",encoding="utf-8").write(gb.build_source_text(digest,brief))
```
读 source，确认 **N 闻 + M 论文**（如 3 头条 + 从 4 篇里挑 2 篇）。论文页常比资讯晚 1 天才更新。

**b. 选稿**。当 DeepSeek 可用时可 `--llm pi` 自动改写；不可用或要更可控时，由 Claude 直接按
`SYSTEM_PROMPT`/`*_INSTRUCTION` 的精神手写。可一次给 **2 版风格**让用户选：
- 版本 A 轻快网感（短句、抓反差、口语、强钩子，利完播涨粉）
- 版本 B 沉稳串点（编辑视角、每条点主题、信息密度高，显专业）
存成 `samples/broadcast-...-A.md` / `-B.md`，**让用户选一版**。每段一空行分隔（= 一个音频段 = 一组卡）。

### 2) 选卡文案 + 选补充卡（文字先定，渲染前确认）
**a. 内容卡文案「3 选 1」**：为每张内容卡给 3 种标题/金句风格——①观点/金句驱动 ②事实/数字驱动
③提问/悬念驱动——让用户逐卡选（回复如 `22231`）。正文统一**加厚**：每张塞 2 个数字/事实 + 1 句金句。

**b. 补充卡「候选池多选」**：列出新闻/论文里值得科普的概念/背景作为候选（每个一句话），
让用户勾选要哪几张。**逐个 WebSearch 查证**（概念定义、事件经过、最新数字/时间），
再写成"高中生也能懂"的 `body`（≤~60 字，`**关键数字/词**` 高亮）。背景类（如"厂商都在喊全员用"
这种旧闻）也算补充卡。**写完文字停下让用户审**，再进入渲染。

### 3) 豆包 TTS（克隆音色）→ 整段合成 + 每段时长（卡点）
**默认 `run_daily.synth_single_synced`**（音色优先）：整段一次合成保证全程音色统一，再逐段临时
合成量"有声时长"等比缩放出卡点时长（临时文件用完即删，不入最终音频）：
```python
import os, run_daily as rd, generate_broadcast as gb
rd.load_dotenv(rd.REPO_ROOT)
os.environ["VOLC_SPEECH_RATE"] = "50"                # ≈1.4×（默认）
spk = os.getenv("VOLC_SPEAKER2")
segs = gb.split_segments(rd.strip_header(md_text))   # 按空行切段 = 一段一组卡
durs = rd.synth_single_synced(segs, mp3_path, log, spk)   # 整段 mp3 + 返回每段秒数
```
- 输出整段 `output/<date>/audio/broadcast-<date>-spacex.mp3`，把 `durs` 存 `audio/durs.json` 备用。
- **语速**：合成前设 `os.environ["VOLC_SPEECH_RATE"]`（默认 `"50"`≈1.4×）。
- **先给音频让用户确认**（打印每段时长 + 总长），确认后再进卡片/视频。
- 旧路径 `run_daily.synth_segmented()`（逐段独立合成再拼接）仍可用，但有段间音色漂移，仅在
  不在意音色一致性时用。**音频一旦满意就别再动**——后面加卡片复用 `durs`，不重配音。

### 4) 组卡 + 渲染（按音频段分组，逐卡卡点）
文案已在步骤 2 定稿，这里把卡片**按音频段分组**并渲染。每个音频段（intro / 每条内容 / 收尾）
对应一组卡：内容卡 + 它的补充卡，**同组同配色**（`grad`），组内时长权重 新闻/论文卡 1.5、补充卡 1.0。
卡片字段、配色、卡点权重、可直接改用的 GROUPS 驱动脚本：见 `references/card-design.md`（**先读它**）。
- 封面 `count`/`toc` 列出内容卡数与一句话标题；配色建议 5 组用 `c1/c3/c4/c5/c2` 区分。
- **渲染后停下让用户审卡片**（抽查封面 + 每组一张 + CTA，确认无乱码/溢出/重叠）。

### 5) 合成 4K 卡点视频 + 1:1 片头
`make_xhs_video_html.build_xhs_video(cards, audio, out, date, seg_durations=durs, intro_path=intro)`：
- `seg_durations` 传"每张卡的可见时长"（已按组切好），实现逐卡卡点；
- `intro_path` 给 `片头/小猫片头_1x1_4s.mp4`，自动模糊铺底适配 + 拼到最前、保留片头音乐。
- 输出 `output/<date>/video/xhs-<date>-spacex.mp4`，4K 2160×3840。
- 校验：用 ffprobe 确认 `width=2160 height=3840`，视频时长 ≈ 片头(4s)+音频（或音频+1s 片尾）。

**片尾做法（替代片头时）**——用 `make_xhs_video_html` 的可复用函数：
```python
photo = xhs.circle_photo("片头/图片_20260606072137.png", 760)   # 圆形裁切（默认参数含住猫头）
import shutil; plain = pngs[-1] + ".plain"; shutil.copy(pngs[-1], plain)   # 留一份无照片的 CTA 背景
xhs.place_photo_on_card(pngs[-1], photo, center=(1080, int(0.24*3840)))     # CTA 静态卡放上满圆照片
xhs.composite(pngs, [d+xhs.XFADE for d in durs], audio, main_mp4)           # 主视频（不传 intro）
xhs.build_shrink_outro(plain, photo, (1080, int(0.24*3840)), outro_mp4, dur=1.0)  # 1s 圆圈缩小消失
xhs.concat_clips([main_mp4, outro_mp4], OUT)                                # 主视频 + 片尾
```
（圆心 center 用卡片像素坐标，2160×3840；`circle_photo` 的 cx/cy/r_frac 可调以适配别的照片。）

> 全自动（无补充卡、每条新闻 1 张卡、同日期）可直接：
> `python scripts/run_daily.py --date <date> --modes concise --video`
> （已默认带片头；`--no-intro` 关闭）。带补充卡/跨日期/选稿/片尾的版本用 GROUPS 驱动脚本组卡。

### 6) 封面（3:4）
```
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python scripts/make_cover.py output/<date>/cover/cover-<date>.png
```
编辑 `make_cover.py` 顶部的 `BRAND/KICKER/BIG/ROWS/DATE` 改当天内容（关键词用 `**…**`）。
- **`BIG` 大标题要吸睛**：别用「今日 AI N 件大事」这种平淡计数，要一句爆点钩子——头条人物/反常动作/
  悬念/超级标题（如「马斯克送显卡上太空」「史上最疯 AI 基建」「最强 Claude 来了」）。`ROWS` 再列 5 条速览。
- 输出 3:4 = 1080×1440（2x → 2160×2880），可单独上传为视频自定义封面。5 行也放得下。

### 7) 标题 + 正文 + 话题标签
**标题**（≤20 字，前 8 字定生死，数字+情绪+悬念取二，口语像爆料）。给 2~3 个选项让用户挑。
**正文（caption）**：开头一句钩子（「今天 AI 圈 N 件大事，1 分钟看完」），中间每条一行短句（可用一、二、三…
或符号编号），结尾「每天一分钟…点赞收藏关注 @柿子树下的猫」。**emoji 默认可加，但用户常要求去掉**——
先问或直接给「带 emoji / 不带 emoji」两版。
**标签金字塔（8~10 个）**：
- 大流量泛标签 ×2：`#人工智能 #AI`
- 领域 ×3：`#AI日报 #每日AI #AI资讯`
- 当天热点具体词 ×3：按内容换（如 `#苹果 #SpaceX #OpenAI` / `#大模型 #ChatGPT #Claude`）
- 品牌 IP ×1：`#柿子树下的猫`
- 场景人群 ×1：`#通勤干货`
固定品牌/领域/场景标签，只换"热点具体词"，利于账号标签沉淀。

## 产物清单（一天，归到 `output/<date>/`）
- `scripts/broadcast-<date>-*.md`（A/B 文稿，含手改版）+ 上游 `samples/source-<date>.md`
- `audio/broadcast-<date>-spacex.mp3`（克隆音色，整段合成）+ `audio/durs.json`（每段卡点时长）
- `video/xhs-<date>-spacex.mp4`（4K 卡点 + 片头/片尾）
- `cover/cover-<date>.png`（3:4 封面）
- `CHANGELOG.md`（当天调整 / MD 版本 / 踩坑 / 决策）
- 标题 + 正文 + 标签（发给用户）

## 排错速记
- DeepSeek 401：先核对 `DEEPSEEK_API_KEY` 尾号（易多打字符）；pi 与 api 后端都受同一 key 影响。
- 豆包 `NO AUDIO RECEIVED` / 403：偶发或限流，`synth_segmented` 已自动重试；仍失败就等额度恢复。
- 末字被吞（快语速更明显）：`doubao_tts_ws.pad_tail()` 在文本尾部补 `，。。。`（逗号停顿+三句号）
  给解码器留余量，别移除/别改短。
- 音色段间跳变：别用逐段拼接，改 `synth_single_synced`（整段一次合成）。
- 卡片乱码/溢出：正文太长就精简 `body`；中文按字断行在 `_wrap()`。
- ffmpeg「Error opening output」/拼接失败：多半是输出 mp3/mp4 正被用户的播放器占用（Windows 文件锁）——
  换个输出文件名（如 `-fast.mp3`）即可，或让用户关掉播放器。
- 媒体文件（mp3/mp4/片头/卡片 png）按 `.gitignore` 不入库，留本地。
