# 2026-06-27 AI Briefcast

## Scope
- 内容：3 新闻（6/26 资讯，头条用户指定）+ 2 论文（liziran 6/26 简报）；无片头 + 猫图圆形片尾；带字幕（字号 96）；语速 1.25×（rate 36）。
- 第一帧即封面，大字钩子「Claude / 当你同事了」。

## Selection（用户指定头条 + AskUserQuestion 选 + 核实）
- 头条用户指定：**Anthropic Claude Tag**（6/23 发布，网络补）—— 常驻 Slack 的 AI 同事，有身份和记忆、@它派活分步做、按权限调工具；企业版/团队版 beta，8/3 下线旧版 Claude in Slack。亮点：Anthropic 自家团队用内部版生成 **65%** 代码（含 Claude Tag 自身大半代码）。
- 其余 2 新闻（用户 AskUserQuestion 选）：
  - OpenAI **GPT-5.6** 发布得先过白宫：特朗普政府以（网络）安全为由要错峰、限量、逐客户放行——**美国政府头一回在发布前限制本国 AI 公司**；Altman 称长久不可持续。GPT-5.6 被视为在网安能力上与 Anthropic Mythos 相当。
  - **Notion** 关停 Notion Mail（9/22）：过半用户压根不开收件箱、全交给 agent，公司"全押 agent 管邮箱"；Gmail 双向同步、邮件不丢。
- 论文 2 篇（liziran 6/26 简报，均未报过）：Confident Layer Decoding（末层"对齐税"把对的改错，提前在置信层解码，training-free、延迟<2%）/ Tmax（终端 agent 卡在题库与数据非算法，outcome-only RL，9B 在 Terminal-Bench2.0 拿 27% 反超更大模型）。

## 文稿（B · 用户定稿）
- `scripts/broadcast-0627-B.md`：原资讯语序较绕，按用户要求**大量重写**为正常主谓宾语序。文风＝0623–0626 定稿；**禁用"不是X而是Y"**、不用"："/"——"、不报硬日期。
- 长度 **109.6s**，用户默认"就这样"（未压缩）。
- 音频 `audio/broadcast-2026-06-27-spacex.mp3` + `durs.json` `[2.11,19.93,21.32,18.13,22.37,22.98,2.73]`（7 段卡点，整段合成）。

## 卡片（15 张，交互式选卡）
- 内容卡 5：Claude住进你的Slack / 发模型得先问白宫 / 没人开收件箱了 / 最后几层把对的改错 / 训AI卡在没好题。配色 c1/c3/c4/c5/c2。
- 补充卡 8（用户勾选 + 查证）：Claude Tag / 怎么干活 / 政府为何插手 / 头一回预先限制 / agent怎么管邮箱 / 对齐税 / 命令行agent / 关键在造题。同新闻同色分组。

## 视频 / 封面 / 文案
- `video/xhs-2026-06-27-spacex-sub.mp4`（发布用）+ `video/xhs-2026-06-27-spacex.mp4`（无字幕基底）+ `video/subs.ass`。
- ffprobe：**2160×3840、30fps、110.59s**（109.6 旁白 + 1s 片尾）。字幕 whisper 对齐 754↔758 字、62 行。
- 封面卡（第一帧）兼作小红书自定义封面（`cards/card-1.png`）。
- 标题（推荐）：「Claude现在能当你同事了」。`caption.md` 无 emoji + 含官方/论文链接（Claude Tag 官方介绍、置信层 2606.21906、Tmax 2606.23321）。

## TODO
- 如需独立 3:4 封面，仿前几日用 make_cover 出一张。
- publish.json + 投稿（半自动）。
