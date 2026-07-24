---
name: ai-briefcast-mg
description: 用 ChatCut MG 动画（手写 JSX Motion Graphic）做"每日 AI 速览"竖屏视频，替代 HTML 卡片版。
  选题/写稿/审核仍走 ai-briefcast-daily 的流程与文风铁律，本技能只管出片方式：豆包 TTS 旁白 →
  ChatCut 竖屏项目 → 水墨淡彩 8 卡结构（每主题 隐喻卡+图表卡，codex 水墨插图+logo 印章）→
  whisper 边界卡点 → 字幕 MG → 云渲染帧验证 → 用户在编辑器导出；封面可走 AI 海报
  （gpt-image-2 直接画字）。含「编辑隐喻拼贴」（Vox 风）风格变体（见 3b）。
  当用户说"做 MG 版 / 动画版 / ChatCut 版 / 拼贴版 / Vox 风（的播报视频）"时使用。
---

# AI Briefcast MG 动画版流水线（ChatCut）

首次跑通：2026-07-22（6 卡暖橙版）；2026-07-23 定型水墨 8 卡结构，7/24 全流程复刻验证
（卡代码跨天复用，半天出片）。与 HTML 版关系：**前置流程完全复用
ai-briefcast-daily**（数据复盘、选题查重、核查到源头、文风铁律、3 审核点、3 新闻+1 论文默认），
只有"出片"从 make_episode.py 换成 ChatCut。产物是可编辑时间轴，**导出由用户在编辑器里点**。

## 0) 前置

- 先按 ai-briefcast-daily 完成：选题（AskUserQuestion 一轮）→ 写稿（≤820 字硬预算、审稿过审）。
- ChatCut 插件已连接（mcp__plugin_chatcut_chatcut__*；未连则 ToolSearch 等待）。
- 依次加载技能：chatcut-plugin-basics-claude → create-motion-graphics（读其 canvas-pipeline-rules）。

## 1) TTS 旁白（本地，先于一切——卡点由它决定）

```python
import doubao_tts_ws   # ★必须先 import：触发 .env 加载。2026-07-22 事故：先读 env 拿到空
                        #  VOLC_SPEAKER2，回落默认 VOLC_SPEAKER=liziran 音色，被用户当场听出
import run_daily as rd, generate_broadcast as gb
from pathlib import Path
speaker = os.environ['VOLC_SPEAKER2']          # 用户克隆音色 S_HHgA...
segs = gb.split_segments(rd.strip_header(md))
segs_tts = [s.replace('Qwen 3.8', 'Qwen三点八') for s in segs]   # ★TTS 读法替换
mp3 = Path('output/<date>/audio/broadcast-<date>-mg.mp3')  # ★必须 Path：传 str 在
                                                            #  run_tts 的 .parent 处崩（7/24 踩）
durs = rd.synth_single_synced(segs_tts, mp3, print, speaker=speaker)
# durs 是返回值，自己落盘 durs.json；VOLC_SPEECH_RATE 不在 .env 里，
# ★命令行前缀显式给：VOLC_SPEECH_RATE=36 python ...（7/24 忘给时 rate=None 走默认语速）
```

- **★ 读法替换只进 TTS，不进字幕/卡片**：豆包把 "3.8" 读成"三月八日"（版本号带小数点必中招），
  合成前把 `X.Y` 版本号替换成 "X点Y" 中文；字幕行仍用原文（对齐按有声字比例，1-2 字差可容忍）。
- 音频改一次 = 全链路重排一次（对齐→字幕 MG 代码→边界→卡时长→卡位置），别嫌麻烦，见第 6 步。

## 2) ChatCut 项目

- `create_project`：1080×1920 / 30fps（不用 4K，导出 1080p 够用）。
- 立刻 `preview_start` 打开编辑器（browserHandoff.url，中文用户加 /zh/ 路径）；
  首次访问域名用户要点授权卡，"navigation denied"≈在等用户点，不是坏了。
- 传音频：`import_media create_session` → 跑插件 helper
  `node <plugin>/skills/asset-import/scripts/upload-media.mjs --token ... --endpoint ... <mp3路径>`。

## 3) 设计系统「新中式水墨淡彩」（2026-07-23 起当前默认，7/23、7/24 连用两期）

用户拿一张 codex 水墨柿子树猫图定调，替代 7/22 的暖橙扁平漫画风（旧风格见 3a 备查）。

