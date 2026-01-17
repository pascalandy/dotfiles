-- pg-memory schema for PostgreSQL 18
-- Database: forzr
-- Version: 5.1
-- Updated: 2025-12-27
--
-- Multi-User: user_id required on all tables (SaaS-ready, Option A)
-- FTS: Uses 'simple' language config for mixed EN/FR content
-- JSONB: tags must be array, metadata must be object
-- OpenCode: Captures provider, model, tokens, cost, timing from LLM calls
-- Git Context: repo_name, repo_path, git_branch, git_commit
-- Command Tracking: custom_cmd_name, custom_cmd_run_date for slash command analytics
-- Importance: 0-7 semantic scale (0=unrated, 1=avoid, 7=perfect)
-- Manual Ingestion: provider_id='manual', model_id='none' for non-LLM content

--------------------------------------------------------------------------------
-- Table: memories
-- Stores agent memories (actions, observations, thoughts, decisions, etc.)
--------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS memories (
  id                  UUID PRIMARY KEY DEFAULT uuidv7(),
  user_id             TEXT NOT NULL CHECK (user_id ~ '^[a-z0-9_-]+$'),      -- 'pascalandy', 'julia'
  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  deleted_at          TIMESTAMPTZ,              -- NULL = active, timestamp = soft deleted
  
  -- Provider/Model (required)
  -- Use 'manual'/'none' for non-LLM content (copy-paste, Obsidian sync)
  provider_id         TEXT NOT NULL CHECK (provider_id ~ '^[a-z0-9_-]+$'),  -- 'anthropic', 'openai', 'google', 'manual'
  model_id            TEXT NOT NULL CHECK (model_id ~ '^[a-z0-9._-]+$'),    -- 'claude-sonnet-4', 'gpt-4o', 'none'
  mode                TEXT,                     -- 'build', 'plan', 'ask'
  
  -- Session tracking
  session_id          TEXT,                     -- OpenCode session ID (e.g., 'ses_4a30f921fffeExOAtr8adv55fz')
  parent_session_id   TEXT,                     -- Parent session ID (for sub-agent/Task tool memories)
  
  -- Git context
  repo_name           TEXT,                     -- 'forzr', 'nuxt_blog'
  repo_path           TEXT,                     -- 'Documents/github_local/forzr' (relative to $HOME)
  git_branch          TEXT,                     -- 'main', 'feature/memory'
  git_commit          TEXT,                     -- 'a1b2c3d' (short SHA)
  
  -- Command tracking
  custom_cmd_name     TEXT,                     -- '.opencode/command/project_status.md'
  custom_cmd_run_date TEXT,                     -- '2025-12-25T14:30:00' (ISO format)
  
  -- Memory content
  type                TEXT NOT NULL,            -- flexible: 'action', 'observation', 'thought', etc.
  content             TEXT NOT NULL,
  content_tsv         TSVECTOR GENERATED ALWAYS AS (to_tsvector('simple', content)) STORED,
  importance          INTEGER DEFAULT 0 CHECK (importance BETWEEN 0 AND 7),  -- 0=unrated, 1=avoid, 7=perfect
  tags                JSONB CHECK (tags IS NULL OR jsonb_typeof(tags) = 'array'),
  metadata            JSONB CHECK (metadata IS NULL OR jsonb_typeof(metadata) = 'object'),
  
  -- Token usage
  tokens_input        INTEGER,
  tokens_output       INTEGER,
  tokens_reasoning    INTEGER,                  -- Extended thinking tokens
  tokens_cache_read   INTEGER,
  tokens_cache_write  INTEGER,
  
  -- Cost and timing
  cost                NUMERIC(15, 8),           -- Cost in dollars (supports micro-costs)
  started_at          TIMESTAMPTZ,              -- When LLM call started
  completed_at        TIMESTAMPTZ,              -- When LLM call completed
  response_time_ms    INTEGER,                  -- Response time in milliseconds
  finish_reason       TEXT                      -- 'stop', 'length', 'tool_calls', etc.
);

