---
name: Distill Brief
description: Brief overview of distill meta-skills project
tags:
  - area/ea
  - kind/project
  - status/stable
date_created: 2026-04-07
date_updated: 2026-04-07
---

# Session brief - distill meta-skill design

A self-contained summary of the revised design conversation that produced the
current `distill` plan.

---

## 1. Starting point

The user has an existing skill, `transcript-sk`, that does this:

```
YouTube URL → yt-dlp (download audio) → Deepgram API (transcribe) → prompt.md (run via claude/codex) → distilled output
```

It supports three prompts today:
- `follow_along_note` - detailed notes
- `short_summary` - concise summary
- `summary_with_quotes` - summary with verbatim quotes

The script lives at
`dot_config/ai_templates/skills/utils/transcript-sk/scripts/transcript.py`.
Prompts live in `transcript-sk/scripts/prompts/`.

**The constraint:** `transcript-sk` works well and must remain untouched.

---

## 2. What the user wants now

1. **Generalize the prompt library to local files.**
2. **Keep the verb `distill`.**
3. **Separate prompts from processing code.**
4. **Keep `distill` as a meta-skill** so more input types can be added later.
5. **Leave `transcript-sk` alone.**
6. **Explicitly remove URL and media input from the current plan.**

---

## 3. Naming decisions

| Question | Decision |
|---|---|
| What to call the verb? | `distill` |
| Split prompts into a separate skill? | Yes - `meta/distill-prompt` |
| What to call the processing meta-skill? | `meta/distill` |
| Keep `distill` as meta even with file-only v1? | Yes |
| Where do outputs go? | Beside the input file by default |
| Run folder name format? | `{slug}_{timestamp}_{prompt}/` |

---

## 4. Architecture in one picture

```
Two new meta-skills:

dot_config/ai_templates/skills/
├── meta/
│   ├── distill/                    ★ NEW - the processor
│   │   ├── SKILL.md
│   │   ├── help.md                 ← rendered via glow on --help
│   │   ├── scripts/
│   │   │   └── distill.py          ← one script, file input only for v1
│   │   └── references/
│   │       ├── ROUTER.md
│   │       └── from-file/SKILL.md  ← docs view: local file workflow
│   │
│   └── distill-prompt/             ★ NEW - the prompt library
│       ├── SKILL.md
│       └── references/
│           ├── ROUTER.md
│           ├── follow-along-note/
│           │   ├── SKILL.md
│           │   └── prompt.md
│           ├── short-summary/
│           │   ├── SKILL.md
│           │   └── prompt.md
│           └── summary-with-quotes/
│               ├── SKILL.md
│               └── prompt.md
```

### Data flow

```
USER INPUT
    │
    ▼
distill <file> [flags]
    │
    ├── Validate input file
    ├── Load file text
    ├── Load prompt (from meta/distill-prompt/references/<stem>/prompt.md)
    ├── Call LLM (claude or codex, with effort ETL applied)
    └── Write output beside the input file

Output folder: {slug}_{timestamp}_{prompt}/
Contents: {prompt}.md, source.txt, meta.txt
```

---

## 5. The architectural decisions

| # | Decision | Why |
|---|---|---|
| 1 | Keep `meta/distill` as a meta-skill | Future URL/media expansion should not force a rename later. |
| 2 | File-only scope for v1 | Solves the immediate need without touching `transcript-sk`. |
| 3 | One unified script | Minimal code surface for v1. |
| 4 | Prompts as a separate meta-skill | Prompts grow independently of the processor. |
| 5 | File output beside input | Local files already have a natural home. |
| 6 | `--effort` is canonical (`low/medium/high/max`); ETL inside script | One vocabulary across providers. |
| 7 | `--help` renders `help.md` via `glow` | Rich, version-controlled help. |
| 8 | PEP 723 + uv + ruff + pyright + distinct exit codes | Matches coding standards. |

---

## 6. CLI surface (summary)

```
distill <input> [--prompt STEM] [--provider PROVIDER]
                [--model MODEL] [--effort LEVEL] [--output-dir DIR]
                [--no-open] [--dry-run] [--quiet]
distill --list-prompts
distill --list-models [--provider PROVIDER]
distill --help
distill --version
```

### Defaults

