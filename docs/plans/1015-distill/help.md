# distill

Distill text from a file, web article, or YouTube video through a named prompt
using Claude or Codex.

## Synopsis

```
distill <input> [options]
distill --list-prompts
distill --list-models [--provider PROVIDER]
distill --help
distill --version
```

## Description

`distill` reads input from one of three sources, optionally extracts clean text,
then runs a named distill prompt against it using your choice of LLM provider.
The result is written to a timestamped output folder.

**Input types** (auto-detected, override with `--source-type`):

| Input shape | Type | Acquisition |
|---|---|---|
| local path | `file` | Read UTF-8 directly |
| `http(s)://youtube.com/...` or `youtu.be/...` | `media` | Transcribe via `transcript-sk` (Deepgram) |
| `http(s)://` anything else | `article` | Fetch + clean with `defuddle` |

## Positional arguments

**`input`**
File path OR `http(s)://` URL. Required unless using `--list-prompts`,
`--list-models`, `--help`, or `--version`.

## Options

### Input handling

**`--source-type {auto,file,article,media}`** — default: `auto`
Force input handling.
- `auto` — detect from input shape
- `file` — treat as local file path
- `article` — fetch URL, clean with `defuddle`
- `media` — fetch URL, transcribe via `transcript-sk`

**`--keep-extracted`**
For URL inputs, save the extracted intermediate text (cleaned article or
raw transcript) in the output folder alongside the distilled result.

### Prompt selection

**`--prompt STEM`** — default: `follow_along_note`
Distill prompt to apply. STEM matches a folder in
`meta/distill-prompt/references/`. Underscores and hyphens both accepted.
Use `--list-prompts` to see all available prompts.

### Provider & model

**`--provider {claude,codex}`** — default: `claude`
LLM backend to use.

**`--model MODEL`**
Specific model name. Defaults depend on provider:
- claude → `claude-opus-4-6`
- codex → `gpt-5.4`

Use `--list-models` to see all supported values.

**`--effort {low,medium,high,max}`** — default: `medium`
Reasoning effort. Canonical vocabulary; the script translates per provider:

| Canonical | Claude | Codex |
|---|---|---|
| `low` | `low` | `low` |
| `medium` | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

### Output

**`--output-dir DIR`**
Parent folder for the timestamped run folder. Defaults depend on input type:
- file input → parent directory of the input file
- URL input → `~/Documents/_my_docs/62_distill_exports`

**`--no-open`**
Do not open the output folder in Finder when done (macOS only).

### Discovery

**`--list-prompts`**
List every prompt available in the distill-prompt library and exit.

**`--list-models`**
List supported models and exit. Combine with `--provider` to filter.

### Behavior

**`--dry-run`**
Resolve all inputs, check dependencies, and print the plan without fetching,
transcribing, calling the LLM, or writing files.

**`-q, --quiet`**
Suppress progress output. Only errors and the final output path are printed.

**`-h, --help`**
Show this help message and exit.

**`--version`**
Show program version and exit.

## Defaults

Everything you get when you run `distill <input>` with no flags:

| Setting | Default value |
|---|---|
| Source type | `auto` (detect from input shape) |
| Prompt | `follow_along_note` |
| Provider | `claude` |
| Model (claude) | `claude-opus-4-6` |
| Model (codex) | `gpt-5.4` |
| Effort | `medium` → `med` (claude) / `medium` (codex) |
| Output dir (file input) | parent directory of the input file |
| Output dir (URL input) | `~/Documents/_my_docs/62_distill_exports` |
| Run folder name | `{slug}_{timestamp}_{prompt}/` |
| Timestamp format | `YYYY-MM-DD_HH-MM-SS` |
| Slug max length | 60 chars |
| Open in Finder when done | yes (macOS only) |
| Keep extracted intermediate | no |
| Quiet mode | no |
| Dry run | no |

**Effort ETL** — canonical → vendor:

| Canonical | Claude CLI | Codex CLI |
|---|---|---|
| `low` | `low` | `low` |
| `medium` (default) | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

