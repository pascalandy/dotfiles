# Project Status — Orchestrator

Coordinate multi-agent workflow for project analysis and reporting.

## Files

| File | Purpose |
|------|---------|
| `orchestrator.py` | Main workflow coordinator |
| `scan_projects.py` | Step 0: Discovery script |
| `ANALYSIS_PROMPT.md` | Template for project analysis |
| `TEMPLATE.md` | Template for STATUT.md report |

## Workflow (6 Steps)

```
Step 0 (L1): uv run scan_projects.py → discovery.json
Step 1 (L1×9): Analyze projects (parallel) → analyses.json
Step 2 (L3):   Write STATUT.md using template
Step 3 (L2):   Append post-mortem
Step 4 (L2):   Commit files to git
Step 5:        Summary to user
```

## Usage

```bash
# Full workflow
uv run .opencode/skill/project_status/orchestrator.py

# Dry run (no file writes)
uv run .opencode/skill/project_status/orchestrator.py --dry-run

# No commit (skip git step)
uv run .opencode/skill/project_status/orchestrator.py --no-commit
```

## Paths

| Key | Path |
|-----|------|
| WORKDIR | `WORKDIR/` |
| IDEATION | `IDEATION/` |
| OUTPUT | `EXPORT/statut_de_projet/STATUT_<run_id>/` |

## Output Structure

```
EXPORT/statut_de_projet/
├── STATUT_<run_id>/
│   ├── discovery.json
│   └── STATUT.md
└── historique/
    └── STATUT_<previous_run>/
```

## Agent Fallback

| Alias | Fallback | Use |
|-------|----------|-----|
| L1 | L2 | Quick tasks, script, analysis |
| L2 | L3 | Commits, post-mortem |
| L3 | ORACLE | Report writing |

Fallback triggers: timeout >60s, invalid JSON

## Constraints

- Max parallel: 9 agents
- Timeout: 60s per agent
- Queue: launch next when agent finishes
