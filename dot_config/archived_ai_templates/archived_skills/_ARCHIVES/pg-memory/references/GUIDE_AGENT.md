# pg-memory Agent Guide

## Goal

You are an AI assistant with access to a PostgreSQL memory system. Use it to:

1. **Remember** — Store decisions, learnings, observations, and errors worth recalling
2. **Retrieve** — Pull relevant context from past sessions before starting work
3. **Search** — Find specific memories or external sources (docs, podcasts, blogs, Obsidian notes)

This guide provides ready-to-use SQL patterns. For schema details, see [SPEC.md](./SPEC.md). For advanced queries, see [PLAYBOOK.md](./PLAYBOOK.md).

## Important: Multi-User

All queries must include `user_id`. The current user is typically `'pascalandy'` unless specified otherwise.

```sql
-- Always filter by user_id
WHERE user_id = 'pascalandy' AND deleted_at IS NULL
```

---

## When to Write a Memory

**Write a memory when:**

- You make an architectural decision
- You learn something about the user's preferences
- You encounter and resolve an error
- You observe a pattern worth remembering
- The user explicitly asks you to remember something

**Skip writing when:**

- The information is trivial or temporary
- It's already stored in a recent memory
- It's project-specific context better suited for a README or config file

---

## Insert pg-memory Preference

When the user asks to add a preference for pg-memory (e.g., "add my preference XYZ for pg-memory"), use this template. **All fields shown are required** to avoid NULL tags or missing importance:

```sql
INSERT INTO memories (
  user_id,
  provider_id,
  model_id,
  type,
  content,
  importance,
  tags
)
VALUES (
  'pascalandy',
  'anthropic',
  'claude-sonnet-4',
  'observation',
  'When using the pg-memory skill, <PREFERENCE_DESCRIPTION>.',
  5,
  '["pg-memory", "preference", "formatting"]'
)
RETURNING id, content, tags, importance;
```

**Required fields checklist:**

- `type` = `'observation'` (preferences are observations about user behavior)
- `importance` = `5` (Good — preferences are worth remembering)
- `tags` = must include `"pg-memory"` and `"preference"` at minimum
- `content` = should start with "When using the pg-memory skill, ..."

**Example — user says "add preference: always show row counts":**

```sql
INSERT INTO memories (
  user_id, provider_id, model_id, type, content, importance, tags
)
VALUES (
  'pascalandy', 'anthropic', 'claude-sonnet-4', 'observation',
  'When using the pg-memory skill, always show row counts in query results.',
  5,
  '["pg-memory", "preference", "formatting"]'
)
RETURNING id, content, tags, importance;
```

---

## Quick Reference

### 1. Insert a Memory

**Minimal insert** (when you just need to store something quickly):

```sql
INSERT INTO memories (user_id, provider_id, model_id, type, content)
VALUES ('pascalandy', 'anthropic', 'claude-sonnet-4', 'observation', 'User prefers concise responses.')
RETURNING id;
```

**Full insert** (with OpenCode context and git context):

```sql
INSERT INTO memories (
  user_id,
  provider_id, model_id, mode,
  session_id,
  repo_name, repo_path, git_branch, git_commit,
  type, content, importance, tags, metadata,
  tokens_input, tokens_output, tokens_reasoning,
  cost, response_time_ms, finish_reason
)
VALUES (
  'pascalandy',
  'anthropic', 'claude-sonnet-4', 'build',
  'ses_4a30f921fffeExOAtr8adv55fz',
  'forzr', 'Documents/github_local/forzr', 'main', 'a1b2c3d',
  'decision',
  'Chose PostgreSQL over SQLite for better JSONB support and full-text search.',
  6,
  '["database", "architecture"]',
  '{"alternatives_considered": ["sqlite", "mysql"], "reason": "native jsonb"}',
  2500, 450, 1200,
  0.0156, 3200, 'stop'
)
RETURNING id, created_at;
```

**Insert an error** (for debugging patterns):

