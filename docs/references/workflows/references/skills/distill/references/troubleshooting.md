---
name: Troubleshooting
description: Exit codes, common failure modes, and `--dry-run` as a diagnostic
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - distill
---

distill is deliberately loud on failure — every error path raises a typed exception with an explicit exit code, and the error message contains the actual subprocess stderr when a provider CLI is involved. This page maps the exit codes to their failure modes and documents the first thing to check for each one. When in doubt, `--dry-run` is the cheapest diagnostic: it resolves every input, validates every flag, and prints the plan without spending tokens.

## Exit code map

Declared at `scripts/distill.py:119-127`:

| Code | Constant | Raised by | Meaning |
|---|---|---|---|
| 0 | `EXIT_SUCCESS` | success path | Run completed, artifacts written |
| 1 | `EXIT_GENERIC_ERROR` | `DistillError` base | Catch-all — should be rare |
| 2 | `EXIT_USAGE` | argparse + `DistillError` with explicit code | Flag validation failed: unknown model, oversized input, `--effort` passed with `--provider opencode`, etc. |
| 3 | `EXIT_INPUT_NOT_FOUND` | `InputFileError` | Input file does not exist, is not a regular file, or is not valid UTF-8 |
| 4 | `EXIT_PROMPT_NOT_FOUND` | `PromptFileError` | Prompt stem did not resolve to a `prompt.md` under `distill-prompt/references/` |
| 5 | `EXIT_PROVIDER_MISSING` | `ProviderMissingError` | The selected provider's CLI binary was not found on `PATH` |
| 6 | `EXIT_LLM_FAILED` | `LLMCallError` | Provider CLI call failed after `LLM_MAX_RETRIES = 3` attempts, or its response could not be parsed |
| 7 | `EXIT_OUTPUT_NOT_WRITABLE` | `OutputDirError` | Run folder could not be created — usually a permission or disk-full issue |

## Common failure modes

### `--effort` is invalid

Historical: before 2026-04-11 the `EFFORT_ETL` table at `scripts/distill.py:94-107` mapped canonical `medium` to the claude vendor flag `med`. Upstream claude CLI removed the `med` short form and started emitting:

```text
error: option '--effort <level>' argument 'med' is invalid.
It must be one of: low, medium, high, max
```

distill would retry three times and then fail with exit code 6. The fix was to update the ETL to `"medium": "medium"`. If a future provider CLI changes its effort vocabulary the same way, the symptom will look identical: the script surfaces the CLI's own stderr inside the `LLMCallError` message, so grep the error output for `option '--effort'` to recognize the class of failure, then update the ETL entry for the affected canonical level.

### Input is too large

`check_context_size` at `scripts/distill.py:543-558` counts input + prompt + framing tokens via `tiktoken` (`cl100k_base` encoding) and compares against the per-provider limits at `scripts/distill.py:110-114`. If the input exceeds the limit:

```text
Input too large for {provider}: {input_tokens} tokens exceeds limit of {limit} tokens
```

Exit code: 2 (`EXIT_USAGE`). Remediation options, cheapest first:

1. Switch to a more permissive provider — claude at 600,000 is the highest ceiling, opencode at 250,000 is the lowest. See [[providers-and-effort]].
2. Split the input into two files and distill them separately, then concatenate the outputs.
3. Pre-summarize the input with a cheaper model first and distill the summary.

Note: the limit is conservative by design — it is below the model's actual context window. Raising the number in `CONTEXT_LIMITS` is the wrong fix unless the operator genuinely wants to push providers to their edges.

### Provider CLI is missing

`ensure_cli_available` checks for the provider's CLI binary on `PATH` during `main`. If claude, codex, or opencode is not found:

```text
{provider} CLI not found on PATH
```

Exit code: 5 (`EXIT_PROVIDER_MISSING`). The macOS-typical install paths for these CLIs are:

