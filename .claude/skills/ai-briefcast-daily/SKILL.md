---
name: ai-briefcast-daily
description: >
  在 ai-briefcast 仓库里生成"每日 AI 速览"的小红书成品：竖屏卡点视频（4K，可带片头或无片头+片尾猫图）+
  3:4 封面 + 标题/话题标签。覆盖抓取(可跨日期混合：某天新闻+另一天论文)→选稿(可出多版让用户挑)→
  固定开场白→分段豆包TTS(克隆音色)→内容卡(标题+加厚正文+金句)+联网查证的科普「信息补充」卡
  (按新闻同色分组)→逐卡精确卡点+片头/片尾→字幕(脚本原文强制对齐烧录)→make_cover 封面→标题/正文/话题标签。
  只要用户提到"做今天/某天/某几天的（AI）播报/视频/小红书/封面/卡片/briefcast/速览/精选"、
  要为某条音频配视频、要选稿/选卡、要补充卡/封面/标题/tag，就使用本技能；即使没说"skill"也要主动用。
  本技能负责小红书成品全流程；其中"选稿/写稿"这一步（步骤 1b）借 ai-news-podcast 技能把关**事实准确性
  和证据纪律**（区分公司自述/预印本/同行评审/独立复现、标注限制、不夸大），最终语言风格仍按本技能★文风铁律
  （大白话、正常语序、禁数数过场、去冒号——这是用户多轮打磨定的，不套用 ai-news-podcast 自己的口播腔和
  时间戳结构）。
---

# AI Briefcast 每日小红书成品流水线

把 ai-briefcast.liziran 两个来源的当天新闻，做成可直接发小红书的一套成品：
**4K 竖屏卡点视频（可带猫片头，或无片头+猫图片尾）+ 3:4 封面 + 标题 + 正文 + 话题标签**。

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
  **每条头条/每篇论文都要配补充卡，一般 1–2 张**（信息量大的头条可 2 张，简单的至少 1 张）——
  别出现"有的新闻两张、有的一张都没有"。选卡时**对每条新闻单独给 2–3 个候选**让用户挑，不要只给一个全局池。
- **音频/文稿是基线，不要为了加卡片去改它**：补充卡是静默视觉卡，把某条新闻/论文的音频时长
  切给"内容卡+几张补充卡"，不重新配音。
- **用户手改稿最高优先级**：如果用户说改稿放在 `changed` / `B-changed` / `*-changed.md`，后续音频、卡片、视频、
  封面、正文/tag 都以它为唯一源。**不要覆盖它**；需要缩短或局部改文时，只按用户明确要求改该文件，并在
  `CHANGELOG.md` 记录。
- **★ 文风铁律（2026-06-23 用户多轮打磨定稿，以后照这个写，别再返工）。范本＝`output/2026-06-23/scripts/broadcast-0623-B-changed.md`**：
  1. **大白话、普通人一听就懂**。专有名词/英文缩写当场用一句话点破（FERC＝美国管电力的机构、SEVRA＝一套方法、LoRA＝小插件），不堆术语。
  2. **正常主谓宾语序，不用被动、不倒装**。把"X 被 Y 放弃了"改成"Y 放弃了 X / Y 也弃了"；别把状语/宾语提前搞倒装。
  3. **不过度缩句，主谓宾齐全**。宁可多几个字把话说圆，也别砍成残句——求短不能牺牲"听得懂"。
  4. **指代必须明确**，不用含糊的"这/它/那个"。人名、机构、对象都点名（"这"指什么写出来）。
  5. **比喻直接、生活化，为"懂"服务不炫技**：如"考试第一≠干活第一""师傅手把手教 vs 徒弟自己关门苦练""电成了 AI 的新瓶颈""社区成了数据矿"。文绉绉/绕的词别用（"二进二出""门轴""旋转门"都被否过）。
  6. **不数数过场**：禁止"第一条/第二条/第三件/最后一件/总结"。用主题或自然连接起句："先说…""欧盟这边…""美国这边在抢电""论文这边…""另一篇…"。
  7. **标点去掉「：」和「——」**（口播里造成别扭停顿）；顿号、逗号、句号正常用。
  8. **每段先因后果、先事实后点评**；**收尾只留署名**「我是柿子树下的猫wanjeans，我们明天见。」，不要"总结金句段"。
  9. **禁用"不是 X 而是 Y / 而是"句式**（2026-07 起用户反复否掉）：想表达转折/递进就正着说，别用"不是…而是…"绕。
  10. **不报硬日期**（2026-07 起）：未来时间用软说法（"下周""九月中""三到五年"），过去发生的关键日期能省则省，别念一串"某月某日"。
  11. 用户要 3 新闻 + 2 论文就别偷偷扩成 4；选题**逐条核发布日期**（聚合站爱把旧闻当"持续报道"混进当日榜，旧的一律踢）。
  - 长度：语速 1.25×（rate 36）时，**内容完整清楚优先**，通常落在 ~85–100s；别为压时长把句子砍残（用户接受过 ~99s 的完整版）。