```sql
INSERT INTO memories (
  user_id,
  provider_id, model_id, session_id,
  repo_name, repo_path, git_branch, git_commit,
  type, content, importance, tags, metadata
)
VALUES (
  'pascalandy',
  'anthropic', 'claude-sonnet-4', 'ses_4a30f921fffeExOAtr8adv55fz',
  'nuxt_blog', 'Documents/github_local/forzr/WORKDIR/nuxt_blog', 'main', 'b2c3d4e',
  'error',
  'TypeError: Cannot read property "map" of undefined in BlogList component',
  2,
  '["typescript", "nuxt", "bug"]',
  '{"file": "components/BlogList.vue", "line": 42, "resolved": false}'
)
RETURNING id;
```

---

### 2. Retrieve Recent Context

**Start of session** — Get last 20 memories to understand recent work:

```sql
SELECT id, type, content, importance, tags, created_at
FROM memories
WHERE user_id = 'pascalandy'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 20;
```

**Today's memories only:**

```sql
SELECT id, type, content, importance, tags
FROM memories
WHERE user_id = 'pascalandy'
  AND created_at >= CURRENT_DATE
  AND created_at < CURRENT_DATE + INTERVAL '1 day'
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

**Current session memories:**

```sql
SELECT id, type, content, importance
FROM memories
WHERE user_id = 'pascalandy'
  AND session_id = 'ses_4a30f921fffeExOAtr8adv55fz'
  AND deleted_at IS NULL
ORDER BY created_at;
```

**High-importance memories** (5+, Good or better):

```sql
SELECT id, type, content, importance, tags
FROM memories
WHERE user_id = 'pascalandy'
  AND importance >= 5
  AND deleted_at IS NULL
ORDER BY importance DESC, created_at DESC
LIMIT 10;
```

**Memories from current repository:**

```sql
SELECT id, type, content, importance, git_branch, git_commit
FROM memories
WHERE user_id = 'pascalandy'
  AND repo_name = 'forzr'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 20;
```

---

### 3. Search Memories

**Full-text search** (keyword-based):

```sql
SELECT id, content, ts_rank(content_tsv, query) as rank
FROM memories, plainto_tsquery('simple', 'postgresql jsonb') query
WHERE user_id = 'pascalandy'
  AND content_tsv @@ query
  AND deleted_at IS NULL
ORDER BY rank DESC
LIMIT 10;
```

**Phrase search** (exact phrase):

```sql
SELECT id, content, ts_rank(content_tsv, query) as rank
FROM memories, phraseto_tsquery('simple', 'memory system') query
WHERE user_id = 'pascalandy'
  AND content_tsv @@ query
  AND deleted_at IS NULL
ORDER BY rank DESC;
```

**Boolean search** (AND, OR, NOT):

```sql
SELECT id, content
FROM memories
WHERE user_id = 'pascalandy'
  AND content_tsv @@ to_tsquery('simple', 'postgres & memory & !error')
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

**By tag** (single tag):

```sql
SELECT id, content, tags
FROM memories
WHERE user_id = 'pascalandy'
  AND tags @> '["git"]'
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

**By tags** (any of these):

```sql
SELECT id, content, tags
FROM memories
WHERE user_id = 'pascalandy'
  AND tags ?| ARRAY['git', 'coding', 'debug']
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

**By tags** (all of these):

```sql
SELECT id, content, tags
FROM memories
WHERE user_id = 'pascalandy'
  AND tags @> '["git", "coding"]'
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

**By type:**

```sql
SELECT id, content, importance
FROM memories
WHERE user_id = 'pascalandy'
  AND type = 'decision'
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

**Combined: FTS + tag:**

```sql
SELECT id, content, tags, ts_rank(content_tsv, query) as rank
FROM memories, plainto_tsquery('simple', 'git commit') query
WHERE user_id = 'pascalandy'
  AND content_tsv @@ query
  AND tags @> '["git"]'
  AND deleted_at IS NULL
ORDER BY rank DESC
LIMIT 10;
```

