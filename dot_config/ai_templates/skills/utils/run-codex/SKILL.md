---
name: run-codex
description: |
  Use only when the user explicitly says `run-codex`. Headless Codex to use codex exec commands.
---

# Headless Codex

## Scope

Run the modern OpenAI Codex CLI in headless mode with `codex exec`.
If behavior differs across versions, trust the installed CLI help output over old blog posts or legacy TypeScript-era examples.

## Essential command patterns

### Models and reasoning

Prefer the configured Codex default unless the user asks for a specific model.

```bash
codex -m gpt-5.4 -c 'model_reasoning_effort="xhigh"' -a never exec -s read-only "Tell me what I should know about this repo within two or three sentences."
```

reasoning-effort values include: - `none`, `minimal`, `low`, `medium`, `high`, `xhigh`

### resume from the most recent session

```bash
codex -m gpt-5.4 -c 'model_reasoning_effort="xhigh"' -a never exec -s read-only resume --last "Now tell me in 3 paragraph"
```

### Pipe

```bash
cat prompt.md | codex -m gpt-5.4 -c 'model_reasoning_effort="xhigh"' -a never exec -s read-only -
```

## Other options

### Approvals

Be explicit about approvals and sandboxing.

| Goal | Recommended shape | Why |
| --- | --- | --- |
| Read-only analysis (default) | `codex -a never exec -s read-only ...` | Safe default for audits, summaries, reviews |
| Workspace edits | `codex -a never exec -s workspace-write ...` | Lets Codex modify files without hanging on approval prompts |
| Low-friction local run with a human nearby | `codex exec --full-auto ...` | Shortcut for `on-request` + `workspace-write` |
| Externally sandboxed runner only | `codex exec --dangerously-bypass-approvals-and-sandbox ...` | Highest risk; only with explicit user permission |

Important:

- For truly unattended headless execution, prefer `-a never`.
- `--full-auto` is not the same as fully unattended execution; it maps to `--ask-for-approval on-request` plus `--sandbox workspace-write`.
- Ask before using `danger-full-access` or `--dangerously-bypass-approvals-and-sandbox`.

### Output handling

By default, `codex exec` prints the final agent message to stdout.
Progress and event-style diagnostics may appear separately, so redirect carefully.

Guidelines:

- Keep stderr visible while debugging auth, sandbox, or startup problems.
- If you need clean machine-readable output, prefer `--json` and/or `-o` instead of blindly suppressing stderr.
- If the user only wants a concise summary, run Codex, then summarize the result in plain language.
- When relevant, include changed files, tests run, warnings, and the session ID in your summary.

### Failure handling

- On non-zero exit, report the exact failure and ask before retrying with broader access.
- If a run stalls because Codex needs approvals, rerun with explicit `-a never` and the smallest sandbox that still fits the task.
- If resume warns about a model mismatch, keep the existing model unless the user wants to switch.
- Ask before escalating from `read-only` to `workspace-write`, and again before any full-access mode.

### Verification shortcuts

If you need to confirm current syntax:

```bash
codex --help
codex exec --help
codex exec resume --help
codex login --help
```
