---
name: headless-claude
description: |
  Use only when the user explicitly says `headless-claude` to use claude -p (print mode) commands.
---

# Headless Claude

## Scope

Run Claude Code CLI in non-interactive print mode (`-p`) for scripting, automation, CI/CD, or quick answers without the TUI.
If behavior differs across versions, trust the installed CLI help output (`claude --help`) over external documentation.

**Important:** Print mode (`-p`) with default permissions **will hang** waiting for approval prompts. For truly unattended execution, always pair `-p` with a permission strategy (see Permissions section).

## Permissions and safety

In headless mode, permission handling determines whether the run completes or hangs. Resolve this first.

| Goal | Recommended shape | Why |
| --- | --- | --- |
| Analysis only, no edits | `claude -p --permission-mode plan "query"` | Safe default for audits, summaries, reviews; never hangs |
| Auto-approve edits, prompt on commands | `claude -p --permission-mode acceptEdits "query"` | Edits proceed; Bash commands still prompt (may hang) |
| Skip prompts, keep sandbox | `claude -p --permission-mode dontAsk "query"` | No prompts but tools remain sandboxed |
| Fully automatic | `claude -p --permission-mode auto "query"` | Claude decides what to approve |
| Fully unattended with all tools | `claude -p --dangerously-skip-permissions "query"` | Skips all prompts; highest risk |
| Enable bypass as an option (not default) | `claude -p --allow-dangerously-skip-permissions "query"` | Makes bypass available without enabling it by default; for sandboxes |
| Fine-grained tool allowlist | `claude -p --allowedTools "Bash(git *)" "Read" "query"` | Specific commands auto-approved, rest prompt |
| Restrict available tools | `claude -p --tools "Bash,Read" "query"` | Only listed tools exist in context |
| Block specific tools | `claude -p --disallowedTools "Edit" "query"` | Named tools removed from context entirely |

Permission mode choices: `default`, `plan`, `acceptEdits`, `dontAsk`, `auto`, `bypassPermissions`.

Important:

- **Default print mode hangs** on any permission prompt. Always specify a permission strategy.
- `--permission-mode plan` is the safest unattended default (read-only analysis, no edits).
- `--dangerously-skip-permissions` is equivalent to `--permission-mode bypassPermissions`.
- Ask before escalating to `--dangerously-skip-permissions`.

## Essential command patterns

### One-shot query (safe unattended)

```bash
claude -p --permission-mode plan "Explain this function"
```

### Pipe content

```bash
cat logs.txt | claude -p --permission-mode plan "Summarize these errors"
```

### Continue most recent conversation

```bash
claude -c -p "Check for type errors"
```

### Resume a named session

```bash
claude -r "auth-refactor" "Finish this PR"
```

### Resume from a PR

```bash
claude --from-pr 42 -p "Continue the review"
claude --from-pr https://github.com/org/repo/pull/42 -p "Check status"
```

### Models

```bash
claude --model opus -p "Review this code"
claude --model sonnet -p "Quick summary"
claude --model claude-sonnet-4-6 -p "Detailed analysis"
```

Use `--fallback-model` to auto-fallback when the primary model is overloaded (print mode only):

```bash
claude -p --fallback-model sonnet "Review this code"
```

### Effort level

```bash
claude --effort low -p "Quick check"
claude --effort high -p "Deep code review"
claude --effort max -p "Exhaustive analysis"
```

Options: `low`, `medium`, `high`, `max` (`max` requires Opus 4.6).

### Agents

Use `--agent` to select a configured subagent, or `--agents` to define one inline:

```bash
claude --agent my-custom-agent -p "Review this PR"
claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}' -p "Check this diff"
```

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

Additional stream-json flags:

```bash
# Include partial message events
claude -p --output-format stream-json --include-partial-messages "query"

# Bidirectional: read stream-json input, write stream-json output
claude -p --input-format stream-json --output-format stream-json "query"

# Echo user messages back on stdout for acknowledgment
claude -p --input-format stream-json --output-format stream-json --replay-user-messages "query"
```

### Structured output with JSON Schema

```bash
claude -p --json-schema '{"type":"object","properties":{"summary":{"type":"string"}}}' "Summarize this file"
```

### Budget limits

```bash
claude -p --max-budget-usd 5.00 "Expensive task"
```

## Fast startup

Use `--bare` to skip hooks, LSP, plugin sync, attribution, auto-memory, background prefetches, keychain reads, and CLAUDE.md auto-discovery. Claude retains Bash, file read, and file edit tools. Sets `CLAUDE_CODE_SIMPLE=1`. Skills still resolve via `/skill-name`.

When using `--bare`, provide context explicitly:

```bash
claude --bare -p "Quick question about Python syntax"
claude --bare --system-prompt "You are a Python expert" --add-dir ../lib -p "Review"
```

Available context flags with `--bare`: `--system-prompt`, `--append-system-prompt`, `--add-dir`, `--mcp-config`, `--settings`, `--agents`, `--plugin-dir`.

## System prompt customization

```bash
# Replace entire system prompt
claude --system-prompt "You are a Python expert" -p "query"

# Append to default prompt
claude --append-system-prompt "Always respond in JSON" -p "query"
```

`--system-prompt` replaces the default. `--append-system-prompt` adds to it. Both accept inline strings.

## Session management

```bash
# Named session (display name)
claude -n "review-session" -p "Start reviewing this PR"

# Explicit session UUID
claude --session-id "550e8400-e29b-41d4-a716-446655440000" -p "query"

# Continue most recent session in current directory
claude -c -p "Now check the tests"

# Resume by ID or name
claude -r "auth-refactor" "Continue where we left off"

# Resume from a PR
claude --from-pr 42 -p "Continue"

# Fork a session (new ID, keeps history)
claude --resume abc123 --fork-session "Try a different approach"

# Disable session persistence (one-off, no disk trace)
claude -p --no-session-persistence "One-off question"
```

## MCP servers

Load MCP servers for headless runs:

```bash
# From config file
claude --mcp-config ./mcp.json -p "query"

# Only use servers from this config (ignore all others)
claude --strict-mcp-config --mcp-config ./mcp.json -p "query"
```

## Additional directories and worktrees

```bash
# Grant access to additional directories
claude --add-dir ../apps ../lib -p "Review all modules"

# Run in an isolated git worktree
claude -w feature-auth -p "Implement auth module"

# Worktree with tmux session
claude -w feature-auth --tmux -p "Implement auth module"
```

## Settings override

```bash
# Load settings from file or JSON string
claude --settings ./settings.json -p "query"

# Control which setting sources are loaded
claude --setting-sources user,project -p "query"
```

## Debugging

```bash
claude --verbose -p "query"
claude --debug "api,mcp" -p "query"
claude --debug-file /tmp/claude-debug.log -p "query"
```

## Subcommands

```bash
claude agents              # List configured agents
claude auth status --text  # Check auth status
claude auto-mode           # Inspect auto mode classifier
claude doctor              # Health check for auto-updater
claude mcp                 # Configure MCP servers
claude plugin              # Manage plugins
claude setup-token         # Set up long-lived auth token
claude update              # Check for and install updates
```

## Failure handling

- On non-zero exit, report the exact failure and ask before retrying with broader permissions.
- If a run hangs waiting for permission prompts, rerun with `--permission-mode plan` (read-only) or `--dangerously-skip-permissions` (full access).
- Prefer the narrowest permission escalation that fits the task.
- Ask before escalating permission levels.

## Verification shortcuts

```bash
claude --help
claude --version
claude auth status --text
```
