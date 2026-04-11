---
name: pa-doc-cleaner
description: Documentation-maintenance entry point for keeping an existing doc system accurate, compact, and navigable. Use `pa-doc-cleaner` for drift review, deduplication, or structural doc hygiene.
keywords: [pa-doc-cleaner, doc-cleaner, drift-refresh, consolidation, structure-governance, frontmatter, routing]
---

# Doc Cleaner

Explicit entry point: `pa-doc-cleaner`.

Use Doc Cleaner when the documentation system already exists and the job is maintenance.

## Route

Load `references/ROUTER.md`.

## Use This When

- You need to check whether docs still match reality.
- You need to merge overlap, condense repetition, or prune dead knowledge.
- You need to repair frontmatter, indexes, routing, taxonomy, or cross-references.

## Internal Modes

| Mode | Owns | Use when |
|---|---|---|
| `DriftRefresh` | Reality-vs-doc review | You need keep, update, replace, consolidate, or remove judgments |
| `ConsolidationPass` | Redundancy reduction | Canonical truth is already clear and the main job is cleanup |
| `StructureGovernance` | Structural doc hygiene | Metadata, indexes, routing, taxonomy, or navigation are broken |

## Boundaries

| If the real need is... | Use instead |
|---|---|
| documenting one concrete change, decision, or artifact | `pa-doc-update` |
| broad orientation | `pa-scout` |
| scoping a requested change | `pa-scope` |
| defining direction or planning execution | `pa-vision` or `pa-architect` |
| applying a change or fixing a bug | `pa-implement` |

## Default Output

Default to a maintenance brief that covers:

1. maintenance objective
2. primary documentation surface
3. evidence reviewed
4. findings and classifications
5. recommended actions
6. structural or cross-reference effects
7. risks and unknowns
8. recommended next step

## Non-Goals

Doc Cleaner does not own fresh documentation authoring, discovery, scoping, product definition, technical planning, or implementation.