---

### 4. Ingest a Source

**Manual ingestion** (no LLM processing — copy-paste, raw files):

```sql
INSERT INTO sources (
  user_id, name, title, source_type, source_url, content,
  provider_id, model_id, tags
)
VALUES (
  'pascalandy',
  'Nuxt',
  'Getting Started',
  'documentation',
  'https://nuxt.com/docs/getting-started',
  'Full documentation content here...',
  'manual', 'none',
  '["framework", "vue", "ssr"]'
)
RETURNING id;
```

**LLM-processed ingestion** (with summarization, transcription, etc.):

```sql
INSERT INTO sources (
  user_id, name, title, source_type, source_url, content, author, published_at,
  provider_id, model_id, tags,
  tokens_input, tokens_output, cost
)
VALUES (
  'pascalandy',
  'Syntax',
  'Episode 842: AI in 2025',
  'podcast',
  'https://syntax.fm/842',
  'Transcript content here...',
  'Scott Tolinski',
  '2025-12-20',
  'anthropic', 'claude-sonnet-4',
  '["ai", "web-development"]',
  25000, 800, 0.0389
)
RETURNING id;
```

**Blog post** (manual, no processing cost):

```sql
INSERT INTO sources (
  user_id, name, title, source_type, source_url, content, author, published_at,
  provider_id, model_id, tags
)
VALUES (
  'pascalandy',
  'Overreacted',
  'A Complete Guide to useEffect',
  'blog_post',
  'https://overreacted.io/a-complete-guide-to-useeffect/',
  'Blog content here...',
  'Dan Abramov',
  '2019-03-09',
  'manual', 'none',
  '["react", "hooks"]'
)
RETURNING id;
```

**Obsidian note** (WIP — schema being finalized):

```sql
INSERT INTO sources (
  user_id, name, title, source_type, source_url, content,
  provider_id, model_id, tags, metadata
)
VALUES (
  'pascalandy',
  'project-ideas.md',
  'Project Ideas for 2025',
  'obsidian_note',
  'obsidian://open?vault=dev-notes&file=project-ideas',
  'The actual markdown content...',
  'manual', 'none',
  '["ideas", "projects", "2025"]',
  '{
    "date_created": "2025-12-26",
    "date_updated": "2025-12-26",
    "is_private": false,
    "schema_version": "1.0",
    "word_count": 342,
    "links_incoming_count": 0
  }'
)
RETURNING id;
```

**Update documentation** (supersede old version):

```sql
BEGIN;

-- Mark old as superseded
UPDATE sources
SET superseded_at = NOW()
WHERE user_id = 'pascalandy'
  AND name = 'Nuxt'
  AND version = '4.0.0'
  AND superseded_at IS NULL
  AND deleted_at IS NULL;

-- Insert new version
INSERT INTO sources (
  user_id, name, title, source_type, version, source_url, content,
  provider_id, model_id, tags
)
VALUES (
  'pascalandy',
  'Nuxt',
  'Getting Started',
  'documentation',
  '4.1.0',
  'https://nuxt.com/docs/getting-started',
  'Updated documentation content...',
  'manual', 'none',
  '["framework", "vue", "ssr"]'
);

COMMIT;
```

---

### 5. Search Sources

**Current docs by name:**

```sql
SELECT id, name, title, version, LENGTH(content) as content_length
FROM sources
WHERE user_id = 'pascalandy'
  AND name = 'Nuxt'
  AND superseded_at IS NULL
  AND deleted_at IS NULL;
```

**Full-text search across sources:**

```sql
SELECT name, title, source_type, ts_rank(content_tsv, query) as rank
FROM sources, plainto_tsquery('simple', 'react hooks') query
WHERE user_id = 'pascalandy'
  AND content_tsv @@ query
  AND deleted_at IS NULL
ORDER BY rank DESC
LIMIT 20;
```

**Search documentation only:**

