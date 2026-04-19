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

Cross-analyzed my current `wiki-map` skill against `potential-skill.md` (wiki-gen). Capturing what's worth pulling in.

## Two pickups I want to pursue

### (a) Ingest-prep layer — its own skill

Convert non-markdown personal data (Day One JSON, Apple Notes, Obsidian, Notion, iMessage, CSV, email, Twitter) into markdown entries before wiki-map's existing Ingest workflows run.

This will be a **standalone skill**, sibling to `dot_config/ai_templates/skills/distill/liteparse`. Not a workflow inside wiki-map. The output of this skill becomes the input to `wiki-map ingest`.

### (b) Breakdown — proactive concept-page mining

Different mental model from Lint. Lint = "is the wiki healthy?" Breakdown = "is the wiki complete?" Spawns parallel subagents to mine existing pages for missing concept entities, then creates them and back-edits siblings to add wikilinks.

Four phases. Coverage in current wiki-map:

| Phase | What it does | Status |
|---|---|---|
| 1. Survey | Flag bloated pages, bare directories, high-reference entities with no page | **Partial** — scattered across FullSweep checks |
| 2. Mining | Parallel subagents, ~10 pages each, concrete-noun test | **Missing** |
| 3. Planning | Dedupe, rank by reference count, candidate table for approval | **Missing** (report shape exists, wrong content kind) |
| 4. Creation | Write new pages + back-edit siblings to add `[[wikilinks]]` | **Missing** |

Side note: no current workflow uses parallel subagents. Once Breakdown introduces the pattern, FullSweep could be parallelized the same way.

Likely lives as a 4th sub-skill alongside Ingest/Query/Lint, not under Lint.

## Skipped

- (c) Life-domain ontology (`person`, `era`, `pattern`, `philosophy`, `transition`) — not pursuing now.
- Writing-craft rules (anti-AI-voice, narrative-vs-diary, quote discipline) — too prescriptive for technical wikis.
- `also:` aliases and `_backlinks.json` — lint already covers the value.

## Related

- [[potential-skill]]
