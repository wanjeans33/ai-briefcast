# AI Briefcast 🎙️

> 每日 AI 新闻播报 —— 把每天的 AI 简报变成可以「听」的播客。
> Your daily AI news, turned into a podcast you can listen to.

**简体中文** | [English](#ai-briefcast-english)

---

## 简介

**AI Briefcast** 自动抓取每日 AI 资讯与论文简报，整理、改写成适合朗读的播报稿，并通过文本转语音（TTS）生成音频，让你每天用几分钟「听」完 AI 圈最重要的进展。

## 内容来源

播报内容来自以下两个高质量、以一手信源为主、不炒作的中文 AI 简报：

| 来源 | 说明 | 链接 |
| --- | --- | --- |
| **AI 资讯速览** | 每日精选的 AI 行业新闻，英文一手信源、如实呈现，不炸裂、不夸张、不接商单。 | <https://ai-digest.liziran.com/zh/> |
| **AI 论文简报** | 每日精选 arXiv 前沿论文摘要，面向创业者 / 产品 / 开发者，每篇附原论文链接可自行验证。 | <https://ai-brief.liziran.com/zh/> |

> 注：内容版权归原作者所有。本项目仅做聚合与播报用途，请遵守来源网站的使用条款。

## 设计目标

- **每日自动更新**：定时抓取最新的资讯与论文简报。
- **播报稿生成**：将原文整理、改写成自然、口语化、适合朗读的稿件。
- **语音合成**：通过 TTS 生成每日音频播报。
- **多种分发方式**（规划中）：RSS 播客订阅、音频文件、文字稿。

## 工作流程（规划）

```
抓取来源  →  内容清洗 / 去重  →  播报稿改写  →  TTS 语音合成  →  发布 / 订阅
 (fetch)      (clean)            (script)        (synthesize)     (publish)
```

## 技术选型

- **TTS 引擎（评估中）**：在以下方案之间选择 ——
  - [Qwen3 TTS](https://github.com/QwenLM)（通义千问 TTS）
  - [Doubao Seed TTS 2.0](https://www.volcengine.com/)（豆包 / 火山引擎）
  - 评估维度：中文自然度、音色多样性、价格、并发与延迟、长文本稳定性。

## 项目状态

🚧 **早期开发中。** 目前仓库处于初始化阶段，本 README 描述的是项目目标与规划，功能尚未实现。

## 路线图

- [ ] 来源抓取（ai-digest / ai-brief）
- [ ] 内容解析与结构化
- [ ] 播报稿生成
- [ ] TTS 引擎选型（Qwen3 TTS vs. Doubao Seed TTS 2.0）
- [ ] TTS 音频合成
- [ ] 自动化定时任务
- [ ] RSS / 播客分发

## 许可证

本项目代码基于 [Apache License 2.0](LICENSE) 开源。新闻与论文内容版权归各自来源所有。

---
<br/>

# AI Briefcast (English)

> Your daily AI news, turned into a podcast you can listen to.

[简体中文](#ai-briefcast-) | **English**

## Overview

**AI Briefcast** automatically fetches daily AI news and research-paper briefs, rewrites them into natural, read-aloud-friendly scripts, and generates audio via text-to-speech (TTS) — so you can *listen* through the most important AI developments in just a few minutes each day.

## Sources

Content is drawn from two high-quality, primary-source-first, no-hype Chinese AI briefings:

| Source | Description | Link |
| --- | --- | --- |
| **AI Digest** | Daily curated AI industry news — primary English sources presented faithfully, no hype, no exaggeration, no sponsored content. | <https://ai-digest.liziran.com/zh/> |
| **AI Brief** | Daily curated arXiv paper summaries for founders / PMs / developers; every entry links to the original paper for verification. | <https://ai-brief.liziran.com/zh/> |

> Note: All content is copyright of its original authors. This project is for aggregation and broadcast purposes only — please respect the terms of use of the source sites.

## Goals

- **Daily auto-updates**: scheduled fetching of the latest news and paper briefs.
- **Script generation**: clean up and rewrite source material into natural, conversational, read-aloud scripts.
- **Speech synthesis**: produce a daily audio broadcast via TTS.
- **Multiple distribution channels** (planned): RSS podcast feed, audio files, transcripts.

## Pipeline (planned)

```
 fetch  →  clean / dedupe  →  script  →  TTS synthesize  →  publish / subscribe
```

## Tech Choices

- **TTS engine (under evaluation)** — choosing between:
  - [Qwen3 TTS](https://github.com/QwenLM)
  - [Doubao Seed TTS 2.0](https://www.volcengine.com/) (ByteDance / Volcengine)
  - Evaluation criteria: Chinese naturalness, voice variety, pricing, concurrency & latency, long-text stability.

## Status

🚧 **Early development.** The repo is at an initialization stage; this README describes goals and plans — features are not yet implemented.

## Roadmap

- [ ] Source fetching (ai-digest / ai-brief)
- [ ] Content parsing & structuring
- [ ] Broadcast script generation
- [ ] TTS engine selection (Qwen3 TTS vs. Doubao Seed TTS 2.0)
- [ ] TTS audio synthesis
- [ ] Scheduled automation
- [ ] RSS / podcast distribution

## License

The project code is open-sourced under the [Apache License 2.0](LICENSE). News and paper content remains the copyright of its respective sources.
