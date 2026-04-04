---
name: lint
description: Health-check and maintain wiki quality -- find contradictions, orphan pages, stale content, missing cross-references, and data gaps. USE WHEN lint wiki, health check, wiki maintenance, find orphans, find contradictions, stale pages, missing cross-references, wiki cleanup, wiki audit, check wiki, wiki health.
---

## Customization

If the current assistant supports user-specific overrides, apply them before execution. Otherwise, use the defaults in this folder.

## Status Update

Before executing, emit a brief text status update such as:
`Running the **WorkflowName** workflow in the **Lint** skill to ACTION...`

# Lint

Health-check the wiki and surface structural issues that degrade quality over time. The LLM systematically examines pages for contradictions, orphans, staleness, missing links, and gaps -- then suggests or applies fixes.

## Core Concept

Wikis decay silently. New sources contradict old claims. Pages lose their cross-references. Important concepts get mentioned but never get their own page. Summaries grow stale as newer data supersedes them. Without periodic maintenance, the wiki's reliability degrades even as it grows.

Lint is the maintenance operation. It treats the wiki like a codebase: run checks, find issues, report or fix them. The LLM is good at this because it can read every page, hold the full structure in context, and spot inconsistencies a human would miss.

## When to Use

- **Periodic maintenance** -- run a full sweep weekly or after a batch of ingestions
- **Targeted check** -- "are there any orphan pages?", "find contradictions"
- **After major ingestion** -- verify the wiki stayed consistent
- **Before a deep query** -- ensure the wiki is healthy before relying on it

## Workflow Routing

Route to the appropriate workflow based on the request.

**When executing a workflow, output this notification directly:**

```
Running the **WorkflowName** workflow in the **Lint** skill to ACTION...
```

- Comprehensive health check -> `workflows/FullSweep.md`
- Check for a specific issue type -> `workflows/QuickCheck.md`

## Issue Categories

| Category | What to Look For |
|----------|-----------------|
| **Contradictions** | Pages that make conflicting claims about the same topic |
| **Orphans** | Pages with zero inbound `[[wikilinks]]` from other pages |
| **Stale** | Pages with `date_updated` significantly older than related pages, or claims superseded by newer sources |
| **Missing pages** | Concepts mentioned in 2+ pages via `[[wikilink]]` that have no corresponding page |
| **Missing cross-refs** | Pages that cover related topics but do not link to each other |
| **Tag issues** | Missing required tags, wrong tag axis order, invalid tag values |
| **INDEX drift** | Pages that exist in `references/` but are not listed in INDEX.md, or INDEX.md entries pointing to deleted pages |

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **Critical** | Contradictions, INDEX drift | Fix immediately or flag for user |
| **Warning** | Orphans, missing pages, stale content | Suggest fixes |
| **Info** | Missing cross-refs, tag issues | Fix automatically or note |

## Principles

1. **Read everything** -- lint requires reading all pages, not sampling
2. **Report before fixing** -- present findings to the user before making changes
3. **Severity matters** -- contradictions are critical; missing cross-refs are minor
4. **Suggest sources** -- if a gap is identified, suggest what source could fill it
5. **Log the sweep** -- every lint operation gets a LOG.md entry