- 色板：纸 #EFE8D9 / 墨 #37322A / 淡墨 #7A7261 / 柿子橙 #D96A28 / 纸片 #F7F1E2。
  字体仍 Smiley Sans + Noto Sans SC（★用 search_fonts 核实）。
- **★ 8 卡结构（用户点名，永久）**：每主题 2 张卡，前=隐喻卡（角标/标题/橙下划线/插图框/
  大数字滚动/chips/金句），后=图表卡（同头部+右上 logo 印章徽章+图表动画+计数器+chips+金句），
  解决"后半段没东西动"。a/b 切分点取段内字幕行边界（内容转折处），金句进场帧=稿中金句实际口播时刻。
- **★ 卡代码跨天复用**：新一期先 `inspect_asset(assetId, code=true)` 从上一期项目把
  cover/隐喻卡/图表卡/outro/字幕 5 套模板代码原样取回，只改 props 和图表中段——别重写。
  上一期 assetIds 在其 CHANGELOG.md。无大数字的隐喻卡用"无 hero 变体"（删 hero 块及其 props，
  chips 改纵排 top 1250）。
- **图表卡图形全用 HTML div 画**（管道+CSS 三角箭头、耗尽/量表条 width 动画、对比双条），
  天然避开 canvas 三禁；已验证机制：流程管道逐段点亮、条从满放空、涨到 N%+角标弹出、双条对比。
- **插图 = codex 生图水墨插画**（codex-imagegen 技能，Bash 后台并行跑）：
  横版 4:3（约 1448×1086），`-i` 传上一期插图锚定风格（可多个 `-i`）；每题 1 张隐喻图 +
  1 张 logo 印章徽章（方形，几何标志水墨橙填色）；通用徽章（OpenAI 花结等）和片尾猫图直接
  复用往期文件。**logo 做进生成图**（用户点名）：prompt 里描述 logo 几何形（四芒星/花结/AMD
  箭头方框/五角星），写明"除该标志外禁任何文字"。生成图默认禁字；用户点名要画字时
  （如钢盔 US Army），prompt 写"必须一字不差+逐字自检"，仅允许该处文字。
  流程仍是先出图→用户过图→再动时间轴。
- 数字动效：大数字滚动（interpolate+clamp+Math.round）、条形图长/缩、计数器
  （千分位 `String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ",")`）。

## 3a) 旧风格「暖橙编辑部 · 扁平漫画风」（7/22 首期用，备查）

- 色板：奶油底 #FFF3E6 / 柿子橙 #E8552F / 炭黑 #2A2118 / 琥珀 #F5A623；片尾深底 #2A2118。
- 卡结构 = 每段一张全屏 MG（1080×1920 不透明）：
  cover（品牌章+大标题两段弹入）→ 每条新闻/论文卡 → CTA（柿子树+橘猫 SVG+关注收藏分享）。
- 内容卡版式（用户调过的定稿参数）：角标 chip top **76**、大标题 Smiley top **205**（角标贴标题被用户
  点名改过，别回退）、橙色下划线、中部 SVG 漫画场景、下部要点 chips（白底黑框硬阴影，随旁白 spring
  滑入）、金句 punch（Smiley 橙色，段落后 2/3 处进场）。
- 插图 = 手写 SVG 漫画（粗描边扁平风）。**本连接器无 submit_image**，AI 位图走 codex-imagegen。

## 3b) 风格变体「编辑隐喻拼贴」（Vox 风，用户点名"拼贴版/Vox 版"时启用）

抄自 ray-broll（github.com/imraywang/rayskills，源头 gbro-collage-broll MIT）。只换视觉层：
选题/写稿/TTS/卡点/字幕全部照旧；不用视频模型——动画走 MG 确定性渲染（= 他家 HyperFrames
路线，零生成成本、无限重跑）。

- **视觉语法**（每卡必过的 4 检）：一眼看懂隐喻；主要物件 ≤4 组且能分开动；主体集中在画面
  中间约七成、色场留白足够；无假字/logo/水印/UI。一句话只做一个隐喻，别堆符号
  （时钟灯泡箭头齿轮全塞进去=没有重点）。
- **卡结构**：底 = 强烈平坦纯色场（按语意选色，相邻卡必须换色）；主体 = 黑白半调照片剪贴
  （halftone 网点感）+ 少量彩色卡纸；文字仍全走 MG 文字层（Smiley Sans 标题/chips/金句，
  天然零假字）——AI 图内**全程禁字**。
