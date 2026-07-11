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

- **★ 出片走单一驱动（2026-07-11 起）**：每天只写一份 `output/<date>/episode.yaml`（卡片文案+封面文案，
  样例＝`output/2026-07-11/episode.yaml`），然后
  `python scripts/make_episode.py --date <date> [--dry-run|--force-audio]` 一条命令跑完
  字数校验→音频(复用已有不重配)→渲染→出片(+XFADE/猫头片尾)→字幕→ffprobe断言→抽帧→3:4封面→publish.json。
  **不要再手搓 `_tmp_audio/_tmp_video/_tmp_cover` 临时脚本**（每天重写引入过 XFADE 漏加、emoji 空框等随机错误）。
  内置 QA 任一失败即中止：正文 ≤820 字、icon 码位 <U+1FA70、组数=段数、成片时长=旁白+1s±0.8、2160×3840。
- **★ 正文字数硬预算 ≤820 字**（rate 36 下 ≈105-110s）：写完稿先 `make_episode.py --dry-run` 或手动 len()，
  超了当场删，别等合成才发现（2026-07-10 曾 990 字失控到 136.9s）。
- **★ 核查到源头**：每条入选新闻必须 WebFetch 到**原始出处页面**（当事人博客/原报道/研究方页面），
  不许只凭搜索摘要写稿。历次事实事故（$149.25"实付"实为折算、GLM"个人在家自建"、Discord 200 实为 8000+、
  "OpenAI 未回应"已过时）全靠这一步拦下。数字要归因到估算人；对方已回应的指控必须带上回应。
- **★ 交互收敛为每期 3 次**（2026-07-12 起）：①选题一轮（新闻+论文合并一组 AskUserQuestion）→
  ②审稿 → ③终审（稿子过审后，卡片文案由 Claude 按用户历史偏好直接定稿——内容卡多用观点/悬念驱动、
  数字版只在数字本身是爆点时用；补充卡按"每条 1-2 张、科普不复述"自选——一次性给全套让用户看，改哪张说哪张）。
  不再逐卡 3 选 1、逐条勾补充卡，除非用户主动要选项。
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
- **用户审核点＝3 个**（见★交互收敛）：选题 → 审稿 → 终审全套卡片文案；通过后 make_episode.py 一口气出片，
  出完交付时附抽帧。用户要求分步（如先听音频）时再拆。

## 前置检查

- `.env`（仓库根）含：`VOLC_APP_ID/VOLC_API_KEY/VOLC_SPEAKER2/VOLC_RESOURCE_ID`，
  改写用 `DEEPSEEK_API_KEY`（pi 后端）。注意 DeepSeek key 易手滑多打字符，401 时先核对尾号。
- ffmpeg：`make_xhs_video_html.FFMPEG` 指向的 exe 存在。
- Playwright Chromium 已装（`playwright install chromium`）。
- 改写后端：`--llm pi`（pi agent + DeepSeek）或 `--llm api`（OpenAI 兼容直连 DeepSeek）。
  pi 在 Windows 要走 `node dist/cli.js`（已在 `_pi_command()` 处理）。

## 流水线（用户审核点只有 3 个：选题 → 审稿 → 终审卡片文案）

### 1) 抓素材 + 选稿（先和用户对齐范围与风格）
**a0. 先看数据复盘**（2026-07-12 起）：读 `output/analytics-summary.md`（由
`python scripts/analyze_notes.py` 从后台导出的 `笔记列表明细表.xlsx` 生成，用户更新 xlsx 后重跑）。
截至 2026-07 的数据结论，选题和封面按这个倾斜：
- **头条优先"大主体+权力冲突+具体动作"**（白宫下令/谷歌留不住人/史上最大IPO 这类，曝光是行业观察类的 2 倍+）；
  "AI检测器/AI写码"这类无主体抽象选题 CTR 只有爆款的 1/3。
- **封面钩子必须带大牌主体名**（白宫/Claude/OpenAI/谷歌…），CTR 高的封面全符合此律。
- **中国用户强相关的选题转化效率最高**（"Claude 偷藏码盯中国用户"千曝光涨粉 8.57 全场第一、
  "阿里卸载 Claude"人均观看 94s 全场唯一近完播）。
- **人均观看只有 15-25s**：头条放全片最强内容，时长继续压（≤820 字预算不放松）。
- **发布建议早间 7-8 点定时**（早间 CTR 中位 0.070 vs 凌晨 0.049），别凌晨 2-4 点发。
- 图文体裁数据显著更好（CTR 中位 0.135 vs 视频 0.048），补充卡可周攒重组图文（第二产品线）。

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
写之前**正式走 `ai-news-podcast` 技能的完整流程**（2026-07-09 用户点名要求，敷衍"参照纪律"被否过）：
读全其 4 份 references、建事实卡、按 `evidence-levels.md` 定 E1-E5 等级、按 `quality-checklist.md` 验收。
**★ 核查到源头**：每条入选新闻 WebFetch 原始出处页面，不许只凭搜索摘要写稿（见关键约定）。
**只借这套事实核验和证据分级，不套用它的输出模板、时间戳或"换句话说"式口播腔**——语言仍按本技能的
★文风铁律写（大白话、正常语序、禁数数过场、去冒号）。
存成 `output/<date>/scripts/broadcast-<date>-B-changed.md`，**写完立刻数字数（≤820），超了先删**，
再给用户审、按批注改到满意（用户常会亲自改这份，它就是唯一源，别覆盖）。每段一空行分隔（= 一个音频段 = 一组卡）。
开场固定 `一分钟带你了解AI圈的新鲜事。`，收尾只留 `我是柿子树下的猫wanjeans，我们明天见。`。
⚠️ 合成前**删掉文末任何备注/footer**（`---` 之后的说明），否则 `split_segments` 会把它当正文读出来
（`make_episode.py` 用 `strip_header` 已处理文首 `>` 备注 + `---` 分隔，文末别再加东西）。

