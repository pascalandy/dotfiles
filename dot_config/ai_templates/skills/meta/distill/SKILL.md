---
name: distill
description: Apply a named distill prompt to a local text file using Claude or Codex, writing the result to a timestamped folder beside the input. USE WHEN distilling a local file, summarizing a text document, generating follow-along notes from a local article or transcript, applying a distill-prompt skill to a file on disk.
keywords: [distill, local-file, summarize, notes, follow-along, claude, codex, llm-cli, prompt]
---

# distill

> Apply a named distill prompt to a local text file. Output lands in a timestamped folder right next to the input.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

There is a good prompt library (`distill-prompt`) and two capable LLM CLIs (`claude`, `codex`), but no thin tool that glues them together for local files. Every time a user wants to apply one of the distill prompts to an article on disk, they either:

- Go through the YouTube transcription skill first (wrong tool for a local file)
- Hand-craft a shell pipeline with cat, the right effort flag, and the right model
- Copy-paste prompt text into an LLM chat

None of that is repeatable, versioned, or friction-free.

- **Prompts are reusable, workflows are not** -- the same prompt gets fed through 3 different ad-hoc pipelines
- **Vendor flag differences** -- `claude` uses `med`/`max`, `codex` uses `medium`/`xhigh`; users should not track that
- **No canonical output location** -- results scatter across Downloads, Desktop, clipboard

The fundamental issue: applying a distill prompt to a local file should be one command, not a workflow.

---

## The Solution

`meta/distill` is a thin CLI (`distill.py`) that takes a local text file and a prompt stem, resolves that prompt from `meta/distill-prompt`, runs the chosen LLM, and writes the output to a timestamped folder next to the source. It is intentionally file-only in v1 -- URL and media inputs are out of scope. The directory structure (`references/from-file/`) keeps room for future `from-url` / `from-media` sub-skills without requiring a rename.

**Core capabilities:**

1. **Thin wrapper** -- reads an input file, resolves a prompt stem, calls an LLM, writes output
2. **Canonical effort vocabulary** -- users type `low|medium|high|max`; script translates to per-vendor values internally
3. **Provider-agnostic** -- `--provider claude` or `--provider codex`, same interface
4. **Context-size pre-flight** -- fails fast with a clear error if input exceeds the safe limit (600k tokens for Claude, 450k for Codex)
5. **Glow-rendered help** -- `--help` reads `help.md` so rich markdown help is version-controlled
6. **Output lives next to source** -- timestamped folder `{slug}_{timestamp}_{prompt}/` beside the input file

---

## Workflow

1. **Pick the prompt.** Ask `distill-prompt` which prompt fits the user's need. Use that prompt's stem with `--prompt`.
2. **Read the CLI help.** Run the script's `--help` to see all flags, defaults, and exit codes:
   ```
   uv run ~/.config/opencode/skill/meta/distill/scripts/distill.py --help
   ```
3. **Invoke with the chosen prompt:**
    ```
    uv run ~/.config/opencode/skill/meta/distill/scripts/distill.py \
        ~/Documents/article.md \
        --prompt follow_along_note
    ```
4. **Output lands beside the input:**
    ```
    ~/Documents/article_2026-04-06_14-32-08_follow_along_note/
    ├── follow_along_note.md    # the distilled result
    ├── article.md              # a copy of the original input file
    └── meta.txt                # provider, model, effort, duration, token count
    ```

For dry-run, alternate providers, or custom output locations, read `help.md` via `--help`.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Router | `references/ROUTER.md` | Routes request patterns to the right input sub-skill |
| from-file sub-skill | `references/from-file/SKILL.md` | Docs for the local-file input path (v1 default) |
| CLI help | `help.md` | Full user-facing CLI help, rendered by `--help` via glow |
| Script | `scripts/distill.py` | PEP 723 single-file Python script |

**Summary:**
- **Input sub-skills:** 1 (from-file)
- **Scripts:** 1 (distill.py)
- **Dependencies:** `distill-prompt` (prompt library), `claude` or `codex` CLI, `uv` runtime, `tiktoken` + `rich` (auto-installed by uv), optional `glow` for rich help rendering

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "distill my article.md" | Routes to from-file -- runs distill.py on the file with default prompt (`follow_along_note`) |
| "summarize this file with short-summary" | Routes to from-file -- invokes distill-prompt to choose `short_summary`, then passes it via `--prompt` |
| "distill with codex max effort" | Routes to from-file -- same flow with `--provider codex --effort max` |
| "what distill options exist" | Run `distill.py --help` to see full flag reference |
| URL or YouTube link | Out of scope in v1. Use `utils/transcript-sk` for YouTube. |

---

## Configuration

No configuration required. Defaults cover the common case:

- Provider: `claude`
- Model: `claude-opus-4-6`
- Effort: `medium`
- Output: beside the input file
- Open in Finder when done (macOS)

All defaults are overridable via flags. See `help.md` via `--help`.

---

## Related Work

- **`meta/distill-prompt`** -- the prompt library that `distill` reads from
- **`utils/transcript-sk`** -- YouTube transcription skill (separate workflow, remains unchanged)

---

## What This Skill Does NOT Do

| Out of Scope | Why |
|---|---|
| URL input | Deferred. `meta/distill` remains a meta-skill so `from-url` can be added later without renaming. |
| Media input (audio/video) | Deferred. `from-media` is a future sub-skill. |
| Stdin / piped input | v1 accepts file paths only. |
| Batch input (`distill *.md`) | Single input per invocation. Use shell loops for batching. |
| Inline prompt text flag | Use the prompt library. Add a folder in `distill-prompt` for new prompts. |
| Prompt chaining | Run `distill` twice with intermediate files. |