- `claude` → via Homebrew or the `cmux.app` bundle at `/Applications/cmux.app/Contents/Resources/bin/claude`
- `codex` → via npm or Homebrew
- `opencode` → via the opencode installer

Sanity-check with `which claude` (or the other names) before blaming distill.

### Provider CLI times out

`LLM_CLI_TIMEOUT_SECONDS = 600` at `scripts/distill.py:116`. A ten-minute timeout is long enough for heavy distillations at `--effort max` on large inputs but short enough to fail fast on a hung CLI. A timeout surfaces as:

```text
{provider} CLI timed out after 600s. Input may be too large or the model overloaded.
```

Exit code: 6 (`EXIT_LLM_FAILED`). The two likely causes are named in the message. If the input is not actually too large, the next-most-likely cause is provider-side backpressure; retry after a few minutes or switch providers.

### Provider returned unexpected JSON

For claude and codex, the runner parses the CLI's JSON output and expects specific keys (`result` for claude, a different schema for codex). A schema mismatch raises `LLMCallError` with the full key list:

```text
Unexpected claude JSON schema. Expected 'result' field. Got keys: [...]
```

Exit code: 6. This usually means the provider CLI version drifted — inspect the CLI's actual output with a standalone invocation (`echo "hi" | claude -p --output-format json`) and compare to what the runner expects in `scripts/distill.py:855-865`.

### Run folder already exists

Extremely rare. `execute_plan` at `scripts/distill.py:1097-1107` handles this by sleeping ~1 second and recomputing the timestamp, which is how the second-level timestamp in the folder name avoids collisions in any practical workflow. If the loop somehow cannot resolve after a retry, the script raises `OutputDirError` with exit code 7.

### Prompt stem did not resolve

`resolve_prompt` at `scripts/distill.py:480-496` fails with `EXIT_PROMPT_NOT_FOUND = 4` if the computed kebab-case folder under `distill-prompt/references/` does not contain a `prompt.md`. Three common causes:

1. Typo in the stem: underscores and hyphens are interchangeable, but spelling is not. Run `--list-prompts` to see the exact set.
2. A new prompt was added under `dot_config/ai_templates/skills/pa-sdlc/distill-prompt/` but `chezmoi apply` has not been run yet, so the fanned-out copy at `~/.claude/skills/distill-prompt/` is missing it.
3. The prompt folder exists but the `prompt.md` file inside is missing or was renamed.

### Input file is not valid UTF-8

`resolve_input_file` at `scripts/distill.py:454-468` calls `.read_text(encoding="utf-8")`. Binary files, files with BOM in unexpected places, or Windows-1252 files raise `InputFileError` with exit code 3. The script does not attempt fallback decoding — convert the file to UTF-8 first.

## `--dry-run` as a diagnostic

Every failure mode above except the provider call itself surfaces during resolution. `--dry-run` runs the full resolution stack and prints the plan without calling the provider. Use it as the first step when:

- A flag combination is suspected of being rejected
- The user wants to confirm which model, effort, and prompt will actually be used before committing tokens
- The input size is unknown and the context-limit check should happen first
- A new prompt was just added and resolution needs to be verified

The dry-run output prints the resolved input path, prompt path, provider CLI path, model, translated effort, run folder path, and the three artifact filenames distill would write. If the dry-run succeeds, the only remaining class of failure is the provider call itself.

## Where to read the actual error

Three places, in order of usefulness:

1. **Terminal stderr** — distill prints the full exception message, including subprocess stderr for provider failures, before exiting.
2. **Retry breadcrumbs** — `retry_request` at `scripts/distill.py:206-253` prints retry attempts to the console (unless `--quiet` is passed), so `Attempt 2 of 3...` followed by the final failure tells you this was a transient-looking error that never recovered.
3. **`meta.yml`** — only written on success. If the meta file is missing from a run folder, the run did not complete.

## Related

- [[overview]]
- [[providers-and-effort]]
- [[prompts-library]]
