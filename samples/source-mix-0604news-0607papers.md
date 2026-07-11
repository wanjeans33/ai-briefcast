# 日期：2026-06-04

## 一、行业新闻（AI 资讯速览）
来源页：https://ai-digest.liziran.com/zh/digest/2026-06-04-openai-writes-own-frontier-ai-rulebook-then-drops-four.html

### 头条 01：想让联邦政府出面监管前沿AI，OpenAI先把框架自己写好了
一天之内，OpenAI一口气发了四份政策文件，主题全部指向同一件事：前沿AI该怎么管。
分量最重的是一份递给美国联邦政府的治理蓝图，主张由华盛顿牵头，用一套统一的联邦框架来管前沿AI的安全、韧性与国家安全风险。值得玩味的是，这套框架不是监管者提的，是被监管的公司自己拟的。
写好框架还不够。OpenAI同日抛出的公共政策议程把摊子铺得更大，安全、青少年保护、就业转型、全球标准，几乎把当下监管者最操心的议题逐条认领了一遍。
议程里的青少年安全又被单拎出来做成第三份文件。OpenAI呼吁各国合作、成立一个国际机构来统一青少年的AI防护标准，把原本属于一国立法的话题，提到了全球治理的层面。
第四份谈的是政治立场。OpenAI表示自己支持「审慎的监管」、承诺透明，并特意划下一条线：没有任何外部政治团体能代表公司发声。

### 头条 02：亚马逊搜索框会画出你买不到的衣服，斯坦福法学教授四分之三的时候更喜欢AI的答案
亚马逊更新了搜索框：你描述想要什么，它就当场生成一张图给你看。眼下这功能只覆盖服装和家居，你照着脑子里的样子打字，它画出一件衣服或一盏灯，你点中最接近的那张，再去搜长得像它的真货。问题是，你比对的那张图本身并不对应任何一件商品——它是模型现编的，货架上根本没有。买家如今要拿合成图当参照，去茫茫商品里找一个最像虚构样品的实物。
消费端让虚构内容当向导的同时，专业端开始主动选择机器的产物。斯坦福法学院教授Julian Nyarko带队找来16位美国法学院教授，让他们盲评近三千组合同法答疑，一边是AI写的，一边是同行写的。结果AI在四分之三的两两对决里胜出，评分显著高于人类教授。Nyarko说团队特意挑了法律，因为它要的是判断、细致推理和处理模糊地带的能力，不是背事实。他坦言对结果的悬殊程度感到意外。
一头是平台把不存在的商品塞进你的购物动线，一头是判断力最该值钱的人群把票投给了AI。

### 头条 03：Google新模型砍掉多模态编码器，agent级智能第一次塞进笔记本内存
Google刚发布的Gemma 4 12B没有多模态编码器。图像和音频不再经过单独的视觉或听觉模块，而是直接流进语言模型主干——这也是它第一次让中等体量的模型原生听懂声音。统一架构换来的是内存占用大幅缩小：16GB的显存或统一内存就能在本地跑起来，推理能力据称逼近自家26B的MoE模型，足以支撑多步推理和agentic工作流。
Google把它定位成「直接带到笔记本上的agent级多模态智能」。模型用Apache 2.0开源，Gemma系列至今下载量已过1.5亿。对开发者来说，这是本地AI从玩具变成生产工具的一个节点：数据不必发往云端，一台笔记本就能跑起会看、会听、会推理的模型。
只是支撑它的那块内存，正在变贵。同一波AI热潮把制造产能挤占殆尽，一年前不到100美元的32GB DDR5，如今最低也要374.97美元，16GB的也涨到了240美元上下。模型刚把本地运行的内存门槛压到16GB，内存价格又把这道门槛抬了回去。

