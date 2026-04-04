# QuickCheck Workflow

Targeted health check for a specific issue type. Faster than FullSweep, focused on one category.

## When to Use

- User asks about a specific issue: "are there orphan pages?", "find contradictions"
- After ingesting a controversial source: "check for contradictions"
- Spot-checking: "any broken links?"

## Steps

### 1. Identify Check Type

Determine which category the user is asking about:

| User Request | Check Type |
|-------------|------------|
| "orphans", "orphan pages", "unlinked pages" | Orphans |
| "contradictions", "conflicts", "disagreements" | Contradictions |
| "stale", "outdated", "old pages" | Stale content |
| "missing pages", "red links", "broken links" | Missing/broken links |
| "cross-references", "missing links" | Missing cross-refs |
| "tags", "frontmatter", "metadata" | Tag issues |
| "index", "INDEX.md" | INDEX drift |

### 2. Read Required Pages

- For **orphan/cross-ref/broken links** checks: read all pages (need full link graph)
- For **contradictions**: read all pages (need to compare claims)
- For **stale content**: read all pages (need dates and content comparison)
- For **tag issues**: read all pages (need frontmatter from each)
- For **INDEX drift**: read INDEX.md and list `references/` directory

### 3. Run the Check

Execute only the specific check from FullSweep steps 2-5 that matches the request.

### 4. Report Results

```markdown
## QuickCheck: {check type}

**Wiki:** {wiki name} | **Pages scanned:** {count}

### Findings

{numbered list of issues found, with page links and details}

### Suggested Fixes

{specific actions to resolve each issue}
```

If no issues found:

```markdown
## QuickCheck: {check type}

**Wiki:** {wiki name} | **Pages scanned:** {count}

No issues found.
```

### 5. Update LOG.md

```markdown
- [[{today}]] lint | {check type} | {count} issues found
```

### 6. Offer to Fix

For issues that can be fixed automatically (tag corrections, missing cross-refs, INDEX updates), offer to apply fixes. For issues requiring judgment (contradictions, stale content), present options and wait for user direction.