```sql
SELECT name, title, ts_rank(content_tsv, query) as rank
FROM sources, plainto_tsquery('simple', 'nuxt vue ssr') query
WHERE user_id = 'pascalandy'
  AND content_tsv @@ query
  AND source_type = 'documentation'
  AND superseded_at IS NULL
  AND deleted_at IS NULL
ORDER BY rank DESC
LIMIT 10;
```

**Find by author:**

```sql
SELECT name, title, published_at, source_url
FROM sources
WHERE user_id = 'pascalandy'
  AND author = 'Dan Abramov'
  AND deleted_at IS NULL
ORDER BY published_at DESC;
```

**Search Obsidian notes** (WIP):

```sql
SELECT name, title, metadata->>'word_count' as words
FROM sources
WHERE user_id = 'pascalandy'
  AND source_type = 'obsidian_note'
  AND deleted_at IS NULL
ORDER BY ingested_at DESC
LIMIT 20;
```

---

### 6. Cross-Table Search

**Search both memories and sources for a topic:**

```sql
(
  SELECT 'memory' as source_table, id, content as text, created_at as date,
         ts_rank(content_tsv, query) as rank
  FROM memories, plainto_tsquery('simple', 'nuxt') query
  WHERE user_id = 'pascalandy' AND content_tsv @@ query AND deleted_at IS NULL
)
UNION ALL
(
  SELECT 'source' as source_table, id, title || ': ' || LEFT(content, 200) as text,
         ingested_at as date, ts_rank(content_tsv, query) as rank
  FROM sources, plainto_tsquery('simple', 'nuxt') query
  WHERE user_id = 'pascalandy' AND content_tsv @@ query AND deleted_at IS NULL
)
ORDER BY rank DESC
LIMIT 20;
```

---

## Conventions

### Memory Types

| Type              | When to Use                                        |
| ----------------- | -------------------------------------------------- |
| `action`          | Something you did (created file, ran command)      |
| `observation`     | Something you noticed (user preference, pattern)   |
| `thought`         | Internal reasoning worth preserving                |
| `decision`        | A choice made with rationale                       |
| `error`           | Something that went wrong (with resolution status) |
| `learning`        | A lesson learned                                   |
| `project_status`  | Status snapshot of a project                       |
| `command_summary` | Summary of a slash command execution               |

No constraint enforced — add new types as needed.

### Importance Scale (0-7)

| Score | Label         | Meaning                                         |
| ----- | ------------- | ----------------------------------------------- |
| 7     | Perfect       | Nothing to change, flawless                     |
| 6     | Excellent     | Life-changing, would enthusiastically recommend |
| 5     | Good          | Would recommend with minor caveats              |
| 4     | Fine          | No strong feelings, wouldn't discourage         |
| 3     | Meh           | Wouldn't recommend, but not upset I tried       |
| 2     | Disappointing | Regret it, would warn others                    |
| 1     | Avoid         | Harmful, offensive, or a complete waste         |
| 0     | Unrated       | Not yet evaluated (default)                     |

**Usage notes:**

- Default is `0` (unrated) — evaluate later if needed
- Negative evaluations (1-2) typically come from user feedback
- Score `1` reserved for serious issues (crashes, data loss, prod incidents)

### Tag Patterns

- Use lowercase: `["git", "nuxt", "typescript"]`
- Use hyphens for multi-word: `["bug-fix", "code-review"]`
- Be consistent: pick one term and stick with it
- Keep tags focused: 2-5 tags per memory is ideal

### Session ID

The `session_id` is provided by OpenCode.

Example: `ses_4a30f921fffeExOAtr8adv55fz`

---

## Git Context

Capture the current git context to link memories to their codebase location.

### Fields

