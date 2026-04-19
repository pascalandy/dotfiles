---
name: idea-personal-knowledge-compilation
description: Cross-analysis of wiki-map vs wiki-gen — what's missing, what to pull in.
tags:
  - area/ea
  - kind/random
  - status/draft
date_created: 2026-04-19
date_updated: 2026-04-19
---

# Personal Knowledge Compilation — gaps in wiki-map

Different mental model from Lint. Lint = "is the wiki healthy?" Breakdown = "is the wiki complete?" Spawns parallel subagents to mine existing pages for missing concept entities, then creates them and back-edits siblings to add wikilinks.

Four phases. Coverage in current wiki-map:

| Phase | What it does | Status |
|---|---|---|
| 1. Survey | Flag bloated pages, bare directories, high-reference entities with no page | **Partial** — scattered across FullSweep checks |
| 2. Mining | Parallel subagents, ~10 pages each, concrete-noun test | **Missing** |
| 3. Planning | Dedupe, rank by reference count, candidate table for approval | **Missing** (report shape exists, wrong content kind) |
| 4. Creation | Write new pages + back-edit siblings to add `[[wikilinks]]` | **Missing** |
