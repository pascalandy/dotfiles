---
name: Skills Wiki
description: Documentation and narrative layer for the skills under `dot_config/ai_templates/skills/`, organized by the 8 workflow-arc buckets
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-19
---

# Skills Wiki

> Content catalog. Every wiki page is listed here with a one-line summary.
> Read this first to find relevant pages for any query.
> **Parent index:** [`../INDEX.md`](../INDEX.md) | **Child wikis:** 2 | **Last updated:** 2026-04-18

This category holds the narrative layer for skills under `dot_config/ai_templates/skills/`. Each `SKILL.md` in the source tree is the authoritative entry point for invocation; this wiki captures mental model, design decisions, and cross-skill context that do not belong in a skill's own frontmatter.

The directory structure here mirrors the 8 workflow-arc buckets in the source tree (`pa-sdlc`, `devtools`, `think`, `knowledge`, `web`, `distill`, `diagram`, `media`). Not every skill has a wiki yet — most skills are documented entirely inside their own `SKILL.md`. A skill graduates to a wiki here when it develops enough mechanical complexity (design trade-offs, failure modes, cross-skill dependencies) to warrant a narrative page.

## How the buckets map to the source tree

| Bucket | Source path | Skills in bucket | Wikis here |
|---|---|---|---|
| `pa-sdlc` | `dot_config/ai_templates/skills/pa-sdlc/` | 9 lifecycle stages (`pa-scout` → `pa-postmortem`) | [pa-sdlc](references/pa-sdlc/INDEX.md) — one wiki covering the whole lifecycle |
| `devtools` | `dot_config/ai_templates/skills/devtools/` | 12 code-adjacent tools | none yet |
| `think` | `dot_config/ai_templates/skills/think/` | 4 reasoning skills | none yet |
| `knowledge` | `dot_config/ai_templates/skills/knowledge/` | 9 memory/index skills | none yet |
| `web` | `dot_config/ai_templates/skills/web/` | 7 research skills | none yet |
| `distill` | `dot_config/ai_templates/skills/distill/` | 6 transformation skills | [distill/distill](references/distill/distill/INDEX.md) |
| `diagram` | `dot_config/ai_templates/skills/diagram/` | 2 visualization skills | none yet |
| `media` | `dot_config/ai_templates/skills/media/` | 5 creative-output skills | none yet |

Wiki pages are **personal-preferences**: they describe how this operator uses the skills, not a neutral third-party reference. For authoritative invocation details, read the `SKILL.md` files.

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/wiki

| File | Description |
|------|-------------|
| [`references/pa-sdlc/INDEX.md`](references/pa-sdlc/INDEX.md) | The Pascal Andy Software Development Lifecycle — nine stages from Scout to Postmortem, plus Advisor |
| [`references/distill/INDEX.md`](references/distill/INDEX.md) | `distill` bucket catalog — routes to per-skill wikis under the transformation bucket |

## Related

- [[docs/INDEX.md]] — root catalog
- [[configs/INDEX.md]] — individual config files and tools
- [[operations/INDEX.md]] — how the repo itself operates
- [[how-ai-templates-are-distributed]] — how these skill sources fan out to every agent home
