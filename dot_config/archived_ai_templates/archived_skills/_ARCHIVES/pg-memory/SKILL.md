---
name: pg-memory
description: Store and retrieve memories for AI agents via PostgreSQL. Use when storing decisions/learnings/observations, retrieving past context, searching memories, or ingesting sources. Triggers "pgm," "remember this," "store memory," "search memories."
---

# pg-memory

PostgreSQL memory system with two tables: `memories` (agent decisions) and `sources` (external content).

## Connection

```bash
psql forzr -P format=wrapped -P border=2
```

## Before Running Queries: Load User Preferences

Run this query first to retrieve user-specific pg-memory preferences:

```sql
SELECT content FROM memories
WHERE user_id = 'pascalandy' AND deleted_at IS NULL
  AND type = 'observation' AND tags @> '["pg-memory"]'
ORDER BY created_at DESC;
```

Apply these preferences to all query results.

## Critical: Multi-User Filter

All queries MUST include `user_id`:

```sql
WHERE user_id = 'pascalandy' AND deleted_at IS NULL
```

---

## When to Write a Memory

**Write when:** architectural decision, user preference learned, error resolved, pattern observed, user requests it.

**Skip when:** trivial/temporary, already stored recently, better suited for README/config.

**Adding pg-memory preferences:** See [GUIDE_AGENT.md](references/.solution_design/GUIDE_AGENT.md#insert-pg-memory-preference) for the required template.

---

## 1. Insert Memory

**Minimal:**

```sql
INSERT INTO memories (user_id, provider_id, model_id, type, content)
VALUES ('pascalandy', 'anthropic', 'claude-sonnet-4', 'observation', 'User prefers concise responses.')
RETURNING id;
```

**Full (with git context):**

```sql
INSERT INTO memories (
  user_id,
  provider_id, model_id, mode, session_id,
  repo_name, repo_path, git_branch, git_commit,
  type, content, importance, tags, metadata,
  tokens_input, tokens_output, cost, response_time_ms, finish_reason
)
VALUES (
  'pascalandy',
  'anthropic', 'claude-sonnet-4', 'build', 'ses_xxx',
  'forzr', 'Documents/github_local/forzr', 'main', 'a1b2c3d',
  'decision',
  'Chose PostgreSQL over SQLite for better JSONB support.',
  6,
  '["database", "architecture"]',
  '{"alternatives": ["sqlite", "mysql"]}',
  2500, 450, 0.0156, 3200, 'stop'
)
RETURNING id, ingested_at;
```

**Error memory:**

```sql
INSERT INTO memories (
  user_id, provider_id, model_id,
  repo_name, repo_path, git_branch, git_commit,
  type, content, importance, tags, metadata
)
VALUES (
  'pascalandy', 'anthropic', 'claude-sonnet-4',
  'nuxt_blog', 'Documents/github_local/forzr/WORKDIR/nuxt_blog', 'main', 'b2c3d4e',
  'error',
  'TypeError: Cannot read property "map" of undefined',
  2,
  '["typescript", "nuxt", "bug"]',
  '{"file": "components/BlogList.vue", "line": 42, "resolved": false}'
)
RETURNING id;
```

---

## 2. Retrieve Context

**Start of session (last 20):**

```sql
SELECT id, type, content, importance, tags, created_at
FROM memories
WHERE user_id = 'pascalandy' AND deleted_at IS NULL
ORDER BY created_at DESC LIMIT 20;
```

**Today only:**

```sql
SELECT id, type, content, importance, tags
FROM memories
WHERE user_id = 'pascalandy'
  AND created_at >= CURRENT_DATE
  AND created_at < CURRENT_DATE + INTERVAL '1 day'
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

**Current session:**

```sql
SELECT id, type, content, importance
FROM memories
WHERE user_id = 'pascalandy'
  AND session_id = 'ses_xxx'
  AND deleted_at IS NULL
ORDER BY created_at;
```

**High-importance (5+):**

```sql
SELECT id, type, content, importance, tags
FROM memories
WHERE user_id = 'pascalandy' AND importance >= 5 AND deleted_at IS NULL
ORDER BY importance DESC, created_at DESC LIMIT 10;
```

**Current repository:**

```sql
SELECT id, type, content, importance, git_branch
FROM memories
WHERE user_id = 'pascalandy' AND repo_name = 'forzr' AND deleted_at IS NULL
ORDER BY created_at DESC LIMIT 20;
```

---

## 3. Search Memories

**Full-text search:**

```sql
SELECT id, content, ts_rank(content_tsv, query) as rank
FROM memories, plainto_tsquery('simple', 'postgresql jsonb') query
WHERE user_id = 'pascalandy' AND content_tsv @@ query AND deleted_at IS NULL
ORDER BY rank DESC LIMIT 10;
```

**Phrase search:**

```sql
SELECT id, content, ts_rank(content_tsv, query) as rank
FROM memories, phraseto_tsquery('simple', 'memory system') query
WHERE user_id = 'pascalandy' AND content_tsv @@ query AND deleted_at IS NULL
ORDER BY rank DESC;
```

**Boolean search (AND, OR, NOT):**

```sql
SELECT id, content
FROM memories
WHERE user_id = 'pascalandy'
  AND content_tsv @@ to_tsquery('simple', 'postgres & memory & !error')
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

**By tag (single):**

```sql
SELECT id, content, tags FROM memories
WHERE user_id = 'pascalandy' AND tags @> '["git"]' AND deleted_at IS NULL;
```

**By tags (any of):**

```sql
SELECT id, content, tags FROM memories
WHERE user_id = 'pascalandy' AND tags ?| ARRAY['git', 'coding', 'debug'] AND deleted_at IS NULL;
```

**By tags (all of):**

```sql
SELECT id, content, tags FROM memories
WHERE user_id = 'pascalandy' AND tags @> '["git", "coding"]' AND deleted_at IS NULL;
```

**By type:**

```sql
SELECT id, content, importance FROM memories
WHERE user_id = 'pascalandy' AND type = 'decision' AND deleted_at IS NULL
ORDER BY created_at DESC;
```

**Combined FTS + tag:**

```sql
SELECT id, content, tags, ts_rank(content_tsv, query) as rank
FROM memories, plainto_tsquery('simple', 'git commit') query
WHERE user_id = 'pascalandy' AND content_tsv @@ query AND tags @> '["git"]' AND deleted_at IS NULL
ORDER BY rank DESC LIMIT 10;
```

---

## 4. Ingest Source

**Manual (no LLM):**

```sql
INSERT INTO sources (
  user_id, name, title, source_type, source_url, content,
  provider_id, model_id, tags
)
VALUES (
  'pascalandy', 'Nuxt', 'Getting Started', 'documentation',
  'https://nuxt.com/docs/getting-started',
  'Full documentation content...',
  'manual', 'none',
  '["framework", "vue", "ssr"]'
)
RETURNING id;
```

**LLM-processed:**

```sql
INSERT INTO sources (
  user_id, name, title, source_type, source_url, content, author, published_at,
  provider_id, model_id, tags, tokens_input, tokens_output, cost
)
VALUES (
  'pascalandy', 'Syntax', 'Episode 842: AI in 2025', 'podcast',
  'https://syntax.fm/842', 'Transcript content...', 'Scott Tolinski', '2025-12-20',
  'anthropic', 'claude-sonnet-4',
  '["ai", "web-development"]',
  25000, 800, 0.0389
)
RETURNING id;
```

**Update docs (supersede old):**

```sql
BEGIN;
UPDATE sources SET superseded_at = NOW()
WHERE user_id = 'pascalandy' AND name = 'Nuxt' AND version = '4.0.0'
  AND superseded_at IS NULL AND deleted_at IS NULL;

INSERT INTO sources (user_id, name, title, source_type, version, content, provider_id, model_id, tags)
VALUES ('pascalandy', 'Nuxt', 'Getting Started', 'documentation', '4.1.0',
  'Updated content...', 'manual', 'none', '["framework", "vue"]');
COMMIT;
```

---

## 5. Search Sources

**By name:**

```sql
SELECT id, name, title, version, LENGTH(content) as len
FROM sources
WHERE user_id = 'pascalandy' AND name = 'Nuxt'
  AND superseded_at IS NULL AND deleted_at IS NULL;
```

**Full-text search:**

```sql
SELECT name, title, source_type, ts_rank(content_tsv, query) as rank
FROM sources, plainto_tsquery('simple', 'react hooks') query
WHERE user_id = 'pascalandy' AND content_tsv @@ query AND deleted_at IS NULL
ORDER BY rank DESC LIMIT 20;
```

**By author:**

```sql
SELECT name, title, published_at FROM sources
WHERE user_id = 'pascalandy' AND author = 'Dan Abramov' AND deleted_at IS NULL
ORDER BY published_at DESC;
```

---

## 6. Cross-Table Search

```sql
(
  SELECT 'memory' as tbl, id, content as text, ts_rank(content_tsv, query) as rank
  FROM memories, plainto_tsquery('simple', 'nuxt') query
  WHERE user_id = 'pascalandy' AND content_tsv @@ query AND deleted_at IS NULL
)
UNION ALL
(
  SELECT 'source', id, title || ': ' || LEFT(content, 200), ts_rank(content_tsv, query)
  FROM sources, plainto_tsquery('simple', 'nuxt') query
  WHERE user_id = 'pascalandy' AND content_tsv @@ query AND deleted_at IS NULL
)
ORDER BY rank DESC LIMIT 20;
```

---

## 7. Soft Delete

```sql
-- Delete
UPDATE memories SET deleted_at = NOW() WHERE id = 'uuid-here';

-- Restore
UPDATE memories SET deleted_at = NULL WHERE id = 'uuid-here';
```

---

## Conventions

### Memory Types

| Type              | When to Use                                      |
| ----------------- | ------------------------------------------------ |
| `action`          | Something you did (created file, ran command)    |
| `observation`     | Something you noticed (user preference, pattern) |
| `thought`         | Internal reasoning worth preserving              |
| `decision`        | A choice made with rationale                     |
| `error`           | Something that went wrong                        |
| `learning`        | A lesson learned                                 |
| `project_status`  | Status snapshot                                  |
| `command_summary` | Slash command execution summary                  |

### Source Types

`documentation`, `podcast`, `blog_post`, `video`, `book`, `obsidian_note`, `coding`

### Importance Scale (0-7)

| Score | Label             |
| ----- | ----------------- |
| 7     | Perfect           |
| 6     | Excellent         |
| 5     | Good              |
| 4     | Fine              |
| 3     | Meh               |
| 2     | Disappointing     |
| 1     | Avoid             |
| 0     | Unrated (default) |

### Tag Patterns

- Lowercase: `["git", "nuxt", "typescript"]`
- Hyphens for multi-word: `["bug-fix", "code-review"]`
- 2-5 tags per memory

### Git Context

| Field        | Command                                                           |
| ------------ | ----------------------------------------------------------------- |
| `repo_name`  | `basename $(git rev-parse --show-toplevel)`                       |
| `repo_path`  | `realpath --relative-to="$HOME" $(git rev-parse --show-toplevel)` |
| `git_branch` | `git branch --show-current`                                       |
| `git_commit` | `git rev-parse --short HEAD`                                      |

---

## References

| File                                                         | When to Read                                   |
| ------------------------------------------------------------ | ---------------------------------------------- |
| [GUIDE_AGENT.md](references/.solution_design/GUIDE_AGENT.md) | Insert pg-memory preferences, command tracking |
| [PLAYBOOK.md](references/PLAYBOOK.md)                        | Cost analytics, advanced queries               |
| [DATA_DICTIONARY.md](references/DATA_DICTIONARY.md)          | All column definitions, types, constraints     |
