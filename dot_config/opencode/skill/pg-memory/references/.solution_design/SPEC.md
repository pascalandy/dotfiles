# pg-memory Specifications

## Deployment Status

This is a **new database**. No existing data, no migrations required. Fresh start.

---

## Design Decisions

| Decision          | Choice                         | Rationale                                                            |
| ----------------- | ------------------------------ | -------------------------------------------------------------------- |
| Database          | PostgreSQL 18                  | Native types, JSONB, GIN indexes, FTS                                |
| Location          | Local via Homebrew             | Simple, no Docker overhead                                           |
| Database name     | `forzr`                        | Single database for simplicity                                       |
| Connection        | Config file + env var override | Flexible, secure                                                     |
| Primary key       | UUID (v7)                      | Time-ordered, better B-tree locality                                 |
| Type validation   | Flexible (no constraint)       | Easy to add new types                                                |
| Provider/Model    | Separate columns               | `provider_id` + `model_id` for analytics                             |
| Manual ingestion  | `'manual'` / `'none'`          | For non-LLM content (copy-paste, Obsidian)                           |
| Session ID        | `session_id`                   | OpenCode session ID (e.g., `ses_4a30f921fffeExOAtr8adv55fz`)         |
| Doc versioning    | `superseded_at` pattern        | Track history, query current                                         |
| Soft deletes      | `deleted_at` column            | Recoverable, audit-friendly                                          |
| Full-text search  | Native tsvector (`simple`)     | Language-agnostic for mixed EN/FR                                    |
| FTS language      | `simple`                       | No stemming, works with any language                                 |
| JSONB constraints | Enforced                       | `tags` = array, `metadata` = object                                  |
| Retention         | Keep everything                | Manual cleanup when needed                                           |
| Tables            | Two: `memories` + `sources`    | Separation of concerns                                               |
| Token tracking    | All 5 token types              | input, output, reasoning, cache_read, cache_write                    |
| Cost tracking     | `NUMERIC(15, 8)`               | Supports micro-costs and aggregations up to ~$10M                    |
| Importance scale  | 0-7 semantic scale             | 0=unrated, 1=avoid, 7=perfect                                        |
| Git context       | 4 columns                      | `repo_name`, `repo_path`, `git_branch`, `git_commit`                 |
| Command tracking  | 2 columns                      | `custom_cmd_name`, `custom_cmd_run_date` for slash command analytics |
| Multi-user        | `user_id` column               | SaaS-ready, no users table (Option A)                                |

## Out of Scope

The following are explicitly **not** part of this implementation:

| Feature                          | Reason                           | Future Consideration                           |
| -------------------------------- | -------------------------------- | ---------------------------------------------- |
| **Vector embeddings (pgvector)** | Semantic search not required     | Add if "conceptually similar" retrieval needed |
| **Automated migrations**         | Manual SQL migrations for now    | Consider `migrate` CLI if complexity grows     |
| **Connection pooling**           | Single-agent CLI access          | Add pgBouncer if multi-agent access needed     |
| **Password authentication**      | Local socket auth sufficient     | Add if remote access required                  |
| **Language-specific FTS**        | Mixed EN/FR content              | Could add `language` column + dynamic tsvector |
| **Users table**                  | Option A: user_id as string only | Add users table if user metadata needed        |
| **Row-Level Security**           | Single-user local use            | Add RLS for true multi-tenant SaaS             |

## Work In Progress

| Feature                      | Status | Notes                                         |
| ---------------------------- | ------ | --------------------------------------------- |
| **Obsidian vault ingestion** | WIP    | Schema for frontmatter fields being finalized |

## Table: `memories`

Stores agent memories — explicit decisions by the agent that something is "worth remembering."

### Columns

