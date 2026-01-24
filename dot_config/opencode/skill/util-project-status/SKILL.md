---
name: project-status
description: |
  Orchestrate a multi-agent workflow for project status reporting across WORKDIR/ and IDEATION.
  Use when the user asks for a project status overview, requests a scan, or says "run project status".
---

# Project Status

Run a multi-agent workflow for project analysis and reporting.

## Quick Start

```bash
# Full workflow (scan + analyze + report + commit)
uv run ~/.config/opencode/skill/util-project-status/scripts/orchestrator.py

# Dry run (no file writes)
uv run ~/.config/opencode/skill/util-project-status/scripts/orchestrator.py --dry-run

# Skip git commit
uv run ~/.config/opencode/skill/util-project-status/scripts/orchestrator.py --no-commit
```

## Scan Only

```bash
# Just scan projects without full analysis
uv run ~/.config/opencode/skill/util-project-status/scripts/scan_projects.py

# Show last scan result
uv run ~/.config/opencode/skill/util-project-status/scripts/scan_projects.py --latest

# Machine-readable output
uv run ~/.config/opencode/skill/util-project-status/scripts/scan_projects.py --json
```

## Workflow Steps

| Step | Agent | Description |
|------|-------|-------------|
| 0 | L1 | Run scan_projects.py → discovery.json |
| 1 | L1×9 | Analyze projects in parallel → analyses.json |
| 2 | L3 | Write STATUT.md using template |
| 3 | L2 | Append post-mortem |
| 4 | L2 | Commit files to git |
| 5 | - | Summary to user |

## Output Structure

```
EXPORT/statut_de_projet/
├── STATUT_<run_id>/
│   ├── discovery.json
│   └── STATUT.md
└── historique/
    └── STATUT_<previous_run>/
```

## Constraints

- Max 9 parallel agents
- 60s timeout per agent

## References

- **Analysis prompt**: See [references/ANALYSIS_PROMPT.md](references/ANALYSIS_PROMPT.md)
- **Report template**: See [references/TEMPLATE.md](references/TEMPLATE.md)
