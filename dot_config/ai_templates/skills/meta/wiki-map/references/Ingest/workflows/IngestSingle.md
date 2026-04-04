# IngestSingle Workflow

Process one source interactively into the wiki. The LLM reads the source, discusses key takeaways with the user, then integrates it into the wiki structure.

## When to Use

- Adding a single article, paper, transcript, or note
- User wants to stay involved and guide emphasis
- User says "ingest this", "process this article", "add this to the wiki"

## Steps

### 1. Read the Source

- Read the source file (or content provided by the user)
- If the source is a URL, ask the user to provide it as a webclip in `references/`
- Identify: key entities, concepts, claims, data points, relationships

### 2. Discuss with User

Present a brief summary:

```markdown
## Source Summary: {source title}

**Key takeaways:**
1. {takeaway 1}
2. {takeaway 2}
3. {takeaway 3}

**Entities identified:** {list of people, orgs, tools}
**Concepts:** {list of topics/themes}
**Notable claims:** {anything surprising or contradicting existing wiki content}

Shall I proceed with ingestion? Anything to emphasize or skip?
```

Wait for user confirmation or guidance before proceeding.

### 3. Create Webclip Page

If the source is external content, create a webclip page:

```yaml
---
name: {Source Title}
description: {One-line summary}
tags:
  - area/ea
  - kind/webclip
  - status/stable
date_updated: {today}
---
```

The webclip page preserves the source content as-is. It is a snapshot, not synthesized.

### 4. Create or Update Wiki Pages

For each key entity, concept, or theme:

- **If a page exists** -- update it with new information from this source. Add a section or extend existing sections. Add the source to the Related section.
- **If no page exists** -- create a new page with the appropriate `kind/` tag.

For each page touched:
- Add or update cross-references (`[[wikilinks]]`)
- Bump `date_updated`
- Ensure the `## Related` section includes relevant links

### 5. Update INDEX.md

Add new pages to the wiki map table. Update descriptions for modified pages if the scope changed. Bump `date_updated`.

### 6. Update LOG.md

Append an entry:

```markdown
- [[{today}]] ingest | {source-name} | {summary of all changes: pages created, pages updated}
```

### 7. Report to User

```markdown
## Ingestion Complete: {source title}

**Created:** {list of new pages}
**Updated:** {list of modified pages}
**Cross-references added:** {count}
**Contradictions flagged:** {any, or "none"}

LOG.md and INDEX.md updated.
```

## Handling Contradictions

If the new source contradicts existing wiki content:
1. Note the contradiction in both the new page and the existing page
2. Use a callout or dedicated section: `## Contradictions`
3. Cite both sources with dates
4. Do not silently overwrite -- flag for user review
