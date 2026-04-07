# Wiki Schema (Global)

> The single source of truth for wiki conventions. All sub-skills and workflows reference this file. There is no per-wiki `SCHEMA.md`.

## Wiki Architecture

```text
{wiki-name}/
  INDEX.md              # Content catalog (kind/wiki)
  references/
    LOG.md              # Append-only operational log (kind/log)
    {page}.md           # Wiki pages
    {subdir}/           # User-managed subdirectories preserved as-is
    _meta/
      topic-map.md      # Optional helper map once INDEX exceeds 200 entries
  assets/               # Optional, for non-markdown files
```

Rules:
- All content lives under `references/`.
- Preserve existing subdirectories as-is. Never flatten or normalize user layout.
- `INDEX.md` stays at the wiki root and catalogs every page, including pages in subdirectories.
- `assets/` is optional and only for non-markdown files.

## Tag Axes

Tag order is always:

```text
area/* -> kind/* -> topic/* -> status/* -> pty/*
```

### area/*

- `area/ea` -- required on every page

### kind/*

- `kind/task`
- `kind/bug`
- `kind/doc`
- `kind/plan`
- `kind/log`
- `kind/wiki`
- `kind/project`
- `kind/webclip`
- `kind/query`
- `kind/tracking`
- `kind/random`

Notes:
- `kind/relationship` is deprecated. Use `topic/relationship` instead.
- `kind/query` is reserved for answers filed from Query workflows.

### topic/*

- `topic/{name}`
- `topic/milestone`
- `topic/playbook`
- `topic/relationship`
- `topic/strategy`
- `topic/role`
- `topic/template`
- `topic/reference`

`topic/*` is optional. Use it for subject domain, not work type.

### status/*

- `status/draft`
- `status/open`
- `status/stable`
- `status/blocked`
- `status/parked`
- `status/close`

### pty/*

- `pty/p1`
- `pty/p2`
- `pty/p3`

`pty/*` is optional and only valid for actionable kinds such as `kind/task`, `kind/bug`, `kind/plan`, and `kind/tracking`.

## Frontmatter Template

```yaml
---
name: Page Title
description: One-line summary
tags:
  - area/ea
  - kind/project
  - topic/example              # optional
  - status/open
  - pty/p2                     # optional
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
sources:
  - source-page-name           # optional
contradictions:
  - conflicting-page-name      # optional
---
```

Rules:
- `date_created` is set once when the page is created and never changed.
- `date_updated` is bumped on every content change.
- `sources` lists wiki page names, not file paths, and is required for `kind/project`, `kind/doc`, and `kind/query`.
- Omit empty `sources` and `contradictions` fields.
- `contradictions` is machine-readable frontmatter. If you also use a `## Contradictions` body section, keep both in sync.

## Page Template

```markdown
Summary paragraph.

## Section Name

Content.

## Related

- [[related-page-one]]
- [[related-page-two]]
```

Guidance:
- Start with a summary paragraph.
- Add sections as needed.
- End with `## Related` unless the page kind is exempt.
- Use Obsidian-style `[[wikilinks]]`.

## INDEX.md Format

```yaml
---
name: Wiki Name
description: One-line description
tags:
  - area/ea
  - kind/wiki
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---
```

```markdown
# Wiki Name

> Content catalog. Every wiki page is listed here with a one-line summary.
> Read this first to find relevant pages for any query.
> **Total pages:** N | **Last updated:** YYYY-MM-DD

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/project

| File | Description |
|------|-------------|
| `references/page-name.md` | One-line description |
```

Rules:
- `INDEX.md` is the navigational entry point.
- Closed pages stay in `INDEX.md`. Do not auto-remove or relabel them.
- Organize the table into `kind/*` sections so scaling rules have a concrete structure to operate on.
- If any section exceeds 50 entries, split it into subsections by first letter or by `topic/*`.
- If total entries exceed 200, create or update `references/_meta/topic-map.md` only with user confirmation if it already exists and may contain manual edits.

## LOG.md Format

```yaml
---
name: Log
description: Append-only operational log for {Wiki Name}
tags:
  - area/ea
  - kind/log
  - status/open
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---
```

```markdown
# Log

- [[YYYY-MM-DD]] create | wiki | Wiki map created. 12 files organized into references/
- [[YYYY-MM-DD]] ingest | source-name | created: [page-a], updated: [page-b]
```

Rules:
- `LOG.md` is append-only.
- Rotate when the active log exceeds 500 entries: rename to `LOG-YYYY.md` and start a fresh `LOG.md`.
- Orientation reads the active `LOG.md`, not rotated logs.

## Naming Convention

- Filenames use kebab-case: `vitamin-d-and-sleep.md`
- Cross-references use Obsidian-style wikilinks: `[[vitamin-d-and-sleep]]`
- Frontmatter `sources` and `contradictions` entries use page names without brackets

## Hard Rules

### Page creation thresholds

Create a new page when:
- the entity, concept, or topic appears in 2 or more sources, or
- it is the central subject of one source

Update an existing page instead when the page already exists.

Do not create pages for passing mentions or off-scope references.

### Outbound wikilink minimum

Content kinds must contain at least 2 outbound `[[wikilinks]]`:
- `kind/project`
- `kind/doc`
- `kind/plan`
- `kind/query`

Operational kinds should contain at least 1 outbound wikilink:
- `kind/task`
- `kind/bug`
- `kind/tracking`

Exempt kinds:
- `kind/wiki`
- `kind/log`
- `kind/webclip`
- `kind/random`

Closed pages are excluded from this rule.

### Page split threshold

- Split a page when it exceeds 200 lines, excluding frontmatter and `## Related`.

### INDEX scaling

- Split any section that exceeds 50 entries.
- Create `references/_meta/topic-map.md` once total entries exceed 200.

### Mass-update confirmation

- If an operation would create or modify 10 or more pages, stop after planning and ask for confirmation.
- In automated mode, halt, log the gate trigger, and exit without writing.

### Closed pages

- `status/close` pages stay in `INDEX.md`.
- Do not auto-suffix, auto-remove, or reorganize closed-page entries.
- Exclude closed pages from orphan, stale, and wikilink-minimum checks.
- Still include them in contradiction and frontmatter validation.

### Interactive vs automated mode

Automated mode may skip conversational confirmation gates, but must still honor:
- the 10-page mass-update gate
- CreateWikiMap directory-scan confirmation
- CreateWikiMap existing-wiki halt
- UpgradeSchema non-automation rule

When in doubt, default to interactive mode.

## Session Orientation Protocol

Before any operation on an existing wiki:

1. Read this `references/SCHEMA.md`.
2. Read the wiki's `INDEX.md`.
3. Read the last 30 entries of the wiki's active `references/LOG.md`.
4. If the wiki has 100 or more pages, search for the current request topic before creating any new page.

For a brand new wiki:
- read this `references/SCHEMA.md`
- skip wiki `INDEX.md` and wiki `LOG.md` reads because they do not exist yet

Subdirectory drift detection:
- If the directory structure differs from what the recent log implies, note it in the orientation summary.
- Do not try to normalize or fix the structure.
- Ask the user whether the new structure should be reflected in `INDEX.md`.

Orientation output:

```text
Oriented: {wiki-name} | {N} pages | {M} recent log entries | {drift status}
```
