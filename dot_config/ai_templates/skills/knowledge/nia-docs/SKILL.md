---
name: nia-docs
description: |
  Use when the user needs to browse documentation sites using npx nia-docs. 
  Provides command patterns for searching, reading, and exploring documentation.
---

# nia-docs

Browse any documentation site via bash commands using `npx nia-docs`.

## Quick Start

```bash
# Browse docs interactively
npx nia-docs "$DOC_URL"

# Execute a single command
npx nia-docs "$DOC_URL" -c "<command>"
```

## Configuration

The nia-docs CLI expects a `DOC_URL` environment variable pointing to the documentation site:

```bash
DOC_URL=
```

Set this before running any nia-docs commands.

## Command Patterns

### Search for a topic

```bash
npx nia-docs "$DOC_URL" -c "grep -rl 'topic' ."
```

### Read a specific page

```bash
npx nia-docs "$DOC_URL" -c "cat page-name.md"
```

### Find all markdown files

```bash
npx nia-docs "$DOC_URL" -c "find . -name '*.md'"
```

### List top-level structure

```bash
npx nia-docs "$DOC_URL" -c "tree -L 1"
```

### Browse interactively

```bash
npx nia-docs "$DOC_URL"
```

## Usage Notes

- The shell starts in the docs root
- Use `.` for relative paths
- All standard Unix tools work: `grep`, `find`, `cat`, `tree`, `ls`, `head`, `tail`, `wc`

## Gotchas

- Large documentation sites may take time to index on first run
- Use `-c` flag for non-interactive commands in scripts
- The tool caches indexed docs for faster subsequent access

## Official Documentation

- **nia-docs homepage:** https://www.agentsearch.sh/
- **Tool help:** `npx nia-docs --help`