| Column                | Type            | Nullable | Default        | Description                                                            |
| --------------------- | --------------- | -------- | -------------- | ---------------------------------------------------------------------- |
| `id`                  | `UUID`          | NO       | `uuidv7()`     | Primary key (time-ordered)                                             |
| `user_id`             | `TEXT`          | NO       | -              | User identifier (e.g., `pascalandy`, `julia`)                          |
| `created_at`          | `TIMESTAMPTZ`   | NO       | `NOW()`        | When memory was inserted into database                                 |
| `deleted_at`          | `TIMESTAMPTZ`   | YES      | -              | Soft delete timestamp (NULL = active)                                  |
| `provider_id`         | `TEXT`          | NO       | -              | Provider identifier (e.g., `anthropic`, `openai`, `google`, `manual`)  |
| `model_id`            | `TEXT`          | NO       | -              | Model identifier (e.g., `claude-sonnet-4`, `gpt-4o`, `none`)           |
| `mode`                | `TEXT`          | YES      | -              | OpenCode mode (e.g., `build`, `plan`, `ask`)                           |
| `session_id`          | `TEXT`          | YES      | -              | OpenCode session ID (e.g., `ses_4a30f921fffeExOAtr8adv55fz`)           |
| `parent_session_id`   | `TEXT`          | YES      | -              | Parent session ID (for sub-agent/Task tool memories)                   |
| `repo_name`           | `TEXT`          | YES      | -              | Git repository name (e.g., `forzr`, `nuxt_blog`)                       |
| `repo_path`           | `TEXT`          | YES      | -              | Relative path from $HOME (e.g., `Documents/github_local/forzr`)        |
| `git_branch`          | `TEXT`          | YES      | -              | Current git branch (e.g., `main`, `feature/memory`)                    |
| `git_commit`          | `TEXT`          | YES      | -              | Current commit SHA, short form (e.g., `a1b2c3d`)                       |
| `custom_cmd_name`     | `TEXT`          | YES      | -              | Slash command path (e.g., `.opencode/command/project_status.md`)       |
| `custom_cmd_run_date` | `TEXT`          | YES      | -              | Timestamp when command started (ISO format: `2025-12-25T14:30:00`)     |
| `type`                | `TEXT`          | NO       | -              | Memory type (flexible, no constraint)                                  |
| `content`             | `TEXT`          | NO       | -              | The memory content                                                     |
| `content_tsv`         | `TSVECTOR`      | NO       | auto-generated | Full-text search vector (`simple` language)                            |
| `importance`          | `INTEGER`       | YES      | `0`            | 0-7 semantic scale (0=unrated, 1=avoid, 7=perfect)                     |
| `tags`                | `JSONB`         | YES      | -              | Array of tags: `["coding", "git"]` (CHECK: must be array or NULL)      |
| `metadata`            | `JSONB`         | YES      | -              | Additional context: `{"key": "value"}` (CHECK: must be object or NULL) |
| `tokens_input`        | `INTEGER`       | YES      | -              | Input tokens used                                                      |
| `tokens_output`       | `INTEGER`       | YES      | -              | Output tokens generated                                                |
| `tokens_reasoning`    | `INTEGER`       | YES      | -              | Reasoning/thinking tokens (for o1/extended thinking models)            |
| `tokens_cache_read`   | `INTEGER`       | YES      | -              | Tokens read from cache                                                 |
| `tokens_cache_write`  | `INTEGER`       | YES      | -              | Tokens written to cache                                                |
| `cost`                | `NUMERIC(15,8)` | YES      | -              | Cost in dollars (supports micro-costs)                                 |
| `started_at`          | `TIMESTAMPTZ`   | YES      | -              | When the LLM call started                                              |
| `completed_at`        | `TIMESTAMPTZ`   | YES      | -              | When the LLM call completed                                            |
| `response_time_ms`    | `INTEGER`       | YES      | -              | Response time in milliseconds                                          |
| `finish_reason`       | `TEXT`          | YES      | -              | How the response ended (e.g., `stop`, `length`, `tool_calls`)          |

### Constraints

