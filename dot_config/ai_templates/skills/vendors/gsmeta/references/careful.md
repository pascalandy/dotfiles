# careful

> Safety guardrails that warn before destructive commands execute and let the user override each one.

## When to Use

- Working in production or a shared environment
- Debugging a live system where a stray command could cause data loss
- Any session where the user says "be careful", "safety mode", "prod mode", or "careful mode"

## Inputs

Nothing required. Activates immediately on invocation. No arguments.

## Methodology

### Activation

Tell the user: "Safety mode is now active. Every terminal command will be checked for destructive patterns before running. If a match is found, you'll see a warning and can choose to proceed or cancel."

### Pattern Check (pre-command gate)

Before running any terminal command, check the command string against the following table:

| Pattern | Example | Risk |
|---------|---------|------|
| `rm -rf` / `rm -r` / `rm --recursive` | `rm -rf /var/data` | Recursive delete |
| `DROP TABLE` / `DROP DATABASE` | `DROP TABLE users;` | Data loss |
| `TRUNCATE` | `TRUNCATE orders;` | Data loss |
| `git push --force` / `-f` | `git push -f origin main` | History rewrite |
| `git reset --hard` | `git reset --hard HEAD~3` | Uncommitted work loss |
| `git checkout .` / `git restore .` | `git checkout .` | Uncommitted work loss |
| `kubectl delete` | `kubectl delete pod` | Production impact |
| `docker rm -f` / `docker system prune` | `docker system prune -a` | Container/image loss |

**Safe exceptions — allow without warning:**

- `rm -rf node_modules`
- `rm -rf .next`
- `rm -rf dist`
- `rm -rf __pycache__`
- `rm -rf .cache`
- `rm -rf build`
- `rm -rf .turbo`
- `rm -rf coverage`

### On Match

1. Surface a warning identifying the destructive pattern
2. Ask the user to confirm or cancel before proceeding
3. The user can always override — this is a gate, not a block

### Scope

- Applies to terminal/shell command execution only
- File reads, searches, and non-destructive commands are unaffected
- Active for the session; ends when the conversation ends

## Quality Gates

- Every command in the protected pattern list triggers a warning before execution
- Safe exception patterns (build artifacts) pass without interruption
- User override is always available — the gate never permanently blocks

## Outputs

No artifacts. Behavioral change for the session: all terminal commands are pre-screened.

## Feeds Into

- >guard (combines careful + freeze for maximum safety)

## Harness Notes

In hook-capable harnesses (Claude Code), this is implemented as a `PreToolUse` hook on the Bash tool that returns `permissionDecision: "ask"` with a warning message on pattern match. In harnesses without hooks, the agent must perform the pattern check inline before issuing each terminal command — read the command, check the list, warn the user, wait for confirmation before proceeding.
