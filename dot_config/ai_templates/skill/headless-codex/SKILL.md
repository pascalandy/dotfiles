---
name: headless-codex
description: Use when user asks to run Codex CLI, says "codex exec," "codex resume," or needs headless code analysis/refactoring via OpenAI Codex.
---

# Headless Codex

## Overview

Run OpenAI Codex CLI in headless mode for automated code analysis, refactoring, and editing. Append `2>/dev/null` to suppress thinking tokens. Default model: `gpt-5.2`.

## Running a Task

1. Default: model `gpt-5.2`, reasoning effort `high`. User can override.
2. Choose sandbox mode. Default: `--sandbox read-only` unless task requires edits or network.
3. Build command with required flags:
   - `-m, --model <MODEL>`
   - `--config model_reasoning_effort="<level>"`
   - `--sandbox <mode>`
   - `--full-auto` (for edits)
   - `-C, --cd <DIR>` (if needed)
   - `--skip-git-repo-check` (always include)
4. Append `2>/dev/null` to suppress stderr thinking tokens.
5. Run command and summarize output.
6. Tell user: "Say 'codex resume' to continue this session."

## Resuming Sessions

Resume with stdin. Do not add flags unless user specifies model or reasoning effort:

```bash
echo "your prompt" | codex exec --skip-git-repo-check resume --last 2>/dev/null
```

Insert flags between `exec` and `resume` if needed.

## Quick Reference

| Task | Command |
| --- | --- |
| Read-only analysis | `codex exec --skip-git-repo-check --sandbox read-only -m gpt-5.2 --config model_reasoning_effort="high" "prompt" 2>/dev/null` |
| Apply edits | `codex exec --skip-git-repo-check --sandbox workspace-write --full-auto -m gpt-5.2 --config model_reasoning_effort="high" "prompt" 2>/dev/null` |
| Full access | `codex exec --skip-git-repo-check --sandbox danger-full-access --full-auto -m gpt-5.2 --config model_reasoning_effort="high" "prompt" 2>/dev/null` |
| Resume | `echo "prompt" \| codex exec --skip-git-repo-check resume --last 2>/dev/null` |
| Different directory | Add `-C <DIR>` before prompt |

## Models

| Model | Use case | Price (input/output) |
| --- | --- | --- |
| `gpt-5.2` | Default. Software engineering, agentic workflows | $1.25/$10.00 per M |
| `gpt-5.2-max` | Ultra-complex reasoning | $1.25/$10.00 per M |
| `gpt-5.2-mini` | Cost-efficient (4x allowance) | $0.25/$2.00 per M |
| `gpt-5.1-thinking` | Deep analysis, 2x slower | — |

All models: 400K input / 128K output context. Cached input: 90% discount ($0.125/M).

## Reasoning Effort

| Level | Use case |
| --- | --- |
| `xhigh` | Deep problem analysis, complex reasoning |
| `high` | Refactoring, architecture, security |
| `medium` | Standard features, bug fixes |
| `low` | Quick fixes, formatting, docs |

## Error Handling

- Non-zero exit: stop and report, ask before retrying
- High-impact flags (`--full-auto`, `--sandbox danger-full-access`): get user permission first
- Warnings in output: summarize and ask how to proceed

## Requirements

Codex CLI v0.57.0+. Check: `codex --version`. Configure default model: `~/.codex/config.toml`.
