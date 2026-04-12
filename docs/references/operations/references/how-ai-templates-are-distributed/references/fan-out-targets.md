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

`fct_sync_agent_assets` at `.chezmoiscripts/run_after_backup.sh:104-150` takes the two compiled scratch directories (`compiled_commands_dir` and `compiled_skills_dir`, both freshly `mktemp -d` before the fan-out) and calls `fct_copy_dir` twice per target — once for commands, once for skills. Eight agent homes total. Each has its own expected directory shape, but all sixteen calls source from the same two compiled directories, so every agent receives the same flattened content.

## The full table

| # | Agent | Commands destination | Skills destination | Source lines |
|---|---|---|---|---|
| 1 | OpenCode | `~/.config/opencode/commands` | `~/.config/opencode/skills` | `.chezmoiscripts/run_after_backup.sh:117-118` |
| 2 | Pi | `~/.pi/agent/prompts` | `~/.pi/agent/skills` | `.chezmoiscripts/run_after_backup.sh:121-122` |
| 3 | Claude Code | `~/.claude/commands` | `~/.claude/skills` | `.chezmoiscripts/run_after_backup.sh:125-126` |
| 4 | Codex | `~/.codex/prompts` | `~/.codex/skills` | `.chezmoiscripts/run_after_backup.sh:129-130` |
| 5 | Gemini | `~/.gemini/commands` | `~/.gemini/skills` | `.chezmoiscripts/run_after_backup.sh:133-134` |
| 6 | Amp | `~/.config/amp/commands` | `~/.config/amp/skills` | `.chezmoiscripts/run_after_backup.sh:137-138` |
| 7 | Agents | `~/.config/agents/commands` | `~/.config/agents/skills` | `.chezmoiscripts/run_after_backup.sh:141-142` |
| 8 | Factory | `~/.factory/commands` | `~/.factory/skills` | `.chezmoiscripts/run_after_backup.sh:145-146` |

All eight rows use the same shape: one `fct_copy_dir` call for commands, one for skills, both with explicit `sync_mode=delete` passed as the third argument. Every call expands to the same `rsync -a --delete --delete-excluded --force --exclude '.DS_Store'` invocation. See [rsync-semantics.md](rsync-semantics.md).

## What each call does

Every row above compiles to two calls of `fct_copy_dir` with three positional arguments: source directory, destination directory, and the literal string `"delete"`. Example for OpenCode at `.chezmoiscripts/run_after_backup.sh:117-118`:

```bash
fct_copy_dir "$compiled_commands_dir" "$HOME/.config/opencode/commands" "delete"
fct_copy_dir "$compiled_skills_dir"   "$HOME/.config/opencode/skills"   "delete"
```

`compiled_commands_dir` and `compiled_skills_dir` are both freshly-created scratch directories populated by `fct_compile_assets` immediately before the sixteen fan-out calls. See [claude-code-flattening.md](claude-code-flattening.md) for how compilation works.

## Two naming quirks

1. **Pi and Codex call commands "prompts".** The commands compile directory renders the same way for every target, but for these two agents the destination directory is named `prompts/` instead of `commands/`. Pi's agent loader expects `~/.pi/agent/prompts/`; Codex expects `~/.codex/prompts/`. If you add a new command under `dot_config/ai_templates/commands/` and expect to invoke it from Pi, it will land in `prompts/`, not `commands/`.
2. **Gemini gets skills.** Earlier versions of the script omitted the skills call for Gemini, leaving it commands-only. Under the current design, Gemini receives the same compiled skills directory every other agent gets. Whether Gemini's loader actually reads that directory is a Gemini-side decision — it may or may not do anything with the skills — but the fan-out no longer treats it as a special case.

## Cleanup

After the sixteen fan-out calls complete, `fct_sync_agent_assets` removes both scratch directories at `.chezmoiscripts/run_after_backup.sh:149`:

```bash
rm -rf "$compiled_commands_dir" "$compiled_skills_dir"
```

This is explicit cleanup, not tied to any `trap`. It runs regardless of success because the function is called from `fct_main` which has its own top-level `trap` for the render stage's scratch directory. If you add a new agent home by inserting more `fct_copy_dir` calls, place them above this cleanup line — after cleanup, the compiled directories are gone.

## Adding a ninth target

If a new agent CLI ships tomorrow, extending the fan-out is a two-line change: add one `fct_copy_dir` call for commands and one for skills, both using `$compiled_commands_dir` / `$compiled_skills_dir` as the source. No change is needed anywhere else in the script.

The harder question is whether the new agent needs any custom transforms on top of the already-flat compiled directory. The current design bakes "every agent gets the same flat shape" into the fan-out; if a new agent needs a structure that differs from the other seven, either pre-process its input before calling `fct_copy_dir`, or consider whether that agent should use a separate compile step tailored to its needs.

## Related

- [[overview]]
- [[render-stage]]
- [[claude-code-flattening]]
- [[rsync-semantics]]
- [[troubleshooting]]
