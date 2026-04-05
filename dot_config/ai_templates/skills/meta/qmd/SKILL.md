---
name: qmd
description: >
  Use only when the user explicitly says "qmd" to search local markdown collections (Obsidian vaults, docs folders, QMD collections). Do not use for web search or generic repo code search.
compatibility: Requires qmd CLI >= 1.1.5. `bun install -g @tobilu/qmd`
allowed-tools: "Bash(qmd:*)"
license: MIT
metadata:
  author: pascalandy
  version: "3.0"
---

# QMD - Query Markup Documents

> Two modes in one skill -- operational QMD retrieval and semantic query engineering, routed automatically based on what you need.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Searching local markdown collections requires two distinct competencies that get conflated:

- **Operational retrieval** -- knowing which QMD commands to run, in what order, with which flags, against which collections. This is CLI workflow knowledge.
- **Query engineering** -- transforming vague user intent into effective search queries using expansion, decomposition, HyDE, and other semantic patterns. This is retrieval science.

When these live in one flat skill, the agent loads everything regardless of whether the task is "find my note about X" (operational) or "why is semantic recall poor on this query" (engineering). You end up:

- **Loading unnecessary context** -- operational lookups drag in query pattern theory; query debugging drags in CLI cheatsheets
- **Blurring responsibilities** -- the agent tries to apply query engineering to simple exact-title lookups, or skips it entirely when recall matters
- **Missing the handoff** -- the operational skill references "load the semantic-patterns skill" but that skill lives elsewhere with no shared entry point

---

## The Solution

The QMD meta-skill provides two distinct modes with a shared entry point:

1. **Query** -- QMD CLI operations: health checks, collection scoping, retrieval mode selection, evidence discipline, command cheatsheet, and MCP setup. This is what runs for most user requests.

2. **Semantic** -- Query pattern engineering: expansion, decomposition, contextual rewriting, HyDE, metadata filtering, multi-hop retrieval, and result aggregation. This activates when the challenge is crafting better queries rather than running QMD commands.

The router dispatches automatically. Most requests go to Query. When the user asks about query patterns, poor recall, or semantic search strategy, Semantic activates instead.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Dispatch table mapping intent to sub-skill |
| Query skill | `references/Query/SKILL.md` | QMD CLI operations, default playbook, examples |
| Query: retrieval workflow | `references/Query/references/retrieval-workflow.md` | Health checks, collection scoping, mode choice, evidence discipline |
| Query: query patterns | `references/Query/references/query-patterns.md` | Query documents, `intent:` / `lex:` / `vec:` / `hyde:`, weighting |
| Query: command cheatsheet | `references/Query/references/command-cheatsheet.md` | High-value flags, command patterns, setup, indexing, maintenance |
| Query: MCP setup | `references/Query/references/mcp-setup.md` | MCP tool names, transport, Claude Code/Desktop integration |
| Semantic skill | `references/Semantic/SKILL.md` | Semantic query pattern engineering |
| Semantic: patterns | `references/Semantic/references/semantic-patterns.md` | Detailed examples for all 9 query patterns |

**Summary:**
- **Modes:** 2 (Query, Semantic)
- **Reference documents:** 6 across both modes
- **Dependencies:** QMD CLI >= 1.1.5

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "qmd find my note about X" | Routes to Query -- runs default playbook |
| "qmd search collection Y for Z" | Routes to Query -- scoped collection search |
| "qmd what collections do I have" | Routes to Query -- health and scope check |
| "qmd update my indexes" | Routes to Query -- maintenance via command cheatsheet |
| "qmd set up MCP" | Routes to Query -- MCP setup reference |
| "qmd why is recall poor on this query" | Routes to Semantic -- diagnose and improve query |
| "qmd help me craft a better search" | Routes to Semantic -- query pattern engineering |
| "qmd use HyDE for this vague question" | Routes to Semantic -- HyDE pattern |
| "qmd decompose this complex question" | Routes to Semantic -- query decomposition pattern |

---

## Example Usage

### Find a note (Query)

```
User: qmd find my note about local markdown retrieval being better than grep

AI:
Running QMD default playbook...
1. qmd update && qmd embed && qmd status
2. Identified collection: vault_obsidian
3. qmd query "local markdown retrieval better than grep for AI agents" -c vault_obsidian -n 10
4. Reopened top hit with qmd get "#abc123"
5. Returned: qmd://vault_obsidian/notes/qmd-vs-grep.md
```

### Improve poor recall (Semantic)

```
User: qmd my search for "performance" returns irrelevant sports articles

AI:
Loading Semantic sub-skill...
Pattern: Intent disambiguation + Query expansion
- Add intent: "C++ runtime optimization, not sports"
- Use lex: "C++ performance" optimization -sports -athlete
- Use vec: how to optimize C++ program performance
Result: Relevant hits only, sports articles excluded.
```

---

## Configuration

No configuration beyond QMD CLI installation. Collections are managed via `qmd collection add`.
