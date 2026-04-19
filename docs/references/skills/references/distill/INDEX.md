---
name: distill bucket
description: Catalog for the `distill` bucket — six transformation skills that turn long-form text into structured notes, summaries, or styled outputs
tags:
  - area/ea
  - kind/wiki
  - status/open
  - bucket/distill
date_created: 2026-04-18
date_updated: 2026-04-18
---

# distill bucket

> Thin bucket catalog. Routes to per-skill wikis under the transformation bucket.
> **Parent index:** [`../../INDEX.md`](../../INDEX.md) | **Child wikis:** 1 | **Last updated:** 2026-04-18

The `distill` bucket groups the skills that transform content — taking a long input (text file, transcript, article, note set) and producing something shorter, cleaner, or more structured. Source tree: `dot_config/ai_templates/skills/distill/`.

## Skills in this bucket

| Skill | Source | Wiki here |
|---|---|---|
| `distill` | `dot_config/ai_templates/skills/distill/distill/` | [distill](distill/INDEX.md) |
| `distill-prompt` | `dot_config/ai_templates/skills/distill/distill-prompt/` | none yet — meta-skill, see its `ROUTER.md` |
| `writer-sk` | `dot_config/ai_templates/skills/distill/writer-sk/` | none yet |
| `simple-editor` | `dot_config/ai_templates/skills/distill/simple-editor/` | none yet |
| `transcript-sk` | `dot_config/ai_templates/skills/distill/transcript-sk/` | none yet |
| `liteparse` | `dot_config/ai_templates/skills/distill/liteparse/` | none yet |

Skills without a wiki are documented entirely inside their own `SKILL.md`.

## Wiki Map

### kind/wiki

| File | Description |
|------|-------------|
| [`distill/INDEX.md`](distill/INDEX.md) | `distill` — apply a named prompt to a local text file via claude, codex, or opencode |

## Related

- [[../INDEX.md]] — parent skills wiki
- [[how-ai-templates-are-distributed]] — how these skill sources fan out to every agent home
