# QMD query patterns reference

Use this file when the hard part is forming the query rather than operating the CLI.

## Plain `qmd query` is the default

A single plain query is treated like an implicit `expand:` query.

```bash
qmd query "how does auth work" -c docs
qmd query "my note about quarterly planning" -c vault_obsidian -n 10
qmd query --intent "web performance and Core Web Vitals" "performance" -c notes
```

Use plain `qmd query` when:
- the user asks in natural language
- you want auto-expansion
- you do not need fine-grained control over `lex:` / `vec:` / `hyde:` lines

## Use query documents when you want control

QMD query documents use typed lines.

Allowed line types:
- `intent:` optional background context; helps disambiguate but does not search on its own
- `lex:` BM25 keyword search, with phrases and negation
- `vec:` semantic search phrased as a natural-language question
- `hyde:` hypothetical answer passage, useful for nuanced retrieval

Important behavior:
- `intent:` may appear at most once
- `intent:` cannot appear alone; add at least one `lex:`, `vec:`, or `hyde:` line
- the **first typed search line gets 2× fusion weight**, so put the strongest signal first
- plain `expand:` queries cannot be mixed with typed lines

Examples:

```bash
qmd query $'lex: "release workflow"\nvec: how do we cut and publish a release' -c docs

qmd query $'intent: C++ runtime optimization, not sports\nlex: "C++ performance" optimization -sports -athlete\nvec: how to optimize C++ program performance' -c notes

qmd query $'lex: "connection pool" timeout -redis\nvec: why do database connections time out under load\nhyde: Connection pool exhaustion happens when all database connections are in use and new requests wait under concurrency.' -c docs
```

## Query type guidance

| Type | Use when | How to write it |
|---|---|---|
| `lex:` | You know important words, titles, names, tags, acronyms | keywords, `"exact phrase"`, `-term`, `-"phrase"` |
| `vec:` | You know the meaning but not the wording | a natural-language question |
| `hyde:` | Topic is nuanced and semantic recall is weak | 1-3 sentences that sound like the answer |
| `intent:` | Query is overloaded or ambiguous | short background context |

Good `lex:` examples:

```text
lex: "connection pool" timeout -redis
lex: "machine learning" -sports -athlete
lex: handleError async typescript
```

Practical guidance:
- For exact matching or disambiguation, start with `lex:`.
- For best recall, combine `lex:` + `vec:`.
- For especially subtle topics, add `hyde:`.
- For overloaded words like `performance`, `shipping`, `apple`, `mercury`, or `python`, add `intent:` or `--intent` early.

## Semantic search strategy

Route to the **Semantic** sub-skill (`../../Semantic/SKILL.md`) when the real challenge is designing better semantic retrieval prompts rather than operating QMD itself.
