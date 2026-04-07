---
name: Distill Flags
description: Flag definitions and usage for distill meta-skills
tags:
  - area/ea
  - kind/project
  - status/close
date_created: 2026-04-07
date_updated: 2026-04-07
---

# Distill - CLI flags spec

Machine-readable flag definitions for `distill.py`. The user-facing rendered
help lives in `HELP.md` (which becomes `meta/distill/help.md` at install time).

Script path: `dot_config/ai_templates/skills/meta/distill/scripts/distill.py`

## Synopsis

```
distill.py <input> [--prompt STEM] [--provider PROVIDER]
                   [--model MODEL] [--effort LEVEL] [--output-dir DIR]
                   [--no-open] [--dry-run] [--quiet]
distill.py --list-prompts
distill.py --list-models [--provider PROVIDER]
distill.py --help
distill.py --version
```

---

## Positional arguments

| Name | Required | Description |
|---|---|---|
| `input` | yes (unless using `--list-*` / `--help` / `--version`) | Local file path. Tilde expansion supported. |

---

## Options

### Prompt selection

| Flag | Type | Default | Description |
|---|---|---|---|
| `--prompt STEM` | string | `follow_along_note` | Distill prompt to apply. STEM matches a folder in `meta/distill-prompt/references/`. Underscores and hyphens both accepted. Use `--list-prompts` to see all available. |

### Provider & model

| Flag | Type | Default | Description |
|---|---|---|---|
| `--provider {claude,codex}` | string | `claude` | LLM backend. `claude` uses the local `claude` CLI; `codex` uses the local `codex` CLI. |
| `--model MODEL` | string | provider-dependent | Specific model name. Defaults: claude → `claude-opus-4-6`; codex → `gpt-5.4`. Use `--list-models` to see supported values. |
| `--effort {low,medium,high,max}` | string | `medium` | Reasoning effort (canonical vocabulary). Script translates internally per provider. See ETL table below. |

### Output

| Flag | Type | Default | Description |
|---|---|---|---|
| `--output-dir DIR` | path | parent dir of the input file | Parent folder where the timestamped run folder is created. Overrides the default location. |
| `--no-open` | flag | off | Do not open the output folder in Finder when done (macOS only; no-op elsewhere). |

### Discovery

| Flag | Type | Description |
|---|---|---|
| `--list-prompts` | flag | List every prompt available in `meta/distill-prompt/references/` and exit. |
| `--list-models [--provider P]` | flag | List supported models. If `--provider` is given, list only that provider's models. Exits after printing. |

### Behavior

| Flag | Type | Description |
|---|---|---|
| `--dry-run` | flag | Resolve everything (input, prompt, provider, model, effort, output dir), check dependencies, print the plan, but do not call the LLM or write files. |
| `--quiet` / `-q` | flag | Suppress progress output. Only errors and the final output path go to stderr/stdout. |
| `--help` / `-h` | flag | Render `meta/distill/help.md` via `glow` (fallback to plain markdown if `glow` not installed). Exit. |
| `--version` | flag | Print program version and exit. |

---

## Defaults summary

| Setting | Default |
|---|---|
| Prompt | `follow_along_note` |
| Provider | `claude` |
| Claude model | `claude-opus-4-6` |
| Codex model | `gpt-5.4` |
| Effort | `medium` |
| Output dir | parent dir of the input file |
| Open in Finder | yes (macOS) |

---

## Output location logic

### File input

Output folder is created inside the parent directory of the input file.

```
~/Documents/article.md                           ← input
~/Documents/article_2026-04-06_14-32-08_follow_along_note/   ← output
    ├── follow_along_note.md
    └── meta.txt
```

### `--output-dir` override

Whenever set, the given directory is used as the parent. Tilde expansion
supported.

### Run folder naming

Format: `{slug}_{timestamp}_{prompt}/`

| Input type | Slug derivation |
|---|---|
| file | filename stem (`article.md` → `article`) |

Timestamp format: `YYYY-MM-DD_HH-MM-SS` (filesystem-safe, sortable).

