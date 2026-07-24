# 2026-07-24 制作记录（水墨MG动画版 · ChatCut · 8卡结构，沿用 7/23 风格）

## 项目
- ChatCut 项目「AI Briefcast 7/24 · 水墨MG版」projectId 70f10a02-6075-4c6a-9cb6-70bf18c6d161，
  1080×1920/30fps，总长 2956 帧（98.5s 旁白 + 片尾缩圈收尾）。
- 结构照抄 7/23：cover + 每主题 2 卡（隐喻卡+图表卡）×4 + outro + 全长字幕 MG；
  卡模板代码直接从 7/23 项目 inspect_asset 取回复用（改 props），图表卡 4 张按内容重写中段。

## 选题与核查
- ① AMD 投 Anthropic（E1 官方新闻稿 globenewswire 7/22）：股权投资至多 50 亿美元；至多 2 吉瓦
  Instinct MI450 系列（Helios 机架），首吉瓦 2027 上半年；双方用 Claude 优化 Instinct/ROCm；
  此前已在用 MI355X（首次披露）。稿中不念型号。
- ② 美军烧光"无限"token（E3 Wired 原报道，cybernews/techradar/slashdot 转述一致）：陆军
  Enterprise LLM Workspace 用 Ask Sage，5 年 4900 万美元；年度企业包 1 亿 token；5 月 CIO 宣布
  不限量、6 月中见底、上限恢复；每人每月至少 20 万 token 用完自动补；10 月后续约不明。
  slashdot 摘要"伊朗行动日耗 200 亿 token"查无原文佐证，弃用。
- ③ OpenAI Presence（E1 官方 7/22）：企业语音+文字 agent 平台；政策/护栏/许可动作配置；
  Codex 复盘生产对话提改进、人批准后生效；自家英文热线 75% 来电无需人工（自称，稿中带"自称"）；
  限量 GA，FDE/集成商部署，不开自助。
- ④ ReViV（arXiv:2607.17790，项目页核实；ETH Zürich+TU Delft+微软，ECCV 2026）：单目第一视角
  一次前馈同时重建 viewer+view；手部重建较 EgoAllo 快 100×、较 Dyn-HaMR 快 400×（稿中"快了几百倍"）；
  代码开源（权重未明确，只说代码）。
- 查重跳过：digest 头条① 世界模型（AlayaWorld 连续剧，7/11 做过）、快讯电费承诺（7/16 续报）。

## 素材
- 插图（codex 生图，参考 7/23 ill-gemini-v2 锚定水墨风）：ill-amd（双锦鲤循环+芯片AMD箭头+Claude芒星）/
  ill-army-monkey（★用户点名改：戴 US Army 钢盔的邪恶猴子往嘴里塞 token 珠，替换初版小麻雀；
  钢盔 US Army 是全片生成图里唯一允许的文字，一次过审）/ ill-presence（橘猫话务员+OpenAI花结）/
  ill-reviv（圆框眼镜左景右人）。
- 印章徽章：logo-amd（箭头）/ logo-army（五角星）/ logo-reviv（眼镜）新生成；logo-openai、
  outro-cat-ink 复用 7/23 文件。初版 ill-army.png（小麻雀）留档未用。
- 音频：broadcast-2026-07-24-mg.mp3（98.4s，S_HHgA 音色 rate36，synth_single_synced 整段合成）。
  本期无需 TTS 读法替换（无 X.Y 版本号）。

## 卡点与字幕
- whisper 词级对齐这次是好的（无空洞，gap≤0.24s），直接用词级边界；
  段边界帧＝[0, 82, 777, 1478, 2187, 2866]，音频末 2953。
- 字幕孤行处理：「态」并回上行；「ReViV」并回上行；「…至多2/吉瓦的算力」改切成
  「…AI芯片 / 建至多2吉瓦的算力」；「OpenAI发布了企业版agent平台Presence」超宽拆两行。
- a/b 卡切分（段内按字幕行边界）：1a 82-474 / 1b 474-777 / 2a 777-1250 / 2b 1250-1478 /
  3a 1478-1868 / 3b 1868-2187 / 4a 2187-2471 / 4b 2471-2866 / outro 2866-2956。
- 金句进场帧：1b/2b/3b/4b 用稿中金句实际口播时刻（614/1379/2110/2756 绝对帧换算相对帧）。

## 时间轴与 assetIds
- 轨道：V1 十张卡 / V2 subtitles-full（0-2956）/ A1 音频（0-2953）。
- MG：cover 35dfdb87 / card-1-amd 00e53e92 / chart-1-amd 147cf363 / card-2-army b440ce8d /
  chart-2-army 7ea8c6e7 / card-3-presence 0770effd / chart-3-presence 436ebdbb /
  card-4-reviv 39e31b65 / chart-4-reviv 435635f2 / card-9-outro afd3f6ff / subtitles-full 9da16425。
- 图：ill-amd f6e5b9f2 / ill-army-monkey 2d8d52e8 / ill-presence 42a45ca4 / ill-reviv 67325016 /
  outro-cat 562bf4b9 / logo-amd 93ce5de0 / logo-army e07a2cea / logo-openai 7772f669 / logo-reviv a0b68e0b。
- 音频 35da678d。

## 踩坑与经验
- MG 验证器：无 hero 变体卡里 inkSoftColor 读了没用会被拒（unused binding）——没用到的 props
  连 schema 一起删。
- PowerShell Start-Job 随会话结束被杀（会话不保状态）——codex 并行生图要用 Bash 后台任务。
- codex exec --cd 会在目标目录建 .git/.agents（已顺手留着，不影响）。
- 图表卡新图形全走 HTML div（管道/箭头/耗尽条），避开 canvas 三禁，云渲染帧验证一次过。

## 验证
- view_timeline_frames 抽 13 帧（9 定格 + 4 换卡/片尾）：布局、计数器落点值、字幕与卡同段、
  换卡后 2-3 帧字幕正好是该段首句、片尾缩圈正常，全部通过。

## 封面
- cover/cover-2026-07-24.png（3:4，hook=美军烧光无限token）+ cover-2026-07-24-4x3.png（抖音横版），
  make_cover 内联 + make_cover_43 读本目录 episode.yaml（该 yaml 仅存封面数据）。
- ★AI 海报封面（用户点名，codex/GPT 直接画字）：cover-2026-07-24-ai.png（3:4）+
  cover-2026-07-24-ai-4x3.png。参考 7/23 cover-art（巨物+浓烟+小人仰望）+ 本期猴子插图双参考图，
  巨猿倒罐构图；标题「美军烧光/无限token」、kicker、品牌名全由模型渲染，两张一次过零假字。
  经验：给足「必须一字不差+逐字自检」指令 + 双 -i 参考图，gpt-image-2 中文毛笔字可直接出片。
  原图 1086×1448 / 1448×1086（codex 内置生图分辨率上限），投稿够用。
