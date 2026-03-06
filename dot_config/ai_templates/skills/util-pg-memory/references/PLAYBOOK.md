# pg-memory Query Reference

Organized by **use case** with ready-to-use SQL examples.

> **Important: Multi-User**
>
> All queries must include `user_id`. Add this filter to every query:
>
> ```sql
> WHERE user_id = 'pascalandy' AND deleted_at IS NULL
> ```
>
> Replace `'pascalandy'` with the appropriate user ID.

> **Critical: Timestamp Columns Differ**
>
> | Table      | Timestamp Column | Description              |
> | ---------- | ---------------- | ------------------------ |
> | `memories` | `created_at`     | When memory was inserted |
> | `sources`  | `ingested_at`    | When source was added    |
>
> Using `created_at` on `sources` will fail with "column does not exist".

> **Note:** All queries assume active records only (`deleted_at IS NULL`). Omit this filter to include soft-deleted records. FTS uses `'simple'` language config for mixed EN/FR content.

> **Manual Ingestion:** For non-LLM content (copy-paste, Obsidian sync), use `provider_id = 'manual'` and `model_id = 'none'`.

---

## Memories Table

### 1. Retrieve Recent Context

**Use case:** Start a new coding session and need to recall what you were working on.

```sql
-- Last 20 memories
SELECT * FROM memories
WHERE deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 20;

-- Today's memories only (uses index)
SELECT * FROM memories
WHERE created_at >= CURRENT_DATE
  AND created_at < CURRENT_DATE + INTERVAL '1 day'
  AND deleted_at IS NULL
ORDER BY created_at DESC;

-- Last 2 days
SELECT * FROM memories
WHERE created_at > NOW() - INTERVAL '2 days'
  AND deleted_at IS NULL
ORDER BY created_at DESC;

-- Last week
SELECT * FROM memories
WHERE created_at > NOW() - INTERVAL '7 days'
  AND deleted_at IS NULL
ORDER BY created_at DESC;

-- Specific date range (uses index - note: end date is exclusive)
SELECT * FROM memories
WHERE created_at >= '2025-12-20'
  AND created_at < '2025-12-26'
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

### 2. Resume a Session

**Use case:** Continue where you left off in a specific coding session.

```sql
-- All memories from a session
SELECT * FROM memories
WHERE session_id = 'ses_4a30f921fffeExOAtr8adv55fz'
  AND deleted_at IS NULL
ORDER BY created_at;
```

### 3. Filter by Provider/Model

**Use case:** See what a specific AI model learned or decided.

```sql
-- Last 20 from Claude Sonnet
SELECT * FROM memories
WHERE provider_id = 'anthropic'
  AND model_id = 'claude-sonnet-4'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 20;

-- All memories from Anthropic (any model)
SELECT * FROM memories
WHERE provider_id = 'anthropic'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 20;

-- Compare learnings across models
SELECT provider_id, model_id, COUNT(*) as count
FROM memories
WHERE type = 'learning'
  AND deleted_at IS NULL
GROUP BY provider_id, model_id
ORDER BY count DESC;
```

### 4. Review Decisions and Learnings

**Use case:** Audit past architectural decisions or recall lessons learned.

```sql
-- All decisions
SELECT * FROM memories
WHERE type = 'decision'
  AND deleted_at IS NULL
ORDER BY created_at DESC;

-- All learnings
SELECT * FROM memories
WHERE type = 'learning'
  AND deleted_at IS NULL
ORDER BY created_at DESC;

-- High-importance decisions (5+ = Good or better)
SELECT * FROM memories
WHERE user_id = 'pascalandy'
  AND importance >= 5
  AND type = 'decision'
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

### 5. Find High-Priority Items

**Use case:** Focus on the most important memories first.

```sql
-- High-importance memories (5+ = Good or better)
SELECT * FROM memories
WHERE user_id = 'pascalandy'
  AND importance >= 5
  AND deleted_at IS NULL
ORDER BY importance DESC, created_at DESC;

-- Top 10 most important from last week
SELECT * FROM memories
WHERE created_at > NOW() - INTERVAL '7 days'
  AND deleted_at IS NULL
ORDER BY importance DESC, created_at DESC
LIMIT 10;
```

### 6. Search by Topic (Tags)

**Use case:** Find all memories related to a specific technology or concept.

