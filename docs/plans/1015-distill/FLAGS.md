# Distill — CLI flags & help spec

Companion to `PLAN.md` and `ARCHITECTURE.md`. This document defines the **complete CLI surface** for `distill.py`. Approve this before any code is written.

The script lives at:
`dot_config/ai_templates/skills/meta/distill/scripts/distill.py`

It mirrors `transcript-sk/scripts/transcript.py` conventions for consistency: same provider/model flags, same output folder shape, same `--list-*` discovery commands. Adds URL handling and explicit source-type override.

---

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
| `--source-type {auto,file,article,media}` | string | `auto` | Force input handling. `auto` detects from input shape. `file` treats input as a local file path. `article` fetches the URL and cleans with `defuddle`. `media` fetches the URL and transcribes via `transcript-sk`. |
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
| `--effort LEVEL` | string | provider-dependent | Reasoning effort. Defaults: claude → `medium`; codex → `high`. Valid per provider: claude `{low,medium,high,max}`; codex `{low,medium,high,xhigh}`. |

### Output

| Flag | Type | Default | Description |
|---|---|---|---|
| `--output-dir DIR` | path | `~/Documents/_my_docs/62_distill_exports` | Parent folder where the timestamped run folder is created. |
| `--no-open` | flag | off | Do not open the output folder in Finder when done (macOS only; no-op elsewhere). |

### Discovery

| Flag | Type | Description |
|---|---|---|
| `--list-prompts` | flag | List every prompt available in `meta/distill-prompt/references/` and exit. |
| `--list-models [--provider P]` | flag | List supported models. If `--provider` is given, list only that provider's models. Exits after printing. |

### Behavior

| Flag | Type | Description |
|---|---|---|
| `--dry-run` | flag | Resolve everything (input, source-type, prompt, provider, model, output dir), check dependencies, print the plan, but do not fetch, transcribe, call LLM, or write files. |
| `--quiet` / `-q` | flag | Suppress progress output. Only errors and the final output path go to stderr/stdout. |
| `--help` / `-h` | flag | Show help and exit. |
| `--version` | flag | Print version and exit. |

---

## Defaults summary

| Setting | Default |
|---|---|
| Source type | `auto` |
| Prompt | `follow_along_note` |
| Provider | `claude` |
| Claude model | `claude-opus-4-6` |
| Claude effort | `medium` |
| Codex model | `gpt-5.4` |
| Codex effort | `high` |
| Output dir | `~/Documents/_my_docs/62_distill_exports` |
| Open in Finder | yes (macOS) |
| Keep extracted | no |

---

## Auto-detection rules (`--source-type auto`)

1. If `input` does not start with `http://` or `https://` → **file**
2. If `input` starts with `http(s)://`:
   - Host matches `youtube.com`, `youtu.be`, `vimeo.com`, `soundcloud.com`, `*.bandcamp.com` → **media**
   - Otherwise → **article**

Use `--source-type` explicitly when auto-detection is wrong (e.g., a YouTube transcript page you want as an article, or a non-standard media host).

---

## Output folder layout

For each run, a timestamped folder is created under `--output-dir`:

```
62_distill_exports/
└── 2026-04-06_14-32-08__article-name__follow_along_note/
    ├── follow_along_note.md      # The distilled output (filename = prompt stem)
    ├── source.txt                # File path or URL of the original input
    ├── extracted.txt             # (only if --keep-extracted and input was a URL)
    └── meta.txt                  # Run metadata
```

`meta.txt` contents:
```
timestamp:    2026-04-06T14:32:08
input:        https://example.com/blog/post
source_type:  article (auto-detected)
extractor:    defuddle 0.6.4
input_size:   12483 bytes / ~3120 tokens
prompt:       follow_along_note
provider:     claude
model:        claude-opus-4-6
effort:       medium
duration:     42.1s
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

---

## `--help` output (exact text)

```
usage: distill.py [-h] [--prompt STEM] [--source-type {auto,file,article,media}]
                  [--provider {claude,codex}] [--model MODEL] [--effort LEVEL]
                  [--output-dir DIR] [--keep-extracted] [--no-open]
                  [--dry-run] [--quiet] [--list-prompts] [--list-models]
                  [--version]
                  [input]

Distill text from a file, web article, or video/audio URL through a named prompt
using Claude or Codex.

Auto-detects the input type:
  - local file path  -> read UTF-8 directly
  - article URL      -> fetch + clean with defuddle
  - media URL        -> transcribe via transcript-sk (Deepgram)

Loads the chosen prompt from the meta/distill-prompt/ library and writes the
result to a timestamped output folder.

positional arguments:
  input                 File path OR http(s):// URL. Required unless using
                        --list-prompts, --list-models, or --version.

input handling:
  --source-type {auto,file,article,media}
                        Force input handling. (default: auto)
                          auto    -> detect from input shape
                          file    -> treat as local file path
                          article -> fetch URL, clean with defuddle
                          media   -> fetch URL, transcribe via transcript-sk
  --keep-extracted      For URL inputs, save the extracted intermediate text
                        in the output folder alongside the distilled result.

prompt selection:
  --prompt STEM         Distill prompt to apply. Must match a folder in
                        meta/distill-prompt/references/. Underscores and
                        hyphens both accepted.
                        (default: follow_along_note)

