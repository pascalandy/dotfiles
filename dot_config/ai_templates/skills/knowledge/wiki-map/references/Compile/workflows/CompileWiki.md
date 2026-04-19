# CompileWiki Workflow

Promote implied-missing entities in the wiki into first-class pages and back-edit siblings with wikilinks, as one atomic plan-then-write operation.

## When to Use

- User says "compile the wiki", "compile wiki", "fill wiki gaps", "promote missing entities", "concept mining", or "is the wiki complete?"
- After a recent Lint report flagged `missing pages implied by repeated references`
- Mature wikis (50+ pages) where mining reveals entities repeated across many sources

## Not for

- External source ingestion -> use `Ingest/workflows/IngestSingle.md` or `Ingest/workflows/IngestBatch.md`
- Rebuilding `INDEX.md` routes after directory changes -> use `Lint/workflows/RecursiveUpdate.md`
- Health reporting -> use `Lint/workflows/FullSweep.md` or `Lint/workflows/QuickCheck.md`

## Core Rule

This workflow is atomic, not per-entity:

1. Orient
2. Gate on a recent Lint report
3. Survey Lint output + bare directories + per-entity reference counts
4. Mine in parallel for concrete-noun candidates
5. Plan + approval gate
6. One write pass with a recovery marker

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

### Phase 2. Lint Gate

1. Scan the last 30 LOG entries for a recent Lint marker:
   - `lint | full-sweep | ...` (preferred)
   - `lint | quick-check | ...` when the quick check covered implied-missing pages (acceptable)
2. "Recent" means within the last 20 LOG entries **and** 14 calendar days -- whichever is stricter.
3. If no recent marker is found, halt:

```text
Compile requires a recent Lint report.
- Run `lint | full sweep` first, then re-run compile.
- No files were read beyond orientation.
```

4. If a recent marker is found, read the Lint report it points to (stored either as a wiki page under `references/` or captured in the LOG entry body, depending on how Lint filed it).
5. Extract the Lint categories useful to Compile:
   - `missing pages implied by repeated references` (primary signal)
   - `thin pages` (candidates that may be absorbed or expanded)
   - `bloated pages over 200 lines` (quarry candidates -- likely hide multiple concepts)
   - `orphan pages` (may hide an implied parent concept)

### Phase 3. Survey

1. Build the candidate pool:
   - Seed with the `missing pages implied by repeated references` list from Lint.
   - Add bare directories (subdirectories that hold markdown files but lack their own `INDEX.md` and have no obvious organizing page).
   - For each candidate entity, record `{entity, ref_count, source_pages[]}` from the Lint report.
2. Prioritize the mining order:
   - bloated pages first (highest information density per read)
   - thin pages second (cheap to scan, may reveal hidden entities)
   - regular content pages third
3. Cap the survey at the top N mining targets. Default `N = 30`. Negotiate with the user if the wiki is very small or very large.
4. Emit a short survey summary:

```text
Survey:
- Lint implied-missing: {X} entities
- Bare directories: {Y}
- Mining targets (capped at {N}): {Z} pages
- Priority: bloated ({A}) -> thin ({B}) -> regular ({C})
```

### Phase 4. Mining (parallel fan-out)

1. Split the mining target list into batches of ~10 pages each.
2. Dispatch one worker per batch. **Harness-agnostic shape:**

   > Use skill `delegate-to-sub` to dispatch one worker per batch if the assistant supports subagent fan-out. Otherwise iterate sequentially. The worker contract below is identical either way.

3. Worker contract (fixed, do not vary between workers):

