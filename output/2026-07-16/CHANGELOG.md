# 2026-07-16 期 CHANGELOG

## 选题
- liziran 7/15 头条=Grok 偷传，与我们 7/14 期撞车（我们抢先了聚合站一天），用户要求换头条
- 新闻：OpenAI 首款硬件（头条）、Bun/Claude 重写风波+口头禅、Hassabis 刹车监管
- 论文页未更新（仍 7/14），按惯例从上期未选用的挑：WorldMove + NanoVSR

## 核源（本期纠了两处聚合站错误）
- OpenAI 硬件：Bloomberg 7/14 首报（TechCrunch/9to5Mac 交叉）——无屏音箱、摄像头传感器、机械件
  自主动、读邮件、io 前苹果团队、年内亮相 2027 开卖 $200-300
- Bun 风波：**liziran 把"Anthropic 放烟雾"安在 Zig 作者头上不准**，实为 HN 榜首评论文标题
  （raymyers.org）；核 Andrew Kelley 博文原文，稿中只用其本人指控（未经审查；宣传称做过模糊测试、
  团队会上承认没做），归因到他。背景补全：Bun 作者 Jarred Sumner 用并行 Claude 11 天 Zig→Rust
  数百万行（The Register/Techzine）。口头禅脚本=jola.dev（Johanna Larsson）wordswap 钩子
- Hassabis：Axios 专访+X 长文（FINRA 模式、发布前送测、叫停权、18 个月开源警告）；
  **liziran"不存在的特权"细节未核到源，弃用**，改用已核实的 Democracy Forward 诉 HUD/国务院
  （FOIA 自 2025-03 未回复）
- 论文：arXiv API 直查 WorldMove=2607.10389（Harvard）、NanoVSR=2607.10495

## 用户要求
- caption 最后一个标签从 #通勤干货 改为 **#宝宝辅食**（已执行；已提醒与内容不相关、可能影响
  标签沉淀，用户未再改口）

## 踩坑与修复
- 卡点漂移最大 1.0s（本期最小），照例 whisper 边界校正后重出
- 封面 hook"OpenAI首款硬件"过宽折三行 → 缩为"OpenAI硬件"重出

## 产物
- 成片 103.25s 4K，字幕 61 行，QA 抽帧复核通过
- 封面 hook=OpenAI硬件/会自己动
