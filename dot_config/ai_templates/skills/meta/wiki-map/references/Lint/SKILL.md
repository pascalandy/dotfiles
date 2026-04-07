---
name: lint
description: Health-check and maintain wiki quality -- find contradictions, orphan pages, stale content, provenance gaps, missing cross-references, and schema drift. USE WHEN lint wiki, health check, wiki maintenance, find orphans, find contradictions, stale pages, missing cross-references, wiki cleanup, wiki audit, check wiki, wiki health, provenance, orphan webclips, topic tags, tag order, long pages, log size, index size.
---

## Customization

If the current assistant supports user-specific overrides, apply them before execution. Otherwise, use the defaults in this folder.

## Status Update

Before executing, emit a brief text status update such as:
`Running the **WorkflowName** workflow in the **Lint** skill...`

# Lint

Health-check the wiki and surface structural issues that degrade quality over time. Lint reads the whole wiki, validates it against the shared schema, and reports findings in severity order.

For the full schema, hard rules, and orientation protocol, read `../SCHEMA.md`.

## Core Concept

Wikis decay silently. New sources contradict old claims. Provenance links break. Pages lose cross-references. INDEX drifts away from the filesystem. Lint treats the wiki like a codebase: run checks, report findings, then fix carefully.

## Workflow Routing

- Comprehensive health check -> `workflows/FullSweep.md`
- Check for one issue type -> `workflows/QuickCheck.md`

## Severity Ordering

Within each severity tier, report issues in this order:

1. broken wikilinks
2. broken `sources:` provenance
3. contradictions
4. orphan pages and orphan webclips
5. missing pages
6. stale content
7. missing cross-references
8. tag and frontmatter issues
9. thin or long pages

## Principles

1. **Read the whole wiki** -- lint is comprehensive by default
2. **Use the shared schema** -- validate against one canonical rule set
3. **Exclude closed pages where required** -- orphan, stale, and weak-link checks skip them
4. **Report before fixing** -- especially for contradictions and provenance issues
5. **Log every sweep** -- health checks leave an audit trail