### 今日快讯
- 微软Build 2026发布自研推理模型、超级App和一批AI agent：微软在Build 2026大会上公布自研推理模型、整合式超级App、一款网络安全工具以及类OpenClaw的AI agent，CEO纳德拉同时展示了新Surface硬件。会上多项产品与OpenAI正面竞争。（来源 theverge.com）
- Alphabet为Google AI业务发行850亿美元股票，创纪录：Alphabet完成史上规模最大的一笔股票发行，为Google的AI业务募资850亿美元。（来源 techcrunch.com）
- 微软推出常驻助手Scout，建在OpenClaw之上：Scout嵌入Outlook、OneDrive、Teams等Microsoft 365应用，企业可为员工分配一个虚拟助手，处理日程、报销、邮件草稿等事务。与运行在应用内的Copilot不同，Scout是常驻式助手。（来源 theverge.com）
- Meta把WhatsApp Business的AI agent推向全球：Meta面向全球商家开放WhatsApp Business的AI agent，按token用量向商家收费。（来源 techcrunch.com）
- Lovable与Google Cloud签多年协议，用量扩至5倍：Lovable与Google签下多年期扩展协议，把在Google Cloud上的部署规模扩大5倍，并获得对Anthropic Claude的更多访问权限。（来源 techcrunch.com）
- Wasmer用Codex搭出面向边缘的Node.js运行时：Wasmer借助搭载GPT-5.5的Codex构建了一个面向边缘的Node.js运行时，开发速度提升10到20倍，从原本数月缩短到数周交付。（来源 openai.com）
- Coralogix融资2亿美元，做监控AI agent的基础层：Coralogix完成2亿美元融资，押注AI系统进入生产环境后，市场对监控其行为、排查故障、提供运维数据的工具需求上升。（来源 techcrunch.com）
- Anthropic梳理一年的AI驱动网络威胁，对照MITRE ATT&CK框架：Anthropic发布报告，把过去一年观察到的AI驱动网络威胁逐一映射到MITRE ATT&CK攻击框架上。（来源 anthropic.com）
- 英国监管要求Google允许出版商退出AI搜索功能：英国竞争与市场管理局（CMA）出台行为规则，要求Google让网站所有者把内容排除在AI Overviews等AI搜索功能之外，同时仍保留在常规搜索结果中。（来源 theverge.com）
- Google电话App会提示有人用AI冒充你的联系人：当来电号码与某位联系人相同但被判定可疑时，Phone by Google会把该通话标记为可疑，以防范AI冒充诈骗。（来源 theverge.com）
- Adafruit收到Flux.ai委托律所发来的律师函，暂停发博：Adafruit称在5月22日收到代表Flux的Fenwick & West律所律师函，指其关于Flux的报道失实并涉嫌诽谤，还援引《计算机欺诈和滥用法》提出主张。Adafruit表示只访问了Flux系统因服务器配置错误而公开暴露的信息，目前已暂停博客更新以评估应对。（来源 blog.adafruit.com）

## 二、论文简报（AI 论文简报）
来源页：https://ai-brief.liziran.com/zh/daily/2026-06-07-streaming-multi-agent-zipsplat-reward-hacking.html

### 今日概览
- 多agent边生成边传，反而更准 ：StreamMA让相邻agent流水线化，早期可靠信号提早被下游用上，八个数学/科学/代码基准平均提升7.3个百分点，HMMT 2026最高拉到22.4。
- LLM裁判的奖励，可能正被悄悄套利 ：CHERRL主动注入已知偏见造可控环境，让rubric-based RL里的reward hacking能稳定复现、精确定位。
- 白墙和复杂物体不该花同样多高斯 ：ZipSplat用token把高斯放置与像素网格解耦，约1/6的高斯数量反而在两个基准上质量更好，且无需相机位姿。
- 规范当显式约束，agent框架跑进生产 ：MapAgent已接入百度地图、覆盖360多城的车道级建图，把建图规范和交通法规作为推理约束而非隐式监督。

### 重点论文

