# pg-memory Human Guide

## Goal

This guide helps you (the human) set up, maintain, and analyze your AI agent's memory system. Use it to:

1. **Install** — Get PostgreSQL running with the memory schema
2. **Analyze** — Track costs, compare models, understand usage patterns
3. **Maintain** — Backup, cleanup, monitor health
4. **Troubleshoot** — Fix common issues

For schema details, see [SPEC.md](./SPEC.md). For SQL query patterns, see [PLAYBOOK.md](./PLAYBOOK.md).

## Important: Multi-User

All queries should include `user_id`. Replace `'pascalandy'` with your user ID.

```sql
WHERE user_id = 'pascalandy' AND deleted_at IS NULL
```

---

## Setup

### Prerequisites

| Requirement | Version    | Check Command    |
| ----------- | ---------- | ---------------- |
| macOS       | Any recent | `sw_vers`        |
| Homebrew    | Any        | `brew --version` |
| PostgreSQL  | 18+        | `psql --version` |

**Why PostgreSQL 18?** Native `uuidv7()` support (time-ordered UUIDs) without extensions.

### Installation

#### 1. Install and start PostgreSQL

```bash
brew install postgresql@18
brew services start postgresql@18
```

Verify it's running:

```bash
pg_isready
# Expected: /tmp:5432 - accepting connections
```

#### 2. Create the database

```bash
createdb forzr
```

Verify:

```bash
psql -l | rg forzr
# Should show: forzr | <username> | UTF8 | ...
```

#### 3. Run the schema

From the pg-memory directory:

```bash
psql -v ON_ERROR_STOP=1 forzr < schema/memory.sql
```

The `-v ON_ERROR_STOP=1` flag ensures psql stops on first error.

#### 4. Create config file

```bash
mkdir -p ~/.config/forzr

cat > ~/.config/forzr/db.conf << 'EOF'
[database]
host=localhost
port=5432
dbname=forzr
user=YOUR_MACOS_USERNAME
EOF

chmod 600 ~/.config/forzr/db.conf
```

Replace `YOUR_MACOS_USERNAME` with your actual username (run `whoami` to check).

#### 5. Verify installation

```bash
./scripts/verify_pg_memory.sh
```

Or manually:

```bash
# Check tables exist
psql forzr -c "\dt"

# Check indexes exist
psql forzr -c "\di"

# Test insert
psql forzr -c "INSERT INTO memories (user_id, provider_id, model_id, type, content) VALUES ('pascalandy', 'anthropic', 'claude-sonnet-4', 'test', 'Verification test') RETURNING id;"

# Cleanup test
psql forzr -c "DELETE FROM memories WHERE type = 'test';"
```

---

## Analytics

### Cost Tracking

**Total cost by provider:**

```sql
SELECT
  provider_id,
  COUNT(*) as memories,
  SUM(tokens_input) as total_input_tokens,
  SUM(tokens_output) as total_output_tokens,
  SUM(cost) as total_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND deleted_at IS NULL
  AND cost IS NOT NULL
GROUP BY provider_id
ORDER BY total_cost DESC;
```

**Cost by provider and model:**

```sql
SELECT
  provider_id,
  model_id,
  COUNT(*) as memories,
  SUM(cost) as total_cost,
  ROUND(AVG(cost)::numeric, 8) as avg_cost_per_memory
FROM memories
WHERE user_id = 'pascalandy'
  AND deleted_at IS NULL
  AND cost IS NOT NULL
GROUP BY provider_id, model_id
ORDER BY total_cost DESC;
```

**Daily spending (last 30 days):**

```sql
SELECT
  created_at::date as day,
  COUNT(*) as memories,
  SUM(tokens_input + COALESCE(tokens_output, 0)) as total_tokens,
  SUM(cost) as daily_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND created_at > NOW() - INTERVAL '30 days'
  AND deleted_at IS NULL
  AND cost IS NOT NULL
GROUP BY day
ORDER BY day DESC;
```

**Weekly spending by provider:**

```sql
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

**Most expensive operations:**

```sql
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
```

**Cost by memory type:**

```sql
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

### Token Usage

**Usage by model:**

```sql
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
```

**Cache efficiency:**

```sql
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

### Response Time Analysis

**Average response time by model:**

```sql
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
```

**Slowest operations:**

```sql
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

### Model Comparison

**Memory count by model:**

```sql
SELECT provider_id, model_id, COUNT(*) as count
FROM memories
WHERE deleted_at IS NULL
GROUP BY provider_id, model_id
ORDER BY count DESC;
```

**Learnings by model:**

```sql
SELECT provider_id, model_id, COUNT(*) as learnings
FROM memories
WHERE type = 'learning'
  AND deleted_at IS NULL
GROUP BY provider_id, model_id
ORDER BY learnings DESC;
```

**Average importance by model:**

```sql
SELECT
  provider_id,
  model_id,
  ROUND(AVG(importance), 2) as avg_importance,
  COUNT(*) as memories
FROM memories
WHERE deleted_at IS NULL
GROUP BY provider_id, model_id
ORDER BY avg_importance DESC;
```

