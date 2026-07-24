# 2026-07-22 制作记录（首次 MG 动画版 · ChatCut）

## 结构变更
- **本期起默认 3 新闻 + 1 论文**（用户选题时点名，SKILL.md 已同步改）。
- 本期不走 make_episode HTML 卡片版，改做 **ChatCut MG 动画版**（用户要求）：
  项目 `AI Briefcast 7/22 · MG动画版`（projectId bb7b8335-5a94-4c3c-95fe-3228827a3444），
  1080×1920 / 30fps / 100.2s，6 个手写 JSX Motion Graphic（封面/头条/研究/诉讼/论文/片尾），
  设计方向「暖橙编辑部 · 扁平漫画风」（奶油底 #FFF3E6 + 柿子橙 #E8552F + 炭黑 #2A2118，
  标题 Smiley Sans 得意黑、正文 Noto Sans SC，插图全部手写 SVG）。

## 选题与核查
- 头条：Kimi K3 + Qwen 3.8（7/19 WAIC 预览，2.4T 参数，阿里自称"仅次于 Fable 5"，无跑分/模型卡）
  同周对标 Fable 5 并承诺开源权重；白宫顾问圈公开互撕（Sacks"闭源双头垄断想借政府消灭开源"原话，
  Axios/MIT TR/TechCrunch 7/20；Sacks 骂 Anthropic woke 的话未用）。
- 研究：arXiv:2607.13562（米兰比可卡+巴黎高师+罗马一大）：有 AI 建议后敢说不知道 44%→3%、
  准确率 27%→9%、信心 30%→76%；发钱只拉回 8%/16%。
- 诉讼：索尼 7/20 纽约南区二告 Udio，30117 首（6/29 法官拒并旧案）；45 亿美元为媒体按法定上限估算。
- 论文：SearchOS（进度外置成表+外部判停）。

## 踩坑（重要）
- **★ 音色事故**：合成时在 `doubao_tts_ws` 加载 `.env` 之前读了 `os.environ['VOLC_SPEAKER2']`，
  取到空回落默认 `VOLC_SPEAKER`＝liziran 音色，被用户当场听出。修法＝先 `import doubao_tts_ws`
  （触发 _load_dotenv）再读环境变量，重配后 85.8s→100.2s（用户音色语速更从容），
  ChatCut 时间轴删旧音频、6 个 MG 按新卡点重排+资产时长拉长。
- ChatCut edit_item 字段名：放置用 `from`（帧）+`durationInFrames`；更新/删除用 `id`+`fromFrame`，
  没有 startFrame/itemId。
- 本连接器（chatcut 0.2.18）**没有 submit_image**（music/video/voice/sound 都有），
  gpt-image-2 插画不可用；本期插图全部手写 SVG（含特朗普漫画形象、国会、法槌黑胶、迷宫机器人、柿子树猫）。
  SVG 遵守 canvas 管线三禁：内层元素禁 transform 属性、svg 元素禁动画 CSS、内层禁 opacity 属性（rgba 代替）。

## 二轮修改（用户审阅后）
- 四张内容卡角标（tag chip）上移 120→76，与标题拉开间距（用户点名太近）。
- 加全片字幕 MG（assetId ab4ef2d3，单独视频轨 V2）：55 行，脚本原文 whisper 强制对齐（复用
  make_xhs_video_html.subtitle_lines + _align_whisper），黑色半透明底(0.58)白字 46px 底部居中。
  真 backdrop 毛玻璃会踩 canvas 管线黑屏坑且纯色底上无差别，用半透明黑替代。
  对齐切碎的孤行（"个实验/庭/训练数据"）手动并回上一行。

## 素材
- 音频：audio/broadcast-2026-07-22-v2-myvoice.mp3（=broadcast-2026-07-22-spacex.mp3，S_HHgA 音色，
  rate36，100.15s），durs [1.99, 26.39, 25.69, 20.01, 23.19, 2.87]。
- ChatCut MG assetIds：封面 820b4386 / 头条 cb565b35 / 研究 6c7bba1a / 诉讼 5a5800d8 /
  论文 8643a01a / 片尾 8ee2d0c1；音频 9e162bae。
