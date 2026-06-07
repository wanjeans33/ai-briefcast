---
name: ai-briefcast-daily
description: >
  在 ai-briefcast 仓库里生成"每日 AI 速览"的小红书成品：竖屏卡点视频（4K，带片头）+
  3:4 封面 + 标题/话题标签。覆盖抓取→改写(固定开场白)→分段豆包TTS(克隆音色)→
  新闻卡+联网查证的「信息补充」解释卡(按新闻同色分组)→逐卡精确卡点+1:1片头→make_cover 封面。
  只要用户提到"做今天/某天的（AI）播报/视频/小红书/封面/卡片/briefcast/速览"、要为某条音频配视频、
  或要补充卡/封面/标题/tag，就使用本技能；即使没说"skill"也要主动用。
---

# AI Briefcast 每日小红书成品流水线

把 ai-briefcast.liziran 两个来源的当天新闻，做成可直接发小红书的一套成品：
**4K 竖屏卡点视频（带猫片头）+ 3:4 封面 + 标题 + 话题标签**。

仓库根：`E:\Github_project\ai-briefcast`。所有命令在仓库根执行，加 `PYTHONUTF8=1 PYTHONIOENCODING=utf-8`（Windows 中文输出）。

## 关键约定（记住这些，少踩坑）

- **声音**：用户自己的豆包克隆音色 `VOLC_SPEAKER2=S_HHgApOH42`（不是 liziran 的）。
- **开场白固定**：`generate_broadcast.fixed_intro()` 已内置"大家好，这里是柿子树下的猫wanjeans，
  三分钟带你了解AI圈的新鲜事。今天是…"，LLM 不再自己写开场白，只换日期。
- **默认只做 concise**；常用"仅 3 条要闻、去掉论文"的版本。
- **音频/文稿是基线，不要为了加卡片去改它**：补充卡是静默视觉卡，把某条新闻的音频时长
  切给"新闻卡+几张补充卡"，不重新配音。
- **视频默认带 1:1 片头** `片头/小猫片头_1x1_4s.mp4`（模糊铺底+居中适配竖屏）。
- **ffmpeg 绝对路径**写在 `make_xhs_video_html.FFMPEG`；输出 4K = `OUT_W,OUT_H=2160,3840`。
- **每一步产出后，先让用户审，再继续**（用户多次强调要审 MD、审卡片）。

## 前置检查

- `.env`（仓库根）含：`VOLC_APP_ID/VOLC_API_KEY/VOLC_SPEAKER2/VOLC_RESOURCE_ID`，
  改写用 `DEEPSEEK_API_KEY`（pi 后端）。注意 DeepSeek key 易手滑多打字符，401 时先核对尾号。
- ffmpeg：`make_xhs_video_html.FFMPEG` 指向的 exe 存在。
- Playwright Chromium 已装（`playwright install chromium`）。
- 改写后端：`--llm pi`（pi agent + DeepSeek）或 `--llm api`（OpenAI 兼容直连 DeepSeek）。
  pi 在 Windows 要走 `node dist/cli.js`（已在 `_pi_command()` 处理）。

## 流水线（按顺序，逐步暂停给用户审）

### 1) 生成文稿（concise，固定开场白）
```
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python scripts/generate_broadcast.py \
  --date YYYY-MM-DD --modes concise --llm pi
```
- 论文简报常比资讯晚更新；若当天没有，脚本会回退到前一天的论文。
- 要"仅 3 条要闻、不要论文"：复制生成的 `samples/broadcast-<date>-concise.md`，删掉"论文方面"那段，
  另存为 `broadcast-<date>-concise-3news.md`（开场白+3 条头条+收尾 = 5 段）。
- **停下让用户审稿**。用户常会改开场白、删冗余过渡句。

### 2) 分段豆包 TTS（克隆音色）→ 拿到每段真实时长
逐段合成保证精确卡点；失败自动重试 3 次。用 `run_daily.synth_segmented()`：
```python
import run_daily as rd, generate_broadcast as gb
rd.load_dotenv(rd.REPO_ROOT)
spk = os.getenv("VOLC_SPEAKER2")
segs = gb.split_segments(rd.strip_header(md_text))   # 按空行切段
durs = rd.synth_segmented(segs, mp3_path, log, spk)  # 生成 segs/*.mp3 + 拼接 mp3，返回每段秒数
```
分段产物在 `audio_output/segs/`，整段在 `audio_output/broadcast-<date>-concise*.mp3`。
**音频一旦满意就别再动**——后面加卡片复用这些 seg 时长，不重配音。

