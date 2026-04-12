---
name: Output Layout
description: The timestamped run folder, the three slug-prefixed artifacts, and the full meta.yml schema
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - distill
---

Every distill run writes exactly one new directory to disk. The directory is self-contained — it holds the distilled output, a copy of the original input, and a YAML sidecar with enough metadata to reproduce or audit the run. Nothing else is written, and nothing is touched outside the directory. This page is the authoritative reference for the naming scheme and the YAML schema.

## Run folder name

Composed by `make_run_folder_path` at `scripts/distill.py:572-577`:

```python
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
run_folder_name = f"{slug}_{timestamp}_{prompt_name}"
```

Resulting pattern:

```text
{slug}_{YYYY-MM-DD_HH-MM-SS}_{prompt_name}/
```

`slug` comes from `derive_slug` at `scripts/distill.py:561-569` — the input file's `Path.stem`, with a small set of separators (`/`, `\`, `:`, newline, tab) replaced by underscores. Unicode characters and other punctuation are preserved. If the stem is empty after sanitization, the literal string `input` is used instead.

`prompt_name` is the canonical underscore form produced by `normalize_prompt_stem` at `scripts/distill.py:471-477`. User-facing hyphens and `.md` suffixes are normalized away before the folder name is built.

The parent of the run folder is whichever directory the user specifies with `--output-dir`, falling back to the input file's parent directory (`scripts/distill.py:657-666`).

### Folder-name collision handling

If a run folder with the exact same name already exists, `execute_plan` sleeps ~1 second and recomputes the timestamp in a loop (`scripts/distill.py:1097-1107`). This covers the narrow case of two invocations landing within the same second; for any realistic workflow the collision retry fires at most once before the timestamp advances.

## The three artifacts inside the run folder

Every run writes three files. All three use the same `{slug}_` prefix for consistency across the folder:

```text
{slug}_{YYYY-MM-DD_HH-MM-SS}_{prompt_name}/
├── {slug}_{prompt_name}.md  # distilled result
├── {slug}_raw.{ext}         # copy of the original input, same extension
└── {slug}_meta.yml          # YAML run metadata
```

### `{slug}_{prompt_name}.md` — the distilled output

Created at `scripts/distill.py:1113`. The content is written directly by the provider runner (`run_claude`, `run_codex`, or `run_opencode`), not by `execute_plan` itself. The runner strips leading/trailing whitespace from the model's response and appends a trailing newline before writing.

### `{slug}_raw.{ext}` — the input copy

Created at `scripts/distill.py:1114-1116` via `shutil.copy2`. The original filename is discarded; the copy always uses `{slug}_raw` as its stem and preserves the input's original extension. `shutil.copy2` copies file metadata (mtime, permissions) along with the content so the raw copy is a faithful snapshot of what was actually distilled.

The copy exists so the run folder is a self-contained reproducibility bundle. The operator can move the folder anywhere, archive it, or ship it to someone else without needing the original input path to still resolve.

### `{slug}_meta.yml` — the sidecar

Created by `write_meta` at `scripts/distill.py:1045-1084`. Emitted as hand-written YAML (not via `yaml.safe_dump`) to preserve field order and keep the file diffable. Every key is output with a single space after the colon — no column alignment.

## Full `meta.yml` schema

The full set of fields `write_meta` can emit, in order:

| Field | Type | Always present? | Source |
|---|---|---|---|
| `file` | string | yes | Filename of the distilled output — `{slug}_{prompt_name}.md` |
| `original_file` | absolute path | yes | Resolved absolute path of the input file passed to the CLI |
| `date` | ISO-8601 datetime | yes | `datetime.now().isoformat(timespec='seconds')` captured at the start of the provider call |
| `prompt` | string | yes | Canonical underscore prompt stem (`follow_along_note`, `short_summary`, `summary_with_quotes`, etc.) |
| `prompt_file` | absolute path | yes | Absolute path of the `prompt.md` file that was loaded from the `distill-prompt` library |
| `provider` | string | yes | `claude`, `codex`, or `opencode` |
| `model` | string | yes | The resolved model ID (e.g. `claude-opus-4-6`, `gpt-5.4`, `1-kimi`) |
| `effort` | string | yes | `{canonical} → {vendor} ({provider})` — records both the user-facing and the vendor-translated values; for opencode the value is `agent-defined → agent-defined (opencode)` |
| `duration` | string | yes | Wall-clock duration of the provider call in seconds, formatted as `{n}s` with one decimal |
| `input_tokens` | integer (comma-separated) | yes | Count from `check_context_size` before the provider call |
| `total_tokens` | integer (comma-separated) | claude and opencode when available | Populated from the provider's usage payload |
| `output_tokens` | integer (comma-separated) | claude when available | Populated from the provider's usage payload |
| `distill_version` | string | yes | `__version__` from `scripts/distill.py:21`, currently `1.0.0` |

### Example meta.yml

From a real test run with input `article.md`, prompt `short_summary`, provider `claude`:

```yaml
file: article_short_summary.md
original_file: /tmp/distill-verify/test_real_run/article.md
date: 2026-04-11T12:18:40
prompt: short_summary
prompt_file: /Users/andy16/.../distill-prompt/references/short-summary/prompt.md
provider: claude
model: claude-opus-4-6
effort: high → high (claude)
duration: 0.2s
input_tokens: 3
total_tokens: 19
output_tokens: 7
distill_version: 1.0.0
```

## Historical note: the rename from `meta.txt`

Before 2026-04-11 the sidecar was named `meta.txt` with aligned-column key/value pairs (`file:            article_short_summary.md`). The extension changed to `.yml` and the formatting collapsed to single-space after the colon. The content is still wall-clock-identical — no fields were added or removed in the rename. The rename also added the `{slug}_` prefix to every file in the run folder (previously the distilled output was `{prompt_name}.md` and the input copy kept its original filename). Older run folders on disk keep their old filenames; the rename is forward-only.

## What is NOT in the run folder

- No log file. Provider stderr and retry-attempt messages go to the terminal during the run and are not persisted.
- No cache of the prompt text. The `prompt_file` field in meta.yml points at the library entry; the prompt's actual content is not copied into the run folder.
- No CLI argv snapshot. `meta.yml` records the resolved values, not the original argv, so defaults and explicit flags look the same after the fact.

## Related

- [[overview]]
- [[providers-and-effort]]
- [[prompts-library]]
