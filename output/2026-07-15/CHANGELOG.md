# 2026-07-15 期 CHANGELOG

## 选题
- 用户要求排除苹果诉OpenAI续报（7/12 已做）；新闻=Siri/Waze 入口之战、Altman 回怼 Musk、
  纳德拉闭源木马警告（用户以 Nadella 换掉推荐的 Lorde 条）；论文=ANCHOR + FlashBEV
- 素材=liziran 2026-07-14

## 核源
- Siri：TechCrunch/Tom's Guide（iOS 27 公测 7/13、多轮/读屏/跨应用/独立App；基础模型与谷歌合作
  蒸馏自 Gemini）；Waze：TechCrunch 7/13（Gemini 语音搜索、对话式上报封路、少话模式）
- 互撕：TechCrunch/Fortune/DCD/Benzinga——Musk"行骗新高度"（借苹果诉讼）、Altman"短期太空数据
  中心卖股民"、专家多认同短期不成立、SpaceX 距高点 -36%、入纳指100
- 纳德拉：本人周日博文（TechCrunch/The Register 转述）——木马、付两遍钱、纠错蒸馏行业知识、
  编排层解法；点评"微软是 OpenAI 最大金主"
- 论文：arXiv API 直查——ANCHOR=2607.10455（E2 预印本），FlashBEV=2607.10071（ECCV 2026 已接收
  =E3，稿中写"过了同行评审"）

## 用户决策
- 终审时用户记起互骂主题似曾做过。查证：6/11 期头条=SpaceX 太空数据中心卫星 AI1，含上一轮
  "Altman 说荒谬、Musk 回怼"。本轮是新交锋（骂骗子+股价36%+纳指100 均为新事实），新闻保留，
  但**封面 hook 按用户要求弃用互骂**，改用头条01"iPhone变天/Siri当家了"；投稿标题同步，互骂留备选。
  经验：冲突类钩子复用前先查历史期数，同一对主角的连续剧别连着当封面。

## 踩坑与修复
- 卡点漂移（最大 2.6s）照例 whisper 边界修正后复用音频重出
- 封面目录"Siri成了iPhone当家"英文过宽折行 → 改"Siri成了手机当家"重出

## 产物
- 成片 112.04s 4K，字幕 59 行，QA 抽帧复核通过
- 封面 hook=iPhone变天/Siri当家了
