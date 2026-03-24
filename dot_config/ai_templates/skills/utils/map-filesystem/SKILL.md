---
name: map-filesystem
description: >
  Use only when the user explicitly say "map-filesystem" to generate or update
  .abstract.md and .overview.md atlas files for repositories and knowledge folders.
  Also use when the user wants to list or batch-update multiple atlas directories.
---

# Map Filesystem

Generate or update `.abstract.md` and `.overview.md` files that help AI agents navigate repositories and knowledge folders.

## Quick reference

| Use case | CLI | AI command |
|----------|-----|------------|
| List atlas directories | `uv run abstract_gen.py list` | `/map-filesystem list` |
| List from custom root | `uv run abstract_gen.py list ~/other/root` | `/map-filesystem list ~/other/root` |
| List everything (heavy) | `uv run abstract_gen.py list --all` | `/map-filesystem list --all` |
| Map one directory | — | `/map-filesystem` |
| Map a specific path | — | `/map-filesystem map ~/path` |
| Batch-update all listed dirs | — | `/map-filesystem batch` |

Default: scans `executive-assistant` only. `--all` scans entire `~/Documents/github_local`.

## First step: learn the CLI

Before doing anything, run:

```bash
uv run ~/.config/opencode/skill/utils/map-filesystem/scripts/abstract_gen.py --help
```

This prints every available command, flag, and exit code. Treat its output as the source of truth for CLI usage.

For a specific subcommand, append `--help`:

```bash
uv run ~/.config/opencode/skill/utils/map-filesystem/scripts/abstract_gen.py list --help
```

## Single directory mode

Map one directory. This is the default when the user runs `/map-filesystem` without other keywords.

1. Determine the target path. If the user provides one, use it. Otherwise use the current working directory.
2. Read the atlas-builder guide: `references/atlas-builder-guide.md`
3. Follow that guide: scan the directory, classify the corpus, inspect key files, decide scope, write `.abstract.md` and `.overview.md`, validate.

## Batch mode

Update multiple directories that already have both atlas files. Triggered when the user says "batch" or "update all".

1. Get the list of directories:
   ```bash
   uv run ~/.config/opencode/skill/utils/map-filesystem/scripts/abstract_gen.py list
   ```
   Defaults to `executive-assistant` only. Use `--all` to scan the entire `~/Documents/github_local` tree. Pass a custom path as argument to override.

2. Create a todo item for each directory path. This gives the user visibility into progress.

3. Spawn one subagent per directory (Task tool, `subagent_type: "worker"`). They run in parallel — each directory is independent. Prompt each subagent with:

   ```
   Read the atlas-builder guide:
   ~/.config/opencode/skill/utils/map-filesystem/references/atlas-builder-guide.md

   Execute those instructions for: <path>
   Write or update .abstract.md and .overview.md in that directory.
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
