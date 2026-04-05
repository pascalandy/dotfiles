---
name: ingest
description: Process sources into an LLM-maintained wiki -- bootstrap new wikis, ingest single sources interactively, or batch-process multiple sources. USE WHEN ingest, process source, add source, add to wiki, webclip, batch ingest, create wiki, bootstrap wiki, init wiki, new wiki, process article, add article, new source.
---

## Customization

If the current assistant supports user-specific overrides, apply them before execution. Otherwise, use the defaults in this folder.

## Status Update

Before executing, emit a brief text status update such as:
`Running the **WorkflowName** workflow in the **Ingest** skill to ACTION...`

# Ingest

Two distinct operations live here: **organizing files** (CreateWikiMap) and **processing sources** (IngestSingle, IngestBatch). They have different rules.

## Critical Guardrail: Organize vs Process

**CreateWikiMap is read-only on file body content.** It moves files, renames them, adds frontmatter, and builds the index. It never reads file bodies for synthesis, never rewrites content, never adds cross-references to existing text. The user's files come out with the same body they went in with.

**IngestSingle and IngestBatch are write operations.** They read a source, synthesize key information, and integrate it into the wiki structure. These only run when the user explicitly asks to "ingest" or "process" a specific source.

Never conflate the two. When the user says "create a wiki" or "organize these files", that is CreateWikiMap. When the user says "ingest this article" or "process this source", that is IngestSingle/IngestBatch.

## Core Concept (Ingest only)

Ingestion is not indexing. The LLM does not store the source for later retrieval. It reads the source, synthesizes the key information, and writes it into the wiki's structure. A single source might touch 10-15 wiki pages. The cross-references are built at ingest time, not at query time.

**New page vs update:** If the source covers an entity or concept that already has a page, update the existing page. If it covers a distinct subtopic, create a new page and cross-link it. Webclips (`kind/webclip`) always get their own page -- they are source snapshots, not synthesized content.

## When to Use

- **Organizing existing files into a wiki** -- CreateWikiMap scans, moves, renames, builds index (content untouched)
- **Starting an empty wiki** -- CreateWikiMap handles this too (empty-directory case)
- **Adding a web article** -- IngestSingle processes it interactively with discussion
- **Processing research papers** -- IngestSingle for deep engagement, IngestBatch for volume
- **Bulk import** -- IngestBatch processes multiple sources sequentially with less supervision
- **Adding meeting notes, transcripts, journal entries** -- any text source

## Workflow Routing

Route to the appropriate workflow based on the request.

**When executing a workflow, output this notification directly:**

```
Running the **WorkflowName** workflow in the **Ingest** skill to ACTION...
```

- Create a wiki map / organize existing files / new wiki -> `workflows/CreateWikiMap.md`
- Process one source interactively (user explicitly asks to ingest) -> `workflows/IngestSingle.md`
- Process multiple sources in sequence (user explicitly asks to ingest) -> `workflows/IngestBatch.md`

## Wiki Structure Reference

Each wiki instance follows this structure:

```
{wiki-name}/
  INDEX.md              # Content catalog (tags: area/ea, kind/wiki)
  references/           # All wiki pages (move existing dirs intact, never flatten or reorganize)
    LOG.md              # Append-only operational log (kind/log)
    {page-name}.md      # Entity, concept, research, webclip pages
  assets/               # Images, PDFs, non-markdown files (optional)
```

## Page Template

Every wiki page follows this template:

```yaml
---
name: Short human-readable title
description: One-line summary of what this page covers
tags:
  - area/ea
  - kind/{type}
  - status/open
date_updated: YYYY-MM-DD
---
```

Body starts with a summary paragraph, then sections as needed, ending with:

```markdown
## Related

- [[other-page]]
- [[another-page]]
```

## INDEX.md Format

```yaml
---
name: Wiki Name
description: One-line description of this wiki's scope
tags:
  - area/ea
  - kind/wiki
date_updated: YYYY-MM-DD
---
```

Followed by a table cataloging every page:

```markdown
## Wiki Map

| File | Description |
|------|-------------|
| `references/page-name.md` | One-line description |
```

## LOG.md Format

Append-only. Each entry is a markdown list item:

```markdown
- [[YYYY-MM-DD]] {operation} | {page} | {summary of changes}
```

Operations: `ingest`, `query`, `lint`, `update`, `create`.

## Tag Reference

Tags follow four axes in order: `area` -> `kind` -> `status` -> `pty`.

- **area/ea** -- applied to every wiki page
- **kind/** -- what the file is (wiki, research, relationship, webclip, log, plan, idea, etc.)
- **status/** -- workflow state (draft, open, stable, blocked, parked, closed)
- **pty/** -- priority, only for actionable kinds (p1, p2, p3)

## Naming Convention

- Filenames use **kebab-case**: `vitamin-d-and-sleep.md`
- Cross-references use **Obsidian wikilinks**: `[[vitamin-d-and-sleep]]`

## Principles

1. **Synthesize, don't index** -- write the knowledge into the wiki structure, not just store the source
2. **Update over duplicate** -- extend existing pages rather than creating redundant ones
3. **Cross-reference aggressively** -- every page should link to related pages
4. **Bump date_updated** -- on any content change to any page
5. **Log everything** -- every ingest operation gets a LOG.md entry
6. **Webclips are sacred** -- source snapshots get their own page, never merged into synthesized pages
