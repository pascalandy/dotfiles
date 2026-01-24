#!/bin/bash
# pg-memory verification script
# Run after schema installation to verify everything works

set -euo pipefail

echo "=== pg-memory Verification ==="
echo ""

# Check PostgreSQL is running
echo "1. Checking PostgreSQL..."
pg_isready || {
	echo "   FAIL: PostgreSQL not running"
	exit 1
}
echo "   OK: PostgreSQL running"

# Check database exists
echo "2. Checking database 'forzr'..."
psql -lqt | cut -d \| -f 1 | rg -qw forzr || {
	echo "   FAIL: Database 'forzr' not found"
	exit 1
}
echo "   OK: Database exists"

# Check uuidv7() works (required by schema defaults)
echo "3. Checking uuidv7()..."
psql -v ON_ERROR_STOP=1 forzr -t -c "SELECT uuidv7();" >/dev/null || {
	echo "   FAIL: uuidv7() not available"
	exit 1
}
echo "   OK: uuidv7() works"

# Check tables exist
echo "4. Checking tables..."
psql -v ON_ERROR_STOP=1 forzr -c "\dt" | rg -q memories || {
	echo "   FAIL: Table 'memories' not found"
	exit 1
}
psql -v ON_ERROR_STOP=1 forzr -c "\dt" | rg -q sources || {
	echo "   FAIL: Table 'sources' not found"
	exit 1
}
echo "   OK: Tables exist (memories, sources)"

# Check index count
echo "5. Checking indexes..."
INDEX_COUNT=$(psql -v ON_ERROR_STOP=1 forzr -tAc "SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public';")
echo "   OK: Found $INDEX_COUNT indexes"

# Test memory insert with JSONB constraints
echo "6. Testing memory insert (with JSONB constraints)..."
TEST_ID=$(psql -v ON_ERROR_STOP=1 forzr -tAc "INSERT INTO memories (user_id, provider_id, model_id, type, content, tags, metadata) VALUES ('pascalandy', 'anthropic', 'claude-sonnet-4', 'test', 'verification test', '[\"test\"]', '{\"verified\": true}') RETURNING id;" | head -1)
echo "   OK: Insert worked (id: $TEST_ID)"

# Test FTS with 'simple' config
echo "7. Testing full-text search..."
FTS_RESULT=$(psql -v ON_ERROR_STOP=1 forzr -tAc "SELECT COUNT(*) FROM memories WHERE user_id = 'pascalandy' AND content_tsv @@ plainto_tsquery('simple', 'verification');")
if [ "$FTS_RESULT" -ge 1 ]; then
	echo "   OK: FTS working (found $FTS_RESULT match)"
else
	echo "   FAIL: FTS not working"
	exit 1
fi

# Test updated_at trigger on sources
echo "8. Testing updated_at trigger..."
SOURCE_ID=$(psql -v ON_ERROR_STOP=1 forzr -tAc "INSERT INTO sources (user_id, name, source_type, content, provider_id, model_id, tags, metadata) VALUES ('pascalandy', 'test_source', 'test', 'initial', 'anthropic', 'claude-sonnet-4', '[\"test\"]', '{\"verified\": true}') RETURNING id;" | head -1)
INITIAL_TS=$(psql -v ON_ERROR_STOP=1 forzr -tAc "SELECT updated_at FROM sources WHERE id = '$SOURCE_ID';")
sleep 0.2
psql -v ON_ERROR_STOP=1 forzr -c "UPDATE sources SET content = 'updated' WHERE id = '$SOURCE_ID';" >/dev/null
UPDATED_TS=$(psql -v ON_ERROR_STOP=1 forzr -tAc "SELECT updated_at FROM sources WHERE id = '$SOURCE_ID';")
if [ "$INITIAL_TS" != "$UPDATED_TS" ]; then
	echo "   OK: Trigger working (updated_at changed)"
else
	echo "   FAIL: Trigger not working (updated_at unchanged)"
	exit 1
fi

# Test full insert with git context and command tracking
echo "9. Testing full insert (git context + command tracking)..."
FULL_ID=$(psql -v ON_ERROR_STOP=1 forzr -tAc "INSERT INTO memories (
  user_id, provider_id, model_id, type, content, importance,
  repo_name, repo_path, git_branch, git_commit,
  custom_cmd_name, custom_cmd_run_date,
  session_id, parent_session_id,
  tags, metadata
) VALUES (
  'pascalandy', 'anthropic', 'claude-sonnet-4', 'test', 'full insert test', 5,
  'forzr', 'Documents/github_local/forzr', 'main', 'abc1234',
  '.opencode/command/test.md', '2025-12-27T10:00:00',
  'ses_test123', 'ses_parent456',
  '[\"test\", \"verification\"]', '{\"full_test\": true}'
) RETURNING id;" | head -1)
echo "   OK: Full insert worked (id: $FULL_ID)"

# Verify git context columns
echo "10. Verifying git context columns..."
GIT_CHECK=$(psql -v ON_ERROR_STOP=1 forzr -tAc "SELECT repo_name || '|' || git_branch FROM memories WHERE id = '$FULL_ID';")
if [[ "$GIT_CHECK" == *"forzr"* ]] && [[ "$GIT_CHECK" == *"main"* ]]; then
	echo "   OK: Git context stored correctly"
else
	echo "   FAIL: Git context not stored correctly"
	exit 1
fi

# Verify command tracking columns
echo "11. Verifying command tracking columns..."
CMD_CHECK=$(psql -v ON_ERROR_STOP=1 forzr -tAc "SELECT custom_cmd_name || '|' || custom_cmd_run_date FROM memories WHERE id = '$FULL_ID';")
if [[ "$CMD_CHECK" == *"test.md"* ]] && [[ "$CMD_CHECK" == *"2025-12-27"* ]]; then
	echo "   OK: Command tracking stored correctly"
else
	echo "   FAIL: Command tracking not stored correctly"
	exit 1
fi

# Cleanup test data
echo "12. Cleaning up test data..."
psql -v ON_ERROR_STOP=1 forzr -c "DELETE FROM memories WHERE user_id = 'pascalandy' AND type = 'test';" >/dev/null
psql -v ON_ERROR_STOP=1 forzr -c "DELETE FROM sources WHERE user_id = 'pascalandy' AND source_type = 'test';" >/dev/null
echo "   OK: Test data removed"

echo ""
echo "=== All checks passed ==="
