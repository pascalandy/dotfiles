---
name: headless-delegation
description: Use only when the user explicitly says "use headless-delegation with <cli> to ..." where <cli> is claude, codex, or opencode. Delegates real execution work to a headless CLI agent from whatever CLI the user is currently driving, using the correct bash pty pattern per target CLI. Distinct from `delegate` (OpenCode sub-agent routing) and `delegate-claude` (executor→advisor pattern).
---

# Headless Delegation

## Scope

Dispatch real execution work to a headless CLI agent — `claude`, `codex`, or `opencode` — from inside whatever CLI the user is currently driving. This skill is the **orchestrator**. Flag references live in the primitives it cites.

**This skill executes work.** It does not route same-CLI sub-agents, and it does not ask an advisor for an opinion. If the task is "ask Opus what it thinks", use `delegate-claude` instead.

## Trigger

Fires only on the explicit, strict phrase:

```
use headless-delegation with <cli> to <task>
```

Where `<cli>` ∈ {`claude`, `codex`, `opencode`}. No shorthand, no inference, no fallback to "closest match". If the target CLI is anything else (e.g., `gemini`, `pi`), stop and tell the user it is out of scope for v1.

## Execution mode matrix

The CLI choice dictates the execution mode. Not negotiable per invocation.

| Target CLI | PTY | Base invocation | Notes |
|---|---|---|---|
| `claude` | **No** | `claude --print --permission-mode <mode> "<task>"` | Using `pty:true` + `--dangerously-skip-permissions` exits after the confirm dialog. `--print` avoids that. |
| `codex` | **Yes** | `codex exec "<task>"` (optional `--full-auto` or `--yolo`) | Must run inside a git repo. For scratch: `SCRATCH=$(mktemp -d) && cd "$SCRATCH" && git init`. |
| `opencode` | **Yes** | `opencode run "<task>"` | Pick agent with `--agent <name>` when the user specifies one. |

## Default permission posture

Start conservative. Only escalate when the task clearly requires writes.

| Task shape | Claude mode | Codex mode | OpenCode |
|---|---|---|---|
| Analysis, summarize, review, explain | `--permission-mode plan` | `codex exec` (default sandbox) | `opencode run` (default) |
| Edits in-place | `--permission-mode acceptEdits` | `codex exec --full-auto` | `opencode run` |
| Fully unattended, edits + shell | `--permission-mode bypassPermissions` | `codex exec --yolo` (ask user) | `opencode run` (rarely needed) |

Ask the user before escalating to `bypassPermissions` or `--yolo`.

## Foreground recipes (default)

### Claude Code

```bash
# Safe read-only analysis
claude --print --permission-mode plan "Summarize the errors in logs.txt"

# With piped input
cat errors.log | claude --print --permission-mode plan "Summarize these errors"

# Unattended edits (ask before using)
claude --print --permission-mode bypassPermissions "Add a dark mode toggle to src/settings.tsx"
```

### Codex

```bash
# Inside an existing repo
bash pty:true workdir:<cwd> command:"codex exec --full-auto 'Add a dark mode toggle to the settings page'"

# Scratch work (Codex refuses to run outside a git repo)
SCRATCH=$(mktemp -d) && cd "$SCRATCH" && git init && codex exec "Write a haiku about caching"
```

### OpenCode

```bash
bash pty:true workdir:<cwd> command:"opencode run 'Refactor src/auth.ts to use async/await'"

# Targeting a specific agent
bash pty:true workdir:<cwd> command:"opencode run --agent 2-opus 'Review this diff and suggest edits'"
```

## Background recipes

Use background mode when the task is long-running and the user wants to keep working. The bash tool returns a session id; track progress via `process` actions.

```bash
# Background codex
bash pty:true workdir:<cwd> background:true command:"codex exec --full-auto 'Build a REST API for todos'"
# → returns sessionId

# Background claude (no pty)
bash workdir:<cwd> background:true command:"claude --print --permission-mode bypassPermissions 'Refactor the auth module'"

# Monitor
process action:log    sessionId:<id>
process action:poll   sessionId:<id>
process action:submit sessionId:<id> data:"yes"   # send input + Enter
process action:kill   sessionId:<id>
```

### Auto-notify on completion

For long-running background jobs, append a wake trigger to the task prompt so the parent CLI gets pinged the moment the delegated agent finishes instead of waiting for the next heartbeat:

```bash
bash pty:true workdir:<cwd> background:true command:"codex exec --full-auto 'Build a REST API for todos.

When completely finished, run: openclaw system event --text \"Done: todos REST API\" --mode now'"
```

Only use the `openclaw` notifier when the parent CLI is OpenClaw. Otherwise skip it.

## Workflow

