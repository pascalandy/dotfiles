---
name: qmd
description: >
  Use this skill whenever the user wants to search, recall, open, or pull information from local indexed markdown collections—especially Obsidian vaults, docs folders, meeting transcripts, personal notes, or any existing QMD collection. Trigger even when they do not say “QMD” and instead ask things like “find my note about X,” “search my vault,” “what markdown docs mention Y,” “open the relevant files,” or need help setting up or maintaining QMD collections, contexts, embeddings, or QMD integrations. Do not use it for web search, generic repo code search, PDFs, or non-markdown systems unless QMD is clearly the source of truth.
license: MIT
compatibility: Requires qmd CLI. Install via `bun install -g @tobilu/qmd`
metadata:
  author: tobi
  version: "2.2.0"
allowed-tools: Bash(qmd:*), mcp__qmd__*
---

# QMD - Query Markup Documents

Use QMD for local markdown retrieval across Obsidian notes, docs, transcripts, knowledge bases, and other indexed markdown collections. Your job is not just to search. Pick the right retrieval mode, narrow to the right collection, and open the real documents before answering.

If the user asks about QMD MCP setup, tool names, or server commands, read `references/mcp-setup.md` first.

## Start with health and scope

Run:

```bash
qmd status
```

Use it to confirm:
- which collections exist
- which collection is the best first target
- whether embeddings are pending
- whether indexing looks stale

Useful follow-ups:

```bash
qmd collection list
qmd context list
qmd ls <collection>
qmd ls <collection/path>
```

Practical guidance:
- If the user names a likely source, still confirm the exact collection name with `status` or `collection list`.
- If semantic or hybrid retrieval looks weak and `status` shows pending embeddings, tell the user and consider `qmd embed`.
- If files changed on disk, run `qmd update` before `qmd embed`.

## Choose the right retrieval mode

QMD has three search modes. Choose deliberately.

| Command | Best for | Default? | Notes |
|---|---|---:|---|
| `qmd search` | Exact titles, keywords, tags, filenames, identifiers | Sometimes | Fast BM25 only |
| `qmd query` | Best-quality retrieval, vague recall, open-ended lookup, multi-doc discovery | Yes | Hybrid: BM25 + vector + query expansion + reranking |
| `qmd vsearch` | Pure semantic lookup when the user remembers meaning, not wording | Sometimes | Vector only; can drift more than `query` |

Rules of thumb:
- If the user knows the exact note title or terms, start with `search`.
- If the user remembers the idea but not the wording, prefer `query` first.
- Use `vsearch` when you explicitly want semantic-only retrieval or a second opinion.
- If `vsearch` feels semantically off, switch back to `query` instead of forcing it.
- When quality matters more than speed, `query` is the safest default.

## Retrieval workflow

1. Run `qmd status`.
2. Search the most likely collection first with `-c <collection>`.
3. If scope is unclear, search across all collections.
4. Inspect the top hits: path, title, context, score, and `docid`.
5. Open the best hit with `qmd get`.
6. If several files matter, use `qmd multi-get`.
7. Then summarize, answer, or compare.

Important retrieval discipline:
- Do **not** answer from snippets alone when accuracy matters.
- Treat search snippets as a shortlist, not final evidence.
- Prefer reopening a hit by `#docid`; it is the safest way to get the exact result you selected.
- When the first search is noisy, refine by collection, switch modes, or raise `--min-score`.

## Semantic search strategies

load skill : "semantic-patterns"

## High-value command patterns

Search and shortlist:

```bash
qmd search "User Guide / Qmd Cli" -c vault_obsidian
qmd query "my note about local markdown search for ai agents" -c vault_obsidian -n 10
qmd search "rate limiter" --all --files --min-score 0.3
qmd query "quarterly planning process" --json -n 10
qmd vsearch "how do we deploy this service" -c docs
qmd --help #for any other feature the agent is curious about
```

Retrieve the actual docs:

```bash
qmd get "#abc123"
qmd get "qmd://vault_obsidian/cards/webclip/qmd.md"
qmd get "notes/meeting.md:50" -l 100
qmd get "notes/meeting.md" --from 120 -l 80
qmd multi-get "journals/2025-05*.md"
qmd multi-get "doc1.md, doc2.md, #abc123"
qmd multi-get "docs/*.md" --max-bytes 20480 --json
```

Useful output controls:

```bash
-n <num>
-c, --collection <name>
--all
--min-score <num>
--full
--line-numbers
--files
--json
--csv | --md | --xml
```

Agent-oriented guidance:
- Use `--files` for a compact candidate list.
- Use `--json` when results will be post-processed.
- Use `--all --files --min-score <threshold>` to build a broader file shortlist before opening documents.
- `qmd get` supports fuzzy path suggestions, but docids are safer when you must reopen the exact search result.

## Setup and maintenance tasks

When the user wants to set up or repair QMD, these are the core commands:

```bash
qmd collection add ~/notes --name notes
qmd collection add ~/work/docs --name docs --mask "**/*.md"
qmd collection list
qmd collection rename old-name new-name
qmd collection remove old-name

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
- Git-backed docs that should be refreshed first: `qmd update --pull`.
- Weak semantic search or pending vectors: `qmd embed`.
- Stale cache or orphaned index data: `qmd cleanup`.
- Avoid destructive collection or context changes unless the user asked for them.

Context matters. Encourage collection-level or path-level context when results are ambiguous. QMD returns that context with results, which helps downstream selection.

## Reference file

For QMD MCP setup, current MCP tool names, tool mappings, and server commands, read `references/mcp-setup.md`.

## Common mistakes to avoid

- Do not use QMD for web search or general codebase grep.
- Do not summarize from snippets alone when the user needs accuracy.
- Do not default to `vsearch` for every fuzzy request; `query` is usually the better first choice.
- Do not forget collection filters when the likely collection is obvious.
- Do not ignore `status` when results look stale, sparse, or semantically weak.
