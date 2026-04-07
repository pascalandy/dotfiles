# FileAnswer Workflow

Save a synthesized answer back into the wiki as a new page so the answer compounds instead of disappearing into chat history.

## When to Use

- After a DeepQuery produces a substantive answer
- User says "save that answer", "file this as a wiki page", or "add this to the wiki"

## Steps

### 0. Orientation

- Read the meta-skill `references/SCHEMA.md`
- Read the wiki's `INDEX.md`
- Read the last 30 entries of `references/LOG.md`
- If the wiki has 100 or more pages, search for the current request topic before planning a new page
- Check for subdirectory drift against the recent log; note it, do not normalize it, and ask whether `INDEX.md` should reflect it if drift is detected

### 1. Wiki-Worthy Judgment

File the answer when:
- re-deriving it would require reading 3 or more pages
- it is a useful comparison, synthesis, timeline, or decision record
- the user explicitly asks to save it

Do not file when:
- it is a simple lookup from one page
- it mostly restates an existing page

If the answer is not worth filing, offer to add a short note or backlink to an existing page instead.

### 2. Determine Metadata

- Choose a descriptive kebab-case filename
- Use `kind/query`
- Use `status/open` unless there is a better status from context
- Add `topic/*` only when it clarifies the subject

### 3. Format as a Wiki Page

Use v2 frontmatter:

```yaml
---
name: {Title}
description: {One-line summary}
tags:
  - area/ea
  - kind/query
  - status/open
date_created: {today}
date_updated: {today}
sources:
  - page-a
  - page-b
---
```

Body rules:
- start with a summary paragraph
- preserve inline `[[wikilinks]]`
- end with `## Related`
- satisfy the outbound-link minimum for content kinds

### 4. Check for Existing Coverage

If an existing page already covers the same topic, ask whether to merge into it or keep a separate filed answer.

### 5. Respect the Mass-Update Gate

If filing the answer would touch 10 or more total pages, counting the new `kind/query` page plus any existing pages to update, stop and ask for confirmation before writing.

In automated mode, halt, append a log entry noting the gate trigger, and exit without writing.

### 6. Write the Page and Update Links

- save the new page under `references/`
- add it to `INDEX.md`
- add backlinks from cited pages when appropriate

### 7. Log the Action

```markdown
- [[{today}]] query | {page-name} | Filed query answer as wiki page, cites {N} pages
```

### 8. Confirm to User

```markdown
## Filed: {page title}

Saved as `references/{filename}.md` (kind/query).
Cross-referenced with {N} existing pages.
INDEX.md and LOG.md updated.
```
