# QMD MCP Reference

Read this file when the user asks about QMD MCP setup, tool names, Claude Code / Claude Desktop integration, HTTP transport, or when an agent should use QMD through MCP instead of the CLI.

## Install and prepare QMD

```bash
npm install -g @tobilu/qmd
# or
bun install -g @tobilu/qmd

qmd collection add ~/path/to/markdown --name myknowledge
qmd context add qmd://myknowledge "Local markdown knowledge base"
qmd embed
```

If files already exist in the collection and have changed since indexing, run:

```bash
qmd update
qmd embed
```

## Current MCP tool names

Upstream QMD currently exposes these MCP tool base names:
- `qmd_search`
- `qmd_vector_search`
- `qmd_deep_search`
- `qmd_get`
- `qmd_multi_get`
- `qmd_status`

In some harnesses they appear namespaced, for example:
- `mcp__qmd__qmd_search`
- `mcp__qmd__qmd_vector_search`
- `mcp__qmd__qmd_deep_search`
- `mcp__qmd__qmd_get`
- `mcp__qmd__qmd_multi_get`
- `mcp__qmd__qmd_status`

## Tool mapping

| Need | CLI | MCP |
|---|---|---|
| Exact keyword/title search | `qmd search` | `qmd_search` |
| Semantic-only search | `qmd vsearch` | `qmd_vector_search` |
| Best-quality hybrid retrieval | `qmd query` | `qmd_deep_search` |
| Retrieve one document | `qmd get` | `qmd_get` |
| Retrieve many documents | `qmd multi-get` | `qmd_multi_get` |
| Check health/collections | `qmd status` | `qmd_status` |

Practical guidance:
- Default to `qmd_deep_search` when recall quality matters.
- Use `qmd_search` for exact titles, keywords, tags, or identifiers.
- Use `qmd_vector_search` when the user remembers meaning more than wording.
- Follow search with `qmd_get` or `qmd_multi_get` before making strong claims.
- Pass a collection filter whenever the likely source is known.

## Claude Code setup

Recommended plugin install:

```bash
claude marketplace add tobi/qmd
claude plugin add qmd@qmd
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

HTTP daemon mode is useful for repeated agent workflows because models stay loaded and startup cost is paid once.

## Troubleshooting

- Verify install: `which qmd`
- Verify collections: `qmd status` or `qmd collection list`
- Weak semantic results: `qmd embed`
- Stale results after file changes: `qmd update && qmd embed`
- Check whether daemon is active: `qmd status`