```text
INPUT
- list of wiki page paths to read
- the current entity candidate list from Phase 3

TASK
- read each page in the batch
- extract concrete-noun entities: people, tools, frameworks, named concepts, named events
- for each extracted entity, record which source pages reference it
- apply the concrete-noun test: nouns must name a discrete thing that could plausibly stand as a wiki page on its own. Reject generic adjectives, verbs, filler phrases, and bare topic words ("productivity", "health", "strategy") unless they are a named subject of a page
- detect the likely page kind from how the entity is used (`kind/project`, `kind/doc`, `kind/relationship`, `kind/reference`, or `topic/*`)

OUTPUT (one record per entity, JSON-like shape)
{
  entity: "Vitamin D",
  source_pages: ["sleep-quality-factors", "magnesium-and-sleep", "dr-smith-profile"],
  ref_count: 3,
  would_be_kind: "topic" | "project" | "doc" | "relationship" | "reference"
}
```

4. Merge worker outputs:
   - dedupe by entity name, normalized to kebab-case
   - union the `source_pages[]` arrays across batches
   - sum `ref_count` across batches (deduped by source page, to avoid double-counting the same page from two batches)
   - when workers disagree on `would_be_kind`, keep the most specific non-`topic` value; fall back to `topic` if there is no consensus
5. In sequential fallback, run the same contract one batch at a time and merge at the end.

### Phase 5. Planning + Approval Gate

1. Filter the merged candidate list against SCHEMA's page-creation rule (`../../SCHEMA.md#page-creation-thresholds`):
   - keep entities with `ref_count >= 2` (the 2+ sources rule), OR
   - keep entities flagged as the central subject of any source page
   - drop the rest (passing mentions, off-scope references)
2. For each surviving candidate, plan:
   - new page filename (kebab-case)
   - page kind (`kind/project`, `kind/doc`, `kind/relationship`, `kind/reference`, or a content kind justified by the mining record)
   - initial summary paragraph synthesized from its `source_pages[]` -- no fabrication; only claims that appear in the source pages
   - `sources:` frontmatter listing the same `source_pages[]`
   - back-edit list: which sibling pages should gain a `[[new-page]]` wikilink, and where (existing prose mention vs `## Related`)
3. Enforce SCHEMA's outbound-link minimums (`../../SCHEMA.md#outbound-wikilink-minimum`) for the chosen kind when drafting each new page.
4. Present the candidate table to the user:

```markdown
## Compile Plan

Lint report referenced: {date} ({full-sweep | quick-check})

| # | Entity | Ref Count | New Page | Kind | Siblings to Back-Edit |
|---|--------|-----------|----------|------|-----------------------|
| 1 | Vitamin D | 6 | vitamin-d.md | kind/topic | [[sleep-quality-factors]], [[magnesium-and-sleep]], [[dr-smith-profile]], ... |
| 2 | Dr. Smith | 4 | dr-smith-profile.md | kind/relationship | [[vitamin-d-and-sleep]], [[smith-2024-study]], ... |

Total new pages: {X}
Total sibling back-edits: {Y}
Total pages touched (X + Y): {T}
```

5. **Mass-Update Gate.** If `T >= 10`:
   - interactive mode: stop, present the table, ask for confirmation before writing
   - automated mode: halt, append a log entry noting the gate trigger, exit without writing
6. If `T < 10`, still show the table and proceed to Phase 6 on user confirmation in interactive mode; automated mode may proceed without conversational confirmation.

### Phase 6. Creation (one write pass)

1. **Write the LOG recovery marker first**, before any page write:

```markdown
- [[YYYY-MM-DD]] compile | start | planned: {X} new, {Y} back-edits (recovery marker)
```

2. Create all new pages in one pass. For each new page:
   - frontmatter with `area/ea`, chosen `kind/*`, `status/draft`, `date_created: {today}`, `date_updated: {today}`, `sources:` listing the source pages
   - summary paragraph synthesized from source pages (no fabrication)
   - body sections only when source material clearly supports them
   - `## Related` section listing the sibling back-edit targets
   - enforce SCHEMA outbound-link minimums for the chosen kind
3. Apply sibling back-edits in the same pass. For each sibling:
   - prefer inserting `[[new-page]]` into existing prose at the first mention of the entity
   - if no suitable prose mention exists, add the link under the sibling's `## Related` section
   - bump `date_updated` to `{today}` on every edited sibling
4. Patch `INDEX.md` once, grouping new entries under their correct `kind/*` sections. If any section exceeds 50 entries after the patch, flag it as a SCHEMA scaling signal for Lint -- do not split during Compile.
5. Append one final LOG entry that supersedes the recovery marker:

```markdown
- [[YYYY-MM-DD]] compile | done | created: [page-a, page-b], back-edited: [page-c, page-d], ref: lint-YYYY-MM-DD
```

6. Report the summary to the user in one message:

```markdown
## Compile Complete

- New pages: {X}
- Sibling back-edits: {Y}
- INDEX sections updated: {list}
- Lint report referenced: {date}
```

### Phase 7. Failure Handling

If any write in Phase 6 fails after the recovery marker was appended:
- the wiki is in an undefined state
- the recovery marker in `LOG.md` is the signal for Lint and human repair
- `Lint/workflows/QuickCheck.md` compares the recovery marker against filesystem and `INDEX.md` state to identify missing creates or incomplete back-edits
- do not attempt to auto-repair in Compile; defer to Lint

## What Compile Does Not Do

- Does not ingest external sources (Ingest's job)
- Does not re-run health checks (Lint's job)
- Does not rebuild `INDEX.md` routes from directory structure (RecursiveUpdate's job)
- Does not regenerate semantic ontology views (parked; future sub-skill)
- Does not loop per-entity through write passes -- Phase 6 is one atomic write