| Column        | Constraint                                                      | Description                                          |
| ------------- | --------------------------------------------------------------- | ---------------------------------------------------- |
| `user_id`     | `CHECK (user_id ~ '^[a-z0-9_-]+$')`                             | Lowercase alphanumeric with underscores/hyphens      |
| `provider_id` | `CHECK (provider_id ~ '^[a-z0-9_-]+$')`                         | Lowercase alphanumeric with underscores/hyphens      |
| `model_id`    | `CHECK (model_id ~ '^[a-z0-9._-]+$')`                           | Lowercase alphanumeric with dots/underscores/hyphens |
| `importance`  | `CHECK (importance BETWEEN 0 AND 7)`                            | Valid range 0-7 (semantic scale)                     |
| `tags`        | `CHECK (tags IS NULL OR jsonb_typeof(tags) = 'array')`          | Must be JSON array or NULL                           |
| `metadata`    | `CHECK (metadata IS NULL OR jsonb_typeof(metadata) = 'object')` | Must be JSON object or NULL                          |

### Indexes

| Index                          | Columns                    | Type   | Purpose                                     |
| ------------------------------ | -------------------------- | ------ | ------------------------------------------- |
| `idx_memories_user`            | `user_id`                  | B-tree | Filter by user                              |
| `idx_memories_user_created`    | `user_id, created_at DESC` | B-tree | User's recent memories                      |
| `idx_memories_created`         | `created_at DESC`          | B-tree | Recency queries                             |
| `idx_memories_provider_model`  | `provider_id, model_id`    | B-tree | Filter by provider and/or model (composite) |
| `idx_memories_session`         | `session_id`               | B-tree | Filter by session                           |
| `idx_memories_parent_session`  | `parent_session_id`        | B-tree | Sub-agent analytics                         |
| `idx_memories_type`            | `type`                     | B-tree | Filter by type                              |
| `idx_memories_importance`      | `importance DESC`          | B-tree | Priority queries                            |
| `idx_memories_tags`            | `tags`                     | GIN    | Tag containment queries                     |
| `idx_memories_metadata`        | `metadata`                 | GIN    | Metadata key queries                        |
| `idx_memories_fts`             | `content_tsv`              | GIN    | Full-text search                            |
| `idx_memories_active`          | `deleted_at` (partial)     | B-tree | Active records only                         |
| `idx_memories_cost`            | `cost`                     | B-tree | Find expensive operations                   |
| `idx_memories_started`         | `started_at DESC`          | B-tree | Filter by LLM call time                     |
| `idx_memories_repo`            | `repo_name`                | B-tree | Filter by repository                        |
| `idx_memories_custom_cmd`      | `custom_cmd_run_date`      | B-tree | Group by command invocation                 |
| `idx_memories_custom_cmd_name` | `custom_cmd_name`          | B-tree | Aggregate by command type                   |

### Known Types (Convention)

| Type              | Description                          |
| ----------------- | ------------------------------------ |
| `action`          | Something the agent did              |
| `observation`     | Something the agent noticed          |
| `thought`         | Internal reasoning                   |
| `decision`        | A choice made                        |
| `error`           | Something that went wrong            |
| `learning`        | A lesson learned                     |
| `project_status`  | Status snapshot of projects          |
| `command_summary` | Summary of a slash command execution |

_No constraint — add new types anytime by using them._

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

## Table: `sources`

Stores external sources: documentation, blog posts, podcasts, books, transcripts, Obsidian notes, and other content you consume but did not produce.

### Columns

