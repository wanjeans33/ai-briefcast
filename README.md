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

## 快速开始

**职责分工**：抓取与解析用 Python（`requests` + `BeautifulSoup`），把新闻**改写成播报稿**交给 LLM（OpenAI 兼容接口，可接 Qwen / DeepSeek / 豆包 / OpenAI 等）。

```bash
pip install -r requirements.txt

# 1) 配置 LLM（OpenAI 兼容接口，以 Qwen/DashScope 为例）
export LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export LLM_API_KEY="sk-..."
export LLM_MODEL="qwen-plus"

# 2) 抓取「今天」最新一期，用 LLM 生成简洁版 + 完整版到 samples/
python scripts/generate_broadcast.py

# 也可指定日期 / 只生成某个版本
python scripts/generate_broadcast.py --date 2026-06-02 --modes concise

# 只抓取+解析、导出原始素材（不调用 LLM，便于调试或离线查看）
python scripts/generate_broadcast.py --dump-raw
```

`scripts/generate_broadcast.py` 的流程：

1. 从两个来源首页定位当日新闻**详情子页面**，解析出干净的原始素材（头条全文 / 快讯 / 论文 / 观察）；
2. 把原始素材交给 LLM，按提示词改写成自然、口语化、TTS 友好的播报稿（数字/日期口语化、保留英文术语、加开场与收尾）。

输出：

- `samples/source-<日期>.md` —— `--dump-raw` 导出的原始素材（LLM 的输入）。
- `samples/broadcast-<日期>-concise.md` —— **简洁版**：约 3 分钟，覆盖头条与论文要点。
- `samples/broadcast-<日期>-full.md` —— **完整版**：头条全文 + 快讯 + 论文逐篇 + 延伸阅读 + 今日观察。

> LLM 配置走环境变量：`LLM_BASE_URL`、`LLM_API_KEY`（缺省回退 `OPENAI_API_KEY`）、`LLM_MODEL`。

## 每日自动化（固定流程）

`scripts/run_daily.py` 把整条链路**固定成一条命令**，可由定时任务每天自动跑：

```
抓取/解析(Python) → pi agent + DeepSeek 改写 → 豆包 TTS 合成 MP3
```

**1. 准备凭据**：复制 `.env.example` 为 `.env`，填入：

```dotenv
DEEPSEEK_API_KEY=sk-...                 # pi 的 DeepSeek provider
VOLC_APP_ID=... / VOLC_API_KEY=... / VOLC_SPEAKER=S_...   # 豆包 TTS
```

