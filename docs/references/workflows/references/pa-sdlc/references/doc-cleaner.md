---
name: Doc-cleaner
description: `pa-doc-cleaner` is the documentation-maintenance entry point — use it for drift review, deduplication, and structural doc hygiene
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - pa-sdlc
---

Doc-cleaner is the seventh stage of `pa-sdlc`. Load it with the explicit entry point `pa-doc-cleaner`.

Use Doc-cleaner when the documentation system already exists and the job is maintenance — checking drift, merging duplicates, repairing frontmatter or routing, pruning dead content. It is the opposite of Doc-update: Doc-update writes one new thing; Doc-cleaner maintains the existing surface.

Source: `dot_config/ai_templates/skills/pa-sdlc/pa-doc-cleaner/SKILL.md`.

## When to reach for Doc-cleaner

| Situation | Mode |
|---|---|
| You need to check whether docs still match reality. | `DriftRefresh` |
| Canonical truth is clear and the main job is reducing redundancy. | `ConsolidationPass` |
| Metadata, indexes, routing, taxonomy, or navigation are broken. | `StructureGovernance` |

## Three internal modes

| Mode | Owns | Use when |
|---|---|---|
| `DriftRefresh` | Reality-vs-doc review | You need keep, update, replace, consolidate, or remove judgments |
| `ConsolidationPass` | Redundancy reduction | Canonical truth is already clear and the main job is cleanup |
| `StructureGovernance` | Structural doc hygiene | Metadata, indexes, routing, taxonomy, or navigation are broken |

## Default output shape

A Doc-cleaner maintenance brief covers:

1. **Maintenance objective** — what this pass is trying to fix.
2. **Primary documentation surface** — the subtree or set of pages under review.
3. **Evidence reviewed** — which pages were read, which source files were checked, which tools were run.
4. **Findings and classifications** — each affected page gets a judgment: keep, update, replace, consolidate, or remove.
5. **Recommended actions** — the concrete edits implied by the findings.
6. **Structural or cross-reference effects** — indexes, LOGs, wikilinks that need to update alongside the page edits.
7. **Risks and unknowns** — what could go wrong if the actions are applied, what the pass could not verify.
8. **Recommended next step** — usually the actual execution of the recommended actions, or a handoff back to Doc-update for a page that turned out to need fresh authoring.

## The five-judgment frame

Every page affected by a DriftRefresh pass gets exactly one of these judgments:

| Judgment | Meaning | Action |
|---|---|---|
| **Keep** | Still accurate, no change needed. | Confirm and move on. |
| **Update** | Still the right page, but details drifted. | Edit in place. |
| **Replace** | Wrong frame or wrong scope; the page needs a full rewrite. | Rewrite from scratch or hand off to Doc-update. |
| **Consolidate** | Overlaps another page; the two should merge. | Merge, leaving one canonical page and redirects or back-links from the other. |
| **Remove** | No longer true, no longer useful, no longer loaded. | Delete and update any indexes that reference it. |

A pass that tries to avoid hard judgments — for example, by applying "update" to a page that really needs "replace" or "remove" — produces a half-cleaned doc tree and is worse than leaving the tree alone.

## Doc-cleaner vs. Doc-update (again)

| | Doc-cleaner | Doc-update |
|---|---|---|
| Trigger | Existing docs drifted or accumulated cruft | A new thing happened |
| Mode of work | Review → classify → edit or prune | Write one new thing |
| Scope | Sweeping or structural | Scoped and targeted |
| Owns new authoring? | No, except as a handoff | Yes |

Two signs you picked the wrong stage:

- You started in Doc-cleaner and find yourself writing a long new page — you are doing Doc-update's job; hand off.
- You started in Doc-update and find yourself editing five existing pages — you are doing Doc-cleaner's job; hand off.

## Structural governance checks

StructureGovernance mode handles the boring-but-important doc-system hygiene:

- Frontmatter present, correct, and consistent across the tree.
- INDEX catalogs accurate — every file listed, no dead links, description lines accurate.
- LOG.md files up to date where new content was added.
- Wikilinks (`[[other-page]]`) resolve to real files.
- Tags follow the repo's taxonomy (`area/ea`, `kind/wiki|doc|log`, `status/open|stable`).
- Date fields (`date_created`, `date_updated`) present and plausible.

This work is tedious in a good way: each check is small, each fix is local, and the cumulative effect is that the doc system stays navigable as it grows.

## Boundaries — when *not* to use Doc-cleaner

| Real need | Reach for |
|---|---|
| Documenting one concrete change, decision, or artifact | [[doc-update]] |
| Broad orientation | [[scout]] |
| Scoping a requested change | [[scope]] |
| Defining direction or planning execution | [[vision]] or [[architect]] |
| Applying a change or fixing a bug | [[implement]] |

## Related

- [[doc-update]]
- [[advisor]]
- source: `dot_config/ai_templates/skills/pa-sdlc/pa-doc-cleaner/SKILL.md`
