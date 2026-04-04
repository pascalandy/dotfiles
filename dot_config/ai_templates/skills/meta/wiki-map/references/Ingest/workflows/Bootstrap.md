# Bootstrap Workflow

Initialize a new wiki instance with the required directory structure and seed files.

## When to Use

- Starting a new wiki for a topic, project, or research area
- User says "create a wiki", "new wiki", "init wiki", "bootstrap wiki"

## Steps

1. **Confirm scope** -- Ask the user:
   - What is this wiki about? (topic/domain)
   - What should we name the directory? (kebab-case)
   - Brief description for the INDEX.md

2. **Create directory structure:**

```
{wiki-name}/
  INDEX.md
  references/
    LOG.md
  assets/           # create only if the user mentions images/PDFs
```

3. **Write INDEX.md:**

```yaml
---
name: {Wiki Name}
description: {User-provided description}
tags:
  - area/ea
  - kind/wiki
date_updated: {today}
---
```

```markdown
## Wiki Map

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |
```

4. **Write references/LOG.md:**

```yaml
---
name: Log
description: Append-only operational log for {Wiki Name}
tags:
  - area/ea
  - kind/log
  - status/open
date_updated: {today}
---
```

```markdown
# Log

- [[{today}]] create | LOG.md | Wiki initialized
```

5. **Confirm to user** -- Report what was created and suggest next steps (e.g., "Add your first source to `references/` and tell me to ingest it").

## Output

- Directory structure created
- INDEX.md with frontmatter and empty wiki map table
- LOG.md with initialization entry
- Status message confirming creation
