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
   Use `--all` only if the user explicitly asks to process everything (resource-intensive).

2. Capture the output — one absolute directory path per line.

3. Create a todo list with one item per directory path. This gives the user visibility into progress.

4. For each path, spawn a subagent (using the Task tool with `subagent_type: "worker"`) with this prompt:

   ```
   Read the skill instructions from ~/.config/opencode/skill/utils/map-filesystem/references/SKILL.md
   then execute those instructions for this directory: <path>
   Write or update the .abstract.md and .overview.md files in that directory.
   Return a short summary of what you generated or updated.
   ```

   Spawn subagents in parallel — they work on independent directories with no shared state.

5. As each subagent completes, mark its todo as completed. If one fails, mark it as cancelled and note the error.

6. After all subagents finish, summarize: N succeeded, M failed, list any failures.

## Mode: Single (default)

When no "refresh" is mentioned, execute the skill directly for the current directory:

Load and follow instructions from skill: `map-filesystem`
