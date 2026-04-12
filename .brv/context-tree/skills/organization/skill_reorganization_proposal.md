---
title: Skill Reorganization Proposal
summary: Document the proposed shift of 62 skills from legacy meta/pa-sdlc/specs/utils categories into future knowledge/dev/think/spec domains with explicit move mappings.
tags: []
keywords: []
importance: 62
recency: 1
maturity: draft
accessCount: 4
createdAt: '2026-04-11T12:33:17.622Z'
updatedAt: '2026-04-11T12:33:17.622Z'
---
## Reason
Capture the 2026-04-11 proposal that reorganizes the legacy skill taxonomy into future domains with a detailed moves table.

## Raw Concept
**Task:**
Document the 62-skill reorganization proposal that realigns legacy categories into a richer future taxonomy and records every skill move.

**Changes:**
- Standardized the idea doc to list one skill per bullet so future sections can match this style.
- Outlined the legacy categories (meta, pa-sdlc, specs, utils) and the future categories (knowledge, dev, think, spec) with their skill members.
- Captured a Moves table mapping each skill from its legacy location to its new future domain.

**Files:**
- docs/ideas/references/2026-04-11-skills-reorganization-proposal/idea.md

**Flow:**
Legacy structure -> Future structure -> Moves table detailing each migration

**Timestamp:** 2026-04-11

## Narrative
### Structure
The document begins by listing the current structure: meta/, pa-sdlc/, specs/, and utils/ categories each containing their associated skills. It then enumerates the proposed future structure with domains knowledge, dev (including lifecycle, code, review, docs, headless, browser, system, media, research, diagram, task, util subcategories), think (reasoning, content, doc, distill), and spec (process, design, score). The final section presents the Moves table showing skill migrations.

### Dependencies
Successful reorganization depends on migrating skills into the new domains without losing the existing knowledge links and ensuring teams owning each skill approve the new placement before updating references.

### Highlights
The future knowledge domain consolidates infrastructure skills (vault, obsidian, wiki-map, qmd, pg-memory, byterover, nia-docs, map-filesystem-abstract, cass). The dev domain reorganizes lifecycle, coding, review, docs, headless, browser, system, media, research, diagram, task, and util tracks. The think domain clusters reasoning, creative/marketing/ContentAnalysis content, documentation/liteparse/investigation research, and distillation tools. The spec domain keeps process, design, and scoring artifacts. The Moves table ensures every skill transition is explicitly captured.

### Examples
| Skill | From | To |
|-------|------|-----|
| changelog | specs/ | dev/docs/ |
| council | specs/ | spec/process/ |
| five-council | pa-sdlc/ | spec/process/ |
| eval-rubric | specs/ | dev/review/ |
| grill-me-v2 | specs/ | spec/process/ |
| color-palette | specs/ | spec/design/ |
| thinking | meta/ | think/reasoning/ |
| creative | meta/ | think/content/ |
| marketing | meta/ | think/content/ |
| ContentAnalysis | meta/ | think/content/ |
| investigation | meta/ | think/doc/ |
| liteparse | meta/ | think/doc/ |


## Facts
- **legacy_skill_structure**: Legacy skill structure splits 62 skills across the meta, pa-sdlc, specs, and utils categories. [project]
- **future_skill_structure**: Future skill structure organizes assets under knowledge, dev (with lifecycle/code/review/docs/headless/browser/system/media/research/diagram/task/util subcategories), think (reasoning/content/doc/distill), and spec (process/design/score) domains. [project]
- **changelog_move**: Changelog moves from specs/ to dev/docs/ per the Moves table. [project]
- **skills_count**: The proposal documents a total of 62 skills being reassigned across the new taxonomy. [project]
