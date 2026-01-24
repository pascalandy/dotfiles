# pg-memory Data Dictionary

Single source of truth for all field definitions.

---

## Table: `memories`

Stores agent memories — decisions, learnings, observations, errors.

### Core Fields

| Column       | Type        | Nullable | Default    | Source         | Example                                | Description                                                    |
| ------------ | ----------- | -------- | ---------- | -------------- | -------------------------------------- | -------------------------------------------------------------- |
| `id`         | UUID        | NO       | `uuidv7()` | Auto-generated | `019400a0-1234-7abc-8def-0123456789ab` | Primary key (time-ordered UUIDv7)                              |
| `user_id`    | TEXT        | NO       | -          | User config    | `pascalandy`                           | User identifier (lowercase alphanumeric, underscores, hyphens) |
| `created_at` | TIMESTAMPTZ | NO       | `NOW()`    | Auto-generated | `2025-12-25 14:30:00-05`               | When memory was inserted into database                         |
| `deleted_at` | TIMESTAMPTZ | YES      | NULL       | Manual         | `2025-12-26 10:00:00-05`               | Soft delete timestamp (NULL = active)                          |

### LLM Context

| Column        | Type | Nullable | Default | Source                                 | Example           | Description                                             |
| ------------- | ---- | -------- | ------- | -------------------------------------- | ----------------- | ------------------------------------------------------- |
| `provider_id` | TEXT | NO       | -       | OpenCode `AssistantMessage.providerID` | `anthropic`       | LLM provider: `anthropic`, `openai`, `google`, `manual` |
| `model_id`    | TEXT | NO       | -       | OpenCode `AssistantMessage.modelID`    | `claude-sonnet-4` | Model identifier: `claude-sonnet-4`, `gpt-4o`, `none`   |
| `mode`        | TEXT | YES      | NULL    | OpenCode `AssistantMessage.mode`       | `build`           | OpenCode mode: `build`, `plan`, `ask`                   |

### Session Tracking

| Column              | Type | Nullable | Default | Source                      | Example                          | Description                                          |
| ------------------- | ---- | -------- | ------- | --------------------------- | -------------------------------- | ---------------------------------------------------- |
| `session_id`        | TEXT | YES      | NULL    | OpenCode `Session.id`       | `ses_4a30f921fffeExOAtr8adv55fz` | OpenCode session identifier                          |
| `parent_session_id` | TEXT | YES      | NULL    | OpenCode `Session.parentID` | `ses_4a30f921fffeExOAtr8adv55fz` | Parent session ID (for sub-agent/Task tool memories) |

### Git Context

| Column       | Type | Nullable | Default | Source                                                            | Example                        | Description                         |
| ------------ | ---- | -------- | ------- | ----------------------------------------------------------------- | ------------------------------ | ----------------------------------- |
| `repo_name`  | TEXT | YES      | NULL    | `basename $(git rev-parse --show-toplevel)`                       | `forzr`                        | Git repository name                 |
| `repo_path`  | TEXT | YES      | NULL    | `realpath --relative-to="$HOME" $(git rev-parse --show-toplevel)` | `Documents/github_local/forzr` | Repository path relative to $HOME   |
| `git_branch` | TEXT | YES      | NULL    | `git branch --show-current`                                       | `main`                         | Current git branch                  |
| `git_commit` | TEXT | YES      | NULL    | `git rev-parse --short HEAD`                                      | `a1b2c3d`                      | Current commit SHA (short, 7 chars) |

### Custom Command Tracking

| Column                | Type | Nullable | Default | Source                                  | Example                               | Description                                |
| --------------------- | ---- | -------- | ------- | --------------------------------------- | ------------------------------------- | ------------------------------------------ |
| `custom_cmd_name`     | TEXT | YES      | NULL    | Slash command file path                 | `.opencode/command/project_status.md` | Full path to the custom slash command file |
| `custom_cmd_run_date` | TEXT | YES      | NULL    | Generated at command start (ISO format) | `2025-12-25T14:30:00`                 | Timestamp when the command started         |

### Memory Content

