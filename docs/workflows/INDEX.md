---
name: Workflows Wiki
description: Documentation and notes about processes and methodologies used in this repo, including the `pa-sdlc` family and individual skills like `distill`
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Workflows Wiki

> Content catalog. Every wiki page is listed here with a one-line summary.
> Read this first to find relevant pages for any query.
> **Parent index:** [`../INDEX.md`](../INDEX.md) | **Total pages:** 2 | **Last updated:** 2026-04-11

This category covers how workflows and methodologies are organized in this repo. Two groupings live here today:

- **`pa-sdlc/`** — the Pascal Andy Software Development Lifecycle, a family of eight `pa-*` skills with a first-person narrative layer explaining when and why to reach for each stage.
- **`skills/`** — standalone, non-lifecycle skills that have enough mechanical complexity to warrant their own wiki. Today this holds `distill`, a content-processing CLI that physically lives under `pa-sdlc/` in the source tree but is not part of the lifecycle itself.

Workflow pages in both groupings are **personal-preferences**: they describe how this operator uses the skills, not a neutral third-party reference. For the skills' own authoritative entry points, read the `SKILL.md` files under `dot_config/ai_templates/skills/`.

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/wiki

| File | Description |
|------|-------------|
| [`references/pa-sdlc/INDEX.md`](references/pa-sdlc/INDEX.md) | The Pascal Andy Software Development Lifecycle — eight stages from Scout to Advisor |
| [`references/skills/distill/INDEX.md`](references/skills/distill/INDEX.md) | `distill` — apply a named prompt to a local text file via claude, codex, or opencode |

## Related

- [[docs/INDEX.md]] — root catalog
- [[configs/INDEX.md]] — individual config files and tools
- [[operations/INDEX.md]] — how the repo itself operates