### Session Analysis

**Cost per session:**

```sql
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
```

**Sub-agent (Task tool) costs:**

```sql
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

### Command Analytics

Track slash command performance over time.

**All commands and their stats:**

```sql
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
```

**Recent runs of a specific command:**

```sql
SELECT
  custom_cmd_run_date,
  created_at,
  ROUND(response_time_ms / 60000.0, 1) as minutes,
  cost,
  content
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name = '.opencode/command/project_status.md'
  AND type = 'command_summary'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 10;
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
  AND type = 'command_summary'
  AND created_at > NOW() - INTERVAL '14 days'
  AND deleted_at IS NULL
GROUP BY period;
```

**Daily command frequency:**

```sql
SELECT
  created_at::date as day,
  custom_cmd_name,
  COUNT(*) as runs,
  ROUND(SUM(response_time_ms) / 60000.0, 1) as total_minutes,
  ROUND(SUM(cost)::numeric, 4) as total_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name IS NOT NULL
  AND type = 'command_summary'
  AND created_at > NOW() - INTERVAL '30 days'
  AND deleted_at IS NULL
GROUP BY day, custom_cmd_name
ORDER BY day DESC, runs DESC;
```

### Repository Analytics

Track work across different repositories.

**Memories by repository:**

```sql
SELECT
  repo_name,
  COUNT(*) as memories,
  COUNT(DISTINCT git_branch) as branches,
  ROUND(SUM(cost)::numeric, 4) as total_cost
FROM memories
WHERE repo_name IS NOT NULL
  AND deleted_at IS NULL
GROUP BY repo_name
ORDER BY memories DESC;
```

**Recent work in a repository:**

```sql
SELECT
  type, git_branch, git_commit,
  LEFT(content, 80) as content_preview,
  created_at
FROM memories
WHERE repo_name = 'forzr'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 20;
```

**Work by branch:**

```sql
SELECT
  repo_name,
  git_branch,
  COUNT(*) as memories,
  MIN(created_at) as first_memory,
  MAX(created_at) as last_memory
FROM memories
WHERE repo_name IS NOT NULL
  AND git_branch IS NOT NULL
  AND deleted_at IS NULL
GROUP BY repo_name, git_branch
ORDER BY last_memory DESC;
```

### Source Ingestion Costs

**Cost by source type:**

```sql
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
```

**Most expensive sources:**

```sql
SELECT
  name, title, source_type,
  tokens_input, cost
FROM sources
WHERE deleted_at IS NULL
  AND cost IS NOT NULL
ORDER BY cost DESC
LIMIT 10;
```

### General Statistics

**Memory count by type:**

```sql
SELECT type, COUNT(*) as count
FROM memories
WHERE deleted_at IS NULL
GROUP BY type
ORDER BY count DESC;
```

**Daily memory count (last 30 days):**

```sql
SELECT created_at::date as day, COUNT(*) as count
FROM memories
WHERE deleted_at IS NULL
GROUP BY day
ORDER BY day DESC
LIMIT 30;
```

**All unique tags:**

```sql
SELECT DISTINCT jsonb_array_elements_text(tags) as tag
FROM memories
WHERE tags IS NOT NULL AND deleted_at IS NULL
ORDER BY tag;
```

**Memory count per tag:**

```sql
SELECT jsonb_array_elements_text(tags) as tag, COUNT(*) as count
FROM memories
WHERE tags IS NOT NULL AND deleted_at IS NULL
GROUP BY tag
ORDER BY count DESC;
```

---

## Maintenance

### Backup

**Plain SQL backup:**

```bash
pg_dump forzr > backup_$(date +%Y%m%d).sql
```

**Compressed backup (recommended):**

```bash
pg_dump -Fc forzr > backup_$(date +%Y%m%d).dump
```

**Verify backup contents:**

```bash
pg_restore --list backup_20251225.dump | head -20
```

### Restore

**From plain SQL:**

```bash
psql -v ON_ERROR_STOP=1 forzr < backup_20251225.sql
```

**From compressed backup:**

```bash
pg_restore -d forzr backup_20251225.dump
```

### Cleanup

**View soft-deleted records:**

```sql
SELECT id, type, LEFT(content, 50), deleted_at
FROM memories
WHERE deleted_at IS NOT NULL
ORDER BY deleted_at DESC;
```

**Permanently delete old soft-deleted records (90+ days):**

```sql
DELETE FROM memories WHERE deleted_at < NOW() - INTERVAL '90 days';
DELETE FROM sources WHERE deleted_at < NOW() - INTERVAL '90 days';
```

**Vacuum and analyze (reclaim space, update statistics):**

```bash
vacuumdb --analyze forzr
```

### Reset Database (DESTRUCTIVE)

**Drop and recreate tables:**

```bash
psql -v ON_ERROR_STOP=1 forzr -c "DROP TABLE IF EXISTS memories CASCADE; DROP TABLE IF EXISTS sources CASCADE;"
psql -v ON_ERROR_STOP=1 forzr < schema/memory.sql
```

This is the current migration strategy. For schema changes, reset and re-apply.

### Monitoring

**Table sizes:**

```bash
psql forzr -c "
SELECT
  relname as table,
  pg_size_pretty(pg_total_relation_size(relid)) as size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
