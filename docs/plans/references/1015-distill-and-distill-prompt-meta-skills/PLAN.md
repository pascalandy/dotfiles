---
name: Distill Plan
description: Plan for creating distill and distill-prompt meta-skills
tags:
  - area/ea
  - kind/project
  - status/stable
date_created: 2026-04-07
date_updated: 2026-04-07
---

# Plan 1015 - distill + distill-prompt meta-skills

## Goal

Create two new meta-skills that generalize the existing prompt workflow so local
text files can be processed through a growing library of "distill" prompts.

- `meta/distill` - the processor. One unified script handles local file input.
- `meta/distill-prompt` - the prompt library. Each distill style is a folder;
  grows independently.

`transcript-sk` stays untouched and out of scope for this plan.

## Why

- Today, processing prompts (`follow_along_note`, `short_summary`,
  `summary_with_quotes`) are locked inside `transcript-sk` and only reachable by
  going through YouTube transcription first.
- We want to distill arbitrary local text files with the same prompt library.
- We want to add new distill styles without touching code.
- We want `meta/distill` to remain a meta-skill because URL and media inputs may
  be added later, but they are explicitly out of scope for v1.

## Cross-skill dependency

```
meta/distill ──reads prompts from──▶ meta/distill-prompt
meta/distill (--help) ──renders via──▶ glow (optional, plain fallback)
```

`distill-prompt` has zero dependencies. `distill` depends on `distill-prompt`.

---

## Meta-skill 1: `meta/distill-prompt/`

Prompt library. Each prompt is its own sub-skill folder so it can grow
independently and be documented.

```
dot_config/ai_templates/skills/meta/distill-prompt/
├── SKILL.md                          # Collection: lists all distill prompts, how to add new ones
└── references/
    ├── ROUTER.md                     # prompt name (stem) → prompt folder
    ├── follow-along-note/
    │   ├── SKILL.md                  # When to use, expected output shape, sample
    │   └── prompt.md                 # Canonical prompt text
    ├── short-summary/
    │   ├── SKILL.md
    │   └── prompt.md
    └── summary-with-quotes/
        ├── SKILL.md
        └── prompt.md
```

### Conventions

- Folder name = prompt stem in kebab-case. Both `follow_along_note` and
  `follow-along-note` resolve to the same folder.
- `prompt.md` = the raw prompt text only. No frontmatter.
- `SKILL.md` = describes intent, when to use it, sample output shape.
- Adding a new distill style = drop a new folder + one row in `ROUTER.md`.
  No code changes.

### Initial content

Copy the 3 existing prompts from
`dot_config/ai_templates/skills/utils/transcript-sk/scripts/prompts/` into the
new structure. `transcript-sk` keeps its own copy.

---

## Meta-skill 2: `meta/distill/`

The processor. One unified script handles local file input. `meta/distill`
stays a meta-skill so future URL and media flows can be added without changing
the top-level skill name.

```
dot_config/ai_templates/skills/meta/distill/
├── SKILL.md                          # Collection: current file workflow + future expansion note
├── help.md                           # Rendered by --help via glow
├── scripts/
│   └── distill.py                    # Unified file-based processor
└── references/
    ├── ROUTER.md                     # Current routing table
    └── from-file/
        └── SKILL.md                  # "distill a local text file"
```

### Why keep it as a meta-skill

- The user explicitly wants `meta/distill` to remain the long-term entry point.
- The prompt library is already a separate concern from the processor.
- File-only scope keeps v1 small, while the directory structure leaves room for
  future `from-url` and `from-media` sub-skills.

### Current routing logic (`distill/references/ROUTER.md`)

| Request pattern | Route to |
|---|---|
| file path, `distill <file>`, local document | `from-file/SKILL.md` |
| URL or media requests | documented as future scope, not implemented in v1 |

### Input model in the script

| Input shape | Resolved type | Acquisition |
|---|---|---|
| local path | `file` | read UTF-8 text directly |

No auto-detection is needed in v1 because local file input is the only supported
source.

### Output location logic

Default output location:

| Input type | Default output parent | Run folder name |
|---|---|---|
| file | parent dir of the input file | `{slug}_{timestamp}_{prompt}/` |

`--output-dir DIR` always overrides the default.

**Slug derivation:** input filename stem (`article.md` → `article`)

**Timestamp format:** `YYYY-MM-DD_HH-MM-SS`

**Example folder names:**
- `article_2026-04-06_14-32-08_follow_along_note/`
- `meeting-notes_2026-04-06_14-32-08_short_summary/`

### `--effort` flag - single canonical vocabulary, internal ETL

User always types canonical values. Script translates per provider.

**Canonical (user-facing):** `low | medium | high | max`
**Default:** `medium`

**Internal ETL:**

