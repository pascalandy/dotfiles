# map-filesystem — User Guide

## Commands

| What you want | Command |
|---------------|---------|
| Map the current directory | `/map-filesystem` |
| Map a specific path | `/map-filesystem map ~/path/to/folder` |
| Refresh all existing atlases | `/map-filesystem refresh` |
| Refresh a custom scan root | `/map-filesystem refresh ~/other/root` |
| Refresh everything (resource-intensive) | `/map-filesystem refresh --all` |

## Glossary

- **Map** — create or update `.abstract.md` + `.overview.md` in a directory
- **Refresh** — batch-update directories that already have both atlas files
- **Atlas** — the pair of `.abstract.md` (L0) + `.overview.md` (L1) that help AI agents navigate

## What happens when you run each command

### `/map-filesystem`

The agent scans the current directory, inspects key files, and writes/updates `.abstract.md` and `.overview.md` at the root.

### `/map-filesystem map ~/path/to/folder`

Same as above but targets a specific directory.

### `/map-filesystem refresh`

1. Scans `~/Documents/github_local/executive-assistant` for directories with existing atlases
2. Creates a todo item per directory
3. Spawns parallel sub-agents — each one refreshes one directory
4. Reports results: N succeeded, M failed

### `/map-filesystem refresh --all`

Same as refresh but scans the entire tree. Use sparingly — processes every directory with atlas files.

## CLI (for manual use)

The underlying script can also be run directly:

```bash
# List directories with both atlas files (default scan root)
uv run abstract_gen.py refresh

# Custom scan root
uv run abstract_gen.py refresh ~/other/path

# List ALL atlas directories
uv run abstract_gen.py refresh --all

# Scan and display atlas files
uv run abstract_gen.py scan ~/path

# Validate frontmatter
uv run abstract_gen.py validate ~/path

# Find directories missing atlases
uv run abstract_gen.py orphans ~/path
```

Run from: `~/.config/opencode/skill/utils/map-filesystem/scripts/`
