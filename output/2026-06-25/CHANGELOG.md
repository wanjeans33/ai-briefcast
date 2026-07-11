# 2026-06-25 AI Briefcast

## Scope
- 内容：3 新闻（来自 6/24 资讯，头条网络补）+ 2 论文（liziran 6/23 简报）；无片头 + 猫图圆形片尾；带字幕（字号 96）；语速 1.25×（rate 36）。
- 第一帧即封面，大字钩子「一条河豚 / 指挥一群AI」。

## Selection（用户给定 + 交互选择 + 核实）
- 头条用户指定：Sakana **Fugu（河豚）**编排模型 —— liziran 6/24 未收录，网络补（6/22 发布，属"突发新闻当头条"）。
  核实：东京 Sakana AI（2023，Transformer 作者 Llion Jones 任 CTO），一个 API 后台调度 Claude/GPT/Gemini；Fugu Ultra 号称比肩 Fable 5，但上线 24h 内 Ethan Mollick 等实测出跑分≠实用。
- 其余 2 新闻（用户 AskUserQuestion 选）：AI 泡沫成本账（每挣1美元或倒贴8–14美元，红杉收入缺口 2000→6000 亿）/ Claude Code 加密"思考"日志本机读不到（开发者 Patrick McCanna 实测，600 字符加密签名、要原文须签企业协议）。
  ⚠️ "8–14美元"按"独立分析估算"口径写，不写成定论。
- 论文 2 篇（用户选，liziran 6/23 简报，均未报过）：Signal Dilution（多轮 agent 贵在关键决策太稀）/ CoPT-AIL（先 BC 预训练再对抗模仿，首次补理论：动作+奖励一起预训练）。

## 文稿（B · 用户定稿）
- `scripts/broadcast-0625-B.md`：原资讯语序较绕，按用户要求**大量重写**为正常主谓宾语序。文风＝0623/0624 定稿；**禁用"不是X而是Y"**；不报硬日期（用相对时间）。
- v1 全量 116s 偏长 → 用户选"压短"，五段各砍一两句 → **v2 = 92.2s**（更贴"1分钟"口径）。
- 音频 `audio/broadcast-2026-06-25-spacex.mp3` + `durs.json` `[2.28,17.69,17.8,14.7,18.27,18.36,3.1]`（7 段卡点，整段一次合成）。

## 卡片（16 张，交互式选卡）
- 内容卡 5：河豚:一个AI当总指挥 / 每挣1块倒贴8到14块 / 你读不到AI的思考 / 训AI为啥这么烧钱 / 老技巧终于有了证明。配色 c1/c3/c4/c5/c2。
- 补充卡 9（用户 AskUserQuestion 勾选 + 联网查证）：编排模型 / Sakana AI / 为何越用越亏 / AI 泡沫之争 / 思考链 / 审计链 / 提示注入 / 训练为何这么贵 / 奖励函数。同新闻同色分组。

## 视频 / 封面
- `video/xhs-2026-06-25-spacex-sub.mp4`（发布用）+ `video/xhs-2026-06-25-spacex.mp4`（无字幕基底）+ `video/subs.ass`。
- ffprobe：**2160×3840、30fps、93.27s**（92.2 旁白 + 1s 片尾）。字幕 whisper 对齐 615↔625 字、55 行，MarginV=820。
- 封面卡（第一帧）大字钩子「一条河豚 / 指挥一群AI」+ 今日 5 条目录；`cards/card-1.png` 兼作小红书自定义封面。

## 标题 + 文案
- 标题（推荐）：「日本河豚模型，一个AI指挥一群AI」。`caption.md` 正文无 emoji；标签含 #SakanaAI #AI泡沫 #Anthropic。
- 论文链接：Fugu 基于 TRINITY + Conductor（ICLR 2026）；Signal Dilution = Drowning in Routine（Mila）；CoPT-AIL = Provably Efficient Policy-Reward Co-Pretraining for Adversarial Imitation Learning。

## TODO
- publish.json + 投稿（半自动）。如需独立 3:4 封面可仿 6/24 用 make_cover 出一张。