- **色彩语义**：焦橙/红=时间消耗、紧迫；芥末黄=工具、警示；墨绿/深青=认知、判断、自动执行；
  深紫=规范、沉淀。点色统一在奶油白/芥末黄/橙一族。
- **贴纸生成**（用 codex-imagegen 技能，不需要 Gemini key）：
  1. 先出**完成态静帧**给用户过审（构图确认，便宜的那道门）；
  2. 过审后按物件逐张出**透明底贴纸 PNG**（以静帧为参考图保持风格一致）；
  3. 贴纸传 ChatCut，MG 里 absolute 定位逐件入场。
  静帧 prompt 模板（物件含便签/卡片/书页时必加 "carrying only abstract wavy squiggle
  doodle lines — absolutely no letters"，否则大概率假字，出假字回静帧重做别想后期修）：

  ```text
  Editorial paper-collage still expressing [一句话视觉命题].
  Flat [颜色] paper field background with subtle uncoated paper fiber.
  Black-and-white halftone photographic cut-outs mixed with selective [点色] colored cardstock.
  Vertical 9:16, central subject within middle 70%, generous negative space,
  [N] large separable paper groups. Visible halftone dots, crisp cut edges,
  thin warm-cream paper keylines, soft low-opacity drop shadows.
  Avoid: no typography, no letters, no numerals, no logos, no watermark, no UI,
  no glossy 3D, no photoreal environment, no clutter.
  ```

- **定格动画质感**：入场动画把进度量化成 4-6 格（`Math.floor(p*N)/N`）做逐格滑入/卡位 +
  小幅 overshoot settle，镜头锁死不推近、不整体淡入、不让所有东西一起漂。落点别目测：
  先渲一帧只有承载结构的画面对着标（贴纸锚点未必是几何中心）。

## 4) MG JSX 硬约束（违者云导出黑屏/崩溃）

- 合同：无 import、`const Component = ({item}) =>`、根 `<div style={rootStyle}>`、逻辑全部在 return
  前算好、props 从 `item.props` 读且**不加 `||` 兜底**、可见文字和主色都声明成 properties、
  加 `transparentBackground` 布尔。
- canvas 三禁（create-motion-graphics/references/canvas-pipeline-rules.md）：
  ① SVG 内层元素禁 `transform` 属性（只许最外层 g；旋转/位移一律包一层 div 用 CSS transform）；
  ② `<svg>` 元素本身禁动画 CSS opacity/transform（包 div）；
  ③ SVG 内层禁 `opacity` 属性（烧成 rgba 颜色）。
- 毛玻璃 backdropFilter 同属禁区——**字幕底用半透明黑 rgba(0,0,0,0.58) 圆角条+白字** 代替
  （纯色底上视觉等价，用户接受）。
- 双状态表情（晕→笑）：两个 svg 叠放，外层 div 按帧 opacity 0/1 切换（div 上的 opacity 安全）。

## 5) 铺时间轴（edit_item 字段名，试错试出来的）

- **add**：`{type, assetId, from(帧), durationInFrames, trackId可省}`；音频省 trackId 自动建 A1。
- **update**：`{id, fromFrame, durationInFrames}`；**delete**：`{id}`。没有 startFrame/itemId。
- 卡片全放 V1 顺序排；字幕 MG 单独一条（省 trackId 自动建更高视频轨，order 大=在上层）。
- MG 资产时长改法：`edit_asset update json={"type":"motion-graphic","durationInSeconds":X}`；
  资产时长（edit_asset）和条目时长（edit_item）是两处，都要改。

## 6) 卡点 + 字幕（whisper 边界，和 HTML 版同一条铁律）

分段测时对含英文词的段会低估（本次研究卡早切 1.7s），**必做 whisper 校正**：

```python
import make_xhs_video_html as mx
lines = mx.subtitle_lines(segs)                      # 展示文本（原文，含 Qwen 3.8）
times = mx._align_whisper(lines, mp3)                # 词级强制对齐
sub = [{'s': round(s*30), 'e': round(e*30), 't': l['text']} for l,(s,e) in zip(lines,times)]
# 段边界 = 每段首行的 s；末尾 = round(total*30)
```

