# 2026-06-22 AI Briefcast

## Scope
- 内容日期：使用 **6/21 新闻与论文**，生成 6/22 小红书 AI 速览。
- 形态：3 新闻 + 2 论文；无片头 + 猫图片尾；带字幕（字号 96）；语速 1.25×（rate 36）；目标 ≤90s。
- 原始素材：`samples/source-2026-06-21.md`
  - digest: https://ai-digest.liziran.com/zh/digest/2026-06-21-openai-hands-health-questions-gpt-55-days-after-test.html
  - brief : https://ai-brief.liziran.com/zh/daily/2026-06-21-leaderboard-predictive-validity-selective-verification-robot-self-improvement.html

## Selection（用户确认）
- 新闻 3 条：① ChatGPT 把健康问答交给 GPT-5.5，独立测试称其幻觉是开源 GLM-5.2 的 3 倍（"更大不是出路"）/
  ② 挪威几乎全面禁止小学课堂用 AI / ③ **AI 垄断遭反弹**（几家巨头把 AI 攥太紧 → 亚马逊工程师作证遭报复 + Sanders 7 万亿方案要分红利给普通人）。
  - 用户反馈：seg3 原用"权力"太泛，改为「垄断」口径，并理顺因果（巨头垄断→大家不满→所以 Sanders 提案）；卡3 标题改「反垄断打响了」/金句「巨头垄断太狠」；封面第 3 行改「巨头垄断 AI 遭反弹」。已重合成音频+重渲染（85.8s）。
- 论文 2 篇：Beyond Static Leaderboards（榜单第一换场景可能垫底，该看 predictive validity）/ ENPIRE（机器人自己试/打分/改，灵巧操作训到 99%）。

## 文稿（B · v6 口径，沿用 6/21 重写经验，一次到位）
- `scripts/broadcast-0622-B-changed.md`：大白话、正常主谓宾，**不用被动、不倒装**；**不数数过场**（用"先说/再说/权力这边/论文这边/最后一篇"）；
  比喻直接（"考试第一≠干活第一""师傅教徒弟 vs 徒弟自己苦练"）；去「：——」；收尾只留署名。
- 长度：一稿到位 **84.3s**（约 555 字，稳进 90s；没再来回删）。
- 音频 `audio/broadcast-2026-06-22-spacex.mp3`（克隆音色 S_HHgApOH42，整段一次合成）+
  `audio/durs.json` `[2.0,16.2,13.6,18.3,15.0,16.3,2.9]`（总 84.3s，7 段卡点）。

## 卡片（16 张，交互式选卡 AskUserQuestion）
- 内容卡「3 选 1」：卡1=②数字「瞎编 3 倍」/「输给了开源 GLM」、卡2=③提问「小学该用 AI 吗？」/「挪威说不」、
  卡3=①观点「两头开始反弹」/「权力太集中了」、卡4=①反差「考试第一≠干活第一」/「换场景就翻车」、卡5=②数字「自己练到 99%」/「不用人盯着」。
- 补充卡「候选池多选」共 9 张，逐个 WebSearch 查证：AI 幻觉 / GLM-5.2 / AI 拐杖效应（认知卸载：越早依赖 AI 越差，年纪越小越明显）/
  数据中心为何招嫌 / AI 财富基金 / 跑分榜 benchmark / 预测有效性 / 灵巧操作 / 自我改进闭环。
- 同新闻同色分组 c1/c3/c4/c5/c2；组内权重 内容卡 1.5、补充卡 1.0。

## 视频 / 封面
- `video/xhs-2026-06-22-spacex-sub.mp4`（发布用，带字幕）+ `video/xhs-2026-06-22-spacex.mp4`（无字幕基底）+ `video/subs.ass`。
  - ffprobe：**2160×3840、30fps、85.29s**（84.3 旁白 + 1s 片尾，≤90）。字幕 whisper 对齐 540↔539 字、48 行。
- 片尾圆形猫照 1s 缩小消失；字幕字号 96。
- 封面 `cover/cover-2026-06-22-spacex.png`（3:4，BIG「AI 健康问答 幻觉 3 倍」）。

## 标题 + 文案 + 投稿
- 标题（推荐，19 字）：「ChatGPT 答健康，瞎编是开源的3倍」。
- `caption.md`：正文无 emoji、无被动、五条短句、结尾 @柿子树下的猫wanjeans；标签 10 个（热点 #ChatGPT #开源大模型 #AI医疗）。
- `publish.json`：`make_publish.py` 生成。投稿半自动（视频/封面需用户在系统框选，见 memory）。