- **交互式选稿/选卡一律走 `AskUserQuestion`（像 plan 的 ask 一样弹选项，别让用户打 "22231" 字符串）**：
  稿子可出 2 版让用户选；内容卡文案「3 选 1」逐卡一个 question；
  **补充卡按新闻逐条给候选池**——每条头条/论文各一个 `multiSelect` question，每条 2–3 个候选，别用一个全局池混选。
- **片头 / 片尾（2026-07 固化默认：无片头 + 圆形猫头片尾）**：默认**不放小猫片头**，第一帧直接是封面卡
  （大字钩子、关键词标红），最后接**猫图圆形片尾**——CTA 卡上放圆形猫头照片，结尾 1 秒圆圈缩小消失
  （见步骤 5 的片尾做法，`build_shrink_outro`）。7/1–7/4 每天都这么做。只有用户明确要"加小猫片头"时，
  才回退用 1:1 片头 `片头/小猫片头_1x1_4s.mp4`（模糊铺底+居中）。二者不叠加。
- **默认带字幕**（2026-06-17 起，见步骤 5b）：竖屏视频默认烧录字幕。用
  `make_xhs_video_html.add_subtitles(segs, durs, audio, 基底mp4, 输出-sub.mp4)`——取**脚本原文**
  （`gb.split_segments(rd.strip_header(md))`，与卡点同一份 segments）+ `faster-whisper(base)` 词级
  **强制对齐**（不用 ASR 文本，专有名词如 Nex/Qwen/CODA-BENCH 不被改错），whisper 不可用自动回退 `durs` 比例。
  ASS 微软雅黑、半透明黑底、**MarginV=820**（约 78% 高度，落在正文与金句之间的空白带——贴底 MarginV=300 会压金句）。
  发布用 `-sub.mp4`，字幕源留 `video/subs.ass`。
- **封面可做进视频第一帧**（2026-06-23 起）：封面卡支持 `hook` 字段＝大字头条钩子（如 `'谷歌<br><em>留不住人了</em>'`），
  给定时大字＝钩子、"今日N条要闻"降为副行。这样**视频第一帧就是封面**，开场即爆点；这张封面卡 PNG（`cards/card-1.png`）
  可复制到 `cover/` 兼作小红书自定义封面（`make_publish` 会取它）。用户要"封面做进视频"时走这条，不必另出 3:4 `make_cover`。
- **liziran 未更当天时**：`generate_broadcast` 抓不到目标日期会回退到最近一期。此时上网找新闻（WebSearch + 逐条 WebFetch 核**发布日期**，
  只用本月/当周、且我们没做过的；聚合站爱混旧闻）；论文优先从 liziran 最近一期**没选用的**里挑（有全文、好科普），或 HF trending 兜底。
