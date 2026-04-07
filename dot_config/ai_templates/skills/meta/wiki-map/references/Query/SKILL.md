---
name: query
description: Search the wiki and synthesize answers with citations -- find relevant pages via the index, combine knowledge across pages, and optionally file answers back as new wiki pages. USE WHEN query wiki, search wiki, ask wiki, synthesize, deep query, what does the wiki say, find in wiki, compare, file answer, save answer, save as wiki page, compound answer.
---

## Customization

If the current assistant supports user-specific overrides, apply them before execution. Otherwise, use the defaults in this folder.

## Status Update

Before executing, emit a brief text status update such as:
`Running the **WorkflowName** workflow in the **Query** skill...`

# Query

Search the wiki and synthesize answers from its accumulated knowledge. Query workflows always start from the shared schema and then orient on the specific wiki before reading relevant pages.

For the full schema, hard rules, and orientation protocol, read `../SCHEMA.md`.

## Core Concept

The wiki is a pre-synthesized knowledge base. Query reads structured pages, follows cross-references, traces `sources:` back to source pages when useful, and answers from wiki content rather than from general memory.

## Workflow Routing

- Find relevant pages for a topic -> `workflows/Search.md`
- Synthesize an answer across multiple pages -> `workflows/DeepQuery.md`
- Save an answer back into the wiki as a new page -> `workflows/FileAnswer.md`

## Principles

1. **Read SCHEMA first** -- use the canonical conventions
2. **Start from INDEX.md** -- orientation before deep reads
3. **Follow cross-references** -- use body links and `## Related`
4. **Cite everything** -- every answer should point back to wiki pages
5. **Preserve provenance** -- use `sources:` when tracing claims back to source pages
6. **File only worthy answers** -- not every lookup should become a page
