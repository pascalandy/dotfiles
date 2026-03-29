---
date: "2026-03-29"
tags:
  - structure
---
# Chezmoi Apply Automation

## What this is
Two run scripts that execute automatically during `chezmoi apply`, handling bidirectional sync between source and runtime environments.

## What lives here
- **.chezmoiscripts/run_before_sync.sh**: Pre-apply automation
  - Syncs VS Code settings and keybindings from `~/` back to chezmoi source
  - Updates VS Code extensions list
  - Can dump Brewfile (currently disabled via `SYNC_BREWFILE=false`)

- **.chezmoiscripts/run_after_backup.sh**: Post-apply automation
  - Copies selected external backup files into the repo
  - Renders `dot_config/ai_templates/` through chezmoi
  - Syncs shared commands/skills to multiple agent homes (Claude, Codex, Gemini, Pi)
  - Uses merge behavior for OpenCode shared assets

## Boundaries
- **Pre-apply**: Only reads from `~/` and writes to chezmoi source — safe to run repeatedly
- **Post-apply**: Reads from chezmoi source and writes to `~/` and agent homes — has side effects
- **Trigger**: Both run automatically on every `chezmoi apply` (or `chezmoi apply -n` for dry-run)

## Dependencies
- chezmoi CLI for template rendering
- VS Code CLI for settings/extensions sync
- Standard Unix tools (rsync, cp, mkdir)

## Key details
- Run scripts show `R` in `chezmoi status` — this is normal, not drift
- Scripts use `run_before_` and `run_after_` prefixes (chezmoi v2.9+ convention)
- `run_once_` variant exists for first-time-only operations (not used here)

## Related
- [[Repository Topology]]
- [[AI Tooling Surface]]
- [[Testing Dotfile Changes]]
