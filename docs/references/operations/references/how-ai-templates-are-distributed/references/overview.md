---
name: Fan-out Overview
description: Mental model for how `dot_config/ai_templates/` lands in every agent home on each chezmoi apply
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-ai-templates-are-distributed
---

This repo has one source of truth for AI agent prompts and skills: `dot_config/ai_templates/`. Every agent home you see on the filesystem (`~/.claude/skills/`, `~/.config/opencode/skills/`, `~/.pi/agent/skills/`, and five others) is a rebuilt copy. The pipeline that keeps those copies in sync with the source lives in `.chezmoiscripts/run_after_backup.sh` and runs on every `chezmoi apply`.

## Why a fan-out script instead of plain chezmoi

Chezmoi alone cannot solve this. Three constraints push the logic into a script:

1. **One source, many destinations.** Each agent CLI expects its own layout — Pi wants `~/.pi/agent/prompts/`, OpenCode wants `~/.config/opencode/commands/`, Claude wants `~/.claude/commands/`. Chezmoi can only materialize one target path per source path.
2. **Source-side category structure that must flatten before fan-out.** The source tree under `dot_config/ai_templates/skills/` is organized into `meta/`, `pa-sdlc/`, `specs/`, `utils/`. Agents do not load skills from nested category subtrees — they expect a flat `skills/<name>/` layout. The fan-out has to flatten the four subtrees before any agent home can use them.
3. **Template rendering has to happen first.** The source tree contains `.tmpl` files, `dot_` prefixes, and possibly `private_`/`executable_` modifiers. Before anything else can run, the script needs a tree where those are resolved to applied names and contents.

The script solves all three with a three-stage pipeline: render, compile, rsync.

## Three-stage pipeline

### Stage 1: render

`fct_render_ai_templates` at `.chezmoiscripts/run_after_backup.sh:152-161` runs `chezmoi archive --format tar` against the applied target path `~/.config/ai_templates` and pipes the tar stream into a `mktemp -d` scratch directory. The output is an applied-style tree where `dot_` is stripped, `.tmpl` files are rendered, and the result looks exactly like what would land under `~/` if chezmoi applied this subtree directly.

This render is scratch-only. A `trap` in `fct_main` cleans up the temp directory on exit. See [render-stage.md](render-stage.md).

### Stage 2: compile

`fct_compile_assets` at `.chezmoiscripts/run_after_backup.sh:75-102` takes the rendered `commands/` and `skills/` subpaths and produces flat compile directories. For skills, it loops over the four category subtrees (`meta`, `pa-sdlc`, `specs`, `utils`) and uses additive `cp -r` to merge their contents into one directory. For commands (which are already flat in the source), it falls into a flat branch that just copies everything across.

The compile step is what makes the fan-out work — the subtree category split exists only in the source, and it is erased before anything leaves the script. See [claude-code-flattening.md](claude-code-flattening.md) for the full compile mechanic and the naming-collision gotcha that survives flattening.

### Stage 3: rsync fan-out

`fct_sync_agent_assets` at `.chezmoiscripts/run_after_backup.sh:104-150` takes the compiled commands and skills directories and calls `fct_copy_dir` exactly twice per agent — once for commands, once for skills. Eight agent homes, so sixteen `fct_copy_dir` calls per apply. Every call uses `sync_mode=delete`, which expands to `rsync -a --delete --delete-excluded --force`, so each destination is reconstructed to exactly match the compiled source. See [fan-out-targets.md](fan-out-targets.md) for the per-agent table and [rsync-semantics.md](rsync-semantics.md) for what the flag set means.

After the sixteen calls complete, `fct_sync_agent_assets` removes both compile scratch directories with `rm -rf` at `.chezmoiscripts/run_after_backup.sh:149`. The render-stage scratch directory is cleaned up separately by the `trap` in `fct_main`.

## What this implies

- **Never edit under an agent home.** Any file you drop into `~/.claude/skills/foo/` survives only until the next `chezmoi apply`, at which point the rsync `--delete` either overwrites it or removes it entirely.
- **`chezmoi apply` is no longer a plain copy.** It runs scripts that reach beyond its own source tree. Read `.chezmoiscripts/run_after_backup.sh` before trusting what a fresh apply will do on a new machine.
- **The source-tree category split (`meta/`, `pa-sdlc/`, `specs/`, `utils/`) is not visible to any agent.** Skills from all four categories land as flat peers under every agent's `skills/` directory. This means a new skill in `pa-sdlc/foo/` cannot have the same name as a skill in `utils/foo/` — the compile step's `cp -r` silently picks whichever category runs last. See [claude-code-flattening.md](claude-code-flattening.md).
- **Gemini now receives skills.** Earlier versions of the script sent only commands to Gemini. Under the current design, Gemini's `~/.gemini/skills/` gets the same compiled skills directory every other agent gets.

## Related

- [[render-stage]]
- [[fan-out-targets]]
- [[claude-code-flattening]]
- [[rsync-semantics]]
- [[troubleshooting]]
- [[how-to-configure-chezmoi]]
