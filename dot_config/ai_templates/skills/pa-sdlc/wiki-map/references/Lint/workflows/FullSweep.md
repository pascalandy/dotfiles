# FullSweep Workflow

Comprehensive health check of the entire wiki. Read every page, validate against the shared schema, and report findings by severity.

## When to Use

- periodic maintenance
- after batch ingestion
- before relying on the wiki for an important analysis
- user says "health check the wiki", "lint the wiki", or "full sweep"

## Steps

### 1. Orientation and Read Set

- read the meta-skill `references/SCHEMA.md`
- read `INDEX.md`
- read the last 30 entries of `references/LOG.md`
- read any rotated `LOG-YYYY.md` files when checking rotation sanity or overlap
- check for subdirectory drift against the recent log; note it, do not normalize it, and ask whether `INDEX.md` should reflect it if drift is detected
- discover nested child wiki boundaries: any directory under `references/` that already contains its own `INDEX.md`
- read every page listed in the current wiki `INDEX.md`
- for each nested child wiki boundary, read the child `INDEX.md` and lint that child boundary recursively instead of expecting the parent `INDEX.md` to inline the child's leaf pages
- scan `references/` for local files missing from `INDEX.md`, excluding files that belong to a nested child wiki boundary

### 2. Run Checks

Run all of these checks:

- **INDEX integrity**
  - local files in `references/` missing from `INDEX.md`
  - phantom `INDEX.md` entries pointing to missing files
  - missing parent routes to direct child wiki `INDEX.md` files
  - stale or inaccurate INDEX descriptions, including direct child wiki route descriptions
  - do not flag a parent as stale just because it does not list a child wiki's leaf pages
  - plain directories without their own `INDEX.md` stay ordinary content and must still be indexed directly

- **Frontmatter and tag validation**
  - required fields present
  - `date_created` present, not in the future, and not later than `date_updated`
  - tag axis order is `area -> kind -> topic -> status -> pty`
  - valid `kind/*`, `topic/*`, `status/*`, `pty/*` values

- **Cross-reference health**
  - broken wikilinks
  - orphan pages
  - orphan webclips not referenced in any page's `sources:`
  - missing cross-references
  - content pages below the outbound-link minimum as warnings
  - operational pages below the soft outbound-link minimum as info

- **Contradictions and provenance**
  - unresolved contradictions from `contradictions:` frontmatter
  - broken `sources:` entries pointing to missing pages
  - `kind/project`, `kind/doc`, and `kind/query` pages missing `sources:`

- **Content structure**
  - pages over 200 lines
  - thin pages that likely should merge elsewhere
  - missing pages implied by repeated references

- **Aging and operational health**
  - stale pages older than 180 days when open or stable
  - active `LOG.md` approaching or exceeding 500 entries
  - `INDEX.md` sections over 50 entries
  - total `INDEX.md` entries over 200
  - post-crash batch inconsistencies between `LOG.md`, filesystem, and `INDEX.md`
  - `LOG.md` and rotated logs with overlapping date ranges

Closed pages are excluded from orphan, stale, and weak-link checks but still included in contradiction and frontmatter validation.

If total `INDEX.md` entries exceed 200:
- recommend creating or regenerating `references/_meta/topic-map.md`
- offer to generate it
- if the file already exists and may contain user edits, ask for confirmation before overwriting it

When nested child wikis are present:
- validate each child wiki boundary on its own terms
- validate that the parent routes only to direct child `INDEX.md` files
- do not flatten grandchild or deeper leaf pages into the parent read model

### 3. Produce Health Report

Report issues by severity using the ordering defined in `Lint/MetaSkill.md`.

```markdown
## Wiki Health Report: {wiki name}

**Date:** {today}
**Pages:** {total} | **Sources:** {webclip count} | **Last ingest:** {from LOG.md}

### Critical
{numbered list}

### Warning
{numbered list}

### Info
{numbered list}

### Suggested Actions
1. {specific fix}
2. {specific fix}
```

### 4. Update LOG.md

```markdown
- [[{today}]] lint | full sweep | {total issues} issues: {critical} critical, {warnings} warnings, {info} info
```

### 5. Offer to Fix

Offer automatic fixes only for low-risk issues such as:
- INDEX drift
- safe tag corrections
- missing cross-references

Keep contradictions, provenance problems, and stale-content decisions for explicit review.
