---
feature_id: feat-1004 (map-filesystem)
name: abstract_gen
status: planned
date_created: 2026-03-21
mode: EXPANSION
---

# abstract_gen

CLI tool to discover, validate, and export atlas files (`.abstract.md`, `.overview.md`) across directory trees.

## Installation

No installation needed. Uses PEP 723 inline dependencies:

```bash
uv run abstract_gen.py --help
```

## Usage

```bash
# Basic scan
uv run abstract_gen.py /path/to/repo

# Show ASCII tree hierarchy
uv run abstract_gen.py /path/to/repo --tree

# JSON output
uv run abstract_gen.py /path/to/repo --format json

# YAML output
uv run abstract_gen.py /path/to/repo --format yaml

# TOML output
uv run abstract_gen.py /path/to/repo --format toml

# Plain list of file paths
uv run abstract_gen.py /path/to/repo --format plain

# Validate atlas files
uv run abstract_gen.py /path/to/repo --validate

# Find orphan directories (missing atlases)
uv run abstract_gen.py /path/to/repo --orphans

# Export as Graphviz DOT
uv run abstract_gen.py /path/to/repo --export graphviz

# Limit recursion depth
uv run abstract_gen.py /path/to/repo --depth 2

# Filter: only dirs with .abstract.md
uv run abstract_gen.py /path/to/repo --has-abstract

# Filter: only dirs with .overview.md
uv run abstract_gen.py /path/to/repo --has-overview

# Filter: only dirs with both atlases
uv run abstract_gen.py /path/to/repo --has-both

# Include frontmatter metadata in output
uv run abstract_gen.py /path/to/repo --metadata

# Show timing statistics
uv run abstract_gen.py /path/to/repo --stats
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success with results |
| 1 | Runtime error (invalid args, path not found) |
| 2 | No matches (valid path, no atlas files) |
| 3 | Validation failures |

## Output Formats

### Human (default)

```
/path/to/repo (abstract, overview)
/path/to/repo/subdir (abstract)
```

### JSON

```json
[
  {
    "path": "/path/to/repo",
    "files": ["abstract", "overview"],
    "layer": "l0",
    "is_valid": true
  }
]
```

### Tree

```
repo/ (l0)
├── subdir/ (l1)
│   └── nested/ (l2)
└── other/ (l1)
```

## Running Tests

```bash
cd /path/to/forzr/tests
uv run pytest ../WORKDIR/abstract_gen/scripts/tests/ -v
```

## Architecture

```
abstract_gen CLI
├── Scanner     — File discovery (symlink-aware)
├── Parser      — YAML frontmatter parsing
├── Validator   — Consistency checks
├── TreeBuilder — Hierarchy construction
└── Exporter    — Multi-format output
```

## Atlas File Format

Atlas files are Markdown with YAML frontmatter:

```yaml
---
type: atlas
layer: l0
corpus: mixed
scope: top
root: project_name
parent:
date_updated: 2026-03-21
---

# Abstract or Overview

Content here...
```

### Required Fields

- `type` — Document type (typically "atlas")
- `layer` — Hierarchy level (l0, l1, l2...)
- `corpus` — Content type (code, mixed, docs...)
- `scope` — Scope indicator (top, sub, project...)
- `root` — Root project name

### Optional Fields

- `parent` — Parent directory reference
- `date_updated` — Last update date (YYYY-MM-DD)