**2. 安装 pi 并注册 DeepSeek provider**（[pi.dev](https://pi.dev)，一次性）：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_pi.ps1
```

该脚本会 `npm i -g @earendil-works/pi-coding-agent`，并把 `automation/pi-extensions/deepseek-provider.mjs` 安装到 `~/.pi/extensions/`。pi 在 `automation/.pi/settings.json` 里默认选用 `deepseek` / `deepseek-chat`。

**3. 跑一次 / 排错**：

```bash
python scripts/run_daily.py --dry-run     # 只抓取并打印计划，不调用 pi/TTS
python scripts/run_daily.py               # 完整跑：默认 pi 改写 + 豆包 TTS
python scripts/run_daily.py --llm api      # 改用 OpenAI 兼容直连（用 DEEPSEEK_API_KEY）
python scripts/run_daily.py --tts none     # 只出文稿，不合成音频
python scripts/run_daily.py --tts-only "--audio-suffix=-myvoice"  # 不重写，仅对已有稿重合成音频
```

**音色**：豆包合成默认优先用 `VOLC_SPEAKER2`（你的克隆音色 / 声音复刻），没有才回退 `VOLC_SPEAKER`——所以每日播报就是你的声音。也可临时 `--doubao-speaker S_xxxx`。`--audio-suffix` 另存对比版（如 `-myvoice`），不覆盖原文件（以 `-` 开头的值需用 `=` 形式传入）。

产物：`samples/source-<日期>.md`、`samples/broadcast-<日期>-{concise,full}.md`、`audio_output/broadcast-<日期>-{concise,full}.mp3`（音频与 `logs/` 均已 gitignore）。前置条件缺失时会**优雅降级**：仅产出能产出的部分并在 `logs/run-<日期>.log` 记录原因。

**4. 注册每日定时任务**（Windows 计划任务）：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\register_daily_task.ps1 -Time 08:00
# 手动触发测试： schtasks /run /tn AI-Briefcast-Daily
# 删除：        powershell -File scripts\register_daily_task.ps1 -Remove
```

> Linux/macOS 可改用 cron 直接调度 `python scripts/run_daily.py`。

## 技术选型

- **TTS 引擎（评估中）**：在以下方案之间选择 ——
  - [Qwen3 TTS](https://github.com/QwenLM)（通义千问 TTS）
  - [Doubao Seed TTS 2.0](https://www.volcengine.com/)（豆包 / 火山引擎）
  - 评估维度：中文自然度、音色多样性、价格、并发与延迟、长文本稳定性。

## 项目状态

🚧 **早期开发中。** 抓取 → 改写 → TTS → 定时任务的端到端流程已固定（见 `scripts/run_daily.py`），分发仍在建设中。

## 路线图

- [x] 来源抓取（ai-digest / ai-brief 详情子页面）
- [x] 内容解析与结构化
- [x] LLM 改写生成播报稿（pi agent + DeepSeek；亦支持 OpenAI 兼容直连）
- [x] TTS 音频合成（豆包 Seed TTS 2.0 / Qwen3 TTS 两套方案）
- [x] 端到端编排 + 每日定时任务（`run_daily.py` + 计划任务）
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

## Quick Start

**Separation of concerns**: fetching & parsing use Python (`requests` + `BeautifulSoup`); rewriting raw news into broadcast scripts is delegated to an **LLM** via an OpenAI-compatible API (works with Qwen / DeepSeek / Doubao / OpenAI, etc.).

```bash
pip install -r requirements.txt

# 1) Configure the LLM (OpenAI-compatible endpoint; Qwen/DashScope shown)
export LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export LLM_API_KEY="sk-..."
export LLM_MODEL="qwen-plus"

# 2) Fetch today's latest issue and let the LLM generate concise + full scripts
python scripts/generate_broadcast.py

# Target a date / only one version
python scripts/generate_broadcast.py --date 2026-06-02 --modes concise

# Fetch + parse only, dump the raw material (no LLM call)
python scripts/generate_broadcast.py --dump-raw
```

How `scripts/generate_broadcast.py` works:

1. Locate the day's **article detail pages** from each source's homepage and parse them into clean raw material (full stories / quick briefs / papers / observation).
2. Hand the raw material to the LLM, which rewrites it into natural, conversational, TTS-friendly scripts (spoken-form numbers/dates, English tech terms preserved, intro & outro added).

Outputs:

- `samples/source-<date>.md` — raw material from `--dump-raw` (the LLM input).
- `samples/broadcast-<date>-concise.md` — **concise** (~3 min): headlines + paper highlights.
- `samples/broadcast-<date>-full.md` — **full**: full stories + quick briefs + per-paper detail + further reading + daily observation.

> LLM config via env vars: `LLM_BASE_URL`, `LLM_API_KEY` (falls back to `OPENAI_API_KEY`), `LLM_MODEL`.

## Daily Automation (fixed pipeline)

`scripts/run_daily.py` wires the whole chain into **one command**, ready to be scheduled:

```
fetch/parse (Python) → rewrite (pi agent + DeepSeek) → TTS (Doubao) → MP3
```

**1. Credentials** — copy `.env.example` to `.env` and fill in `DEEPSEEK_API_KEY` (for pi's DeepSeek provider) and `VOLC_APP_ID` / `VOLC_API_KEY` / `VOLC_SPEAKER` (Doubao TTS).

**2. Install pi + DeepSeek provider** ([pi.dev](https://pi.dev), one-time):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup_pi.ps1
```

Installs `@earendil-works/pi-coding-agent` and the provider extension into `~/.pi/extensions/`; pi defaults to `deepseek` / `deepseek-chat` via `automation/.pi/settings.json`.

**3. Run / debug**:

```bash
python scripts/run_daily.py --dry-run    # fetch + print plan only
python scripts/run_daily.py              # full run: pi rewrite + Doubao TTS
python scripts/run_daily.py --llm api     # OpenAI-compatible direct (uses DEEPSEEK_API_KEY)
python scripts/run_daily.py --tts none    # scripts only, no audio
python scripts/run_daily.py --tts-only "--audio-suffix=-myvoice"  # re-synthesize existing scripts only
```

**Voice**: Doubao synthesis prefers `VOLC_SPEAKER2` (your cloned voice) and falls back to `VOLC_SPEAKER`, so the daily broadcast is in your own voice. Override per-run with `--doubao-speaker S_xxxx`. Use `--audio-suffix` (e.g. `-myvoice`) to save a comparison copy without overwriting (pass `-`-leading values with the `=` form).

Outputs: `samples/source-<date>.md`, `samples/broadcast-<date>-{concise,full}.md`, `audio_output/broadcast-<date>-{concise,full}.mp3` (audio and `logs/` are gitignored). Missing prerequisites degrade gracefully and are logged to `logs/run-<date>.log`.

**4. Schedule it** (Windows Task Scheduler):

```powershell
powershell -ExecutionPolicy Bypass -File scripts\register_daily_task.ps1 -Time 08:00
# test now: schtasks /run /tn AI-Briefcast-Daily
# remove:   powershell -File scripts\register_daily_task.ps1 -Remove
```

> On Linux/macOS, schedule `python scripts/run_daily.py` with cron instead.

## Pipeline

```
 fetch  →  clean / dedupe  →  script  →  TTS synthesize  →  publish / subscribe
```

## Tech Choices

- **TTS engine (under evaluation)** — choosing between:
  - [Qwen3 TTS](https://github.com/QwenLM)
  - [Doubao Seed TTS 2.0](https://www.volcengine.com/) (ByteDance / Volcengine)
  - Evaluation criteria: Chinese naturalness, voice variety, pricing, concurrency & latency, long-text stability.

## Status

🚧 **Early development.** The fetch → rewrite → TTS → schedule pipeline is wired end to end (see `scripts/run_daily.py`); distribution is still being built.

## Roadmap

- [x] Source fetching (ai-digest / ai-brief detail pages)
- [x] Content parsing & structuring
- [x] LLM-based script rewriting (pi agent + DeepSeek; OpenAI-compatible direct also supported)
- [x] TTS audio synthesis (Doubao Seed TTS 2.0 / Qwen3 TTS)
- [x] End-to-end orchestration + daily scheduled task (`run_daily.py` + Task Scheduler)
- [ ] RSS / podcast distribution

## License

The project code is open-sourced under the [Apache License 2.0](LICENSE). News and paper content remains the copyright of its respective sources.