```sql
-- Memories tagged with "git"
SELECT * FROM memories
WHERE tags @> '["git"]'
  AND deleted_at IS NULL;

-- Memories with ANY of these tags
SELECT * FROM memories
WHERE tags ?| ARRAY['git', 'coding', 'debug']
  AND deleted_at IS NULL;

-- Memories with ALL of these tags
SELECT * FROM memories
WHERE tags @> '["git", "coding"]'
  AND deleted_at IS NULL;

-- Sort by most matching tags (relevance)
SELECT
  id, content, tags,
  (SELECT COUNT(*) FROM jsonb_array_elements_text(tags) t WHERE t = ANY(ARRAY['git', 'debug'])) as match_count
FROM memories
WHERE tags ?| ARRAY['git', 'debug']
  AND deleted_at IS NULL
ORDER BY match_count DESC, created_at DESC;
```

### 7. Full-Text Search

**Use case:** Find memories mentioning specific terms or concepts.

```sql
-- Basic keyword search
SELECT id, content, ts_rank(content_tsv, query) as rank
FROM memories, plainto_tsquery('simple', 'postgresql jsonb') query
WHERE content_tsv @@ query
  AND deleted_at IS NULL
ORDER BY rank DESC
LIMIT 10;

-- Phrase search (exact phrase)
SELECT id, content, ts_rank(content_tsv, query) as rank
FROM memories, phraseto_tsquery('simple', 'memory system') query
WHERE content_tsv @@ query
  AND deleted_at IS NULL
ORDER BY rank DESC;

-- Boolean search (AND, OR, NOT)
SELECT id, content
FROM memories
WHERE content_tsv @@ to_tsquery('simple', 'postgres & memory & !error')
  AND deleted_at IS NULL
ORDER BY created_at DESC;

-- Combined: FTS + specific tag
SELECT id, content, tags, ts_rank(content_tsv, query) as text_rank
FROM memories, plainto_tsquery('simple', 'git commit') query
WHERE content_tsv @@ query
  AND tags @> '["git"]'
  AND deleted_at IS NULL
ORDER BY text_rank DESC, created_at DESC
LIMIT 10;
```

### 8. Query Metadata

**Use case:** Find memories with specific context or attributes stored in metadata.

```sql
-- Filter by metadata field (uses GIN index via containment)
SELECT * FROM memories
WHERE metadata @> '{"source": "user_request"}'
  AND deleted_at IS NULL;

-- Check if metadata key exists (uses GIN index)
SELECT * FROM memories
WHERE metadata ? 'error_code'
  AND deleted_at IS NULL;

-- Nested metadata query (uses GIN index via containment)
SELECT * FROM memories
WHERE metadata @> '{"context": {"file": "main.py"}}'
  AND deleted_at IS NULL;
```

### 9. Get Statistics

**Use case:** Understand your memory patterns and usage.

```sql
-- Count by type
SELECT type, COUNT(*) as count
FROM memories
WHERE deleted_at IS NULL
GROUP BY type
ORDER BY count DESC;

-- Count by provider/model
SELECT provider_id, model_id, COUNT(*) as count
FROM memories
WHERE deleted_at IS NULL
GROUP BY provider_id, model_id
ORDER BY count DESC;

-- Daily memory count (last 30 days)
SELECT created_at::date as day, COUNT(*) as count
FROM memories
WHERE deleted_at IS NULL
GROUP BY day
ORDER BY day DESC
LIMIT 30;

-- Average importance by type
SELECT type, ROUND(AVG(importance), 2) as avg_importance
FROM memories
WHERE deleted_at IS NULL
GROUP BY type
ORDER BY avg_importance DESC;

-- List all unique tags
SELECT DISTINCT jsonb_array_elements_text(tags) as tag
FROM memories
WHERE tags IS NOT NULL AND deleted_at IS NULL
ORDER BY tag;

-- Count memories per tag
SELECT jsonb_array_elements_text(tags) as tag, COUNT(*) as count
FROM memories
WHERE tags IS NOT NULL AND deleted_at IS NULL
GROUP BY tag
ORDER BY count DESC;
```

### 10. Insert New Memory

**Use case:** Store a new memory from your coding session.