- **对外口径用"1分钟"**：封面、内容卡、CTA、正文默认写"1分钟/每天一分钟"，不要写"90秒"；实际音频可因稿长
  在 60~100 秒间浮动，必要时告诉用户真实时长。
- **语速可调（2026-07 固化默认：1.25×＝rate 36）**：`doubao_tts_ws` 读 `VOLC_SPEECH_RATE`（正数更快）。
  实测 rate 30≈1.19×、**36≈1.25×**、50≈1.4×、60≈1.51×、上限约 1.85×。**默认 rate 36（1.25×）**——
  7/1–7/4 全用它，从容好懂。想要更短先调语速，但**只靠语速到不了大幅缩短**，真要 1 分钟还得删稿。
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

**b. 写稿**（2026-06-23 起：不再 A/B 两版，**直接按上面「★ 文风铁律」写一版定稿**，范本＝`output/2026-06-23/scripts/broadcast-0623-B-changed.md`）。
写之前先借 `ai-news-podcast` 技能过一遍**事实关**：每条新闻/论文按其 `references/evidence-levels.md`
定证据等级（公司自述/预印本/同行评审/独立复现/真实部署），核对数字的基线和来源（`references/source-verification.md`），
论文按 `references/paper-review-guide.md` 找方法、结果、限制。**只借这套事实核验和证据分级，不套用它的
输出模板、时间戳或"换句话说"式口播腔**——语言仍按本技能的★文风铁律写（大白话、正常语序、禁数数过场、去冒号）。
由 Claude 直接手写（DeepSeek 可用也行，但务必按文风铁律收口）。存成 `output/<date>/scripts/broadcast-<date>-B-changed.md`，
**先给用户审、按批注改到满意**（用户常会亲自改这份，它就是唯一源，别覆盖）。每段一空行分隔（= 一个音频段 = 一组卡）。
开场固定 `一分钟带你了解AI圈的新鲜事。`，收尾只留 `我是柿子树下的猫wanjeans，我们明天见。`。
⚠️ 合成前**删掉文末任何备注/footer**（`---` 之后的说明），否则 `split_segments` 会把它当正文读出来。

### 2) 选卡文案 + 选补充卡（文字先定，渲染前确认）
**用 `AskUserQuestion` 工具做交互式选卡**（像 plan 的 ask 一样弹选项，别让用户打 `22231` 这种字符串）：
- **a. 内容卡文案「3 选 1」**：每张内容卡一个 question，3 个 option——①观点/金句驱动 ②事实/数字驱动
  ③提问/悬念驱动（option 描述里写出该版标题+金句）。逐卡问（一次最多 4 个 question，卡多就分批）。
  正文统一**加厚**：每张塞 2 个数字/事实 + 1 句金句。用户也可在 option 里补充自定义文案。
- **b. 补充卡「逐条候选池多选」**：**每条头条、每篇论文各一个 `multiSelect:true` 的 question**，
  给该条 2–3 个候选概念作 options（每个一句话方向），让用户勾出 1–2 张。**别用一个全局池混选，
  也别漏掉任何一条新闻**——每条至少配 1 张（一次最多 4 个 question，新闻多就分批问）。
  选定后**逐个 WebSearch 查证**（概念定义、事件经过、最新数字/时间），
  再写成"高中生也能懂"的 `body`（≤~60 字，`**关键数字/词**` 高亮）。
- 选完**把全部卡片文字汇总成一版让用户终审**（可用纯文本列出），通过后再渲染。

