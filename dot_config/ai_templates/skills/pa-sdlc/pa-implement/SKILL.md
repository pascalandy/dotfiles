---
name: pa-implement
description: Execution entry point for applying a bounded change or repairing broken behavior. Use `pa-implement` when the work is ready to build or when a bug must be reproduced, explained, and fixed.
keywords: [pa-implement, implement, change-application, root-cause-repair, tdd, vertical-slices, debugging]
---

# Implement

Explicit entry point: `pa-implement`.

Use Implement when the work is ready to execute.

## Route

Load `references/ROUTER.md`.

Choose one primary mode in this order:

1. `RootCauseRepair` when the request is bug-shaped, failure-shaped, or regression-shaped.
2. `ChangeApplication` for all other bounded execution work.

Before `ChangeApplication`, confirm all three:

1. the outcome is specific enough to name one first slice
2. the execution surface is known enough to start
3. the remaining uncertainty is execution detail, not unresolved discovery, scope, direction, or planning

## Internal Modes

| Mode | Owns | Use when |
|---|---|---|
| `ChangeApplication` | Normal bounded execution | The work is ready and one first slice can be named clearly |
| `RootCauseRepair` | Debugging and repair | Something is broken and a trustworthy fix requires reproduction and root-cause reasoning |

## Default Posture

- For behavior-bearing software work, default to `TDD`.
- Across all subjects, default to vertical slices over horizontal layers.
- For bug work, reproduce first and keep the repair tied to the explained defect.

## Boundaries

| If the real need is... | Use instead |
|---|---|
| broad orientation | `pa-scout` |
| the change surface or blast radius | `pa-scope` |
| direction, value, or end state | `pa-vision` |
| roadmap design, spikes, or structure design | `pa-architect` |
| post-change documentation for one concrete result | `pa-doc-update` |
| refreshing, deduplicating, or repairing existing docs | `pa-doc-cleaner` |

## Default Output

Keep these six anchors visible:

1. requested change or problem
2. execution boundary
3. work performed or planned
4. verification performed
5. risks or unresolved items
6. recommended next phase

## Non-Goals

Implement does not own discovery, scoping, product definition, execution planning, release documentation, or documentation maintenance.