```sql
-- Basic insert
INSERT INTO memories (user_id, provider_id, model_id, type, content)
VALUES ('pascalandy', 'anthropic', 'claude-sonnet-4', 'observation', 'User prefers concise responses.')
RETURNING id;

-- Full insert with all fields including git context
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
  'anthropic', 'claude-opus-4', 'build',
  'ses_4a30f921fffeExOAtr8adv55fz',
  'forzr', 'Documents/github_local/forzr', 'main', 'a1b2c3d',
  'decision',
  'Chose to use PostgreSQL over SQLite for better JSONB support.',
  6,
  '["database", "architecture"]',
  '{"alternatives_considered": ["sqlite", "mysql"], "reason": "native jsonb"}',
  2500, 450, 1200,
  0.0156, 3200, 'stop'
)
RETURNING id, created_at, cost;
```

### 11. Lookup by ID

**Use case:** Retrieve a specific memory by its UUID.

```sql
SELECT * FROM memories
WHERE id = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';
```

---

## Sources Table

### 12. Find Documentation

**Use case:** Look up reference docs for a framework or library.

```sql
-- Current docs by name
SELECT * FROM sources
WHERE name = 'Nuxt'
  AND superseded_at IS NULL
  AND deleted_at IS NULL;

-- Specific version
SELECT * FROM sources
WHERE name = 'Nuxt'
  AND version = '4.0.0'
  AND superseded_at IS NULL
  AND deleted_at IS NULL;

-- All current documentation
SELECT id, name, title, version, LENGTH(content) as content_length
FROM sources
WHERE source_type = 'documentation'
  AND superseded_at IS NULL
  AND deleted_at IS NULL
ORDER BY name, version;
```

### 13. Browse Content by Type

**Use case:** Find all podcasts, blog posts, or videos you've ingested.

```sql
-- All podcast transcripts
SELECT name, title, author, published_at
FROM sources
WHERE source_type = 'podcast'
  AND deleted_at IS NULL
ORDER BY published_at DESC;

-- All video transcripts
SELECT name, title, author, published_at
FROM sources
WHERE source_type = 'video'
  AND deleted_at IS NULL
ORDER BY published_at DESC;

-- All blog posts by author
SELECT name, title, published_at, source_url
FROM sources
WHERE source_type = 'blog_post'
  AND author = 'Dan Abramov'
  AND deleted_at IS NULL
ORDER BY published_at DESC;
```

### 14. Search Source Content

**Use case:** Find sources that discuss a specific topic.

```sql
-- Search all sources
SELECT name, title, source_type, ts_rank(content_tsv, query) as rank
FROM sources, plainto_tsquery('simple', 'react hooks') query
WHERE content_tsv @@ query
  AND deleted_at IS NULL
ORDER BY rank DESC
LIMIT 20;

-- Search only documentation
SELECT name, title, ts_rank(content_tsv, query) as rank
FROM sources, plainto_tsquery('simple', 'nuxt vue ssr') query
WHERE content_tsv @@ query
  AND source_type = 'documentation'
  AND superseded_at IS NULL
  AND deleted_at IS NULL
ORDER BY rank DESC
LIMIT 10;
```

### 15. Track Recent Ingestions

**Use case:** See what content was recently added to your knowledge base.

```sql
-- Recently ingested
SELECT name, title, source_type, ingested_at
FROM sources
WHERE superseded_at IS NULL AND deleted_at IS NULL
ORDER BY ingested_at DESC
LIMIT 10;

-- Recently updated
SELECT name, title, source_type, updated_at
FROM sources
WHERE superseded_at IS NULL AND deleted_at IS NULL
ORDER BY updated_at DESC
LIMIT 10;

-- Published in last 30 days
SELECT name, title, source_type, author, published_at
FROM sources
WHERE published_at > NOW() - INTERVAL '30 days'
  AND deleted_at IS NULL
ORDER BY published_at DESC;
```

### 16. View Version History

**Use case:** See all versions of a documentation source.

```sql
SELECT id, name, title, version, ingested_at, superseded_at
FROM sources
WHERE name = 'Nuxt'
  AND deleted_at IS NULL
ORDER BY ingested_at DESC;
```

### 17. Ingest New Source

**Use case:** Add new documentation, podcast, or blog post to your knowledge base.

