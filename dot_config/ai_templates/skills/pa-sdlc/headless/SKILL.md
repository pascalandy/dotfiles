---
name: headless
description: |
  Headless CLI delegation and flag references. Use when the user says "use headless-delegation with <cli> to ..." to dispatch real execution work to a headless Claude / Codex / OpenCode agent using the correct pty pattern and permission posture. Also use when the user says `headless-claude`, `headless-codex`, or `headless-opencode` to look up CLI flags for non-interactive runs.
keywords:
  - headless-delegation
  - headless-claude
  - headless-codex
  - headless-opencode
  - claude -p
  - claude --print
  - claude --permission-mode
  - codex exec
  - codex --full-auto
  - codex --yolo
  - opencode run
  - opencode --agent
  - pty
  - non-interactive
---

# Headless

> Dispatch real execution work to a headless CLI agent -- Claude, Codex, or OpenCode -- and look up the flag surface of each CLI. Delegation is the core; the three CLI references are flag-lookup tables delegation cites.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Running a headless CLI agent from inside another CLI looks simple from the outside, but the details punish guesswork:

- **Execution mode is not interchangeable.** Claude Code `--print` without pty. Codex `exec` with pty, inside a git repo. OpenCode `run` with pty. Mixing these makes the delegated agent exit silently, hang on a permission dialog, or refuse to start.
- **Permission posture decides whether the run completes.** Print-mode Claude hangs on the first approval prompt unless paired with `--permission-mode <mode>`. Codex `exec` hangs unless paired with `-s read-only` or `-s workspace-write`. OpenCode needs the right agent and server mode.
- **Flag surfaces drift.** Each CLI has dozens of flags -- models, session resume, output format, MCP config, worktrees, budget limits -- and they change between versions.

An AI assistant handling this by feel produces broken bash, wrong permission modes, and quiet failures that look like model refusals.

---

## The Solution

This meta-skill collapses four related concerns into one entry point:

1. **Delegation** (core) -- The PTY matrix, permission posture, workdir refusal list, background / foreground recipes, and trigger discipline. Fires only on the strict phrase `use headless-delegation with <cli> to ...`. Cites the three CLI sub-skills for flag detail instead of duplicating them.

2. **Claude** (flag reference) -- Complete flag surface of `claude -p` / `claude --print`: permission modes, output formats, session management, MCP servers, worktrees, system prompts, beta headers, effort levels, Remote Control, subcommands.

3. **Codex** (flag reference) -- Complete flag surface of `codex exec`: model selection, reasoning effort, session resume, sandbox levels, image attachments, JSON output, piping input.

4. **OpenCode** (flag reference) -- Complete flag surface of `opencode run`: numbered core agents, specialized agents, session continuation, file attachments, server mode, output format.

The router dispatches to the right sub-skill based on the trigger phrase. The user never picks a sub-skill -- they describe what they need, and the right specialist activates.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | 4-row dispatch table that routes to the right sub-skill |
| Delegation sub-skill | `references/delegation/MetaSkill.md` | PTY matrix, permission posture, workdir hygiene, foreground / background recipes |
| Delegation update checklist | `references/delegation/references/UPDATE.md` | How to keep the orchestrator in sync with the three flag references and observed CLI behavior |
| Claude flag reference | `references/claude/MetaSkill.md` | Complete `claude -p` flag surface from the official CLI reference |
| Claude update checklist | `references/claude/references/UPDATE.md` | How to refresh against the official Claude Code CLI docs |
| Codex flag reference | `references/codex/MetaSkill.md` | Complete `codex exec` flag surface from the official CLI reference |
| Codex update checklist | `references/codex/references/UPDATE.md` | How to refresh against the official Codex CLI docs |
| OpenCode flag reference | `references/opencode/MetaSkill.md` | Complete `opencode run` flag surface with project-specific agents |
| OpenCode update checklist | `references/opencode/references/UPDATE.md` | How to refresh against the official OpenCode CLI docs |

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| `use headless-delegation with claude to summarize logs.txt` | Routes to `delegation/MetaSkill.md` -- emits `claude --print --permission-mode plan "Summarize the errors in logs.txt"` |
| `use headless-delegation with codex to add a dark mode toggle` | Routes to `delegation/MetaSkill.md` -- emits `bash pty:true workdir:<cwd> command:"codex exec --full-auto '...'"` |
| `use headless-delegation with opencode to refactor auth.ts` | Routes to `delegation/MetaSkill.md` -- emits `bash pty:true workdir:<cwd> command:"opencode run '...'"` |
| `headless-claude` | Routes to `claude/MetaSkill.md` -- shows the flag reference for `claude -p` |
| `headless-codex` | Routes to `codex/MetaSkill.md` -- shows the flag reference for `codex exec` |
| `headless-opencode` | Routes to `opencode/MetaSkill.md` -- shows the flag reference for `opencode run` |
| `claude --permission-mode acceptEdits "..."` | Routes to `claude/MetaSkill.md` -- looks up the permission-mode table |
| `codex exec --full-auto "..."` | Routes to `codex/MetaSkill.md` -- looks up the sandbox / approval matrix |
| `opencode run --agent 2-opus "..."` | Routes to `opencode/MetaSkill.md` -- looks up the agent catalogue |

---

## Example Usage

### Delegating execution (core path)

```
User: use headless-delegation with codex to write a REST API for todos

AI responds:
Routing to delegation sub-skill...

bash pty:true workdir:<cwd> command:"codex exec --full-auto 'Write a REST API for todos'"

Running inside an existing git repo. For scratch work, prefix with:
  SCRATCH=$(mktemp -d) && cd "$SCRATCH" && git init
```

### Looking up Claude flags

```
User: headless-claude

AI responds:
Routing to claude sub-skill...

[Shows the complete `claude -p` flag reference: permission modes,
output formats, session management, MCP servers, worktrees,
system prompts, effort levels, Remote Control, subcommands.]
```

### Cross-reference from delegation to flag table

```
User: use headless-delegation with claude to review src/auth.ts

AI responds:
Routing to delegation sub-skill...

  claude --print --permission-mode plan "Review src/auth.ts"

Permission-mode choices: default, plan, acceptEdits, dontAsk, auto,
bypassPermissions. See references/claude/MetaSkill.md for the full
flag surface.
```

---

## Configuration

No configuration required. The sub-skills are pure references plus one orchestrator. They read no persistent state and require no API keys beyond whatever the underlying CLI already needs.

---

## Customization

| Customization | Location | Impact |
|--------------|----------|--------|
| Add a new target CLI | new `references/<cli>/MetaSkill.md` + new row in `references/ROUTER.md` + one row in `delegation/MetaSkill.md` execution matrix | Extends delegation to a fourth CLI without touching existing sub-skills |
| Tighten / loosen delegation trigger | `references/delegation/MetaSkill.md` "Trigger" section | Change the strict phrase or the accepted `<cli>` set |
| Adjust default permission posture | `references/delegation/MetaSkill.md` "Default permission posture" table | Shift defaults conservative / permissive per CLI |
| Refresh flag references | `references/<cli>/references/UPDATE.md` | Follow the `npx nia-docs` workflow to diff against the official CLI docs |

---

## Related

- `delegate-to-sub` -- Same-CLI sub-agent routing (not headless delegation).
- `pa-advisor` -- Executor→advisor pattern (advice, not execution). Uses `claude -p` internally; see `references/claude/MetaSkill.md` for flag detail.
