---
name: obsidian-sk
description: >
  Use only when the user explicitly say "obsidian-sk" 
  Use whenever you have to interact in user's obsidian vault. Search, create, and manage notes in the Obsidian vault with wikilinks and index notes. Use when user wants to find, create, or organize notes in Obsidian.
---

# Obsidian Vault

## Quick orientation

vault_path=`/Users/andy16/Documents/_my_docs/10_obsidian/vault_obsidian`
- Read `_bases/The Vault 🧠.base`, I have more than 40 well curated views in that base

## Naming conventions

- **Index notes**: aggregate related topics (e.g., `Ralph Wiggum Index.md`, `Skills Index.md`, `RAG Index.md`)
- **Title case** for all note names
- No folders for organization - use links and index notes instead

## Linking

- Use Obsidian `[[wikilinks]]` syntax: `[[Note Title]]`
- Notes link to dependencies/related notes at the bottom
- Index notes are lists of `[[wikilinks]]`

## Workflows

### Search for notes

```bash
# Search by filename
fd "{vault_path}" -name "*.md" | grep -i "keyword"

# Search by content
grep -rl "keyword" "{vault_path}" --include="*.md"
```

Or use Grep/Glob tools directly on the vault path.

### Create a new note

1. Use **Title Case** for filename
2. Write content as a unit of learning (per vault rules)
3. Add `[[wikilinks]]` to related notes at the bottom
4. If part of a numbered sequence, use the hierarchical numbering scheme

### Find related notes

Search for `[[Note Title]]` across the vault to find backlinks:

```bash
grep -rl "\\[\\[Note Title\\]\\]" "{vault_path}"
```

### Find index notes

```bash
find "{vault_path}" -name "*Index*"
```