### 3) 豆包 TTS（克隆音色）→ 整段合成 + 每段时长（卡点）
**默认 `run_daily.synth_single_synced`**（音色优先）：整段一次合成保证全程音色统一，再逐段临时
合成量"有声时长"等比缩放出卡点时长（临时文件用完即删，不入最终音频）：
```python
import os, run_daily as rd, generate_broadcast as gb
rd.load_dotenv(rd.REPO_ROOT)
os.environ["VOLC_SPEECH_RATE"] = "36"                # ≈1.25×（2026-07 默认）
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

### 5) 合成 4K 卡点视频（默认无片头 + 猫头片尾）
**⚠️ 出片脚本别凭记忆重写**：直接复制上一日 `scripts/_tmp_video_<上一日>.py`（最新已验证＝
`scripts/_tmp_video_0705.py`，含片尾+字幕全流程）改 DATE/GROUPS 即用。两个易错点：
① 用裸 `composite()` 时每张卡时长必须 **`+xhs.XFADE`**（交叉淡变吃掉转场时长，漏加则视频比音频短、
收尾被截；`build_xhs_video()` 才会自动加）；② 片尾固定参数 `circle_photo(photo, 760)` +
`center=(1080, int(0.24*3840))`（卡片 2160×3840），别换算别自创。
出片后必查：`ffprobe` 时长 ≈ 旁白 + 1s 片尾、2160×3840。

**（备选）带片头的旧路径**：
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
实操时建议保存 `card-N.plain.png` 作为无照片 CTA 底图；若重复出片，先从 plain 恢复 CTA，再放圆形照片，
避免多次叠图。最终用 ffprobe 校验 `2160x3840`、30fps、音频轨和 `音频时长+1s片尾`，并抽首帧/片尾帧 QA。

### 5b) 烧字幕（默认）
片尾 concat 出**基底视频**后，再烧字幕（基底无字幕，留作备用；发布用 `-sub.mp4`）：
```python
segs = gb.split_segments(rd.strip_header(md_text))   # 与卡点同一份 segments（顺序＝音频段）
durs = json.load(open(f"output/{DATE}/audio/durs.json", encoding="utf-8"))
xhs.add_subtitles(segs, durs, AUDIO, OUT, OUT.with_name(OUT.stem + "-sub.mp4"))
```
- 时间轴：`faster-whisper(base)` 词级强制对齐脚本原文（专有名词不被 ASR 改错）；无 whisper 回退 `durs` 比例。
- 样式在 `make_xhs_video_html`：`SUB_FONT/SUB_FONTSIZE/SUB_MARGINV`（默认 微软雅黑 82 / **MarginV=820**，
  落在正文与金句空白带；想贴底改小，想更高改大）。半透明黑底、底部居中。
- 烧录用 cwd 下相对路径（`ass=_burn_*.ass`）避开 Windows 盘符冒号转义。
- **抽帧 QA**：`ffmpeg -ss <t> -i out-sub.mp4 -frames:v 1 f.png` 看字体无乱码、对齐准、不压金句/关联/水印。

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
为避免污染其他日期，优先写 `scripts/_tmp_cover_<date>.py` 临时脚本，import `make_cover` 后覆盖 `BRAND/KICKER/BIG/ROWS/DATE`
再调用 `make_cover.main()`；不要直接把当天文案长期写死进 `make_cover.py`。生成后用 `view_image` 检查标题、5 行摘要、
右下角收藏贴纸是否溢出或遮挡。

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
当用户只说"正文 tag"时，直接输出：
- `正文`：无编号词"第一条/第二条"，用 5 行短句覆盖 3 新闻 + 2 论文，结尾带 `@柿子树下的猫wanjeans`。
- `Tag`：8~10 个，包含 `#人工智能 #AI #AI日报 #每日AI #AI资讯` + 当天热点 + `#柿子树下的猫`。
默认不加 emoji，除非用户明确喜欢。

### 8) 投稿（半自动 · Route B = Claude-in-Chrome 驱动创作者后台）
**只有浏览器自动化能传自定义 3:4 封面**：社区 `xiaohongshu-mcp` 的 publish 没有封面参数（会用视频首帧，
开头那张很难看），小红书对个人也无官方 API。所以投稿走 **Claude-in-Chrome 驱动 `creator.xiaohongshu.com`**。