| Column                | Type            | Nullable | Default        | Description                                                                  |
| --------------------- | --------------- | -------- | -------------- | ---------------------------------------------------------------------------- |
| `id`                  | `UUID`          | NO       | `uuidv7()`     | Primary key (time-ordered)                                                   |
| `user_id`             | `TEXT`          | NO       | -              | User identifier (e.g., `pascalandy`, `julia`)                                |
| `name`                | `TEXT`          | NO       | -              | Source name (e.g., `Nuxt`, `Syntax`, `project-ideas.md`)                     |
| `title`               | `TEXT`          | YES      | -              | Specific piece title (e.g., `Getting Started`, `Episode 842: AI in 2025`)    |
| `source_type`         | `TEXT`          | NO       | -              | Type of source (flexible, no constraint)                                     |
| `version`             | `TEXT`          | YES      | -              | Version (e.g., `4.0.0`) or NULL if unversioned                               |
| `source_url`          | `TEXT`          | YES      | -              | URL where content was obtained                                               |
| `content`             | `TEXT`          | NO       | -              | The actual content                                                           |
| `content_tsv`         | `TSVECTOR`      | NO       | auto-generated | Full-text search vector (`simple` language)                                  |
| `author`              | `TEXT`          | YES      | -              | Who created it (e.g., `Evan You`, `Scott Tolinski`)                          |
| `published_at`        | `TIMESTAMPTZ`   | YES      | -              | When original was published                                                  |
| `ingested_at`         | `TIMESTAMPTZ`   | NO       | `NOW()`        | When you added it to the database                                            |
| `updated_at`          | `TIMESTAMPTZ`   | NO       | `NOW()`        | Last modification (auto-updated)                                             |
| `superseded_at`       | `TIMESTAMPTZ`   | YES      | -              | NULL = current, timestamp = replaced                                         |
| `deleted_at`          | `TIMESTAMPTZ`   | YES      | -              | Soft delete timestamp (NULL = active)                                        |
| `provider_id`         | `TEXT`          | NO       | -              | Provider identifier (e.g., `anthropic`, `openai`, `google`, `manual`)        |
| `model_id`            | `TEXT`          | NO       | -              | Model identifier (e.g., `claude-sonnet-4`, `gpt-4o`, `none`)                 |
| `mode`                | `TEXT`          | YES      | -              | OpenCode mode (e.g., `build`, `plan`, `ask`)                                 |
| `session_id`          | `TEXT`          | YES      | -              | OpenCode session ID (e.g., `ses_4a30f921fffeExOAtr8adv55fz`)                 |
| `parent_session_id`   | `TEXT`          | YES      | -              | Parent session ID (for sub-agent ingestions)                                 |
| `repo_name`           | `TEXT`          | YES      | -              | Git repository name where source was ingested                                |
| `repo_path`           | `TEXT`          | YES      | -              | Relative path from $HOME                                                     |
| `git_branch`          | `TEXT`          | YES      | -              | Current git branch at ingestion time                                         |
| `git_commit`          | `TEXT`          | YES      | -              | Current commit SHA at ingestion time                                         |
| `custom_cmd_name`     | `TEXT`          | YES      | -              | Slash command that triggered ingestion                                       |
| `custom_cmd_run_date` | `TEXT`          | YES      | -              | Timestamp when command started (ISO format)                                  |
| `tokens_input`        | `INTEGER`       | YES      | -              | Input tokens used (NULL for manual ingestion)                                |
| `tokens_output`       | `INTEGER`       | YES      | -              | Output tokens generated (NULL for manual ingestion)                          |
| `tokens_reasoning`    | `INTEGER`       | YES      | -              | Reasoning/thinking tokens                                                    |
| `tokens_cache_read`   | `INTEGER`       | YES      | -              | Tokens read from cache                                                       |
| `tokens_cache_write`  | `INTEGER`       | YES      | -              | Tokens written to cache                                                      |
| `cost`                | `NUMERIC(15,8)` | YES      | -              | Cost in dollars (NULL for manual ingestion)                                  |
| `started_at`          | `TIMESTAMPTZ`   | YES      | -              | When the LLM call started                                                    |
| `completed_at`        | `TIMESTAMPTZ`   | YES      | -              | When the LLM call completed                                                  |
| `response_time_ms`    | `INTEGER`       | YES      | -              | Response time in milliseconds                                                |
| `finish_reason`       | `TEXT`          | YES      | -              | How the response ended                                                       |
| `tags`                | `JSONB`         | YES      | -              | Array of tags: `["framework", "frontend"]` (CHECK: must be array or NULL)    |
| `metadata`            | `JSONB`         | YES      | -              | Additional context — flexible JSONB object for frontmatter, vault info, etc. |

### Constraints

