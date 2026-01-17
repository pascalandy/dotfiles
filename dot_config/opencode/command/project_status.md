# Project Status — Orchestrator

Delegate to agents, aggregate responses

## Agents

| Alias | Fallback | Use                           |
| ----- | -------- | ----------------------------- |
| L1    | L2       | Quick tasks, script, analysis |
| L2    | L3       | Commits, post-mortem          |
| L3    | ORACLE   | Report writing                |

Fallback triggers: timeout >60s, invalid JSON

## Paths

| Key    | Path                                              |
| ------ | ------------------------------------------------- |
| SCRIPT | `.opencode/skill/project_status/scan_projects.py` |
| OUT    | `EXPORT/statut_de_projet/STATUT_<RUN_ID>/`        |

## Constraints

Max parallel: 9
Queue: when agent finishes, launch next

## File Structure

```
EXPORT/statut_de_projet/
├── STATUT_<run_id>/
│   ├── discovery.json
│   └── STATUT.md
└── historique/
```

## Workflow (6 Steps)

| Step | Agent | Action                      | Returns          |
| ---- | ----- | --------------------------- | ---------------- |
| 0    | L1    | `uv run {SCRIPT}`           | run_id           |
| 1    | L1×9  | Analyze projects (parallel) | JSON per project |
| 2    | L3    | Write {OUT}STATUT.md        | success          |
| 3    | L2    | Append post-mortem          | —                |
| 4    | L2    | Commit files                | committed        |
| 5    | —     | Summary to user             | —                |

## Step 0: Pre-scan

Agent: L1

```bash
uv run .opencode/skill/project_status/scan_projects.py
```

Post-agent: store RUN_ID, read discovery.json

## Step 1: Analysis

Agent: L1 per project (max 9 parallel)

Prompt: see `ANALYSIS_PROMPT.md`

Queue until all projects analyzed

## Step 2: Report

Agent: L3

Write {OUT}STATUT.md using template from `TEMPLATE.md`

Content:

1. YAML frontmatter
2. Git metrics (7 days, recent first)
3. WORKDIR: table + details (sort: maturity desc, priority)
4. Ideation: table only

## Step 3: Post-mortem

Orchestrator drafts:

- Duration
- Projects analyzed/total
- Agent failures

Detail: short if OK, detailed if problems

Agent: L2 appends to STATUT.md

## Step 4: Commit

Agent: L2

```bash
git add {OUT}STATUT.md {OUT}discovery.json
git commit -m "chore(status): update project status <DATE> (<N>/<TOTAL> projects)"
```

## Step 5: Return

Display:

- Folder path
- Commit confirmation
- Duration

Example:

```
Folder: EXPORT/statut_de_projet/STATUT_2025_12_30_14h30/
Files: STATUT.md + discovery.json
Commit: chore(status): update project status 2025-12-30 (27/27)
Duration: 8m 42s
```
