---
name: Log
description: Append-only operational log for how-ai-templates-are-distributed
tags:
  - area/ea
  - kind/log
  - status/stable
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Log

- [[2026-04-11]] create | wiki | Wiki created. 6 reference pages authored from `.chezmoiscripts/run_after_backup.sh`.
- [[2026-04-11]] discovery | bug | While writing [[claude-code-flattening]], verified that the four `fct_copy_dir` calls into `~/.claude/skills/` each run with `--delete`, so only the last subtree (`utils/`) survives. `~/.claude/skills/` equals `dot_config/ai_templates/skills/utils/` exactly on this machine. Every `meta/`, `pa-sdlc/`, and `specs/` skill is invisible to Claude Code. Wiki documents current behavior and three fix options. Fix itself is out of scope for this documentation pass.
