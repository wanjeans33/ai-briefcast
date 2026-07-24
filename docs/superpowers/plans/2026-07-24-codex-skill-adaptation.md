# Codex Skill Adaptation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Preserve all Claude Code skills unchanged while adding four validated, Codex-native Briefcast project skills under `.agents/skills`.

**Architecture:** Maintain independent Claude and Codex adapters. Build each Codex skill as a standalone folder with a concise `SKILL.md`, required resources, and `agents/openai.yaml`; replace Claude-only tool references with Codex skill and tool contracts while preserving the Briefcast business rules.

**Tech Stack:** Markdown Agent Skills, YAML, Codex project skill discovery, Python `quick_validate.py`, `rg`, Git.

## Global Constraints

- Do not edit, delete, move, or symlink anything under `.claude/skills`.
- Do not install or publish a global Codex skill.
- Do not push commits or publish content to external platforms.
- Use only `name` and `description` in `SKILL.md` YAML frontmatter.
- Quote every string in `agents/openai.yaml`.
- Every `interface.default_prompt` must explicitly mention its `$skill-name`.
- Route bitmap generation through the built-in `imagegen` skill.
- Stop creator-platform automation before the final publish action.
- Use `apply_patch` for authored file changes; exact resource directory copies may use a mechanical copy command.
- Validate and commit one skill before starting the next.

---

### Task 1: Add the Codex AI News Podcast Skill

**Files:**

- Create: `.agents/skills/ai-news-podcast/SKILL.md`
- Create: `.agents/skills/ai-news-podcast/agents/openai.yaml`
- Create: `.agents/skills/ai-news-podcast/references/evidence-levels.md`
- Create: `.agents/skills/ai-news-podcast/references/paper-review-guide.md`
- Create: `.agents/skills/ai-news-podcast/references/podcast-structure.md`
- Create: `.agents/skills/ai-news-podcast/references/quality-checklist.md`
- Create: `.agents/skills/ai-news-podcast/references/source-verification.md`
- Create: `.agents/skills/ai-news-podcast/references/style-profile.md`
- Create: `.agents/skills/ai-news-podcast/examples/paper-update-example.md`
- Create: `.agents/skills/ai-news-podcast/examples/rewrite-example.md`
- Create: `.agents/skills/ai-news-podcast/examples/weekly-brief-example.md`
- Create: `.agents/skills/ai-news-podcast/evals/sample-scorecard.csv`
- Create: `.agents/skills/ai-news-podcast/evals/scoring-rubric.md`
- Create: `.agents/skills/ai-news-podcast/evals/test-prompts.md`

**Interfaces:**

- Consumes: AI-news source material, links, papers, or draft scripts.
- Produces: A fact-checked Chinese spoken-news script using the E1-E5 evidence model.

- [ ] **Step 1: Run a baseline application scenario without the Codex skill**

Dispatch a fresh validation agent with no intended solution:

```text
Prepare a concise plan for turning a vendor announcement and an arXiv
preprint into a Chinese AI podcast segment. Explain how you would distinguish
claims, evidence status, limitations, and independent verification. Do not
change files.
```

Record whether the response independently defines the repository's E1-E5
scheme, reads the project quality gate, and distinguishes vendor claims from
independent evidence. The expected baseline failure is omission of at least one
project-specific requirement.

- [ ] **Step 2: Create the adapted `SKILL.md`**

Use `.claude/skills/ai-news-podcast/SKILL.md` as the business-content source.
Replace its frontmatter with exactly:

```yaml
---
name: ai-news-podcast
description: >-
  Use when writing, rewriting, reviewing, or fact-checking Chinese spoken
  scripts about AI news, model releases, company announcements, research
  papers, preprints, or weekly AI roundups.
---
```

Keep the E1-E5 model, task modes, workflow, output structure, hard constraints,
and prohibited claims. Add this Codex source-verification contract immediately
before the workflow:

```markdown
## Codex 工具约定

- 读取仓库文件时使用当前工作区路径，并按需加载本技能直接链接的 references。
- 需要外部核验时使用 Codex 的联网工具；优先打开公司、作者、论文、会议或监管机构的一手页面。
- 搜索摘要只用于定位来源，不作为最终事实依据。
- 若联网工具不可用，明确标注未核验项，不把待核实内容写成确定事实。
```