1. **Parse target CLI** from the user's prompt — match the literal token after `with` against `{claude, codex, opencode}`. If no match, stop and report.
2. **Resolve workdir** — current working directory by default. Accept an explicit override if the user names one.
3. **Refuse unsafe workdirs** — never dispatch into `~/.claude`, `~/.openclaw`, `~/.opencode`, or `~/Projects/openclaw/`. The delegated agent will read internal config and produce unpredictable output.
4. **Select execution mode** from the matrix above. Claude → no pty, `--print`. Codex / OpenCode → `pty:true`.
5. **Pick permission posture** — conservative by default. Escalate only if the task clearly needs writes; ask before `bypassPermissions` / `--yolo`.
6. **Prepare the workdir** — for Codex scratch work, create `mktemp -d && git init` first. For PR reviews, clone into a temp directory.
7. **Emit (and execute) the bash command.** Foreground by default. Background only on explicit request.
8. **Relay the output verbatim.** If the delegated agent fails, hangs, or exits non-zero, say so in one message. Do not silently take over and hand-code the patch yourself.

## Patterns to follow

- Strict trigger match — literal `with claude|codex|opencode`.
- PTY for Codex and OpenCode; never for Claude Code.
- `claude --print --permission-mode <mode>` is the Claude invocation; pick the mode from the permission posture table.
- Codex scratch work: `mktemp -d && git init` before `codex exec`.
- Background jobs: return the session id and show the `process` cheat sheet.
- PR reviews: clone to a temp directory — never review inside the parent CLI's own repo.
- Cite `headless-claude` / `headless-codex` / `headless-opencode` for flag details; do not duplicate their tables here.
- Bash code shown to the user must satisfy project bash standards (`set -euo pipefail`, `fct_*`, `log_*`) when the snippet is multi-line or saved as a script.

## Patterns to avoid

- Do not accept loose triggers like `delegate to codex` or `run this in claude headless` — they collide with `delegate` and `delegate-claude`.
- Do not use `--dangerously-skip-permissions` with `pty:true` for Claude Code — the CLI exits after the confirm dialog.
- Do not invoke Codex outside a git repo without creating a throwaway repo first.
- Do not start a delegated agent inside the parent CLI's state directory (`~/.claude`, `~/.openclaw`, `~/.opencode`, `~/Projects/openclaw/`).
- Do not silently substitute your own edits when the delegated agent fails — surface the failure.
- Do not swap the target CLI for a cheaper one. If the user said `with codex`, use Codex.
- Do not duplicate flag tables from the `headless-*` primitives. Link instead.
- Do not use `headless-delegation with claude` for tight advisor loops that re-paste `<PRIOR_ADVICE>` — that job belongs to `delegate-claude`.

## Gotchas

- **Claude Code + pty**: `bash pty:true command:"claude --dangerously-skip-permissions ..."` exits silently after the permission dialog. Use `--print --permission-mode bypassPermissions` with no pty.
- **Codex without git**: `codex exec` refuses to run outside a trusted git directory. Symptom is an immediate error about "untrusted directory". Fix: `mktemp -d && git init`.
- **OpenCode MCP cold boot**: if MCP startup is slow, run `opencode serve` in a background session and use `opencode run --attach http://localhost:<port>` for subsequent commands.
- **Background session forgets input**: `process action:write` sends raw bytes with no newline. Use `action:submit` to send text + Enter (simulating the user pressing return).
- **PR review inside the parent repo**: never check out a PR branch in the CLI's live working copy. Use `mktemp -d && gh repo clone ... && gh pr checkout <n>` and trash the temp dir after.
- **Unrelated context leak**: launching a headless agent without `workdir` pointed at the target project causes it to wander into adjacent folders. Always pass `workdir:<target>`.
- **Model pinning**: this skill is model-neutral per CLI. If the user wants a specific model, pass it explicitly (`opencode run --agent 2-opus`, `codex exec -m gpt-5-codex`, `claude --print --model claude-opus-4-7`).

## Cross-references

- Flag details for Claude: see `headless-claude/SKILL.md`.
- Flag details for Codex: see `headless-codex/SKILL.md`.
- Flag details for OpenCode: see `headless-opencode/SKILL.md`.
- OpenCode sub-agent routing (not delegation): see `delegate/SKILL.md`.
- Executor→advisor pattern (advice, not execution): see `delegate-claude/SKILL.md`.

## Update This Skill

Triggered when the user wants to refresh the skill against the latest primitives or CLI behavior.

**Trigger phrases:**
- "update the headless-delegation skill"
- "about skill headless-delegation, UPDATE the skill"
- "skill headless-delegation, check if we need to update"
- "refresh headless-delegation skill"

Load `references/UPDATE.md` for the checklist.
