# 2026-07-03 AI Briefcast

## Scope
- 内容：3 新闻（7/2 资讯）+ 2 论文（7/2 简报）；无片头 + 猫图圆形片尾；带字幕（字号 96）；语速 1.25×（rate 36）。
- 第一帧即封面，大字钩子「Cloudflare / 逼AI / 为内容付费」（逼AI 红）。

## Selection（AskUserQuestion 选 + 核实）
- ⚠️ 7/2 资讯头条是 Fable 5 回归 + Claude Code 隐写标记，**已在 7/2 视频做过，本期主动排除、不重复**。
- 新闻 3 条（均 web 核实）：
  ① 头条 Cloudflare 逼 AI 为内容付费：给 AI 公司 9/15 期限，把搜索爬虫与训练/agent 爬虫分开，否则在带广告页面默认屏蔽；推「按使用付费」（内容产生价值才收钱，初期伙伴 Ceramic.ai/You.com）。适用新客户/新站点/所有现有免费用户。
  ② OpenAI 给欧盟岗位画自动化地图（The AI Jobs Transition Framework for the EU，延续 4 月美国版）：18% 高自动化风险 / 24% 流程重排 / 12% 增长 / 46% 短期变化不大（ESCO 分类 + Eurostat）；德/希/意风险高，卢/瑞/荷更偏增长。
  ③ Netflix《The Golden Ticket》真人秀（9/23 上线）旁白用 AI 合成已故演员 Gene Wilder 声音，技术方 ElevenLabs，**经遗产方/家人同意**（遗孀 Karen Wilder "delighted"）。
- 论文 2 篇（7/2 简报，未报过）：① GBC：多 agent 系统跑砸时定位该改哪个 agent，把系统建成计算图、错误信号沿交互链反传、token 级归因（arxiv 2606.28187）② 像素空间 AR（Parallel Rollout Approximation）：绕过 tokenizer 直接 pixel-in/pixel-out，先预测低维中间态再细化压误差（arxiv 2606.27978）。

## 文稿（B · 用户"继续"确认）
- `scripts/broadcast-0703-B.md`：原资讯语序较绕，**大量重写**为正常主谓宾语序。文风＝0623–0702 定稿；**禁用"不是X而是Y / 而是"**、不用"："/"——"、不报硬日期（未来期限用"九月中"软说法）。
- 长度 **123.2s**（用户"继续"，未压）。
- 音频 `audio/broadcast-2026-07-03-spacex.mp3` + `durs.json` `[2.14,26.97,23.24,22.71,23.03,22.45,2.7]`（7 段卡点，整段合成）。

## 卡片（15 张，交互式选卡）
- 内容卡 5：Cloudflare逼AI付费 / OpenAI画欧盟岗位图 / AI复活已故演员配音 / 多agent出错该改谁 / 画图省掉分词器。配色 c1/c3/c4/c5/c2。
- 补充卡 8（用户勾选 + 查证）：爬虫 crawler / Cloudflare 是谁（头条）；自动化风险啥意思（OpenAI）；AI 语音克隆（Netflix）；多智能体系统、计算图/反向传播（GBC）；tokenizer 分词器、自回归生成（像素AR）。同新闻同色分组。

## 视频 / 封面 / 文案
- `video/xhs-2026-07-03-spacex-sub.mp4`（发布用）+ `video/xhs-2026-07-03-spacex.mp4`（无字幕基底）+ `video/subs.ass`。
- ffprobe：**2160×3840、30fps、124.29s**（123.2 旁白 + 1s 片尾）。字幕 whisper 对齐 817↔859 字、73 行。
- 封面卡（第一帧）兼作小红书自定义封面（`cards/card-1.png`）；另出独立 3:4 封面 `cover/cover-2026-07-03.png`（2160×2880，逼AI 红）。
- 标题（推荐）：「AI白嫖内容的日子，要到头了」。`caption.md` 无 emoji + 含论文链接（GBC 2606.28187、像素AR 2606.27978）。

## 踩坑
- 封面/内容卡大字钩子含长英文词（Cloudflare）易撑爆换行：钩子改 3 行「Cloudflare / 逼AI / 为内容付费」，封面目录缩短到 ≤8 全宽字避免孤字。

## TODO
- publish.json + 投稿（半自动；首条建议仅自己可见、逐条确认）。
