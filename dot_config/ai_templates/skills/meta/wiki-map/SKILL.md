---
name: wiki-map
description: Build and maintain LLM-written personal wikis -- ingest sources into structured interlinked markdown, query across pages with synthesized answers, and lint for contradictions, orphans, and gaps. USE WHEN wiki, ingest, ingest source, process source, process article, add to wiki, add source, add article, new source, webclip, batch ingest, create wiki, bootstrap wiki, init wiki, new wiki, query wiki, search wiki, ask wiki, synthesize, deep query, what does the wiki say, find in wiki, compare, file answer, save answer, save as wiki page, compound answer, lint wiki, health check, wiki health check, wiki maintenance, find orphans, find contradictions, stale pages, missing cross-references, wiki cleanup, wiki audit, check wiki, wiki health, knowledge base, personal wiki, research wiki, wiki index, wiki log, cross-reference, update wiki.
---

# Wiki Map

> Three wiki operations in one skill -- ingest sources into a persistent knowledge base, query across pages with citations, and lint for structural health -- routed automatically based on what you need.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Most people's experience with LLMs and documents is stateless retrieval: upload files, the LLM finds relevant chunks at query time, generates an answer, and forgets everything. Nothing compounds. Ask a subtle question that requires synthesizing five documents, and the LLM re-derives the answer from scratch every time. The knowledge is never built up.

Maintaining a knowledge base manually is the alternative, but humans abandon wikis because the maintenance burden grows faster than the value. Updating cross-references, keeping summaries current, noting contradictions, maintaining consistency across dozens of pages -- the bookkeeping is relentless.

The result:
- **Scattered knowledge** -- information lives in chat histories, bookmarks, note fragments, and memory
- **No accumulation** -- each session starts from zero; past synthesis is lost
- **Maintenance collapse** -- wikis that start strong decay as the effort to maintain them exceeds the value extracted
- **Missing connections** -- relationships between sources that would be obvious with cross-references remain invisible

---

## The Solution

The LLM incrementally builds and maintains a persistent wiki -- a structured, interlinked collection of markdown files. When you add a source, the LLM reads it, extracts key information, and integrates it into existing pages. Cross-references are maintained. Contradictions are flagged. The synthesis reflects everything ingested so far. The wiki compounds with every source and every question.

Three operations make this work:

1. **Ingest** -- Two distinct operations. **CreateWikiMap** organizes existing files into a wiki structure -- moving, renaming, adding frontmatter, building the index -- without touching file body content. **IngestSingle** and **IngestBatch** are the synthesis operations: the LLM reads a source, discusses key takeaways, writes or updates wiki pages, maintains cross-references. A single ingest might touch 10-15 pages. Three workflows: CreateWikiMap (organize files / initialize wiki), IngestSingle (process one source interactively), IngestBatch (process multiple sources).

2. **Query** -- Search the wiki and synthesize answers. The LLM reads the index to find relevant pages, drills into them, and produces an answer with citations. Answers can take different forms: a markdown page, a comparison table, a timeline. Valuable answers can be filed back into the wiki as new pages, so explorations compound alongside ingested sources. Three workflows: Search, DeepQuery, FileAnswer.

3. **Lint** -- Health-check the wiki. Look for contradictions between pages, stale claims superseded by newer sources, orphan pages with no inbound links, important concepts lacking their own page, missing cross-references, and data gaps. Two workflows: FullSweep (comprehensive) and QuickCheck (targeted).

The collection `SKILL.md` loads `references/ROUTER.md`, which routes to the right operation based on keyword matching. Each operation has its own `SKILL.md`, workflows, and conventions.

---

## Wiki Architecture

Each wiki instance is a self-contained directory:

```
{wiki-name}/
  INDEX.md            # Content catalog (area/ea, kind/wiki)
  /references/        # All wiki pages: sources, entities, concepts, logs
  /assets/            # Non-markdown files: images, PDFs (optional)
```

All content lives under `/references/`. When organizing a wiki, move root files and existing subdirectories into `references/` as-is -- preserve directory structure, do not flatten subdirectories. Never create new subdirectories, never move files between directories, never reorganize the user's folder layout. The user manages directory structure; the assistant processes files wherever they are. For example, if `z_varia/` exists, move it to `references/z_varia/` intact. If the user has archive subdirectories, they stay as subdirectories under `references/`. Tags handle categorization. INDEX.md sits at the root and catalogs every page including those in subdirectories.

The schema (conventions, workflows, structure rules) is defined globally, not per-wiki.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Dispatch table routing requests to sub-skills |
| Ingest skill | `references/Ingest/SKILL.md` | Organize files and process sources into the wiki |
| Ingest workflows | `references/Ingest/workflows/` | 3 workflows: CreateWikiMap (read-only), IngestSingle, IngestBatch |
| Query skill | `references/Query/SKILL.md` | Search and synthesize answers from wiki |
| Query workflows | `references/Query/workflows/` | 3 workflows: Search, DeepQuery, FileAnswer |
| Lint skill | `references/Lint/SKILL.md` | Health-check and maintain wiki quality |
| Lint workflows | `references/Lint/workflows/` | 2 workflows: FullSweep, QuickCheck |