Remove Claude-only `argument-hint` and `allowed-tools` fields. Do not copy
`README.md` or `CHANGELOG.md`.

- [ ] **Step 3: Copy the runtime and evaluation resources exactly**

Run:

```bash
mkdir -p .agents/skills/ai-news-podcast
cp -R .claude/skills/ai-news-podcast/references .agents/skills/ai-news-podcast/
cp -R .claude/skills/ai-news-podcast/examples .agents/skills/ai-news-podcast/
cp -R .claude/skills/ai-news-podcast/evals .agents/skills/ai-news-podcast/
```

Expected: the three resource directories exist, while `README.md` and
`CHANGELOG.md` do not exist in the Codex skill folder.

- [ ] **Step 4: Add Codex UI metadata**

Create `.agents/skills/ai-news-podcast/agents/openai.yaml`:

```yaml
interface:
  display_name: "AI News Podcast"
  short_description: "核验 AI 新闻与论文并撰写准确克制的中文口播稿"
  default_prompt: "Use $ai-news-podcast to fact-check these AI stories and turn them into a concise Chinese spoken-news script."
```

- [ ] **Step 5: Validate the skill structure**

Prepare the validator dependency outside the repository:

```bash
python3 -m pip install --target /tmp/ai-briefcast-skill-validator PyYAML==6.0.2
```

Run:

```bash
PYTHONPATH=/tmp/ai-briefcast-skill-validator python3 -B /Users/wanjeans/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/ai-news-podcast
```

Expected: `Skill is valid!`

- [ ] **Step 6: Forward-test the adapted skill**

Dispatch a fresh agent:

```text
Use $ai-news-podcast to outline a Chinese spoken segment for a fictional
vendor-announced model benchmark plus an unreviewed paper. Do not browse or
write files; state the evidence labels and the caveats you would require.
```

Expected: it loads the skill, uses E1 for the vendor claim and E2 for the
preprint, does not treat either as independently reproduced, and mentions the
quality gate.

- [ ] **Step 7: Commit the podcast skill**

```bash
git add .agents/skills/ai-news-podcast
git commit -m "feat(skills): add Codex AI news podcast workflow"
```

---

### Task 2: Add the Codex-Native Briefcast Image Skill

**Files:**

- Create: `.agents/skills/ai-briefcast-imagegen/SKILL.md`
- Create: `.agents/skills/ai-briefcast-imagegen/agents/openai.yaml`

**Interfaces:**

- Consumes: A Briefcast visual brief plus optional local reference images.
- Produces: Inspected raster assets in the requested `output/<date>/` location.

- [ ] **Step 1: Run the Claude-side baseline scenario**

Dispatch a fresh agent:

```text
Read .claude/skills/codex-imagegen/SKILL.md and explain the first concrete
actions you would take in this macOS Codex desktop workspace to generate a
Briefcast watercolor illustration. Do not perform the actions.
```

Expected baseline failure: the response inherits at least one nested
`codex exec`, Windows executable, PowerShell, or CLI-version instruction that
is unnecessary inside Codex desktop.

- [ ] **Step 2: Create the project-specific ImageGen skill**

Create `.agents/skills/ai-briefcast-imagegen/SKILL.md` with this complete
structure and contract:

