---
name: Log
description: Append-only operational log for distill
tags:
  - area/ea
  - kind/log
  - status/stable
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Log

- [[2026-04-11]] create | wiki | Wiki map created. 6 pages seeded: INDEX + overview, providers-and-effort, output-layout, prompts-library, troubleshooting.
- [[2026-04-11]] note | providers-and-effort | Claude `--effort` ETL fixed: canonical `medium` now maps to vendor `medium` (was stale `med` which upstream claude CLI rejected). `DEFAULT_EFFORT` bumped from `medium` to `high` for claude/codex. Sonnet special-case to `low` preserved.
- [[2026-04-11]] note | output-layout | Artifact naming scheme changed. Every file in the run folder is now prefixed with the input slug: `{slug}_{prompt}.md`, `{slug}_raw.{ext}`, `{slug}_meta.yml`. Meta file renamed from `meta.txt` (aligned-column format) to `{slug}_meta.yml` (proper YAML).
