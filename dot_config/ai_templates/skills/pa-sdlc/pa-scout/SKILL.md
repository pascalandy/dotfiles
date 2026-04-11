---
name: pa-scout
description: Discovery entry point for unfamiliar repos, workspaces, content systems, knowledge bases, or personal systems. Use `pa-scout` when you need orientation, onboarding, focused research, or history before deciding what to change.
keywords: [pa-scout, scout, orientation, onboarding, targeted-inquiry, history, archaeology]
---

# Scout

Explicit entry point: `pa-scout`.

Use Scout to understand what exists before you decide what to change.

## Route

Load `references/ROUTER.md`.

## Use This When

- You need a fast map of an unfamiliar surface.
- You need a guided walkthrough for a human audience.
- You need a focused current-state answer.
- You need history to explain the current state.

## Internal Modes

| Mode | Owns | Use when |
|---|---|---|
| `OrientationScan` | Broad first-pass discovery | You need a quick map and the next place to look |
| `StructuredOnboarding` | Human-friendly walkthrough | You need a newcomer guide or teachable explanation |
| `TargetedInquiry` | Narrow current-state research | You have one focused question and need evidence |
| `HistoryArchaeology` | Evolution over time | History matters more than current-state inspection alone |

## Boundaries

| If the real need is... | Use instead |
|---|---|
| what is in play for a change | `pa-scope` |
| whether the direction is worth pursuing | `pa-vision` |
| how to execute settled work | `pa-architect` |
| applying a change or fixing a bug | `pa-implement` |
| documenting a concrete change, decision, or artifact | `pa-doc-update` |
| refreshing, deduplicating, or repairing existing docs | `pa-doc-cleaner` |

## Default Output

Default to a concise brief that answers:

1. what this is
2. who it serves
3. how it is organized
4. where to look next
5. what is still unknown

## Non-Goals

Scout does not own scoping, product direction, execution planning, implementation, or documentation maintenance.
