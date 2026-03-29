---
date: "2026-03-29"
tags:
  - structure
---
# AI Tooling Surface

## What this is
The active AI agent configuration and shared templates that get distributed to multiple agent homes during `chezmoi apply`.

## What lives here
- **dot_config/opencode/**: OpenCode runtime configuration
  - `opencode.json.tmpl` — main config with agent definitions and model routing
  - `AGENTS.md` — OpenCode-specific agent guidelines
  - `agent/` — agent prompt definitions
  - `plugin/` — OpenCode plugins
  - `skill/` — OpenCode-specific skills
  - `tools/` — MCP tool configurations

- **dot_config/ai_templates/**: Shared templates distributed to all agent homes
  - `commands/` — 34 slash commands for various operations
  - `skills/` — 9 active skills (ce:plan, ce:work, qa, browse, etc.)
  - `commands_archives/` — archived commands (reference only)
  - `skills_archived/` — archived skills (reference only)

## Boundaries
- **Active**: `commands/`, `skills/` — maintained and synced
- **Archived**: `commands_archives/`, `skills_archived/` — historical reference, do not edit
- **OpenCode-specific**: `dot_config/opencode/skill/` — only for OpenCode, not shared
- **Distribution target**: Claude, Codex, Gemini, Pi, and other agent homes under `~/`

## Dependencies
- `run_after_backup.sh` — renders templates and syncs to agent homes
- `run_before_sync.sh` — syncs VS Code settings and extensions back to source
- chezmoi templating for variable substitution (`{{ .variable }}`)

## Key details
- Shared assets use merge behavior — OpenCode-specific entries can coexist with shared ones
- Template rendering happens during `chezmoi apply` via the run_after script
- Skills follow a standard structure: `SKILL.md`, optional `scripts/`, `references/`

## Related
- [[Repository Topology]]
- [[Chezmoi Apply Automation]]
- [[Adding a New Skill]]