### 3) 卡片：新闻卡 + 联网查证的「信息补充」卡（按新闻同色分组）
这是质量核心，**不能只凭记忆**。对每条新闻：
1. 找出普通读者看不懂的实体/术语（公司、产品、概念、事件、金融词等）。
2. **逐个 WebSearch 查证**（公司是什么、事件经过、概念怎么运作、最新数字/时间）。
3. 汇总成"高中生也能懂"的口语解释，写进补充卡 `body`（≤~60 字，`**关键数字/词**` 高亮）。

卡片字段、配色分组、卡点权重、可直接改用的驱动脚本：见
`references/card-design.md`（**做卡片前先读它**）。

分组示例（用户认可的密度）：
- 每条新闻 = 1 张新闻卡 + 2~3 张补充卡，同一条用同一配色（`grad`）。
- 组内时长权重：新闻卡 1.5、每张补充卡 1.0，把该段音频时长按权重切分。

**渲染后停下让用户审卡片**（抽查封面 + 每组一张 + CTA，确认无乱码/溢出/重叠）。

### 4) 合成 4K 卡点视频 + 1:1 片头
`make_xhs_video_html.build_xhs_video(cards, audio, out, date, seg_durations=durs, intro_path=intro)`：
- `seg_durations` 传"每张卡的可见时长"（已按组切好），实现逐卡卡点；
- `intro_path` 给 `片头/小猫片头_1x1_4s.mp4`，自动模糊铺底适配 + 拼到最前、保留片头音乐。
- 输出 `audio_output/xhs-<date>-concise*.mp4`，4K 2160×3840。
- 校验：用 ffprobe 确认 `width=2160 height=3840`，视频时长 ≈ 片头(4s)+音频。

> 全自动（无补充卡、每条新闻 1 张卡）可直接：
> `python scripts/run_daily.py --date <date> --modes concise --video`
> （已默认带片头；`--no-intro` 关闭）。补充卡版目前用 `references/card-design.md` 的驱动脚本手工组卡。

### 5) 封面（3:4）
```
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python scripts/make_cover.py assets/cover/cover-<date>.png
```
编辑 `make_cover.py` 顶部的 `BRAND/KICKER/BIG/ROWS/DATE` 改当天内容（钩子词放最前、关键词用 `**…**`）。
输出 3:4 = 1080×1440（2x → 2160×2880）。封面可单独上传为视频自定义封面。

### 6) 标题 + 话题标签
**标题**（≤20 字，前 8 字定生死，数字+情绪+悬念取二，配 1~2 emoji，口语像爆料）。给 2~3 个选项让用户挑。
**标签金字塔（8~10 个）**：
- 大流量泛标签 ×2：`#人工智能 #AI`
- 领域 ×3：`#AI日报 #每日AI #AI资讯`
- 当天热点具体词 ×3：按内容换（如 `#苹果 #SpaceX #OpenAI` / `#大模型 #ChatGPT #Claude`）
- 品牌 IP ×1：`#柿子树下的猫`
- 场景人群 ×1：`#通勤干货`
固定品牌/领域/场景标签，只换"热点具体词"，利于账号标签沉淀。

## 产物清单（一天）
- `samples/source-<date>.md`、`samples/broadcast-<date>-concise*.md`
- `audio_output/broadcast-<date>-concise*.mp3`（克隆音色）
- `audio_output/xhs-<date>-concise*.mp4`（4K 卡点 + 片头）
- `assets/cover/cover-<date>.png`（3:4 封面）
- 标题 + 标签（发给用户）

## 排错速记
- DeepSeek 401：先核对 `DEEPSEEK_API_KEY` 尾号（易多打字符）；pi 与 api 后端都受同一 key 影响。
- 豆包 `NO AUDIO RECEIVED` / 403：偶发或限流，`synth_segmented` 已自动重试；仍失败就等额度恢复。
- 末字被吞：`doubao_tts_ws.pad_tail()` 已在文本尾部补停顿，别移除。
- 卡片乱码/溢出：正文太长就精简 `body`；中文按字断行在 `_wrap()`。
- 媒体文件（mp3/mp4/片头/卡片 png）按 `.gitignore` 不入库，留本地。
