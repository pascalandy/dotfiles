# FullSweep Workflow

Comprehensive health check of the entire wiki. Examines every page across all issue categories.

## When to Use

- Periodic maintenance (weekly, after batch ingestion)
- User says "health check the wiki", "lint the wiki", "full sweep"
- Before relying on the wiki for an important analysis

## Steps

### 1. Read All Pages

- Read INDEX.md
- Read every page listed in INDEX.md
- Scan `references/` directory for any files not in INDEX.md

### 2. Check INDEX Integrity

- **Missing from INDEX**: files in `references/` not listed in INDEX.md
- **Phantom entries**: INDEX.md entries pointing to files that do not exist
- **Stale descriptions**: INDEX.md description that no longer matches the page content

### 3. Check Frontmatter

For each page, verify:
- Required fields present: `name`, `description`, `tags`, `date_updated`
- Tag axes in correct order: `area` -> `kind` -> `status` -> `pty`
- All tag values are valid (per the label model)
- `area/ea` is present
- `kind/*` is present and appropriate
- `status/*` is present
- `pty/*` present only for actionable kinds

### 4. Check Cross-References

- **Orphan pages**: pages with zero inbound `[[wikilinks]]` from other pages (LOG.md and INDEX.md excluded from this check)
- **Broken links**: `[[wikilinks]]` pointing to pages that do not exist
- **Missing cross-refs**: pages covering related topics that do not link to each other (use topic overlap and shared entities as signals)

### 5. Check Content Quality

- **Contradictions**: claims in one page that conflict with claims in another. Cross-check factual assertions, dates, numbers, and causal claims.
- **Stale content**: pages with `date_updated` more than 3x older than the wiki average, or pages whose claims have been superseded by newer sources.
- **Missing pages**: concepts referenced via `[[wikilink]]` in 2+ pages that have no corresponding file.
- **Thin pages**: pages with less than 3 sentences of content (excluding frontmatter and Related section).

### 6. Produce Health Report

```markdown
## Wiki Health Report: {wiki name}

**Date:** {today}
**Pages:** {total} | **Sources:** {webclip count} | **Last ingest:** {from LOG.md}

### Summary

| Category | Count | Severity |
|----------|-------|----------|
| Contradictions | {n} | Critical |
| INDEX drift | {n} | Critical |
| Orphan pages | {n} | Warning |
| Missing pages | {n} | Warning |
| Stale content | {n} | Warning |
| Missing cross-refs | {n} | Info |
| Tag issues | {n} | Info |
| Thin pages | {n} | Info |

### Critical Issues

{numbered list with details, page links, and specific claims}

### Warnings

{numbered list with details and suggested fixes}

### Info

{numbered list with details}

### Suggested Actions

1. {specific fix with command or instruction}
2. {specific fix}
...

### Suggested Sources

{if gaps were found, suggest what sources could fill them}
```

### 7. Update LOG.md

```markdown
- [[{today}]] lint | full sweep | {total issues} issues: {critical} critical, {warnings} warnings, {info} info
```

### 8. Offer to Fix

After presenting the report:

```
Want me to fix the Info-level issues automatically? (tag fixes, missing cross-refs, INDEX updates)
Critical and Warning issues require your review before changes.
```
