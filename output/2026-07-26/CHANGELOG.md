# 2026-07-26 制作记录（水墨MG动画版 · ChatCut · 8卡结构，首次在 Mac 端全流程复刻）

## 项目
- ChatCut 项目「AI Briefcast 7/26 · 水墨MG版」projectId c7b9eb77-9ebd-4f2e-92d5-4e6ca76a3dd0，
  1080×1920/30fps，总长 3068 帧（101.7s 旁白 + 片尾缩圈收尾）。
- 结构照抄 7/23-24：cover + 每主题 2 卡（隐喻卡+图表卡）×4 + outro + 全长字幕 MG；
  卡模板代码从 7/24 项目（70f10a02）inspect_asset 取回复用，图表卡中段按内容重写。
- ⚠️ create_project 传 1080×1920 建出来是横版 1920×1080，用 manage_timelines update 改回竖屏（新坑）。

## 选题与核查
- liziran 停在 7/24 期（素材已被 7/25 用过），本期全部联网自采，逐条核到原始出处。
- ① Opus 5 发布（E1 官方 anthropic.com/news/claude-opus-5 7/24 + Bloomberg/Fortune/Axios/TechCrunch）：
  $5/$25 与 Opus 4.8 持平、为 Fable 5 一半；CursorBench 最高档差 0.5% 内成本一半；OSWorld 反超成本 1/3；
  effort 档位；Max 默认模型。跑分全官方口径，稿中归因一次不追加怀疑句。
- ② 黄仁勋首帖+联名信（E1 本人 X 帖/联名信 + Fortune/TechCrunch/CNBC/CyberScoop）：7/23 白宫 OSTP 负责人
  Kratsios 点名月之暗面蒸馏 Fable 5 训 Kimi K3+经泰国用 GB300，财政部威胁制裁；月之暗面员工回应
  "Fable 7/1 公开、K3 7/15 上线，15 天训出新模型"（回应已带上）；专家称指控政治化（SCMP）。
  7/24 二十五家机构联名信《Open Weights and American AI Leadership》，黄仁勋人生首条 X 帖转发；
  OpenAI/Anthropic/Google DeepMind 未签。查重：7/22 只做过"顾问吵架"回合，本期为新进展。
- ③ Cognition 收购 Poke（E3 TechCrunch 等 7/23-24）："low nine figures"≈1-3 亿美元，稿写"上亿美元"；
  Poke＝iMessage/WhatsApp 文字助理，近 3 个月 1 亿+ 条消息；2025.9 种子轮 1500 万/估值 1 亿；并入 Devin。
- ④ H²SD（E2 预印本 arXiv 2607.18955，7/21）：对/错轨迹分开蒸馏；任务＝数独/算独/箭头迷宫，
  赢过 GRPO/OPSD/RLSD/SDPO/SRPO。限制留档不上稿：预印本、任务窄、收益依赖结果路由、摘要无具体数字。
- 排除：OpenAI Codex 键盘（7/15 旧闻）、SpaceX-Google 云约（6/5）、UN 治理会（7/5）、Midjourney 买 Co-Star（备选未用）。

## 素材
- 插图（codex 生图，Mac homebrew 版 codex 0.145+，参考 7/24 ill-amd/ill-presence 锚定水墨风，
  参考图从 7/24 项目 S3 下载——Windows 本地文件 Mac 上没有）：
  ill-opus（双峰+芒星+半价签）/ ill-huang（卷轴印章+皮衣人落笔+旋涡眼徽章）/
  ill-poke（手机小雀衔气泡+钱袋铜钱）/ ill-h2sd（私塾先生朱笔批卷+学童）。
- 印章徽章：logo-claude（12芒星）/ logo-nvidia（方框旋涡眼）/ logo-poke（气泡三点）/
  logo-h2sd（橙勾+墨叉）全新生成；outro-cat-ink.png 复用 7/24 文件（S3 下载后重传）。
- ⚠️ Mac 上 codex exec 的 `-i` 会吞掉后面的位置参数提示词——提示词必须走 stdin 管道（echo "..." | codex exec ... -）。
- 音频：broadcast-2026-07-26-mg.mp3（101.66s，S_HHgA 音色 rate36 整段合成）。
  TTS 读法替换：H²SD→"H2SD"（上标²豆包读不稳），仅进 TTS。
- ⚠️ Mac venv 初始缺 playwright（make_xhs_video_html import 需要）和 chromium，pip install + playwright install 补齐。

