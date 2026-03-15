# OpenCode CLI Reference

Use this file when the user needs command-line help or a smoke test.

## Core commands

```bash
opencode
opencode --continue
opencode --agent plan
opencode run "your prompt"
opencode web
opencode serve
```

## Discovery commands

```bash
opencode models
opencode agent create
opencode agent list
opencode mcp list
opencode session list
opencode stats
```

## Practical checks

- `opencode models` helps verify model identifiers.
- A small `opencode run "..."` call is a practical smoke test when config changes may affect startup.
- Use the least invasive command that proves the config loads.
