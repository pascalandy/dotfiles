# pg-memory Implementation Plan

version: `solution_design_v1-0`

## Prerequisites

- macOS with Homebrew installed
- PostgreSQL 18 installed (`brew install postgresql@18`)
- Terminal access

## Out of Scope

The following are explicitly **not** part of this implementation:

| Feature                          | Reason                                                                      |
| -------------------------------- | --------------------------------------------------------------------------- |
| **Vector embeddings (pgvector)** | Semantic search not required; FTS is sufficient for keyword-based retrieval |
| **Schema migrations**            | Initial implementation; use reset pattern for now                           |
| **Connection pooling**           | Single-agent CLI access only                                                |
| **Password authentication**      | Local socket auth via Homebrew PostgreSQL                                   |
| **Multi-language FTS**           | Using `'simple'` config for mixed EN/FR content                             |

## Step 1: Start PostgreSQL

```bash
brew services start postgresql@18
```

Verify it's running:

```bash
pg_isready
# Expected: /tmp:5432 - accepting connections
```

Check version:

```bash
psql --version
# Expected: psql (PostgreSQL) 18.x
```

## Step 2: Create Database

```bash
createdb forzr
```

Verify:

```bash
psql -l | rg forzr
# Should show: forzr | <username> | UTF8 | ...
```

## Step 3: Verify uuidv7() Support

```bash
psql postgres -c "SELECT uuidv7();"
```

Expected: a UUID like `019400a0-1234-7abc-8def-0123456789ab`

**Note:** `uuidv7()` is native to PostgreSQL 18 — no extension required. UUIDv7 is time-ordered, which provides better B-tree index locality than random UUIDs.

## Step 4: Create Config Directory

```bash
mkdir -p ~/.config/forzr
```

Create config file:

```bash
cat > ~/.config/forzr/db.conf << 'EOF'
[database]
host=localhost
port=5432
dbname=forzr
user=andy16
EOF
```

_Replace `andy16` with your macOS username._

**Secure the config file:**

```bash
chmod 600 ~/.config/forzr/db.conf
```

## Step 5: Set Environment Variable (Optional)

The config file is the primary connection method. Environment variable is optional override.

Add to `~/.zshrc` only if you need to override the config:

```bash
echo 'export DATABASE_URL="postgres://localhost:5432/forzr"' >> ~/.zshrc
source ~/.zshrc
```

## Step 6: Run Schema

From the pg-memory directory:

```bash
psql -v ON_ERROR_STOP=1 forzr < schema/memory.sql
```

Or with absolute path:

```bash
psql -v ON_ERROR_STOP=1 forzr < /path/to/pg-memory/schema/memory.sql
```

**Note:** The `-v ON_ERROR_STOP=1` flag ensures psql stops on first error, preventing partial schema application.

## Step 7: Verify Tables

```bash
psql forzr -c "\dt"
```

Expected output:

```
         List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+-------
 public | memories        | table | andy16
 public | sources         | table | andy16
```

## Step 8: Verify Indexes

```bash
psql forzr -c "\di"
```

Expected indexes:

- `idx_memories_user`
- `idx_memories_user_created`
- `idx_memories_created`
- `idx_memories_provider_model`
- `idx_memories_session`
- `idx_memories_parent_session`
- `idx_memories_type`
- `idx_memories_importance`
- `idx_memories_tags`
- `idx_memories_metadata`
- `idx_memories_fts`
- `idx_memories_active`
- `idx_memories_cost`
- `idx_memories_started`
- `idx_memories_repo`
- `idx_memories_custom_cmd`
- `idx_memories_custom_cmd_name`
- `idx_sources_user`
- `idx_sources_user_ingested`
- `idx_sources_lookup`
- `idx_sources_type`
- `idx_sources_author`
- `idx_sources_ingested`
- `idx_sources_updated`
- `idx_sources_published`
- `idx_sources_provider_model`
- `idx_sources_session`
- `idx_sources_tags`
- `idx_sources_metadata`
- `idx_sources_fts`
- `idx_sources_active`
- `idx_sources_cost`
- `idx_sources_started`
- `idx_sources_repo`
- `idx_sources_custom_cmd`
- `idx_sources_custom_cmd_name`

