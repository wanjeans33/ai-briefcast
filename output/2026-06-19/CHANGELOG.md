# 2026-06-19 AI Briefcast

## Scope
- 内容日期：使用 **6/18 新闻与论文**，生成 6/19 小红书 AI 速览。
- 形态：3 新闻 + 2 论文；**无片头 + 猫图片尾**；**带字幕（放大到 96）**；**语速 1.25×（rate 36）**；目标 ≤100s。
- 原始素材：`samples/source-2026-06-18.md`
  - digest: https://ai-digest.liziran.com/zh/digest/2026-06-18-leaked-audited-books-show-openai-lost-385-billion-2025.html
  - brief : https://ai-brief.liziran.com/zh/daily/2026-06-18-context-pruning-cache-cost-reward-distillation.html

## Selection（用户确认）
- 新闻 3 条：① OpenAI 去年净亏 385 亿美元（审计版坐实，调轻后的数，原始总亏 603 亿）/
  ② 仅 16% 美国人信 AI 让社会变好（皮尤；67% 不信政府监管；近半在用，两年前 33%）/
  ③ G7 上马克龙、莫迪担心美国"一键关停"AI（Anthropic 封停成真）。
- 论文 2 篇：TokenPilot（删 context 触发缓存失效、反而更贵，降本 56%–87%）/
  Quality-Utility 悖论（挑 reward 最高数据蒸馏小模型反更差，分布漂移）。
- 主线「光鲜 AI 背后，都是还没算清的账」。

## 文稿（B 沉稳串点 · 用户手改定稿）
- 选 B 版。手改要点（`scripts/broadcast-0619-B-changed.md`）：**去掉所有「：」「——」**，一句一意、每句说清楚，
  语序理顺（先因后果、先事实后点评）。
- 长度迭代：v1 全清晰版 **105.7s 超标** → v2 微删冗余连接/次要细节 → **v3 收尾只留署名**
  （删掉"还没算清的账"总结段，按用户要求）→ 终版 **84.1s**。
- 音频 `audio/broadcast-2026-06-19-spacex.mp3`（克隆音色 S_HHgApOH42，整段一次合成）+
  `audio/durs.json` `[1.99,16.60,15.13,15.59,17.35,14.97,2.45]`（总 84.1s，7 段卡点）。

## 卡片（15 张，交互式选卡）
- 内容卡「3 选 1」（AskUserQuestion）：卡1=②数字「净亏385亿」/「调轻后真账603亿」、卡2=①观点「嘴上不信」/「身体却很诚实」、
  卡3=①观点「开关在别人手里」/「命门在外」、卡4=③提问「删了反而亏？」/「乱删触发缓存失效」、卡5=②数字「reward高≠最优」/「分布漂移抬高成本」。
- 补充卡「候选池多选」共 8 张，逐个 WebSearch 查证后写：审计与独立核对 / 营收涨还巨亏 / 皮尤研究中心 /
  AI 主权（卡脖子）/ 提示缓存 prompt cache / AI agent / 知识蒸馏 / 奖励分 reward。
- 同新闻同色分组：c1/c3/c4/c5/c2。组内权重 内容卡 1.5、补充卡 1.0。
- 封面 count=5 + 5 行目录；CTA 暗色 c7 放圆形猫照。

## 视频 / 封面
- `video/xhs-2026-06-19-spacex.mp4`（无字幕基底）/ **`xhs-2026-06-19-spacex-sub.mp4`（带字幕，发布用）** + `video/subs.ass`。
  - ffprobe：**2160×3840、30fps、85.12s**（84.1 旁白 + 1s 片尾）。
  - 字幕：脚本原文 + faster-whisper 词级对齐（560↔571 字，47 行）。
- ⚙️ **字幕放大固化**：`make_xhs_video_html` 默认 `SUB_FONTSIZE 78→96`、`SUB_MAXLEN 22→18`（防溢出），对以后每天生效。
- 片尾：`circle_photo/place_photo_on_card/build_shrink_outro/concat_clips`，圆形猫照（片头/图片_20260606072137.png）1s 缩小消失。
- 封面 `cover/cover-2026-06-19-spacex.png`（3:4，BIG「OpenAI 一年亏 385亿」，5 行以 OpenAI 领头）。

## 标题 + 文案
- 标题（用户选 数字+反转）：「OpenAI 一年亏掉385亿，这还是少算的」。
- `caption.md`：正文无 emoji、五条一行短句、结尾 @柿子树下的猫wanjeans；标签 10 个（热点 #OpenAI #大模型 #AI监管）。
