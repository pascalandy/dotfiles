# map-filesystem — User Guide

Two core commands: **list** and **update**. Both share the same scope logic.

`--all` expands scope from `executive-assistant` to entire `~/Documents/github_local`.

## Commands

| Command | AI | CLI |
|---------|-----|-----|
| **list** | | |
| List atlas dirs (executive-assistant) | `/map-filesystem list` | `uv run abstract_gen.py list` |
| List atlas dirs (all projects) | `/map-filesystem list --all` | `uv run abstract_gen.py list --all` |
| List atlas dirs (custom root) | `/map-filesystem list ~/path` | `uv run abstract_gen.py list ~/path` |
| **update** | | |
| Update atlas dirs (executive-assistant) | `/map-filesystem update` | — |
| Update atlas dirs (all projects) | `/map-filesystem update --all` | — |
| Update one specific directory | `/map-filesystem update ~/path` | — |

## Glossary

- **Update** — create or update `.abstract.md` + `.overview.md` in a directory
- **List** — show directories that already have both atlas files
- **`--all`** — expand scope from executive-assistant to all projects
- **Atlas** — the pair of `.abstract.md` (L0) + `.overview.md` (L1) that help AI agents navigate

## What happens

### `/map-filesystem list`

Prints directories with both atlas files. One path per line. No files are modified.

### `/map-filesystem update ~/path`

The agent reads the atlas-builder guide, scans the directory, inspects key files, and writes/updates `.abstract.md` and `.overview.md`.

### `/map-filesystem update`

1. Runs `list` to get atlas directories (executive-assistant only)
2. Creates a todo item per directory
3. Spawns parallel sub-agents — each one updates one directory
4. Reports results: N succeeded, M failed

### `/map-filesystem update --all`

Same but uses `list --all` to get all projects.

## CLI diagnostics

```bash
# Discover atlas files with filters and output formats
uv run abstract_gen.py scan ~/path

# Validate frontmatter consistency
uv run abstract_gen.py validate ~/path

# Find directories missing atlas files
uv run abstract_gen.py orphans ~/path

# List as JSON
uv run abstract_gen.py list --json
```

Run from: `~/.config/opencode/skill/utils/map-filesystem/scripts/`
