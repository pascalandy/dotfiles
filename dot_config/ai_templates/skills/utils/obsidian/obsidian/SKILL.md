---
name: obsidian
description: >
  Use only when the user explicitly says "obsidian". Search, create, edit, and organize notes in the user's  Obsidian vault using wikilinks, embeds, callouts, properties, and Obsidian Flavored Markdown. Use when the user mentions Obsidian notes, vault search, wikilinks,
  frontmatter, tags, embeds, callouts, or wants to find, create, or manage notes in Obsidian. Do not use that skill automatically.
---

# Obsidian Vault

## Quick orientation

OBSIDIAN_VAULT_PATH=$(chezmoi secret keyring get --service=OBSIDIAN_VAULT --user=path)

Read `_bases/The Vault 🧠.base` for 40+ curated views of the vault.

## Naming conventions

- **Title Case** for all note names
- **Index notes** aggregate related topics (e.g., `Ralph Wiggum Index.md`, `Skills Index.md`)
- No folders for organization -- use `[[wikilinks]]` and index notes instead

## Workflows

### Search for notes

Use Grep/Glob tools on the vault path. For CLI fallback:

```bash
# By filename
fd -e md "keyword" "$OBSIDIAN_VAULT_PATH"

# By content
rg -l "keyword" "$OBSIDIAN_VAULT_PATH" --glob "*.md"
```

### Create a new note

1. Choose a **Title Case** filename
2. Add YAML frontmatter (`title`, `tags`, `aliases`). Read [PROPERTIES.md](references/PROPERTIES.md) if using non-standard property types
3. Write content using standard Markdown plus the Obsidian syntax below
4. Link related notes with `[[wikilinks]]` at the bottom
5. Verify the note has no orphan wikilinks pointing to non-existent notes

### Find backlinks

```bash
rg -l "\[\[Note Title\]\]" "$OBSIDIAN_VAULT_PATH" --glob "*.md"
```

### Find index notes

```bash
fd -e md "Index" "$OBSIDIAN_VAULT_PATH"
```

## Obsidian-specific syntax

Standard Markdown (headings, bold, italic, lists, quotes, code blocks, tables) is assumed knowledge. Only Obsidian extensions are documented here.

### Wikilinks

```markdown
[[Note Name]]                          Link to note
[[Note Name|Display Text]]             Custom display text
[[Note Name#Heading]]                  Link to heading
[[#Heading in same note]]              Same-note heading link
```

Use `[[wikilinks]]` for vault-internal notes (Obsidian tracks renames). Use `[text](url)` for external URLs only.

### Embeds

Prefix any wikilink with `!` to embed inline:

```markdown
![[Note Name]]                         Embed full note
![[image.png]]                         Embed image
![[image.png|300]]                     Embed with width
```

Read [EMBEDS.md](references/EMBEDS.md) when embedding audio, PDFs, search results, or external images.

### Callouts

```markdown
> [!note]
> Basic callout.

> [!warning] Custom Title
> With custom title.

> [!faq]- Collapsed by default
> Foldable (- collapsed, + expanded).
```

Types: `note`, `tip`, `warning`, `info`, `example`, `quote`, `bug`, `danger`, `success`, `failure`, `question`, `abstract`, `todo`.

Read [CALLOUTS.md](references/CALLOUTS.md) when nesting callouts or creating custom CSS callout types.

### Properties (frontmatter)

```yaml
---
title: My Note
tags:
  - project
  - active
aliases:
  - Alternative Name
---
```

Read [PROPERTIES.md](references/PROPERTIES.md) when using dates, numbers, checkboxes, links, or `cssclasses`.

### Tags, comments, highlights

```markdown
#tag                                   Inline tag
#nested/tag                            Nested hierarchy
%%hidden in reading view%%             Comment
==highlighted text==                   Highlight
```

Tags allow letters, numbers (not first char), underscores, hyphens, slashes. Tags can also go in frontmatter `tags:` property.

Read [MARKDOWN.md](references/MARKDOWN.md) when using block IDs, math/LaTeX, Mermaid diagrams, or footnotes.

## Gotchas

- Wikilinks are **not** standard Markdown. `[[Link]]` only works in Obsidian; for export-safe links use `[text](file.md)` instead.
- The `aliases` property is a list, not a string. `aliases: Name` is invalid YAML; use `aliases: [Name]` or a YAML list.
- Frontmatter must be the very first thing in the file. Even a blank line before `---` breaks it.
- Block IDs (`^my-id`) must be on their own line for lists and quotes. For paragraphs, append to the end of the line.
- `%%comments%%` are only hidden in Reading View. They remain visible in Source/Live Preview mode.
- Tags starting with a number (`#123`) are invalid. Use `#tag-123` instead.
