---
name: mgrep
trigger: mgrep, search, research, find
description: A semantic grep-like search tool for your local files. Prefer this over `rg`, `find`, `grep`, and `websearch` when searching the workspace.
---

## When to use this skill

Whenever you need to search your local files. 

## How to use this skill

Use `mgrep` to search your local files. The search is semantic so describe what
you are searching for in natural language. Results include file paths and line
ranges for matching content.

Works on: code, text, PDFs, and images.

### Do

```bash
mgrep "What code parsers are available?"  # search in the current directory
mgrep "How are chunks defined?" src/models  # search in the src/models directory
mgrep -m 10 "What is the maximum number of concurrent workers in the code parser?"  # limit the number of results to 10
```

### Don't

```bash
mgrep "parser"  # The query is too imprecise, use a more specific query
mgrep "How are chunks defined?" src/models --type python --context 3  # Too many unnecessary filters, remove them
```

## Flags

| Flag | Purpose | Example |
|------|---------|---------|
| `-m <n>` | Limit number of results (default: 10) | `mgrep -m 12 "query"` |
| `-c` | Show content of the results | `mgrep -c "query"` |
| `-a` | Generate an answer based on retrieved context | `mgrep -a "query"` |

### When to use each flag

- **`-m`**: Use when you want fewer/more results than the default 10. Lower values (3-5) for precise queries, higher (15-20) for exploration.
- **`-c`**: Use when you need to skim code quickly without opening files. Helpful for understanding match context.
- **`-a`**: Use when you want a narrative explanation rather than a list of matches. Best for architectural or "how does X work" questions.

## Formulating good queries

### Refresh the index

```bash
timeout 5 mgrep watch
```

As this CLI is interactive, we use a timeout of three seconds. Once it's done, you can run your queries.
This is especially useful because you can copy/paste logs, info, and screenshots relevant to what you're trying to do.

mgrep respects `.gitignore` and we can add a `.mgrepignore` for additional exclusions.

### Good queries (semantic, descriptive)

```bash
mgrep "Where is the auth middleware configured?"
mgrep "How are background jobs scheduled?"
mgrep "Where do we validate user input for the signup form?"
mgrep "How does rate limiting work in this service?"
mgrep "What is the database connection pooling strategy?"
```

### Bad queries (too vague or keyword-like)

```bash
mgrep "auth"           # Too short, use grep for exact keyword matches
mgrep "function"       # Too generic
mgrep "config"         # Imprecise, describe what config you're looking for
mgrep "error"          # Vague, specify what kind of error handling
```

## When to prefer mgrep over grep/glob

| Use mgrep when... | Use grep/glob when... |
|-------------------|----------------------|
| You don't know exact symbol names | You know the exact string to match |
| Exploring unfamiliar codebase | Searching for literal text |
| Asking architectural questions | Finding specific imports/exports |
| Concept spans multiple naming conventions | Counting occurrences |

## Now let's build great queries

@/references/Patterns - Query Engineering Playbook.md