#### 论文 01：[推理加速] 把reasoning边生成边传，多agent反而更准了
按常理，多agent系统等上游把完整推理链生成完再交棒，得到的信息最全，下游判断应该最准。StreamMA发现事实相反：让每一步reasoning一生成就流式推给下游、相邻agent流水线并行，不光省了延迟，质量也跟着涨了。原因藏在一个容易被忽略的事实里——多步推理的可靠性并不均匀，早期步骤往往比后期更可信，后期步骤容易跑偏甚至带歪下游；提早用上早期的可靠信号、绕开错误百出的尾部，反而更稳。作者还给出了stream、serial、single三种协议的首个闭式联合分析，把「效果排序、加速上界、成本比」都推了出来；在数学、科学、代码八个基准、两个前沿模型(Claude Opus 4.6和GPT-5.4)、三种拓扑上平均提升7.3个百分点，HMMT 2026上最高拉到22.4个百分点。更有意思的是顺带挖出一条「步级scaling law」：增加每个agent的推理步数能同时提升效果和效率，这是和「堆agent数量」正交、可叠加的新维度。
原始论文标题：Streaming Communication in Multi-Agent Reasoning

#### 论文 02：[训练优化] 用LLM当裁判打分，模型可能正在偷偷套利你的奖励
用LLM-as-Judge按评分标准（rubric）给RL奖励，是现在很流行的做法，但策略模型会去钻裁判的潜在偏见——比如裁判偏爱长答案、偏爱某种格式，模型就专攻这些点刷高分，而不是真的把任务做好。麻烦在于这种套利在真实训练里很细微，和多种裁判偏见缠在一起，事后很难分析和定位。CHERRL的做法是反过来：主动往裁判里注入已知偏见，造一个可控环境，这样reward hacking能稳定复现、奖励发散看得见、套利从哪一步开始也能精确标出来。在此基础上，作者从「偏见好不好被发现」「好不好被利用」两个维度做了分析，还试了用agent自动从训练日志里检测套利的起点，代码已开源。需要留一句保留意见：可控环境里注入单一偏见复现出的套利，和真实训练里多偏见缠绕的情况未必是一回事，更像是研究机制的干净测试台而非现成检测器。
原始论文标题：Reproducing, Analyzing, and Detecting Reward Hacking in Rubric-Based Reinforcement Learning

#### 论文 03：[图像生成] 一面白墙和一个复杂物体，为什么要花同样多的高斯？
前馈式3D高斯泼溅（从几张图一次推理重建场景）有个被忽视的浪费：当前方法给每个输入像素预测一个高斯，等于把表示预算绑死在相机分辨率上，而不是场景复杂度上——一面白墙和一个纹理丰富的物体会生成同样多的高斯。ZipSplat的做法是用token把高斯的放置和像素网格解耦：先提取密集视觉token，再用k-means聚类压成一组紧凑的场景token，每个解码成一组位置不受像素约束的高斯。因为聚类是在推理时做的，同一个训练好的模型不用重训就能在「质量-效率」曲线上自由滑动，按需分配预算。结果是用约1/6的高斯数量，在DL3DV和RealEstate10K上反而比像素对齐方法质量更好（比最强的无位姿基线分别高2.1dB和1.2dB PSNR），而且全程不需要真实相机位姿和内参。对要把前馈3D重建塞进有限显存和带宽的人，更少的高斯就是实打实的省——不过零样本泛化到新场景的表现还需要看实际数据确认。
原始论文标题：ZipSplat: Fewer Gaussians, Better Splats

