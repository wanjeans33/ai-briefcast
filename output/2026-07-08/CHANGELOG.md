# 2026-07-08 AI Briefcast

## Scope
- 内容：3 新闻 + 2 论文（均来自 liziran 7/7，逐条联网核实）；无片头 + 猫图圆形片尾；带字幕；
  语速 1.25×（rate 36）。

## Selection（AskUserQuestion 选 + web 核实）
- 用户对头条候选"Willison $149.25"先提问（误读成飞书/欧元），解释清楚计费来龙去脉后选定它当头条。
- 新闻 3 条：
  ① 头条 Willison 花 $149.25 让 Fable 收尾 sqlite-utils 4.0（37 prompts/34 commits/+1321-190/30 文件，
    rc2 7/5 发布；背景＝Fable 从 Max 订阅移出改按量计费）。
  ② Google 默认拿搜索上传数据训练 AI（Web & App Activity 拆出独立 Search data 开关默认开；
    Lens/Search Live/翻译音频都存；关闭＝搜索服务历史设置取消 Save Media）。
  ③ 美国富人送孩子上 AI 学校（Alpha 奥斯汀 2 小时 AI 辅导+项目制、最高 $75k/年、无成绩数据；
    WIRED/404media 曝辅导员为菲/哥远程零工无教师资格）。
- 头条 03「Anthropic 被指追踪中国用户」与 7/5 期重叠且停在指控层面，用户未选。
- 论文 2 篇：GLLS（training-free 可验证工业质检）/ MPSelectTune（最坏提示选择改进概念遗忘）。

## 文稿 / 音频
- `scripts/broadcast-0708-B-changed.md`：文风铁律 + 证据纪律。
- ⚠ **头条 $149.25 口径纠正（用户追问后核实原文 simonwillison.net）**：Willison 用的是 Max 包月
  （$200/月），此单**没有实际掏钱**；149.25 是他事后用 AgentsView 按 API 单价折算的估价
  （"if I had been paying those costs directly"）。口播/卡片一律写"折算值 149.25 美元 / 包月里没另掏钱"，
  **不写"花了/账单/明码标价"**（liziran digest 原文的"明码标价账单"框架是误导，弃用）。文稿+卡片已按此改。
- 音频 `audio/broadcast-2026-07-08-spacex.mp3` **109.3s**（rate 36 整段合成一次）+ `durs.json`
  `[1.9,29.8,19.6,20.7,19.0,15.5,2.7]`。比 7/7（120.6s）短 11s，主动收紧稿子的结果。

## 卡片（17 张，交互式选卡）
- 内容卡 5：37条指令值149美元(数字) / 默认是最大的权力(观点) / 富人的孩子AI在教(悬念) /
  大模型进不了工厂(悬念) / AI忘掉的换个问法又回来(悬念)。配色 c1/c3/c4/c5/c2；GLLS 组 4 卡、遗忘组 2 卡。
- 补充卡 10（逐个 web 查证）：开源维护者、包月vs按量；默认勾选套路、AI要照片语音的原因；
  7.5万学费概念(≈54万RMB/顶级寄宿名校)、AI家教证据(两个标准差结论+实测缩水)；工业质检、可解释AI、few-shot；
  换问法套话攻击。
- 封面卡 hook「AI干活 值多少钱」（按纠正口径，不写账单/花了）。

## 视频 / 封面 / 文案
- `video/xhs-2026-07-08-spacex-sub.mp4`（发布用）+ 无字幕基底 + `subs.ass`（62 行，whisper 对齐 731↔736 字）。
- ffprobe：**2160×3840、30fps、110.33s**（109.3 旁白 + 1s 片尾）。抽帧 QA 通过。
- 封面 `cover/cover-2026-07-08.png`（3:4 2160×2880），BIG=「AI干活 值多少钱」。
- 标题「AI干活值多少钱，第一次算清了」（15 字）；论文只给可搜标题（GLLS/MPSelectTune 未查到 2607 arXiv
  编号，caption 用"搜标题可达"，不编号）；`publish.json` visibility=self。

## 踩坑（留档）
- 沿用 7/7 教训，本期 icon 全部用老码位 emoji（🧾💻🍱🔓☑️📸🎓💵📚🏭🔎📋🎯🕳️🎭），未再出现空框。
- 论文 arXiv 编号查证：GLLS、MPSelectTune 均未查到明确的 2607.xxxxx 编号（MPSelectTune 见于 OpenReview），
  故 caption 不硬编号，改"搜标题可达"，避免编错。

## TODO
- 用户自行上传（publish.json 已备好；首条建议仅自己可见）。