```markdown
---
name: ai-briefcast-imagegen
description: >-
  Use when generating or editing raster illustrations, seals, editorial
  collage assets, transparent stickers, or 3:4 and 4:3 covers for the
  ai-briefcast production workflow.
---

# AI Briefcast Image Generation

Create Briefcast bitmap assets through the built-in `imagegen` skill.

**REQUIRED SUB-SKILL:** Use imagegen for every generation or edit. Do not run a
nested Codex CLI, install Codex, or substitute SVG, canvas, matplotlib, or
programmatic drawing.

## Workflow

1. Resolve the repository root and exact output path under `output/<date>/`.
2. Read the relevant visual rules from `ai-briefcast-mg` when producing MG
   assets.
3. Inspect every local reference image before using it.
4. Build a prompt that specifies subject, medium, composition, palette,
   aspect ratio, allowed text, and prohibited elements.
5. Generate or edit through the built-in image tool.
6. Inspect the saved image at original detail.
7. Verify composition, text, extra marks, transparency, and output location.
8. Regenerate when a required visual or character is wrong.

## Asset Contracts

| Asset | Required treatment |
| --- | --- |
| Ink illustration | New-Chinese ink wash, muted paper, ink brown, persimmon orange, no text |
| Seal asset | Square composition, one recognizable geometric mark, no extra letters |
| Collage still | 9:16, central subject in middle 70%, no typography, separable paper groups |
| Sticker | Transparent background, one isolated object, crisp cut edge, no shadow outside the cutout |
| 3:4 cover | Strong single focal subject, safe title area, only explicitly supplied text |
| 4:3 cover | Landscape hierarchy, short headline area, no extra text |

## Prompt Requirements

- Treat generated text as high risk. List every allowed string exactly and ban
  all other letters, numerals, logos, signatures, and watermarks.
- For no-text assets, explicitly prohibit typography and abstract glyphs.
- Use reference images only to preserve the requested subject or style.
- Do not claim an exact output resolution beyond the image tool's supported
  sizes; verify the actual saved dimensions.

## Delivery

- Save final assets directly in the requested Briefcast output directory.
- Use descriptive stable names such as `topic-ink.png`,
  `topic-seal.png`, `topic-sticker.png`, or `cover-3x4.png`.
- Show the inspected image to the user and report its absolute path.
```

- [ ] **Step 3: Add Codex UI metadata**

Create `.agents/skills/ai-briefcast-imagegen/agents/openai.yaml`:

```yaml
interface:
  display_name: "AI Briefcast ImageGen"
  short_description: "生成 Briefcast 水墨插图、拼贴素材和双比例封面"
  default_prompt: "Use $ai-briefcast-imagegen to create and inspect a production-ready visual asset for this Briefcast episode."
```

- [ ] **Step 4: Validate and scan the skill**

Run:

```bash
PYTHONPATH=/tmp/ai-briefcast-skill-validator python3 -B /Users/wanjeans/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/ai-briefcast-imagegen
rg -n 'codex exec|PowerShell|codex\\.exe|npm install -g|Start-Job' .agents/skills/ai-briefcast-imagegen
```

Expected: validator passes and `rg` returns no matches.

- [ ] **Step 5: Forward-test routing without generating an image**

Dispatch a fresh agent:

```text
Use $ai-briefcast-imagegen to describe the exact tool route and validation
steps for a text-free 9:16 ink-wash Briefcast illustration. Do not generate the
image.
```

Expected: it selects the built-in `imagegen` skill, includes inspection, and
does not invoke a nested CLI.

- [ ] **Step 6: Commit the image skill**

```bash
git add .agents/skills/ai-briefcast-imagegen
git commit -m "feat(skills): add native Briefcast ImageGen workflow"
```

---

### Task 3: Refresh the Codex Daily Briefcast Skill

**Files:**

- Modify: `.agents/skills/ai-briefcast-daily/SKILL.md`
- Create: `.agents/skills/ai-briefcast-daily/agents/openai.yaml`
- Verify unchanged: `.agents/skills/ai-briefcast-daily/references/card-design.md`

**Interfaces:**

- Consumes: A requested date range, source material, or an existing episode
  artifact.
- Produces: Script, audio, timed cards, subtitled video, covers, caption,
  chapters, and publishing data with three user approval checkpoints.

- [ ] **Step 1: Capture the stale-skill baseline**

Dispatch a fresh agent:

```text
Read .agents/skills/ai-briefcast-daily/SKILL.md. In this Codex desktop
workspace, list the exact first tools and paths it instructs you to use for
selection, source verification, repository access, and publishing. Do not
perform the workflow.
```

Expected baseline failures include the stale Windows root, Claude
`AskUserQuestion`, missing current `episode.yaml` behavior, or missing Codex
browser publishing instructions.

