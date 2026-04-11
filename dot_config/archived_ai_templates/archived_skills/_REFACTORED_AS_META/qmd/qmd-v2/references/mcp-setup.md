# QMD MCP Reference

Read this file when the user asks about QMD MCP setup, current tool names, Claude Code / Claude Desktop integration, HTTP transport, or when an agent should use QMD through MCP instead of the CLI.

## Install and prepare QMD

```bash
npm install -g @tobilu/qmd
# or
bun install -g @tobilu/qmd

qmd collection add ~/path/to/markdown --name myknowledge
qmd context add qmd://myknowledge "Local markdown knowledge base"
qmd update
qmd embed
```

If files already exist in the collection and have changed since indexing, run:

```bash
qmd update
qmd embed
```

## Current MCP tool names

Current upstream MCP tool names are:
- `query`
- `get`
- `multi_get`
- `status`

In some harnesses they appear namespaced, for example:
- `mcp__qmd__query`
- `mcp__qmd__get`
- `mcp__qmd__multi_get`
- `mcp__qmd__status`

Important migration note:
- older names like `search`, `vector_search`, `deep_search`, and `structured_search` are obsolete
- some older docs or examples may still mention them; prefer the tool names above

## Tool mapping

| Need | CLI | MCP |
|---|---|---|
| Best-quality search | `qmd query` | `query` |
| Retrieve one document | `qmd get` | `get` |
| Retrieve many documents | `qmd multi-get` | `multi_get` |
| Check health / collections | `qmd status` | `status` |

Practical guidance:
- Default to `query` when recall quality matters.
- Follow every important search with `get` or `multi_get` before making strong claims.
- Pass collection filters whenever the likely source is known.
- Provide `intent` whenever the query is ambiguous.

## MCP `query` input shape

The MCP `query` tool takes structured sub-queries instead of raw CLI text.

Core fields:
- `searches`: array of typed sub-queries
- `limit`: max results
- `minScore`: minimum score threshold
- `candidateLimit`: rerank candidate cap
- `collections`: array of collection names
- `intent`: background context for disambiguation

Each `searches` item looks like:

```json
{ "type": "lex", "query": "\"connection pool\" timeout -redis" }
```

Supported types:
- `lex`
- `vec`
- `hyde`

## MCP query examples

Simple exact lookup:

```json
{
  "searches": [
    { "type": "lex", "query": "CAP theorem" }
  ],
  "collections": ["docs"],
  "limit": 5
}
```

Best recall on a technical topic:

```json
{
  "searches": [
    { "type": "lex", "query": "\"connection pool\" timeout -redis" },
    { "type": "vec", "query": "why do database connections time out under load" },
    { "type": "hyde", "query": "Connection pool exhaustion happens when all database connections are in use and new requests wait under concurrency." }
  ],
  "collections": ["docs"],
  "candidateLimit": 60,
  "limit": 10
}
```

Intent-aware ambiguous query:

```json
{
  "searches": [
    { "type": "lex", "query": "\"performance\" optimization" },
    { "type": "vec", "query": "how to optimize C++ program performance" }
  ],
  "collections": ["notes"],
  "intent": "C++ runtime optimization, not sports",
  "limit": 10
}
```

## Claude Code setup

Recommended plugin install:

```bash
claude plugin marketplace add tobi/qmd
claude plugin install qmd@qmd
```

Manual MCP config in `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

## Claude Desktop setup

File: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

## HTTP transport and daemon mode

By default, `qmd mcp` uses stdio. For a shared long-lived server:

```bash
qmd mcp
qmd mcp --http              # localhost:8181/mcp
qmd mcp --http --port 8080
qmd mcp --http --daemon
qmd mcp stop
```

Useful endpoints:
- `POST /mcp`
- `GET /health`
- `POST /query` as the lightweight HTTP search endpoint
- `POST /search` remains as a silent alias for compatibility

HTTP transport is useful for repeated agent workflows because model startup cost is paid once. Recent QMD releases also added multi-session HTTP support, so concurrent clients can connect without sharing the same in-process session.

## Troubleshooting

- Verify install: `which qmd`
- Verify version: `qmd --version`
- Verify collections: `qmd status` or `qmd collection list`
- Weak semantic results: `qmd embed`
- Stale results after file changes: `qmd update && qmd embed`
- Check whether daemon is active: `qmd status`
- If an integration still uses old MCP tool names, update it to `query`, `get`, `multi_get`, and `status`
