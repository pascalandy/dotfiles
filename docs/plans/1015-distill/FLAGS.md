# Distill — CLI flags spec

Machine-readable flag definitions for `distill.py`. The user-facing rendered help lives in `HELP.md` (which becomes `meta/distill/help.md` at install time).

Script path: `dot_config/ai_templates/skills/meta/distill/scripts/distill.py`

## Synopsis

```
distill.py <input> [--prompt STEM] [--source-type TYPE] [--provider PROVIDER]
                   [--model MODEL] [--effort LEVEL] [--output-dir DIR]
                   [--keep-extracted] [--no-open] [--dry-run] [--quiet]
distill.py --list-prompts
distill.py --list-models [--provider PROVIDER]
distill.py --help
distill.py --version
```

---

## Positional arguments

| Name | Required | Description |
|---|---|---|
| `input` | yes (unless using `--list-*` / `--help` / `--version`) | File path OR `http(s)://` URL. Auto-detected. Tilde expansion supported for file paths. |

---

## Options

### Input handling

| Flag | Type | Default | Description |
|---|---|---|---|
| `--source-type {auto,file,article,media}` | string | `auto` | Force input handling. `auto` detects from input shape. `file` treats input as a local file path. `article` fetches the URL and cleans with `defuddle`. `media` fetches the URL and transcribes via `transcript-sk` (YouTube only for v1). |
| `--keep-extracted` | flag | off | For URL inputs, save the extracted intermediate text (cleaned article or raw transcript) in the output folder alongside the distilled result. |

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
| `--output-dir DIR` | path | type-dependent (see below) | Parent folder where the timestamped run folder is created. Overrides the default location. |
| `--no-open` | flag | off | Do not open the output folder in Finder when done (macOS only; no-op elsewhere). |

### Discovery

| Flag | Type | Description |
|---|---|---|
| `--list-prompts` | flag | List every prompt available in `meta/distill-prompt/references/` and exit. |
| `--list-models [--provider P]` | flag | List supported models. If `--provider` is given, list only that provider's models. Exits after printing. |

### Behavior

| Flag | Type | Description |
|---|---|---|
| `--dry-run` | flag | Resolve everything (input, source-type, prompt, provider, model, effort, output dir), check dependencies, print the plan, but do not fetch, transcribe, call LLM, or write files. |
| `--quiet` / `-q` | flag | Suppress progress output. Only errors and the final output path go to stderr/stdout. |
| `--help` / `-h` | flag | Render `meta/distill/help.md` via `glow` (fallback to plain markdown if `glow` not installed). Exit. |
| `--version` | flag | Print program version and exit. |

---

## Defaults summary

| Setting | Default |
|---|---|
| Source type | `auto` |
| Prompt | `follow_along_note` |
| Provider | `claude` |
| Claude model | `claude-opus-4-6` |
| Codex model | `gpt-5.4` |
| Effort | `medium` |
| Output dir (file input) | parent dir of the input file |
| Output dir (URL input) | `~/Documents/_my_docs/62_distill_exports` |
| Open in Finder | yes (macOS) |
| Keep extracted | no |

---

## Auto-detection rules (`--source-type auto`)

1. If `input` does not start with `http://` or `https://` → **file**
2. If `input` starts with `http(s)://`:
   - Host is `youtube.com`, `www.youtube.com`, `m.youtube.com`, or `youtu.be` → **media**
   - Otherwise → **article**

YouTube is the only auto-detected media host in v1. For other media hosts, use `--source-type media` explicitly.

Override with `--source-type` whenever auto-detection is wrong (e.g., a YouTube transcript HTML page you want as an article, or a non-standard media host).

---

## Output location logic

### File input
Output folder is created **inside the parent directory of the input file**.

```
~/Documents/article.md                           ← input
~/Documents/article_2026-04-06_14-32-08_follow_along_note/   ← output (sibling)
    ├── follow_along_note.md
    ├── source.txt
    └── meta.txt
```

### URL input (article or media)
Output folder is created in `~/Documents/_my_docs/62_distill_exports/`.

```
~/Documents/_my_docs/62_distill_exports/
└── 2QpXab8z_Gw_2026-04-06_14-32-08_summary_with_quotes/
    ├── summary_with_quotes.md
    ├── source.txt              # the URL
    ├── extracted.txt           # only if --keep-extracted
    └── meta.txt
```

