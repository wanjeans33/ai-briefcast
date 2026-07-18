# 2026-07-14 期 CHANGELOG

## 选题
- 头条=用户指定 Grok 4.5（能力+安全丑闻双拍）；另两条用户选 Claude Code token 开销、geohot 泼冷水
  （放弃推荐的苹果芯片造车遗产）；论文 UniClawBench + IdeaGene
- 素材=liziran 2026-07-13 + 用户指定头条独立核源；SK 海力士主新闻与 7/12 期重复，跳过

## 核源
- Grok 4.5：多方交叉（marktechpost/officechai/devops/roo）——Cursor 真实开发数据训练、跑分互有胜负
  （DeepSWE 1.0/Terminal-Bench 赢，DeepSWE 1.1/SWE-Bench Pro 输）、token 省 4.2 倍、$2/$6；
  安全=研究员 cereblab GitHub Gist+HN 首页（byteiota 详报）：git bundle 传 GCS 桶、12GB 传 5.1GB/73 块、
  .env 金丝雀密钥明文、隐私开关失效；复测 6 次零上传（服务端悄悄关闭）、xAI 无公开回应
- Claude Code：Systima 实测博客+HN+GIGAZINE（33k vs 7k、工具定义 24k、缓存写入 54 倍、实配 7.5 万起步）
- geohot：博客原文《AI 2040 and the Cult of Intelligence》（7/11）
- 论文：arXiv:2607.08768（UniClawBench）、arXiv:2607.08758（IdeaGene）编号已验证

## 用户改稿
1. 头条"赢了Claude的旗舰Opus，一些仍然输"→"在几项编程测试上赢了Claude的Opus 4.8"（Opus 已非旗舰、
   去啰嗦对冲；保留"自家跑分/几项"兜住互有胜负的事实边界）；"字"→"token"
2. IdeaGene 段用户没看懂"家谱"比喻→整段重写为"考它说清想法沿用谁的方法、修补哪个缺陷"，
   金句改"点子一大堆，来路说不清"

## 踩坑与修复
- 卡点漂移（最大 2.3s）照例用 subs.ass whisper 边界修正 durs.json 后复用音频重出
- 封面目录"Claude Code天价开销"英文过宽折行 → 改"Claude烧钱账单之谜"重出（音频复用，成本低）

## 产物
- 成片 110.04s 4K，字幕 63 行，QA 抽帧复核通过（封面单行、各段音画同步）
- 封面 hook=Grok 4.5/偷传代码库
