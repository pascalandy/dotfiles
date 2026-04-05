---
name: wiki-map
description: Build and maintain LLM-written personal wikis -- ingest sources, query across pages, and lint for health. USE WHEN wiki, ingest, ingest source, process source, process article, add to wiki, add source, add article, new source, webclip, batch ingest, create wiki, bootstrap wiki, init wiki, new wiki, query wiki, search wiki, ask wiki, synthesize, deep query, what does the wiki say, find in wiki, compare, file answer, save answer, save as wiki page, compound answer, lint wiki, health check, wiki health check, wiki maintenance, find orphans, find contradictions, stale pages, missing cross-references, wiki cleanup, wiki audit, check wiki, wiki health, knowledge base, personal wiki, research wiki, wiki index, wiki log, cross-reference, update wiki.
---

# Wiki Map

## Routing

| Request Pattern | Route To |
|---|---|
| create wiki map, create wiki, bootstrap, init wiki, new wiki, organize files | `Ingest/SKILL.md` -> `workflows/CreateWikiMap.md` (content read-only) |
| ingest, process source, add source, add to wiki, webclip, batch ingest | `Ingest/SKILL.md` -> `workflows/IngestSingle.md` or `IngestBatch.md` |
| query, search wiki, ask wiki, synthesize, deep query, what does the wiki say | `Query/SKILL.md` |
| file answer, save answer, save as wiki page, compound answer | `Query/SKILL.md` |
| lint, health check, wiki maintenance, find orphans, find contradictions, stale pages, missing cross-references | `Lint/SKILL.md` |