| Column        | Constraint                                                      | Description                                          |
| ------------- | --------------------------------------------------------------- | ---------------------------------------------------- |
| `user_id`     | `CHECK (user_id ~ '^[a-z0-9_-]+$')`                             | Lowercase alphanumeric with underscores/hyphens      |
| `provider_id` | `CHECK (provider_id ~ '^[a-z0-9_-]+$')`                         | Lowercase alphanumeric with underscores/hyphens      |
| `model_id`    | `CHECK (model_id ~ '^[a-z0-9._-]+$')`                           | Lowercase alphanumeric with dots/underscores/hyphens |
| `tags`        | `CHECK (tags IS NULL OR jsonb_typeof(tags) = 'array')`          | Must be JSON array or NULL                           |
| `metadata`    | `CHECK (metadata IS NULL OR jsonb_typeof(metadata) = 'object')` | Must be JSON object or NULL                          |

### Indexes

| Index                         | Columns                        | Type   | Purpose                                     |
| ----------------------------- | ------------------------------ | ------ | ------------------------------------------- |
| `idx_sources_user`            | `user_id`                      | B-tree | Filter by user                              |
| `idx_sources_user_ingested`   | `user_id, ingested_at DESC`    | B-tree | User's recent sources                       |
| `idx_sources_lookup`          | `name, version, superseded_at` | B-tree | Find current content                        |
| `idx_sources_type`            | `source_type`                  | B-tree | Filter by type                              |
| `idx_sources_author`          | `author`                       | B-tree | Find by author                              |
| `idx_sources_ingested`        | `ingested_at DESC`             | B-tree | Recent additions                            |
| `idx_sources_updated`         | `updated_at DESC`              | B-tree | Recent modifications                        |
| `idx_sources_published`       | `published_at DESC`            | B-tree | Sort by original date                       |
| `idx_sources_provider_model`  | `provider_id, model_id`        | B-tree | Filter by provider and/or model (composite) |
| `idx_sources_session`         | `session_id`                   | B-tree | Filter by session                           |
| `idx_sources_tags`            | `tags`                         | GIN    | Tag queries                                 |
| `idx_sources_metadata`        | `metadata`                     | GIN    | Metadata queries                            |
| `idx_sources_fts`             | `content_tsv`                  | GIN    | Full-text search                            |
| `idx_sources_active`          | `deleted_at` (partial)         | B-tree | Active records only                         |
| `idx_sources_cost`            | `cost`                         | B-tree | Find expensive ingestions                   |
| `idx_sources_started`         | `started_at DESC`              | B-tree | Filter by LLM call time                     |
| `idx_sources_repo`            | `repo_name`                    | B-tree | Filter by repository                        |
| `idx_sources_custom_cmd`      | `custom_cmd_run_date`          | B-tree | Group by command invocation                 |
| `idx_sources_custom_cmd_name` | `custom_cmd_name`              | B-tree | Aggregate by command type                   |

### Known Types (Convention)

| Type            | Description                                   |
| --------------- | --------------------------------------------- |
| `documentation` | Official project docs (Nuxt, Astro, Tailwind) |
| `blog_post`     | Blog articles                                 |
| `podcast`       | Podcast episode transcripts                   |
| `video`         | YouTube/video transcripts                     |
| `book`          | Book content/chapters                         |
| `audiobook`     | Audiobook transcripts                         |
| `article`       | General web articles                          |
| `coding`        | Code examples, repos, snippets                |
| `obsidian_note` | Notes from Obsidian vault (WIP)               |

_No constraint — add new types anytime by using them._

### Manual Ingestion (Non-LLM)

For content ingested without LLM processing (copy-paste, Obsidian sync, raw files):

| Field         | Value      |
| ------------- | ---------- |
| `provider_id` | `'manual'` |
| `model_id`    | `'none'`   |
| `tokens_*`    | `NULL`     |
| `cost`        | `NULL`     |

This distinguishes human-added content from LLM-processed content.

### Column Usage Examples

| Content         | `name`           | `title`                       | `source_type` | `author`         |
| --------------- | ---------------- | ----------------------------- | ------------- | ---------------- |
| Nuxt docs       | Nuxt             | Getting Started               | documentation | NULL             |
| Podcast episode | Syntax           | Episode 842: AI in 2025       | podcast       | Scott Tolinski   |
| Blog post       | Overreacted      | A Complete Guide to useEffect | blog_post     | Dan Abramov      |
| Book chapter    | Clean Code       | Chapter 3: Functions          | book          | Robert C. Martin |
| YouTube video   | Fireship         | 100 Seconds of Rust           | video         | Jeff Delaney     |
| Obsidian note   | project-ideas.md | Project Ideas for 2025        | obsidian_note | NULL             |

