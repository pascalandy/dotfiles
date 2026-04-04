# FileAnswer Workflow

Save a synthesized answer back into the wiki as a new page, so explorations compound alongside ingested sources.

## When to Use

- After a DeepQuery produces a substantive answer
- User says "save that answer", "file this as a wiki page", "add this to the wiki"
- Any time a valuable synthesis should be preserved

## Steps

### 1. Determine Page Metadata

Ask (or infer from context):
- **Filename** -- kebab-case, descriptive (e.g., `magnesium-vs-zinc-comparison.md`)
- **Kind tag** -- typically `kind/research` for synthesized knowledge, but could be `kind/plan`, `kind/idea`, etc.
- **Status** -- typically `status/open` (can be refined later)

### 2. Format as Wiki Page

Convert the answer into standard wiki page format:

```yaml
---
name: {Title}
description: {One-line summary}
tags:
  - area/ea
  - kind/{type}
  - status/open
date_updated: {today}
---
```

Body:
- Start with a summary paragraph
- Include the synthesized content with `[[wikilinks]]` preserved
- Add citations as inline wikilinks
- End with `## Related` linking to all source pages

### 3. Check for Existing Page

Before writing, verify no existing page covers the same topic. If one does:
- Ask the user: merge into the existing page or create a separate page?
- If merging, follow the update pattern from IngestSingle step 4

### 4. Write the Page

Save to `references/{filename}.md` in the wiki directory.

### 5. Update INDEX.md

Add the new page to the wiki map table. Bump `date_updated`.

### 6. Update Cross-References

For each page cited in the answer, add a backlink to the new page in their `## Related` section (if not already present).

### 7. Update LOG.md

```markdown
- [[{today}]] query | {page-name} | Filed query answer as wiki page, cites {N} pages
```

### 8. Confirm to User

```markdown
## Filed: {page title}

Saved as `references/{filename}.md` (kind/{type}).
Cross-referenced with {N} existing pages.
INDEX.md and LOG.md updated.
```
