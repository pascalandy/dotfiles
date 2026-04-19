---
name: pa-scout
description: Discovery entry point — map an unfamiliar surface before deciding what to change
tags:
  - area/ea
  - kind/doc
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-11
date_updated: 2026-04-18
---

# pa-scout

**Entry point:** `pa-scout`
**Source:** `dot_config/ai_templates/skills/pa-sdlc/pa-scout/SKILL.md`

## What it does

Discover and map the current state of an unfamiliar surface. Produces a map, a walkthrough, an answer, or a history — not a plan.

## When to use

- Landing in an unfamiliar repo, content system, or workspace.
- Walking a human (or yourself) through a surface for teaching.
- One focused question needs current-state evidence.
- The current state only makes sense with its history.

## Modes

| Mode | Use when |
|---|---|
| `OrientationScan` | Quick first-pass map and next place to look |
| `StructuredOnboarding` | Human-friendly guided walkthrough |
| `TargetedInquiry` | Narrow research on one focused question |
| `HistoryArchaeology` | Evolution over time matters more than current state |

## Don't use for

- Scoping a specific change → `pa-scope`
- Deciding whether a direction is worth pursuing → `pa-vision`
- Designing execution → `pa-architect`