## 卡点与字幕
- whisper 词级对齐健康（gap 全 ≤0.36s），直接用词级边界。
- 段边界帧＝[0, 76, 887, 1809, 2345, 2978]，音频末 3050。
- a/b 卡切分（段内字幕行边界）：1a 76-296（"官方跑分里"起切）/ 1b 296-887 / 2a 887-1369（"行业跟着表态"起切）/
  2b 1369-1809 / 3a 1809-2032（"Cognition就看上"起切）/ 3b 2032-2345 / 4a 2345-2580（"题做对了"起切）/
  4b 2580-2978 / outro 2978-3068。
- 与终审文案的对齐微调（为音画同步）：2a hero 由「25家」改为「15天」（15 天在 2a 段口播），
  2b 图表由时间条改为 25 枚印章逐枚盖上+计数器 25 家（联名在 2b 段口播）；已在卡上落实。
- 金句进场帧（绝对）：1b 810 / 2b 1740 / 3b 2273 / 4b 2861（＝稿中金句口播时刻）。
- 字幕修行：「个百分点」孤行→重切为「写代码的测试它最高档/只比Fable 5低半个百分点」；
  「网页版」3 字孤行→并入下行；「Devin」孤行→重切为「要把Poke的说话风格/装进自家写码智能体Devin」。
  61 行，估宽全 ≤980px。

## 时间轴与 assetIds
- 轨道：V1 十张卡 / V2 subtitles-full（0-3068）/ A1 音频（0-3050）。
- MG：card-0-cover e8c6e915 / card-1-opus 35641194 / chart-1-opus aa4d69c3 / card-2-huang 307a519a /
  chart-2-huang c152bc9a / card-3-poke 0a689653 / chart-3-poke 19ba9855 / card-4-h2sd b62c4ba0 /
  chart-4-h2sd 187a6d09 / card-9-outro bbd6d97a / subtitles-full c7f625ce。
- 图：ill-opus 50228cda / ill-huang c68d17d2 / ill-poke 724a41fe / ill-h2sd e7b8ddd6 /
  logo-claude 208a5ee7 / logo-nvidia 35472953 / logo-poke 3c28df94 / logo-h2sd 774aa68d / outro-cat 3cf8d39c。
- 音频 3f97bac598（上传助手对同文件二次注册产生过重复资产，已删重复 4 图+1 音频）。

## 踩坑与经验（本期新增）
- edit_item 参数是 adds/updates/deletes 数组，不是 operations/扁平参数——传错静默返回空且不报错。
  条目内 trackId 用完整 uuid。字幕省 trackId 自动建 V2。
- edit_item 改 MG 实例属性的字段叫 propertyOverrides（propertyValues/properties/props 都不对）；
  改资产默认值走 edit_asset json.propertyDefaults（本期用它修了 chart-2 计数器说明的错字"勝"→"劝"）。
- MG 验证器：顶层只许函数（const SEAL_COUNT 顶层常量被拒，挪进组件）；无 hero 变体删 heroLabel 后
  inkSoftColor unused binding 被拒，连 schema 一起删（7/24 同款坑）。
- upload-media.mjs 单次限 4 文件；跑一次就够，重跑会重复注册资产。
- 大数字 1 亿：hero/counter 用 comma 格式 "100,000,000条"，hero fontSize 降至 130、counter 128 可容。

## 验证
- view_timeline_frames 抽 15 帧（9 定格 + 3 换卡后 2-4 帧 + 金句帧 + 片尾 2 帧）：
  换卡后字幕正好是该段首句（890/1812/2348）、计数器落点值（50%/33%/15天/25家/100,000,000条）、
  布局无折行、金句与口播同刻、片尾缩圈正常，全部通过。

## 封面
- HTML 流水线：cover/cover-2026-07-26.png（3:4 2160×2880）+ cover-2026-07-26-4x3.png（4:3 2880×2160），
  make_cover 内联 + make_cover_43 读本目录 episode.yaml（该 yaml 仅存封面数据）；抽查无折行。
- AI 海报（gpt-image-2 画字）：cover-2026-07-26-ai.png（3:4）+ cover-2026-07-26-ai-4x3.png，
  巨碑+乌云+小人构图，参考图=本期 ill-opus（7/23 cover-art 在 Windows 机上没有）。

## 交付状态
- 视频＝ChatCut 可编辑时间轴，用户在编辑器 Play 审核后自行导出；导出 mp4 放本目录 video/。
- caption.md（标题/正文/tag/章节，章节时间=whisper 段边界）已出。
