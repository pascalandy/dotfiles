---
name: wiki-map
description: Route wiki-map requests to ingest, query, or lint workflows.
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
