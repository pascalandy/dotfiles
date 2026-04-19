---
name: compile
description: Promote implied-missing entities inside the wiki into first-class pages from the wiki's own content, under an explicit approval gate.
---

## Customization

If the current assistant supports user-specific overrides, apply them before execution. Otherwise, use the defaults in this folder.

## Status Update

Before executing, emit a brief text status update such as:
`Running the **WorkflowName** workflow in the **Compile** skill...`

# Compile

Answer "is the wiki complete?" by mining existing pages for repeatedly-referenced entities that do not yet have their own page, then creating those pages and back-editing siblings with wikilinks under user approval.

For the full schema, hard rules, and orientation protocol, read `../SCHEMA.md`.

## Critical Guardrails

**Compile writes from the wiki itself. It never ingests external sources.**
If you need to process an external source, use Ingest, not Compile.

**Compile never rebuilds INDEX routes.** INDEX route rebuilds live in `Lint/workflows/RecursiveUpdate.md`.

**Compile never re-scans the wiki for health.** It consumes Lint output as input. If no recent Lint report exists, Phase 2 halts and instructs the user to run a health check first.

## Core Concept

A mature wiki already contains the raw material for its next layer of structure. Concrete-noun entities -- people, tools, frameworks, named concepts, named events -- often appear in many pages before they get their own. Compile promotes those entities to first-class pages, applies the shared schema (`2+ sources` or central-subject rule from `../SCHEMA.md`), and back-edits siblings with wikilinks.

The wiki's own pages are the mine. Lint's latest report is the compass.

## Workflow Routing

- Full compile pass (gate -> survey -> mine -> plan -> write) -> `workflows/CompileWiki.md`

Only one workflow today. A read-only `Survey.md` variant may be added later if the approval gate proves useful to run in isolation.

## Principles

1. **Require a Lint gate** -- never run blind; rely on a recent `FullSweep` or `QuickCheck` entry in `LOG.md`
2. **Mine in parallel, write once** -- parallel fan-out for extraction, one atomic write pass for creation
3. **Apply schema thresholds** -- only promote entities that clear the `2+ sources` or central-subject rule
4. **Respect the mass-update gate** -- plan first, approve before any write touching 10+ pages
5. **Write from the wiki, not from outside** -- new pages are synthesized from existing wiki content, never from new external sources
6. **Preserve INDEX authority** -- one INDEX patch at the end, never per-page, never rebuild routes
7. **Fail safely** -- append the compile pass to `LOG.md` as a recovery marker before writing pages

## Sub-Agent Dispatch

Phase 4 mines pages in parallel batches. When the harness supports sub-agent fan-out, dispatch via the `delegate-to-sub` skill (one worker per batch). When it does not, iterate batches sequentially. The worker contract in `workflows/CompileWiki.md` is identical either way, so the output shape is stable across harnesses.