provider & model:
  --provider {claude,codex}
                        LLM backend to use. (default: claude)
  --model MODEL         Specific model name. Defaults depend on provider:
                          claude -> claude-opus-4-6
                          codex  -> gpt-5.4
                        Use --list-models to see all supported values.
  --effort LEVEL        Reasoning effort. Valid values per provider:
                          claude: low, medium, high, max  (default: medium)
                          codex:  low, medium, high, xhigh (default: high)

output:
  --output-dir DIR      Parent folder for timestamped run folders.
                        (default: ~/Documents/_my_docs/62_distill_exports)
  --no-open             Do not open the output folder in Finder when done.

discovery:
  --list-prompts        List every prompt available in the distill-prompt
                        library and exit.
  --list-models         List supported models and exit. Combine with
                        --provider to filter.

behavior:
  --dry-run             Resolve all inputs, check dependencies, and print the
                        plan without fetching, transcribing, calling the LLM,
                        or writing files.
  -q, --quiet           Suppress progress output. Only errors and the final
                        output path are printed.
  -h, --help            Show this help message and exit.
  --version             Show program version and exit.

examples:
  # Local file, default prompt
  distill.py ~/Documents/article.md

  # Local file with specific prompt
  distill.py --prompt short_summary ~/notes.txt

  # Web article (auto-detected, defuddle extraction)
  distill.py https://example.com/blog/post

  # Web article with specific prompt
  distill.py --prompt summary_with_quotes https://example.com/article

  # YouTube video (auto-detected, transcript-sk delegation)
  distill.py https://youtube.com/watch?v=2QpXab8z_Gw

  # Force article handling on a media URL
  distill.py --source-type article https://youtube.com/watch?v=...

  # Use codex with specific model and effort
  distill.py --provider codex --model gpt-5.4 --effort xhigh ./meeting.md

  # Keep the extracted intermediate text
  distill.py --keep-extracted https://example.com/long-article

  # See what prompts exist
  distill.py --list-prompts

  # See claude models only
  distill.py --list-models --provider claude

  # Verify flags without running
  distill.py --dry-run --prompt summary_with_quotes https://example.com/post

exit codes:
  0   success
  1   generic error
  2   invalid arguments
  3   input file not found / not readable
  4   unknown prompt stem
  5   provider CLI not found in PATH
  6   LLM call failed
  7   output directory not writable
  8   URL fetch failed
  9   defuddle not found in PATH
  10  transcript.py not found or failed
```

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
  efforts: low, medium (default), high, max

Codex models:
  gpt-5.4                (default)
  efforts: low, medium, high (default), xhigh
```

With `--provider claude`, only the Claude block prints. Same for codex.

---

## `--dry-run` output (example, article URL)

```
DRY RUN — no fetch, no LLM call, no files written

input:           https://example.com/blog/distillation-techniques
source type:     article (auto-detected from URL host)
extractor:       defuddle (found at /opt/homebrew/bin/defuddle)
prompt:          follow_along_note
prompt path:     ~/.config/opencode/skill/meta/distill-prompt/references/follow-along-note/prompt.md
provider:        claude (found at /opt/homebrew/bin/claude)
model:           claude-opus-4-6
effort:          medium
output folder:   ~/Documents/_my_docs/62_distill_exports/2026-04-06_14-32-08__distillation-techniques__follow_along_note/
keep extracted:  no

Would write:
  follow_along_note.md
  source.txt
  meta.txt
```

---

## Validation rules

1. Exactly one positional `input` required unless using `--list-*`, `--help`, `--version`. Else exit `2`.
2. If resolved type is `file`: input must exist, be a regular file, be readable. Else exit `3`.
3. If resolved type is `article` or `media`: input must be a valid `http(s)://` URL. Else exit `2`.
4. `--prompt` stem must resolve to `meta/distill-prompt/references/<stem>/prompt.md`. Underscores and hyphens both accepted (normalize to kebab-case for filesystem lookup). Else exit `4`.
5. `--provider` must be in `{claude, codex}`. Argparse handles → exit `2`.
6. `--model` must be in the provider's valid list. Else exit `2`, suggest `--list-models`.
7. `--effort` must be in the provider's valid list. Else exit `2`.
8. Provider CLI must be in PATH. Else exit `5`.
9. If type resolves to `article`: `defuddle` must be in PATH. Else exit `9`.
10. If type resolves to `media`: `transcript-sk/scripts/transcript.py` must exist + be runnable. Else exit `10`.
11. `--output-dir` parent must be writable. Else exit `7`.

Dependency checks are **lazy** — only the dependencies for the resolved source-type are checked. A user distilling local files never needs `defuddle` or Deepgram.

---

## Open questions before coding

- (a) Output dir default: `~/Documents/_my_docs/62_distill_exports` — agree with the `62_*` numbering convention? ✅/❌
- (b) Run folder naming: `{timestamp}__{input-stem-or-slug}__{prompt-stem}/` — good? ✅/❌
- (c) Media host list: `youtube.com`, `youtu.be`, `vimeo.com`, `soundcloud.com`, `*.bandcamp.com` — add/remove? ✅/❌
- (d) `--effort` as a single flag (current) vs separate `--claude-effort` / `--codex-effort`? Single is simpler. ✅/❌
- (e) Any flags missing? (e.g., `--max-tokens`, `--temperature`, `--no-source-copy`, `--timeout`)
