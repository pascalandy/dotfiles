---
date: "2026-03-29"
tags:
  - structure
---
# Repository Topology

## What this is
The chezmoi source tree that manages personal dotfiles. Source lives in `~/.local/share/chezmoi/` and applies to `~/` via `chezmoi apply` (copies, not symlinks).

## What lives here
- **Top-level dotfiles**: `dot_zshrc`, `dot_gitconfig`, `dot_Brewfile`, `dot_bashrc` — classic shell and tool configuration
- **dot_config/**: Application configs including OpenCode (`dot_config/opencode/`) and shared AI templates (`dot_config/ai_templates/`)
- **dot_local/bin/**: Custom executable scripts (11 scripts for git operations, utilities, and helpers)
- **.chezmoiscripts/**: Pre-apply (`run_before_sync.sh`) and post-apply (`run_after_backup.sh`) automation
- **docs/**: Reference materials, archived patterns, and planning documents

## Boundaries
- **Source of truth**: Everything under `~/.local/share/chezmoi/`
- **Applied copies**: Everything under `~/` — these get overwritten on every `chezmoi apply`
- **Active surfaces**: `dot_config/opencode/`, `dot_config/ai_templates/commands/`, `dot_config/ai_templates/skills/`
- **Archived**: `docs/bienvenue_chez_moi/`, `dot_config/ai_templates/commands_archives/`, `dot_config/ai_templates/skills_archived/`

## Dependencies
- chezmoi CLI for apply/sync operations
- just (command runner) for workflow automation
- lefthook for pre-commit hooks
- GitHub Actions for CI (gitleaks, shellcheck, shfmt)

## Key details
- Files with `{{ .variable }}` MUST use `.tmpl` extension for template processing
- `dot_` prefix = file starts with `.` when applied; `executable_` = execute permission; `private_` = 600/700 permissions
- Run scripts execute automatically during `chezmoi apply` — `run_before_*` before, `run_after_*` after

## Related
- [[AI Tooling Surface]]
- [[Chezmoi Apply Automation]]
- [[Adding a New Dotfile]]
