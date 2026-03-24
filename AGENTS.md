# AGENTS.md - Chezmoi Dotfiles Repository

This file provides guidelines for AI coding agents working in this repository.

## File Structure

Read the atlas files for navigation context:
1. `.abstract.md` — fast relevance check (what this repo is for)
2. `.overview.md` — navigation map + retrieval routes

## Repository Overview

This is a **chezmoi dotfiles repository** that manages configuration files across machines.
- **Source directory**: `~/.local/share/chezmoi/`
- **Target directory**: `~/` (home directory)
- **Repository**: https://github.com/pascalandy/dotfiles

Chezmoi stores desired state here and syncs to home via `chezmoi apply` (copies, not symlinks).

## Critical Rules

### Never Edit Target Files Directly

Files in `~/` that are managed by chezmoi should NEVER be edited directly.
Always edit the source in `~/.local/share/chezmoi/` or use `chezmoi edit`.

```bash
# Check if a file is managed
chezmoi managed | grep <filename>

# Edit via chezmoi (opens source file)
chezmoi edit ~/.zshrc
```

### Chezmoi Naming Conventions

| Prefix/Suffix | Meaning |
|---------------|---------|
| `dot_` | File starts with `.` (e.g., `dot_zshrc` → `.zshrc`) |
| `private_` | Applied with `600`/`700` permissions (still visible in git) |
| `executable_` | Applied with execute permission |
| `symlink_` | Creates a symlink |
| `.tmpl` | Template file (processes `{{ }}` variables) |
| `run_before_` | Script runs before apply |
| `run_after_` | Script runs after every apply |
| `run_once_` | Script runs only on first apply |

## Commands Reference

load skill `chezmoi`

## User Preferences

### Custom Scripts Location

**Preference**: Store user scripts in `~/.local/bin/` (XDG-compliant standard location).

```bash
# Create a new script
code ~/.local/bin/[script-name]

# Make executable and add to chezmoi
chmod +x ~/.local/bin/[script-name]
chezmoi add ~/.local/bin/[script-name]
```

Scripts are stored in chezmoi as: `dot_local/bin/executable_[script-name]`

Ensure `~/.local/bin` is in PATH (add to `.zshrc` if needed):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Note**: Script names should NOT have `.sh` extension for cleaner CLI usage.

## Bash Script Standards

if needed, load skill `bash`

## Source vs Applied Paths

Many AI-related files have two path forms:

- source-tree paths in this repo, for example `dot_config/opencode/plugin/`
- applied runtime paths under `~/.config/...`, for example `~/.config/opencode/plugin/`

When documenting or editing behavior, verify whether the source of truth is the
chezmoi source path or the applied runtime path. Do not edit the applied file
directly if chezmoi manages it.

## Templates and Secrets

Files containing `{{ .variable }}` MUST have `.tmpl` extension:

```bash
# Wrong: Variables won't be processed
opencode.json

# Correct: chezmoi processes templates
opencode.json.tmpl
```

Define variables in `~/.config/chezmoi/chezmoi.toml`:
```toml
[data]
openrouter_api_key = "sk-or-v1-.."
```

## Testing Changes

```bash
# Run the main local checks
just ci

# Preview what would change (dry run)
just cm-apply-dry

# Apply with verbose output
just cm-apply-verbose

# Verify a specific file
chezmoi cat ~/.zshrc
```

Pre-commit hooks run staged `gitleaks`, `shellcheck`, and `shfmt` via
`lefthook`. GitHub Actions currently runs repository-wide `gitleaks`,
`shellcheck`, and `shfmt`.

## Run Scripts

This repo has two run scripts located in `.chezmoiscripts/` (chezmoi v2.9+ convention):

### `.chezmoiscripts/run_before_sync.sh`
- Syncs VS Code settings/keybindings to chezmoi source
- Updates VS Code extensions list
- Can dump the Brewfile, but that path is currently disabled by default via `SYNC_BREWFILE=false`

### `.chezmoiscripts/run_after_backup.sh`
- Copies selected external backup files into the repo
- Renders `dot_config/ai_templates/` through chezmoi and syncs shared commands/skills to multiple agent homes
- Uses merge behavior for OpenCode shared assets so OpenCode-specific entries can stay managed separately

