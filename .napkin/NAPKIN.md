# Chezmoi Dotfiles Repository

## What is this
Personal dotfiles managed by chezmoi, combining classic shell/Git config with a substantial AI tooling surface. Source lives in `~/.local/share/chezmoi/` and applies to `~/` via `chezmoi apply`.

## Structure
- **Top-level dotfiles**: `dot_zshrc`, `dot_gitconfig`, `dot_Brewfile` — classic workstation config
- **dot_config/**: Application configs including OpenCode runtime and shared AI templates
- **dot_local/bin/**: Custom executable scripts managed through chezmoi
- **.chezmoiscripts/**: Pre/post-apply automation with side effects
- **docs/**: Reference materials and archived patterns

## Key conventions
- **NEVER edit files under `~/` directly** — always edit chezmoi source and run `chezmoi apply`
- Files with `{{ .variable }}` MUST use `.tmpl` extension for chezmoi template processing
- `dot_` prefix = file starts with `.` when applied; `executable_` = execute permission; `private_` = 600/700 permissions
- AI templates in `dot_config/ai_templates/` are synced to multiple agent homes via `run_after_backup.sh`

## Current state
Stable — active maintenance on OpenCode config and AI template distribution. No blocked items.

## Atlas guide
- `napkin overview` — map of this atlas with keywords
- `napkin search "<topic>"` — find specific knowledge
- `napkin read "<entry>"` — read a full map entry