- **★ 词级对齐先体检再用**（7/23 坏、7/24 好，两种都遇过）：逐行看 gap 和覆盖率——
  行间 gap 全 ≤0.3s 即健康，直接用词级边界；出现 3s+ 空洞/大段字没认出（7/23 只认出 421/695 字）
  则降级用 whisper 整段级 segment 起点当段边界 + `mx._align_durs` 字数比例摊行内。
- 字幕 = 一个全片时长的 MG：LINES 数组烧进代码（★验证器只许顶层函数，LINES 包进
  `const getLines = () => [...]`），按帧找 active 行渲染底部居中黑条白字
  （top 1768 / 46px / maxWidth 980 nowrap；pillColor/textColor 留成可编辑属性）。
  烧之前修行：① 1-3 字孤行（"态"/"ReViV"）并回上一行；② 断在数字/词中间的
  （"…至多2/吉瓦"）把字挪到后一行重切；③ 估宽 >980px 的长行（中文≈46px/字+拉丁≈25px/字，
  如 "OpenAI发布了企业版agent平台Presence"）按字数比例拆两行。
- 卡片 items 的 from/durationInFrames 全部按 whisper 边界写；MG 内部动效帧不用改
  （都是"进场→定格"设计，段变长只是多停）。

## 7) 验证（成功的工具调用≠验证）

- `view_timeline_frames` 一次抽 6-9 帧：每卡定格帧 + **换卡后 2-4 帧**（字幕应正好是该段第一句）。
- 签名 URL 用 python urllib 下载到 scratchpad 再 Read 看像素；确认：角标/标题间距、无折行、
  数字动效值合理、字幕与卡同段、CTA 正常。
- 有问题：位置/时长错 → edit_item；画面错 → edit_asset 全量替换 code。

## 8) 交付

- 用户在编辑器点 Play 审、自己导出（或要求时走 export skill）；导出的 mp4 放 output/<date>/。
- caption.md 照 daily 技能第 7 步（标题/正文/标签/章节；章节时间=whisper 段边界，论文链接查证编号）。
- 封面两条路（都出，用户挑）：
  ① HTML 流水线：内联设 make_cover 的 KICKER/BIG/ROWS/DATE 后调 mc.main()（ROWS 行数=当天条数）；
    4:3 横版写个只含 cover3x4 的 episode.yaml 再跑 `make_cover_43.py --date <date>`。
  ② **★AI 海报封面（7/24 起用户点名喜欢，gpt-image-2 直接画字）**：codex 生图出 3:4+4:3 两张，
    构图学 7/23 cover-art「巨物+浓墨乌云+底下小人仰望」的压迫感；`-i` 传两张参考
    （往期 cover-art 定气势 + 当期插图定主角形象）；文字全列清楚（大标题两行、kicker、
    品牌名，重点词标柿子橙），prompt 写"必须一字不差，除指定文字禁任何其他文字水印，
    生成后逐字自检"——毛笔中文+英文一次过率高。出图后自己逐字核对再给用户。
    分辨率上限约 1448px 长边，投稿够用；要更高清走超分。
- CHANGELOG.md 照记：assetIds、边界帧、纠错、踩坑。

## 排错速记

- 音色不对/像 liziran → env 加载顺序（第 1 步★）。
- 数字读成日期 → TTS 读法替换（第 1 步★）。
- 卡比声音早/晚几秒 → 没做 whisper 边界校正（第 6 步）。
- 预览正常导出黑屏 → canvas 三禁踩了哪条（第 4 步）。
- edit_item 报 unknown field → add 用 from、update 用 id+fromFrame（第 5 步）。
- submit_image 不存在 → 该连接器版本没有图片生成，走 codex-imagegen 本地生图再上传。
- 浏览器 navigation denied → 等用户点授权卡，重试同一 navigate。
- synth_single_synced 报 `'str' object has no attribute 'parent'` → mp3 参数要 Path 不是 str。
- MG 验证器拒 "unused binding" → 读了没用的 props（如无 hero 变体里的 inkSoftColor），
  连 schema 声明一起删；顶层只许函数（数组常量包进 helper 函数）。
- codex 并行生图别用 PowerShell Start-Job（会话不保状态，Job 随会话被杀）→ 用 Bash
  run_in_background，一个任务一条命令，完成有通知。
- 上传图片的 S3 URL 规律：`.../projects/<projectId>/assets/image/<assetId全uuid>/<原文件名>`，
  写进 MG 的 image prop defaultValue 用（browse_assets 的 thumbnail url 去掉 `-thumbnail.jpg` 同理）。
