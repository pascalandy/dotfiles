---
name: map-filesystem
metadata:
  author: Pascal Andy
---

## Mode: Refresh (batch)

When the user says "refresh" or wants to update multiple projects:

1. Run the refresh subcommand to get atlas directory paths:
   ```bash
   uv run ~/.config/opencode/skill/utils/map-filesystem/scripts/abstract_gen.py refresh
   ```
   This defaults to `~/Documents/github_local/executive-assistant`. Pass a custom path as argument if needed.

2. Capture the output — one absolute directory path per line.

3. For each path in the output, sequentially:
   - Announce: "Refreshing atlas for: `<path>`"
   - Read the skill instructions from `~/.config/opencode/skill/utils/map-filesystem/references/SKILL.md`
   - Execute those instructions with `<path>` as the working directory
   - If the skill fails for a path, log the error to the user and continue to the next path

4. After all paths are processed, summarize: N succeeded, M failed, list any failures.

Note: Use `--all` only if the user explicitly asks to process everything (resource-intensive).

## Mode: Single (default)

When no "refresh" is mentioned, execute the skill directly for the current directory:

Load and follow instructions from skill: `map-filesystem`
