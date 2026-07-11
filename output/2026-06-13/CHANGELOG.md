# 2026-06-13 AI Briefcast

## Scope

- 内容日期：使用 6/12 新闻与论文，生成 6/13 小红书 AI 速览。
- 头条：SpaceX IPO 冲高又回落，切入「AI 泡沫最后的疯狂？」。
- 选稿：版本 B（沉稳串点）作为音频基线。

## Verification

- SpaceX IPO：公开报道核到 135 美元发行价、750 亿美元募资、首日冲高至 176.52 后收 161.11 附近。
- botsitting：Glean Work AI Institute 报告核到 6000 名白领、87% 使用 AI、75% 自觉更高效、13% 认为组织显著受益、每周 6.4 小时收尾。
- 供应链投毒：核到 Miasma / Shai-Hulud 相关攻击波及 73 个 Microsoft GitHub 仓库、Azure / CI/CD / 开发者凭据风险。
- 论文：核到 One Token per Multimodal Evidence 与 WorldOlympiad 两篇 arXiv 摘要。

## Decisions

- 采用整段一次豆包 TTS，`VOLC_SPEECH_RATE=50`，优先 `VOLC_SPEAKER2`。
- 卡片共 14 张：封面目录 1、内容/补充卡 12、CTA 1。
- SpaceX 组内「OpenAI / Anthropic 同期冲刺 IPO」补充卡改成更稳的「AI 上市潮」，不写未核到的具体交表日期与估值。

## Outputs

- 音频：`output/2026-06-13/audio/broadcast-2026-06-13-spacex.mp3`
- 卡点：`output/2026-06-13/audio/durs.json`，7 段，总长 93.14 秒。
- 卡片：`output/2026-06-13/cards/card-*.png` 与 `cards.json`，共 14 张。
- 视频：`output/2026-06-13/video/xhs-2026-06-13-spacex.mp4`，2160×3840，97.25 秒（4 秒片头 + 93.14 秒旁白）。
- 封面：`output/2026-06-13/cover/cover-2026-06-13.png`，2160×2880。
- 标题/正文/标签：`output/2026-06-13/caption.md`。

## Revision

- 按用户要求移除开头小猫视频，视频开头直接进入 6/13 新闻目录卡。
- 改成片尾：最后一张 CTA 卡静态显示 `片头/图片_20260606072137.png` 的圆形裁切图，随后 1 秒原地缩小到消失。
- 将发布文案、视频目录卡与 3:4 封面里的时长表达统一为「1分钟」。
- 更新后视频：`output/2026-06-13/video/xhs-2026-06-13-spacex.mp4`，2160×3840，94.21 秒（93.14 秒主体 + 1 秒片尾），无片头。