| Column        | Type     | Nullable | Default        | Source         | Example                           | Description                                                                                                           |
| ------------- | -------- | -------- | -------------- | -------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| `type`        | TEXT     | NO       | -              | Agent decision | `learning`                        | Memory type: `action`, `observation`, `thought`, `decision`, `error`, `learning`, `project_status`, `command_summary` |
| `content`     | TEXT     | NO       | -              | Agent          | `User prefers concise responses.` | The memory content                                                                                                    |
| `content_tsv` | TSVECTOR | NO       | Auto-generated | PostgreSQL     | -                                 | Full-text search vector (`simple` language config)                                                                    |
| `importance`  | INTEGER  | YES      | `0`            | Agent or user  | `6`                               | 0-7 semantic scale (0=unrated, 1=avoid, 7=perfect)                                                                    |
| `tags`        | JSONB    | YES      | NULL           | Agent          | `["coding", "git"]`               | Array of tags (must be JSON array or NULL)                                                                            |
| `metadata`    | JSONB    | YES      | NULL           | Agent          | `{"file": "main.py"}`             | Additional context (must be JSON object or NULL)                                                                      |

### Token Usage

| Column               | Type    | Nullable | Default | Source                                        | Example | Description                        |
| -------------------- | ------- | -------- | ------- | --------------------------------------------- | ------- | ---------------------------------- |
| `tokens_input`       | INTEGER | YES      | NULL    | OpenCode `AssistantMessage.tokens.input`      | `1500`  | Input tokens used in LLM call      |
| `tokens_output`      | INTEGER | YES      | NULL    | OpenCode `AssistantMessage.tokens.output`     | `250`   | Output tokens generated            |
| `tokens_reasoning`   | INTEGER | YES      | NULL    | OpenCode `AssistantMessage.tokens.reasoning`  | `1200`  | Extended thinking/reasoning tokens |
| `tokens_cache_read`  | INTEGER | YES      | NULL    | OpenCode `AssistantMessage.tokens.cacheRead`  | `500`   | Tokens read from provider cache    |
| `tokens_cache_write` | INTEGER | YES      | NULL    | OpenCode `AssistantMessage.tokens.cacheWrite` | `100`   | Tokens written to provider cache   |

### Cost and Timing

| Column             | Type          | Nullable | Default | Source                             | Example                  | Description                                                                   |
| ------------------ | ------------- | -------- | ------- | ---------------------------------- | ------------------------ | ----------------------------------------------------------------------------- |
| `cost`             | NUMERIC(15,8) | YES      | NULL    | OpenCode `AssistantMessage.cost`   | `0.00234000`             | Cost in dollars (supports micro-costs)                                        |
| `started_at`       | TIMESTAMPTZ   | YES      | NULL    | OpenCode (epoch ms converted)      | `2025-12-25 14:30:00-05` | When the LLM call started                                                     |
| `completed_at`     | TIMESTAMPTZ   | YES      | NULL    | OpenCode (epoch ms converted)      | `2025-12-25 14:30:05-05` | When the LLM call completed                                                   |
| `response_time_ms` | INTEGER       | YES      | NULL    | Calculated or OpenCode             | `3200`                   | Response time in milliseconds                                                 |
| `finish_reason`    | TEXT          | YES      | NULL    | OpenCode `AssistantMessage.finish` | `stop`                   | How response ended: `stop`, `length`, `tool_calls`, `content_filter`, `error` |

---

## Table: `sources`

Stores external sources — documentation, blog posts, podcasts, books, Obsidian notes.

### Core Fields

| Column        | Type     | Nullable | Default        | Source         | Example                                | Description                                                                           |
| ------------- | -------- | -------- | -------------- | -------------- | -------------------------------------- | ------------------------------------------------------------------------------------- |
| `id`          | UUID     | NO       | `uuidv7()`     | Auto-generated | `019400a0-1234-7abc-8def-0123456789ab` | Primary key (time-ordered UUIDv7)                                                     |
| `user_id`     | TEXT     | NO       | -              | User config    | `pascalandy`                           | User identifier                                                                       |
| `name`        | TEXT     | NO       | -              | User/Agent     | `Nuxt`                                 | Source name (project, podcast, blog)                                                  |
| `title`       | TEXT     | YES      | NULL           | User/Agent     | `Getting Started`                      | Specific piece title (page, episode, article)                                         |
| `source_type` | TEXT     | NO       | -              | User/Agent     | `documentation`                        | Type: `documentation`, `podcast`, `blog_post`, `video`, `book`, `obsidian_note`, etc. |
| `version`     | TEXT     | YES      | NULL           | User/Agent     | `4.0.0`                                | Version (NULL if unversioned)                                                         |
| `source_url`  | TEXT     | YES      | NULL           | User/Agent     | `https://nuxt.com/docs`                | URL where content was obtained                                                        |
| `content`     | TEXT     | NO       | -              | User/Agent     | `Full documentation...`                | The actual content                                                                    |
| `content_tsv` | TSVECTOR | NO       | Auto-generated | PostgreSQL     | -                                      | Full-text search vector on `name` + `title` + `content`                               |
| `author`      | TEXT     | YES      | NULL           | User/Agent     | `Dan Abramov`                          | Who created the content                                                               |

