---
description: prime obsidian
---

# Obsidian Base-First Context

Load skills: `obsidian-cli`, `obsidian-markdown`

## Objective

For any vault question, start from existing Base views before manual search.

1. Resolve the active vault path.
2. Inspect `_bases/The Vault 🧠.base`.
3. Reuse the matching view filter.
4. Search notes with the same filter keys (`tags`, `project_id`, `links`).

## Vault Path

Preferred vault:
`/Users/andy16/Documents/_my_docs/10_obsidian/vault_obsidian`

Confirm current vault from Obsidian config:

```bash
VAULT_PATH="$(rg -o '"path":"[^"]+"' ~/Library/Application\ Support/obsidian/obsidian.json | head -1 | cut -d'"' -f4)"
```

## Primary Base

- Name: `The Vault 🧠`
- File: `_bases/The Vault 🧠.base`
- Role: main index with ~50 views

## View Patterns

### 1) Area tags (primary)

- `area/life/*`: `sante`, `workout`, `supplement`, `dentaire`, `voyage`, `maison`, `finance`, `recette`, `gear`, `contact`, `think`
- `area/work/*`: `ai`, `coding`, `analyste`, `obsidian`, `comptabilite`
- `area/resource/*`: `book`, `app`, `webclip`, `definition`, `share`

### 2) Project views

Some views filter by `project_id` (examples: `s5C5t`, `D1Q3k`, `K5R7d`, `p3Y7q`).

### 3) Link views

Some views filter by links to specific files (example: `_cards/journal`).

## Query Workflow

1. Find a matching view in `The Vault 🧠.base`.
2. Extract its filter logic.
3. Run targeted search using that logic.
4. Broaden search only if no view fits.

## Useful Commands

```bash
# list notes by tag
rg -l 'area/life/sante' "$VAULT_PATH" --type md

# list notes by project_id in frontmatter
rg -l 'project_id:\s*s5C5t' "$VAULT_PATH" --type md

# inspect base config and filters
cat "$VAULT_PATH/_bases/The Vault 🧠.base"
```

## Canvas

When working on a canvas, load the skill "obsidian-json-canvas"

Rule: Treat `The Vault 🧠` as the default entry point for retrieval.