- [ ] **Step 2: Rebase the Codex skill on current business rules**

Use `.claude/skills/ai-briefcast-daily/SKILL.md` as the complete business-rule
baseline. Preserve its current editorial rules and pipeline details, then apply
these exact Codex adaptations:

```text
E:\Github_project\ai-briefcast
  -> repository root from `git rev-parse --show-toplevel`; fall back to the
     active workspace only when Git discovery fails

WebSearch + WebFetch / WebFetch
  -> Codex联网工具；搜索只定位来源，必须打开并核对一手页面

grep output/
  -> rg -n "关键词" output/

AskUserQuestion
  -> Codex 对话审核点；一次展示一组候选并请用户回复选择，结构化输入工具可用时优先使用

Claude 直接出全套
  -> Codex 直接出全套

Claude-in-Chrome
  -> browser:control-in-app-browser

list_connected_browsers
  -> 按 browser 技能检查当前 Codex 应用内浏览器会话
```

Replace the repository paragraph with:

```markdown
仓库根目录优先用 `git rev-parse --show-toplevel` 动态取得；若当前目录不在 Git
仓库中，再使用 Codex 当前工作区。所有命令在仓库根执行。不要硬编码 Windows
盘符或用户目录。
```

Replace every structured-selection instruction with:

```markdown
**Codex 审核点**：选题、审稿、终审卡片文案分别停一次。一次展示一组候选并请
用户回复选择；结构化输入工具在当前模式可用时优先使用。不要依赖
Claude Code 专属交互工具。
```

Replace the publishing section integration text with:

```markdown
投稿表单使用 `browser:control-in-app-browser` 操作已登录的 Codex 应用内浏览器。
先读取 `publish.json`，上传视频和对应比例封面，填标题、正文、标签、章节和
可见性。遇到登录或授权页面时停下让用户处理。始终停在最终发布按钮前，只有
用户明确批准该次发布动作后才能继续。
```

- [ ] **Step 3: Set Codex-compatible frontmatter**

Use exactly:

```yaml
---
name: ai-briefcast-daily
description: >-
  Use when creating or updating an ai-briefcast daily AI roundup, Chinese
  spoken script, topic selection, timed vertical video, subtitles, cards,
  explanatory cards, 3:4 or 4:3 cover, caption, tags, chapters, publishing
  data, or a video synchronized to existing episode audio.
---
```

- [ ] **Step 4: Add Codex UI metadata**

Create `.agents/skills/ai-briefcast-daily/agents/openai.yaml`:

```yaml
interface:
  display_name: "AI Briefcast Daily"
  short_description: "制作每日 AI 速览视频、字幕、双比例封面和发布物料"
  default_prompt: "Use $ai-briefcast-daily to produce today's verified AI roundup and stop at each required review checkpoint."
```

- [ ] **Step 5: Validate and scan the refreshed skill**

Run:

```bash
PYTHONPATH=/tmp/ai-briefcast-skill-validator python3 -B /Users/wanjeans/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/ai-briefcast-daily
rg -n 'AskUserQuestion|WebSearch|WebFetch|Claude-in-Chrome|list_connected_browsers|E:\\\\Github_project' .agents/skills/ai-briefcast-daily
cmp .claude/skills/ai-briefcast-daily/references/card-design.md .agents/skills/ai-briefcast-daily/references/card-design.md
```

Expected: validator passes, `rg` returns no matches, and `cmp` exits `0`.

- [ ] **Step 6: Forward-test the daily workflow**

Dispatch a fresh agent:

```text
Use $ai-briefcast-daily to describe the first five actions for producing
today's episode in this repository. Do not browse, generate media, or edit
files. Name the repository-root strategy, source-verification rule, approval
checkpoints, primary episode driver, and publish safety boundary.
```

Expected: dynamic root, primary-source verification, three checkpoints,
`episode.yaml` plus `make_episode.py`, and stopping before final publish.

- [ ] **Step 7: Commit the refreshed daily skill**

```bash
git add .agents/skills/ai-briefcast-daily
git commit -m "feat(skills): refresh Codex daily Briefcast workflow"
```

