# distill

Distill a local text file through a named prompt using Claude or Codex.

## Synopsis

```text
distill.py <input> [options]
distill.py --list-prompts
distill.py --list-models [--provider PROVIDER]
distill.py --help
distill.py --version
```

## Description

`distill` reads a local text file, resolves a prompt name from `meta/distill-prompt`, runs it against your chosen LLM provider, and writes the result to a timestamped output folder.

This v1 scope is file-only. `meta/distill` remains a meta-skill so URL and media flows can be added later without changing the top-level skill name.

## Positional arguments

**`input`**
Local file path. Required unless using `--list-prompts`, `--list-models`, `--help`, or `--version`.

## Options

### Prompt selection

**`--prompt STEM`** - default: `follow_along_note`
Distill prompt to apply. STEM matches a folder in `meta/distill-prompt/references/`. Underscores and hyphens both accepted. Use `--list-prompts` to see all available prompts.

### Provider & model

**`--provider {claude,codex}`** - default: `claude`
LLM backend to use.

**`--model MODEL`**
Specific model name. Defaults depend on provider:
- claude -> `claude-opus-4-6`
- codex -> `gpt-5.4`

Use `--list-models` to see all supported values.

**`--effort {low,medium,high,max}`** - default: `medium`
Reasoning effort. Canonical vocabulary; the script translates per provider:

| Canonical | Claude | Codex |
|---|---|---|
| `low` | `low` | `low` |
| `medium` | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

### Output

**`--output-dir DIR`**
Parent folder for the timestamped run folder. Default: parent directory of the input file.

**`--no-open`**
Do not open the output folder in Finder when done (macOS only).

### Discovery

**`--list-prompts`**
List every prompt available in the distill-prompt library and exit.

**`--list-models`**
List supported models and exit. Combine with `--provider` to filter.

### Behavior

**`--dry-run`**
Resolve all inputs, check dependencies, and print the plan without calling the LLM or writing files.

**`-q, --quiet`**
Suppress progress output. Only errors and the final output path are printed.

**`-h, --help`**
Show this help message and exit.

**`--version`**
Show program version and exit.

## Defaults

| Setting | Default value |
|---|---|
| Prompt | `follow_along_note` |
| Provider | `claude` |
| Model (claude) | `claude-opus-4-6` |
| Model (codex) | `gpt-5.4` |
| Effort | `medium` -> `med` (claude) / `medium` (codex) |
| Output dir | parent directory of the input file |
| Run folder name | `{slug}_{timestamp}_{prompt}/` |
| Timestamp format | `YYYY-MM-DD_HH-MM-SS` |
| Open in Finder when done | yes (macOS only) |

## Output

Each run creates a timestamped folder named:

```text
{slug}_{timestamp}_{prompt}/
```

The folder contains:

- **`{prompt}.md`** - the distilled output
- **`{original_filename}`** - a copy of the original input file
- **`meta.txt`** - run metadata (timestamp, provider, model, effort, duration)

### Default output location

The output folder is created alongside the input file:

```text
~/Documents/article.md
~/Documents/article_2026-04-06_14-32-08_follow_along_note/
```

Override with `--output-dir`.

## Examples

**Local file, default prompt:**
```bash
distill ~/Documents/article.md
```

**Local file with specific prompt:**
```bash
distill --prompt short_summary ~/notes.txt
```

**Use codex with specific model and effort:**
```bash
distill --provider codex --model gpt-5.4 --effort max ./meeting.md
```

**See what prompts exist:**
```bash
distill --list-prompts
```

**See claude models only:**
```bash
distill --list-models --provider claude
```

**Verify flags without running:**
```bash
distill --dry-run --prompt summary_with_quotes ~/Documents/article.md
```

## See also

- `meta/distill-prompt` - the prompt library
- `transcript-sk` - unchanged, separate YouTube transcription workflow
