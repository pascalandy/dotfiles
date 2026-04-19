# CompileWiki Workflow

Promote implied-missing entities in the wiki into first-class pages and back-edit siblings with wikilinks, as one atomic plan-then-write operation.

## When to Use

- User says "compile the wiki", "compile wiki", "fill wiki gaps", "promote missing entities", "concept mining", or "is the wiki complete?"
- After a recent Lint full sweep or quick check has left a marker in `LOG.md`
- Mature wikis (50+ pages) where mining reveals entities repeated across many sources

## Not for

- External source ingestion -> use `Ingest/workflows/IngestSingle.md` or `Ingest/workflows/IngestBatch.md`
- Rebuilding `INDEX.md` routes after directory changes -> use `Lint/workflows/RecursiveUpdate.md`
- Health reporting -> use `Lint/workflows/FullSweep.md` or `Lint/workflows/QuickCheck.md`

## Core Rule

This workflow is atomic, not per-entity:

1. Orient
2. Gate on a recent Lint marker in `LOG.md`
3. Survey (focused scan for Compile-specific signals)
4. Mine in parallel for concrete-noun candidates
5. Plan + approval gate
6. One write pass with a recovery marker, plus failure handling

## Workflow

### Phase 1. Orientation

1. Read the meta-skill `../../SCHEMA.md`.
2. Read the wiki's `INDEX.md`.
3. Read the last 30 entries of the wiki's `references/LOG.md`.
4. Check subdirectory drift against the recent log. Note drift, do not normalize it, and ask whether `INDEX.md` should reflect it if drift is detected.
5. Emit orientation summary:

```text
Oriented: {wiki-name} | {N} pages | {M} recent log entries | {drift status}
```

### Phase 2. Lint Gate (freshness precondition)

Compile trusts structural assumptions -- valid INDEX, valid tags, no phantom entries, no post-crash batch inconsistency. Those assumptions are validated by Lint. A recent Lint marker in `LOG.md` is the signal that the wiki is in known-good shape.

1. Scan the last 30 LOG entries for a recent Lint marker. Lint's actual entry formats are:
   - `- [[{date}]] lint | full sweep | {count} issues: {n} critical, {n} warnings, {n} info` (from `FullSweep.md`)
   - `- [[{date}]] lint | {check type} | {count} issues found` (from `QuickCheck.md`)
2. "Recent" means within the last 20 LOG entries **and** within 14 calendar days -- whichever is stricter.
3. Prefer a full-sweep marker. A quick-check marker is acceptable only when it covered a check type relevant to Compile's preconditions (`missing pages`, `cross-references`, `tag and frontmatter validation`, `INDEX integrity`).
4. If no recent marker is found, halt without reading further:

```text
Compile requires a recent Lint pass.
- Run a Lint full sweep first (for example: "health check the wiki"), then re-run compile.
- No files beyond orientation were read.
```

5. If a recent marker is found but Lint reported unresolved `critical` issues in its most recent LOG line counts, warn the user and offer to proceed or halt. Critical issues typically break the assumptions Compile relies on.

Compile does not read a persisted Lint report. Lint reports are conversational, not filed. Compile performs its own focused survey in Phase 3.

### Phase 3. Survey (focused scan)

Scope is narrower than a Lint full sweep. Scan only the signals Compile needs.

1. Identify survey targets:
   - every page listed in `INDEX.md` (content and operational pages)
   - bare directories under `references/` (subdirectories holding markdown files but lacking their own `INDEX.md` and lacking an organizing page)
2. Rank mining priority:
   - bloated pages over 200 lines first (highest information density per read)
   - thin pages second (cheap to scan, may reveal hidden entities)
   - regular content pages third
3. Cap the mining target list at the top `N` pages. Default `N = 30`. Offer to raise or lower with the user if the wiki is very small or very large.
4. Emit a short survey summary:

```text
Survey:
- Pages in scope: {total}
- Bloated (>200 lines): {A}
- Thin: {B}
- Bare directories: {C}
- Mining targets (capped at N={N}): {Z} pages
- Priority order: bloated -> thin -> regular
```

### Phase 4. Mining (parallel fan-out)

1. Split the mining target list into batches of ~10 pages each.
2. Dispatch one worker per batch. Harness-agnostic shape:

   > Use skill `delegate-to-sub` to dispatch one worker per batch when the assistant supports sub-agent fan-out. Otherwise iterate batches sequentially. The worker contract below is identical either way.

3. Worker contract (fixed, do not vary between workers):

```text
INPUT
- list of wiki page paths to read
- the current candidate list from Phase 3 orientation (for deduping and context)

TASK
- read each page in the batch
- extract concrete-noun entities: named people, tools, frameworks, concepts, events
- for each extracted entity, record which source pages in the batch reference it
- apply the concrete-noun test: the entity must name a discrete thing that could plausibly
  stand as a wiki page on its own. Reject generic adjectives, verbs, filler phrases, and
  bare topic words ("productivity", "health", "strategy") unless they are the named subject
  of at least one page
- suggest a kind for a future page based on how the entity is used: content pages are
  kind/doc or kind/project. If the entity is primarily about a person or ongoing
  relationship, tag it topic/relationship on a kind/doc page (kind/relationship is
  deprecated per SCHEMA)

OUTPUT (one record per entity, JSON-like shape)
{
  entity: "vitamin-d",
  source_pages: ["sleep-quality-factors", "magnesium-and-sleep", "dr-smith-profile"],
  ref_count: 3,
  suggested_kind: "doc" | "project",
  suggested_topic: "relationship" | "strategy" | "playbook" | null
}
```

