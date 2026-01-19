# AGENTS.md - Chezmoi Dotfiles Repository

This file provides guidelines for AI coding agents working in this repository.

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

### Daily Operations

```bash
# Check status (what changed)
chezmoi status
chezmoi diff

# Apply changes (sync to home)
chezmoi apply -v

# Add a new file to management
chezmoi add ~/.newfile

# List all managed files
chezmoi managed
```

### Git Operations

```bash
# Commit and push (from this directory)
git add . && git commit -m "message" && git push
```

## User Preferences

### Custom Scripts Location

**Preference**: Store user scripts in `~/.local/bin/` (XDG-compliant standard location).

```bash
# Create a new script
vim ~/.local/bin/my-script

# Make executable and add to chezmoi
chmod +x ~/.local/bin/my-script
chezmoi add ~/.local/bin/my-script
```

Scripts are stored in chezmoi as: `dot_local/bin/executable_<scriptname>`

Ensure `~/.local/bin` is in PATH (add to `.zshrc` if needed):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

**Note**: Script names should NOT have `.sh` extension for cleaner CLI usage.

## Bash Script Standards

All bash scripts in this repo follow the template in:
`dot_config/opencode/skill/bash/scripts/pref_bash_script_template.sh`

### Required Conventions

```bash
#!/usr/bin/env bash
set -euo pipefail
```

### Naming Conventions

| Pattern | Example | Usage |
|---------|---------|-------|
| `fct_*` | `fct_parse_arguments()` | All functions |
| `log_*` | `log_info()`, `log_error()` | Logging functions |
| `UPPER_CASE` | `SCRIPT_VERSION` | Constants and env vars |
| `lower_case` | `local message` | Local variables |

### Logging

```bash
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_info "Starting process"
log_error "Something failed"
```

### Error Handling

```bash
die() {
    local message="${1:-Unknown error}"
    local exit_code="${2:-1}"
    log_error "${message}"
    exit "${exit_code}"
}
```

## File Structure

```
~/.local/share/chezmoi/
├── AGENTS.md                    # This file
├── README.md                    # User documentation
├── dot_zshrc                    # → ~/.zshrc
├── dot_gitconfig                # → ~/.gitconfig
├── dot_Brewfile                 # → ~/.Brewfile
├── dot_local/bin/               # → ~/.local/bin/ (user scripts)
├── dot_config/                  # → ~/.config/
├── private_dot_ssh/             # → ~/.ssh/ (private)
├── private_dot_gnupg/           # → ~/.gnupg/ (private)
├── run_before_sync.sh           # Pre-apply: sync VS Code, Brewfile
├── run_after_backup.sh          # Post-apply: backup external files
└── bienvenue_chez_moi/          # Archived configs (source: ~/Documents/github_local/Z_ARCHIVED/)
```

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
openrouter_api_key = "sk-or-v1-..."
```

## Testing Changes

```bash
# Preview what would change (dry run)
chezmoi diff

# Apply with verbose output
chezmoi apply -v

# Verify a specific file
chezmoi cat ~/.zshrc
```

## Run Scripts

This repo has two run scripts:

### `run_before_sync.sh`
- Syncs VS Code settings/keybindings to chezmoi source
- Updates VS Code extensions list
- Dumps Brewfile

### `run_after_backup.sh`
- Backs up external files to the repo
- Copies `bienvenue_chez_moi` directory

## Ignored Files

See `.chezmoiignore` for files excluded from chezmoi management:
- `.git/` directories
- `node_modules/`, `__pycache__/`
- Environment files (`.env*`)
- OS files (`.DS_Store`)

## Emergency Recovery

See `crash_procedure.md` for crash recovery procedures.

## External Resources

- Official docs: https://www.chezmoi.io/user-guide/command-overview/
- Repository: https://github.com/pascalandy/dotfiles
