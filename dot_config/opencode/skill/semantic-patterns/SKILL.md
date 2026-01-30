---
name: semantic-patterns
description: Transform user questions into effective vector search queries for RAG systems. Use when building semantic search, designing RAG pipelines, writing retrieval code, or debugging poor recall. Covers query expansion, decomposition, HyDE, metadata filtering, multi-hop retrieval, and result aggregation.
---

# Semantic Search Query Patterns

Query engineering determines retrieval quality. Raw user questions rarely match how information is stored. These patterns transform user intent into effective vector searches.

**Core principle:** Combine patterns. A single search often benefits from expansion + filtering + temporal awareness.

## Query Patterns

| Pattern | When to Use |
|---------|-------------|
| **Expansion** | User vocabulary differs from document vocabulary; want recall over precision |
| **Decomposition** | Multi-faceted questions (procedure + legal + technical); cross-domain queries |
| **Contextual Rewriting** | Multi-turn conversations; pronouns or references to previous context |
| **Diagnostic Expansion** | User describes a problem; troubleshooting scenarios |
| **Self-Ask** | Ambiguous queries; high-stakes queries where precision matters |
| **HyDE** | Vague questions; user doesn't know domain vocabulary; large semantic gap |
| **Metadata Pre-filtering** | Large corpus; known user context; document lifecycle states |
| **Multi-hop Retrieval** | Questions about document relationships; hierarchical navigation |
| **Temporal Rewriting** | Versioned corpus; time-sensitive documents; document lifecycle |

## Pattern Combinations

**Complex compliance question:**
1. Decomposition - Break into legal + procedural sub-queries
2. Metadata filtering - Filter by region and doc_type
3. Temporal - Ensure current/approved versions

**Vague troubleshooting query:**
1. Self-Ask - Generate clarifying questions
2. Diagnostic Expansion - Cover symptoms + causes + solutions
3. Query Expansion - Add vocabulary variations

**Follow-up in conversation:**
1. Contextual Rewriting - Inject prior context
2. HyDE - Bridge short question to detailed docs
3. Multi-hop - Find referenced doc, then search within it

## Result Aggregation

When running multiple queries:
- **Reciprocal Rank Fusion (RRF)**: Weight by position across result sets
- **Score normalization**: Normalize similarity scores, then combine
- **De-duplication**: Remove duplicate chunks by ID before final ranking

## Reference

For code examples and implementation details of each pattern, see [patterns.md](references/patterns.md).
