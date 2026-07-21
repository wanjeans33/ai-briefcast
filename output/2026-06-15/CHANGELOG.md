# 2026-06-15 AI Briefcast

## Scope

- 内容日期：使用 **6/14 新闻与论文**，生成 6/15 小红书 AI 速览。
- 形态：3 新闻 + 2 论文；**片尾**（圆形猫照缩小消失，无片头）；A/B 两版选稿。
- 去重决策：昨天（output/2026-06-14，用 6/13 新闻）已讲过"Claude Fable 5 被禁用"。今天头条01
  与之同源，但角度换成**"为什么被切断"**——亚马逊提交网安研究 + CEO Jassy 找白宫 → 白宫下令。
  作为对昨天的跟进，不复述禁用细节。

## Selection（用户已确认）

- 新闻 3 条：
  1. 白宫令切断 Fable 5 / Mythos 5（推手是竞争对手亚马逊的网安研究）。
  2. 《开源AI必须赢》宣言冲 HN 1500 分 + "认知订阅制"警告 + MiniMax 开源兑现（稀疏注意力 / 数学证明合并）。
  3. iOS 27 给 iPhone 装 AI 修图（重构图/扩展/清杂物）+ Siri 终于好用。
- 论文 2 篇：SpatialClaw（换"动作接口" 20 benchmark +11.2 分）/ VideoMDM（不用 3D 数据、只靠 2D 姿态学 3D 人体运动）。
- 风格：先出 A（轻快网感）/ B（沉稳串点）两版，用户挑一版。

## Sources

- 原始素材：`samples/source-2026-06-14.md`
  - digest：https://ai-digest.liziran.com/zh/digest/2026-06-14-anthropic-locks-every-foreign-user-out-two-best-models.html
  - brief ：https://ai-brief.liziran.com/zh/daily/2026-06-14-action-interface-spatial-reasoning.html

## Scripts

- A 版（轻快网感）：`output/2026-06-15/scripts/broadcast-0615-spacex-A.md`
- B 版（沉稳串点，主线"控制权下沉"）：`output/2026-06-15/scripts/broadcast-0615-spacex-B.md`
- 两版结构均为：开场 + 3 新闻 + 2 论文 + 收尾 = 7 个音频段。
- 用户选 B 版。

## Audio（卡点）

- 用户选 B → 存为 `broadcast-0615-spacex-B-changed.md` 逐步压缩长度（音色优先：整段一次合成）。
- 语速 `VOLC_SPEECH_RATE=50`（≈1.4×），克隆音色 `VOLC_SPEAKER2=S_HHgApOH42`。
- 长度迭代（用户连续要求更短，目标"理论 90 秒"）：
  - B 原文 ~175s → 收紧中间 5 段 ~136s → 再压 ~110s → 深压（每条 2 句）**101.4s** 定稿。
  - 实测：豆包克隆音色每段有 ~1.5–2s 停顿/pad，101s 是不伤干货的实际下限；再短得删事实。
  - 核心数字全保留：HN 1500 分、+11.2 分、六个底座、FID 0.88 对 0.54（舍 59.9% 绝对值）。
- 输出 `audio/broadcast-2026-06-15-spacex.mp3`，7 段时长写 `audio/durs.json`：
  `[1.9, 18.6, 19.0, 15.3, 17.2, 19.6, 9.8]`（开场/头条①②③/论文①②/收尾）。

## Cards（补充卡＝联网查证科普）

- 用户"自己点"补充卡：要全部 7 张 + 额外一张"亚马逊 AI 研究情况"，共 **15 张**：
  封面 + 5 内容卡 + 8 信息补充卡 + CTA。
- 内容卡 3 头条 + 2 论文，同条新闻与其补充卡同色分组：c1/c3/c4/c5/c2。
- 8 张补充卡逐个 WebSearch 查证后写"高中生也能懂"：
  亚马逊研究（一连串提问越狱套出可攻击信息，Anthropic 反驳 GPT 5.5 也能）/ 视同出口（deemed export）/
  认知订阅经济（manifesto 原话 subscription economy for cognition）/ 稀疏注意力（1M token≈16GB）/
  生成式补图（outpainting）/ 动作接口 / FID（越低越好，0=一样）/ 动捕为何贵（光学棚起步 2 万刀，AMASS 仅 ~45h）。
- 卡片结构写 `cards/cards.json`；抽查封面/内容卡/最长补充卡/CTA，无乱码/溢出/重叠。

## Video（4K + 圆形猫片尾）

- 按音频段分组、组内权重（内容卡 1.5 / 补充卡 1.0）切卡点，逐卡精确对齐。
- **不用片头**；CTA 卡放满圆猫照（`片头/图片_20260606072137.png`），另存 `card-15.plain.png`，
  结尾 1 秒圆形缩小消失片尾。中间文件 `_main-…` / `_outro-…`。
- 输出 `video/xhs-2026-06-15-spacex.mp4`。ffprobe：`2160x3840`、30fps、AAC 立体声、时长 **102.44s**
  （101.4s 旁白 + 1s 片尾；composite 的 `-shortest` 把主体收到音频长度）。

## Cover（3:4）

- `make_cover.py` 改 6/15：BIG 钩子初版 `竞对掀翻 Fable 5`，按用户要求改为 `凶手是亚马逊`（亚马逊高亮，
  与标题"凶手居然是亚马逊"呼应；Fable 5 上下文移到 KICKER `6月15日 · Fable 5 被全球拉闸`）；5 行速览镜像 5 张内容卡。
- 输出 `cover/cover-2026-06-15-spacex.png`，`2160x2880`，无溢出。

## 文案（caption.md）

- 用户选标题 B：`Fable 5 被拉闸，凶手居然是亚马逊`；正文**不带 emoji**（用户常要）。
- 标签 9 个：泛(#人工智能 #AI) + 领域(#AI日报 #每日AI #AI资讯) + 热点(#Anthropic #开源AI #iOS27) +
  品牌(#柿子树下的猫) + 场景(#通勤干货)。

## 踩坑 / 决策

- **长度估算反复偏低**：按 8.4 字/秒估，实测豆包克隆音色约 **9 字/秒**且每段有固定停顿开销，
  短稿越短越"不成比例地长"。经验：1.4× 下 ~145 字/段≈16–18s；要 ~90s 总长，5 条内容各压到 ~2 句仍只到 ~100s。
- 头条与昨日（6/14 视频用 6/13 新闻）的"Fable 5 禁用"同源，靠**换角度（揭推手＝亚马逊+白宫令）**去重，不复述。