## Step 9: Test Insert

```bash
psql forzr << 'EOF'
INSERT INTO memories (
  user_id,
  provider_id, model_id, mode,
  session_id,
  repo_name, repo_path, git_branch, git_commit,
  type, content, importance, tags,
  tokens_input, tokens_output, cost, response_time_ms, finish_reason
)
VALUES (
  'pascalandy',
  'anthropic', 'claude-sonnet-4', 'build',
  'ses_4a30f921fffeExOAtr8adv55fz',
  'forzr', 'Documents/github_local/forzr', 'main', 'a1b2c3d',
  'learning',
  'PostgreSQL memory system is now operational.',
  6,
  '["setup", "postgres"]',
  1500, 250, 0.00234, 1250, 'stop'
)
RETURNING id, created_at, cost;
EOF
```

Expected output:

```
                  id                  |          created_at           |   cost
--------------------------------------+-------------------------------+----------
 a1b2c3d4-e5f6-7890-abcd-ef1234567890 | 2025-12-25 14:30:22.123456-05 | 0.00234000
```

Verify the record:

```bash
psql forzr -c "SELECT id, provider_id, model_id, repo_name, type, content, cost FROM memories WHERE user_id = 'pascalandy' AND deleted_at IS NULL;"
```

## Step 10: Test Full-Text Search

```bash
psql forzr -c "SELECT id, content FROM memories WHERE user_id = 'pascalandy' AND content_tsv @@ plainto_tsquery('simple', 'postgresql') AND deleted_at IS NULL;"
```

**Note:** We use `'simple'` language configuration for mixed English/French content support.

## Step 11: Test updated_at Trigger

```bash
psql forzr << 'EOF'
-- Insert a test source
INSERT INTO sources (user_id, name, source_type, content, provider_id, model_id)
VALUES ('pascalandy', 'test_source', 'documentation', 'Initial content', 'anthropic', 'claude-sonnet-4')
RETURNING id, updated_at;

-- Wait a moment and update
SELECT pg_sleep(0.1);

-- Update and verify updated_at changed
UPDATE sources SET content = 'Updated content' WHERE name = 'test_source';
SELECT id, updated_at FROM sources WHERE name = 'test_source';

-- Cleanup
DELETE FROM sources WHERE name = 'test_source';
EOF
```

Expected: `updated_at` should be different (later) after the UPDATE.

## Step 12: Test Cost and Token Tracking

```bash
psql forzr << 'EOF'
-- Insert memories with cost data
INSERT INTO memories (user_id, provider_id, model_id, type, content, tokens_input, tokens_output, cost)
VALUES
  ('pascalandy', 'anthropic', 'claude-sonnet-4', 'observation', 'Test memory 1', 1000, 200, 0.0015),
  ('pascalandy', 'openai', 'gpt-4o', 'observation', 'Test memory 2', 2000, 400, 0.0045),
  ('pascalandy', 'anthropic', 'claude-opus-4', 'observation', 'Test memory 3', 5000, 1000, 0.075);

-- Query total cost by provider
SELECT provider_id,
       COUNT(*) as memories,
       SUM(tokens_input) as total_input,
       SUM(tokens_output) as total_output,
       SUM(cost) as total_cost
FROM memories
WHERE user_id = 'pascalandy'
  AND deleted_at IS NULL
GROUP BY provider_id
ORDER BY total_cost DESC;

-- Cleanup
DELETE FROM memories WHERE type = 'observation' AND content LIKE 'Test memory%';
EOF
```

## Step 13: Test Git Context and Command Tracking

