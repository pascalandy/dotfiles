---
name: pa-vision
description: Direction-setting entry point — pressure-test or define where the work is going before execution planning
tags:
  - area/ea
  - kind/doc
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-11
date_updated: 2026-04-18
---

# pa-vision

**Entry point:** `pa-vision`
**Source:** `dot_config/ai_templates/skills/pa-sdlc/pa-vision/SKILL.md`

## What it does

Make the target state and the pattern choices behind it explicit, before execution planning starts. The review point where a human can redirect the direction cheaply.

## When to use

- You are not sure the direction is worth pursuing.
- The target state is implicit and needs to become explicit before Architect starts.
- The direction is settled and needs a durable brief for future reference.

## Modes

| Mode | Use when |
|---|---|
| `DirectionCheck` | Direction pressure test — recommend go, revise, defer, or stop |
| `AlignmentDraft` | Default pre-planning artifact — current state, end state, pattern choices |
| `BriefAuthoring` | Package a settled direction as a durable brief or PRD |

## Don't use for

- Understanding what exists today → `pa-scout`
- Identifying what a change touches → `pa-scope`
- Designing execution or signatures → `pa-architect`
- Building the change → `pa-implement`
