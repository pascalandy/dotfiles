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
2. **Per-agent shape differences.** Claude Code is *intended* to flatten `skills/meta/`, `skills/pa-sdlc/`, `skills/specs/`, and `skills/utils/` into one directory. Every other agent keeps the four-way split. Chezmoi cannot express either transform declaratively. (In practice the Claude Code flattening is broken in the current script — see [claude-code-flattening.md](claude-code-flattening.md).)
3. **Template rendering has to happen first.** The source tree contains `.tmpl` files, `dot_` prefixes, and possibly `private_`/`executable_` modifiers. Before the fan-out can copy anything, it needs a tree where those are resolved to applied names and contents.

The script solves all three by rendering the source through chezmoi into a scratch directory first, then rsyncing that rendered tree to eight specific destinations.

## Two-stage pipeline

### Stage 1: render

`fct_render_ai_templates` (`.chezmoiscripts/run_after_backup.sh:114`) runs `chezmoi archive --format tar` against the applied target path `~/.config/ai_templates` and pipes the tar stream into a `mktemp -d` scratch directory. The output is an applied-style tree where `dot_` is stripped, `.tmpl` files are rendered, and the result looks exactly like what would land under `~/` if chezmoi applied this subtree directly.

This render is scratch-only. A `trap` on the main function cleans up the temp directory on exit. See [render-stage.md](render-stage.md).

### Stage 2: rsync fan-out

`fct_sync_agent_assets` (`.chezmoiscripts/run_after_backup.sh:75`) takes the rendered `commands/` and `skills/` paths and calls `fct_copy_dir` once per agent home. Eight agent homes, each with their own path shape. See [fan-out-targets.md](fan-out-targets.md).

Every call defaults to `rsync -a --delete --delete-excluded --force`, so the rendered tree mirrors exactly — files removed from `dot_config/ai_templates/` disappear from every agent home on the next apply. See [rsync-semantics.md](rsync-semantics.md).

## What this implies

- **Never edit under an agent home.** Any file you drop into `~/.claude/skills/foo/` survives only until the next `chezmoi apply`, at which point the rsync `--delete` either overwrites it or removes it entirely.
- **`chezmoi apply` is no longer a plain copy.** It runs scripts that reach beyond its own source tree. Read `.chezmoiscripts/run_after_backup.sh` before trusting what a fresh apply will do on a new machine.
- **Claude Code only sees the `utils/` subtree today.** The four-call rsync pattern meant to flatten `meta/`, `pa-sdlc/`, `specs/`, and `utils/` into `~/.claude/skills/` wipes each previous call's output because of `--delete`. Only the last call (`utils/`) survives. A new `pa-sdlc` skill will ship to OpenCode, Pi, Codex, Amp, Agents, and Factory, but not to Claude Code. See [claude-code-flattening.md](claude-code-flattening.md) for the verification and three proposed fixes.

## Related

- [[render-stage]]
- [[fan-out-targets]]
- [[claude-code-flattening]]
- [[rsync-semantics]]
- [[troubleshooting]]
- [[how-to-configure-chezmoi]]
