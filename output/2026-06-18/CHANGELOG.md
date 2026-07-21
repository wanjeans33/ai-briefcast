# 2026-06-18 AI Briefcast

## Scope

- 内容日期：使用 **6/17 新闻与论文**，生成 6/18 小红书 AI 速览。
- 形态：3 新闻 + 2 论文；片尾圆猫；**带字幕**；**语速 1.25×（rate 36）**；**目标 ≤100s**。
- 原始素材：`samples/source-2026-06-17.md`
  - digest: https://ai-digest.liziran.com/zh/digest/2026-06-17-spacex-pours-60-billion-fresh-stock-into-cursor-days-after.html
  - brief : https://ai-brief.liziran.com/zh/daily/2026-06-17-agent-memory-forgetting-truthful-heads-event-forecasting.html

## 本期三处用户要求

1. **修字幕断句**（昨天反馈：断在词中间，如"官网或/网页"）：重写 `make_xhs_video_html.subtitle_lines`——
   只在标点（逗号/顿号/分句）处断、句末强制收行、单子句超宽才在助词后折；改用**视觉宽度**（英文/数字半宽）
   判断，最宽 22 全宽字，字号 82→78。验证 6/17 脚本：行数 62→53，"AI Mode"/"三千九百七十亿参数大模型"
   不再被切。6/18 实跑断句全部落在标点处（"Claude Sonnet 3.5""IDE"整词不切）。
2. **语速 1.25×**：`VOLC_SPEECH_RATE=36`（≈1.25×，介于 rate 30≈1.19× 与 50≈1.4× 之间）。
3. **≤100s**：脚本按 1.25× 估偏长，迭代删稿 106s→102s→**88.7s** 定稿（豆包测时单段缩放有 ±10% 波动，
   102 那版用 ×1.056、88.7 用 ×0.948，留足余量稳进 100）。

## Selection（用户确认）

- 新闻 3 条：① SpaceX 600 亿全股票收购 Cursor（救掉队 AI 部门，自称面对 26 万亿市场）/
  ② ChatGPT 份额首破 50%（月活 11 亿；Gemini 6.62 亿、Claude 2.45 亿）/ ③ 五角大楼用 AI 代写国会报告（150 万人在用）。
- 论文 2 篇：牛津 1.5B 小模型事件预测赢过 Claude Sonnet 3.5（GRPO+工具）/ MIT 记忆遗忘根因在架构位置（挂改写端九成以上）。
- 主线「大≠赢」。

## 产物

- `audio/broadcast-2026-06-18-spacex.mp3`（1.25×）+ `audio/durs.json` `[2.0,16.3,13.6,13.8,16.5,15.2,11.4]`（总 88.7s）。
- `cards/`（12 张：封面+5 内容卡+5 补充卡+CTA，色 c1/c3/c4/c5/c2）+ `cards.json`。
  - 5 补充卡 WebSearch 查证：全股票收购 / 月活 vs 份额 / 法定报告 / 事件预测 / 记忆召回端 vs 改写端。
- `video/xhs-2026-06-18-spacex.mp4`（无字幕基底）/ **`xhs-2026-06-18-spacex-sub.mp4`（带字幕，发布用）** + `video/subs.ass`。
  - ffprobe：2160×3840、时长 89.7s（88.7 旁白 + 1s 片尾）。

## Cover + 文案

- `cover/cover-2026-06-18-spacex.png`（3:4，BIG「600 亿 买 Cursor」，5 行以 SpaceX 领头）。
- `caption.md`：标题「造火箭的 SpaceX，600 亿买下写代码的 Cursor」；正文无 emoji；标签 9 个（热点 #SpaceX #ChatGPT #大模型）。
