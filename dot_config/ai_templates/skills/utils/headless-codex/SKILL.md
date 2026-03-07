---
name: headless-codex
description: Use whenever the user wants OpenAI Codex CLI run non-interactively: `codex exec`, `codex exec resume`, scripted/CI Codex automation, JSONL or schema-constrained Codex output, or headless Codex authentication with API keys or device code. Prefer this skill over interactive Codex guidance when the task should finish in one terminal command or continue a previous non-interactive Codex run.
---

# Headless Codex

## Scope

Run the modern OpenAI Codex CLI in headless mode with `codex exec`.
If behavior differs across versions, trust the installed CLI help output over old blog posts or legacy TypeScript-era examples.

## Core rules

- Use `codex exec` for a new non-interactive run.
- Use `codex exec resume` to continue a previous non-interactive run.
- Use top-level `codex resume` only for interactive TUI sessions, not for this skill.
- Prefer putting approval/global flags before `exec`, e.g. `codex -a never exec ...`.
- Do not hardcode outdated model defaults or old pricing tables.
- Do not blindly append `2>/dev/null`; it can hide auth, sandbox, and startup errors.

## Decide authentication first

Codex CLI reuses existing login state when available.

Choose the auth path that matches the environment:

- Local interactive login: `codex login`
- Headless ChatGPT login: `codex login --device-auth`
- CI / automation: prefer API-key auth

Useful patterns:

```bash
# One-off API-key-backed exec run
CODEX_API_KEY="$CODEX_API_KEY" codex -a never exec --ephemeral -s read-only "summarize this repo"

# Store API-key auth in the CLI cache
printenv OPENAI_API_KEY | codex login --with-api-key
```

Notes:

- Current Codex docs recommend API keys for programmatic automation.
- ChatGPT login is still valid for local use and can be done on headless machines with device code.
- Treat `~/.codex/auth.json` like a password if file-based credential storage is enabled.

## Choose the right safety profile

For headless runs, be explicit about approvals and sandboxing.

| Goal | Recommended shape | Why |
| --- | --- | --- |
| Read-only analysis | `codex -a never exec -s read-only ...` | Safe default for audits, summaries, reviews |
| Workspace edits | `codex -a never exec -s workspace-write ...` | Lets Codex modify files without hanging on approval prompts |
| Low-friction local run with a human nearby | `codex exec --full-auto ...` | Shortcut for `on-request` + `workspace-write` |
| Externally sandboxed runner only | `codex exec --dangerously-bypass-approvals-and-sandbox ...` | Highest risk; only with explicit user permission |

Important:

- For truly unattended headless execution, prefer `-a never`.
- `--full-auto` is not the same as fully unattended execution; it maps to `--ask-for-approval on-request` plus `--sandbox workspace-write`.
- Ask before using `danger-full-access` or `--dangerously-bypass-approvals-and-sandbox`.

## Command construction order

Use this order to avoid flag parsing surprises:

1. Start with `codex`
2. Add root/global flags before `exec` when needed: `-a`, `-m`, `-c`, `-p`, `-C`, `--search`
3. Add `exec`
4. Add exec-specific flags: `--ephemeral`, `-s`, `--skip-git-repo-check`, `--json`, `-o`, `--output-schema`, `-i`, `--add-dir`
5. Add the prompt as a positional argument, or use `-` to read the prompt from stdin

If the installed CLI rejects a flag after `exec`, move that flag before the subcommand.

## Recommended command patterns

### Read-only analysis

```bash
codex -C /path/to/repo -a never exec --ephemeral -s read-only \
  "Audit this repository and list the top 5 risks."
```

### Apply edits inside the workspace

```bash
codex -C /path/to/repo -a never exec --ephemeral -s workspace-write \
  "Fix the failing tests, run the relevant checks, and summarize what changed."
```

### Continue the most recent non-interactive session

```bash
codex -a never exec resume --last "Continue from the last result and implement the approved fix."
```

### Continue a specific non-interactive session

```bash
codex -a never exec resume 7f9f9a2e-1b3c-4c7a-9b0e-000000000000 \
  "Use the previous analysis and prepare the patch."
```

### Pipe the prompt from stdin

```bash
printf '%s' "Summarize the architecture and likely failure modes." | \
  codex -a never exec --ephemeral -s read-only -
```

### Capture JSONL events and the final answer separately

```bash
codex -a never exec --ephemeral -s read-only --json \
  -o /tmp/codex-final.txt \
  "Summarize the repo structure and highlight risky files." \
  > /tmp/codex-events.jsonl
```

### Enforce a structured final response

```bash
codex -a never exec --ephemeral -s read-only \
  --output-schema /tmp/schema.json \
  -o /tmp/result.json \
  "Extract project metadata into the required JSON schema."
```

### Run outside a Git repo only when necessary

```bash
codex -a never exec --ephemeral -s read-only --skip-git-repo-check \
  "Inspect this directory and explain what it contains."
```

## Models and reasoning

Prefer the configured Codex default unless the user asks for a specific model.
Current Codex docs recommend `gpt-5.4` for most tasks, but avoid hardcoding a model unless the user wants reproducibility or an override.

Useful overrides:

```bash
codex -m gpt-5.4 -a never exec --ephemeral -s read-only "review this repo"
codex -c 'model_reasoning_effort="high"' -a never exec --ephemeral -s read-only "debug this issue"
codex -c 'model_reasoning_summary="concise"' -a never exec --ephemeral -s read-only "explain this design"
```

Supported reasoning-effort values include:

- `none`
- `minimal`
- `low`
- `medium`
- `high`
- `xhigh`

## Output handling

By default, `codex exec` prints the final agent message to stdout.
Progress and event-style diagnostics may appear separately, so redirect carefully.

Guidelines:

- Keep stderr visible while debugging auth, sandbox, or startup problems.
- If you need clean machine-readable output, prefer `--json` and/or `-o` instead of blindly suppressing stderr.
- If the user only wants a concise summary, run Codex, then summarize the result in plain language.
- When relevant, include changed files, tests run, warnings, and the session ID in your summary.

## Web search and extra roots

Use root-level flags when needed:

```bash
codex --search -a never exec --ephemeral -s read-only "Find the latest docs for this dependency and summarize changes."
codex -C /repo -a never exec --ephemeral -s workspace-write --add-dir /tmp/build-artifacts "run the fix and write artifacts there"
```

Notes:

- `--search` enables live web search.
- Codex CLI may otherwise use cached web-search behavior depending on config and mode.
- `--add-dir` is useful when Codex must write outside the main worktree but still stay constrained.

## Failure handling

- On non-zero exit, report the exact failure and ask before retrying with broader access.
- If a run stalls because Codex needs approvals, rerun with explicit `-a never` and the smallest sandbox that still fits the task.
- If resume warns about a model mismatch, keep the existing model unless the user wants to switch.
- Ask before escalating from `read-only` to `workspace-write`, and again before any full-access mode.

## What to tell the user after a run

After running Codex:

1. Give the final answer in plain English.
2. Mention important side effects: files changed, commands/tests run, and warnings.
3. If the session should continue later, mention the user can ask for another `codex exec resume` run.

## Verification shortcuts

If you need to confirm current syntax, check the installed CLI directly:

```bash
codex --help
codex exec --help
codex exec resume --help
codex login --help
```

These commands are the fastest way to resolve version-specific uncertainty.