---

### Task 4: Add the Codex ChatCut MG Skill

**Files:**

- Create: `.agents/skills/ai-briefcast-mg/SKILL.md`
- Create: `.agents/skills/ai-briefcast-mg/agents/openai.yaml`

**Interfaces:**

- Consumes: An approved daily Briefcast script and audio plan.
- Produces: An editable ChatCut MG timeline with synchronized subtitles and
  verified frames.

- [ ] **Step 1: Run the Claude-side MG baseline scenario**

Dispatch a fresh agent:

```text
Read .claude/skills/ai-briefcast-mg/SKILL.md and list the exact skills, tool
discovery names, image route, browser route, and background execution method
you would use in this Codex desktop workspace. Do not perform any action.
```

Expected baseline failures include Claude plugin skill names,
`mcp__plugin_chatcut_chatcut__*`, `ToolSearch`, Claude image bridging, or
PowerShell background jobs.

- [ ] **Step 2: Create the adapted MG skill**

Use `.claude/skills/ai-briefcast-mg/SKILL.md` as the complete visual and
timeline baseline. Preserve the TTS, eight-card design, collage variant, canvas
restrictions, item field names, Whisper alignment, frame QA, and handoff rules.
Apply these exact replacements:

```text
AskUserQuestion
  -> ai-briefcast-daily 的 Codex 审核点

mcp__plugin_chatcut_chatcut__*；未连则 ToolSearch 等待
  -> 先使用 chatcut:chatcut-skill；需要延迟工具时通过 Codex tool_search
     查找 ChatCut 工具，找不到则报告缺失能力

chatcut-plugin-basics-claude → create-motion-graphics
  -> chatcut:chatcut-skill，并按该技能路由加载所需 ChatCut 参考

codex-imagegen
  -> ai-briefcast-imagegen（实际生成或编辑时继续使用内置 imagegen）

Bash 后台并行跑 / PowerShell Start-Job
  -> 使用 Codex 原生图片工具调用；多张独立素材可并行生成，逐张检查后再上传

browserHandoff / navigation denied
  -> 按 chatcut:chatcut-skill 和 browser:control-in-app-browser 处理编辑器交接与授权
```

Add this dependency contract after the introduction:

```markdown
## Codex 依赖

- **REQUIRED SUB-SKILL:** Use ai-briefcast-daily for selection, writing, and
  approval checkpoints.
- **REQUIRED SUB-SKILL:** Use chatcut:chatcut-skill for ChatCut project,
  timeline, preview, and export operations.
- **REQUIRED SUB-SKILL:** Use ai-briefcast-imagegen for Briefcast bitmap
  assets; it routes generation and editing through the built-in imagegen skill.
- Use browser:control-in-app-browser when an authenticated editor handoff or
  visible browser interaction is required.
- Search for deferred ChatCut tools through Codex tool search. If unavailable,
  report the missing capability instead of inventing a tool name.
```

- [ ] **Step 3: Set Codex-compatible frontmatter**

Use exactly:

```yaml
---
name: ai-briefcast-mg
description: >-
  Use when turning an approved ai-briefcast episode into an editable ChatCut
  vertical MG animation, ink-wash eight-card video, editorial collage or
  Vox-style variant, synchronized subtitle timeline, or ChatCut cover workflow.
---
```

- [ ] **Step 4: Add Codex UI metadata**

Create `.agents/skills/ai-briefcast-mg/agents/openai.yaml`:

```yaml
interface:
  display_name: "AI Briefcast MG"
  short_description: "用 ChatCut 制作水墨或编辑拼贴风的竖屏 MG 动画"
  default_prompt: "Use $ai-briefcast-mg to turn this approved Briefcast script into a verified editable ChatCut MG timeline."
```

- [ ] **Step 5: Validate and scan the MG skill**

Run:

```bash
PYTHONPATH=/tmp/ai-briefcast-skill-validator python3 -B /Users/wanjeans/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/ai-briefcast-mg
rg -n 'AskUserQuestion|mcp__plugin_chatcut_chatcut__|ToolSearch|chatcut-plugin-basics-claude|codex-imagegen|Start-Job|Claude-in-Chrome' .agents/skills/ai-briefcast-mg
```