```sql
-- Documentation
INSERT INTO sources (
  name, title, source_type, version, source_url, content,
  provider_id, model_id, tags,
  tokens_input, tokens_output, cost
)
VALUES (
  'Nuxt',
  'Getting Started',
  'documentation',
  '4.0.0',
  'https://nuxt.com/docs/getting-started',
  'Full documentation content here...',
  'anthropic', 'claude-sonnet-4',
  '["framework", "vue", "ssr"]',
  15000, 500, 0.0234
)
RETURNING id, cost;

-- Podcast transcript
INSERT INTO sources (
  name, title, source_type, source_url, content, author, published_at,
  provider_id, model_id, tags,
  tokens_input, tokens_output, cost
)
VALUES (
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
RETURNING id, cost;

-- Blog post
INSERT INTO sources (
  name, title, source_type, source_url, content, author, published_at,
  provider_id, model_id, tags,
  tokens_input, tokens_output, cost
)
VALUES (
  'Overreacted',
  'A Complete Guide to useEffect',
  'blog_post',
  'https://overreacted.io/a-complete-guide-to-useeffect/',
  'Blog content here...',
  'Dan Abramov',
  '2019-03-09',
  'anthropic', 'claude-sonnet-4',
  '["react", "hooks"]',
  8000, 300, 0.0125
)
RETURNING id, cost;
```

### 18. Update Documentation (Upsert Pattern)

**Use case:** Replace outdated docs with a new version.

```sql
BEGIN;

-- Mark old version as superseded
UPDATE sources
SET superseded_at = NOW()
WHERE name = 'Nuxt'
  AND version = '4.0.0'
  AND superseded_at IS NULL
  AND deleted_at IS NULL;

-- Insert new version
INSERT INTO sources (
  name, title, source_type, version, source_url, content,
  provider_id, model_id, tags,
  tokens_input, tokens_output, cost
)
VALUES (
  'Nuxt',
  'Getting Started',
  'documentation',
  '4.0.0',
  'https://nuxt.com/docs/getting-started',
  'Updated documentation content...',
  'anthropic', 'claude-sonnet-4',
  '["framework", "vue", "ssr"]',
  16000, 550, 0.0248
);

COMMIT;
```

### 19. Source Statistics

**Use case:** Get an overview of your knowledge base.

```sql
-- Count by type
SELECT source_type, COUNT(*) as count
FROM sources
WHERE superseded_at IS NULL AND deleted_at IS NULL
GROUP BY source_type
ORDER BY count DESC;

-- Count by name
SELECT name, COUNT(*) as total_entries
FROM sources
WHERE deleted_at IS NULL
GROUP BY name
ORDER BY total_entries DESC;

-- Count by author
SELECT author, COUNT(*) as count
FROM sources
WHERE author IS NOT NULL AND deleted_at IS NULL
GROUP BY author
ORDER BY count DESC;

-- Current vs superseded vs deleted
SELECT
  COUNT(*) FILTER (WHERE superseded_at IS NULL AND deleted_at IS NULL) as current,
  COUNT(*) FILTER (WHERE superseded_at IS NOT NULL AND deleted_at IS NULL) as superseded,
  COUNT(*) FILTER (WHERE deleted_at IS NOT NULL) as deleted
FROM sources;

-- List all current sources
SELECT id, name, title, source_type, version, ingested_at, LENGTH(content) as content_length
FROM sources
WHERE superseded_at IS NULL AND deleted_at IS NULL
ORDER BY name, version;
```

---

## Cost and Token Analytics

### 31. Track Spending by Provider

**Use case:** See how much you're spending on each AI provider.

```sql
-- Total cost by provider
SELECT
  provider_id,
  COUNT(*) as memories,
  SUM(tokens_input) as total_input_tokens,
  SUM(tokens_output) as total_output_tokens,
  SUM(cost) as total_cost
FROM memories
WHERE deleted_at IS NULL
  AND cost IS NOT NULL
GROUP BY provider_id
ORDER BY total_cost DESC;

-- Cost by provider/model
SELECT
  provider_id,
  model_id,
  COUNT(*) as memories,
  SUM(cost) as total_cost,
  ROUND(AVG(cost)::numeric, 8) as avg_cost_per_memory
FROM memories
WHERE deleted_at IS NULL
  AND cost IS NOT NULL
GROUP BY provider_id, model_id
ORDER BY total_cost DESC;
```

### 32. Daily Cost Tracking

**Use case:** Monitor spending over time.

```sql
-- Daily cost (last 30 days)
SELECT
  created_at::date as day,
  COUNT(*) as memories,
  SUM(tokens_input + COALESCE(tokens_output, 0)) as total_tokens,
  SUM(cost) as daily_cost
FROM memories
WHERE created_at > NOW() - INTERVAL '30 days'
  AND deleted_at IS NULL
  AND cost IS NOT NULL
GROUP BY day
ORDER BY day DESC;

-- Weekly cost summary
SELECT
  date_trunc('week', created_at) as week,
  provider_id,
  COUNT(*) as memories,
  SUM(cost) as weekly_cost
FROM memories
WHERE created_at > NOW() - INTERVAL '12 weeks'
  AND deleted_at IS NULL
  AND cost IS NOT NULL
GROUP BY week, provider_id
ORDER BY week DESC, weekly_cost DESC;
```