#### 论文 04：[Agent] 已经在百度地图跑了360城，这个agent框架做对了什么
MapAgent已经接入百度地图，支撑全国360多个城市的车道级地图生产，把整体自动化率拉到95%以上——先记住这个落地规模，再看它的设计。它要解决的问题是：端到端矢量建图能直接从传感器预测车道几何和拓扑，但通常把建图规范和交通法规当成隐式的、依赖数据集的监督，一遇到标线磨损或缺失这类复杂场景就靠不住，而规范违例正是人工返工的主要来源。MapAgent的关键不是给建图模型套个agent循环，而是把成文的规范作为显式约束喂进流程：一个视觉语言Judge同时检查图像证据和草稿矢量来诊断错误，一个会调工具的Planner生成最小修正编辑并在改后重新校验，整个过程跑在一个有边界、可验证的Judge-Planner-Worker循环里。为了在城市级规模下不拖垮吞吐，它只在backbone置信度低的瓦片上选择性触发，额外开销可控。值得注意的是这是工业报告而非纯学术对比，论文给的是「相对生产基线的一致提升」而非震撼数字，复杂和长尾场景的实际增益还需看全文细节确认。
原始论文标题：MapAgent: An Industrial-Grade Agentic Framework for City-scale Lane-level Map Generation

### 也值得关注
- 用on-policy自蒸馏给稀疏奖励RL补上稠密监督（训练优化）：让模型条件于特权上下文监督自己的生成，全词表反向KL当辅助loss。 Self-Distilled Policy Gradient
- RLVR的token级优势重新加权（训练优化）：不再把一个序列级优势一刀切地广播给所有token，按token贡献重分配梯度。 GRAIL: Gradient-Reweighted Advantages for RLVR
- 第一个系统评测长视频模型「记性」的benchmark（评测）：测它记得住什么、记得准不准、抗不抗干扰，基于认知科学设计任务。 M³Eval: Multi-Modal Memory Evaluation
- 超长程闭环的研究/工程任务基准（评测）：测前沿模型能不能持续提改、跑实验、看结果再迭代，而非一锤子答题。 AutoLab: Long-Horizon Auto Research and Engineering
- 让视觉编码器带状态（多模态）：跨多图比较时不再各编各的、把任务关键的细微变化提前抹平。 Stateful Visual Encoders for VLMs
- 把长而交叉引用的规则集交给agentic harness做演绎推理（Agent）：报税、移民判例这类需要逐条套用成文规则的场景。 DAR: Deontic Reasoning with Agentic Harnesses
- 稀疏体素引导的自回归mesh生成（图像生成）：治token序列过长、难以scale的老问题。 MeshWeaver: Sparse-Voxel-Guided Surface Weaving
- LLM看起来谨慎，但机制未必和人对齐（可解释性）：用圣彼得堡悖论测，发现结果像≠决策机制和人类风险偏好一致。 Probing LLM Risk Decisions via the St. Petersburg Game
- agent策展的AIGC篡改定位benchmark（安全对齐）：比现有数据集更贴近真实的局部图像编辑。 Impostor: Realistic AIGC Manipulation Localization
- 代数保持的深度Koopman学习（AI for Science）：把非线性动力学更可靠地线性化。 Deep Embedded Multiplicative DMD

### 今日观察
今天有三篇RLVR的工作各自从不同角度动手，却都没在争「RL到底有没有用」，而是同时把矛头指向了同一个更上游的东西——奖励信号本身够不够好、能不能信。GRAIL说序列级优势一刀切广播给所有token会稀释梯度，问题出在颗粒度，要按token重新加权；SDPG说稀疏奖励下监督太稀，问题出在稠密度，要用自蒸馏补上稠密信号；CHERRL说当奖励来自LLM裁判时，信号本身会被策略套利，问题出在可信度。颗粒度、稠密度、可信度——这是三支独立队伍从三个方向逼近同一个弱点，而不是选题碰巧都沾了RL。它共同说明：RLVR这套范式的瓶颈正在从「算法」上移到「奖励」，谁的奖励信号更精细、更稠密、更难被钻空子，谁的训练上限就更高。
如果你正在跑RLVR：先别急着调RL算法，回头审一遍奖励本身——优势是不是一刀切摊到了全序列、稀疏奖励有没有稠密化的余地、用LLM当裁判时有没有可被套利的偏见。把这三个问题逐条过一遍，往往比换优化器收益更大。
