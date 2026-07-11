# 2026-07-02 AI Briefcast

## Scope
- 内容：3 新闻（7/1 资讯）+ 2 论文（7/1 + 6/30 简报）；无片头 + 猫图圆形片尾；带字幕（字号 96）；语速 1.25×（rate 36）。
- 第一帧即封面，大字钩子「Claude偷藏码 / 封禁中国用户」（封禁 红）。

## Selection（用户指定头条 + AskUserQuestion 选 + 核实）
- 新闻 3 条：
  ① 头条（用户指定）Claude Code 隐写标记：安全研究员逆向 2.1.196，发现仅当 ANTHROPIC_BASE_URL 指向非官方（硬编码的中国域名/AI 实验室关键词/转售网关）且系统时区为 Asia/Shanghai|Urumqi 时，把系统提示里日期的撇号/分隔符换成肉眼难辨的 Unicode 变体，给请求打隐形指纹。冲上 HN 第一（605 赞），Anthropic 在 2.1.197 悄悄移除（changelog 未提）。
  ② Fable 5 回归（用户指定）：Anthropic 最强公开模型，6/12 与 Mythos 5 因网络安全风险被美商务部施加出口管制下线（起因亚马逊发现越狱），6/30 解除管制、7/1 全球恢复（Claude.ai/Platform/Code/Cowork），回归为加固版（护栏更强、更会中止高风险网络安全任务）。
  ③ 35B 小模型摸万亿级（选）：Agents-A1（35B MoE）靠 scaling the horizon（拉长任务链、平均轨迹 45 步）追到万亿参数级；开源 Ornith-1.0 走自搭脚手架。
- 论文 2 篇（未报过）：① OSWorld 2.0：人类中位 1.6h/318 次操作的长任务基准，最强 Claude Opus 4.8 只完成两成（arxiv 2606.29537）② Agentic Abstention：把"该知道何时停手/主动弃权"单拎成一项该考核的能力（arxiv 2606.28733）。

## ⚠️ 事实核查与编辑决定（重要，留档）
- 头条我 web 多源核实（thereallo.dev 原帖 / TechTimes / The Hacker News / cybersecuritynews / aiweekly）：该机制是**隐写"标记/指纹"**，用于**识别**走非官方中国转售通道 + 中国时区的请求，**不封号、不影响功能**；无任何来源支持"封号/大面积封号"。
- 用户手改稿把头条改为"给这条请求打上一个隐形标记，**并依此大面积封号**"。我已明确指出该句与所有来源冲突、属未经证实的严重指控并有风险，用户经 AskUserQuestion **选择"保留我的写法"**。据"用户手改稿最高优先级"，音频/卡片/封面/文案均按用户口径（含"封号"）产出。此为用户编辑决定，非核实结论。

## 文稿（B · 用户定稿）
- `scripts/broadcast-0702-B.md`：原资讯语序较绕，**大量重写**为正常主谓宾语序；用户手改（缩短 Fable 5/35B 两段、头条改用"封号"口径）。文风＝0623–0701 定稿；**禁用"不是X而是Y / 而是"**、不用"："/"——"、不报硬日期。
- 长度 **109.1s**（用户手改后自然落点，未再压）。
- 音频 `audio/broadcast-2026-07-02-spacex.mp3` + `durs.json` `[2.27,24.38,16.07,21.96,19.51,22.24,2.7]`（7 段卡点，整段合成）。

## 卡片（13 张，交互式选卡）
- 内容卡 5：Claude偷藏隐形标记 / Fable 5 加固回归 / 35B小模型摸万亿级 / 长任务只做完两成 / AI得知道何时停手。配色 c1/c3/c4/c5/c2。
- 补充卡 6（用户勾选 + 查证）：隐写术 / base_url 接口地址（头条）；越狱 jailbreak（Fable5）；参数量是什么（35B）；computer-use agent（OSWorld）；主动弃权 abstention（Abstention）。同新闻同色分组。

## 视频 / 封面 / 文案
- `video/xhs-2026-07-02-spacex-sub.mp4`（发布用）+ `video/xhs-2026-07-02-spacex.mp4`（无字幕基底）+ `video/subs.ass`。
- ffprobe：**2160×3840、30fps、110.16s**（109.1 旁白 + 1s 片尾）。字幕 whisper 对齐 793↔815 字、64 行。
- 封面卡（第一帧）兼作小红书自定义封面（`cards/card-1.png`）；另出独立 3:4 封面 `cover/cover-2026-07-02.png`（2160×2880，封禁 红）。
- 标题（推荐）：「Claude被扒偷藏码，专盯中国用户封号」。`caption.md` 无 emoji + 含论文链接（OSWorld 2.0 2606.29537、Agentic Abstention 2606.28733）。

## TODO
- publish.json + 投稿（半自动；首条建议仅自己可见、逐条确认）。