| Canonical | Claude CLI value | Codex CLI value |
|---|---|---|
| `low` | `low` | `low` |
| `medium` | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

User never sees the vendor-specific values. If a vendor adds a new effort level
later, the ETL absorbs it.

### `--help` rendered via glow

`-h` / `--help` does not use argparse's auto-generated help. Instead:

1. Locate `meta/distill/help.md` relative to the script
   (`Path(__file__).parent.parent / "help.md"`)
2. If `glow` is in PATH → `glow help.md` (rendered terminal markdown)
3. If `glow` not in PATH → print raw markdown to stdout
4. Exit `0`

This means:

- `help.md` is the canonical CLI documentation, version-controlled with the
  meta-skill
- Help can be richer than argparse allows (sections, code blocks, tables,
  examples)
- Help renders well in any terminal that has `glow`
- Help still works without `glow` (fallback to plain markdown)
- Argparse parser uses `add_help=False`; we add a custom `-h/--help` action

### External dependency matrix

| Path | Required tools | Detected when |
|---|---|---|
| file | provider CLI (`claude` or `codex`) | always |
| `--help` | `glow` (optional, falls back to plain print) | only on `--help` |

File-only users do not need `defuddle`, Deepgram, or `transcript-sk`.

### Invocation examples

```
distill ~/Documents/article.md
distill --prompt short_summary ~/notes.txt
distill --provider codex --effort max ./meeting.md
distill --list-prompts
distill --list-models --provider claude
distill --help
```

---

## Build order

1. **Create `meta/distill-prompt/`**
   - Root `SKILL.md` (collection)
   - `references/ROUTER.md`
   - Three prompt sub-folders, each with `SKILL.md` + `prompt.md`
   - Copy prompt text from `transcript-sk/scripts/prompts/*.md`

2. **Create `meta/distill/` skeleton**
   - Root `SKILL.md` (collection) with file-oriented invocation scenarios and a
     note that URL/media flows are future scope
   - `help.md` (rich markdown CLI documentation, see `FLAGS.md`)
   - `references/ROUTER.md`
   - `references/from-file/SKILL.md`

3. **Build `scripts/distill.py`** (per `FLAGS.md` and `ARCHITECTURE.md`)
   - PEP 723 inline metadata, `uv run` shebang
   - Argparse with `add_help=False` + custom `-h/--help` action
   - File path validation and UTF-8 text loading
   - Output location logic (alongside file unless overridden)
   - Effort ETL (canonical → vendor-specific)
   - Prompt loading from `distill-prompt`
   - Type hints, ruff/pyright clean

4. **Test paths**
   - `distill --help` → renders help.md via glow
   - `distill --help` (without glow) → prints raw markdown
   - `distill --list-prompts` → enumerates from `distill-prompt`
   - `distill --dry-run ~/some-file.md` → resolves all flags, prints plan
   - `distill ~/some-file.md` → file path, output beside input
   - `distill --prompt summary_with_quotes ~/some-file.md`
   - `distill --effort max ~/file.md` → claude gets `max`
   - `distill --effort max --provider codex ~/file.md` → codex gets `xhigh`

5. **Apply via chezmoi**
   - `chezmoi apply -v` to sync to `~/.config/opencode/skill/meta/distill*`

---

## Acceptance criteria

- [ ] `meta/distill-prompt/` exists with 3 migrated prompts, each in its own sub-folder
- [ ] `meta/distill/` exists with `help.md`, `references/from-file`, and shared `scripts/distill.py`
- [ ] `distill.py` accepts local file paths
- [ ] `distill --help` renders `help.md` via glow (or plain fallback)
- [ ] File input writes output beside the input file by default
- [ ] Run folder naming follows `{slug}_{timestamp}_{prompt}/`
- [ ] `--effort` accepts canonical `low|medium|high|max` and ETLs per provider
- [ ] `distill --list-prompts` lists all prompts from `distill-prompt`
- [ ] File path works without `defuddle`, Deepgram, or `transcript-sk` installed
- [ ] `transcript-sk` is unchanged and still works on its own
- [ ] Both meta-skills follow the meta-skill-creator structure
- [ ] Script passes `ruff check` and `pyright`

---

## Open questions deferred

- Whether to eventually add URL input to `meta/distill`. Deferred.
- Whether to eventually add media input to `meta/distill`. Deferred.
- Whether to eventually delete prompts from `transcript-sk/scripts/prompts/` and
  have `transcript-sk` read from `distill-prompt`. Deferred.
- Stdin support for piped input. Deferred.
- Multiple inputs in one run (`distill *.md`). Deferred.

---

## Companion documents

- `FLAGS.md` - complete CLI surface, every flag, exit codes
- `HELP.md` - the rendered `help.md` content (canonical user-facing help)
- `ARCHITECTURE.md` - design decisions and invariants
