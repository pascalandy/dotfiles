## When we edit the configuration for a given MCP, on which file should this configuration be done?

MCP configuration should be done in your OpenCode config file (`opencode.json` or `opencode.jsonc`).
You can place this config in:

- `~/.config/opencode/opencode.json` (global)
- `opencode.json` in your project root (per-project)
- Custom path via `OPENCODE_CONFIG` environment variable
  The MCP configuration goes under the `mcp` key in your config file.