### 33. Find Expensive Operations

**Use case:** Identify which memories/operations cost the most.

```sql
-- Top 10 most expensive memories
SELECT
  id, provider_id, model_id, type,
  LEFT(content, 100) as content_preview,
  tokens_input, tokens_output, tokens_reasoning,
  cost
FROM memories
WHERE deleted_at IS NULL
  AND cost IS NOT NULL
ORDER BY cost DESC
LIMIT 10;

-- Average cost by memory type
SELECT
  type,
  COUNT(*) as count,
  ROUND(AVG(cost)::numeric, 8) as avg_cost,
  SUM(cost) as total_cost
FROM memories
WHERE deleted_at IS NULL
  AND cost IS NOT NULL
GROUP BY type
ORDER BY total_cost DESC;
```

### 34. Token Usage Analysis

**Use case:** Understand token consumption patterns.

```sql
-- Token usage by model
SELECT
  provider_id,
  model_id,
  COUNT(*) as memories,
  SUM(tokens_input) as total_input,
  SUM(tokens_output) as total_output,
  SUM(tokens_reasoning) as total_reasoning,
  SUM(tokens_cache_read) as cache_reads,
  SUM(tokens_cache_write) as cache_writes
FROM memories
WHERE deleted_at IS NULL
GROUP BY provider_id, model_id
ORDER BY total_input DESC;

-- Cache efficiency
SELECT
  provider_id,
  model_id,
  SUM(tokens_cache_read) as cache_reads,
  SUM(tokens_input) as total_input,
  ROUND(
    100.0 * SUM(tokens_cache_read) / NULLIF(SUM(tokens_input), 0),
    2
  ) as cache_hit_percent
FROM memories
WHERE deleted_at IS NULL
  AND tokens_input > 0
GROUP BY provider_id, model_id
ORDER BY cache_hit_percent DESC;
```

### 35. Response Time Analysis

**Use case:** Identify slow operations.

```sql
-- Average response time by model
SELECT
  provider_id,
  model_id,
  COUNT(*) as memories,
  ROUND(AVG(response_time_ms)) as avg_ms,
  MIN(response_time_ms) as min_ms,
  MAX(response_time_ms) as max_ms
FROM memories
WHERE deleted_at IS NULL
  AND response_time_ms IS NOT NULL
GROUP BY provider_id, model_id
ORDER BY avg_ms DESC;

-- Slowest operations
SELECT
  id, provider_id, model_id, type,
  response_time_ms,
  tokens_input, tokens_output,
  LEFT(content, 80) as content_preview
FROM memories
WHERE deleted_at IS NULL
  AND response_time_ms IS NOT NULL
ORDER BY response_time_ms DESC
LIMIT 10;
```

### 36. Source Ingestion Costs

**Use case:** Track cost of ingesting external sources.

```sql
-- Cost by source type
SELECT
  source_type,
  COUNT(*) as sources,
  SUM(tokens_input) as total_tokens,
  SUM(cost) as total_cost
FROM sources
WHERE deleted_at IS NULL
  AND superseded_at IS NULL
  AND cost IS NOT NULL
GROUP BY source_type
ORDER BY total_cost DESC;

-- Most expensive sources
SELECT
  name, title, source_type,
  tokens_input, cost
FROM sources
WHERE deleted_at IS NULL
  AND cost IS NOT NULL
ORDER BY cost DESC
LIMIT 10;
```

### 37. Session Analysis

**Use case:** Analyze costs and patterns by session.

```sql
-- Cost per session
SELECT
  session_id,
  COUNT(*) as memories,
  SUM(tokens_input) as total_input,
  SUM(tokens_output) as total_output,
  SUM(cost) as session_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND deleted_at IS NULL
  AND session_id IS NOT NULL
  AND cost IS NOT NULL
GROUP BY session_id
ORDER BY session_cost DESC
LIMIT 20;

-- Sub-agent (Task tool) analysis
SELECT
  parent_session_id,
  COUNT(*) as sub_agent_memories,
  SUM(cost) as sub_agent_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND deleted_at IS NULL
  AND parent_session_id IS NOT NULL
  AND cost IS NOT NULL
GROUP BY parent_session_id
ORDER BY sub_agent_cost DESC;
```

