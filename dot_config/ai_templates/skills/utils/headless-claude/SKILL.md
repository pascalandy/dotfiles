---
name: headless-claude
description: |
  Use only when the user explicitly says `headless-claude` to use claude -p (print mode) commands.
---

# Headless Claude

Run Claude Code CLI in non-interactive print mode for scripting, automation, CI/CD, or quick answers without the TUI.

## Essential command patterns

### One-shot query

```bash
claude -p "Explain this function"
```

### Pipe content

```bash
cat logs.txt | claude -p "Summarize these errors"
```

### Continue most recent conversation

```bash
claude -c -p "Check for type errors"
```

### Resume a named session

```bash
claude -r "auth-refactor" "Finish this PR"
```

### Attach a specific model

```bash
claude --model opus -p "Review this code"
claude --model sonnet -p "Quick summary"
claude --model claude-sonnet-4-6 -p "Detailed analysis"
```

### Set effort level

```bash
claude --effort high -p "Deep code review"
claude --effort max -p "Exhaustive analysis"
```

Options: `low`, `medium`, `high`, `max` (Opus 4.6 only).

## Permissions and safety

| Goal | Recommended shape | Why |
| --- | --- | --- |
| Read-only analysis (default) | `claude -p "query"` | Safe default; no file edits |
| Skip permission prompts | `claude --dangerously-skip-permissions -p "query"` | Unattended execution; highest risk |
| Plan mode (no edits) | `claude --permission-mode plan -p "query"` | Shows intent without executing changes |
| Accept edits without prompting | `claude --permission-mode acceptEdits -p "query"` | Edits auto-approved, commands still prompt |
| Specific tool allowlist | `claude --allowedTools "Bash(git *)" "Read" -p "query"` | Fine-grained control over what runs |
| Restrict available tools | `claude --tools "Bash,Read" -p "query"` | Limits which tools Claude can use |

Important:

- For unattended headless execution, `--dangerously-skip-permissions` is the only way to avoid hanging on prompts.
- Prefer the narrowest permission mode that fits the task.
- Ask before escalating to `--dangerously-skip-permissions`.

## Output handling

### Text output (default)

```bash
claude -p "query"
```

### JSON output

```bash
claude -p --output-format json "query"
```

### Streaming JSON

```bash
claude -p --output-format stream-json "query"
```

### Structured output with JSON Schema

```bash
claude -p --json-schema '{"type":"object","properties":{"summary":{"type":"string"}}}' "Summarize this file"
```

### Budget and turn limits

```bash
claude -p --max-budget-usd 5.00 "Expensive task"
claude -p --max-turns 3 "Quick analysis"
```

## Fast startup

Use `--bare` to skip auto-discovery of hooks, skills, plugins, MCP servers, and CLAUDE.md:

```bash
claude --bare -p "Quick question about Python syntax"
```

## System prompt customization

```bash
# Replace entire system prompt
claude --system-prompt "You are a Python expert" -p "query"

# Append to default prompt
claude --append-system-prompt "Always respond in JSON" -p "query"

# Load from file
claude --system-prompt-file ./custom-prompt.txt -p "query"
claude --append-system-prompt-file ./extra-rules.txt -p "query"
```

## Session management

```bash
# Named session
claude -n "review-session" -p "Start reviewing this PR"

# Continue that session
claude -c -p "Now check the tests"

# Fork a session (new ID, keeps history)
claude --resume abc123 --fork-session "Try a different approach"

# Disable session persistence
claude -p --no-session-persistence "One-off question"
```

## Additional directories

```bash
claude --add-dir ../apps ../lib -p "Review all modules"
```

## Failure handling

- On non-zero exit, report the exact failure and ask before retrying with broader permissions.
- If a run stalls waiting for permission prompts, rerun with `--dangerously-skip-permissions` or a more permissive `--permission-mode`.
- Ask before escalating permission levels.

## Verification shortcuts

```bash
claude --help
claude --version
claude auth status --text
```
