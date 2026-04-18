---
name: Log
description: Append-only operational log for how-ai-templates-are-distributed
tags:
  - area/ea
  - kind/log
  - status/stable
date_created: 2026-04-11
date_updated: 2026-04-18
---

# Log

- [[2026-04-18]] lint | recursive update | refreshed local index and direct child wiki routes
- [[2026-04-11]] create | wiki | Wiki created. 6 reference pages authored from `.chezmoiscripts/run_after_backup.sh`.
- [[2026-04-11]] discovery | bug | While writing [[claude-code-flattening]], verified that the four `fct_copy_dir` calls into `~/.claude/skills/` each ran with `--delete`, so only the last subtree (`utils/`) survived. `~/.claude/skills/` equaled `dot_config/ai_templates/skills/utils/` exactly on this machine. Every `meta/`, `pa-sdlc/`, and `specs/` skill was invisible to Claude Code.
- [[2026-04-11]] fix-landed | refactor | Commit `b6d0042` refactored `.chezmoiscripts/run_after_backup.sh` to introduce `fct_compile_assets` — a pre-compile-then-single-rsync pattern. The four-call pattern is gone. Every agent home now receives the same flat compiled skills directory. The `utils/`-only bug is fixed and the flattening is uniform.
- [[2026-04-11]] rewrite | drift-refresh | Rewrote [[claude-code-flattening]], [[overview]], [[fan-out-targets]], [[rsync-semantics]], and [[render-stage]] to describe the post-`b6d0042` script. Updated [[troubleshooting]] and the wiki's INDEX to match. The historical bug is preserved as a short closing section in [[claude-code-flattening]]. The old "Claude Code only" framing is gone.
