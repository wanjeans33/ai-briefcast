# AI Briefcast 播报稿（7/24 · 新闻来自 7/22-7/23 · 待用户审 · 1.25×）

> 来源：liziran 2026-07-23 digest/brief 仅当线索源，全部核到原始出处自写。
> 查重：digest 头条① 世界模型（AlayaWorld/ABot-World）与 7/11 期同题材连续剧，跳过；
> 快讯"电费保护承诺"为 7/16 工厂电费续报，跳过。
> 证据分级：
>   ① AMD 投 Anthropic（E1 官方新闻稿 globenewswire/AMD 7/22）：战略股权投资至多 50 亿美元；
>     部署至多 2 吉瓦 Instinct MI450 系列（MI455X + EPYC Venice + Pensando + ROCm，Helios 机架），
>     首吉瓦 2027 上半年上线；双方用 Claude 优化 Instinct 负载、加速 ROCm 开发；
>     此前 Anthropic 已在用 MI355X（首次披露）。稿中不念具体型号。
>   ② 美军烧光"无限"token（E3 Wired 独立报道，cybernews/techradar/slashdot 转述一致）：
>     陆军 Enterprise LLM Workspace 用 Ask Sage（政府版聚合平台，可调 ChatGPT/Gemini 等），
>     5 年 4900 万美元合同；年度企业包 1 亿 token；今年 5 月陆军 CIO 宣布不限量，6 月中池子见底，
>     DEVCOM 员工收到邮件被要求省用，上限恢复；此前每人每月至少 20 万 token 用完自动补。
>     slashdot 摘要里"伊朗行动日耗 200 亿 token"未能核实，不用。
>   ③ OpenAI Presence（E1 官方发布 7/22 + helpnetsecurity/venturebeat 同报）：企业版语音+文字
>     agent 平台；政策/护栏/许可动作配置 + 上线前模拟评测；Codex 复盘生产对话提改进、
>     员工测试批准后生效；OpenAI 自家英文电话客服在用，自称 75% 来电无需人工；
>     限量 GA，需 OpenAI 驻场工程师或指定集成商部署，不开自助。
>   ④ ReViV（论文 arXiv:2607.17790 已从项目页核实；ETH Zürich+TU Delft+微软，ECCV 2026 接收）：
>     单目第一视角视频一次前馈同时重建 viewer（身体/手/视线/相机轨迹）与 view（场景深度）；
>     Masked Generative Egocentric Transformer；HoloAssist/HOT3D/ARCTIC/Aria Digital Twin/TACO
>     多榜 SOTA；手部重建较 EgoAllo 快 100×、较 Dyn-HaMR 快 400×（稿中说"快了几百倍"取保守口径）；
>     代码已开源（github.com/lvsean/reviv4d），权重未明确提及——稿中只说代码开源。
> 文风：不报硬日期、去冒号破折号、禁"不是…而是"、说 token 不说字块；正文硬预算 ≤820 字。

---

一分钟带你了解AI圈的新鲜事。

先说AMD花大钱抱住了Anthropic。AMD要向Anthropic投资至多50亿美元，Anthropic则用AMD新一代AI芯片建至多2吉瓦的算力，头一批明年上半年开机，两家还会用Claude帮AMD打磨自家软件生态。2吉瓦差不多是两座大型核电机组的出力，这种规模的订单过去几乎都归英伟达。投钱给客户，客户再拿钱买你的卡，英伟达和OpenAI带火的循环打法，AMD也用上了。

美军这边闹了个笑话。美国陆军给全军买了个政府版AI平台，能调ChatGPT、Gemini这些模型，五年合同4900万美元。官方前脚刚宣布token不限量，一个多月后全年的池子就见了底，员工收到邮件说要省着用，上限又给设了回来。之前是每人每月至少20万token，用完还自动补，等于变相不限量。号称无限的额度，撞上真实的用量，一个多月就现了原形。

OpenAI发布了企业版agent平台Presence，帮大公司上线电话和文字客服机器人。企业把自家政策、话术红线、允许的操作都配进去，上线之后Codex会复盘每天的对话，提出改进建议，但改动要员工测试批准了才生效。OpenAI自己的英文客服热线已经在用，自称75%的来电不需要人工。这个平台不开放自助注册，得OpenAI派工程师上门部署。卖模型的，开始接装修全包的活了。

论文这边看苏黎世联邦理工和微软的ReViV。用第一视角视频做重建，以前要两套流水线，一套算相机位置和场景深度，另一套算身体和手的动作，两边各干各的。ReViV用一个网络从单目视频里一次全出，看的人和被看的景同时重建，手部重建比老方法快了几百倍，多个榜单拿了最好成绩，代码开源，还被顶会ECCV收了。以后一台便宜的可穿戴相机，就能同时录下你在做什么和你眼前是什么。

我是柿子树下的猫wanjeans，我们明天见。