| Setting | Default |
|---|---|
| Prompt | `follow_along_note` |
| Provider | `claude` |
| Model (claude) | `claude-opus-4-6` |
| Model (codex) | `gpt-5.4` |
| Effort | `medium` |
| Output dir | parent dir of input file |
| Run folder | `{slug}_{timestamp}_{prompt}/` |
| Open in Finder | yes (macOS) |

### Effort ETL (canonical → vendor)

| Canonical | Claude | Codex |
|---|---|---|
| `low` | `low` | `low` |
| `medium` | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Generic error |
| 2 | Invalid arguments |
| 3 | Input file not found / not readable |
| 4 | Unknown prompt stem |
| 5 | Provider CLI not found in PATH |
| 6 | LLM call failed |
| 7 | Output directory not writable |

### Example invocations

```bash
distill ~/Documents/article.md
distill --prompt short_summary ~/notes.txt
distill --provider codex --effort max ./meeting.md
distill --list-prompts
distill --list-models --provider claude
distill --dry-run --prompt summary_with_quotes ~/Documents/article.md
```

---

## 7. External dependencies

| Path | Required tools | Lazy-checked? |
|---|---|---|
| `file` | `claude` or `codex` CLI | always required |
| `--help` | `glow` (optional, plain fallback) | only on `--help` |

A user distilling local text files needs nothing beyond `claude` or `codex` in
PATH.

---

## 8. Cross-skill relationships

```
meta/distill ──reads prompts from──▶ meta/distill-prompt
meta/distill (--help) ──renders via──▶ glow (optional, plain fallback)
```

- `distill-prompt` has zero dependencies.
- `distill` depends on `distill-prompt`.
- `transcript-sk` stays separate and unchanged.

---

## 9. What's deliberately NOT in scope

| Feature | Why deferred |
|---|---|
| URL input | Explicitly removed from this plan |
| Media input | Explicitly removed from this plan |
| Stdin / piped input | v1 takes file input only |
| Multiple inputs (`distill *.md`) | Single input only; shell loops handle batching |
| Custom prompts via inline flag | Use the prompt library; add a folder |
| `--temperature` / `--max-tokens` | Provider CLIs handle these |
| Prompt chaining | Run distill twice if needed |
| Web UI / TUI | CLI only |
| MCP tool wrapping | CLI works in any harness today |
| Migrating `transcript-sk` to read from `distill-prompt` | Future cleanup |

---

## 10. Build order

1. **Create `meta/distill-prompt/`**
   - Root `SKILL.md` + `references/ROUTER.md`
   - 3 prompt sub-folders, each with `SKILL.md` + `prompt.md`
   - Copy prompt text from `transcript-sk/scripts/prompts/*.md`

2. **Create `meta/distill/` skeleton**
   - Root `SKILL.md` + `help.md`
   - `references/ROUTER.md`
   - `references/from-file/SKILL.md`

3. **Build `scripts/distill.py`**
   - PEP 723 inline metadata, `uv run` shebang
   - Argparse with `add_help=False` + custom `-h/--help` action
   - File validation, prompt loading, effort ETL, output writing
   - Type hints, ruff/pyright clean

4. **Test** the file path, prompt, provider, and dry-run matrix

5. **Apply via chezmoi**: `chezmoi apply -v`

---

## 11. Artifacts produced in this session

All files live in `docs/plans/1015-distill/`:

| File | Purpose | Audience |
|---|---|---|
| `PLAN.md` | Full implementation plan | Engineer building this |
| `FLAGS.md` | Machine-readable flag spec | Engineer building this |
| `HELP.md` | Final user-facing help text | End user running `distill --help` |
| `ARCHITECTURE.md` | Design decisions with rationale + invariants | Future maintainer |
| `BRIEF.md` | Self-contained summary for review | External reviewer |

---

## 12. TL;DR for the reviewer

> Build two new meta-skills: `meta/distill` and `meta/distill-prompt`.
> `distill` is intentionally file-only in v1, but remains a meta-skill so URL
> and media inputs can be added later. Prompts move into a separate prompt
> library, while `transcript-sk` remains untouched. File inputs export beside the
> source file. Help is rendered via `glow` from a version-controlled `help.md`.
> Effort levels are canonical (`low/medium/high/max`) with internal ETL to
> vendor-specific values.