### `--output-dir` override
Whenever set, all input types use the given directory as the parent. Tilde expansion supported.

### Run folder naming
Format: `{slug}_{timestamp}_{prompt}/`

| Input type | Slug derivation |
|---|---|
| file | filename stem (`article.md` → `article`) |
| article URL | last non-empty path segment slugified, fallback to hostname |
| media URL (YouTube) | video ID extracted from `?v=` or `youtu.be/<id>` |

Timestamp format: `YYYY-MM-DD_HH-MM-SS` (filesystem-safe, sortable).

Slugification: lowercase, alphanumerics + hyphens, max 60 chars.

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

The script applies the translation right before invoking the provider CLI. Users never see vendor-specific values. Adding a new effort level requires updating only the ETL table.

---

## Output folder contents

```
{slug}_{timestamp}_{prompt}/
├── {prompt}.md                # The distilled output (filename = prompt stem)
├── source.txt                 # File path or URL of the original input
├── extracted.txt              # (only if --keep-extracted and input was a URL)
└── meta.txt                   # Run metadata
```

`meta.txt` contents:
```
timestamp:    2026-04-06T14:32:08
input:        https://youtube.com/watch?v=2QpXab8z_Gw
source_type:  media (auto-detected)
extractor:    transcript-sk (Deepgram nova-3)
input_size:   18342 bytes / ~4585 tokens
prompt:       follow_along_note
provider:     claude
model:        claude-opus-4-6
effort:       medium → med (claude)
duration:     67.4s
version:      distill.py 1.0.0
```

---

## Exit codes

| Code | Meaning |
|---|---|
| `0` | Success |
| `1` | Generic error (unexpected exception) |
| `2` | Invalid arguments / usage error (argparse default) |
| `3` | Input file not found or not readable |
| `4` | Unknown prompt stem (suggests `--list-prompts`) |
| `5` | Provider CLI not found in PATH (`claude` or `codex`) |
| `6` | LLM call failed (timeout, context overflow, non-zero exit) |
| `7` | Output directory not writable |
| `8` | URL fetch failed (network error, non-200 response, timeout) |
| `9` | `defuddle` not found in PATH (required for article URLs) |
| `10` | `transcript.py` from transcript-sk not found or failed (required for media URLs) |

`glow` is **not** required — its absence falls back to plain print, no error.

---

## Validation rules

1. Exactly one positional `input` required unless using `--list-*`, `--help`, `--version`. Else exit `2`.
2. If resolved type is `file`: input must exist, be a regular file, be readable. Else exit `3`.
3. If resolved type is `article` or `media`: input must be a valid `http(s)://` URL. Else exit `2`.
4. `--prompt` stem must resolve to `meta/distill-prompt/references/<stem>/prompt.md`. Underscores and hyphens both accepted (normalize to kebab-case for filesystem lookup). Else exit `4`.
5. `--provider` must be in `{claude, codex}`. Argparse handles → exit `2`.
6. `--model` must be in the provider's valid list. Else exit `2`, suggest `--list-models`.
7. `--effort` must be in `{low, medium, high, max}`. Argparse handles → exit `2`.
8. Provider CLI must be in PATH. Else exit `5`.
9. If type resolves to `article`: `defuddle` must be in PATH. Else exit `9`.
10. If type resolves to `media`: `transcript-sk/scripts/transcript.py` must exist + be runnable. Else exit `10`.
11. Output dir parent must be writable. Else exit `7`.

Dependency checks are **lazy** — only the dependencies for the resolved source-type are checked. A user distilling local files never needs `defuddle` or Deepgram.

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

## `--dry-run` output (example, file input)

```
DRY RUN — no LLM call, no files written

input:           /Users/andy16/Documents/article.md (12483 bytes, ~3120 tokens)
source type:     file (auto-detected)
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

- (a) Output dir for URL inputs: `~/Documents/_my_docs/62_distill_exports` — agree? ✅/❌
- (b) Slug max length: 60 chars — agree? ✅/❌
- (c) For media URLs, is video ID a good slug, or do you prefer the video title (requires extra API call)? Video ID is faster and deterministic.
- (d) Any flags missing? (e.g., `--max-tokens`, `--temperature`, `--no-source-copy`, `--timeout`)
