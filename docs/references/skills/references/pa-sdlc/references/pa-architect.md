---
name: pa-architect
description: Execution-design entry point — turn settled direction into a plan (roadmap, slice, spike, or structural design)
tags:
  - area/ea
  - kind/doc
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-11
date_updated: 2026-04-18
---

# pa-architect

**Entry point:** `pa-architect`
**Source:** `dot_config/ai_templates/skills/pa-sdlc/pa-architect/SKILL.md`

## What it does

Design execution for a settled direction: signatures, phases, vertical slices, decision spikes, or a stress test of a plan that already exists. Defaults to vertical slices over horizontal layers.

## When to use

- A meaningful plan already exists and needs a readiness review.
- One blocking unknown would make any plan fake until it is resolved.
- The main blocker is target shape or boundary design, not sequencing.
- Direction is settled and the next step is to sequence execution.

## Modes

| Mode | Use when |
|---|---|
| `RoadmapDesign` | Default execution roadmap — sequencing, decisions, risks, checkpoints |
| `DecisionSpike` | One bounded unknown must be answered before planning |
| `StructuralDesign` | Target shape, boundaries, or interface design |
| `PlanStressTest` | A real plan exists and needs challenge before implementation |

## Don't use for

- Scouting the surface → `pa-scout`
- Identifying blast radius → `pa-scope`
- Deciding direction → `pa-vision`
- Writing the code → `pa-implement`
