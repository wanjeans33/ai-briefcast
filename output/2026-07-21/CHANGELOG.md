# 2026-07-21 制作记录

## 选题
- 头条用户指定：Fable 5 进 Max 套餐、"Anthropic 服软了"（Fable 5 连续剧第三集，接 6/14 暂停键、7/13 收费拉锯）。
- 用户选题一轮定：+ 雅可比反例 + Google Gemini 用量（后踢换）；论文 SEED + 宏观谬误。
- **踢稿**：Google 收紧 Gemini 用量核实为 5 月旧闻（5/17 生效、5/28 已微调，WIRED 只是新出整理文），
  按"逐条核发布日期"纪律踢掉，换备选印度手机（Counterpoint 7/17 数据，新）。

## 纠错（liziran 线索源）
- 印度手机条：liziran 写数据来源 IDC、"涨价 4%~68%"——核实为 **Counterpoint** 数据、平均涨约 15%（Q2 末），
  按 Republic World 7/17 等原报道改写。
- 宏观谬误论文 arXiv 编号：搜索首结果给 2607.15272（实为 SciDiagramEdit），经 arXiv API 核实为 **2607.15277**。

## 核查要点
- 头条：7/20 生效，Max/Team Premium 含 Fable 5（限额 50%），Pro/Team Standard 一次性 $100 额度；
  原计划完全撤出订阅按用量卖；免费期最后延至 7/19。动机分析引 Simon Willison（E4）。
- 雅可比：Levent Alpöge（普林斯顿数学博士、现供职 Anthropic，稿中交代身份）7/20 发帖；
  行列式恒 -2、三点映同一点、可手工验算；HN 多人独立验算无实质质疑；未同行评审，稿中留"等数学界核验"。
- SEED 数字 14.9~45.9 个百分点在论文正文（ALFWorld vs GRPO，三个模型规模），摘要无数字，卡片用 45.9 标"最多"。
- 补充卡查证：HBM 同容量吃 3~4 倍晶圆产能（TrendForce/Tom's Hardware）；1966 Lander-Parkin 用 CDC 6600
  推翻欧拉猜想、论文正文两句话（给"一个反例终结猜想"卡作类比）。

## 流程
- 稿 820 字整（预算 820），一版过审无改动。
- make_episode 首跑 107.7s；whisper 边界校正（最大偏差 0.56s，开场卡）写回 durs.json 后重跑；
  QA 2160×3840、108.71s（预期 108.69±0.8）通过；抽帧 5 张全对位、无折行。
- caption.md 标签节名需用 `## 标签`（首版写成 `## Tag` 导致 publish.json 0 标签，已修）。
- 章节 5 个取 whisper 真实边界：00:00 / 00:24 / 00:47 / 01:04 / 01:25。
- publish.json：visibility=self，视频 -sub.mp4 + 双封面齐备。
