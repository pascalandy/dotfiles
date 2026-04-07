---
name: wiki-map
description: Build and maintain LLM-written personal wikis -- ingest sources, query across pages, and lint for health. USE WHEN wiki, ingest, ingest source, process source, process article, add to wiki, add source, add article, new source, webclip, batch ingest, create wiki, bootstrap wiki, init wiki, new wiki, delete wiki page, remove wiki page, delete webclip, upgrade wiki, upgrade schema, query wiki, search wiki, ask wiki, synthesize, deep query, what does the wiki say, find in wiki, compare, file answer, save answer, save as wiki page, compound answer, lint wiki, health check, wiki maintenance, find orphans, find contradictions, stale pages, missing cross-references, provenance, orphan webclips, tag order, big pages, log size, index size.
---

# Wiki Map

## Routing

| Request Pattern | Route To |
|---|---|
| create wiki map, create wiki, bootstrap, init wiki, new wiki, organize files | `Ingest/SKILL.md` -> `workflows/CreateWikiMap.md` |
| ingest, process source, add source, add to wiki, webclip, process article | `Ingest/SKILL.md` -> `workflows/IngestSingle.md` |
| batch ingest, process sources, ingest all, bulk import | `Ingest/SKILL.md` -> `workflows/IngestBatch.md` |
| delete page, remove page, get rid of page, delete webclip | `Ingest/SKILL.md` -> `workflows/Delete.md` |
| upgrade wiki, upgrade schema, migrate wiki to v2 | `Ingest/SKILL.md` -> `workflows/UpgradeSchema.md` |
| query, search wiki, ask wiki, what does the wiki say, find in wiki | `Query/SKILL.md` -> `workflows/Search.md` or `workflows/DeepQuery.md` |
| synthesize, deep query, compare, timeline, current understanding | `Query/SKILL.md` -> `workflows/DeepQuery.md` |
| file answer, save answer, save as wiki page, compound answer | `Query/SKILL.md` -> `workflows/FileAnswer.md` |
| lint, health check, wiki maintenance, full sweep | `Lint/SKILL.md` -> `workflows/FullSweep.md` |
| find orphans, contradictions, provenance, sources, topic tags, tag order, big pages, log size, index size, rotate log, recovery | `Lint/SKILL.md` -> `workflows/QuickCheck.md` |
