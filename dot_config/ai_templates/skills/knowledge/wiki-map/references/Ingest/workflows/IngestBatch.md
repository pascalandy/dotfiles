# IngestBatch Workflow

Process multiple sources into the wiki as one atomic plan-then-write operation.

## When to Use

- Adding several sources at once
- Bulk import of webclips, articles, notes, or transcripts
- User says "process these sources", "batch ingest", "ingest all of these"

## Core Rule

This workflow is not sequential per-source ingestion. It is atomic:

1. Read everything
2. Plan everything
3. Apply one write pass
4. Append one summary log entry

## Workflow

### Phase 1. Orientation

1. Read the meta-skill `references/SCHEMA.md`
2. If the wiki exists, read `INDEX.md` and the last 30 entries of `references/LOG.md`
3. If the wiki has 100 or more pages, search for the current request topic before planning any new pages
4. Check for subdirectory drift against the recent log; note it, do not normalize it, and ask whether `INDEX.md` should reflect it if drift is detected
5. Inventory the sources to be processed
6. In interactive mode, confirm scope with the user

```markdown
## Batch Ingest Plan

| # | Source | Status |
|---|--------|--------|
| 1 | {filename or title} | pending |
| 2 | {filename or title} | pending |
| 3 | {filename or title} | pending |

Proceed with batch ingestion?
```

In automated mode, skip the conversational confirmation but still honor the mass-update gate later.

### Phase 2. Read All Sources

1. Read every source file
2. Extract entities, concepts, claims, and relationships from each
3. Build one unified discovery map in memory covering:
   - all entities across all sources
   - all concepts across all sources
   - all cross-source relationships
   - all source pages that must appear in `sources:`

### Phase 3. Plan All Writes

1. Search once for which entities and concepts already exist in the wiki
2. For each unique entity or concept, decide: create or update
3. Compute the full final state for every page to update
4. Resolve cross-references at planning time, including links between newly created pages
5. Resolve `sources:` frontmatter at planning time
6. Preserve `date_created` on existing pages and plan `date_created` plus `date_updated` for new pages
7. Plan `contradictions:` frontmatter updates anywhere conflicting claims are introduced
8. Enforce the schema's outbound-link minimums for both content kinds and operational kinds
9. Build one write plan containing:
   - pages to create with final content
   - pages to update with final content
   - one `INDEX.md` patch
   - one `LOG.md` entry

### Phase 4. Mass-Update Gate

If total pages touched, created plus updated, is 10 or more:
- stop after planning
- present the full page list
- ask for confirmation in interactive mode

In automated mode:
- halt
- append a log entry noting the gate trigger
- exit without writing page changes

### Phase 5. Write Once

1. Write all create pages
2. Write all update pages
3. Preserve `date_created`, bump `date_updated`, and write planned `contradictions:` updates
4. Update `INDEX.md` once
5. Append one `LOG.md` entry:

```markdown
- [[{today}]] ingest | batch-{N-sources} | created: [page-a, page-b], updated: [page-c, page-d], sources: [src-1, src-2]
```

6. Report all changes to the user in one summary

### Phase 6. Failure Handling

If any write in Phase 5 fails, the batch is in an undefined state.

The batch's `LOG.md` entry is the recovery marker for lint and human repair. If a write failure occurs after the log entry is written, lint can compare that real batch marker against filesystem and `INDEX.md` state to detect post-crash inconsistency.

## What Changed From v1

- No per-source progress loop
- No per-source `INDEX.md` updates
- No per-source `LOG.md` entries
- No final cross-reference sweep after writes; links are resolved during planning
- One plan, one write pass, one log entry
