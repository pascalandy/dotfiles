---
name: pa-scope
description: Scoping entry point — decide what a requested change actually touches
tags:
  - area/ea
  - kind/doc
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-11
date_updated: 2026-04-18
---

# pa-scope

**Entry point:** `pa-scope`
**Source:** `dot_config/ai_templates/skills/pa-sdlc/pa-scope/SKILL.md`

## What it does

Decide what is in play for a specific requested change — the touch surface, adjacent affected areas, and blast radius. Factual map only: no plan, no direction, no implementation.

## When to use

- A change was requested and you need the likely touch surface.
- You already know the starting artifact and want propagation paths up and down the dependency graph.
- You need a yes/no decision on whether one specific artifact belongs in scope.

## Modes

| Mode | Use when |
|---|---|
| `ChangeSurface` | Bounded map of primary + adjacent surfaces for a requested change |
| `ImpactTrace` | Walk upstream and downstream dependencies from a known artifact |
| `ArtifactClarifier` | One scoping decision around one artifact |

## Don't use for

- Scouting without a change request → `pa-scout`
- Deciding whether the change is worth doing → `pa-vision`
- Sequencing the execution → `pa-architect`
