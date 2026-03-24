# map-filesystem — User Guide

## Commands

| Goal | Command |
|------|---------|
| Map the current directory | `/map-filesystem` |
| Map a specific path | `/map-filesystem map ~/path/to/folder` |
| List all atlas directories | `/map-filesystem list` |
| List from a custom scan root | `/map-filesystem list ~/other/root` |
| List everything (heavy) | `/map-filesystem list --all` |
| Batch-update all listed dirs | `/map-filesystem batch` |

## Glossary

- **Map** — create or update `.abstract.md` + `.overview.md` in a directory
- **List** — show directories that already have both atlas files
- **Batch** — run map on every listed directory using parallel sub-agents
- **Atlas** — the pair of `.abstract.md` (L0) + `.overview.md` (L1) that help AI agents navigate

## What happens when you run each command

### `/map-filesystem`

The agent scans the current directory, inspects key files, and writes/updates `.abstract.md` and `.overview.md` at the root.

### `/map-filesystem map ~/path/to/folder`

Same as above but targets a specific directory.

### `/map-filesystem list`

Runs the CLI to discover directories with both atlas files under `~/Documents/github_local/executive-assistant`. Prints one path per line. No files are modified.

### `/map-filesystem batch`

1. Runs `list` to get all atlas directories
2. Creates a todo item per directory
3. Spawns parallel sub-agents — each one updates one directory
4. Reports results: N succeeded, M failed

### `/map-filesystem list --all`

Same as list but scans the entire tree. Use sparingly — may return many directories.

## CLI (for manual use)

The underlying script can also be run directly:

```bash
# List directories with both atlas files (default scan root)
uv run abstract_gen.py list

# Custom scan root
uv run abstract_gen.py list ~/other/path

# List ALL atlas directories
uv run abstract_gen.py list --all

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
