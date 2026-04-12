---
title: Skill Reorganization Proposal
summary: Documents current buckets, the future taxonomy, and the Moves table aligning each skill with its destination.
tags: []
keywords: []
importance: 65
recency: 1
maturity: validated
accessCount: 5
createdAt: '2026-04-11T12:32:42.797Z'
updatedAt: '2026-04-11T12:32:42.797Z'
---
## Reason
Capture the April 11, 2026 skill bucket redesign with before/after lists and the move table for every skill.

## Raw Concept
**Task:**
Document the April 11, 2026 skill reorganization plan with current/future structures and the moves table.

**Changes:**
- Standardized list formatting so every skill/category section uses one bullet per item for consistency with future sections.
- Specified the future structure with knowledge, dev, think, and spec partitions plus their nested sub-buckets.
- Captured the moves table that deterministically reassigns each skill from its current bucket to a new one.

**Files:**
- docs/ideas/references/2026-04-11-skills-reorganization-proposal/idea.md

**Flow:**
Document current structure -> Define future taxonomy -> Tabulate moves table

**Timestamp:** 2026-04-11

## Narrative
### Structure
The idea begins with "# Skill Reorganization — 62 Skills", then defines Current Structure sections for meta, pa-sdlc, specs, and utils (each listing skills one per bullet). The Future section describes knowledge, dev (with lifecycle/code/review/docs/headless/browser/system/media/research/diagram/task/util subcategories), think (reasoning/content/doc/distill), and spec (process/design/score) partitions with matching single-bullet formatting. The Moves section concludes with a three-column table that ties each skill to its origin and destination without altering the table contents.

### Dependencies
Planning depends on the accuracy of the current bucket lists (meta, pa-sdlc, specs, utils) because the move table references those groupings directly.

### Highlights
Highlights include the future knowledge bucket (vault, obsidian, wiki-map, qmd, pg-memory, byterover, nia-docs, map-filesystem-abstract, cass) plus the Moves table below.

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
| obsidian | pa-sdlc/ | knowledge/vault/ |
| wiki-map | pa-sdlc/ | knowledge/vault/ |
| qmd | pa-sdlc/ | knowledge/vault/ |
| pg-memory | utils/ | knowledge/memory/ |
| byterover | utils/ | knowledge/memory/ |
| nia-docs | utils/ | knowledge/browse/ |
| map-filesystem-abstract | utils/ | knowledge/fs/ |
| cass | utils/ | knowledge/fs/ |
| distill | pa-sdlc/ | think/distill/ |
| distill-prompt | pa-sdlc/ | think/distill/ |
| writer-sk | utils/ | think/distill/ |
| simple-editor | utils/ | think/distill/ |
| transcript-sk | utils/ | think/distill/ |

## Facts
- **current_meta_skills**: Current meta category lists thinking, creative, marketing, ContentAnalysis, investigation, and liteparse. [project]
- **future_knowledge_bucket**: Future knowledge bucket groups vault, obsidian, wiki-map, qmd, pg-memory, byterover, nia-docs, map-filesystem-abstract, and cass. [project]
- **skills_moves_table**: Moves table reassigns every listed skill (changelog, council, five-council, eval-rubric, grill-me-v2, color-palette, thinking, creative, marketing, ContentAnalysis, investigation, liteparse, obsidian, wiki-map, qmd, pg-memory, byterover, nia-docs, map-filesystem-abstract, cass, distill, distill-prompt, writer-sk, simple-editor, transcript-sk) from their current buckets to futures such as dev/docs, spec/process, think/content, knowledge/vault, and think/distill. [project]