### Obsidian Vault Integration (WIP)

> **Status:** Work in progress. Frontmatter schema being finalized.

**Architecture:**

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────┐
│   PROD VAULT        │     │   INDEXED VAULT     │     │  pg-memory  │
│   (your real notes) │ ──► │   (enriched copy)   │ ──► │  sources    │
│                     │     │   + generated fields│     │  table      │
└─────────────────────┘     └─────────────────────┘     └─────────────┘
```

**Mapping:**

| Obsidian                       | sources column                                                  |
| ------------------------------ | --------------------------------------------------------------- |
| Filename                       | `name`                                                          |
| Title (from frontmatter or H1) | `title`                                                         |
| `source_type`                  | `'obsidian_note'`                                               |
| Vault path                     | `source_url` (e.g., `obsidian://open?vault=dev-notes&file=...`) |
| Body content                   | `content`                                                       |
| **All frontmatter**            | `metadata` (as JSONB object)                                    |
| Tags from frontmatter          | `tags` (as JSONB array)                                         |
| `provider_id`                  | `'manual'`                                                      |
| `model_id`                     | `'none'`                                                        |

**Key insight:** Frontmatter goes into `metadata` as a flexible JSONB object. If you add new frontmatter fields in Obsidian, they just appear in the JSON — no schema change needed.

**Example frontmatter (user-authored + generated):**

```yaml
---
# User-authored fields
tags:
  - area/resource/webclip
  - area/resource/app/cli
project_id: pg-memory
date_created: 2025-12-26
date_updated: 2025-12-26
source: https://github.com/example/repo
is_private: false

# Generated fields (added during indexing)
schema_version: "1.0"
ai_summary: "TODO: generate summary"
date_indexed: 2025-12-27
links_internal:
  - 2025-W22
  - 2025-05-29
links_incoming: []
links_incoming_count: 0
word_count: 342
---
```

**All of this becomes `metadata` JSONB:**

```json
{
  "tags": ["area/resource/webclip", "area/resource/app/cli"],
  "project_id": "pg-memory",
  "date_created": "2025-12-26",
  "date_updated": "2025-12-26",
  "source": "https://github.com/example/repo",
  "is_private": false,
  "schema_version": "1.0",
  "ai_summary": "TODO: generate summary",
  "date_indexed": "2025-12-27",
  "links_internal": ["2025-W22", "2025-05-29"],
  "links_incoming": [],
  "links_incoming_count": 0,
  "word_count": 342
}
```

**Querying Obsidian notes:**

```sql
-- Find notes with a specific project_id
SELECT name, title FROM sources
WHERE user_id = 'pascalandy'
  AND source_type = 'obsidian_note'
  AND metadata->>'project_id' = 'pg-memory'
  AND deleted_at IS NULL;

-- Find private notes
SELECT name, title FROM sources
WHERE user_id = 'pascalandy'
  AND source_type = 'obsidian_note'
  AND (metadata->>'is_private')::boolean = true
  AND deleted_at IS NULL;

-- Find notes with backlinks
SELECT name, title, metadata->'links_incoming_count' as backlinks
FROM sources
WHERE user_id = 'pascalandy'
  AND source_type = 'obsidian_note'
  AND (metadata->>'links_incoming_count')::int > 0
  AND deleted_at IS NULL
ORDER BY (metadata->>'links_incoming_count')::int DESC;
```

### Versioning Pattern

When ingesting updated content for a source:

1. **Mark old as superseded:**

   ```sql
   UPDATE sources
   SET superseded_at = NOW()
   WHERE name = 'Nuxt'
     AND version = '4.0.0'
     AND superseded_at IS NULL
     AND deleted_at IS NULL;
   ```