**前置**：① Claude-in-Chrome 扩展已连接（`list_connected_browsers` 非空，否则让用户装/连）；
② 该 Chrome 已登录小红书创作者后台。

**a. 生成投稿数据**（单一数据源，从 `caption.md` + 成品文件汇出）：
```
python scripts/make_publish.py --date <date>                       # 默认 visibility=self（仅自己可见）
python scripts/make_publish.py --date <date> --visibility public
python scripts/make_publish.py --date <date> --schedule "YYYY-MM-DD HH:MM"
```
出 `output/<date>/publish.json`：`title / body / tags / content（正文+标签）/ video（-sub.mp4 绝对路径）/
cover（3:4 png 绝对路径）/ visibility / schedule_at`。**标题 >20 字会告警**，投稿前先精简到 ≤20。

**b. Claude-in-Chrome 填表**（读 publish.json）：导航到 `https://creator.xiaohongshu.com/publish/publish?from=menu`
→ 选「上传视频」传 `video` → 等转码完成 → **设置自定义封面、上传 `cover`**（别用自动截帧）→ 填 `title`（≤20 字）
→ 把 `content` 粘进正文（标签以 `#` 随正文带）→ 设可见性（`self`=仅自己可见 / 或按 `schedule_at` 定时）。

**c. 停在发布键前**：**绝不自动点「发布」**，最终确认交给用户逐条过。

**约束（已与用户敲定）**：主号 @柿子树下的猫wanjeans；**首条用「仅自己可见」或定时**；
非官方自动化有封号风险，**低频（一天最多 1 条）、人工过内容**；每次发布动作必须用户确认。

## 产物清单（一天，归到 `output/<date>/`）
- `scripts/broadcast-<date>-*.md`（A/B 文稿，含手改版）+ 上游 `samples/source-<date>.md`
- `audio/broadcast-<date>-spacex.mp3`（克隆音色，整段合成）+ `audio/durs.json`（每段卡点时长）
- `video/xhs-<date>-spacex.mp4`（4K 卡点 + 片头/片尾，无字幕基底）
- `video/xhs-<date>-spacex-sub.mp4`（**带字幕，发布用**）+ `video/subs.ass`（字幕源）
- `cover/cover-<date>.png`（3:4 封面）
- `CHANGELOG.md`（当天调整 / MD 版本 / 踩坑 / 决策）
- `caption.md`（标题 + 正文 + 标签）
- `publish.json`（投稿数据源：标题/正文/标签 + 视频&封面绝对路径 + 可见性，`make_publish.py` 生成）

## 排错速记
- 视频比音频短 ≈ 每卡少 ~1s、收尾被截：裸 `composite()` 的时长忘了逐卡 `+xhs.XFADE`（见步骤 5 ⚠️）。
- DeepSeek 401：先核对 `DEEPSEEK_API_KEY` 尾号（易多打字符）；pi 与 api 后端都受同一 key 影响。
- 豆包 `NO AUDIO RECEIVED` / 403：偶发或限流，`synth_segmented` 已自动重试；仍失败就等额度恢复。
- 末字/段末字被吞（快语速更明显）：根因是该字落在句末终止音前被匆匆收尾。修法是让**末字后接逗号**
  （连续语气读完）再用句号制造停顿——`pad_tail()` 用 `…字，。。。`；`synth_single_synced` 段间拼接用
  `，。。`（不是 `。。`）。别把逗号改回句号、别移除缓冲。
- 音色段间跳变：别用逐段拼接，改 `synth_single_synced`（整段一次合成）。
- 卡片乱码/溢出：正文太长就精简 `body`；中文按字断行在 `_wrap()`。
- ffmpeg「Error opening output」/拼接失败：多半是输出 mp3/mp4 正被用户的播放器占用（Windows 文件锁）——
  换个输出文件名（如 `-fast.mp3`）即可，或让用户关掉播放器。
- 媒体文件（mp3/mp4/片头/卡片 png）按 `.gitignore` 不入库，留本地。