**Summary:**
- **Sub-skills:** 3 (Ingest, Query, Lint)
- **Workflows:** 8 across all sub-skills
- **Dependencies:** None (works with any markdown-capable assistant)

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "create a wiki map for [topic]" | Routes to Ingest -- runs CreateWikiMap workflow (content read-only) |
| "create a new wiki for [topic]" | Routes to Ingest -- runs CreateWikiMap workflow (content read-only) |
| "organize these files into a wiki" | Routes to Ingest -- runs CreateWikiMap workflow (content read-only) |
| "ingest this article into the wiki" | Routes to Ingest -- runs IngestSingle workflow (synthesis) |
| "process these 5 sources" | Routes to Ingest -- runs IngestBatch workflow (synthesis) |
| "add this webclip to the wiki" | Routes to Ingest -- runs IngestSingle workflow (synthesis) |
| "what does the wiki say about X?" | Routes to Query -- runs Search or DeepQuery workflow |
| "synthesize everything we know about X" | Routes to Query -- runs DeepQuery workflow |
| "save that answer as a wiki page" | Routes to Query -- runs FileAnswer workflow |
| "search the wiki for Y" | Routes to Query -- runs Search workflow |
| "health check the wiki" | Routes to Lint -- runs FullSweep workflow |
| "find orphan pages" | Routes to Lint -- runs QuickCheck workflow |
| "check for contradictions" | Routes to Lint -- runs QuickCheck workflow |
| "lint the wiki" | Routes to Lint -- runs FullSweep workflow |

---

## Example Usage

### Creating a Wiki Map

```
User: create a wiki map from my health-notes folder

AI responds:
Running the **CreateWikiMap** workflow in the **Ingest** skill...

Directory scan: health-notes/
Files found: 12
Need to move to references/: 10

| File | Current Location | Proposed Name |
|------|-----------------|---------------|
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

Next steps:
- Review the wiki map in INDEX.md
- Refine kind/ tags where the default doesn't fit
- Tell me to "ingest" a specific file when you want synthesis
```

### Ingesting a Source

```
User: ingest this article on vitamin D and sleep into the health wiki

AI responds:
Running the **IngestSingle** workflow in the **Ingest** skill...

Reading source... Key takeaways:
1. Vitamin D deficiency correlates with poor sleep quality
2. Optimal levels: 40-60 ng/mL
3. Dr. Smith's 2024 study: 500-person cohort

Actions taken:
- Created: references/vitamin-d-and-sleep.md (kind/research)
- Created: references/dr-smith-profile.md (kind/relationship)
- Updated: references/sleep-quality-factors.md (added vitamin D section)
- Updated: references/supplement-comparison.md (added vitamin D data)
- Updated: INDEX.md (4 entries added/modified)
- Appended: references/LOG.md
```

### Querying the Wiki

```
User: what supplements affect sleep quality according to the wiki?

AI responds:
Running the **DeepQuery** workflow in the **Query** skill...

Based on 6 wiki pages:

**Supplements with evidence for sleep quality:**
1. Magnesium — [[magnesium-and-sleep]]: 3 studies cited, strongest evidence
2. Vitamin D — [[vitamin-d-and-sleep]]: correlation with deficiency
3. Melatonin — [[melatonin-overview]]: direct mechanism, timing-dependent

**Contradictions noted:**
- [[dr-jones-review]] claims magnesium effect is placebo;
  [[magnesium-and-sleep]] cites controlled trials showing significance

Sources: 6 pages, 4 original webclips
```

### Linting the Wiki

```
User: health check the wiki

AI responds:
Running the **FullSweep** workflow in the **Lint** skill...

Wiki health report for health-wiki/:
- Pages: 47 | Sources: 23 | Orphans: 3 | Contradictions: 1

Issues found:
1. ORPHAN: references/zinc-dosage.md — no inbound links
2. ORPHAN: references/old-sleep-study.md — no inbound links
3. ORPHAN: references/draft-notes.md — no inbound links
4. CONTRADICTION: references/magnesium-and-sleep.md vs
   references/dr-jones-review.md — conflicting efficacy claims
5. MISSING PAGE: "circadian rhythm" mentioned in 4 pages but has no own page
6. STALE: references/supplement-prices.md — date_updated 6 months ago

Suggested actions: [list of fixes with commands]
```

---

## Frontmatter Convention

Every wiki page uses YAML frontmatter with four tag axes:

| Axis | Question | Required | Examples |
|------|----------|----------|---------|
| `area/ea` | Which system component? | Always | Applied to every wiki page |
| `kind/*` | What is this file? | Always | `kind/research`, `kind/webclip`, `kind/relationship`, `kind/log` |
| `status/*` | Where in the workflow? | Always | `status/open`, `status/stable`, `status/draft` |
| `pty/*` | How urgent? | Actionable kinds only | `pty/p1`, `pty/p2`, `pty/p3` |

Tags always appear in order: `area` -> `kind` -> `status` -> `pty`.

**Valid `kind/*` values:** wiki, research, relationship, webclip, log, plan, idea, playbook, blog, tracking, project/{name}, task, template, hygiene, bug, role, random.

**Valid `status/*` values:** draft, open, stable, blocked, parked, closed.

**Valid `pty/*` values:** p1 (urgent), p2 (normal), p3 (low). Only for actionable kinds: task, bug, plan, project/{name}, hygiene.

---

## Configuration

No configuration required. The skill works with any directory of markdown files.

Optional per-wiki configuration lives in each wiki's INDEX.md frontmatter (the `kind/wiki` tag identifies it as a wiki root).

---

## Customization

| Customization | Where | Impact |
|---------------|-------|--------|
| Tag taxonomy | Plan document label model | Add new `kind/*` or `status/*` values |
| Page template | Ingest workflows | Change default page structure |
| Lint rules | Lint workflows | Add or disable specific health checks |
| Query output formats | Query workflows | Add new synthesis formats |
