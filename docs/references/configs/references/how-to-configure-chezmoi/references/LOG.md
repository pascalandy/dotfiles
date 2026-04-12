---
name: Log
description: Append-only operational log for How to Configure Chezmoi
tags:
  - area/ea
  - kind/log
  - status/stable
date_created: 2026-04-11
date_updated: 2026-04-11
---


# Log

- [[2026-04-11]] create | wiki | Wiki created by absorbing content from `dot_config/ai_templates/skills/utils/chezmoi/`. 7 reference pages seeded.
- [[2026-04-11]] retire | skill | Deleted `dot_config/ai_templates/skills/utils/chezmoi/` after cross-check confirmed this wiki is a strict superset. `apply_chezmoi.sh` helper dropped (redundant wrapper around `chezmoi apply -v`). `AGENTS.md` "Commands Reference" now points here instead of `load skill chezmoi`. Applied copies under `~/.config/*/skills/utils/chezmoi`, `~/.claude/skills/chezmoi`, `~/.codex/skills/...`, `~/.pi/agent/skills/...`, `~/.factory/skills/...` cleaned by `chezmoi apply -v` (rsync `--delete` in `run_after_backup.sh`); stale targets under `~/.config/ai_templates/skills/utils/chezmoi` and `~/.config/ai_templates/TMP_skills/utils/chezmoi` trashed manually (source tree has no `exact_` prefix).
