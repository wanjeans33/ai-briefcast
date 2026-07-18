# 2026-06-24 AI Briefcast

## Scope
- 内容：3 新闻 + 2 论文；旁白**不报任何具体日期**（用户要求）；无片头 + 猫图圆形片尾；带字幕（字号 96）；语速 1.25×（rate 36）。
- 封面做进视频、**视频第一帧即封面**，大字钩子「谷歌市值蒸发 2250 亿」（用户指定）。

## Selection（用户给定 + 核实）
- 新闻 3 条（用户给题，逐条网络核实均 6/22 发布）：
  ① 五眼联盟（美英加澳新）罕见联合声明《The AI shift in cyber risk》，警告前沿 AI 数月内大幅增强黑客攻击力 /
  ② 谷歌人才流失（Jumper→Anthropic、Shazeer→OpenAI）致 Alphabet 单日最多跌 7%、蒸发约 **2250 亿美元（$225B）**，史上最大单日市值损失 /
  ③ Anthropic 与内存芯片大厂美光签战略协议（多年供货 + 共设 AI 内存架构 + 美光参投 Series H）。
- 论文 2 篇：⚠️ 用户首选的"榜单 predictive validity"和"ENPIRE 机器人"**经查均已在 6/22 报过** → 全部更换。
  改用 liziran 6/19–6/20 简报里**此前未报过**的两篇：
  GameCraft-Bench（AI 在 Godot 引擎里从头做能玩的游戏，多模态评委回放打分）/ Xcientist「Research Harness」（AI 科研每一步留可查证据，治 claim drift）。
- 选题教训追加：跨期补论文时必须先扫 output/<近几日>/scripts 去重——liziran 简报会跨天回收同一批论文。

## 文稿（B · 用户多轮修改定稿）
- `scripts/broadcast-0624-B.md`：文风以 0623-B-changed 为基础。用户多轮要求：去掉所有具体日期；五眼简介缩短为"五眼联盟"；谷歌段不重复人名去向；美光段以 Anthropic 起头；**全程禁用"不是X而是Y"句式**。
- 顺序：五眼 → 谷歌市值 → 美光×Anthropic → 游戏论文 → 科研论文。
- 音频 `audio/broadcast-2026-06-24-spacex.mp3` + `audio/durs.json` `[1.98,16.92,13.16,13.88,27.94,27.86,2.68]`（7 段卡点，整段一次合成）。**总长 104.4s**（两篇论文段各 ~28s 偏长，用户接受完整版）。

## 卡片（17 张，交互式选卡）
- 内容卡 5：五眼联盟罕见警告 / 谷歌一天蒸发2250亿 / Anthropic 绑定美光 / AI能做出能玩的游戏吗 / AI做科研也要留证据。配色 c1/c3/c4/c5/c2。
- 补充卡 10（用户 AskUserQuestion 勾选 + 逐条联网查证）：五眼联盟 / 钓鱼与恶意软件 / Alphabet与谷歌 / 2250亿有多大 / 美光是谁 / 内存墙 / 游戏引擎Godot / 多模态评委 / AI科学家 / claim drift。同新闻同色分组。

## 视频 / 封面
- `video/xhs-2026-06-24-spacex-sub.mp4`（发布用）+ `video/xhs-2026-06-24-spacex.mp4`（无字幕基底）+ `video/subs.ass`。
- ffprobe：**2160×3840、30fps、105.47s**（104.4 旁白 + 1s 片尾）。字幕 whisper 对齐 726↔738 字、64 行，MarginV=820 不压金句。
- 封面卡（第一帧）大字钩子「谷歌市值蒸发2250亿」+ 今日 5 条目录；`cards/card-1.png` 兼作小红书自定义封面。

## TODO（下一步）
- 标题 + 正文 + 话题标签（caption.md）；publish.json；投稿（半自动）。
