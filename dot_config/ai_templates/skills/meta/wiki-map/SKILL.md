---
name: wiki-map
description: Build and maintain LLM-written personal wikis -- ingest sources into structured interlinked markdown.
---

# Wiki Map

> Three wiki operations in one skill -- ingest sources into a persistent knowledge base, query across pages with citations, and lint for structural health -- routed automatically based on what you need.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

For the full schema, hard rules, and orientation protocol, read `references/SCHEMA.md`.

> **Reading principle:** Agents should read progressively — only load documents when
> specific information is needed. Do not read all sub-skills or workflows upfront.

---

## The Problem

Most people's experience with LLMs and documents is stateless retrieval: upload files, the LLM finds relevant chunks at query time, generates an answer, and forgets everything. Nothing compounds. Ask a subtle question that requires synthesizing five documents, and the LLM re-derives the answer from scratch every time.

Maintaining a knowledge base manually is the alternative, but humans abandon wikis because the maintenance burden grows faster than the value. Updating cross-references, preserving provenance, tracking contradictions, and keeping structure consistent across dozens of pages is relentless bookkeeping.

The result:
- **Scattered knowledge** -- information lives in chat histories, bookmarks, note fragments, and memory
- **No accumulation** -- each session starts from zero; past synthesis is lost
- **Maintenance collapse** -- wikis decay as upkeep cost exceeds value
- **Missing connections** -- relationships across sources stay invisible

---

## The Solution

The LLM incrementally builds and maintains a persistent wiki -- a structured, interlinked collection of markdown files. New sources are ingested into existing pages or new pages with provenance. Cross-references are maintained. Contradictions are recorded in frontmatter. Query answers can be filed back into the wiki. Lint treats the wiki like a codebase and checks for drift.

Three operations make this work:

1. **Ingest** -- organize existing files into a wiki, process one source, process many sources atomically, delete pages safely, and upgrade old wikis to the current schema.
2. **Query** -- search the wiki, synthesize answers with citations, and file substantial answers back into the wiki.
3. **Lint** -- health-check the wiki for contradictions, provenance gaps, INDEX drift, orphan pages, stale content, weak cross-references, and schema violations.

The collection `SKILL.md` loads `references/ROUTER.md`, which routes to the right operation based on keyword matching. Each operation has its own `SKILL.md`, workflows, and conventions, but all of them share one canonical schema in `references/SCHEMA.md`.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Dispatch table routing requests to sub-skills |
| Global schema | `references/SCHEMA.md` | Canonical tag model, frontmatter, hard rules, orientation protocol |
| Ingest skill | `references/Ingest/SKILL.md` | Organize files, process sources, delete pages, upgrade old wikis |
| Ingest workflows | `references/Ingest/workflows/` | 5 workflows: CreateWikiMap, IngestSingle, IngestBatch, Delete, UpgradeSchema |
| Query skill | `references/Query/SKILL.md` | Search and synthesize answers from the wiki |
| Query workflows | `references/Query/workflows/` | 3 workflows: Search, DeepQuery, FileAnswer |
| Lint skill | `references/Lint/SKILL.md` | Health-check and maintain wiki quality |
| Lint workflows | `references/Lint/workflows/` | 2 workflows: FullSweep, QuickCheck |

**Summary:**
- **Sub-skills:** 3 (Ingest, Query, Lint)
- **Workflows:** 10 across all sub-skills
- **Dependencies:** None (works with any markdown-capable assistant)

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "create a wiki map for [topic]" | Routes to Ingest -> runs CreateWikiMap workflow |
| "organize these files into a wiki" | Routes to Ingest -> runs CreateWikiMap workflow |
| "ingest this article into the wiki" | Routes to Ingest -> runs IngestSingle workflow |
| "process these 5 sources" | Routes to Ingest -> runs IngestBatch workflow |
| "delete this wiki page" | Routes to Ingest -> runs Delete workflow |
| "upgrade this wiki to v2" | Routes to Ingest -> runs UpgradeSchema workflow |
| "what does the wiki say about X?" | Routes to Query -> runs Search or DeepQuery workflow |
| "synthesize everything we know about X" | Routes to Query -> runs DeepQuery workflow |
| "save that answer as a wiki page" | Routes to Query -> runs FileAnswer workflow |
| "health check the wiki" | Routes to Lint -> runs FullSweep workflow |
| "find orphan pages" | Routes to Lint -> runs QuickCheck workflow |
| "check provenance" | Routes to Lint -> runs QuickCheck workflow |

---

## Example Usage

### Creating a Wiki Map

```text
User: create a wiki map from my health-notes folder

AI responds:
Running the **CreateWikiMap** workflow in the **Ingest** skill...

Directory scan: health-notes/
Files found: 12
Need to move to references/: 10

| File | Current Location | Proposed Name |
|------|------------------|---------------|
| Vitamin D Notes.md | ./ | references/vitamin-d-notes.md |
| sleep_tracking.md | ./ | references/sleep-tracking.md |
| Dr Smith article.md | ./ | references/dr-smith-article.md |

Proceed? [user confirms]

Actions taken:
- Moved 10 files into references/ (body content untouched)
- Renamed 8 files to kebab-case
- Added frontmatter to 6 files (body content untouched)
- Created: INDEX.md (12 entries)
- Created: references/LOG.md
```

### Ingesting a Source

```text
User: ingest this article on vitamin D and sleep into the health wiki

AI responds:
Running the **IngestSingle** workflow in the **Ingest** skill...

Oriented: health-wiki | 47 pages | 30 recent log entries | no structure drift

Key takeaways:
1. Vitamin D deficiency correlates with poor sleep quality
2. Optimal levels: 40-60 ng/mL
3. Dr. Smith's 2024 study used a 500-person cohort

Actions taken:
- Created: references/vitamin-d-and-sleep.md (kind/project)
- Created: references/dr-smith-profile.md (topic/relationship)
- Updated: references/sleep-quality-factors.md
- Updated: references/supplement-comparison.md
- Updated: INDEX.md
- Appended: references/LOG.md
```

### Querying the Wiki

```text
User: what supplements affect sleep quality according to the wiki?

AI responds:
Running the **DeepQuery** workflow in the **Query** skill...

Based on 6 wiki pages:

1. Magnesium -- [[magnesium-and-sleep]]: strongest evidence base
2. Vitamin D -- [[vitamin-d-and-sleep]]: deficiency correlation
3. Melatonin -- [[melatonin-overview]]: direct mechanism, timing-dependent

Contradictions:
- [[dr-jones-review]] disputes the magnesium effect
- [[magnesium-and-sleep]] cites controlled trials showing significance

Source webclips: [[smith-2024-study]], [[supplement-review-2025]]
```

---

## Configuration

No runtime configuration is required. The skill works with any directory of markdown files that follows the shared schema.

The schema is global to this meta-skill. There is no per-wiki `SCHEMA.md`.

---

## Customization

| Customization | Where | Impact |
|---------------|-------|--------|
| Tag taxonomy | `references/SCHEMA.md` | Add or revise `kind/*`, `topic/*`, `status/*`, `pty/*` values |
| Page template | `references/SCHEMA.md` + Ingest workflows | Change default page structure |
| Lint rules | `references/SCHEMA.md` + Lint workflows | Add or disable health checks |
| Query output formats | Query workflows | Add new synthesis formats |
