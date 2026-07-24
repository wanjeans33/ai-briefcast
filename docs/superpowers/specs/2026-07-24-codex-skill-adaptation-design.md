# Codex Skill Adaptation Design

Date: 2026-07-24

## Goal

Keep the existing Claude Code skills under `.claude/skills` unchanged and add
Codex-native project skills under `.agents/skills`. The Codex copies must retain
the current Briefcast editorial and production knowledge while using Codex tool
names, project discovery conventions, and the current macOS workspace safely.

## Scope

Create or refresh four Codex project skills:

1. `ai-briefcast-daily`
2. `ai-news-podcast`
3. `ai-briefcast-mg`
4. `ai-briefcast-imagegen`

Copy only resources needed at runtime or for skill evaluation. Do not copy the
Claude-oriented README or changelog into Codex skill folders.

## Non-goals

- Do not edit, delete, move, or symlink anything under `.claude/skills`.
- Do not redesign the Briefcast editorial rules or production pipeline.
- Do not install or publish a global Codex skill.
- Do not push commits or publish content to external platforms.
- Do not preserve Claude-only tool syntax merely for textual fidelity.

## Architecture

`.claude/skills` and `.agents/skills` remain independent adapters for the same
project workflow. Claude remains the source of the latest business rules during
this migration, but the Codex versions are complete standalone skills rather
than symbolic links or thin wrappers.

Each Codex skill contains:

- `SKILL.md` with only `name` and `description` in YAML frontmatter.
- `agents/openai.yaml` with Codex UI metadata.
- Required `references/`, `examples/`, or `evals/` resources.

The skills form this dependency chain:

```text
ai-briefcast-daily
├── ai-news-podcast          editorial evidence discipline
├── ai-briefcast-mg          optional ChatCut rendering route
└── ai-briefcast-imagegen    project-specific visual generation rules
    └── imagegen             Codex built-in raster image skill
```

## Skill Designs

### ai-briefcast-daily

Refresh the stale Codex copy from the latest Claude business rules. Preserve the
three approval checkpoints, source verification, writing constraints,
`episode.yaml` workflow, TTS behavior, subtitle alignment, cover generation,
publishing metadata, and QA requirements.

Adapt platform-specific behavior:

- Discover the repository root dynamically with Git instead of using a Windows
  absolute path.
- Use `rg` for local history and duplicate searches.
- Use Codex web access and primary-source links instead of `WebSearch` and
  `WebFetch`.
- Use ordinary Codex conversation checkpoints; when structured user-input
  tooling is available, use it, but do not require Claude's
  `AskUserQuestion`.
- Use `browser:control-in-app-browser` for creator-platform form filling.
- Stop before the final publish action and require explicit user approval.
- Refer to Codex skills by their discoverable names.

### ai-news-podcast

Preserve the E1-E5 evidence model, source verification, paper review, style
rules, structure rules, and quality gate. Remove Claude-only frontmatter fields
and tool allowlists. Use Codex web access when external verification is required.

Copy:

- `references/`
- `examples/`
- `evals/`

Do not copy:

- `README.md`
- `CHANGELOG.md`

### ai-briefcast-mg

Preserve the ChatCut timeline workflow, TTS requirements, ink-and-wash design
system, collage variant, canvas restrictions, Whisper alignment, frame
verification, and delivery rules.

Adapt integrations:

- Use `chatcut:chatcut-skill` for editable ChatCut work.
- Discover deferred ChatCut tools through Codex tool search when required.
- Use `ai-briefcast-imagegen` and the built-in `imagegen` skill for bitmap
  assets.
- Use the Codex in-app browser for editor handoff and inspection.
- Replace PowerShell/background-job advice with Codex tool orchestration that
  works in the active workspace.

### ai-briefcast-imagegen

Replace the Claude-side `codex-imagegen` CLI bridge with a Codex-native,
project-specific skill. It must route actual image creation or editing through
the built-in `imagegen` skill and add only Briefcast conventions:

- ink-and-wash illustrations
- logo-like seal assets
- editorial collage stills and transparent stickers
- 3:4 and 4:3 covers
- output naming and placement
- reference-image handling
- visual inspection and text-accuracy checks

It must not invoke a nested `codex exec`, install Codex, depend on a Windows
executable, or duplicate the full generic ImageGen instructions.

## Tool Mapping

| Claude-oriented reference | Codex adaptation |
| --- | --- |
| `AskUserQuestion` | Conversation approval checkpoint; structured input only when available |
| `WebSearch` / `WebFetch` | Codex web tool with primary-source verification |
| `ToolSearch` | Codex tool search |
| `Claude-in-Chrome` | `browser:control-in-app-browser` |
| `Read` image inspection | Codex image inspection tools |
| `codex exec` image bridge | Built-in `imagegen` skill and image generation tool |
| Windows repository path | Dynamic Git root / active workspace |
| PowerShell background jobs | Codex-native tool calls or bounded shell execution |

## Error Handling

- If an optional connector is unavailable, report the missing capability and
  continue with any safe local work; do not invent tool calls.
- If source verification cannot reach a primary source, label the evidence gap
  and do not promote the claim to verified fact.
- If generated assets fail visual inspection, regenerate or revise them before
  continuing to the timeline.
- If publishing automation cannot access an authenticated browser session,
  deliver the prepared files and publishing data without attempting final
  submission.
- Never overwrite user-edited `changed` scripts.

## Validation

Validate each skill independently before moving to the next:

1. Run a baseline scenario against the unadapted Claude instructions and record
   the incompatible behavior.
2. Validate YAML frontmatter and directory naming with `quick_validate.py`.
3. Scan Codex skill files for forbidden Claude-only tool names, Windows
   hard-coded paths, and nested Codex CLI image generation.
4. Forward-test realistic trigger prompts with the adapted skill.
5. Confirm required references resolve from each `SKILL.md`.
6. Confirm `agents/openai.yaml` matches the final skill description.
7. Inspect the final Git diff and verify `.claude/skills` is unchanged.

## Acceptance Criteria

- Codex discovers all four project skills from `.agents/skills`.
- The daily skill contains the current Claude business rules without stale
  workflow regressions.
- No Codex skill instructs the agent to call unavailable Claude-only tools.
- The image workflow uses native Codex ImageGen.
- The MG workflow routes through the available ChatCut skill and tool discovery.
- Claude skill files are byte-for-byte unchanged.
- All skill validators and repository-specific checks pass.
