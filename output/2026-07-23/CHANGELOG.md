# 2026-07-23 制作记录（水墨MG动画版 · ChatCut · 8卡结构）

## 结构与风格（本期新定型）
- **视觉风格「新中式水墨淡彩」**：用户拿一张 codex 生成的水墨柿子树猫图定调（宣纸底/墨色主体/柿子橙点缀），
  替代 7/22 的「暖橙编辑部扁平漫画风」。原图＝assets/outro-cat-ink.png，兼作片尾。
  色板：纸 #EFE8D9 / 墨 #37322A / 淡墨 #7A7261 / 柿子橙 #D96A28 / 纸片 #F7F1E2。字体仍 Smiley Sans + Noto Sans SC。
- **★ 8 卡结构（用户点名，永久经验）**：每主题 2 张卡（前=隐喻卡、后=图表动画卡），解决"后半段没东西动、
  注意力掉"的问题。图表卡含条形图长缩、计数器滚动、对比条、流程链逐节点点亮（MG 代码画，确定性动画）。
- **★ logo 做进生成图（用户点名）**：Gemini 四芒星、OpenAI 花结、五巨头 G/田字/微笑箭头/∞/圆环、QQ 企鹅，
  全部由 codex 按参考图水墨风生成（隐喻图内嵌 + 独立印章徽章两套）。生图流程＝先出图→用户过图→再动时间轴。
- 项目：AI Briefcast 7/23 · 水墨MG版（projectId 57edd7fd-cdae-41a3-a265-7138a0bce1a2），1080×1920/30fps，
  总长 2730 帧（91s：90s 旁白 + 1s 片尾缩圈）。

## 选题与核查
- 头条1 Gemini 三连发（blog.google 7/21）：省 17% token=Artificial Analysis 第三方、编程省 65%=Datacurve DeepSWE
  第三方；Flash-Lite 350 token/s；Cyber 仅 CodeMender 内政府+受信伙伴试点；3.5 Pro 内测；Gemini 4 官宣开训。
- 头条2 ChatGPT 开放广告（7/22 全面开放自助 Ads Manager）：2 月测试→4 月邀请制（门槛 20 万→5 万美元）→全面开放；
  广告在回答下方、仅 Free/Go 档；OpenAI 自报今年 25 亿、2030 目标 1000 亿（emarketer 转述）；Altman 2024"最后手段"转述。
- 头条3 日经账外债：五家（Alphabet/微软/亚马逊/Meta/甲骨文）账外 1.65 万亿 > 账面 1.35 万亿，4 年 8 倍；
  Meta 4200 亿≈公开 3 倍。E3 独立调查。
- 论文 RxBrain（arXiv:2607.14187 已核实，腾讯 Robotics X+福田实验室+混元）：6.2B MoT，语言+视觉想象同一条计划序列，
  权重 Apache 2.0 已放；限制=单序列误差串联。SEED/宏观谬误/SearchOS 前两天已用，仅剩此篇。

## 踩坑与经验
- **whisper 词级对齐这次是坏的**：word_timestamps 模式只认出 421-622/695 字，中段出现 33s/9.6s 空洞，比例映射全歪。
  改用 **whisper 整段级识别的 segment 起点当段边界**（[2, 27, 45, 66, 88]，与 durs 预估互验），
  字幕行=段边界锚定+字数比例（mx._align_durs），1-3 字孤行并回上一行。
- TTS 读法替换：3.6/3.5→三点六/三点五、1.65万亿→一点六五万亿（防"三月八日"式误读）；只进 TTS 不进字幕。
- synth_single_synced 签名是 (segments, out_mp3, log函数, speaker)，durs 是返回值需自己落盘（两次踩错参数）。
- MG 验证器新规：顶层只许函数（LINES 数组要包进 helper 函数）；声明未用的 props 读绑定会被拒。
- codex 生图带品牌 logo 可行且效果好：参考图 -i + 明确描述 logo 几何形（四芒星/六瓣花结/田字/微笑箭头/∞/圆环），
  prompt 写"除该 logo 外禁任何文字"，8/8 张一次过审。

## 时间轴（帧，30fps）
- 边界：cover 0-60 / 1a 60-385 / 1b 385-810 / 2a 810-1107 / 2b 1107-1350 / 3a 1350-1663 / 3b 1663-1980 /
  4a 1980-2360 / 4b 2360-2640 / outro 2640-2730；字幕 V2 全长；音频 A1 0-2700。
- 章节（caption 用）：00:00 / 00:27 / 00:45 / 01:06。

## 素材 assetIds
- 音频 97943b7c（90.0s，S_HHgA 音色 rate36）
- MG：cover 4a6c27d5 / card-1 7fe35a36 / chart-1 bda38a27 / card-2 37ee78ce / chart-2 14e86c70 /
  card-3 72d5246b / chart-3 9d03a787 / card-4 5cc50741 / chart-4 229a44c3 / outro 7806a90e / subtitles 2846ed4e
- 图：outro-cat-ink 3feba287 / ill-gemini-v2 2968cf8e / ill-ads-v2 63ef29a3 / ill-debt-v2 493a64fc /
  ill-robot-v2 294ed9bc / logo-gemini 48040f1d / logo-openai 35cf1cf8 / logo-five 5154ed8d / logo-penguin 7dd0321d
  （v1 无 logo 版 ill-* 四张已弃用，本地留档）
- 封面：cover/cover-2026-07-23.png（HTML 流水线 make_cover 单出，hook=ChatGPT要有广告了）
