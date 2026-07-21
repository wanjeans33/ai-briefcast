# 2026-06-16 AI Briefcast

## Scope

- 内容日期：使用 **2026-06-15** 新闻与论文，准备 6/16 briefcast 稿子。
- 原始素材：`samples/source-2026-06-15.md`
  - digest: https://ai-digest.liziran.com/zh/digest/2026-06-15-anthropic-says-one-jailbreak-shouldnt-doom-model-startups.html
  - brief: https://ai-brief.liziran.com/zh/daily/2026-06-15-pruning-vs-scratch-budget.html
- 注意：仓库已有 `output/2026-06-15/`，那是使用 6/14 新闻生成的 6/15 发布版。为避免覆盖用户手改稿，本次使用 6/15 内容，产物放入 `output/2026-06-16/`。

## Selection

- 新闻 3 条：
  - Anthropic 反驳 Fable 5 / Mythos 5 下架逻辑，安全顾虑源头指向 Amazon CEO Andy Jassy。
  - FAANG 叙事让位 MANGOS，SpaceX / OpenAI / Anthropic 等挤进同一上市窗口，Mistral 传出新一轮高估值融资。
  - Gemini vibecoding 五分钟生成可运行 App，但暴露修复、订阅、按量付费和本地硬件的成本账。
- 论文 2 篇：
  - Small LLMs: Pruning vs. Training from Scratch，剪枝优势取决于训练预算，细粒度剪枝更稳。
  - VISTA，用同一 GUI 实例多视图构造比较组，救回 GRPO 组内全对/全错时消失的相对信号。

## Scripts

- A 版轻快网感：`output/2026-06-16/scripts/broadcast-0616-from-0615-A.md`
- B 版沉稳串点：`output/2026-06-16/scripts/broadcast-0616-from-0615-B.md`
- 推荐 B 版作为主线：`AI 圈开始重新算账`，从安全账、资本账、使用账写到训练预算和梯度信号。
- 用户指定 3 新闻版：`broadcast-0616-3news-rewrite.md`（Fable5 暗流 / 乌克兰无人机 / Prometheus）。

## Review（用户要求审/打磨 3news-rewrite）

- 校订稿（不覆盖用户原稿）：`output/2026-06-16/scripts/broadcast-0616-3news-rewrite-reviewed.md`，用户选 **3 闻 + 2 论文**。
- 查到的硬伤（已改）：
  1. **无人机段失实**：原稿"已部署…猎杀俄军士兵"夸大；源素材为「一次性测试击杀、全自主作战仍属罕见个例」。
     已改为"一次测试"+"罕见个例"。
  2. **"中美承诺不把杀戮决策权交给 AI" 不准确**：WebSearch 查证——2024-11 Biden-Xi 仅就 **核武器** 达成
     "由人而非 AI 决定动用核武"，不含常规武器，乌克兰亦非缔约方。已删除该假托，改为不点名的伦理设问。
     来源：CNBC / Interesting Engineering（2024-11-16 APEC 利马）。
  3. **Fable 5 段漏 Semafor 关键事实**：白宫对 Mythos 出口管制，部分因担心其落入"与中国关联团体"。已补。
  4. 论文段：删 VISTA 段尾 `，。` pad 标记；剪枝段补"细粒度剪枝才保得住优势"收束。
  5. 结构矛盾：原头注"不加论文"与正文挂 2 段论文冲突 → 用户定为 3 闻+2 论文，头注已改。
- 校订稿先文字定稿（~120s），用户问"90 秒读不完吧" → 收紧到 **809 字**（主压段1 306→201），
  估算 ~94s。用户"不用了，开始音频视频" → 进入合成。

## Audio

- 源：`broadcast-0616-3news-rewrite-reviewed.md`；克隆音色 `S_HHgApOH42`，rate 50（≈1.4×），整段一次合成。
- 输出 `audio/broadcast-2026-06-16-spacex.mp3`，**实测 93.9s**（估算 94s 命中）。
- 7 段卡点 `audio/durs.json`：`[1.9, 21.2, 15.3, 14.4, 15.8, 17.4, 7.9]`。

## Cards（12 张）+ Video（4K + 圆形猫片尾）

- 封面 + 5 内容卡（3 闻 + 2 论文，色 c1/c3/c4/c5/c2）+ 5 信息补充卡 + CTA。
- 5 张补充卡逐个 WebSearch 查证：越狱 jailbreak / 全自主武器（人在回路 vs 脱离回路，UNGA Res 80/57、120+ 国想立约、美反对、2025 底僵持）/
  物理 AI（英伟达「机器人的 ChatGPT 时刻」）/ 模型剪枝（粗 vs 细粒度）/ GRPO（全对全错无组内差异 → 梯度白给）。
- 无人机两张卡（内容+补充）措辞保持事实与克制：「一次测试」「罕见个例」「人完全脱离回路」，不煽情。
- 卡片结构 `cards/cards.json`；抽查封面/无人机内容卡/全自主武器补充卡，无乱码/溢出/重叠。
- 视频 `video/xhs-2026-06-16-spacex.mp4`：ffprobe `2160x3840`、30fps、时长 **94.93s**（93.9s 旁白 + 1s 圆形猫片尾，无片头）。
## Cover（3:4）

- 用户指定大钩子用「全自动杀戮 AI」（以无人机自主开火为头条），`make_cover.py` 改 6/16：
  BIG `全自动 / 杀戮 AI`、KICKER `6月16日 · 乌克兰战场实测`、5 行以无人机领头并标「仍属个例」防夸大。
- 输出 `cover/cover-2026-06-16-spacex.png`，`2160x2880`，无溢出。
- 备注：暖色+柿子/猫品牌模板与「杀戮 AI」调性反差，已向用户提示可另做冷/暗版背景，用户未要求即沿用模板。

## 标题/正文/话题标签（caption.md）

- 标题（推荐）：`战场上第一次，AI 自己扣下了扳机`（呼应封面"全自动杀戮 AI"钩子）；备选 2 条。
- 正文**不带 emoji**（用户常要），5 条以无人机领头，措辞保持"一次测试/罕见个例"克制。
- 标签 9 个：泛(#人工智能 #AI)+领域(#AI日报 #每日AI #AI资讯)+热点(#自主武器 #Anthropic #物理AI)+品牌(#柿子树下的猫)+场景(#通勤干货)。
