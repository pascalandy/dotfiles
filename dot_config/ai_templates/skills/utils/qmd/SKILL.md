---
name: qmd
description: >
  Use this skill whenever the user wants to search, recall, open, or pull
  information from local indexed markdown collections—especially Obsidian
  vaults, docs folders, personal notes, or any existing QMD collection. 
  Also use it when the user mentions QMD itself, query
  documents, `lex:` / `vec:` / `hyde:` / `intent:`, collection filters,
  `qmd query`, `qmd search`, `qmd vsearch`, MCP integration, or wants better
  retrieval quality from local markdown. Trigger even when they do not say
  “QMD” and instead ask things like “find my note about X,” “search my vault,”
  “what markdown docs mention Y,” “open the relevant files,” or “tune this
  retrieval.” Do not use it for web search, generic repo code search, or
  non-QMD data sources unless QMD is clearly the source of truth.
compatibility: Requires qmd CLI >= 1.1.5. Install via `npm install -g @tobilu/qmd` or `bun install -g @tobilu/qmd`
allowed-tools: "Bash(qmd:*),mcp__qmd__*"
license: MIT
metadata:
  author: pascalandy
  based_on: qmd-v1
  version: "2.0.0"
---

# QMD - Query Markup Documents

Use QMD for local markdown retrieval: Obsidian notes, docs, transcripts, journals, and other indexed markdown collections. The job is not just to search, but to choose the right search mode, steer the search well, narrow to the right collection, then open the real documents before answering.

If the user asks about QMD MCP setup, current MCP tool names, Claude Code / Claude Desktop integration, or HTTP transport, read `references/mcp-setup.md` before answering.

## Start with health and scope

Run this first when the source is unclear, results may be stale, or the user asks about setup/maintenance:

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
- If files changed on disk, run `qmd update` before `qmd embed`.
- If semantic or hybrid retrieval looks weak and embeddings are pending, tell the user and consider `qmd embed`.
- If a collection was excluded with `qmd collection exclude`, it will not be searched unless you explicitly pass `-c <collection>`.

## Choose the right retrieval mode

Pick deliberately.

| Command | Best for | Default? | Notes |
|---|---|---:|---|
| `qmd query` | Best-quality retrieval, vague recall, ambiguous terms, multi-doc discovery | Yes | Hybrid: BM25 + vector + expansion + reranking |
| `qmd search` | Exact titles, filenames, tags, identifiers, strong keywords | Sometimes | Fast BM25 only; no LLM |
| `qmd vsearch` | Semantic-only lookup or a second opinion | Sometimes | Pure vector search; can drift more than `query` |

Rules of thumb:
- If quality matters more than raw speed, start with `qmd query`.
- If the user knows the exact note title or exact terms, start with `qmd search`.
- If the user remembers meaning more than wording, prefer `qmd query` first and use `qmd vsearch` as a fallback or comparison.
- Do not default to `vsearch` for every fuzzy request; `query` is usually the better first choice.

## Retrieval workflow

1. Run `qmd status` when health or scope is uncertain.
2. Search the most likely collection first with `-c <collection>`.
3. If you need several collections, repeat `-c` multiple times.
4. For ambiguous queries, add intent.
5. Shortlist with `--files` or `--json`.
6. Reopen the best hits with `qmd get` or `qmd multi-get`.
7. Only then summarize, answer, or compare.

Important retrieval discipline:
- Do **not** answer from snippets alone when accuracy matters.
- Treat search snippets as a shortlist, not as final evidence.
- Prefer reopening a hit by `#docid`; it is the safest way to retrieve the exact result you selected.
- When the first search is noisy, refine by collection, add intent, switch modes, or raise `--min-score`.

## Search well: the modern QMD query model

### 1) Plain `qmd query` is still the easiest default

A single plain query is treated like an implicit `expand:` query.

```bash
qmd query "how does auth work" -c docs
qmd query "my note about quarterly planning" -c vault_obsidian -n 10
qmd query --intent "web performance and Core Web Vitals" "performance" -c notes
```

Use plain `qmd query` when:
- the user asks in natural language
- you want auto-expansion
- you do not need fine-grained control over lex / vec / hyde lines

### 2) Use query documents when you want control

QMD 1.1 introduced **query documents**. Each line is typed.

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

### 3) Know what each query type is for

| Type | Use when | How to write it |
|---|---|---|
| `lex:` | You know important words, titles, names, tags, acronyms | keywords, `"exact phrase"`, `-term`, `-"phrase"` |
| `vec:` | You know the meaning but not the wording | a natural-language question |
| `hyde:` | Topic is nuanced and semantic recall is weak | 1-3 sentences that sound like the answer |
| `intent:` | Query is overloaded or ambiguous | short background context |

Good lex examples:

```text
lex: "connection pool" timeout -redis
lex: "machine learning" -sports -athlete
lex: handleError async typescript
```

Agent guidance:
- For exact matching or disambiguation, start with `lex:`.
- For best recall, combine `lex:` + `vec:`.
- For especially subtle topics, add `hyde:`.
- For overloaded words like `performance`, `shipping`, `apple`, `mercury`, or `python`, add `intent:` or `--intent` early.

