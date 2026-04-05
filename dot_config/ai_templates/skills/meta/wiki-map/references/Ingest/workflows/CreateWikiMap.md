# CreateWikiMap Workflow

Organize existing files into a wiki structure. Scan a directory, move files into `references/`, rename to kebab-case, add frontmatter where missing, and build INDEX.md + LOG.md.

**This workflow is read-only on file body content. No synthesis, no rewriting, no summarization. Only frontmatter and file location may change. Content edits require a separate explicit user request.**

## When to Use

- Turning an existing directory of markdown files into a wiki
- User says "create a wiki map", "create wiki", "bootstrap wiki", "init wiki", "new wiki", "organize these files into a wiki"
- Starting a brand new empty wiki (the empty-directory case)

## Steps

### 1. Confirm Scope

Ask the user:
- Which directory are we organizing? (or: what should we name a new one?)
- Brief description for INDEX.md

If the directory already exists, list what's in it:

```markdown
## Directory Scan: {path}

**Files found:** {count}
**Already in references/:** {count}
**Need to move:** {count}
**Subdirectories to preserve:** {list}

| File | Current Location | Proposed Name |
|------|-----------------|---------------|
| My Article.md | ./ | references/my-article.md |
| notes_on_sleep.md | ./ | references/notes-on-sleep.md |
| z_varia/old-draft.md | z_varia/ | references/z_varia/old-draft.md |
| references/already-here.md | references/ | (no change) |

Proceed?
```

Wait for user confirmation before moving anything.

### 2. Create Directory Structure

```
{wiki-name}/
  INDEX.md
  references/
    LOG.md
  assets/           # create only if non-markdown files exist
```

If the directory already exists, only create what's missing.

### 3. Move Everything into references/

Create `references/` then move **all** existing files and folders into it as-is:

- Move every file and subdirectory from the wiki root into `references/`
- **Preserve the existing structure exactly** -- subdirectories go in intact, files keep their relative paths
- After the move, rename files to **kebab-case**: spaces to hyphens, underscores to hyphens, lowercase, strip special characters
- Use `git mv` if inside a git repo, plain `mv` otherwise
- **Do not read, modify, or rewrite file bodies**
- **Never flatten, reorganize, or split subdirectories**

If a naming collision would occur, append a suffix: `my-article-2.md`.

Only INDEX.md and AGENTS.md (if present) stay at the wiki root.

### 4. Add Frontmatter Where Missing

For each markdown file in `references/`:

- **If frontmatter already exists**: leave it untouched. Do not modify, reformat, or "improve" it.
- **If frontmatter is missing**: prepend minimal frontmatter. Derive `name` and `description` from the filename and first line of content. Do not read deeply into the body.

Minimal frontmatter to add:

```yaml
---
name: {derived from filename}
description: {first heading or filename}
tags:
  - area/ea
  - kind/research
  - status/open
date_updated: {today}
---
```

Use `kind/webclip` if the file looks like a clipped article (has a URL source or was clearly copied from the web). Use `kind/research` as the default for everything else. The user can refine kinds later.

**Guardrail**: Only the frontmatter block is added. The body below the `---` closing fence is never touched.

### 5. Build INDEX.md

Create (or overwrite) INDEX.md at the wiki root:

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
| `references/{page}.md` | {description from frontmatter or filename} |
```

Build the table by reading the `name` or `description` from each file's frontmatter. If a file has no frontmatter (shouldn't happen after step 4, but defensive), use the filename.

### 6. Create LOG.md

Create `references/LOG.md` (if it doesn't exist):

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

- [[{today}]] create | wiki | Wiki map created. {N} files organized into references/
```

If LOG.md already exists, append the entry only.

### 7. Report to User

```markdown
## Wiki Map Created: {wiki-name}

**Files moved:** {count}
**Files renamed:** {count}
**Frontmatter added:** {count} (body content untouched)
**Already organized:** {count}

INDEX.md and LOG.md created.

Next steps:
- Review the wiki map in INDEX.md
- Refine `kind/` tags where the default doesn't fit
- Tell me to "ingest" a specific file when you want synthesis and cross-referencing
```

## Empty Directory Case

If the target directory has no existing files, this workflow still works -- it creates the structure with an empty INDEX.md table and LOG.md. This covers the "brand new wiki" case without needing a separate workflow.

## What This Workflow Does NOT Do

- Read file bodies for synthesis or summarization
- Create new pages based on file content
- Rewrite, restructure, or "improve" existing content
- Add cross-references or wikilinks to file bodies
- Merge or split files

All of those are **Ingest** operations (IngestSingle, IngestBatch) that the user must explicitly request afterward.
