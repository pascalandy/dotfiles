---
name: Nested Wiki Maps Plan V2
description: Clarified plan for bottom-up updates across user-created nested wiki-map trees
tags:
  - area/ea
  - kind/plan
  - status/open
date_created: 2026-04-12
date_updated: 2026-04-12
---

# Plan: nested wiki maps V2

## Context

Some wiki trees contain nested wiki maps: a root parent wiki routes to child wikis, and those child wikis can themselves route to grandchild wikis. The docs tree already uses this pattern in places like `docs/INDEX.md -> references/workflows/INDEX.md -> references/skills/distill/INDEX.md`, but the active `wiki-map` skill still describes a flatter indexing model in its schema and workflows.

This V2 plan replaces ambiguity from the earlier draft and locks the implementation contract around one critical rule: nested wiki maps are user-created boundaries. The skill must recognize and preserve them, but must never create them proactively.

## Goals

1. Make recursive nested-wiki updates the default behavior when a requested wiki already contains nested child wikis.
2. Process nested wiki trees bottom-up: grandchild first, then child, then root parent.
3. Treat only existing directories with their own `INDEX.md` as nested wiki boundaries.
4. Keep parent indexes as routers: list direct child wiki `INDEX.md` files, not the child's leaf pages.
5. Regenerate each parent-level child description on every run so routed entries stay accurate.
6. Preserve mixed directories: list ordinary notes directly and nested child wikis as routes.
7. Continue other branches if one branch fails, then report warnings.
8. Show traversal progress in visible bottom-up order.
9. Preserve the current rule that the user decides when a directory becomes its own wiki map.

## Locked Decisions

### 1. Family model

- A `grandchild wiki` updates first.
- Then its `child wiki` updates.
- Then the `root parent wiki` updates.
- A nested wiki can be both a child from above and a parent for what sits below it.

### 2. Boundary detection

- A directory counts as a nested wiki boundary only if it already contains its own `INDEX.md`.
- A plain directory does not become a wiki map automatically.
- The skill must never create nested wiki boundaries on its own.
- The user decides when to create a child wiki.

### 3. Parent behavior

- Parent indexes link to direct child `INDEX.md` files only.
- Parent route paths should follow the existing docs pattern: `references/{child}/INDEX.md`.
- Parent indexes do not flatten grandchild or deeper leaf pages into the parent table.
- The parent-level one-line child description is refreshed on every recursive update.
- Description source order:
  1. child `INDEX.md` frontmatter `description`
  2. fallback to the first non-empty paragraph after frontmatter and title

### 4. Mixed directories

- If a wiki contains ordinary notes and nested child wikis, its `INDEX.md` lists both:
  - ordinary notes directly
  - nested child wikis as routes to their `INDEX.md`
- Plain directories under `references/` that do not contain an `INDEX.md` stay ordinary directories.
- Their markdown files are indexed directly according to existing wiki-map rules.

### 5. CreateWikiMap behavior

- `CreateWikiMap` must preserve existing child wikis only.
- If a subdirectory already has its own `INDEX.md`, treat it as a child wiki route.
- Do not move that child wiki's internal files into the parent indexing model.
- Do not bootstrap new child wikis.
- Do not ask to convert ordinary directories into child wikis as part of this phase.

### 6. Failure behavior

- If one branch fails, skip that branch.
- Continue updating sibling branches.
- Report the failed branch as a warning at the end.
- Keep the execution model best-effort and agent-managed rather than over-specifying parent refresh internals.

### 7. Reporting

- Show progress level by level in the actual traversal order.
- Expected mental model:
  1. updated grandchild
  2. updated child
  3. updated root parent

## Implementation Surface

### 1. Schema contract

Update `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/SCHEMA.md` to define:

- nested wiki boundary detection by existing `INDEX.md`
- bottom-up recursive updates as the default nested-tree behavior
- parent router behavior using direct child `INDEX.md` routes
- mixed-directory behavior
- explicit non-goal: do not create child wikis automatically
- failed-branch handling expectations

### 2. Recursive update workflow

Add a new Lint workflow:

- `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/Lint/workflows/RecursiveUpdate.md`

This workflow becomes the home for nested recursive updates.

Responsibilities:

1. discover nested descendants under the requested wiki
2. ignore plain directories that do not define their own child wiki boundary
3. sort nested descendants deepest first
4. update each wiki bottom-up
5. refresh local indexing and direct child routes at each level
6. continue sibling branches when one branch fails
7. report warnings at the end

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
- plain directories without child `INDEX.md` are still indexed as ordinary content, not as child wikis

### 5. Ingest behavior changes

Update `dot_config/ai_templates/skills/pa-sdlc/wiki-map/references/Ingest/workflows/CreateWikiMap.md` so index building respects nested wiki boundaries.

Rules:

- if a subdirectory already has its own `INDEX.md`, treat it as a child wiki route
- preserve that child wiki in place
- do not move or flatten that child wiki's internal files into the parent wiki map
- if a subdirectory does not have its own `INDEX.md`, keep the current direct-file behavior
- do not create nested child wikis automatically

## Minimal Change Plan

### Phase 1. Schema

- teach the canonical schema about parent, child, and grandchild boundaries
- update examples so they reflect routed child `INDEX.md` entries
- add the explicit rule that child wiki creation is user-driven

### Phase 2. Lint workflow

- add `RecursiveUpdate.md`
- update Lint routing docs and meta-skill text

### Phase 3. Drift rules

- update FullSweep so nested child leaves are not considered missing parent entries
- ensure plain directories are still treated as ordinary indexed content

### Phase 4. CreateWikiMap

- change index generation to route existing nested children rather than flatten them
- preserve ordinary directories as ordinary directories unless they already define a child wiki with `INDEX.md`
- do not bootstrap child wikis

### Phase 5. Verification

- verify the traversal order is bottom-up
- verify mixed directories keep both direct notes and child routes
- verify a failed branch does not block sibling branches
- verify parent descriptions regenerate from child `description`, with fallback to first body paragraph when needed
- verify plain directories are never auto-promoted into child wikis

## Out Of Scope For This Phase

- standalone `wiki-update` shell command in `~/.local/bin/`
- new discovery CLI outside the `wiki-map` skill
- changing the existing process for ordinary non-nested markdown files
- automatic conversion of directories into child wiki maps
- prompting users to convert directories into child wiki maps during `CreateWikiMap`

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
- ordinary directories without `INDEX.md` remain ordinary directories and are indexed directly

## Current Recommendation

Implement this as a new Lint workflow first, then update schema and existing workflow text to match the real parent/child/grandchild routing model already used in the docs tree.

Use `docs/INDEX.md` as the canonical parent-router example for path shape and index behavior.