```bash
psql forzr << 'EOF'
-- Insert a command summary with git context
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
  'Test command: completed successfully',
  5,
  'forzr', 'Documents/github_local/forzr', 'main', 'test123',
  '.opencode/command/test.md', '2025-12-26T10:00:00',
  NOW() - INTERVAL '5 minutes', NOW(), 300000, 0.05,
  '{"test": true}'
)
RETURNING id, custom_cmd_name, response_time_ms;

-- Query by repository
SELECT repo_name, git_branch, type, LEFT(content, 50) as content
FROM memories
WHERE user_id = 'pascalandy'
  AND repo_name = 'forzr'
  AND deleted_at IS NULL
ORDER BY created_at DESC
LIMIT 5;

-- Query command analytics
SELECT
  custom_cmd_name,
  COUNT(*) as runs,
  ROUND(AVG(response_time_ms) / 60000.0, 1) as avg_minutes
FROM memories
WHERE user_id = 'pascalandy'
  AND custom_cmd_name IS NOT NULL
  AND deleted_at IS NULL
GROUP BY custom_cmd_name;

-- Cleanup
DELETE FROM memories WHERE custom_cmd_name = '.opencode/command/test.md';
EOF
```

## Step 14: Verify Installation

Run the verification script:

```bash
./scripts/verify_pg_memory.sh
```

See `scripts/verify_pg_memory.sh` for the full verification script.

**Note:** The verification script may need updating to test the new columns.

## Troubleshooting

### PostgreSQL not running

```bash
brew services list | rg postgresql
# If not started:
brew services start postgresql@18
```

### Permission denied

```bash
# Check current user
whoami

# Ensure your user owns the database
psql -c "SELECT current_user;"
```

### Database doesn't exist

```bash
createdb forzr
```

### Can't connect

```bash
# Test connection
psql postgres -c "SELECT 1;"

# If socket error, check PostgreSQL is running
pg_isready

# Check what's on port 5432
lsof -i :5432
```

### Schema errors

```bash
# Check PostgreSQL version (must be 18+)
psql --version

# View logs
tail -50 /opt/homebrew/var/log/postgresql@18.log
```

## Maintenance Commands

### Backup

```bash
# Plain SQL backup
pg_dump forzr > backup_$(date +%Y%m%d).sql

# Compressed backup (recommended)
pg_dump -Fc forzr > backup_$(date +%Y%m%d).dump
```

### Verify Backup

```bash
# List contents of compressed backup
pg_restore --list backup_20251225.dump | head -20
```

### Restore

```bash
# From plain SQL
psql -v ON_ERROR_STOP=1 forzr < backup_20251225.sql

# From compressed backup
pg_restore -d forzr backup_20251225.dump
```

### Reset Database (DESTRUCTIVE)

```bash
psql -v ON_ERROR_STOP=1 forzr -c "DROP TABLE IF EXISTS memories CASCADE; DROP TABLE IF EXISTS sources CASCADE;"
psql -v ON_ERROR_STOP=1 forzr < schema/memory.sql
```

**Note:** This is the current migration strategy. For schema changes, reset and re-apply. See "Out of Scope" section for future migration tooling.

### Check Table Sizes

```bash
psql forzr -c "
SELECT
  relname as table,
  pg_size_pretty(pg_total_relation_size(relid)) as size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
"
```

### Count Rows

```bash
psql forzr -c "
SELECT 'memories' as table, COUNT(*) as total, COUNT(*) FILTER (WHERE deleted_at IS NULL) as active FROM memories
UNION ALL
SELECT 'sources', COUNT(*), COUNT(*) FILTER (WHERE deleted_at IS NULL) FROM sources;
"
```

### Vacuum and Analyze

```bash
vacuumdb --analyze forzr
```

### Permanently Delete Old Soft-Deleted Records

```bash
psql forzr -c "
DELETE FROM memories WHERE deleted_at < NOW() - INTERVAL '90 days';
DELETE FROM sources WHERE deleted_at < NOW() - INTERVAL '90 days';
"
```
