---
name: pa-scope
description: Scoping entry point for deciding what is in play for a requested change across code, content, workflows, knowledge systems, or personal systems. Use `pa-scope` when you need the touch surface, blast radius, or a judgment about whether one artifact matters.
keywords: [pa-scope, scope, scoping, blast-radius, impact, touch-surface, artifact-clarifier]
---

# Scope

Explicit entry point: `pa-scope`.

Use Scope to answer one question before planning or implementation: what is actually in play here?

## Route

Load `references/ROUTER.md`.

## Use This When

- You need the likely touch surface for a requested change.
- You need upstream or downstream impact from a known artifact.
- You need to decide whether one artifact belongs in scope.

## Internal Modes

| Mode | Owns | Use when |
|---|---|---|
| `ChangeSurface` | Bounded scope map | You need the likely primary and adjacent surfaces |
| `ImpactTrace` | Blast-radius tracing | You already know the starting artifact and need propagation paths |
| `ArtifactClarifier` | One scoping decision around one artifact | You must understand one file, page, workflow, or note before including it |

## Boundaries

| If the real need is... | Use instead |
|---|---|
| broad orientation or current-state research | `pa-scout` |
| deciding whether the direction is right | `pa-vision` |
| designing execution or sequencing work | `pa-architect` |
| building the change or fixing the bug | `pa-implement` |
| documenting the result or one concrete artifact | `pa-doc-update` |
| refreshing, deduplicating, or repairing existing docs | `pa-doc-cleaner` |

## Default Output

Default to a brief that covers:

1. requested change
2. primary scope
3. adjacent affected areas
4. relationship paths
5. validation surfaces
6. risks and unknowns
7. recommended next step

## Non-Goals

Scope does not own broad discovery, product direction, execution planning, implementation, or documentation work.