### 2) 卡片文案定稿（2026-07-12 起：Claude 直接出全套，一次终审）
稿子过审后，**卡片文案由 Claude 按用户历史偏好直接定稿，不再逐卡 AskUserQuestion**（交互收敛，见关键约定）：
- **内容卡**：短标题(视觉锤) + 加厚正文(塞 2 个数字/事实，`**高亮**`) + 金句。风格按历史偏好——
  多用**观点/悬念驱动**，数字版只在数字本身是爆点时用（"从2%到45%"这类）。
- **补充卡**：每条头条/论文配 1–2 张科普概念卡（解释概念，不复述新闻），**逐个 WebSearch 查证**
  （概念定义、事件经过、最新数字），写成"高中生也能懂"的 `body`（≤~60 字，`**关键数字/词**` 高亮）。
- **把全套卡片文字（含封面 hook、3:4 封面 ROWS）汇总成一版给用户终审**，改哪张说哪张，通过后写进
  `episode.yaml`。用户主动要选项时才回到旧的 3 选 1 / 多选流程。

### 3~6) 一条命令出全套（2026-07-11 起默认）：`make_episode.py`
卡片文案终审通过后，把全套数据写进 **`output/<date>/episode.yaml`**（结构照抄
`output/2026-07-11/episode.yaml`：`script`＝文稿文件名、`groups`＝封面卡/每组内容卡+补充卡/CTA、
`cover3x4`＝3:4 封面文案），然后：
```
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python scripts/make_episode.py --date <date> --dry-run   # 先校验
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python scripts/make_episode.py --date <date>             # 出全套
```
一条命令完成：字数校验(≤820)→emoji 码位校验(<U+1FA70)→TTS(整段 rate36；**音频已存在则复用不重配**，
`--force-audio` 才重合成)→渲染→出片(+XFADE 逐卡补偿、猫头片尾 circle_photo(photo,760)+center=(1080,0.24H))→
字幕(whisper 强制对齐)→ffprobe 断言(2160×3840、时长=旁白+1s±0.8)→抽 5 帧到 `video/qa/`→卡片归档→
3:4 封面→publish.json。**QA 断言任一失败即中止，不会产出坏片**。
- 跑完读 `video/qa/` 抽帧确认画面（封面钩子、高亮块、字幕落位、CTA 猫头），再交付用户。
- 音频想单独先给用户听：先跑一次（会合成音频），把 mp3 给用户，确认后不动音频继续。
- 旧手工路径（逐步骤 `_tmp_*` 脚本）已废弃，仅当 make_episode.py 不能覆盖的特殊需求（如带片头）才回退；
  片头路径见 `references/card-design.md` 与 `build_xhs_video(intro_path=...)`。

**实现细节备查**（make_episode.py 内部即这套已验证做法；手工回退时才需要）：
- 音频＝`run_daily.synth_single_synced`（整段一次合成音色统一）；语速 `VOLC_SPEECH_RATE=36`≈1.25×。
- 片尾＝`circle_photo(photo,760)` + `place_photo_on_card(center=(1080,int(0.24*3840)))` +
  `composite([d+XFADE...])` + `build_shrink_outro(dur=1.0)` + `concat_clips`。
  裸 `composite()` 逐卡必须 `+XFADE`（漏加则视频比音频短、收尾被截）。
- 字幕＝`add_subtitles(segs, durs, ...)`，whisper(base) 词级强制对齐脚本原文，样式
  `SUB_FONT/SUB_FONTSIZE/SUB_MARGINV`（微软雅黑 82 / MarginV=820），烧录用 cwd 相对路径避开盘符冒号。
- 3:4 封面＝episode.yaml 的 `cover3x4`（BIG 要爆点钩子，别用"今日N件大事"；ROWS 5 行速览，`**…**` 标红）。
- 全自动兜底（无补充卡、同日期）：`python scripts/run_daily.py --date <date> --modes concise --video`。

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
**论文传送门给具体链接**（2026-07-11 用户要求）：查证后写 arXiv 编号（`arxiv.org/abs/26xx.xxxxx`）或
官方仓库/项目页；查不到编号就给仓库链接，**绝不硬编编号**，也不再用"搜标题可达"兜底。
⚠️ caption.md 的 `## 标题` 节首行就是标题本体，别写"- A（选用）：…"选项列表（make_publish 会整行当标题）；
备选标题放文末单独一节。

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
- **卡片 icon 渲染成空框**：emoji 码位 ≥U+1FA70（Unicode 12+，如 🫥🫓）渲染字体不支持——
  make_episode.py 已内置拦截；手工路径时 icon 只用老码位常见 emoji（💔🍞📮⚖️🎮 这类）。
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
