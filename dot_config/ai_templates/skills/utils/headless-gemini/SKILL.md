---
name: headless-gemini
description: Use whenever a user wants Gemini CLI run headlessly or non-interactively in scripts, CI, cron jobs, background shells, or other automation. Also use for Gemini-powered code review, architecture review, multi-directory analysis, large-context terminal workflows, structured JSON/JSONL output, or resuming Gemini CLI sessions outside the TUI.
---

# Headless Gemini CLI

## Goal

Run Gemini CLI safely and predictably in non-interactive environments.

This skill exists because headless Gemini runs have a few sharp edges:
- approval prompts do not behave like an interactive TUI session
- `--yolo` is deprecated in favor of `--approval-mode=yolo`
- output format matters a lot for automation
- sandboxing and enterprise policy can change what works
- model aliases are usually safer than hard-coding old preview model names

## Use this skill for

- CI/CD or cron-style Gemini CLI runs
- background shell jobs or one-shot terminal automation
- code review, security review, or architecture review via Gemini CLI
- large-context repo analysis, especially across multiple directories
- scripts that need machine-readable output
- follow-up runs that should resume a prior Gemini session

## Preflight

Before running anything substantial:

1. Check the installed CLI version:
   ```bash
   gemini --version
   ```
2. Prefer running from the relevant project root.
3. Confirm whether the user wants:
   - a **safe read-only review**
   - an **automated tool-using run**
   - **structured output** for another script
4. If the task spans more than one codebase, use `--include-directories` instead of changing directories repeatedly.

## Headless mode rules

### Prefer explicit headless invocation

For automation, prefer `-p` / `--prompt` even though Gemini docs also show positional one-shot prompts.
Using `-p` makes the intent explicit and matches current CLI help text.

```bash
gemini -p "Review this repository for security risks"
```

### Input sources

- `-p` / `--prompt` runs non-interactively.
- stdin can be piped into Gemini and is appended as extra context.
- `-i` / `--prompt-interactive` is for interactive sessions and should not be used for headless automation.
- `-i` cannot be used when piping from stdin.

Examples:

```bash
git diff --cached | gemini -p "Write a concise Conventional Commit message. Output only the subject line."
```

```bash
cat error.log | gemini -p "Explain the root cause and propose the smallest fix."
```

## Approval mode strategy

### The important rule

In non-interactive mode, actions that would normally require `ask_user` approval are effectively denied.
That means `default` approval mode is a poor fit for headless runs that need tools.
Do not rely on interactive confirmations in scripts.

### Which mode to choose

- `default`: fine only when the task is unlikely to need tool approval.
- `auto_edit`: auto-approves edit tools, but other tools can still be blocked.
- `yolo`: auto-approves all tool calls; the normal choice for unattended tool-using automation.
- `plan`: read-only planning mode; use only when you explicitly want analysis without execution and your environment supports it.

### Prefer the unified flag

Use:

```bash
--approval-mode=yolo
```

Avoid relying on:

```bash
--yolo
```

`--yolo` still exists, but current docs mark it as deprecated in favor of `--approval-mode=yolo`.

### Enterprise/policy caveat

If YOLO mode is blocked by policy, the run can still fail even with the right flags.
In hardened environments, prefer approved policy files over deprecated `--allowed-tools`.
Also note that org settings can disable YOLO mode entirely.

## Sandboxing

Gemini CLI supports sandboxing via `-s` / `--sandbox`, config, or `GEMINI_SANDBOX`.
Current docs also note that sandboxing is enabled by default when using `--approval-mode=yolo`.

Practical guidance:
- keep the default sandbox when possible
- use the most restrictive setup that still allows the task
- be explicit if the task truly needs host access, Docker, Podman, or another sandbox backend
- remember that sandbox constraints can explain missing commands, mount issues, or permission errors

## Model selection

Prefer stable aliases unless the user explicitly wants a pinned model.

### Good defaults

