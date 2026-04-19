---
name: wiki-map
description: Route wiki-map requests to ingest, query, lint, or compile workflows.
---

# Wiki Map

> **Note:** This router dispatches to sub-skills. Read only the sub-skill
> referenced by the matched pattern. Do not read all sub-skills preemptively.

## Routing

| Request Pattern | Route To |
|---|---|
| create wiki map, create wiki, bootstrap, init wiki, new wiki, organize files | `Ingest/MetaSkill.md` -> `workflows/CreateWikiMap.md` |
| ingest, process source, add source, add to wiki, webclip, process article | `Ingest/MetaSkill.md` -> `workflows/IngestSingle.md` |
| batch ingest, process sources, ingest all, bulk import | `Ingest/MetaSkill.md` -> `workflows/IngestBatch.md` |
| delete page, remove page, get rid of page, delete webclip | `Ingest/MetaSkill.md` -> `workflows/Delete.md` |
| upgrade wiki, upgrade schema, migrate wiki to v2 | `Ingest/MetaSkill.md` -> `workflows/UpgradeSchema.md` |
| query, search wiki, ask wiki, what does the wiki say, find in wiki | `Query/MetaSkill.md` -> `workflows/Search.md` or `workflows/DeepQuery.md` |
| synthesize, deep query, compare, timeline, current understanding | `Query/MetaSkill.md` -> `workflows/DeepQuery.md` |
| file answer, save answer, save as wiki page, compound answer | `Query/MetaSkill.md` -> `workflows/FileAnswer.md` |
| recursive wiki update, refresh wiki tree, update nested wiki, rebuild index routes | `Lint/MetaSkill.md` -> `workflows/RecursiveUpdate.md` |
| lint, health check, wiki maintenance, full sweep | `Lint/MetaSkill.md` -> `workflows/FullSweep.md` |
| find orphans, contradictions, provenance, sources, topic tags, tag order, big pages, log size, index size, rotate log, recovery | `Lint/MetaSkill.md` -> `workflows/QuickCheck.md` |
| compile wiki, fill wiki gaps, promote missing entities, is the wiki complete, concept mining | `Compile/MetaSkill.md` -> `workflows/CompileWiki.md` |
| wiki-map update (bare phrase, ambiguous) | Disambiguate: ask the user whether they want **lint** (health check), **refresh** (rebuild INDEX routes via RecursiveUpdate), or **compile** (fill gaps). Do not silently route. |
