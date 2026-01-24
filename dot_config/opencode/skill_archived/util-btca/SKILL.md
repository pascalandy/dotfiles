---
name: cli-btca
description: "btca is a cli to query docs. Use when the user asks to 'use btca' or has questions about specific frameworks/libraries that btca supports."
---

# btca (Better Context App)

`btca` is a CLI tool for asking questions about libraries and frameworks by cloning their repositories locally and searching the source code directly.

## Core Workflow

### Asking Questions

To answer a single question about a specific technology:

```bash
btca ask -t <tech> -q "<question>"
```

**Example:**

```bash
btca ask -t opencode -q "Does opencode have an sdk available?"
```

### Available Technologies

To see which technologies are currently configured and available:

```bash
btca config repos list
```

Commonly available: `svelte`, `tailwindcss`, `nextjs`, `opencode`.

## Troubleshooting & Due Diligence

### Technology Not Found

If a requested `<tech>` is not in the list, inform the user: "I can't find <tech>".

### CLI Issues

If the command fails, verify the installation:

```bash
which btca
```

## Advanced Usage & Configuration

For detailed information on adding new repositories, changing models, or using the interactive TUI, refer to the full documentation:

- `references/`
