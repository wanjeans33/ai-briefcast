# AI Briefcast 播报稿（7/26 · 新闻来自 7/23-7/24 · 待用户审 · 1.25× · MG 版）
> 来源：liziran 停在 7/24 期（其素材已被 7/25 用过），本期全部联网自采，逐条核到原始出处。
> 查重：白宫 vs 中国开源模型 7/22 做过"顾问吵架"回合，本期是新进展（正式点名指控+行业联名信+黄仁勋首帖），保留；
> OpenAI Codex 键盘为 7/15 旧闻（7/24 只是测评）排除；SpaceX-Google 云约为 6/5 旧闻排除；UN 治理会为 7/5 旧闻排除。
> 证据分级：
>   ① Opus 5 发布（E1 官方公告 anthropic.com/news/claude-opus-5 7/24 + E3 Bloomberg/Fortune/Axios/TechCrunch 同报）：
>     $5/$25 每百万 token 与 Opus 4.8 持平、为 Fable 5 一半；CursorBench 3.2 最高档距 Fable 5 0.5% 内且成本一半；
>     OSWorld 2.0 超 Fable 5 最好成绩、成本三分之一；effort 档位（low/high/xhigh/max）；fast mode 2 倍价 2.5 倍速；
>     Max 套餐默认模型；API/claude.ai/Claude Code/Cowork/Bedrock/Google Cloud/Microsoft Foundry 当天可用。
>     跑分全为官方口径，稿中归因一次（"官方跑分"），不追加怀疑句（铁律 12/13）。
>   ② 黄仁勋首帖+开源联名信（E1 本人 X 帖 + 联名信原文 + E3 Fortune/TechCrunch/CNBC/CyberScoop 7/23-24）：
>     7/23 白宫 OSTP 负责人 Kratsios 点名月之暗面蒸馏 Fable 5 训练 Kimi K3、经泰国渠道用 GB300，财政部威胁制裁；
>     月之暗面员工回应"Fable 7/1 公开、K3 7/15 上线，15 天训出全新前沿模型"（回应必须带上，已带）；
>     多位专家称指控"政治化"（SCMP）。7/24 二十五家机构（Nvidia/微软/Meta/HF/Mistral/IBM/a16z/YC/Perplexity/Replit 等）
>     联名信《Open Weights and American AI Leadership》；黄仁勋人生首条 X 帖转发该信；OpenAI/Anthropic/Google DeepMind 未签。
>   ③ Cognition 收购 Poke（E3 TechCrunch/多家 7/23-24，金额"low nine figures"≈1-3 亿美元，稿中写"上亿美元"）：
>     Poke＝The Interaction Company 的 iMessage/WhatsApp/Telegram 文字助理，近 3 个月用户消息 1 亿+ 条；
>     2025 年 9 月种子轮 1500 万美元、估值 1 亿；目的＝把对话风格/个性并入 Devin。
>   ④ H²SD（E2 预印本 arXiv 2607.18955，7/21 v1/7/22 v2，Cai 等）：对/错轨迹分开蒸馏，对的重估自身解法调 credit，
>     错的用验证器确认的参考提示做反向 KL 纠偏；任务＝数独/算独/箭头迷宫，赢过 GRPO/OPSD/RLSD/SDPO/SRPO。
>     限制留档（按 7 月偏好不上稿）：预印本；任务窄（谜题类）；作者自承收益依赖结果路由和改述指令；摘要未给具体数字。
> TTS 读法替换（只进 TTS 不进字幕/卡片）：H²SD → "H2SD"（上标²豆包读不稳）；0.5% 已写成"半个百分点"。

---

一分钟带你了解AI圈的新鲜事。

先说Anthropic发了新模型Opus 5。它加量不加价，价格和上一代持平，只有旗舰Fable 5的一半。官方跑分里，写代码的测试它最高档只比Fable 5低半个百分点，成本只要一半，操作电脑的测试反倒超了，钱只花三分之一。它还带力度档位，简单活调低省token，难题调高多想几步。网页版、Claude Code和各大云平台当天就能用，Max套餐里它成了默认模型。旗舰还没换代，二当家先把价格打了下来。

白宫和中国开源模型的架升级了。白宫科技政策负责人点名月之暗面，说Kimi K3是蒸馏Anthropic的Fable 5练出来的，还用了禁售的英伟达芯片，财政部还威胁要制裁。月之暗面员工反问，Fable 5七月初才公开，K3半个月后就上线，十五天怎么蒸馏出全新模型。行业跟着表态，英伟达、微软、Meta等二十五家机构联名上书，劝华盛顿别封杀开源模型，蒸馏本来就是行业通用技术。黄仁勋注册X账号发了人生第一条帖子，专门转这封信，他说世界既需要闭源旗舰，也需要开源旗舰。OpenAI和Anthropic都没签名。

写代码的AI公司Cognition花上亿美元，买下聊天助理Poke。Poke住在iMessage和WhatsApp里，说话像朋友，三个月里用户跟它聊了一亿多条消息。Cognition就看上这份会聊天，要把Poke的说话风格装进自家写码智能体Devin。买方说得直白，有性格的同事，总比像机器的同事招人喜欢。模型分数卷不动了，性格成了新卖点。

论文这边教AI怎么改作业。训练推理模型，通常只告诉它整道题对了还是错了，哪一步立了功没人说。H²SD把两种卷子分开批。题做对了，就顺着模型自己的解法，标出真正关键的步骤。做错了，才拿出带解题提示的参考答案，把它往正路上掰。在数独这类谜题测试里，它赢过了常用的训练方法。好学生只要点拨，差作业才要重讲，AI也吃因材施教这一套。

我是柿子树下的猫wanjeans，我们明天见。
