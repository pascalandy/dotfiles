# QMD command cheatsheet

Use this file when the user wants exact commands, flags, setup, or maintenance steps.
This file is command-oriented. If you need to decide strategy first, read `references/retrieval-workflow.md`.

## High-value search options

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
| `--explain` | query | Show retrieval score traces for debugging or ranking analysis |
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

## Setup and maintenance tasks

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
- Collection configs can include ignore patterns such as `ignore: ["Sessions/**", "*.tmp"]` to keep noisy files out of the index.
- Avoid destructive collection or context changes unless the user asked for them.