-- Indexes for memories
CREATE INDEX IF NOT EXISTS idx_memories_user           ON memories(user_id);
CREATE INDEX IF NOT EXISTS idx_memories_user_created   ON memories(user_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_created        ON memories(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_provider_model ON memories(provider_id, model_id);
CREATE INDEX IF NOT EXISTS idx_memories_session        ON memories(session_id);
CREATE INDEX IF NOT EXISTS idx_memories_parent_session ON memories(parent_session_id);
CREATE INDEX IF NOT EXISTS idx_memories_type           ON memories(type);
CREATE INDEX IF NOT EXISTS idx_memories_importance     ON memories(importance DESC);
CREATE INDEX IF NOT EXISTS idx_memories_tags           ON memories USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_memories_metadata       ON memories USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_memories_fts            ON memories USING GIN(content_tsv);
CREATE INDEX IF NOT EXISTS idx_memories_active         ON memories(deleted_at) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_memories_cost           ON memories(cost);
CREATE INDEX IF NOT EXISTS idx_memories_started        ON memories(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_memories_repo           ON memories(repo_name);
CREATE INDEX IF NOT EXISTS idx_memories_custom_cmd      ON memories(custom_cmd_run_date);
CREATE INDEX IF NOT EXISTS idx_memories_custom_cmd_name ON memories(custom_cmd_name);


--------------------------------------------------------------------------------
-- Table: sources
-- Stores external sources: documentation, blog posts, podcasts, books, etc.
--------------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS sources (
  id                  UUID PRIMARY KEY DEFAULT uuidv7(),
  user_id             TEXT NOT NULL CHECK (user_id ~ '^[a-z0-9_-]+$'),      -- 'pascalandy', 'julia'
  name                TEXT NOT NULL,            -- 'Nuxt', 'Syntax', 'project-ideas.md'
  title               TEXT,                     -- 'Getting Started', 'Episode 842: AI in 2025'
  source_type         TEXT NOT NULL,            -- 'documentation', 'podcast', 'blog_post', 'obsidian_note', etc.
  version             TEXT,                     -- '4.0.0' or NULL if unversioned
  source_url          TEXT,
  content             TEXT NOT NULL,
  content_tsv         TSVECTOR GENERATED ALWAYS AS (
                        to_tsvector('simple', COALESCE(name, '') || ' ' || COALESCE(title, '') || ' ' || content)
                      ) STORED,
  author              TEXT,                     -- 'Evan You', 'Scott Tolinski'
  published_at        TIMESTAMPTZ,              -- when original was published
  ingested_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  superseded_at       TIMESTAMPTZ,              -- NULL = current version
  deleted_at          TIMESTAMPTZ,              -- NULL = active, timestamp = soft deleted
  
  -- Provider/Model (required)
  -- Use 'manual'/'none' for non-LLM content (copy-paste, Obsidian sync)
  provider_id         TEXT NOT NULL CHECK (provider_id ~ '^[a-z0-9_-]+$'),  -- 'anthropic', 'manual'
  model_id            TEXT NOT NULL CHECK (model_id ~ '^[a-z0-9._-]+$'),    -- 'claude-sonnet-4', 'none'
  mode                TEXT,
  
  -- Session tracking
  session_id          TEXT,                     -- OpenCode session ID (e.g., 'ses_4a30f921fffeExOAtr8adv55fz')
  parent_session_id   TEXT,                     -- Parent session ID (for sub-agent ingestions)
  
  -- Git context
  repo_name           TEXT,
  repo_path           TEXT,
  git_branch          TEXT,
  git_commit          TEXT,
  
  -- Command tracking
  custom_cmd_name     TEXT,
  custom_cmd_run_date TEXT,
  
  -- Token usage
  tokens_input        INTEGER,
  tokens_output       INTEGER,
  tokens_reasoning    INTEGER,
  tokens_cache_read   INTEGER,
  tokens_cache_write  INTEGER,
  
  -- Cost and timing
  cost                NUMERIC(15, 8),
  started_at          TIMESTAMPTZ,
  completed_at        TIMESTAMPTZ,
  response_time_ms    INTEGER,
  finish_reason       TEXT,
  
  -- Metadata
  tags                JSONB CHECK (tags IS NULL OR jsonb_typeof(tags) = 'array'),
  metadata            JSONB CHECK (metadata IS NULL OR jsonb_typeof(metadata) = 'object')
);

-- Indexes for sources
CREATE INDEX IF NOT EXISTS idx_sources_user           ON sources(user_id);
CREATE INDEX IF NOT EXISTS idx_sources_user_ingested  ON sources(user_id, ingested_at DESC);
CREATE INDEX IF NOT EXISTS idx_sources_lookup         ON sources(name, version, superseded_at);
CREATE INDEX IF NOT EXISTS idx_sources_type           ON sources(source_type);
CREATE INDEX IF NOT EXISTS idx_sources_author         ON sources(author);
CREATE INDEX IF NOT EXISTS idx_sources_ingested       ON sources(ingested_at DESC);
CREATE INDEX IF NOT EXISTS idx_sources_updated        ON sources(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_sources_published      ON sources(published_at DESC);
CREATE INDEX IF NOT EXISTS idx_sources_provider_model ON sources(provider_id, model_id);
CREATE INDEX IF NOT EXISTS idx_sources_session        ON sources(session_id);
CREATE INDEX IF NOT EXISTS idx_sources_tags           ON sources USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_sources_metadata       ON sources USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_sources_fts            ON sources USING GIN(content_tsv);
CREATE INDEX IF NOT EXISTS idx_sources_active         ON sources(deleted_at) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_sources_cost           ON sources(cost);
CREATE INDEX IF NOT EXISTS idx_sources_started        ON sources(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_sources_repo           ON sources(repo_name);
CREATE INDEX IF NOT EXISTS idx_sources_custom_cmd      ON sources(custom_cmd_run_date);
CREATE INDEX IF NOT EXISTS idx_sources_custom_cmd_name ON sources(custom_cmd_name);


--------------------------------------------------------------------------------
-- Trigger: auto-update updated_at on sources
--------------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS sources_updated_at ON sources;
CREATE TRIGGER sources_updated_at
    BEFORE UPDATE ON sources
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();


--------------------------------------------------------------------------------
-- Comments (documentation)
--------------------------------------------------------------------------------

COMMENT ON TABLE memories IS 'Agent memories - explicit decisions that something is worth remembering';
COMMENT ON TABLE sources IS 'External sources: documentation, blog posts, podcasts, books, transcripts, Obsidian notes';

-- memories columns
COMMENT ON COLUMN memories.id IS 'UUID primary key (uuidv7 - time-ordered)';
COMMENT ON COLUMN memories.user_id IS 'User identifier: pascalandy, julia (required for multi-user)';
COMMENT ON COLUMN memories.deleted_at IS 'Soft delete: NULL = active, timestamp = deleted';
COMMENT ON COLUMN memories.provider_id IS 'LLM provider: anthropic, openai, google, manual (for non-LLM content)';
COMMENT ON COLUMN memories.model_id IS 'Model identifier: claude-sonnet-4, gpt-4o, none (for non-LLM content)';
COMMENT ON COLUMN memories.mode IS 'OpenCode mode: build, plan, ask';
COMMENT ON COLUMN memories.session_id IS 'OpenCode session ID (e.g., ses_4a30f921fffeExOAtr8adv55fz)';
COMMENT ON COLUMN memories.parent_session_id IS 'Parent session ID for sub-agent memories (Task tool)';
COMMENT ON COLUMN memories.repo_name IS 'Git repository name (basename)';
COMMENT ON COLUMN memories.repo_path IS 'Repository path relative to $HOME';
COMMENT ON COLUMN memories.git_branch IS 'Git branch at time of memory creation';
COMMENT ON COLUMN memories.git_commit IS 'Git commit SHA (short) at time of memory creation';
COMMENT ON COLUMN memories.custom_cmd_name IS 'Slash command path: .opencode/command/project_status.md';
COMMENT ON COLUMN memories.custom_cmd_run_date IS 'Timestamp when command started (ISO format): 2025-12-25T14:30:00';
COMMENT ON COLUMN memories.type IS 'Flexible types: action, observation, thought, decision, error, learning, project_status, command_summary';
COMMENT ON COLUMN memories.content_tsv IS 'Auto-generated tsvector for full-text search (simple language config)';
COMMENT ON COLUMN memories.importance IS 'Semantic scale 0-7: 0=unrated, 1=avoid, 7=perfect';
COMMENT ON COLUMN memories.tokens_input IS 'Input tokens used in LLM call';
COMMENT ON COLUMN memories.tokens_output IS 'Output tokens generated';
COMMENT ON COLUMN memories.tokens_reasoning IS 'Extended thinking/reasoning tokens';
COMMENT ON COLUMN memories.tokens_cache_read IS 'Tokens read from provider cache';
COMMENT ON COLUMN memories.tokens_cache_write IS 'Tokens written to provider cache';
COMMENT ON COLUMN memories.cost IS 'Cost in dollars (NUMERIC for precision)';
COMMENT ON COLUMN memories.started_at IS 'When the LLM call started';
COMMENT ON COLUMN memories.completed_at IS 'When the LLM call completed';
COMMENT ON COLUMN memories.response_time_ms IS 'Response time in milliseconds';
COMMENT ON COLUMN memories.finish_reason IS 'How response ended: stop, length, tool_calls, content_filter, error';

-- sources columns
COMMENT ON COLUMN sources.id IS 'UUID primary key (uuidv7 - time-ordered)';
COMMENT ON COLUMN sources.user_id IS 'User identifier: pascalandy, julia (required for multi-user)';
COMMENT ON COLUMN sources.name IS 'Source name: project, podcast, blog, filename (e.g., Nuxt, Syntax, project-ideas.md)';
COMMENT ON COLUMN sources.title IS 'Specific piece title: page, episode, article (e.g., Getting Started, Episode 842)';
COMMENT ON COLUMN sources.source_type IS 'Flexible types: documentation, blog_post, podcast, video, book, audiobook, article, coding, obsidian_note';
COMMENT ON COLUMN sources.content_tsv IS 'Auto-generated tsvector for FTS on name + title + content (simple language config)';
COMMENT ON COLUMN sources.updated_at IS 'Last modification time (auto-updated via trigger)';
COMMENT ON COLUMN sources.superseded_at IS 'NULL = current version, timestamp = when it was replaced';
COMMENT ON COLUMN sources.deleted_at IS 'Soft delete: NULL = active, timestamp = deleted';
COMMENT ON COLUMN sources.provider_id IS 'LLM provider: anthropic, openai, google, manual (for non-LLM content)';
COMMENT ON COLUMN sources.model_id IS 'Model identifier: claude-sonnet-4, gpt-4o, none (for non-LLM content)';
COMMENT ON COLUMN sources.repo_name IS 'Git repository where source was ingested';
COMMENT ON COLUMN sources.repo_path IS 'Repository path relative to $HOME';
COMMENT ON COLUMN sources.git_branch IS 'Git branch at ingestion time';
COMMENT ON COLUMN sources.git_commit IS 'Git commit SHA at ingestion time';
COMMENT ON COLUMN sources.custom_cmd_name IS 'Slash command that triggered ingestion';
COMMENT ON COLUMN sources.custom_cmd_run_date IS 'Timestamp when command started (ISO format)';
COMMENT ON COLUMN sources.cost IS 'Cost to ingest this source';
