---
date: "2026-03-29"
tags:
  - context
---
# Source vs Applied Paths

The most common mistake in this repository: editing files under `~/` instead of chezmoi source.

## The two-path problem

Every managed file has two locations:

| Location | Path | Purpose |
|----------|------|---------|
| **Source** | `~/.local/share/chezmoi/` | Authoritative — edit here |
| **Applied** | `~/` (home directory) | Runtime copy — gets overwritten |

## Common path translations

| Applied path (WRONG to edit) | Source path (CORRECT to edit) |
|------------------------------|-------------------------------|
| `~/.zshrc` | `~/.local/share/chezmoi/dot_zshrc` |
| `~/.gitconfig` | `~/.local/share/chezmoi/dot_gitconfig` |
| `~/.config/opencode/opencode.json` | `~/.local/share/chezmoi/dot_config/opencode/opencode.json.tmpl` |
| `~/.config/opencode/skill/...` | `~/.local/share/chezmoi/dot_config/ai_templates/skills/...` |
| `~/.local/bin/my-script` | `~/.local/share/chezmoi/dot_local/bin/executable_my-script` |

## How to check if a file is managed

```bash
chezmoi managed | grep <filename>
```

If it appears, edit the source. If not, you can edit directly or add it to chezmoi.

## Workflow

1. Always edit in `~/.local/share/chezmoi/`
2. Run `chezmoi apply` to sync to `~/`
3. Never edit directly in `~/.config/`, `~/.local/bin/`, etc.

## Related
- [[Repository Topology]]
- [[Adding a New Dotfile]]
- [[Testing Dotfile Changes]]
