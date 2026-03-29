---
date: "2026-03-29"
tags:
  - context
---
# Chezmoi Naming Conventions

Quick reference for chezmoi source file naming.

## Prefixes

| Prefix | Effect | Example |
|--------|--------|---------|
| `dot_` | File starts with `.` when applied | `dot_zshrc` → `.zshrc` |
| `private_` | Applied with 600 (file) or 700 (dir) permissions | `private_dot_ssh/` |
| `executable_` | Applied with execute permission | `executable_script` |
| `symlink_` | Creates a symlink | `symlink_dot_vimrc` |

## Suffixes

| Suffix | Effect | Example |
|--------|--------|---------|
| `.tmpl` | Processed as chezmoi template | `opencode.json.tmpl` |

## Run Scripts

| Prefix | When it runs |
|--------|--------------|
| `run_before_` | Before every `chezmoi apply` |
| `run_after_` | After every `chezmoi apply` |
| `run_once_` | Only on first `chezmoi apply` |

## Common patterns

- **Config files**: `dot_config/appname/config.json`
- **Scripts**: `dot_local/bin/executable_script-name`
- **Templates**: `dot_config/app/config.json.tmpl`
- **Private configs**: `private_dot_config/app/secrets.json`

## Related
- [[Repository Topology]]
- [[Adding a New Dotfile]]
