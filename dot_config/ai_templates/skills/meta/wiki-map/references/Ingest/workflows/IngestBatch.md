# IngestBatch Workflow

Process multiple sources sequentially into the wiki with less supervision than IngestSingle.

## When to Use

- Adding several sources at once
- Bulk import of webclips, articles, or notes
- User says "process these sources", "batch ingest", "ingest all of these"

## Steps

### 1. Inventory Sources

List all sources to be processed:

```markdown
## Batch Ingest Plan

| # | Source | Status |
|---|--------|--------|
| 1 | {filename or title} | pending |
| 2 | {filename or title} | pending |
| ... | ... | ... |

Proceed with batch ingestion?
```

Wait for user confirmation.

### 2. Process Each Source

For each source, follow the IngestSingle workflow steps 1, 3, 4, 5, and 6 -- but skip step 2 (detailed discussion with user). Instead, provide a brief one-line summary per source as you go:

```markdown
[1/5] Ingested: {source title} — created 2 pages, updated 3 pages
[2/5] Ingested: {source title} — created 1 page, updated 2 pages, 1 contradiction flagged
...
```

### 3. Cross-Reference Pass

After all sources are processed, do a cross-reference sweep:
- Check if any newly created pages should link to each other
- Check if any existing pages should now reference newly created pages
- Add missing `[[wikilinks]]`

### 4. Final INDEX.md Update

Update INDEX.md once with all new and modified entries. Bump `date_updated`.

### 5. Final LOG.md Update

Append one summary entry per source:

```markdown
- [[{today}]] ingest | {source-1} | Created: {pages}, Updated: {pages}
- [[{today}]] ingest | {source-2} | Created: {pages}, Updated: {pages}
```

### 6. Report to User

```markdown
## Batch Ingestion Complete

**Sources processed:** {count}
**Pages created:** {count}
**Pages updated:** {count}
**Cross-references added:** {count}
**Contradictions flagged:** {count, with links}

INDEX.md and LOG.md updated.
```

## When to Pause

Stop batch processing and consult the user if:
- A source contradicts multiple existing pages (not just one)
- A source is ambiguous about scope or categorization
- A source would require creating more than 5 new pages (may indicate a scope boundary)
