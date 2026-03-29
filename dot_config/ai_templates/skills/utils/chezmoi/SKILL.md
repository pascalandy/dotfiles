---
name: chezmoi
description: Manage dotfiles via chezmoi CLI. Use when reading, modifying, or adding config files (dotfiles) in user's home directory. Ensures edits happen in chezmoi source (~/.local/share/chezmoi) and apply correctly.
---

# Chezmoi Skill

Manage dotfiles using chezmoi. All edits MUST happen in the chezmoi source directory (`~/.local/share/chezmoi/`), never directly under `~/`.

## Critical Rule

**Never edit files under home directory.** Files under `~/` and `~/.config/` are applied copies. Always edit the chezmoi source, then apply.

```bash
# Step 1: Check if managed
chezmoi managed | grep <filename>

# Step 2: Edit the source (translates path automatically)
chezmoi edit ~/.zshrc

# Step 3: Apply changes to home
chezmoi apply -v
```

## Core Workflow

### Identify a dotfile

```bash
chezmoi managed | grep <filename>
```

### Edit a managed file

```bash
chezmoi edit ~/.zshrc
```

Opens the source file (e.g., `~/.local/share/chezmoi/dot_zshrc`).

### Apply changes

```bash
chezmoi apply -v
```

### Add a new file

```bash
chezmoi add ~/.new_config
```

## Common Commands

| Command | Purpose |
|---------|---------|
| `chezmoi status` | Show file states (modified, pending) |
| `chezmoi diff` | Diff between source and target |
| `chezmoi cd` | Shell into the source directory |
| `chezmoi managed` | List all managed files |
| `chezmoi data` | Show available template variables |

## Naming Conventions

| Prefix/Suffix | Meaning |
|---------------|---------|
| `dot_` | File starts with `.` (e.g., `dot_zshrc` -> `.zshrc`) |
| `private_` | Applied with `600`/`700` permissions |
| `executable_` | Applied with execute permission |
| `symlink_` | Creates a symlink |
| `.tmpl` | Template file (processes `{{ }}` variables) |

## References

| Document | Path | Content |
|----------|------|---------|
| **CLI Reference** | [references/cli_reference.md](references/cli_reference.md) | Full command table, naming conventions, template syntax |
| **Secrets Management** | [references/secrets.md](references/secrets.md) | Keyring integration, API keys, alternative backends, best practices, .env migration |
| **Source** | [references/source.md](references/source.md) | External links and upstream documentation |

## Scripts

| Script | Path | Purpose |
|--------|------|---------|
| **Apply** | [scripts/apply_chezmoi.sh](scripts/apply_chezmoi.sh) | Runs `chezmoi apply -v` with logging, strict mode, and dependency checks |