- `-m auto`: best default for most users
- `-m pro`: deeper review and harder reasoning
- `-m flash`: faster turnaround
- `-m flash-lite`: cheapest and fastest simple runs

### When to pin a concrete model

Use a concrete model name only when reproducibility or a specific preview capability matters.
Examples that may exist depending on account access and CLI version:
- `gemini-3.1-pro-preview`

If the user does not care, do **not** force a manual model choice first. Start with `auto` or `pro`.

## Output formats for automation

Choose output deliberately:

- `-o text`: human-readable output
- `-o json`: single JSON object
- `-o stream-json`: newline-delimited JSON events for progress-aware automation

### JSON mode

`--output-format json` returns a single object with:
- `response`
- `stats`
- optional `error`

Example:

```bash
gemini -m flash -p "Return a raw JSON object with keys 'version' and 'deps' from @package.json" \
  -o json | jq -r '.response'
```

### Streaming JSON mode

`--output-format stream-json` is better when you need incremental visibility.
Documented event types include:
- `init`
- `message`
- `tool_use`
- `tool_result`
- `error`
- `result`

## Exit codes to handle

Headless scripts should treat these as meaningful outcomes:

- `0`: success
- `1`: general error or API failure
- `42`: invalid input or arguments
- `53`: turn limit exceeded

If you hit `53`, split the task, narrow the prompt, or resume with a focused follow-up.

## Multi-directory analysis

Use `--include-directories` when the relevant context lives outside the current working tree.
The docs allow comma-separated values or repeated flags, with a maximum of 5 directories.

```bash
gemini -m pro \
  --include-directories ../backend,../docs \
  -p "Compare implementation and docs, then list mismatches."
```

## Session continuation

For longer investigations, reuse a recent session instead of starting from scratch:

```bash
gemini -r latest -p "Continue the prior review and focus on missing test coverage."
```

Use this when the user wants a follow-up pass and preserving prior context matters more than starting fresh.

## Recommended command patterns

### 1. Human-readable repo review

```bash
gemini -m pro --approval-mode=yolo \
  -p "Review this repository for security issues, risky shell usage, and secret leaks."
```

### 2. Structured output for another tool

```bash
gemini -m flash -o json \
  -p "Return a JSON array of the top 5 refactoring opportunities in @src with fields: file, reason, severity"
```

### 3. Streaming progress for long analysis

```bash
gemini -m pro -o stream-json --approval-mode=yolo \
  -p "Audit this repo and emit findings as you work."
```

### 4. Diff-based commit-message helper

```bash
git diff --cached | gemini -m flash \
  -p "Write one Conventional Commit subject line for these staged changes. Output only the line."
```

### 5. Bounded shell execution

Use a shell-level timeout wrapper for unattended runs.

```bash
timeout 300 gemini -m pro --approval-mode=yolo \
  -p "Review this codebase and summarize the 10 highest-risk issues."
```

On macOS, `timeout` may require GNU coreutils (`gtimeout`).

## Failure handling

When a headless run fails, check these in order:

1. **Auth / account / enterprise policy**
   - mismatched enforced auth can fail in non-interactive mode
   - org policy can disable YOLO mode
2. **Approval mode mismatch**
   - `default` or `auto_edit` may block the tools the task actually needs
3. **Sandbox restrictions**
   - missing commands, blocked writes, or mount issues often point here
4. **Output mode mismatch**
   - a downstream script may expect JSON while the run emitted text
5. **Prompt scope**
   - split overly broad tasks if you hit turn or context limits

## Working style

When using this skill:

1. Default to `-m auto` or `-m pro` unless the user asked for a specific model.
2. Default to `--approval-mode=yolo` for unattended tool-using automation.
3. Prefer `-o json` or `-o stream-json` when another script will consume the output.
4. Use `--include-directories` for cross-repo context instead of ad hoc directory hopping.
5. Add a shell timeout for background jobs.
6. Explain any security tradeoff before broadening permissions or disabling safeguards.
