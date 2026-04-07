# CreateWikiMap Workflow

Organize existing files into a wiki structure. Scan a directory, move files into `references/`, rename to kebab-case, add frontmatter where missing, and build `INDEX.md` plus `LOG.md`.

**This workflow is read-only on file body content. No synthesis, no rewriting, no summarization. Only frontmatter, file location, and filenames may change.**

## When to Use

- Turning an existing directory of markdown files into a wiki
- Creating a brand new empty wiki
- User says "create a wiki map", "create wiki", "bootstrap wiki", "init wiki", "organize these files into a wiki"

## Steps

### 0. Read SCHEMA and Detect Existing Wiki

Always read the meta-skill `references/SCHEMA.md` first.

Then inspect the target directory:
- Empty directory -> proceed
- Has files but no `INDEX.md` -> proceed in organize mode
- Has `INDEX.md` with v1 markers such as missing `date_created`, missing `sources:` on content pages, or `kind/relationship` tags -> halt and report: `This looks like a v1 wiki. Run UpgradeSchema instead.`
- Has `INDEX.md` already following v2 conventions -> halt and report: `Wiki already exists. Nothing to do.`

Never auto-upgrade an existing wiki from this workflow.

### 1. Confirm Scope

Ask the user:
- Which directory are we organizing?
- If creating a new wiki, what should we name it?
- What one-line description should go in `INDEX.md`?

If the directory exists, present a scan summary and wait for confirmation before moving anything.

```markdown
## Directory Scan: {path}

**Files found:** {count}
**Already in references/:** {count}
**Need to move:** {count}
**Subdirectories to preserve:** {list}

| File | Current Location | Proposed Name |
|------|------------------|---------------|
| My Article.md | ./ | references/my-article.md |
| notes_on_sleep.md | ./ | references/notes-on-sleep.md |
| z_varia/old-draft.md | z_varia/ | references/z_varia/old-draft.md |
| references/already-here.md | references/ | no change |

Proceed?
```

This confirmation is mandatory even in automated mode. If no human can confirm, halt without changing files.

### 2. Create Directory Structure

```text
{wiki-name}/
  INDEX.md
  references/
    LOG.md
  assets/           # only if non-markdown files exist
```

If the directory already exists, create only what is missing.

### 3. Move Everything into references/

- Move every existing file and subdirectory from the wiki root into `references/`
- Preserve the existing structure exactly
- Never flatten, normalize, or reorganize subdirectories
- Rename markdown files to kebab-case after the move
- If there is a collision, append a suffix such as `-2`
- Keep `INDEX.md` at the root
- Keep `AGENTS.md` at the root if present
- Do not read deeply into body content and do not modify it

### 4. Add Frontmatter Where Missing

For each markdown file in `references/`:

- If frontmatter already exists: leave it untouched
- If frontmatter is missing: prepend minimal v2 frontmatter

Use this template:

```yaml
---
name: {derived from filename}
description: {first heading or filename}
tags:
  - area/ea
  - kind/research
  - status/open
date_created: {today}
date_updated: {today}
---
```

Notes:
- Use `kind/webclip` if the file clearly looks like a clipped article or source snapshot
- Include an empty `topic/*` slot in the v2 template only as an omitted placeholder in your planning model. Do not invent a topic tag without evidence.
- Leave `sources:` and `contradictions:` absent unless you can infer them without reading deeply
- Only the frontmatter block is added. The body below it is untouched.

### 5. Build INDEX.md

Create `INDEX.md` at the wiki root with the v2 header block:

```yaml
---
name: {Wiki Name}
description: {User-provided description}
tags:
  - area/ea
  - kind/wiki
date_created: {today}
date_updated: {today}
---
```

```markdown
# {Wiki Name}

> Content catalog. Every wiki page is listed here with a one-line summary.
> Read this first to find relevant pages for any query.
> **Total pages:** {N} | **Last updated:** {today}

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/research

| File | Description |
|------|-------------|
| `references/{page}.md` | {description from frontmatter or filename} |
```

Catalog every page, including pages inside preserved subdirectories, under its `kind/*` section.

### 6. Create LOG.md

Create `references/LOG.md` if it does not exist:

```yaml
---
name: Log
description: Append-only operational log for {Wiki Name}
tags:
  - area/ea
  - kind/log
  - status/open
date_created: {today}
date_updated: {today}
---
```

```markdown
# Log

- [[{today}]] create | wiki | Wiki map created. {N} files organized into references/
```

If `LOG.md` already exists in an organize-mode directory, append the create entry instead of overwriting it.

### 7. Report to User

```markdown
## Wiki Map Created: {wiki-name}

**Files moved:** {count}
**Files renamed:** {count}
**Frontmatter added:** {count} (body content untouched)
**Already organized:** {count}

INDEX.md and LOG.md created or updated.

Next steps:
- Review the wiki map in INDEX.md
- Refine `kind/` and `topic/` tags where defaults do not fit
- Tell me to "ingest" a specific file when you want synthesis and cross-referencing
```