"
```

**Row counts (active vs deleted):**

```bash
psql forzr -c "
SELECT 'memories' as table, COUNT(*) as total, COUNT(*) FILTER (WHERE deleted_at IS NULL) as active FROM memories
UNION ALL
SELECT 'sources', COUNT(*), COUNT(*) FILTER (WHERE deleted_at IS NULL) FROM sources;
"
```

**Index usage:**

```sql
SELECT
  indexrelname as index_name,
  idx_scan as times_used,
  idx_tup_read as rows_read
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;
```

**Table statistics:**

```sql
SELECT
  relname as table_name,
  n_tup_ins as inserts,
  n_tup_upd as updates,
  n_tup_del as deletes,
  n_live_tup as live_rows
FROM pg_stat_user_tables;
```

---

## Troubleshooting

### PostgreSQL not running

```bash
# Check status
brew services list | rg postgresql

# Start it
brew services start postgresql@18

# Verify
pg_isready
```

### Connection issues

```bash
# Test basic connection
psql postgres -c "SELECT 1;"

# Check what's on port 5432
lsof -i :5432

# Check PostgreSQL logs
tail -50 /opt/homebrew/var/log/postgresql@18.log
```

### Database doesn't exist

```bash
# List databases
psql -l

# Create it
createdb forzr
```

### Permission denied

```bash
# Check current user
whoami

# Verify database owner
psql -c "SELECT current_user;"

# Check database ownership
psql -c "SELECT datname, datdba::regrole FROM pg_database WHERE datname = 'forzr';"
```

### Schema errors

```bash
# Check PostgreSQL version (must be 18+)
psql --version

# Verify uuidv7() works
psql postgres -c "SELECT uuidv7();"

# View recent logs
tail -50 /opt/homebrew/var/log/postgresql@18.log
```

### Insert fails with CHECK constraint

The schema enforces:

- `provider_id` must match `^[a-z0-9_-]+$` (lowercase, alphanumeric, underscores, hyphens)
- `model_id` must match `^[a-z0-9._-]+$` (same plus dots)
- `importance` must be between 0 and 7
- `tags` must be a JSON array or NULL
- `metadata` must be a JSON object or NULL

Check your values match these patterns.

### Full-text search returns nothing

FTS uses `'simple'` language config (no stemming). Check:

```sql
-- Verify tsvector is populated
SELECT id, LEFT(content, 50), content_tsv FROM memories LIMIT 5;

-- Test query directly
SELECT plainto_tsquery('simple', 'your search terms');
```

---

## Quick Reference

### Useful psql commands

```bash
# Connect to database
psql forzr

# List tables
\dt

# List indexes
\di

# Describe table
\d memories
\d sources

# Exit
\q
```

### Common one-liners

```bash
# Count all memories
psql forzr -c "SELECT COUNT(*) FROM memories WHERE deleted_at IS NULL;"

# Total cost
psql forzr -c "SELECT SUM(cost) FROM memories WHERE deleted_at IS NULL;"

# Recent memories
psql forzr -c "SELECT type, LEFT(content, 60) FROM memories WHERE deleted_at IS NULL ORDER BY created_at DESC LIMIT 10;"

# Memory types breakdown
psql forzr -c "SELECT type, COUNT(*) FROM memories WHERE deleted_at IS NULL GROUP BY type ORDER BY count DESC;"
```

---

## Obsidian Vault Integration (WIP)

> **Status:** Work in progress. Frontmatter schema being finalized.

Obsidian notes are stored in the `sources` table with `source_type = 'obsidian_note'`.

**Query Obsidian notes:**

```sql
SELECT name, title, metadata->>'word_count' as words
FROM sources
WHERE user_id = 'pascalandy'
  AND source_type = 'obsidian_note'
  AND deleted_at IS NULL
ORDER BY ingested_at DESC
LIMIT 20;
```

**Find notes by frontmatter field:**

```sql
-- Notes with a specific project_id
SELECT name, title FROM sources
WHERE user_id = 'pascalandy'
  AND source_type = 'obsidian_note'
  AND metadata->>'project_id' = 'pg-memory'
  AND deleted_at IS NULL;

-- Notes with backlinks
SELECT name, title, (metadata->>'links_incoming_count')::int as backlinks
FROM sources
WHERE user_id = 'pascalandy'
  AND source_type = 'obsidian_note'
  AND (metadata->>'links_incoming_count')::int > 0
  AND deleted_at IS NULL
ORDER BY backlinks DESC;
```

See [SPEC.md](./SPEC.md) for full Obsidian integration details.

---

## References

- [SPEC.md](./SPEC.md) — Full schema, columns, indexes, constraints
- [PLAYBOOK.md](./PLAYBOOK.md) — Comprehensive query recipes by use case
- [PLAN.md](./PLAN.md) — Detailed setup steps and test procedures
- [GUIDE_AGENT.md](./GUIDE_AGENT.md) — SQL patterns for AI assistants
