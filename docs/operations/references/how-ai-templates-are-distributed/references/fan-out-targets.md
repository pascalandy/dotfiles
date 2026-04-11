---
name: Fan-out Targets
description: The eight agent homes that receive commands and skills from the post-apply rsync, with each one's destination layout
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-ai-templates-are-distributed
---

`fct_sync_agent_assets` at `.chezmoiscripts/run_after_backup.sh:75` takes the two rendered subpaths `commands_src` and `skills_src` and calls `fct_copy_dir` once per target. Eight agent homes total. Each has its own expected directory shape.

## The full table

| # | Agent | Commands destination | Skills destination | Source lines | Notes |
|---|---|---|---|---|---|
| 1 | OpenCode | `~/.config/opencode/commands` | `~/.config/opencode/skills` | `.chezmoiscripts/run_after_backup.sh:80-81` | Plain 1:1 mirror |
| 2 | Pi | `~/.pi/agent/prompts` | `~/.pi/agent/skills` | `.chezmoiscripts/run_after_backup.sh:84-85` | Commands land in `prompts/`, not `commands/` |
| 3 | Claude Code | `~/.claude/commands` | `~/.claude/skills` (flattened) | `.chezmoiscripts/run_after_backup.sh:88-92` | **Four subtrees merged up one level**. See [claude-code-flattening.md](claude-code-flattening.md). |
| 4 | Codex | `~/.codex/prompts` | `~/.codex/skills` | `.chezmoiscripts/run_after_backup.sh:95-96` | Commands land in `prompts/`, not `commands/` |
| 5 | Gemini | `~/.gemini/commands` | *(none)* | `.chezmoiscripts/run_after_backup.sh:99` | **Commands only** — Gemini does not receive skills |
| 6 | Amp | `~/.config/amp/commands` | `~/.config/amp/skills` | `.chezmoiscripts/run_after_backup.sh:102-103` | Plain 1:1 mirror |
| 7 | Agents | `~/.config/agents/commands` | `~/.config/agents/skills` | `.chezmoiscripts/run_after_backup.sh:106-107` | Plain 1:1 mirror |
| 8 | Factory | `~/.factory/commands` | `~/.factory/skills` | `.chezmoiscripts/run_after_backup.sh:110-111` | Plain 1:1 mirror |

## What each call does

Every row above compiles to one or more calls of `fct_copy_dir` with three positional arguments: source directory, destination directory, and sync mode. Example for OpenCode:

```bash
fct_copy_dir "$commands_src" "$HOME/.config/opencode/commands"
fct_copy_dir "$skills_src"   "$HOME/.config/opencode/skills"
```

The sync mode argument is omitted, so it defaults to `delete` — meaning `rsync -a --delete --delete-excluded --force`. See [rsync-semantics.md](rsync-semantics.md) for exactly what that expands to and why `--delete` is load-bearing.

## Two naming quirks

1. **Pi and Codex call commands "prompts".** The commands source renders the same way for every target, but for these two agents the destination directory is named `prompts/` instead of `commands/`. Pi's agent loader expects `~/.pi/agent/prompts/`; Codex expects `~/.codex/prompts/`. If you add a new command under `dot_config/ai_templates/commands/` and expect to invoke it from Pi, it will land in `prompts/`, not `commands/`.
2. **Gemini is commands-only.** There is no `fct_copy_dir "$skills_src" "$HOME/.gemini/..."` call in the script. Gemini CLI has no skill loader, so skills are never copied to Gemini. If you rely on a skill for a workflow and also use Gemini for that workflow, move the logic into a command.

## Special case: Claude Code flattening

Claude Code is the only target that does not mirror the source layout 1:1. Its four calls are:

```bash
fct_copy_dir "$skills_src/meta"    "$HOME/.claude/skills"
fct_copy_dir "$skills_src/pa-sdlc" "$HOME/.claude/skills"
fct_copy_dir "$skills_src/specs"   "$HOME/.claude/skills"
fct_copy_dir "$skills_src/utils"   "$HOME/.claude/skills"
```

All four subtrees land as siblings in `~/.claude/skills/`. This is important for skill naming. See the dedicated page: [claude-code-flattening.md](claude-code-flattening.md).

## Adding a ninth target

If a new agent CLI ships tomorrow, extending the fan-out is a two-step change: add one `fct_copy_dir` call per directory (usually `commands/` plus `skills/`) and verify the destination directory exists by running `mkdir -p` inside `fct_copy_dir` — which it already does. No change is needed anywhere else in the script.

The harder question is whether the new agent needs any layout transforms (flattening, renames like `prompts/`, skills exclusion). Read the script's existing calls as a template before adding yours.

## Related

- [[overview]]
- [[render-stage]]
- [[claude-code-flattening]]
- [[rsync-semantics]]
- [[troubleshooting]]
