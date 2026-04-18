# Vision — headless-delegation

## Request Or Decision

Create a new skill named `headless-delegation` that delegates real work TO a headless CLI agent (`claude`, `codex`, `opencode`) from whatever CLI the user is currently driving, using the correct bash pty pattern per target CLI.

Trigger shape:

- `use headless-delegation with claude to do X-Y-Z`
- `use headless-delegation with codex to do X-Y-Z`
- `use headless-delegation with opencode to do X-Y-Z`

## Current State

Five existing skills partially cover the delegation / headless grid:

| Skill | Role | What it actually does |
|---|---|---|
| `headless-claude` | Primitive | Reference card for `claude -p` / `--print` flags |
| `headless-codex` | Primitive | Reference card for `codex exec` flags |
| `headless-opencode` | Primitive | Reference card for `opencode run` flags |
| `delegate` | Orchestrator | OpenCode sub-agent routing matrix (`1-kimi` spawns `2-gpt`, `3-glm`) |
| `delegate-claude` | Orchestrator | CLI-agnostic executor→advisor pattern — current CLI consults Claude Opus for advice via `claude -p` |

*Gap*: none of these actually **dispatch work** to a headless CLI from inside another CLI. `delegate` is a same-CLI sub-agent router (OpenCode only). `delegate-claude` keeps the work and only asks for advice. The `headless-*` trio are reference-only, not orchestrators.

The inspiration block the user shared (OpenClaw `Coding Agent (bash-first)` guide) already codifies the correct bash pty rules per CLI, including the Claude Code `--print` exception. That guide is the behavioral source of truth for what this new skill should encode.

## Observed Constraints

- **PTY required** for Codex and OpenCode. They are interactive terminal apps; without a pty, output corrupts or the agent hangs.
- **PTY forbidden** (or at least unnecessary) for Claude Code. `--dangerously-skip-permissions` + pty exits after the confirm dialog. Correct pattern is `claude --print --permission-mode bypassPermissions "task"`.
- **Codex requires a git repo.** Scratch work needs `mktemp -d && git init` first.
- **Never invoke the target CLI in the parent CLI's own state directory** (e.g., `~/.openclaw`, `~/.claude`, `~/.opencode`). The target will read internal configs and produce unpredictable output.
- **User bash standards** apply: `set -euo pipefail`, `fct_*` functions, `log_*` logging, no `.sh` extension on user scripts, XDG-compliant `~/.local/bin` for executables.
- **User CLI choice is authoritative.** If the user says "with codex", do not silently swap to a cheaper CLI.
- **Default Claude model**: Opus 4.7 is the user's default; Opus 4.7 1M is the current session. The advisor skill `delegate-claude` is pinned to Opus; `headless-delegation` must remain model-neutral per target CLI.

## Desired End State

A single skill, loaded by the trigger phrase `headless-delegation`, that:

1. Parses the target CLI from the user prompt (`with <cli>`).
2. Selects the correct execution mode for that CLI:
   - `claude` → bash, no pty, `--print --permission-mode bypassPermissions`
   - `codex` → bash + pty, `codex exec` (with optional `--full-auto` / `--yolo`)
   - `opencode` → bash + pty, `opencode run`
3. Emits (and by default executes) the right bash command for the task in the user's current working directory.
4. Supports a **foreground one-shot** mode as the default.
5. Supports a **background** mode on explicit request (session id, `process action:log / poll / submit / kill` monitoring).
6. Documents — but does not duplicate — the flag surface already covered in `headless-claude`, `headless-codex`, `headless-opencode`. It links to those primitives instead of copying their tables.
7. Stays distinct from `delegate` (OpenCode sub-agent routing) and `delegate-claude` (advisor pattern, no execution).

## Proposed Interaction Or Behavior

User (inside any CLI, e.g., OpenCode):

> use headless-delegation with codex to add a dark mode toggle to the settings page

Skill behavior:

1. Recognize target CLI: `codex`.
2. Resolve workdir: current project root (or explicit arg if given).
3. Emit bash command:
   ```bash
   bash pty:true workdir:<cwd> command:"codex exec --full-auto 'add a dark mode toggle to the settings page'"
   ```
4. For a background request, add `background:true`, return session id, show the `process action:log / poll / kill` cheat sheet.
5. On completion, surface the agent's output back to the user verbatim. If the delegated agent fails or hangs, say so explicitly — do not silently take over.

