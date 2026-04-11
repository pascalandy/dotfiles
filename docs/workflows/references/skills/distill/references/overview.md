---
name: distill Overview
description: What distill is, why it exists, and the three-stage pipeline inside `execute_plan`
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - distill
---

`distill` solves one specific frustration: applying a long-form prompt to a local text file should be one command, not a workflow. Before distill, the operator's pipeline for "summarize this article" was copy-paste the prompt into a chat UI, copy-paste the article, wait, copy the answer back into some notes folder, and hope to remember which prompt was used and which model produced it. None of that was repeatable, versioned, or friction-free. distill encodes the whole loop as a Python CLI that runs in ~second-digit seconds of setup and writes every artifact to disk with provenance.

The script is self-contained: no config file, no hidden state, no network clients — it shells out to whichever provider CLI the user picks. All behavior is either a command-line flag, an input file, or a constant declared in the first 130 lines of `scripts/distill.py:21-117`. When distill surprises you, those first 130 lines are where the answer lives.

## The pipeline inside `execute_plan`

distill's runtime is a single function: `execute_plan` at `scripts/distill.py:1091-1148`. It runs three stages in order, with no branching on success paths:

### Stage 1: resolve

Before `execute_plan` is called, `main` at `scripts/distill.py:613-690` resolves every input to a concrete value:

- `resolve_input_file` reads the file and validates it as UTF-8 text (`scripts/distill.py:454-468`)
- `resolve_prompt` normalizes the user-provided stem (underscores and hyphens are equivalent, `.md` suffix is stripped) and maps it to `distill-prompt/references/<folder>/prompt.md` (`scripts/distill.py:471-496`)
- `resolve_model` validates the model string against the per-provider allowlist and falls back to the default if the user did not pass `--model` (`scripts/distill.py:499-536`)
- effort is resolved in three tiers: explicit `--effort` wins, otherwise Sonnet models get `low`, otherwise `DEFAULT_EFFORT` which is currently `high` (`scripts/distill.py:641-653`)
- `derive_slug` strips the input path's extension and sanitizes a short list of separators (`scripts/distill.py:561-569`)
- `make_run_folder_path` composes `{slug}_{timestamp}_{prompt}` for the run folder name (`scripts/distill.py:572-577`)

All of this lands in a frozen `ResolvedPlan` dataclass (`scripts/distill.py:177-196`). Every downstream function takes the plan and derives what it needs; nothing later in the pipeline looks at raw argv.

### Stage 2: call the provider

`execute_plan` creates the run folder, computes the three artifact paths, copies the input into `{slug}_raw.{ext}`, and then calls the matching provider runner: `run_claude`, `run_codex`, or `run_opencode`. Each runner shells out to the provider CLI with the resolved model and effort, captures structured output (JSON for claude and codex; a text-event stream for opencode), and writes the distilled result directly to the prompt output file.

Every provider call goes through `retry_request` (`scripts/distill.py:206-253`) with exponential backoff and `LLM_MAX_RETRIES = 3` (`scripts/distill.py:117`). Hard failures after the final attempt raise `LLMCallError` with the last CLI stderr embedded. Timeouts hit `LLM_CLI_TIMEOUT_SECONDS = 600` — ten minutes per attempt (`scripts/distill.py:116`).

### Stage 3: write meta and hand off

`write_meta` at `scripts/distill.py:1045-1084` emits the YAML sidecar. The run folder is opened in Finder on macOS unless `--no-open` is passed.

That is the entire runtime. There is no streaming output during the provider call (except for opencode, which reports incremental token events), no partial-state recovery, and no cleanup on failure — a crashed run leaves an incomplete folder on disk that the operator can either delete or inspect.

## What distill does not do

- It does not fetch URLs. The input must be a local file already on disk. The sibling `transcript-sk` skill exists for YouTube transcription and writes its output as a local file that distill can then consume.
- It does not render PDFs, DOCX, PPTX, or images. `liteparse` (a separate skill) handles that conversion to markdown, and distill runs on the conversion output.
- It does not compose prompts. Every prompt is a complete, standalone file in `distill-prompt/references/<stem>/prompt.md`. See [[prompts-library]].
- It does not track runs across invocations. Each run is independent; the only "memory" is the timestamped folder on disk and the `{slug}_meta.yml` inside it.
- It does not stream the distilled output back into the terminal for claude or codex. The output is written straight to `{slug}_{prompt}.md` and the script prints a one-line summary.

## Why three providers

distill supports `claude`, `codex`, and `opencode` because each one is good at a different tradeoff:

- **`claude`** is the default. Opus 4.6 with `--effort high` (the current default) produces the highest-quality distillations at the cost of latency and token spend.
- **`codex`** is a second opinion. GPT-5.4 with `--effort high` is a useful cross-check when a distillation feels off — it often frames the same content differently.
- **`opencode`** is the budget option. It routes through curated agents (`1-kimi`, `2-opus`, `3-gpt`, and others at `scripts/distill.py:71-86`) and respects the agent's own reasoning configuration — `--effort` is rejected at the argparse level when `--provider opencode` is used (`scripts/distill.py:435-436`).

Provider choice, model choice, and effort are orthogonal knobs. The full matrix and the Sonnet special-case are in [[providers-and-effort]].

## Related

- [[providers-and-effort]]
- [[output-layout]]
- [[prompts-library]]
- [[troubleshooting]]
- [[how-ai-templates-are-distributed]]
