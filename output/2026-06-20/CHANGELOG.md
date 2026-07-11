# 2026-06-20 AI Briefcast

## Scope
- 内容日期：使用 **6/19 新闻与论文**，生成 6/20 小红书 AI 速览。
- 形态：3 新闻 + 2 论文；**无片头 + 猫图片尾**；**带字幕（字号 96）**；**语速 1.25×（rate 36）**；目标 ≤100s。
- 原始素材：`samples/source-2026-06-19.md`
  - digest: https://ai-digest.liziran.com/zh/digest/2026-06-19-white-house-forced-anthropic-cut-off-one-biggest-korean.html
  - brief : https://ai-brief.liziran.com/zh/daily/2026-06-19-looped-transformer-test-time-compute.html

## Selection（用户确认）
- 新闻 3 条：① 白宫令 Anthropic 切断韩国 SK Telecom 对最强模型 Claude Mythos 的访问权（涉华，出口管制令；接 6/18「一键关停」续集）/
  ② Z.ai 以 MIT 许可开源 GLM-5.2（7530 亿参数、激活 400 亿、百万 token，疑似最强纯文本开源权重）/
  ③ Adobe 把对话式 AI 助手装进 PS/Pr/Ai 全线 + Firefly 工作室重做。
- 论文 2 篇：LoopCoder-v2（循环加深计算只能加两层，SWE-bench 43→64，3 次以上退化）/
  ZPPO（老师放进 prompt 而非梯度，4 规模全超蒸馏，越小越受益）。

## 文稿（B 沉稳串点 · 用户偏好定稿，直接写 B-changed）
- `scripts/broadcast-0620-B-changed.md`：去掉所有「：」「——」、一句一意、先因后果、收尾只留署名（沿用 6/19 偏好）。
- 长度迭代：v1 99.9s 压线 → v2 微删最长段（白宫/LoopCoder）留余量 → 终版 **95.1s**。
- 音频 `audio/broadcast-2026-06-20-spacex.mp3`（克隆音色 S_HHgApOH42，整段一次合成）+
  `audio/durs.json` `[2.18,16.43,16.64,16.50,20.81,20.24,2.34]`（总 95.1s，7 段卡点）。

## 卡片（14 张，交互式选卡 AskUserQuestion）
- 内容卡「3 选 1」：卡1=②事实「白宫令断供」/「同周首尔刚挂牌」、卡2=②数字「753B 开源」/「最强开源权重」、
  卡3=②事实「全线装AI助手」/「一句话替你改图」、卡4=①反差「只能循环两次」/「再深就退化」、
  卡5=①观点「老师该站哪」/「放进提示，别塞梯度」。
- 补充卡「候选池多选」共 7 张，逐个 WebSearch 查证：Claude Mythos（强到不公开）/ 开源权重 / Firefly（Adobe Stock 训练、可商用）/
  循环 Transformer / test-time compute / 强化学习后训练 / 全错就白学。
- 同新闻同色分组 c1/c3/c4/c5/c2；组内权重 内容卡 1.5、补充卡 1.0。

## 视频 / 封面
- `video/xhs-2026-06-20-spacex-sub.mp4`（发布用，带字幕）+ `video/xhs-2026-06-20-spacex.mp4`（无字幕基底）+ `video/subs.ass`。
  - ffprobe：**2160×3840、30fps、96.17s**（95.1 旁白 + 1s 片尾）。字幕 whisper 对齐 663↔670 字、54 行。
- 片尾圆形猫照 1s 缩小消失；字幕字号 96（6/19 起固化放大）。
- 封面 `cover/cover-2026-06-20-spacex.png`（待生成；BIG 待定）。

## 标题 + 文案 + 投稿
- 标题（用户选 权力+悬念，精简到 20 字）：「白宫下令，切断最强Claude的韩国客户」。
- `caption.md`：正文无 emoji、五条短句、结尾 @柿子树下的猫wanjeans；标签 10 个（热点 #Anthropic #Claude #开源大模型）。
- `publish.json`：`make_publish.py` 生成（投稿数据源）。
- ⚠️ 投稿沙箱：Claude-in-Chrome 的 file_upload 仅接受会话共享目录，当前 unsupervised 模式下目录授权弹窗不可用；
  待切到 supervised 模式后授权仓库目录即可全自动上传（见 memory xhs-publish-automation）。