User (inside Claude Code):

> use headless-delegation with codex to review PR #130

Skill behavior: clone target repo to `mktemp -d`, `gh pr checkout 130`, then `codex review --base origin/main` with pty. Clean up the temp dir after.

User (inside OpenCode):

> use headless-delegation with claude to summarize this error log

Skill behavior: `cat error.log | claude --print --permission-mode plan "Summarize these errors"` — no pty, safe read-only mode.

## Design Decisions

1. **Role of this skill**: delegation-as-worker. Execution is delegated; advising is not. Advising stays in `delegate-claude`.
2. **Target CLIs in v1**: `claude`, `codex`, `opencode`. No Gemini, no Pi in scope.
3. **Execution mode matrix is hard-coded** per CLI (pty vs `--print`). Not negotiable per invocation — the CLI choice dictates the mode.
4. **Primitives stay primitives.** `headless-claude`, `headless-codex`, `headless-opencode` remain reference cards. This skill cites them; it does not replace them.
5. **Skill location**: `dot_config/ai_templates/skills/utils/headless-delegation/` — sits next to the `headless-*` primitives it cites.
6. **Default permission posture**: conservative by default. Use `--permission-mode plan` or equivalent read-only modes for analysis tasks; escalate to edit/auto modes only when the task clearly requires writes.
7. **Background mode is v1.** The bash pty pattern already supports `background:true`; documenting it is cheap. No git worktrees — out of scope.
8. **Trigger parsing is explicit.** Skill reads `with <cli>` from the user prompt; no inference, no fallback to "closest match".

## Patterns To Follow

- Bash pty for Codex and OpenCode.
- `claude --print --permission-mode bypassPermissions` for Claude Code — never pty.
- For Codex scratch work: `SCRATCH=$(mktemp -d) && cd $SCRATCH && git init && codex exec "..."`.
- For background sessions: return session id, document `process action:log | poll | submit | kill`.
- For PR reviews: clone to a temp directory — **never** review inside the parent CLI's own repo.
- Auto-notify on completion via `openclaw system event --text "Done: ..." --mode now` when the user is inside OpenClaw and the job is long-running.
- Cite `headless-claude` / `headless-codex` / `headless-opencode` for flag details rather than duplicating tables.
- Bash code in the skill examples must satisfy user bash standards (`set -euo pipefail`, `fct_*`, `log_*`).

## Patterns To Avoid

- Do not conflate with `delegate` (OpenCode sub-agent routing only).
- Do not conflate with `delegate-claude` (advisor pattern — returns advice, not execution).
- Do not use `--dangerously-skip-permissions` with pty for Claude Code — the CLI exits after the confirm dialog.
- Do not invoke Codex outside a git directory without creating a throwaway repo first.
- Do not start Codex, Claude, or OpenCode inside the parent CLI's state directory (`~/.claude`, `~/.openclaw`, `~/.opencode`, `~/Projects/openclaw/`).
- Do not hand-code patches yourself when the user asked to delegate — if the target agent fails, surface the failure, do not quietly substitute.
- Do not duplicate the flag tables from `headless-*` primitives; link instead.
- Do not silently pick a different CLI than the one named in the trigger.

## Success Signals

- User types `use headless-delegation with <cli> to ...` and the exact correct bash invocation fires, in the right workdir, with the right pty/print mode.
- The three delegation skills (`delegate`, `delegate-claude`, `headless-delegation`) feel mechanically distinct: sub-agent router, advisor, worker dispatcher.
- The primitives (`headless-*`) are still the single source of truth for flags; `headless-delegation` orchestrates them without overlap.
- Background mode returns a session id the user can poll.
- No regression in `delegate-claude` — advisor loops still work, and the user never confuses "ask Claude" with "run Claude".
- When the target CLI fails or hangs, the skill reports it within one message rather than taking over.

## Settled Decisions

- **Location**: `dot_config/ai_templates/skills/utils/headless-delegation/`.
- **v1 CLI coverage**: `claude`, `codex`, `opencode` only. No Gemini, no Pi.
- **Background mode**: in scope. Git worktrees / parallel recipes: out of scope.
- **Boundary with `delegate-claude`**: not resolved in this vision; carry forward as-is.

## Open Questions And Risks

confirmation: use headless-delegation with <cli>
