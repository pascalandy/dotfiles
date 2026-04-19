# QuickCheck Workflow

Targeted health check for one issue type. Faster than FullSweep, but still grounded in the shared schema.

## When to Use

- user asks about one specific issue type
- after a risky ingest
- spot-checking wiki integrity

## Steps

### 1. Identify the Check Type

Map the request to one check:

| User Request | Check Type |
|-------------|------------|
| "orphans", "orphan pages", "unlinked pages" | orphan pages |
| "orphan webclips", "sources", "provenance" | provenance and orphan webclips |
| "contradictions", "conflicts", "disagreements" | contradictions |
| "stale", "outdated", "old pages" | stale content |
| "missing pages", "red links", "broken links" | broken or missing links |
| "cross-references", "missing links", "underlinked", "few links", "thin links" | cross-reference health |
| "tags", "frontmatter", "metadata", "topic tags", "tag order", "axis order" | tag and frontmatter validation |
| "index", "INDEX.md", "index size", "huge index" | INDEX integrity and scaling |
| "log size", "rotate log" | LOG size and rotation |
| "big pages", "long pages", "split" | page size |
| "inconsistent batch", "recovery" | post-crash batch inconsistency |

### 2. Read What You Need

Always begin orientation for an existing wiki by reading:
- the meta-skill `references/SCHEMA.md`
- the wiki's `INDEX.md`
- the last 30 entries of `references/LOG.md`

Also check for subdirectory drift against the recent log; note it, do not normalize it, and ask whether `INDEX.md` should reflect it if drift is detected.

After orientation, read the smallest additional set that can answer the question:
- link, contradiction, stale, provenance, and tag checks usually require all pages
- INDEX checks require a directory inventory in addition to `INDEX.md`
- log checks require any rotated logs in addition to the active `LOG.md`
- index scaling checks should also inspect `references/_meta/topic-map.md` when it already exists

### 3. Run the Check

Run only the targeted check, using the same rules as FullSweep.

If the targeted check is INDEX scaling and the wiki exceeds 200 indexed pages:
- report whether `references/_meta/topic-map.md` is missing, stale, or present
- offer to create or regenerate it
- ask before overwriting an existing file that may contain user edits

### 4. Report Results

```markdown
## QuickCheck: {check type}

**Wiki:** {wiki name} | **Pages scanned:** {count}

### Findings
{numbered list}

### Suggested Fixes
{specific actions}
```

If nothing is wrong, say so explicitly.

### 5. Update LOG.md

```markdown
- [[{today}]] lint | {check type} | {count} issues found
```

### 6. Offer to Fix

Offer automatic fixes only for low-risk issues. For contradictions, provenance problems, and stale-content decisions, report first and wait for direction.
