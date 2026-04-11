---
name: Log
description: Append-only operational log for how-vscode-and-brewfile-sync-back
tags:
  - area/ea
  - kind/log
  - status/stable
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Log

- [[2026-04-11]] create | wiki | Wiki created. 2 reference pages authored from `.chezmoiscripts/run_before_sync.sh`. Documents VS Code three-file diff-gated copy and the Brewfile 72h rate-limited dump.
- [[2026-04-11]] note | brewfile | Documented that `SYNC_BREWFILE=true` in the current source (`.chezmoiscripts/run_before_sync.sh:35`), which contradicts the AGENTS.md claim of "currently disabled by default". The 72-hour rate limit makes the practical sync cadence much lower than every-apply, which is likely the source of the "disabled" description.
