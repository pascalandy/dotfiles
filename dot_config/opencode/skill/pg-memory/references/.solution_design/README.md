# pg-memory

PostgreSQL-based memory system for AI agents. Multi-user ready (SaaS-compatible).

## What It Does

Two tables for storing:

- **memories** — Agent decisions, learnings, observations, errors
- **sources** — External content: docs, podcasts, blog posts, Obsidian notes

## Key Features

| Feature          | Description                                |
| ---------------- | ------------------------------------------ |
| Multi-user       | `user_id` on all records (SaaS-ready)      |
| Full-text search | Native PostgreSQL tsvector (mixed EN/FR)   |
| Cost tracking    | Token usage and costs per memory           |
| Git context      | Link memories to repos, branches, commits  |
| Manual ingestion | `provider_id='manual'` for non-LLM content |
| Soft deletes     | Recoverable via `deleted_at`               |

## Quick Start

```bash
brew services start postgresql@18
createdb forzr
psql -v ON_ERROR_STOP=1 forzr < schema/memory.sql
./scripts/verify_pg_memory.sh
```

See [PLAN.md](./PLAN.md) for detailed setup instructions.

## Documentation

| File                                       | Description                                      |
| ------------------------------------------ | ------------------------------------------------ |
| [DATA_DICTIONARY.md](./DATA_DICTIONARY.md) | Single source of truth for all field definitions |
| [GUIDE_AGENT.md](./GUIDE_AGENT.md)         | Quick-reference SQL patterns for AI assistants   |
| [GUIDE_HUMAN.md](./GUIDE_HUMAN.md)         | Setup, analytics, maintenance for humans         |
| [SPEC.md](./SPEC.md)                       | Schema design, columns, indexes, constraints     |
| [PLAN.md](./PLAN.md)                       | Detailed setup steps and test procedures         |
| [PLAYBOOK.md](./PLAYBOOK.md)               | Comprehensive query recipes by use case          |
| [schema/memory.sql](./schema/memory.sql)   | PostgreSQL schema                                |

## Work In Progress

- **Obsidian vault ingestion** — Frontmatter schema being finalized