| Field        | How to Get                                                        | Example                        |
| ------------ | ----------------------------------------------------------------- | ------------------------------ |
| `repo_name`  | `basename $(git rev-parse --show-toplevel)`                       | `forzr`                        |
| `repo_path`  | `realpath --relative-to="$HOME" $(git rev-parse --show-toplevel)` | `Documents/github_local/forzr` |
| `git_branch` | `git branch --show-current`                                       | `main`                         |
| `git_commit` | `git rev-parse --short HEAD`                                      | `a1b2c3d`                      |

### Use Cases

- **"What did I learn in this repo?"** — Filter by `repo_name`
- **"What was I working on at this commit?"** — Filter by `git_commit`
- **"Show memories from feature branches"** — Filter by `git_branch`

---

## Command Tracking

When executing slash commands (like `/project-status`), write a summary memory at completion.

### Command Summary Pattern

```sql
INSERT INTO memories (
  user_id,
  provider_id, model_id, type, content, importance,
  repo_name, repo_path, git_branch, git_commit,
  custom_cmd_name, custom_cmd_run_date,
  started_at, completed_at, response_time_ms, cost,
  metadata
)
VALUES (
  'pascalandy',
  'anthropic', 'claude-sonnet-4',
  'command_summary',
  'Completed project status: 21/21 projects analyzed, 0 void',
  5,
  'forzr', 'Documents/github_local/forzr', 'main', 'a1b2c3d',
  '.opencode/command/project_status.md', '2025-12-25T14:30:00',
  '2025-12-25 14:30:00', '2025-12-25 14:42:34', 754000, 0.0856,
  '{"analyzed": 21, "void": 0, "manifest_path": "_personal/statut_de_projet/STATUT_2025_12_25_14h30_00/manifest.yml"}'
)
RETURNING id;
```

### Query Command History

**All runs of a specific command:**

```sql
SELECT
  custom_cmd_run_date,
  created_at,
  response_time_ms / 60000.0 as minutes,
  cost,
  content
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name = '.opencode/command/project_status.md'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 10;
```

**Average duration for a command:**

```sql
SELECT
  COUNT(*) as runs,
  ROUND(AVG(response_time_ms) / 60000.0, 1) as avg_minutes,
  ROUND(SUM(cost)::numeric, 4) as total_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name = '.opencode/command/project_status.md'
  AND deleted_at IS NULL;
```

---

## OpenCode Context

When writing memories, capture these fields from the current OpenCode context:

| Field              | Source                              | Description                     |
| ------------------ | ----------------------------------- | ------------------------------- |
| `provider_id`      | `AssistantMessage.providerID`       | `anthropic`, `openai`, `google` |
| `model_id`         | `AssistantMessage.modelID`          | `claude-sonnet-4`, `gpt-4o`     |
| `mode`             | `AssistantMessage.mode`             | `build`, `plan`, `ask`          |
| `session_id`       | `Session.id`                        | OpenCode session ID             |
| `tokens_input`     | `AssistantMessage.tokens.input`     | Input tokens                    |
| `tokens_output`    | `AssistantMessage.tokens.output`    | Output tokens                   |
| `tokens_reasoning` | `AssistantMessage.tokens.reasoning` | Extended thinking tokens        |
| `cost`             | `AssistantMessage.cost`             | Cost in dollars                 |
| `finish_reason`    | `AssistantMessage.finish`           | `stop`, `length`, `tool_calls`  |

**Epoch conversion** (OpenCode returns milliseconds):

```sql
-- Convert OpenCode epoch ms to TIMESTAMPTZ
to_timestamp(epoch_ms / 1000.0) AT TIME ZONE 'UTC'
```

---

## Soft Delete

Never hard-delete memories. Use soft delete:

```sql
UPDATE memories SET deleted_at = NOW() WHERE id = 'uuid-here';
```

To restore:

```sql
UPDATE memories SET deleted_at = NULL WHERE id = 'uuid-here';
```

---

## References

- [SPEC.md](./SPEC.md) — Full schema, columns, indexes, constraints
- [PLAYBOOK.md](./PLAYBOOK.md) — Comprehensive query recipes by use case
- [PLAN.md](./PLAN.md) — Setup and maintenance commands
