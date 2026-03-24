---
name: map-filesystem
metadata:
  author: Pascal Andy
---

## Mode: Refresh (batch)

When the user says "refresh" or wants to update multiple projects:

1. Run `uv run abstract_gen.py refresh [path]` to get list of atlas directories
   - Default path: `~/Documents/github_local/executive-assistant`
   - Use `--all` only if the user explicitly requests processing all projects
2. For each path in the output:
   - Announce: "Refreshing atlas for: <path>"
   - Execute the map-filesystem skill instructions with that path as the working directory
   - If the skill fails, log the error and continue to the next path
3. After all paths processed, summarize: N succeeded, M failed

## Mode: Single (default)

Execute instructions within the skill: `map-filesystem`