Slugification: preserve the filename stem unless sanitization is needed for
filesystem safety.

---

## `--effort` ETL (canonical → vendor)

User-facing canonical values: `low | medium | high | max`. Default `medium`.

Internal translation table:

| Canonical | Claude CLI | Codex CLI |
|---|---|---|
| `low` | `low` | `low` |
| `medium` | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

The script applies the translation right before invoking the provider CLI. Users
never see vendor-specific values. Adding a new effort level requires updating
only the ETL table.

---

## Output folder contents

```
{slug}_{timestamp}_{prompt}/
├── {prompt}.md                # The distilled output (filename = prompt stem)
├── source.txt                 # File path of the original input
└── meta.txt                   # Run metadata
```

`meta.txt` contents:
```
timestamp:    2026-04-06T14:32:08
input:        /Users/andy16/Documents/article.md
source_type:  file
input_size:   12483 bytes / ~3120 tokens
prompt:       follow_along_note
provider:     claude
model:        claude-opus-4-6
effort:       medium → med (claude)
duration:     12.4s
version:      distill.py 1.0.0
```

---

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Generic error (unexpected exception) |
| `2` | Invalid arguments / usage error |
| `3` | Input file not found or not readable |
| `4` | Unknown prompt stem (suggests `--list-prompts`) |
| `5` | Provider CLI not found in PATH (`claude` or `codex`) |
| `6` | LLM call failed (timeout, context overflow, non-zero exit) |
| `7` | Output directory not writable |

`glow` is not required - its absence falls back to plain print, no error.

---

## Validation rules

1. Exactly one positional `input` required unless using `--list-*`, `--help`,
   `--version`. Else exit `2`.
2. Input must exist, be a regular file, and be readable. Else exit `3`.
3. `--prompt` stem must resolve to
   `meta/distill-prompt/references/<stem>/prompt.md`. Underscores and hyphens
   both accepted (normalize to kebab-case for filesystem lookup). Else exit `4`.
4. `--provider` must be in `{claude, codex}`. Argparse handles → exit `2`.
5. `--model` must be in the provider's valid list. Else exit `2`, suggest
   `--list-models`.
6. `--effort` must be in `{low, medium, high, max}`. Argparse handles → exit `2`.
7. Provider CLI must be in PATH. Else exit `5`.
8. Output dir parent must be writable. Else exit `7`.

Dependency checks are minimal in v1. File-only usage requires only the selected
provider CLI.

---

## `--list-prompts` output (example)

```
Available distill prompts (from meta/distill-prompt/references/):

  follow_along_note      Detailed follow-along notes preserving structure
  short_summary          Concise high-level summary
  summary_with_quotes    Summary with verbatim quotes from the source

Use:  distill.py --prompt <stem> <input>
```

---

## `--list-models` output (example)

```
Claude models:
  claude-opus-4-6        (default)
  claude-opus-4-5
  claude-sonnet-4-5
  claude-haiku-4-5

Codex models:
  gpt-5.4                (default)

Effort levels (canonical, all providers):
  low, medium (default), high, max

Internal ETL:
  canonical  claude   codex
  low        low      low
  medium     med      medium
  high       high     high
  max        max      xhigh
```

With `--provider claude`, only the Claude block + ETL prints. Same for codex.

---

## `--dry-run` output (example)

```
DRY RUN - no LLM call, no files written

input:           /Users/andy16/Documents/article.md (12483 bytes, ~3120 tokens)
prompt:          follow_along_note
prompt path:     ~/.config/opencode/skill/meta/distill-prompt/references/follow-along-note/prompt.md
provider:        claude (found at /opt/homebrew/bin/claude)
model:           claude-opus-4-6
effort:          medium → med (claude)
output folder:   /Users/andy16/Documents/article_2026-04-06_14-32-08_follow_along_note/

Would write:
  follow_along_note.md
  source.txt
  meta.txt
```

---

## Open questions

- (a) Should v1 reject non-UTF-8 text files explicitly, or attempt a fallback?
- (b) Do you want any additional file-only flags later, such as `--no-source-copy`
  or `--timeout`?
