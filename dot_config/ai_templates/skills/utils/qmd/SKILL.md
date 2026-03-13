---
name: qmd
description: >
  Use this skill whenever the user wants to search, recall, open, or pull
  information from local indexed markdown collections—especially Obsidian
  vaults, docs folders, personal notes, or any existing QMD collection.
  Also use it when the user mentions QMD itself, query documents,
  `lex:` / `vec:` / `hyde:` / `intent:`, collection filters,
  `qmd query`, `qmd search`, or `qmd vsearch`, or wants better retrieval
  quality from local markdown. Trigger even when they do not say “QMD” and
  instead ask things like “find my note about X,” “search my vault,” “what
  markdown docs mention Y,” “open the relevant files,” or “tune this
  retrieval.” Do not use it for web search, generic repo code search, or
  non-QMD data sources unless QMD is clearly the source of truth.
compatibility: Requires qmd CLI >= 1.1.5. `bun install -g @tobilu/qmd`
allowed-tools: "Bash(qmd:*)"
license: MIT
metadata:
  author: pascalandy
  based_on: qmd-v1
  version: "2.0"
---

# QMD - Query Markup Documents

## Core operating rules

- Default to QMD CLI workflows.
- Search the most likely collection first and pass `-c <collection>` whenever you can.
- Prefer `qmd query` for most retrieval work, `qmd search` for exact title or filename lookup, and `qmd vsearch` mainly as a fallback or second opinion.
- Reopen strong hits with `qmd get` or `qmd multi-get` before making accuracy-sensitive claims.
- Return resolved QMD URI(s) whenever possible.
- If scope, indexing, or freshness is unclear, run `qmd status` first.
- If the hard part is crafting better `vec:` or `hyde:` searches, load the `semantic-patterns` skill.

## Default playbook

1. Identify the most likely collection.
2. Run `qmd query` first unless the user gave an exact title, path, or filename.
3. Reopen the best hit(s) with `qmd get` or `qmd multi-get`.
4. Answer with resolved QMD URI(s) and only use evidence from reopened documents.

## Reference map

Read extra material only when needed:

- `references/retrieval-workflow.md` — health checks, collection scoping, mode choice, evidence discipline, common mistakes
- `references/query-patterns.md` — query documents, `intent:` / `lex:` / `vec:` / `hyde:`, weighting, ambiguity handling
- `references/command-cheatsheet.md` — high-value flags, command patterns, setup, indexing, maintenance
- `references/mcp-setup.md` — keep MCP details out of the main path; read only if the user explicitly asks about MCP

## Example user requests

Users may ask for QMD retrieval with very little detail. These examples show effective prompt patterns for common retrieval tasks.

### Default retrieval approach

Unless the user says otherwise

- use QMD CLI only
- be efficient and chain related commands with `&&` when it saves steps
- search the most likely collection first
- prefer exact repo, path, filename, or title matching before broader discovery
- reopen the strongest matching documents before answering
- do not rely on snippets alone when accuracy matters
- return resolved QMD URI(s) whenever possible

### Map documentation

```text
Use QMD CLI only

In collection: vendors

Find the repo or project for: pi
Then identify: the documentation root
Then return: a tree of all docs and examples

Prefer:
- exact repo or path matching first
- targeted discovery only if needed
- reopen the best matching documents before answering

Return:
- the resolved QMD URI root
- a clean tree of the docs and examples

Conclude with a 2-3 sentence summary of what this project and its documentation cover
```

### Find the canonical document

```text
Use QMD CLI only

In collection: vendors

Find the repo or project for: pi
Then find: the canonical document for extensions

Prefer:
- exact repo, path, or title matching first
- targeted discovery only if needed
- reopen the best matching documents before answering

Return:
- the resolved QMD URI(s)
- the canonical document
- 2-5 relevant alternatives if they exist

Conclude with a 2-3 sentence summary of what the extensions documentation covers
```

### Answer a documentation question

```text
Use QMD CLI only

In collection: vendors

Find the repo or project for: pi
Then answer this question: how does extension loading work?

Prefer:
- exact repo or path discovery first
- targeted search only if needed
- reopen the strongest matching documents before answering

Return:
- the resolved QMD URI(s)
- a cited answer based on the reopened documents

Conclude with a 2-3 sentence summary of how extension loading works
```

### Compare across collections

```text
Use QMD CLI only

Across collections:
- vendors
- vault_obsidian

Find information about: Pi extensions

First:
- identify the most relevant documents in each collection
- reopen the strongest matches
- compare the findings by collection

Return:
- grouped results by collection
- best-match QMD URI(s)
- a short summary for each collection
- a final synthesis

Conclude with a 2-3 sentence summary of the main differences or overlaps
```

### Find a note from vague memory

```text
Use QMD CLI only

In collection: vault_obsidian

Find my note about: local markdown retrieval being better than grep for AI agents

Prefer:
- `qmd query` first
- semantic recall over exact title matching
- reopen the strongest matches before answering

Return:
- best-match QMD URI(s)
- a short explanation of why each match is relevant
- a 2-3 sentence synthesis
```

### Recover an exact note or title

```text
Use QMD CLI only

In collection: vault_obsidian

Find the note titled something like: QMD roadmap

Prefer:
- exact title or filename matching first
- reopen the best hit before answering

Return:
- the resolved QMD URI
- the note title and path
- a 2-3 sentence summary
```

### Refresh stale results

```text
Use QMD CLI only

My markdown files changed on disk and QMD results look stale.

Return:
- the exact commands I should run
- the correct order for update vs embed
- a short explanation of what each command fixes
```