2. **Insert new:**
   ```sql
   INSERT INTO sources (user_id, name, title, source_type, version, source_url, content, author, provider_id, model_id, tags)
   VALUES ('pascalandy', 'Nuxt', 'Getting Started', 'documentation', '4.0.0', 'https://nuxt.com/docs', '...', NULL, 'anthropic', 'claude-opus-4', '["framework", "vue"]');
   ```

### Non-Versioned Content

For content that doesn't have versions (podcasts, blog posts, videos):

- Leave `version` as NULL
- Leave `superseded_at` as NULL (it will never be superseded)
- Use `published_at` to track when the original was created

### Soft Delete Pattern

To "delete" a record (recoverable):

```sql
UPDATE memories SET deleted_at = NOW() WHERE id = 'uuid-here';
UPDATE sources SET deleted_at = NOW() WHERE id = 'uuid-here';
```

To query active records only:

```sql
SELECT * FROM memories WHERE deleted_at IS NULL;
SELECT * FROM sources WHERE deleted_at IS NULL;
```

To permanently delete old soft-deleted records:

```sql
DELETE FROM memories WHERE deleted_at < NOW() - INTERVAL '90 days';
DELETE FROM sources WHERE deleted_at < NOW() - INTERVAL '90 days';
```

## Multi-User Support

### Design (Option A: No Users Table)

- `user_id` is a required string identifier on both tables
- Format: lowercase alphanumeric with underscores/hyphens (e.g., `pascalandy`, `julia`)
- User management happens externally (auth system, config file)
- No referential integrity — just a string column

### Why Option A?

| Pros                               | Cons                           |
| ---------------------------------- | ------------------------------ |
| Simple — no joins needed           | No user metadata in database   |
| Fast — no FK lookups               | No referential integrity       |
| Flexible — add users by using them | Can't query "all users" easily |

### Query Pattern

All queries should include `WHERE user_id = 'pascalandy'`:

```sql
-- Before (single-user)
SELECT * FROM memories WHERE deleted_at IS NULL ORDER BY created_at DESC LIMIT 20;

-- After (multi-user)
SELECT * FROM memories
WHERE user_id = 'pascalandy'
  AND deleted_at IS NULL
ORDER BY created_at DESC LIMIT 20;
```

### Adding a New User

Just start using the new `user_id`:

```sql
INSERT INTO memories (user_id, provider_id, model_id, type, content)
VALUES ('julia', 'anthropic', 'claude-sonnet-4', 'observation', 'First memory for Julia');
```

### Future: Row-Level Security

For true SaaS multi-tenancy, PostgreSQL RLS can enforce isolation:

```sql
-- Not implemented yet — for future consideration
ALTER TABLE memories ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_isolation ON memories
  USING (user_id = current_setting('app.current_user'));
```

## Connection Configuration

### Priority Order

1. **Config file:** `~/.config/forzr/db.conf` (primary)
2. **Environment variable:** `DATABASE_URL` (override)

### Config File

**Location:** `~/.config/forzr/db.conf`

**Format (INI):**

```ini
[database]
host=localhost
port=5432
dbname=forzr
user=<your-macos-username>
```

### Environment Variable (Optional Override)

```bash
export DATABASE_URL="postgres://localhost:5432/forzr"
```

## PostgreSQL Features Used

| Feature                          | Usage                                                   |
| -------------------------------- | ------------------------------------------------------- |
| `UUID`                           | Primary keys via `uuidv7()` (time-ordered, native PG18) |
| `TIMESTAMPTZ`                    | All timestamps (timezone-aware)                         |
| `NUMERIC(15,8)`                  | Cost tracking with micro-cent precision                 |
| `JSONB`                          | Tags and metadata (binary, indexable)                   |
| `GIN`                            | Indexes for JSONB and tsvector                          |
| `TSVECTOR`                       | Full-text search (auto-generated, `simple` config)      |
| `GENERATED ALWAYS AS ... STORED` | Auto-computed tsvector                                  |
| `CHECK` constraints              | JSONB type validation, provider/model format validation |
| Composite indexes                | `(provider_id, model_id)` for analytics queries         |
| Partial indexes                  | Active records only (`WHERE deleted_at IS NULL`)        |
| Triggers                         | Auto-update `updated_at` on sources                     |

