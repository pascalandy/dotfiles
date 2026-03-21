# ORCHESTRATOR MEMORY

## Repo Summary

Chezmoi dotfiles repository managing configuration files across machines. Source: `~/.local/share/chezmoi/`, Target: `~/`. Syncs via `chezmoi apply` (copies, not symlinks). Contains classic dotfiles, AI tooling config (OpenCode, Pi, Claude, Codex, Gemini), and apply-time automation scripts.

## Architecture and Boundaries

- **Core dotfiles**: Shell configs (`dot_zshrc`, `dot_bashrc`), git, Brewfile, p10k
- **App config namespace**: `dot_config/` with subdirectories for opencode, ai_templates, bat, fish, ghostty, tmux, vscode, zed
- **AI surfaces**: `dot_config/opencode/` (runtime), `dot_config/ai_templates/` (shared commands/skills), `dot_pi/agent/` (Pi agent)
- **Local executables**: `dot_local/bin/` for custom scripts
- **Private/templated**: `private_dot_ssh/`, `private_dot_gnupg/`, `private_Library/`
- **Archived**: `bienvenue_chez_moi/`, `dot_config/ai_templates/commands_archives/`, `dot_config/ai_templates/skills_archived/`

## Entry Points and Important Paths

- **Main operator**: `justfile` - all workflows via `just` commands
- **Pre-apply hook**: `.chezmoiscripts/run_before_sync.sh` - syncs VS Code state back to repo
- **Post-apply hook**: `.chezmoiscripts/run_after_backup.sh` - distributes rendered AI assets to multiple agent homes
- **OpenCode config**: `dot_config/opencode/opencode.json.tmpl` (template entrypoint), `dot_config/opencode/config.json`
- **Template variables**: `~/.config/chezmoi/chezmoi.toml` defines secrets
- **Git hooks**: `lefthook.yml` wires staged gitleaks, shellcheck, shfmt

## Commands and Verification

- `just ci` - main local check: gitleaks + shellcheck + shfmt + chezmoi apply dry-run
- `just cm-status` / `just cm-diff` - drift inspection (excludes run scripts)
- `just cm-apply-dry` / `just cm-apply-verbose` - preview/apply
- `just cma` - actual `chezmoi apply`
- `lefthook install` - install pre-commit hooks
- CI (`.github/workflows/ci.yml`): runs gitleaks, shellcheck, shfmt on PR/push

## Conventions and Patterns

- **Chezmoi naming**: `dot_` (hidden), `private_` (restricted perms), `executable_` (+x), `symlink_`, `.tmpl` (template)
- **Run scripts**: `run_before_`, `run_after_`, `run_once_` prefixes in `.chezmoiscripts/`
- **Bash scripts**: `#!/usr/bin/env bash` + `set -euo pipefail`, `fct_*` functions, `log_*` logging, `UPPER_CASE` constants
- **Template pattern**: `dot_config/ai_templates/` is source-of-truth for multi-agent prompts/skills

## Fragile Areas and Risks

- **Source vs applied paths**: Never edit files in `~/` directly; always use chezmoi source or `chezmoi edit`
- **Template suffix**: Files with `{{ }}` MUST have `.tmpl` extension or raw placeholders leak
- **Apply side effects**: `chezmoi apply` triggers sync/render scripts - use `just cm-status`/`just cm-diff` for drift checks
- **Brewfile churn**: Mitigated by `SYNC_BREWFILE=false` in pre-sync script
- **Archived content**: Archived dirs look realistic but are not live workflow

## Decisions and Rationale

- Delegation policy: All meaningful repo work delegated to subagents immediately
- User scripts preference: Store in `~/.local/bin/` (XDG-compliant), no `.sh` extension
- Active AI surfaces: opencode, ai_templates/commands, ai_templates/skills, dot_pi/agent

## Active Work

- Atlas generation complete: `.abstract.md` and `.overview.md` created at repo root

## Recent Meaningful Changes

- OpenCode config iteration: GLM 5 as default agent, worker agent added, thinking mode enabled
- Command/script cleanup: removed obsolete scripts in `dot_local/bin/`
- Justfile updates: automation and local workflow refinements
- Documentation: atlas navigation maps refreshed

## Lessons Learned

- Use `just cm-diff` not raw `chezmoi apply` output to judge drift
- Pre-commit hooks via lefthook catch issues before CI
- Archived directories may contain realistic code but are reference-only
