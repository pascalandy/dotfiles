---
name: Query
description: >
  QMD CLI operations for searching local markdown collections. USE WHEN find note, search collection, retrieve document, list collections, update indexes, status, maintenance, MCP setup, qmd command, map documentation, compare collections.
---

# Query - QMD CLI Operations

Operational retrieval using the QMD CLI. Covers health checks, collection scoping, retrieval mode selection, evidence discipline, and maintenance.

## Core operating rules

- Default to QMD CLI workflows
- Search the most likely collection first and pass `-c <collection>` whenever you can
- Prefer `qmd query` for most retrieval work, `qmd search` for exact title or filename lookup, and `qmd vsearch` mainly as a fallback or second opinion
- Reopen strong hits with `qmd get` or `qmd multi-get` before making accuracy-sensitive claims
- Return resolved QMD URI(s) whenever possible
- If scope, indexing, or freshness is unclear, run `qmd status` first
- If the hard part is crafting better `vec:` or `hyde:` searches, route to the Semantic sub-skill instead

## Default playbook

1. Run: `qmd update &> /dev/null && qmd embed &> /dev/null && qmd cleanup &> /dev/null && qmd status && qmd ls`
   - Why? Updates file indexes, regenerates embeddings, cleans stale entries, and shows current status.
2. Wait for the previous command to end then identify the most likely collection(s)
3. Run `qmd query` first unless the user gave an exact title, path, or filename.
4. Reopen the best hit(s) with `qmd get` or `qmd multi-get`.
5. Answer with resolved QMD URI(s) and only use evidence from reopened documents.

## Default retrieval approach

Unless the user says otherwise:

- Use QMD CLI only
- Be efficient and chain related commands with `&&` when it saves steps
- Search the most likely collection first
- Prefer exact repo, path, filename, or title matching before broader discovery
- Reopen the strongest matching documents before answering
- Do not rely on snippets alone when accuracy matters
- Return resolved QMD URI(s) whenever possible

## Reference map

Read extra material only when needed:

- `references/retrieval-workflow.md` -- health checks, collection scoping, mode choice, evidence discipline, common mistakes
- `references/query-patterns.md` -- query documents, `intent:` / `lex:` / `vec:` / `hyde:`, weighting, ambiguity handling
- `references/command-cheatsheet.md` -- high-value flags, command patterns, setup, indexing, maintenance
- `references/mcp-setup.md` -- MCP details; read only if the user explicitly asks about MCP

## Example user requests

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
