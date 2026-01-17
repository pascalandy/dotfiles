# 🚨 CRASH RECOVERY PROCEDURE

---

## First Steps (DO THIS FIRST)

```bash
# Check chezmoi status
chezmoi doctor

# Apply current state
chezmoi apply

# Check what would change
chezmoi diff
```

If something is broken, start here. chezmoi will show you what's wrong.

---

## How This System Works

**Core Concept**: chezmoi stores the *desired state* of your system in `~/.local/share/chezmoi` and copies (not symlinks) files to your home directory on `chezmoi apply`.

**Source of Truth**: https://github.com/pascalandy/dotfiles

**Your Working Directory**: `~/.local/share/chezmoi` (this is chezmoi's state, edit files here)

**Applied Files**: `~/.*` (this is what your system actually uses)

---

## Daily Workflow

```bash
# 1. Edit configuration
chezmoi edit ~/.zshrc  # Opens in VS Code (alias: cfgzsh)
chezmoi edit ~/.config/opencode/config.json  # (alias: cfgoc)

# 2. Apply changes
chezmoi apply

# 3. Commit to remote repo
chezmoi cd && git add . && git commit -m "your message" && git push
```

---

## Add New Files

```bash
chezmoi add ~/.file
chezmoi apply
chezmoi cd && git add . && git commit && git push
```

---

## Templates for Secrets

**CRITICAL**: Any file with `{{ variable }}` must end in `.tmpl`

**Example** (`dot_config/opencode/opencode.json.tmpl`):
```json
"apiKey": "{{ .openrouter_api_key }}"
```

**Define secret** in `~/.config/chezmoi/chezmoi.toml`:
```toml
[data]
openrouter_api_key = "sk-or-v1-..."
```

**Then**: `chezmoi apply` renders the template and replaces `{{ .openrouter_api_key }}` with the actual key.

---

## ⚠️ Common Issues

### Issue: "No cookie auth credentials found" in opencode

**Cause**: Template file named `opencode.json` instead of `opencode.json.tmpl`

**Fix**:
```bash
chezmoi cd
mv opencode.json opencode.json.tmpl
chezmoi apply
```

**Lesson**: If you see `{{ variable }}` literally in your actual config file, it's not a template. Rename it.

### Issue: Infinite loop with Brewfile

**Cause**: Dumping Brewfile to chezmoi source directory triggers apply → dump loop

**Fix**: Use `run_before_sync.sh` for pre-sync operations, `run_after_backup.sh` for post-sync backups

---

## Automation Scripts

Scripts live in chezmoi source and run automatically on `chezmoi apply`:

- `run_before_sync.sh` - Runs BEFORE applying changes
- `run_after_backup.sh` - Runs AFTER applying changes
- `run_once_*.sh` - Runs only once ever (first apply)

**Make executable**: `chmod +x script_name.sh`

---

## What You've Been Working On (Recent)

**Last week intensive work**:

1. **tmux** - Enhanced with mouse support, smart shell readiness detection
2. **VS Code** - Added config management
3. **amp** - Background update commands
4. **opencode** - docus-docs MCP configuration, glm model v4.7
5. **universal run() function** - Enhanced to find Python or Bash scripts anywhere
6. **mgrep tool** - Semantic file searching (added, then removed)

**Latest improvements**:
- Split chezmoi scripts into `run_before` and `run_after`
- Prevented infinite loop with Brewfile dumps
- Fixed zsh array indexing (1-indexed)

---

## Recovery Procedure

If your system is messed up:

```bash
# 1. See what chezmoi would change
chezmoi diff

# 2. If safe, apply
chezmoi apply

# 3. If not safe, investigate specific files
chezmoi edit ~/.file

# 4. Check templates
chezmoi doctor

# 5. Sync from remote if needed
chezmoi cd && git pull origin main
chezmoi apply
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `chezmoi apply` | Apply all changes to home directory |
| `chezmoi diff` | Show what would change |
| `chezmoi doctor` | Check system status |
| `chezmoi edit ~/.file` | Edit file in chezmoi source |
| `chezmoi add ~/.file` | Add file to chezmoi management |
| `chezmoi cd` | Go to chezmoi source directory |
| `cfgzsh` | Edit ~/.zshrc (alias) |
| `cfgoc` | Edit opencode config (alias) |

---

## Official Documentation

The truth is here: https://www.chezmoi.io/user-guide/command-overview/

**Last updated**: 2025-12-23
