---
name: pa-doc-cleaner
description: Documentation maintenance entry point — drift review, deduplication, and structural doc hygiene
tags:
  - area/ea
  - kind/doc
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-11
date_updated: 2026-04-18
---

# pa-doc-cleaner

**Entry point:** `pa-doc-cleaner`
**Source:** `dot_config/ai_templates/skills/pa-sdlc/pa-doc-cleaner/SKILL.md`

## What it does

Maintain an existing documentation surface. Review pages for drift, reduce redundancy, repair frontmatter and routing — no new authoring.

## When to use

- Docs may have drifted from reality and need a keep/update/replace/consolidate/remove pass.
- Canonical truth is clear and the job is reducing redundancy.
- Metadata, indexes, routing, taxonomy, or navigation are broken.

## Modes

| Mode | Use when |
|---|---|
| `DriftRefresh` | Reality-vs-doc review with explicit keep/update/replace/consolidate/remove judgments |
| `ConsolidationPass` | Canonical truth is clear; main job is reducing redundancy |
| `StructureGovernance` | Frontmatter, indexes, wikilinks, tags, date fields |

## Don't use for

- Writing one new doc for a specific change or artifact → `pa-doc-update`
- Retrospectives → `pa-postmortem`
- Scouting, scoping, direction, planning, implementation → the matching `pa-*` stage