## OpenCode Integration

### Epoch Conversion

OpenCode returns timestamps as Unix epoch in milliseconds. Convert to `TIMESTAMPTZ`:

```sql
-- Convert OpenCode epoch milliseconds to TIMESTAMPTZ
-- Example: 1735200000000 → '2024-12-26 12:00:00+00'
to_timestamp(epoch_ms / 1000.0) AT TIME ZONE 'UTC'
```

### Token Fields

| Field                | Description                                         |
| -------------------- | --------------------------------------------------- |
| `tokens_input`       | Tokens in the prompt/context                        |
| `tokens_output`      | Tokens in the response                              |
| `tokens_reasoning`   | Extended thinking tokens (o1, Claude with thinking) |
| `tokens_cache_read`  | Tokens retrieved from provider cache                |
| `tokens_cache_write` | Tokens written to provider cache                    |

### Finish Reasons

Common values for `finish_reason`:

- `stop` — Normal completion
- `length` — Hit max tokens limit
- `tool_calls` — Stopped to execute tools
- `content_filter` — Blocked by safety filter
- `error` — Error during generation

## Git Context

Memories and sources can be linked to their git context for better traceability.

### Fields

| Field        | Description                | Example                        |
| ------------ | -------------------------- | ------------------------------ |
| `repo_name`  | Repository basename        | `forzr`, `nuxt_blog`           |
| `repo_path`  | Relative path from $HOME   | `Documents/github_local/forzr` |
| `git_branch` | Current branch             | `main`, `feature/memory`       |
| `git_commit` | Short commit SHA (7 chars) | `a1b2c3d`                      |

### Capturing Git Context

```bash
# Get repo name
basename $(git rev-parse --show-toplevel)

# Get repo path (relative to $HOME)
realpath --relative-to="$HOME" $(git rev-parse --show-toplevel)

# Get current branch
git branch --show-current

# Get current commit (short)
git rev-parse --short HEAD
```

### Use Cases

- **"What did I learn in this repo?"** — Filter by `repo_name`
- **"What was I working on at this commit?"** — Filter by `git_commit`
- **"Show memories from feature branches"** — Filter by `git_branch`

## Command Tracking

Track slash command executions for analytics and historical comparison.

### Fields

| Field                 | Description                                 | Example                               |
| --------------------- | ------------------------------------------- | ------------------------------------- |
| `custom_cmd_name`     | Full path to command file                   | `.opencode/command/project_status.md` |
| `custom_cmd_run_date` | Timestamp when command started (ISO format) | `2025-12-25T14:30:00`                 |

### How It Works

1. When a slash command starts, record the timestamp as `custom_cmd_run_date`
2. At command completion, write ONE summary memory with:
   - `type`: `command_summary`
   - `custom_cmd_name`: full path to command
   - `custom_cmd_run_date`: start timestamp
   - `started_at` / `completed_at`: timing
   - `cost`: total cost across all sub-agents
   - `metadata`: additional details (projects analyzed, errors, etc.)

### Example Summary Memory

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
);
```

### Analytics Queries

**Average duration by command:**

```sql
SELECT
  custom_cmd_name,
  COUNT(*) as runs,
  ROUND(AVG(response_time_ms) / 60000.0, 1) as avg_minutes,
  ROUND(SUM(cost)::numeric, 4) as total_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name IS NOT NULL
  AND deleted_at IS NULL
GROUP BY custom_cmd_name
ORDER BY runs DESC;
```

**Compare this week vs last week:**

```sql
SELECT
  CASE
    WHEN created_at > NOW() - INTERVAL '7 days' THEN 'This week'
    ELSE 'Last week'
  END as period,
  COUNT(*) as runs,
  ROUND(AVG(response_time_ms) / 60000.0, 1) as avg_minutes,
  ROUND(AVG(cost)::numeric, 6) as avg_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name = '.opencode/command/project_status.md'
  AND created_at > NOW() - INTERVAL '14 days'
  AND deleted_at IS NULL
GROUP BY period;
```
