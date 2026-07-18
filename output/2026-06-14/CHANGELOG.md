# 2026-06-14 AI Briefcast

## Scope

- 内容日期：使用 6/13 新闻与论文，生成 6/14 小红书 AI 速览。
- 用户指定头条：Claude Fable 5 全球禁用，仅存活 3 天。
- 用户选择：新闻 A+C，论文 A+B。

## Selection

- 新闻主线：Claude Fable 5 / Mythos 5 暂停访问；AI agent 烧出 6531.30 美元 AWS 账单；OpenAI 嵌进企业培训、教育和 Oracle 云采购；Google AI 诈骗诉讼与 DeepMind multi-agent 安全基金。
- 论文主线：Arbor（Hypothesis Tree 自主科研）与 RACES（可验证环境递归组合）。InternVideo3 / Bebop 暂作为扩展备选，避免稿件过长。

## Verification Notes

- 6/13 原始素材来自 `samples/source-2026-06-13.md`。
- Claude Fable 5 头条为用户指定突发角度，已按公开报道口径写成「暂停访问 / 拉闸」，正文明确说明是出口管制合规引发，非把所有 Claude 模型描述为停用。
- 当前已输出 A/B 两版文稿：
  - `output/2026-06-14/scripts/broadcast-0614-fable5-A.md`
  - `output/2026-06-14/scripts/broadcast-0614-fable5-B.md`

## Rewrite

- 按用户反馈重写 B 版：
  - 不使用「第一条 / 第二条 / 第三条」式描述。
  - 收敛为 3 条新闻 + 2 篇论文。
  - 移除 OpenAI 企业流程新闻，保留 Fable 5、DN42 AWS 账单、Google/DeepMind 安全监管。
  - 移除总结段，文稿停在第二篇论文 RACES。

## User Edited Version

- 用户确认修改后的最终稿放在 `output/2026-06-14/scripts/broadcast-0614-fable5-B-changed.md`。
- 后续音频与卡片均以 `B-changed` 为源，不覆盖用户手改稿。
- 用户要求缩短 2/3/4/5 四条内容后，已在 `B-changed` 内压缩为更短段落。

## Audio And Cards

- 使用 `B-changed` 生成豆包克隆音色整段音频：`output/2026-06-14/audio/broadcast-2026-06-14-fable5.mp3`。
- 音频卡点写入 `output/2026-06-14/audio/durs.json`，总长约 90.05 秒，7 个音频段。
- 渲染卡片到 `output/2026-06-14/cards/`，共 13 张：封面 + 5 张内容卡 + 6 张信息补充卡 + CTA。
- 卡片结构写入 `output/2026-06-14/cards/cards.json`，按音频分组切卡点；当前仅出音频和卡片，未合成最终视频。
- 按用户此前要求，不使用小猫片头；CTA 卡 `card-13.png` 已放入圆形猫图，另存 `card-13.plain.png` 作为后续 1 秒圆形缩小片尾动画的无图背景。

## Video

- 合成最终 4K 竖屏视频：`output/2026-06-14/video/xhs-2026-06-14-fable5.mp4`。
- 视频不使用小猫片头，第一帧直接进入新闻封面。
- 结尾追加 1 秒猫图圆形缩小消失片尾；中间文件为 `_main-2026-06-14-fable5.mp4` 与 `_outro-2026-06-14-fable5.mp4`。
- ffprobe 校验：`2160x3840`，30fps，时长约 91.09 秒，含 AAC 立体声音轨。
- 抽帧 QA 存在 `output/2026-06-14/video/_qa/`：开头为新闻封面，片尾猫图缩小正常。

## Cover

- 生成 3:4 小红书封面：`output/2026-06-14/cover/cover-2026-06-14-fable5.png`。
- 封面主钩子为 `Fable 5 只活3天`，下方列出 5 条内容摘要。
- 尺寸校验：`2160x2880`；人工检查未见文字溢出或重叠。
