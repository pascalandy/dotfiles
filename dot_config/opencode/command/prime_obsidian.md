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
4. Run Obsidian CLI queries with the same filter keys (`tags`, `project_id`, `links`).
5. Use file-level fallback checks only if needed.

## Preflight (CLI)

Run first:

```bash
obsidian help
```

If CLI reports installer/version issues, stop and ask for an Obsidian update from `https://obsidian.md/download`.

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
3. Run targeted Obsidian CLI search using that logic.
4. Read top note(s), then expand with backlinks.
5. Broaden search only if no view fits.

## Obsidian CLI Commands (Primary)

```bash
# list tags and counts
obsidian tags sort=count counts total

# search by a tag key from Base filters
obsidian search query="tag:#area/life/sante" limit=50

# search by project_id from Base filters
obsidian search query="project_id: s5C5t" limit=50

# search by linked note from Base filters
obsidian search query="[[_cards/journal]]" limit=50

# read one candidate note
obsidian read file="<note-name>"

# expand context graph
obsidian backlinks file="<note-name>" total
```

For broad research prompts, run one French and one English variant of the query:

```bash
obsidian search query="$ARGUMENTS" limit=50
```

## Useful Fallback Commands (Secondary)

Use these only for strict verification or when CLI output needs file-level checks:

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

Execution order:
1. Base view matching
2. Obsidian CLI retrieval
3. Fallback file-level checks