4. Merge worker outputs:
   - dedupe by entity name, normalized to kebab-case
   - union `source_pages[]` across batches
   - recompute `ref_count` as the size of the unioned `source_pages[]` (so a page counted twice across batches contributes once)
   - when workers disagree on `suggested_kind`, prefer `project` for entities that look like ongoing initiatives, otherwise default to `doc`
5. In sequential fallback, run the same contract one batch at a time and merge at the end. Output shape is identical.

### Phase 5. Planning + Approval Gate

1. Filter the merged candidate list against SCHEMA's page-creation rule (`../../SCHEMA.md#page-creation-thresholds`):
   - keep entities with `ref_count >= 2` (the 2+ sources rule), OR
   - keep entities flagged as the central subject of any source page
   - drop the rest (passing mentions, off-scope references)
2. For each surviving candidate, plan:
   - new page filename in kebab-case
   - page kind: `kind/doc` by default, `kind/project` when the entity is an ongoing initiative with clear scope
   - `topic/*` tag when applicable (`topic/relationship`, `topic/strategy`, `topic/playbook`, `topic/reference`, or a domain-specific `topic/{name}`)
   - initial summary paragraph synthesized from `source_pages[]` -- no fabrication; only claims that appear in the source pages
   - `sources:` frontmatter listing the same `source_pages[]`
   - back-edit list: which sibling pages should gain a `[[new-page]]` wikilink, and where (existing prose mention preferred, `## Related` as fallback)
3. Enforce SCHEMA's outbound-link minimums (`../../SCHEMA.md#outbound-wikilink-minimum`) for the chosen kind when drafting each new page.
4. Present the candidate table to the user:

```markdown
## Compile Plan

Lint marker referenced: [[{lint-date}]] ({lint | full sweep} | lint | {check type})

| # | Entity | Ref Count | New Page | Kind | Topic Tag | Siblings to Back-Edit |
|---|--------|-----------|----------|------|-----------|-----------------------|
| 1 | Vitamin D | 6 | vitamin-d.md | kind/doc | topic/reference | [[sleep-quality-factors]], [[magnesium-and-sleep]], [[dr-smith-profile]] |
| 2 | Dr. Smith | 4 | dr-smith-profile.md | kind/doc | topic/relationship | [[vitamin-d-and-sleep]], [[smith-2024-study]] |

Total new pages: {X}
Total sibling back-edits: {Y}
Total pages touched (X + Y): {T}
```

5. **Mass-Update Gate.** If `T >= 10`:
   - interactive mode: stop, present the table, ask for confirmation before writing
   - automated mode: halt, append a log entry noting the gate trigger, exit without writing
6. If `T < 10`, still show the table. In interactive mode, proceed to Phase 6 on user confirmation. In automated mode, proceed without conversational confirmation.

### Phase 6. Creation (one write pass)

All writes happen in one pass after the recovery marker is appended.

1. **Append the LOG recovery marker first**, before any page write:

```markdown
- [[{today}]] compile | start | planned: {X} new pages, {Y} back-edits (recovery marker)
```

2. Create all new pages. For each new page:
   - frontmatter with `area/ea`, chosen `kind/*`, optional `topic/*`, `status/draft`, `date_created: {today}`, `date_updated: {today}`, and `sources:` listing the source pages
   - tag axis order: `area -> kind -> topic -> status -> pty` (SCHEMA)
   - summary paragraph synthesized from the source pages (no fabrication)
   - body sections only where the source material clearly supports them
   - `## Related` section listing the sibling back-edit targets
   - enforce SCHEMA outbound-link minimums for the chosen kind
3. Apply sibling back-edits. For each sibling:
   - prefer inserting `[[new-page]]` into existing prose at the first mention of the entity
   - if no suitable prose mention exists, add the link under the sibling's `## Related` section
   - bump `date_updated` to `{today}` on every edited sibling
4. Patch `INDEX.md` once, grouping new entries under their correct `kind/*` sections. If any section would exceed 50 entries after the patch, flag it as a SCHEMA scaling signal for Lint -- do not split during Compile.
5. Append one final LOG entry that supersedes the recovery marker:

```markdown
- [[{today}]] compile | done | created: [page-a, page-b], back-edited: [page-c, page-d], ref: [[{lint-date}]]
```

6. Report the summary to the user in one message:

```markdown
## Compile Complete

- New pages: {X}
- Sibling back-edits: {Y}
- INDEX sections updated: {list}
- Lint marker referenced: [[{lint-date}]]
```

#### Failure Handling

If any write after the recovery marker fails, the wiki is in an undefined state.

- The recovery marker in `LOG.md` is the signal for Lint and human repair.
- `Lint/workflows/QuickCheck.md` compares the recovery marker against filesystem and `INDEX.md` state to identify missing creates or incomplete back-edits (check type: `post-crash batch inconsistency`).
- Compile does not attempt to auto-repair. Defer to Lint.

## What Compile Does Not Do

- Does not ingest external sources (Ingest's job)
- Does not re-run health checks (Lint's job)
- Does not rebuild `INDEX.md` routes from directory structure (`RecursiveUpdate`'s job)
- Does not regenerate semantic ontology views (parked; future sub-skill)
- Does not loop per-entity through write passes -- Phase 6 is one atomic write
