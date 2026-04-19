---
name: pa-implement
description: Execution entry point — apply a bounded change (TDD, vertical slices) or repair broken behavior from root cause
tags:
  - area/ea
  - kind/doc
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-11
date_updated: 2026-04-18
---

# pa-implement

**Entry point:** `pa-implement`
**Source:** `dot_config/ai_templates/skills/pa-sdlc/pa-implement/SKILL.md`

## What it does

Build the change or fix the bug. TDD by default for behavior-bearing work, vertical slices over horizontal layers, and for bugs: reproduce first, explain the defect, then repair at the root.

## When to use

- Work is ready to execute and one first slice can be named clearly.
- Something is broken and a trustworthy fix needs reproduction + root-cause reasoning.

## Modes

| Mode | Use when |
|---|---|
| `ChangeApplication` | Normal bounded execution — one first slice, TDD posture |
| `RootCauseRepair` | Debug path: reproduce → explain → repair → verify |

## Pre-flight before ChangeApplication

Confirm all three or back up a stage:

- Outcome is specific enough to **name one first slice**.
- Execution surface is known enough to **start**.
- Remaining uncertainty is **execution detail**, not discovery, scope, direction, or planning.

## Don't use for

- Orientation → `pa-scout`
- Change surface → `pa-scope`
- Direction → `pa-vision`
- Roadmap, spike, structure → `pa-architect`
- Post-change docs → `pa-doc-update`