**Auto-detection rules** (when `--source-type auto`):
1. Input does not start with `http(s)://` → **file**
2. Input starts with `http(s)://`:
   - Host is `youtube.com`, `www.youtube.com`, `m.youtube.com`, or `youtu.be` → **media**
   - Otherwise → **article**

**Lazy dependency checks** — only the tools for the resolved source type are required:

| Source type | Required tools |
|---|---|
| `file` | `claude` or `codex` CLI |
| `article` | `defuddle` + `claude` or `codex` CLI |
| `media` | `transcript.py` from transcript-sk + Deepgram keyring + `claude` or `codex` CLI |

`glow` is optional everywhere — used only to render this help text. Without it, plain markdown is printed.

## Output

Each run creates a timestamped folder named:

```
{slug}_{timestamp}_{prompt}/
```

where:
- **slug** — filename stem (file), URL path slug (article), or video ID (media)
- **timestamp** — `YYYY-MM-DD_HH-MM-SS`
- **prompt** — the prompt stem used

The folder contains:

- **`{prompt}.md`** — the distilled output
- **`source.txt`** — original file path or URL
- **`extracted.txt`** — intermediate extracted text (only with `--keep-extracted`)
- **`meta.txt`** — run metadata (timestamp, provider, model, effort, duration)

### File input output location

For file inputs, the output folder is created **alongside the input file**:

```
~/Documents/article.md                                           ← input
~/Documents/article_2026-04-06_14-32-08_follow_along_note/       ← output
```

### URL input output location

For URL inputs, the output folder is created in
`~/Documents/_my_docs/62_distill_exports/`:

```
~/Documents/_my_docs/62_distill_exports/
└── 2QpXab8z_Gw_2026-04-06_14-32-08_summary_with_quotes/
```

Override either with `--output-dir`.

## Examples

**Local file, default prompt:**
```bash
distill ~/Documents/article.md
```

**Local file with specific prompt:**
```bash
distill --prompt short_summary ~/notes.txt
```

**Web article (auto-detected, defuddle extraction):**
```bash
distill https://example.com/blog/post
```

**Web article with specific prompt:**
```bash
distill --prompt summary_with_quotes https://example.com/article
```

**YouTube video (auto-detected, transcript-sk delegation):**
```bash
distill https://youtube.com/watch?v=2QpXab8z_Gw
```

**Force article handling on a YouTube URL:**
```bash
distill --source-type article https://youtube.com/watch?v=...
```

**Use codex with specific model and effort:**
```bash
distill --provider codex --model gpt-5.4 --effort max ./meeting.md
```

**Keep the extracted intermediate text for review:**
```bash
distill --keep-extracted https://example.com/long-article
```

**Custom output directory:**
```bash
distill --output-dir ~/Desktop/distill-runs ~/Documents/article.md
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
distill --dry-run --prompt summary_with_quotes https://example.com/post
```

## Auto-detection rules

`--source-type auto` (the default) decides input type from the input shape:

1. Does not start with `http://` or `https://` → **file**
2. Starts with `http(s)://`:
   - Host is `youtube.com`, `www.youtube.com`, `m.youtube.com`, or `youtu.be`
     → **media**
   - Otherwise → **article**

YouTube is the only auto-detected media host. For other media hosts, pass
`--source-type media` explicitly.

## Dependencies

Lazy-checked. You only need the tools for the input type you actually use.

| Path | Required tools |
|---|---|
| file | `claude` or `codex` CLI |
| article | `defuddle` + `claude` or `codex` CLI |
| media | `transcript.py` from transcript-sk + Deepgram keyring + `claude` or `codex` CLI |

`glow` is optional and only used to render this help text. Without it, you'll
see plain markdown.

## Exit codes

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
| 8 | URL fetch failed |
| 9 | `defuddle` not found in PATH |
| 10 | `transcript.py` not found or failed |

## See also

- `transcript-sk` — the underlying YouTube transcription script
- `meta/distill-prompt` — the prompt library
- `defuddle` — HTML-to-markdown extractor
- `glow` — terminal markdown renderer