## High-value search options

These are the options that matter most when driving QMD well.

| Option | Applies to | Why it matters |
|---|---|---|
| `-c, --collection <name>` | search/query/vsearch | Narrow to likely sources; repeat `-c` for multiple collections |
| `-n <num>` | search/query/vsearch | Increase shortlist size when exploring |
| `--all` | search/query/vsearch | Return all matches; pair with `--min-score` |
| `--min-score <num>` | search/query/vsearch | Cut noise when broad searches return too much |
| `--full` | search/query/vsearch | Return full document text instead of snippets |
| `--line-numbers` | search/query/vsearch/get | Easier citation and follow-up retrieval |
| `--json` | search/query/vsearch/multi-get | Best for post-processing or structured follow-up |
| `--files` | search/query/vsearch/multi-get | Fast compact shortlist of candidate files |
| `--csv`, `--md`, `--xml` | search/query/vsearch/multi-get | Alternate output formats |
| `-C, --candidate-limit <n>` | query | Tune reranking breadth; lower is faster, higher may improve recall |
| `--explain` | query | Show retrieval score traces for debugging/ranking analysis |
| `--intent "..."` | query | Add disambiguating context across the full query pipeline |
| `--index <name>` | global | Use a named index |

Practical defaults:
- Use `--files` when you mainly need a shortlist.
- Use `--json` when another tool or step will consume the results.
- Use `--explain` when the user is debugging retrieval quality.
- Lower `--candidate-limit` when speed matters; raise it if reranking may be cutting off relevant results too early.
- Use `--all --min-score <threshold>` when building a broad but controlled candidate set.

## High-value command patterns

Shortlist fast:

```bash
qmd search "User Guide / Qmd Cli" -c vault_obsidian
qmd query "my note about local markdown search for ai agents" -c vault_obsidian -n 10
qmd query --intent "web page load time and Core Web Vitals" "performance" -c docs
qmd query $'lex: "C++ performance" optimization -sports -athlete\nvec: how to optimize C++ program performance' -c notes
qmd query "quarterly planning process" --json -n 10
qmd query "error handling" --all --files --min-score 0.4
qmd query "quarterly reports" --json --explain
qmd vsearch "how do we deploy this service" -c docs
qmd --help
```

Retrieve the actual documents:

```bash
qmd get "#abc123"
qmd get "qmd://vault_obsidian/cards/webclip/qmd.md"
qmd get "notes/meeting.md:50" -l 100
qmd get "notes/meeting.md" --from 120 -l 80
qmd multi-get "journals/2025-05*.md"
qmd multi-get "doc1.md, doc2.md, #abc123"
qmd multi-get "docs/*.md" --max-bytes 20480 --json
```

## Semantic search strategy

load skill: "semantic-patterns"

Use that skill when the hard part is designing the right `vec:` or `hyde:` queries rather than operating QMD itself.

## Setup and maintenance tasks

Core commands:

```bash
qmd collection add ~/notes --name notes
qmd collection add ~/work/docs --name docs --mask "**/*.md"
qmd collection list
qmd collection show notes
qmd collection rename old-name new-name
qmd collection remove old-name
qmd collection update-cmd docs 'git pull --rebase --ff-only'
qmd collection exclude archive
qmd collection include archive

qmd context add qmd://notes "Personal notes and ideas"
qmd context add qmd://docs/api "API documentation"
qmd context list
qmd context rm qmd://notes/old

qmd status
qmd update
qmd update --pull
qmd embed
qmd embed -f
qmd cleanup
```

Maintenance guidance:
- New or changed files: run `qmd update`, then `qmd embed`.
- Git-backed docs that should refresh first: use `qmd collection update-cmd` and/or `qmd update --pull`.
- Weak semantic retrieval or pending vectors: run `qmd embed`.
- Stale cache or orphaned index data: run `qmd cleanup`.
- Collection configs can now include ignore patterns such as `ignore: ["Sessions/**", "*.tmp"]` to keep noisy files out of the index.
- Avoid destructive collection or context changes unless the user asked for them.

## MCP / agent integration summary

Current MCP usage changed:
- the main MCP search tool is now `query`
- current helper tools are `get`, `multi_get`, and `status`
- older MCP tool names like `search`, `vector_search`, `deep_search`, and `structured_search` are obsolete
- for MCP and HTTP requests, collection filters are now a `collections` array, not a single `collection` string
- the `intent` field is worth providing whenever the query is ambiguous

Read `references/mcp-setup.md` when the user asks for exact setup, tool schemas, or HTTP examples.

## Common mistakes to avoid

- Do not use QMD for web search or generic repo grep.
- Do not summarize from snippets alone when the user needs accuracy.
- Do not keep using obsolete MCP tool names.
- Do not forget that excluded collections are skipped by default.
- Do not default to `vsearch` for every fuzzy request.
- Do not skip `intent` when the query is obviously ambiguous.
- Do not force huge candidate sets unless the user really needs exhaustive recall.
