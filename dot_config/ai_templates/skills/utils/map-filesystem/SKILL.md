---
name: map-filesystem
description: >
  Generate or refresh .abstract.md and .overview.md atlas files for repositories
  and knowledge folders. Use when the user says "map this folder", "map filesystem",
  "generate atlas", "refresh atlas", "create .abstract.md", "create .overview.md",
  or wants to build a lightweight navigation system for AI agents to find files faster.
  Also use when the user wants to batch-refresh multiple atlas directories.
---

# Map Filesystem

Generate or refresh a lightweight navigation system (atlas) for AI agents.

The atlas has three layers:
- **L0** = `.abstract.md` — fast relevance check
- **L1** = `.overview.md` — navigation map + retrieval guide
- **L2** = original source files — source of truth

## Quick Reference (for the human)

| What you want | Command |
|---------------|---------|
| Map the current directory | `/map-filesystem` |
| Map a specific path | `/map-filesystem map ~/path/to/folder` |
| Refresh all existing atlases | `/map-filesystem refresh` |
| Refresh a custom scan root | `/map-filesystem refresh ~/other/root` |
| Refresh everything (resource-intensive) | `/map-filesystem refresh --all` |

"Map" = create or update `.abstract.md` + `.overview.md` in a directory.
"Refresh" = batch-update directories that already have both atlas files.

## Modes

### Single directory (default)

When the user says nothing specific or provides a path to map, read the full atlas-builder guide and follow it:

```
references/atlas-builder-guide.md
```

That reference contains the complete workflow: scan, classify, inspect, decide scope, write atlas files, validate.

If the user provides a path (e.g., `/map-filesystem map ~/some/folder`), use that path as the working directory. Otherwise use the current working directory.

### Batch refresh

When the user says "refresh" or wants to update multiple projects:

1. Run the refresh subcommand to get atlas directory paths:
   ```bash
   uv run ~/.config/opencode/skill/utils/map-filesystem/scripts/abstract_gen.py refresh
   ```
   Default scan path: `~/Documents/github_local/executive-assistant`.
   Pass a custom path as argument if needed.
   Use `--all` only if the user explicitly asks to process everything (resource-intensive).

2. Create a todo list with one item per directory path for progress visibility.

3. For each path, spawn a subagent (Task tool, `subagent_type: "worker"`) with this prompt:

   ```
   Read the atlas-builder guide from:
   ~/.config/opencode/skill/utils/map-filesystem/references/atlas-builder-guide.md

   Execute those instructions for this directory: <path>
   Write or update the .abstract.md and .overview.md files in that directory.
   Return a short summary of what you generated or updated.
   ```

   Spawn subagents in parallel — they work on independent directories with no shared state.

4. As each subagent completes, mark its todo as completed. If one fails, mark as cancelled with the error.

5. Summarize: N succeeded, M failed, list any failures.

## Scripts

The `scripts/` directory contains `abstract_gen.py`, a CLI for discovering, validating, and exporting atlas files. See `references/README.md` for full usage.

Key subcommands:
- `scan` — discover atlas files with filters and output formats
- `validate` — check frontmatter consistency
- `orphans` — find directories missing expected atlas files
- `refresh` — list directories with both atlas files for batch refresh