---

## Git Context and Repository Analytics

### 38. Filter by Repository

**Use case:** Find all memories from a specific project.

```sql
-- All memories from a repository
SELECT id, type, content, git_branch, git_commit, created_at
FROM memories
WHERE repo_name = 'forzr'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 20;

-- Memories from a specific branch
SELECT id, type, content, git_commit
FROM memories
WHERE repo_name = 'nuxt_blog'
  AND git_branch = 'feature/dark-mode'
  AND deleted_at IS NULL
ORDER BY created_at DESC;

-- What was I working on at this commit?
SELECT id, type, content, importance
FROM memories
WHERE git_commit = 'a1b2c3d'
  AND deleted_at IS NULL
ORDER BY created_at;
```

### 39. Repository Statistics

**Use case:** Understand work distribution across projects.

```sql
-- Memories per repository
SELECT
  repo_name,
  COUNT(*) as memories,
  COUNT(DISTINCT git_branch) as branches_touched,
  MIN(created_at) as first_memory,
  MAX(created_at) as last_memory
FROM memories
WHERE repo_name IS NOT NULL
  AND deleted_at IS NULL
GROUP BY repo_name
ORDER BY memories DESC;

-- Cost per repository
SELECT
  repo_name,
  COUNT(*) as memories,
  ROUND(SUM(cost)::numeric, 4) as total_cost
FROM memories
WHERE repo_name IS NOT NULL
  AND cost IS NOT NULL
  AND deleted_at IS NULL
GROUP BY repo_name
ORDER BY total_cost DESC;

-- Work by branch across all repos
SELECT
  repo_name,
  git_branch,
  COUNT(*) as memories,
  MAX(created_at) as last_activity
FROM memories
WHERE repo_name IS NOT NULL
  AND git_branch IS NOT NULL
  AND deleted_at IS NULL
GROUP BY repo_name, git_branch
ORDER BY last_activity DESC
LIMIT 20;
```

---

## Command Tracking

### 40. Slash Command Analytics

**Use case:** Track performance of custom commands like `/project-status`.

```sql
-- All command runs with stats
SELECT
  custom_cmd_name,
  COUNT(*) as runs,
  ROUND(AVG(response_time_ms) / 60000.0, 1) as avg_minutes,
  ROUND(MIN(response_time_ms) / 60000.0, 1) as min_minutes,
  ROUND(MAX(response_time_ms) / 60000.0, 1) as max_minutes,
  ROUND(SUM(cost)::numeric, 4) as total_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name IS NOT NULL
  AND type = 'command_summary'
  AND deleted_at IS NULL
GROUP BY custom_cmd_name
ORDER BY runs DESC;

-- Recent runs of a specific command
SELECT
  custom_cmd_run_date,
  created_at,
  ROUND(response_time_ms / 60000.0, 1) as minutes,
  cost,
  LEFT(content, 80) as summary
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name = '.opencode/command/project_status.md'
  AND type = 'command_summary'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 10;
```

### 41. Command Performance Comparison

**Use case:** Compare command performance over time.

```sql
-- This week vs last week
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
  AND type = 'command_summary'
  AND created_at > NOW() - INTERVAL '14 days'
  AND deleted_at IS NULL
GROUP BY period;

-- Daily trend for a command
SELECT
  created_at::date as day,
  COUNT(*) as runs,
  ROUND(AVG(response_time_ms) / 60000.0, 1) as avg_minutes,
  ROUND(SUM(cost)::numeric, 4) as daily_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name = '.opencode/command/project_status.md'
  AND type = 'command_summary'
  AND created_at > NOW() - INTERVAL '30 days'
  AND deleted_at IS NULL
GROUP BY day
ORDER BY day DESC;
```

### 42. Insert Command Summary

**Use case:** Record a slash command execution summary.

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

---

## Data Management

### 20. Soft Delete and Restore

**Use case:** Remove records without permanent deletion (recoverable).

```sql
-- Soft delete a memory
UPDATE memories SET deleted_at = NOW() WHERE id = 'uuid-here';

-- Soft delete a source
UPDATE sources SET deleted_at = NOW() WHERE id = 'uuid-here';

-- Restore a soft-deleted record
UPDATE memories SET deleted_at = NULL WHERE id = 'uuid-here';

-- View deleted records
SELECT * FROM memories WHERE deleted_at IS NOT NULL ORDER BY deleted_at DESC;
SELECT * FROM sources WHERE deleted_at IS NOT NULL ORDER BY deleted_at DESC;
```