### Timestamps

| Column          | Type        | Nullable | Default | Source                 | Example                  | Description                                  |
| --------------- | ----------- | -------- | ------- | ---------------------- | ------------------------ | -------------------------------------------- |
| `published_at`  | TIMESTAMPTZ | YES      | NULL    | User/Agent             | `2025-12-20 00:00:00-05` | When original was published                  |
| `ingested_at`   | TIMESTAMPTZ | NO       | `NOW()` | Auto-generated         | `2025-12-25 14:30:00-05` | When added to database                       |
| `updated_at`    | TIMESTAMPTZ | NO       | `NOW()` | Auto-updated (trigger) | `2025-12-25 14:30:00-05` | Last modification time                       |
| `superseded_at` | TIMESTAMPTZ | YES      | NULL    | Manual                 | `2025-12-26 10:00:00-05` | NULL = current version, timestamp = replaced |
| `deleted_at`    | TIMESTAMPTZ | YES      | NULL    | Manual                 | `2025-12-26 10:00:00-05` | Soft delete timestamp                        |

### LLM Context

Same as `memories` table: `provider_id`, `model_id`, `mode`

For manual ingestion (no LLM): `provider_id = 'manual'`, `model_id = 'none'`

### Session Tracking

Same as `memories` table: `session_id`, `parent_session_id`

### Git Context

Same as `memories` table: `repo_name`, `repo_path`, `git_branch`, `git_commit`

### Custom Command Tracking

Same as `memories` table: `custom_cmd_name`, `custom_cmd_run_date`

### Token Usage

Same as `memories` table: `tokens_input`, `tokens_output`, `tokens_reasoning`, `tokens_cache_read`, `tokens_cache_write`

### Cost and Timing

Same as `memories` table: `cost`, `started_at`, `completed_at`, `response_time_ms`, `finish_reason`

### Metadata

| Column     | Type  | Nullable | Default | Source     | Example                  | Description                                   |
| ---------- | ----- | -------- | ------- | ---------- | ------------------------ | --------------------------------------------- |
| `tags`     | JSONB | YES      | NULL    | User/Agent | `["framework", "vue"]`   | Array of tags                                 |
| `metadata` | JSONB | YES      | NULL    | User/Agent | `{"vault": "dev-notes"}` | Additional context (frontmatter for Obsidian) |

---

## Importance Scale (0-7)

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

---

## Memory Types (Convention)

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

No constraint enforced — add new types by using them.

---

## Source Types (Convention)

| Type            | Description                    |
| --------------- | ------------------------------ |
| `documentation` | Official project docs          |
| `blog_post`     | Blog articles                  |
| `podcast`       | Podcast episode transcripts    |
| `video`         | YouTube/video transcripts      |
| `book`          | Book content/chapters          |
| `audiobook`     | Audiobook transcripts          |
| `article`       | General web articles           |
| `coding`        | Code examples, repos, snippets |
| `obsidian_note` | Notes from Obsidian vault      |

No constraint enforced — add new types by using them.

---

## Constraints

### Format Constraints

| Column        | Pattern          | Description                                          |
| ------------- | ---------------- | ---------------------------------------------------- |
| `user_id`     | `^[a-z0-9_-]+$`  | Lowercase alphanumeric with underscores/hyphens      |
| `provider_id` | `^[a-z0-9_-]+$`  | Lowercase alphanumeric with underscores/hyphens      |
| `model_id`    | `^[a-z0-9._-]+$` | Lowercase alphanumeric with dots/underscores/hyphens |

### Value Constraints

| Column       | Constraint                          | Description                 |
| ------------ | ----------------------------------- | --------------------------- |
| `importance` | `BETWEEN 0 AND 7`                   | Valid range 0-7             |
| `tags`       | `jsonb_typeof(tags) = 'array'`      | Must be JSON array or NULL  |
| `metadata`   | `jsonb_typeof(metadata) = 'object'` | Must be JSON object or NULL |

---

## Epoch Conversion

OpenCode returns timestamps as Unix epoch in milliseconds. Convert to `TIMESTAMPTZ`:

```sql
to_timestamp(epoch_ms / 1000.0) AT TIME ZONE 'UTC'
```
