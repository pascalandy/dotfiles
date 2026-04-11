---
name: pa-vision
description: Direction-setting entry point for defining where work is going before execution planning begins. Use `pa-vision` when you need to pressure-test the direction, align on the end state, or package settled direction into a durable brief.
keywords: [pa-vision, vision, direction, alignment, brief, prd, direction-check]
---

# Vision

Explicit entry point: `pa-vision`.

Use Vision to answer one question before planning: where are we going?

## Route

Load `references/ROUTER.md`.

## Use This When

- You need to test whether a direction is worth pursuing.
- You need to make the target state explicit before planning.
- You need a durable brief for settled direction.

## Internal Modes

| Mode | Owns | Use when |
|---|---|---|
| `DirectionCheck` | Direction pressure test | You need a go, revise, defer, or stop recommendation |
| `AlignmentDraft` | Default pre-planning artifact | You need the current state, end state, and pattern choices made explicit |
| `BriefAuthoring` | Durable brief or PRD | The direction is settled and the main job is packaging it cleanly |

## Boundaries

| If the real need is... | Use instead |
|---|---|
| understanding what exists today | `pa-scout` |
| identifying what is in play for a change | `pa-scope` |
| designing execution, structure, or sequencing | `pa-architect` |
| building the change or fixing a bug | `pa-implement` |
| documenting an already-made change, decision, or artifact | `pa-doc-update` |
| refreshing, deduplicating, or repairing existing docs | `pa-doc-cleaner` |

## Default Output

Default to a direction-oriented artifact that makes these easy to find:

1. request or decision
2. current state
3. desired end state
4. key decisions or pattern choices
5. success signals
6. risks and review points
7. recommended next phase

## Non-Goals

Vision does not own scoping, execution planning, implementation, release documentation, or documentation maintenance.
