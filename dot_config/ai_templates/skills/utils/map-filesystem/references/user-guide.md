# map-filesystem — User Guide

## Commands

| Use case | CLI | AI command |
|----------|-----|------------|
| List atlas directories | `uv run abstract_gen.py list` | `/map-filesystem list` |
| List ALL projects | `uv run abstract_gen.py list --all` | `/map-filesystem list --all` |
| Update current directory | — | `/map-filesystem` |
| Update a specific path | — | `/map-filesystem ~/path` |
| Update all listed dirs | — | `/map-filesystem update` |
| Update ALL projects | — | `/map-filesystem update --all` |

`--all` expands scope from `executive-assistant` to entire `~/Documents/github_local`.

## Glossary

- **Update** — create or update `.abstract.md` + `.overview.md` in a directory
- **List** — show directories that already have both atlas files
- **`--all`** — expand scope from executive-assistant to all projects
- **Atlas** — the pair of `.abstract.md` (L0) + `.overview.md` (L1) that help AI agents navigate

## What happens when you run each command

### `/map-filesystem`

The agent scans the current directory, inspects key files, and writes/updates `.abstract.md` and `.overview.md` at the root.

### `/map-filesystem ~/path/to/folder`

Same as above but targets a specific directory.

### `/map-filesystem list`

Lists directories with both atlas files under `executive-assistant`. One path per line. No files are modified.

### `/map-filesystem list --all`

Same but scans entire `~/Documents/github_local`. May return many directories.

### `/map-filesystem update`

1. Runs `list` to get atlas directories (executive-assistant only)
2. Creates a todo item per directory
3. Spawns parallel sub-agents — each one updates one directory
4. Reports results: N succeeded, M failed

### `/map-filesystem update --all`

Same but uses `list --all` to get all projects.

## CLI (for manual use)

```bash
# List directories with both atlas files (executive-assistant only)
uv run abstract_gen.py list

# List ALL projects
uv run abstract_gen.py list --all

# Custom scan root
uv run abstract_gen.py list ~/other/path

# JSON output
uv run abstract_gen.py list --json

# Scan and display atlas files
uv run abstract_gen.py scan ~/path

# Validate frontmatter
uv run abstract_gen.py validate ~/path

# Find directories missing atlases
uv run abstract_gen.py orphans ~/path
```

Run from: `~/.config/opencode/skill/utils/map-filesystem/scripts/`
