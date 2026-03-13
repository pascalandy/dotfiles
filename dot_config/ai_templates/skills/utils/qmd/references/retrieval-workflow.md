# QMD retrieval workflow reference

Use this file when the problem is operational: unclear collection scope, stale indexes, weak results, or deciding how to move from search to evidence.
This file is decision-oriented. For exact maintenance commands, flags, or setup syntax, read `references/command-cheatsheet.md`.

## Start with health and scope

Run this first when the source is unclear, results may be stale, or the user asks about setup or maintenance:

```bash
qmd status
```

Useful follow-ups:

```bash
qmd collection list
qmd collection
qmd ls <collection>
qmd ls <collection/path>
```

Use them to confirm:
- which collections exist
- whether a collection is excluded from default search
- whether indexing or embeddings look stale
- which collection is the best first target

Practical guidance:
- If the user already names a likely source, still confirm the exact collection name.
- If files changed on disk or embeddings look stale, switch to `references/command-cheatsheet.md` for the exact refresh commands.
- If a collection was excluded with `qmd collection exclude`, it will not be searched unless you explicitly pass `-c <collection>`.

## Choose the right retrieval mode

| Command | Best for | Notes |
|---|---|---|
| `qmd query` | Best-quality retrieval, vague recall, ambiguous terms, multi-doc discovery | Default choice |
| `qmd search` | Exact titles, filenames, tags, identifiers, strong keywords | Fast BM25 only |
| `qmd vsearch` | Semantic-only lookup or a second opinion | Useful fallback, can drift |

Rules of thumb:
- If quality matters more than raw speed, start with `qmd query`.
- If the user knows the exact note title or exact terms, start with `qmd search`.
- If the user remembers meaning more than wording, prefer `qmd query` first and use `qmd vsearch` as a fallback or comparison.
- Do not default to `vsearch` for every fuzzy request.

## Retrieval workflow

1. Run `qmd status` when health or scope is uncertain.
2. Search the most likely collection first with `-c <collection>`.
3. If needed, search multiple collections deliberately.
4. For ambiguous queries, add intent.
5. Shortlist with `--files` or `--json`.
6. Reopen the best hits with `qmd get` or `qmd multi-get`.
7. Only then summarize, answer, or compare.

## Evidence discipline

- Do **not** answer from snippets alone when accuracy matters.
- Treat search snippets as a shortlist, not as final evidence.
- Prefer reopening a hit by `#docid`; it is the safest way to retrieve the exact result you selected.
- When the first search is noisy, refine by collection, add intent, switch modes, or raise `--min-score`.

## Common mistakes to avoid

- Do not use QMD for web search or generic repo grep.
- Do not summarize from snippets alone when the user needs accuracy.
- Do not forget that excluded collections are skipped by default.
- Do not default to `vsearch` for every fuzzy request.
- Do not skip `intent` when the query is obviously ambiguous.
- Do not force huge candidate sets unless the user really needs exhaustive recall.