### 21. Permanent Cleanup

**Use case:** Purge old soft-deleted records to reclaim space.

```sql
-- Delete records soft-deleted more than 90 days ago
DELETE FROM memories WHERE deleted_at < NOW() - INTERVAL '90 days';
DELETE FROM sources WHERE deleted_at < NOW() - INTERVAL '90 days';
```

---

## Database Maintenance

### 22. Monitor Performance

**Use case:** Check table sizes and index usage.

```sql
-- Table statistics
SELECT
  relname as table_name,
  n_tup_ins as inserts,
  n_tup_upd as updates,
  n_tup_del as deletes,
  n_live_tup as live_rows
FROM pg_stat_user_tables;

-- Index usage
SELECT
  indexrelname as index_name,
  idx_scan as times_used,
  idx_tup_read as rows_read
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

---

## Suggested Additional Use Cases

Based on your workflow (Python/TypeScript/Bash development, Obsidian notes, blog, AI coding CLIs), here are use cases not yet covered:

### 23. Track Errors and Debug Sessions

**Use case:** Log errors encountered during development for future reference.

```sql
-- Insert an error memory
INSERT INTO memories (provider_id, model_id, session_id, type, content, importance, tags, metadata)
VALUES (
  'anthropic', 'claude-sonnet-4',
  'ses_4a30f921fffeExOAtr8adv55fz',
  'error',
  'TypeError: Cannot read property "map" of undefined in BlogList component',
  7,
  '["typescript", "nuxt", "bug"]',
  '{"file": "components/BlogList.vue", "line": 42, "resolved": false}'
)
RETURNING id;

-- Find unresolved errors (uses GIN index via containment)
SELECT * FROM memories
WHERE type = 'error'
  AND metadata @> '{"resolved": false}'
  AND deleted_at IS NULL
ORDER BY created_at DESC;

-- Find errors by exact file (uses GIN index via containment)
SELECT * FROM memories
WHERE type = 'error'
  AND metadata @> '{"file": "components/BlogList.vue"}'
  AND deleted_at IS NULL;
```

### 24. Track Project Status Snapshots

**Use case:** Record periodic status updates for your projects.

```sql
-- Insert project status
INSERT INTO memories (provider_id, model_id, type, content, importance, tags, metadata)
VALUES (
  'anthropic', 'claude-sonnet-4',
  'project_status',
  'Nuxt blog: implemented dark mode, fixed RSS feed, pending: i18n support',
  6,
  '["nuxt", "blog", "status"]',
  '{"project": "nuxt_blog", "completed": ["dark-mode", "rss"], "pending": ["i18n"]}'
)
RETURNING id;

-- Get latest status per project
SELECT DISTINCT ON (metadata->>'project')
  id, content, created_at, metadata->>'project' as project
FROM memories
WHERE type = 'project_status'
  AND deleted_at IS NULL
ORDER BY metadata->>'project', created_at DESC;
```

### 25. Link Memories to Files

**Use case:** Associate memories with specific files in your codebase.

```sql
-- Insert memory linked to a file
INSERT INTO memories (provider_id, model_id, type, content, tags, metadata)
VALUES (
  'anthropic', 'claude-sonnet-4',
  'observation',
  'The useAsyncData composable needs error handling for network failures',
  '["nuxt", "composables"]',
  '{"file": "composables/useBlogPosts.ts", "line_range": "15-30"}'
)
RETURNING id;

-- Find all memories for a specific file (uses GIN index via containment)
SELECT * FROM memories
WHERE metadata @> '{"file": "composables/useBlogPosts.ts"}'
  AND deleted_at IS NULL
ORDER BY created_at DESC;

-- Find memories for files in a directory (LIKE requires extraction - no index)
-- For frequent queries, consider adding a separate indexed column
SELECT * FROM memories
WHERE metadata->>'file' LIKE 'composables/%'
  AND deleted_at IS NULL
ORDER BY created_at DESC;
```

### 26. Obsidian Notes Integration

**Use case:** Store Obsidian notes as sources for searchable reference.

```sql
-- Insert Obsidian note
INSERT INTO sources (name, title, source_type, content, provider_id, model_id, tags, metadata)
VALUES (
  'Obsidian',
  'PostgreSQL JSONB Patterns',
  'note',
  'Content of the note...',
  'anthropic', 'claude-sonnet-4',
  '["postgres", "jsonb", "patterns"]',
  '{"vault": "dev-notes", "path": "databases/postgresql-jsonb.md"}'
)
RETURNING id;