Expected: validator passes and `rg` returns no matches.

- [ ] **Step 6: Forward-test the MG routing**

Dispatch a fresh agent:

```text
Use $ai-briefcast-mg to describe the tool and skill sequence for converting an
approved script into an editable ink-wash ChatCut timeline. Do not call tools
or edit files. Include image generation, browser handoff, alignment, and frame
verification.
```

Expected: daily skill, ChatCut skill, Briefcast ImageGen plus built-in
ImageGen, browser skill, Whisper alignment, and frame inspection all appear.

- [ ] **Step 7: Commit the MG skill**

```bash
git add .agents/skills/ai-briefcast-mg
git commit -m "feat(skills): add Codex ChatCut MG workflow"
```

---

### Task 5: Run Cross-Skill Integration Validation

**Files:**

- Verify: `.agents/skills/ai-briefcast-daily/**`
- Verify: `.agents/skills/ai-news-podcast/**`
- Verify: `.agents/skills/ai-briefcast-mg/**`
- Verify: `.agents/skills/ai-briefcast-imagegen/**`
- Verify unchanged: `.claude/skills/**`

**Interfaces:**

- Consumes: The four independently validated Codex project skills.
- Produces: A clean repository state whose Codex skill graph resolves without
  Claude-only calls.

- [ ] **Step 1: Validate all four skill folders**

Run:

```bash
for skill in ai-briefcast-daily ai-news-podcast ai-briefcast-mg ai-briefcast-imagegen; do
  PYTHONPATH=/tmp/ai-briefcast-skill-validator python3 -B /Users/wanjeans/.codex/skills/.system/skill-creator/scripts/quick_validate.py ".agents/skills/$skill"
done
```

Expected: four `Skill is valid!` results.

- [ ] **Step 2: Scan the Codex tree for incompatible instructions**

Run:

```bash
rg -n 'AskUserQuestion|WebSearch|WebFetch|Claude-in-Chrome|list_connected_browsers|mcp__plugin_chatcut_chatcut__|ToolSearch|chatcut-plugin-basics-claude|codex exec|codex\\.exe|Start-Job|E:\\\\Github_project' .agents/skills
```

Expected: no matches.

- [ ] **Step 3: Verify skill metadata and resource links**

Run:

```bash
find .agents/skills -mindepth 2 -maxdepth 2 -name SKILL.md -print | sort
find .agents/skills -mindepth 3 -maxdepth 3 -path '*/agents/openai.yaml' -print | sort
test -f .agents/skills/ai-news-podcast/references/quality-checklist.md
test -f .agents/skills/ai-briefcast-daily/references/card-design.md
```

Expected: exactly four `SKILL.md` files, four `agents/openai.yaml` files, and
both `test` commands exit `0`.

- [ ] **Step 4: Prove the Claude tree is unchanged**

Run:

```bash
git diff e4aebb5 -- .claude/skills
```

Expected: no output.

- [ ] **Step 5: Run an integration forward-test**

Dispatch a fresh agent:

```text
In this repository, identify which project skills should handle these four
requests and why: write a verified AI podcast script; make today's Briefcast;
turn the approved episode into a ChatCut ink-wash MG video; generate a 3:4
Briefcast cover. Do not perform the work.
```

Expected mapping:

```text
verified podcast script -> ai-news-podcast
daily episode -> ai-briefcast-daily
ChatCut MG -> ai-briefcast-mg
Briefcast cover -> ai-briefcast-imagegen + built-in imagegen
```

- [ ] **Step 6: Run final repository verification**

Run:

```bash
git diff --check
git status --short --branch
git log -5 --oneline
```

Expected: no whitespace errors; only intentional commits are ahead of
`origin/main`; no untracked or unstaged implementation files remain.

- [ ] **Step 7: Commit any validation-only correction**

If integration validation required a correction, stage only the corrected
skill files and commit:

```bash
git add .agents/skills
git commit -m "fix(skills): complete Codex integration validation"
```

If no correction was needed, do not create an empty commit.
