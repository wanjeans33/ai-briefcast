# 2026-06-17 AI Briefcast

## Scope

- 内容日期：使用 **6/16 新闻与论文**，生成 6/17 小红书 AI 速览。
- 形态：3 新闻 + 2 论文；**片尾**圆形猫照（无片头）；**首次加字幕**（用户要求）。
- 原始素材：`samples/source-2026-06-16.md`
  - digest: https://ai-digest.liziran.com/zh/digest/2026-06-16-meta-feeds-your-facebook-posts-strangers-audit-says-rio.html
  - brief : https://ai-brief.liziran.com/zh/daily/2026-06-16-code-agent-data-sandbox-vla-latent-reasoning.html
- 与 6/16 视频（用 6/15 新闻）无重复。

## Selection（用户确认）

- 新闻 3 条：① Meta AI Mode 把公开帖变成别人搜索的 AI 答案 / ③ 里约 397B「自研」被扒成 Qwen 基座 0.6:0.4 加权合并 / 快讯 对地观测卫星首次自主锁定目标。
- 论文 2 篇：CODA-BENCH（代码+数据沙箱，最强 61.1%）/ AVA-VLA（潜在推理+提前退出，LIBERO 98.3%、快 6 倍）。
- 风格：直接 B 沉稳串点，主线「自主 × 真实」。

## Audio

- 源：`broadcast-0617-spacex-B.md`；克隆音色 `S_HHgApOH42`，rate 50（≈1.4×），整段一次合成。
- 长度：首版 ~108s（超 90），收紧 Meta/里约两段（数字全留）→ 重合成 **93.2s**。
- 输出 `audio/broadcast-2026-06-17-spacex.mp3`，7 段卡点 `audio/durs.json`：`[1.9, 15.1, 17.9, 13.7, 16.7, 17.3, 10.6]`。

## Cards（12 张）+ Video（4K + 圆形猫片尾）

- 封面 + 5 内容卡（c1/c3/c4/c5/c2）+ 5 信息补充卡 + CTA。
- 5 补充卡逐个 WebSearch 查证：语境崩塌（context collapse）/ 模型合并（不训练按比例加权拼）/ 在轨自主（卫星天上自决、响应从天缩到分钟、下行减≤80%）/ 沙箱测评 / 思维链 CoT（显式 vs 潜在）。
- 卫星两张卡保持事实克制（首次、无地面指令）。
- 视频 `video/xhs-2026-06-17-spacex.mp4`（无字幕基底）：`2160x3840`、30fps、约 94s（93.2 旁白 + 1s 片尾）。
- 备注：首跑 compose 时遇一次外部工具中断、video/ 为空，重跑即成。

## Subtitles（首次 · 新增能力）

- **方法**：用脚本原文 + faster-whisper(base) 词级时间戳做**强制对齐**（不用 ASR 文本，避免 Nex/Qwen/CODA-BENCH/AVA-VLA 被转错）：
  1. 脚本按标点切成 ≤16 字的字幕行（64 行，有声字 724）；
  2. whisper 取词级时间 → 展开成「有声字 → 时间」序列（708 字），按字数比例把脚本行映射到时间；
  3. 写 ASS（微软雅黑 82、半透明黑底 BorderStyle=3、底部居中）；
  4. ffmpeg `ass=` 滤镜烧进基底视频（相对路径避开 Windows 盘符冒号转义）。
- 无 whisper/离线时**自动回退** durs 按段比例分配（精度略低，有段间停顿漂移）。
- **字幕位置**：初版 MarginV=300 贴底，与内容卡金句相挤 → 用户要求**抬到正文与金句间的空白带**，改 MarginV=820（约 78% 高度），point/explainer 两类卡均清爽。
- 成品：`video/xhs-2026-06-17-spacex-sub.mp4`（**带字幕，发布用这个**），`2160x3840`、94.2s；字幕源 `video/subs.ass`。
- QA 抽帧 `video/_qa/sub2-*.png`：字体无乱码、对齐准、不压金句/关联/水印。

## 待办

- 3:4 封面 + 标题/正文/话题标签：尚未做（用户此次到带字幕视频为止）。
- 字幕目前是一次性脚本（已删）；如需每日常态化，建议把"whisper 对齐 + ASS 烧录"折进 `make_xhs_video_html`，并更新 skill。
