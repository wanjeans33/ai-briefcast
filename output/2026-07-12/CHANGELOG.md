# 2026-07-12 期 CHANGELOG

## 选题（用户一轮定稿）
- 新闻：苹果诉OpenAI偷硬件机密 ／ Musk承诺不断供Anthropic ／ SK海力士美股史上最大外企IPO
- 论文：LingBot-Video（MoE视频底座）／ LaMem-VLA（双latent记忆）
- 素材=liziran 2026-07-11（digest+brief）；7/11 期用的是 7/10 素材，无撞车
- 有意避开 LingBot-World 2.0（与 7/11 期 AlayaWorld 世界模型题材连播撞车）

## 稿件
- broadcast-0712-B-changed.md 初版 878 字→删到 820→用户要求去掉"预印本/还没同行评审"与
  "作者承认实验全在仿真里，真机还没验证"两处→786 字定稿（预印本声明保留在本文件与 header 备注）
- 核源：TechCrunch(苹果诉状细节+OpenAI否认；Musk合同 12.5亿/月×至2029.5=400亿、Colossus 1 300MW)、
  Al Jazeera/CNN/CNBC(SK 265亿、7倍超购、超阿里2014)、arXiv 2607.07675/2607.07608（编号已逐一验证）

## 踩坑与修复
1. **make_episode.py 类型 bug**：`synth_single_synced(segs, str(AUDIO), ...)` 传了 str，
   run_tts 调 `.parent` 崩。7/11 因音频已存在走复用分支未触发。已修：传 Path（scripts/make_episode.py:159）。
2. **分段测时漂移 ~4s**：news1 段含 OpenAI/Jony Ive 等英文词，单独测时 18.5s vs 整段语境实际 22.3s，
   自 news1 起所有卡整体提前约 4 秒（57.7s 音频还在 SK 段、画面已切论文01）。
   修法：用 subs.ass（whisper 强制对齐）各段首句时刻反推真实边界，改写 durs.json 后复用音频重跑
   make_episode 出片。**含较多英文词的段落建议以后默认用 whisper 边界校一遍 durs**。

## 产物
- 成片 96.21s 4K（旁白 95.2s + 1s 片尾收缩），字幕 55 行，QA 抽帧已人工复核（卡点/字幕/CTA 猫头均正常）
- 封面 hook=苹果动手/告了OpenAI（带大牌主体，按 analytics 结论）
- caption：标题「苹果动手，告了OpenAI」，论文传送门给了已验证 arXiv 链接
