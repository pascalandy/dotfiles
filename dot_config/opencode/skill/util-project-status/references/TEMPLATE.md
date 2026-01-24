# Report Template

Path: `{OUT}STATUT.md`

## Structure

```md
---
title: Project Status
author: OpenCode
run_id: <RUN_ID>
projects_analyzed: <n>
projects_total: <n>
timestamp_start: <YYYY-MM-DD HH:MM:SS>
timestamp_end: <YYYY-MM-DD HH:MM:SS>
duration: <Xh Ym Zs>
---

# Project Status

Review of projects in `WORKDIR/` and `IDEATION/`

## Codebase Metrics

### <DATE> (most recent)

| Metric | Value |
|--------|-------|
| Commits | <n> |
| Files touched | <prod> + <tests> = <total> |
| Lines added | <prod> + <tests> = <total> |
| Lines deleted | <prod> + <tests> = <total> |
| Net | +<net> |

## WORKDIR

| Priority | Project | Maturity | Action |
|----------|---------|----------|--------|
| High | **<name>** | <X>/5 | <action> |

### 1. <project_name>

**Purpose**: <description>

- Maturity: <X>/5
- Current state: <state>
- Next step: <action>
- Blocker: <blocker> (omit if null)

## Ideation

| Project | Purpose | Maturity |
|---------|---------|----------|
| **<name>** | <description> | <X>/5 |

## Post-mortem

<content>
```

## Rules

- No emojis
- No additional `---` separators after frontmatter
- Project names: basename only, bold
- Duration: `Xh Ym Zs`
- WORKDIR: table + detailed sections
- Ideation: table only
- Sort: maturity desc, then priority
