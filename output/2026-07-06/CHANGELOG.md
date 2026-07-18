# 2026-07-06 AI Briefcast

## Scope
- 内容：3 新闻 + 2 论文（均来自 liziran 7/5 期，逐条联网核实）；无片头 + 猫图圆形片尾；带字幕；语速 1.25×（rate 36）。
- digest 头条 02「阿里判 Claude Code 高危」＝昨天头条同一事件跟进，经用户确认跳过。

## Selection（AskUserQuestion 选 + web 核实）
- 新闻 3 条：
  ① 头条 AO3 上线 Claude 检测器误伤真人（6/29 匿名账号发布 AO3 skin，只认 font-claude-response-body
    代码痕迹，Word 中转即失效、改错别字也标红）+ Midjourney 反手要迪士尼/环球/华纳自曝内部 AI 用量
    （7/4 动议，要求推翻「只交 consumer-facing」限制，片厂称 fishing expedition）。
  ② 企业嫌 AI 太贵开始限流（404 Media 泄露材料：Amazon/Adobe/Atlassian/Citi 等；某公司月支出翻三倍
    超 1500 万美元；Uber 预算四月花光、人均月上限 1500 美元；根因＝包月改按 token 计费）。
  ③ Google 2025 用电 +37%（2026 环境报告 6/30 发：史上最大年涨幅、较 2019 +250%、数据中心 42M MWh≈新西兰
    全国、单次 Gemini 提问能耗降 33 倍、自认「AI 基建扩张快过电网脱碳」）。
- 论文 2 篇：① MemSyco-Bench（arXiv 2607.01071）记忆致谄媚，5 类任务，代码公开
  ② P2R（arXiv 2607.01191，浙大 ZJU-REAL）感知/推理解耦 + PRA-GRPO，P2R-4B V-Star 93.2%、
  HR-Bench-4K 81.9%，底座 Qwen3-VL，同日 PixelEyes 同路线。

## 文稿
- `scripts/broadcast-0706-B-changed.md`：按文风铁律 + 证据纪律（预印本归因「论文指出」、404 Media
  泄露材料归因、Google 数字为自报）。用户一版过审（"过"），初稿后做过一轮统一压缩（每段砍冗词）。
- 音频 `audio/broadcast-2026-07-06-spacex.mp3` **105.9s**（rate 36 整段合成，一次成功）+ `durs.json`
  `[1.8,25.9,19.6,16.4,18.6,21.1,2.4]`。93.2% 口播念「九成三」，卡片写精确数字。

## 卡片（17 张，交互式选卡）
- 内容卡 5：AI检测器误伤真人(数字版) / 全员拥抱AI先限流再说(观点版) / 一家公司用电抵一个国(悬念版) /
  你的AI正在顺着你说(悬念版) / 4B小模型看图93.2%(数字版)。配色 c1/c3/c4/c5/c2。
- 补充卡 10（每条 2 张，用户勾选 + 逐个 web 查证）：AO3是什么(1720万部/700志愿者/雨果奖)、
  检测器为何不靠谱(OpenAI 26%下架)；token计费、月烧1500万美元概念(≈900人年薪)；
  420亿度≈小半个三峡、单次提问0.24Wh≈微波炉1秒；AI谄媚(GPT-4o 4天回滚)、检索式记忆；
  AI怎么看图(切块)、强化学习(学骑车)。
- 封面卡带 hook「AI检测器 误伤真人」＝视频第一帧即封面。

## 视频 / 封面 / 文案
- `video/xhs-2026-07-06-spacex-sub.mp4`（发布用）+ 无字幕基底 + `video/subs.ass`。
- ffprobe：**2160×3840、30fps、106.96s**（105.9 旁白 + 1s 片尾）。字幕 whisper 对齐 778↔802 字、67 行。
- 抽帧 QA（0.5/7/20/62/105.3/106.7s）：封面钩子、高亮色块、字幕落位、CTA 圆猫头、片尾均正常。
- 封面 `cover/cover-2026-07-06.png`（3:4 2160×2880），BIG=「AI检测器 误伤真人」。
- 标题「文笔太好，被AI检测器冤枉了」（14 字）；`caption.md` 无 emoji + 论文链接
  （MemSyco-Bench 2607.01071、P2R 2607.01191）；`publish.json` visibility=self。

## 踩坑（留档）
- `make_publish.py` 解析 `## 标题` 节的首行文本：caption.md 里标题节别写"- A（选用）：…"这种选项列表，
  会被整行当标题（22 字超限告警）。备选标题放文末单独一节。
- durs.json 本期是 dict（`{"durs":[...]}`），出片脚本读取时做了 dict/list 兼容。

## TODO
- 用户自行上传（Route B 或手动）；publish.json 已备好（首条建议仅自己可见）。
