# 2026-07-07 AI Briefcast

## Scope
- 内容：3 新闻（网络多源核实，digest 7/6 未更）+ 2 论文（liziran 7/6 简报）；无片头 + 猫图圆形片尾；
  带字幕；语速 1.25×（rate 36）。

## Selection（AskUserQuestion 选 + web 核实）
- 候选核日期后踢掉：GPT-5.6 Sol/Terra/Luna 预览（6/26 旧闻）、Claude Science（6/30 旧闻）、
  Gemini 3.5 Pro 跳票（仅聚合源，未独立核实）、联合国 AI 治理对话（7/6 开幕但对受众偏干）。
- 新闻 3 条：
  ① 头条 豆包/千问下线个性化 AI 智能体：《AI拟人化交互服务管理暂行办法》网信办等五部门 4 月发布、
    7/15 生效；豆包智能体 7/15 下线、只读至 10/15 后删；千问永久删除无迁移；字节导流自家猫箱
    （TechNode 7/6、ChinaTechNews 7/5 等）。⚠ 网传"3.45 亿用户"查无实锤，弃用。
  ② Tesla 无监控 Robotaxi 登陆迈阿密：7/3 第五城（Austin/Dallas/Houston 后首个德州加州以外）、
    首日无安全员、西迈阿密戴德 10-14 平方英里、年底 12 州目标；NHTSA 3 月把纯视觉 FSD 调查升级为
    工程分析（召回前最后一步，眩光/雨雾看不清）（The Information/Techmeme 7/5）。
  ③ 中国模型占 OpenRouter 流量 >45%（一年前 <2%）；小米 MiMo-V2-Pro 单模型 21.1% ≈ 3× OpenAI 7.5%；
    100M 输出 token $300 vs Claude Opus 4.6 $2500 ≈ 8 倍价差（Q2 2026 平台数据）。
- 论文 2 篇（liziran 7/6）：
  ① PAW（Program-as-Weights）：4B 编译器读自然语言规格→吐出 adapter 挂冻结 0.6B 解释器；
    追平 32B 直接 prompt、显存 ~1/50、MacBook M3 30 tok/s；开源 FuzzyBench 1000 万样本。
  ② AgenticSTS：typed retrieval 记忆合约，每决策拼干净上下文；《杀戮尖塔2》胜率 3/10→6/10，
    p≈0.37 不显著（作者自标 directional），口播如实带"谈不上统计显著"。

## 文稿 / 音频
- `scripts/broadcast-0707-B-changed.md`：文风铁律 + 证据纪律；不报硬日期（7/15→"这个月中"、
  10/15→"十月中"）。用户过审（"继续"）。
- 音频 `audio/broadcast-2026-07-07-spacex.mp3` **120.6s**（rate 36 整段合成一次）+ `durs.json`
  `[2.1,30.3,19.2,17.8,25.2,23.2,2.7]`。⚠ 比 7/6（105.9s）长 15s——头条信息量大 + 两论文段偏长；
  按"内容完整优先"保留，已向用户说明可砍稿重合成。

## 卡片（17 张，交互式选卡）
- 内容卡 5：你捏的AI月中就没了(悬念) / 特斯拉抢跑监管追查(观点) / 从2%到45%(数字) /
  0.6B追平32B(数字) / AI记忆要讲卫生(观点)。配色 c1/c3/c4/c5/c2；头条组 4 卡 [1.5,1,1,1]、PAW 组 2 卡。
- 补充卡 10（逐个 web 查证）：新规管什么(五部门/2小时提醒/未成年人禁虚拟伴侣)、捏崽、猫箱；
  纯视觉vs激光雷达、各家进度(Waymo周50万单/萝卜快跑Q1 320万单27城)；OpenRouter是什么、便宜8倍为什么是大事；
  模糊函数；统计显著(10局翻倍可能是运气)、游戏当试验场。
- 封面卡 hook「你捏的AI 要没了」。

## 视频 / 封面 / 文案
- `video/xhs-2026-07-07-spacex-sub.mp4`（发布用）+ 无字幕基底 + `subs.ass`（66 行，whisper 对齐 752↔762 字）。
- ffprobe：**2160×3840、30fps、121.68s**（120.6 旁白 + 1s 片尾）。抽帧 QA 通过。
- 封面 `cover/cover-2026-07-07.png`（3:4 2160×2880），BIG=「你捏的AI 要没了」。
- 标题「你捏的AI智能体，月中就没了」（13 字）；论文 arXiv 已核实（PAW 2607.02512、AgenticSTS 2607.02255）；
  `publish.json` visibility=self。

## 踩坑（留档）
- **emoji 选卡要用老码位**：🫥（U+1FAE5，Unicode 14）渲染成空框，换 💔 后重跑全流程才正常。
  以后 icon 用 Unicode ≤12 的常见 emoji（📱🥪🏛️💔🚕🛒 这类）。
- liziran digest 未更当天时的选题流程走通：WebSearch 找候选 → 逐条核发布日期（GPT-5.6 6/26、
  Claude Science 6/30 被踢）→ AskUserQuestion 选稿；网传数字（"3.45 亿用户"）查无实锤就弃用。

## TODO
- 用户自行上传（publish.json 已备好；首条建议仅自己可见）。
- 音频 120.6s 若用户嫌长：候选砍点＝头条"字节让用户搬去猫箱"句、PAW"以前只能每次都去问大模型"句，
  可省 ~10s，需砍后重合成+重出片。
