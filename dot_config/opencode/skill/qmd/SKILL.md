---
name: qmd
description: Use when user asks to index markdown files, update embeddings, rebuild indexes, or perform semantic search over local knowledge bases with qmd CLI.
---

# qmd - Local Semantic Search CLI

QMD=“/Users/andy16/Documents/github_local/SKILLS_MONO/apps/qmd/qmd --backend lmstudio --index andy_alpha”
## Workflow

### 1. Update Index (run before searching stale content)

```shell
$QMD update && \
$QMD embed
```

Delegate indexing to a subagent if the index is large.

### 2. Craft Search Queries

# Semantic Search Query Patterns

Query engineering determines retrieval quality. Raw user questions rarely match how information is stored. These patterns transform user intent into effective vector searches.

- Study and understand the patterns `references/semantic-patterns.md`

**Core principle:** Combine patterns. A single search often benefits from expansion + filtering + temporal awareness.

- Select the most optimal pattern(s) that you will use to do your research.
- explicitly share with the user these patterns
- explicitly share with the user the queries

### 3. Execute and Iterate semantic search

Spun multiple @charlie subagents in parallel to run the queries:

```shell
$QMD --compact -n 15 vsearch "refined search"
```

### 4. Get the final answer

Now use your usual tools in order to do search within the files that were identified.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Searching without recent `embed` | Run `update && embed` first |
| Missing backend flag | Always specify `--backend lmstudio` |