-- Search across Obsidian notes
SELECT name, title, ts_rank(content_tsv, query) as rank
FROM sources, plainto_tsquery('simple', 'jsonb array') query
WHERE content_tsv @@ query
  AND source_type = 'note'
  AND deleted_at IS NULL
ORDER BY rank DESC;

-- Find notes by exact vault path (uses GIN index via containment)
SELECT * FROM sources
WHERE source_type = 'note'
  AND metadata @> '{"path": "databases/postgresql-jsonb.md"}'
  AND deleted_at IS NULL;

-- Find notes by vault path prefix (LIKE requires extraction - no index)
SELECT * FROM sources
WHERE source_type = 'note'
  AND metadata->>'path' LIKE 'databases/%'
  AND deleted_at IS NULL;
```

### 27. Track Code Snippets and Patterns

**Use case:** Store reusable code patterns for quick reference.

```sql
-- Insert code snippet
INSERT INTO sources (name, title, source_type, content, provider_id, model_id, tags, metadata)
VALUES (
  'Snippets',
  'PostgreSQL Upsert Pattern',
  'coding',
  'BEGIN; UPDATE ... SET superseded_at = NOW() WHERE ...; INSERT INTO ...; COMMIT;',
  'anthropic', 'claude-sonnet-4',
  '["postgres", "upsert", "pattern"]',
  '{"language": "sql", "category": "database"}'
)
RETURNING id;

-- Find snippets by language (uses GIN index via containment)
SELECT title, content, tags
FROM sources
WHERE source_type = 'coding'
  AND metadata @> '{"language": "python"}'
  AND deleted_at IS NULL;

-- Search snippets
SELECT title, content, ts_rank(content_tsv, query) as rank
FROM sources, plainto_tsquery('simple', 'async await') query
WHERE content_tsv @@ query
  AND source_type = 'coding'
  AND deleted_at IS NULL
ORDER BY rank DESC;
```

### 28. Cross-Table Search

**Use case:** Search both memories and sources for a topic.

```sql
-- Search everything for "nuxt"
(
  SELECT 'memory' as source_table, id, content as text, created_at as date,
         ts_rank(content_tsv, query) as rank
  FROM memories, plainto_tsquery('simple', 'nuxt') query
  WHERE content_tsv @@ query AND deleted_at IS NULL
)
UNION ALL
(
  SELECT 'source' as source_table, id, title || ': ' || LEFT(content, 200) as text,
         ingested_at as date, ts_rank(content_tsv, query) as rank
  FROM sources, plainto_tsquery('simple', 'nuxt') query
  WHERE content_tsv @@ query AND deleted_at IS NULL
)
ORDER BY rank DESC
LIMIT 20;
```

### 29. Track CLI Tool Preferences

**Use case:** Remember which CLI tools and flags you prefer.

```sql
-- Insert tool preference
INSERT INTO memories (provider_id, model_id, type, content, importance, tags, metadata)
VALUES (
  'anthropic', 'claude-sonnet-4',
  'learning',
  'User prefers rg over grep, fd over find, uv over pip, bun over npm',
  9,
  '["cli", "preferences", "tools"]',
  '{"tools": {"search": "rg", "find": "fd", "python": "uv", "js": "bun"}}'
)
RETURNING id;

-- Find tool preferences
SELECT * FROM memories
WHERE type = 'learning'
  AND tags @> '["cli", "preferences"]'
  AND deleted_at IS NULL
ORDER BY importance DESC;
```

### 30. Session Summary

**Use case:** Generate a summary of what happened in a coding session.

```sql
-- Get session overview
SELECT
  type,
  COUNT(*) as count,
  ROUND(AVG(importance), 1) as avg_importance
FROM memories
WHERE session_id = 'ses_4a30f921fffeExOAtr8adv55fz'
  AND deleted_at IS NULL
GROUP BY type
ORDER BY count DESC;

-- Get high-importance items from session
SELECT type, content, importance
FROM memories
WHERE session_id = 'ses_4a30f921fffeExOAtr8adv55fz'
  AND importance >= 7
  AND deleted_at IS NULL
ORDER BY importance DESC, created_at;
```
