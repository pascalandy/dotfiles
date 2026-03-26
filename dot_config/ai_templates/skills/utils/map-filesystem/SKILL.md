---
name: map-filesystem
description: >
  Use only when the user explicitly say "map-filesystem" to generate or update
  .abstract.md and .overview.md atlas files for repositories and knowledge folders.
  Also use when the user wants to list or update multiple atlas directories.
---

# Map Filesystem

Generate or update `.abstract.md` and `.overview.md` files that help AI agents navigate repositories and knowledge folders.

## Quick reference

Two core commands: `list` and `update`. Both share the same scope logic.

| Command | AI harness | CLI |
|---------|-----|-----|
| **list** | | |
| List atlas dirs (executive-assistant) | `/map-filesystem list` | `uv run abstract_gen.py list` |
| List atlas dirs (all projects) | `/map-filesystem list all` | `uv run abstract_gen.py list --all` |
| List atlas dirs (custom root) | `/map-filesystem list ~/path` | `uv run abstract_gen.py list ~/path` |
| **update** | | |
| Update atlas dirs (executive-assistant) | `/map-filesystem update` | — |
| Update atlas dirs (all projects) | `/map-filesystem update all` | — |
| Update one specific directory | `/map-filesystem update ~/path` | — |

`all` expands scope from `executive-assistant` to entire `~/Documents/github_local`.

**CLI-only diagnostics:**

| Command | What it does |
|---------|-------------|
| `uv run abstract_gen.py scan ~/path` | Discover atlas files with filters and output formats |
| `uv run abstract_gen.py validate ~/path` | Check frontmatter consistency |
| `uv run abstract_gen.py orphans ~/path` | Find directories missing atlas files |

## First step: learn the CLI

Before doing anything, run:

```bash
uv run ~/.config/opencode/skill/utils/map-filesystem/scripts/abstract_gen.py --help
```

Treat its output as the source of truth for CLI usage. For a specific subcommand, append `--help`.

## Update single directory

When the user runs `/map-filesystem update ~/path`:

1. Read the atlas-builder guide: `references/atlas-builder-guide.md`
2. Follow that guide for the given path: scan, classify, inspect, decide scope, write `.abstract.md` and `.overview.md`, validate.
3. **AGENTS.md check:** If this is a top-level atlas (`scope: top`) and `AGENTS.md` exists in the target directory, verify the `## Entrypoint` section exists word for word per the atlas-builder guide. Add it if missing. Do not modify anything else in `AGENTS.md`.
4. **Wiring check:** If child atlases exist, verify they appear in the parent's Reference Tree. If creating a child, update the parent's Reference Tree to include it.

## Update multiple directories

When the user runs `/map-filesystem update` or `/map-filesystem update all`:

1. Get the list of directories:
   ```bash
   uv run ~/.config/opencode/skill/utils/map-filesystem/scripts/abstract_gen.py list
   ```
   Add `--all` if the user requested it. Pass a custom path as argument to override the default root.

2. Create a todo item for each directory path. This gives the user visibility into progress.

3. Spawn one subagent per directory (Task tool, `subagent_type: "worker"`). They run in parallel — each directory is independent. Prompt each subagent with:

    ```
    Read the atlas-builder guide:
    ~/.config/opencode/skill/utils/map-filesystem/references/atlas-builder-guide.md

    Execute those instructions for: <path>
    Write or update .abstract.md and .overview.md in that directory.
    If this is a top-level atlas (scope: top) and AGENTS.md exists, verify the
    ## Entrypoint section exists per the guide. Add if missing, touch nothing else.
    If child atlases exist, verify wiring in the parent Reference Tree.
    Return a short summary of what changed.
    ```

4. Mark each todo complete or cancelled as subagents finish.

5. Summarize results: N succeeded, M failed, list failures.

## References

| File | Contents |
|------|----------|
| `references/atlas-builder-guide.md` | Full instructions for writing atlas files |
| `references/user-guide.md` | Human-readable command reference |
| `references/README.md` | `abstract_gen.py` architecture and output formats |
