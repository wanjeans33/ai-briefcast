# 2026-06-21 AI Briefcast

## Scope
- 内容日期：使用 **6/20 新闻与论文**，生成 6/21 小红书 AI 速览。
- 形态：3 新闻 + 2 论文；无片头 + 猫图片尾；带字幕（字号 96）；语速 1.25×（rate 36）；目标 ≤100s。
- 原始素材：`samples/source-2026-06-20.md`
  - digest: https://ai-digest.liziran.com/zh/digest/2026-06-20-barret-zoph-exits-openai-five-months-engineers-say-ai.html
  - brief : https://ai-brief.liziran.com/zh/daily/2026-06-20-omniagent-long-video-uniform-diffusion-memory-gap.html

## Selection（用户确认）
- 新闻 3 条：① OpenAI 旋转门（Barret Zoph 5 个月二进二出 / Transformer 作者 Noam Shazeer 加盟 / 电影《Artificial》被亚马逊弃）/
  ② "AI 让工程更省事"一线相反，纪律只多不少、先失控的是账单 / ③ 2B 做 10B 级修图 + Subquadratic 称破十年数学瓶颈，都在拆算力墙。
- 论文 2 篇：OmniAgent（长视频不必逐帧看，7B 在 LVBench 50.5% 反超 72B Qwen）/ Turing-RL（用户模拟器目标从"像那句话"改"像一个人"，图灵测试式奖励）。

## 文稿（B · 用户偏好定稿，多轮重写）
- `scripts/broadcast-0621-B-changed.md`。用户反馈后**整篇通俗化重写（v3→v6）**：① 大白话、正常主谓宾，**不用被动、不倒装**；
  ② **去掉"旋转门/门轴"比喻**（卡1/封面/标题一并去掉）；③ 不用"第三件/第四件"数数式过场，改"先说/再说/省钱这边/论文这边/另一篇"自然起句；
  ④ 配生活化比喻（"AI 一下端出十道菜，你把关更重""看长片只抓关键情节"）；⑤ 收尾只留署名。
- 长度（⚠️豆包测时 run 间有 ±7% 浮动）：v4 97.8s → v5 93.3s → **v6 压到约 550 字 = 88.4s 旁白**，稳进 90s。
- 音频 `audio/broadcast-2026-06-21-spacex.mp3`（克隆音色 S_HHgApOH42，整段一次合成）+
  `audio/durs.json` `[2.1,15.7,17.3,15.0,17.4,18.4,2.6]`（总 88.4s，7 段卡点）。

## 卡片（17 张，交互式选卡 AskUserQuestion）
- 内容卡「3 选 1」：卡1=①观点「OpenAI 旋转门」/「门轴几乎没停过」、卡2=①观点「AI 没让你更轻松」/「先失控的是账单」、
  卡3=②数字「2 亿干 100 亿的活」/「都在拆算力墙」、卡4=①反差「7B 反超 72B」/「会挑着看就赢」、卡5=③提问「怎么算像真人？」/「过得了图灵测试」。
  - 卡1 去旋转门后改为：标题「OpenAI 人事变动」/ 金句「走了又来没消停」/ 正文也去掉被动（"亚马逊也弃了"）。
- 补充卡「候选池多选」共 10 张（每条 2 张），逐个 WebSearch 查证：Transformer / 电影《Artificial》（亚马逊投 OpenAI 500 亿、怕利益冲突弃片）/
  不可变基础设施 / 代码审查 / 扩散模型 / 参数多≠更强 / LVBench（近两小时长视频基准，Z.ai 出）/ 文本记忆 / 图灵测试 / 用户模拟器。
  - 注：卡5 用户原勾"多模态"与 Turing-RL 不搭，改用"用户模拟器"。
- 同新闻同色分组 c1/c3/c4/c5/c2；组内权重 内容卡 1.5、补充卡 1.0。

## 视频 / 封面
- `video/xhs-2026-06-21-spacex-sub.mp4`（发布用，带字幕）+ `video/xhs-2026-06-21-spacex.mp4`（无字幕基底）+ `video/subs.ass`。
  - ffprobe：**2160×3840、30fps、89.47s**（88.4 旁白 + 1s 片尾，≤90）。字幕 whisper 对齐 568↔571 字、50 行。
- 片尾圆形猫照 1s 缩小消失；字幕字号 96。
- 封面 `cover/cover-2026-06-21-spacex.png`（3:4，BIG「OpenAI 人事大变动」，5 行以 OpenAI 领头）。

## 标题 + 文案 + 投稿
- 标题（去旋转门，18 字）：「OpenAI 人事大变动，高管来去匆匆」。
- `caption.md`：正文无 emoji、五条短句、结尾 @柿子树下的猫wanjeans；标签 10 个（热点 #OpenAI #大模型 #AI编程）。
- `publish.json`：`make_publish.py` 生成。投稿仍半自动（Claude-in-Chrome 填表，视频/封面需用户在系统框选，见 memory）。
