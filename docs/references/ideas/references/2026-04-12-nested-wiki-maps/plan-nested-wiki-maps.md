---
name: Nested Wiki Maps Plan
description: Plan for bottom-up recursive updates across nested wiki-map trees
tags:
  - area/ea
  - kind/project
  - status/open
date_created: 2026-04-12
date_updated: 2026-04-12
---

# Plan: nested wiki maps

## Context

Some wiki trees contain nested wiki maps: a root parent wiki routes to child wikis, and those child wikis can themselves route to grandchild wikis. The current docs already use this pattern in places like `docs/INDEX.md -> workflows/INDEX.md -> skills/distill/INDEX.md`, but the active `wiki-map` skill still describes a flatter indexing model in its schema and workflows.

This plan exports the agreed behavior so implementation can follow one clear contract.

## Goals

1. Make recursive nested-wiki updates the default behavior.
2. Process nested wiki trees bottom-up: grandchild first, then child, then root parent.
3. Treat any directory with its own `INDEX.md` as a nested wiki boundary.
4. Keep parent indexes as routers: list direct child wiki `INDEX.md` files, not the child's leaf pages.
5. Regenerate each parent-level child description on every run so routed entries stay accurate.
6. Preserve mixed directories: list ordinary notes directly and nested child wikis as routes.
7. Continue other branches if one branch fails, then report warnings.
8. Show traversal progress in the visible bottom-up order.

## Locked Decisions

### 1. Family model

- A `grandchild wiki` updates first.
- Then its `child wiki` updates.
- Then the `root parent wiki` updates.
- A nested wiki can be both a child from above and a parent for what sits below it.

### 2. Boundary detection

- Any directory with `INDEX.md` counts as a nested wiki map.

### 3. Parent behavior

- Parent indexes link to direct child `INDEX.md` files only.
- Parent indexes do not flatten grandchild or deeper leaf pages into the parent table.
- The parent-level one-line child description is refreshed on every recursive update.
- Description source order:
  1. child `INDEX.md` frontmatter `description`
  2. fallback to child `INDEX.md` intro/body text when needed

### 4. Mixed directories

- If a wiki contains ordinary notes and nested child wikis, its `INDEX.md` lists both:
  - ordinary notes directly
  - nested child wikis as routes to their `INDEX.md`

### 5. Failure behavior

- If one branch fails, skip that branch.
- Continue updating sibling branches.
- Report the failed branch as a warning at the end.

### 6. Reporting

- Show progress level by level in the actual traversal order.
- Expected mental model:
  1. updated grandchild
  2. updated child
  3. updated root parent

## Implementation Surface

### 1. Schema contract

Update `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/SCHEMA.md` to define:

- nested wiki boundary detection by `INDEX.md`
- bottom-up recursive updates as the default nested-tree behavior
- parent router behavior
- mixed-directory behavior
- failed-branch handling expectations

### 2. Recursive update workflow

Add a new Lint workflow:

- `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/Lint/workflows/RecursiveUpdate.md`

This workflow becomes the home for nested recursive updates.

Responsibilities:

1. discover nested descendants under the requested wiki
2. sort them deepest first
3. update each wiki bottom-up
4. refresh local indexing and direct child routes at each level
5. continue sibling branches when one branch fails
6. report warnings at the end

### 3. Router integration

Update `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/ROUTER.md` so requests like these route into the new recursive workflow:

- `wiki-map update`
- `recursive wiki update`
- `refresh wiki tree`
- `update nested wiki`

### 4. Lint behavior changes

Update `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/Lint/workflows/FullSweep.md` so nested boundaries are treated correctly.

FullSweep should no longer treat a parent as stale just because it does not inline a child wiki's leaf pages.

Checks should validate:

- child wiki exists
- child `INDEX.md` exists
- parent route entry exists
- parent child-description is current

### 5. Ingest behavior changes

Update `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/Ingest/workflows/CreateWikiMap.md` so index building respects nested wiki boundaries.

Rules:

- if a subdirectory has its own `INDEX.md`, treat it as a child wiki route
- otherwise keep the current direct-file behavior

## Minimal Change Plan

### Phase 1. Schema

- teach the canonical schema about parent, child, and grandchild boundaries
- update examples so they reflect routed child `INDEX.md` entries

### Phase 2. Lint workflow

- add `RecursiveUpdate.md`
- update Lint routing docs and meta-skill text

### Phase 3. Drift rules

- update FullSweep so nested child leaves are not considered missing parent entries

### Phase 4. CreateWikiMap

- change index generation to route nested children rather than flatten them

### Phase 5. Verification

- verify the traversal order is bottom-up
- verify mixed directories keep both direct notes and child routes
- verify a failed branch does not block sibling branches
- verify parent descriptions regenerate from child `description`, with fallback to body intro when needed

## Out Of Scope For This Phase

- standalone `wiki-update` shell command in `~/.local/bin/`
- new discovery CLI outside the `wiki-map` skill
- changing the existing process for ordinary non-nested markdown files

## Files Expected To Change

- `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/SCHEMA.md`
- `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/ROUTER.md`
- `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/Lint/MetaSkill.md`
- `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/Lint/workflows/FullSweep.md`
- `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/Lint/workflows/RecursiveUpdate.md`
- `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/Ingest/workflows/CreateWikiMap.md`

## Verification Notes

Use the family test case during implementation:

1. root parent wiki
2. child wiki
3. grandchild wiki

Expected run order:

1. update grandchild
2. update child
3. update root parent

Expected indexing behavior:

- grandchild indexes its own local notes
- child indexes its own local notes plus a route to grandchild `INDEX.md`
- root parent indexes its own local notes plus routes to direct child `INDEX.md` files

## Current Recommendation

Implement this as a new Lint workflow first, then update schema and existing workflow text to match the real parent/child/grandchild routing model already used in the docs tree.
