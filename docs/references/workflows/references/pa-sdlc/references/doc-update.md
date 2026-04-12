---
name: Doc-update
description: `pa-doc-update` is the concrete documentation entry point — use it for one bounded documentation job after the change, decision, or artifact already exists
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - pa-sdlc
---

Doc-update is the sixth stage of `pa-sdlc`. Load it with the explicit entry point `pa-doc-update`.

Use Doc-update when a specific thing has already happened — a change was made, a decision was reached, an incident occurred, an artifact exists — and the job is to capture it in documentation before the context fades.

Source: `dot_config/ai_templates/skills/pa-sdlc/pa-doc-update/SKILL.md`.

## When to reach for Doc-update

| Situation | Mode |
|---|---|
| A change was just made and needs capturing while context is fresh. | `ChangeCapture` |
| A decision was reached, or an incident happened, or a lesson was learned. | `RationaleCapture` |
| One current-state artifact (module, page, workflow, board, note set) needs documentation. | `ArtifactDocumenter` |

Doc-update is always **anchored to something that already exists**. If the thing does not exist yet — if the change has not been made, the decision has not been reached, the artifact has not been built — you are in the wrong stage. Go back to Implement (for the change), Vision (for the decision), or Architect (for the artifact plan).

## Three internal modes

| Mode | Owns | Use when |
|---|---|---|
| `ChangeCapture` | Recent change documentation | The anchor is what changed and where that update belongs |
| `RationaleCapture` | Decision, incident, or lesson | The anchor is why something was chosen or what was learned |
| `ArtifactDocumenter` | One current-state artifact | The anchor is one module, page, workflow, board, or note set as it exists now |

## Default output shape

A Doc-update brief covers:

1. **Documentation objective** — what the doc is for.
2. **Primary target** — the specific thing being documented.
3. **Evidence used** — files read, logs reviewed, conversations cited.
4. **Key content to capture** — the load-bearing facts and claims.
5. **Canonical placement or output shape** — where the doc lives, what format it takes.
6. **Dependencies and unknowns** — other docs this one links to, gaps this doc cannot close.
7. **Recommended next step** — usually a commit, a PR, or a follow-up Doc-cleaner pass.

The canonical-placement item is important. In this repo, documentation lives under `docs/` in the [[wiki-map]] shape (INDEX + references + LOG). Doc-update outputs should respect that shape rather than scatter content across arbitrary locations.

## Doc-update vs. Doc-cleaner

This is the most commonly confused pair in the `pa-sdlc` family.

| | Doc-update | Doc-cleaner |
|---|---|---|
| Trigger | A specific new thing happened | An existing doc system has drifted or accumulated cruft |
| Scope | One artifact, one decision, one change | The whole doc surface, or a subtree of it |
| Owns fresh authoring? | Yes — this is mostly fresh writing | No — mostly review, merge, prune, repair |
| Output size | Small, scoped, targeted | Can be large, structural, sweeping |

If you find yourself editing multiple existing docs during a Doc-update pass, stop. That is Doc-cleaner's job. Doc-update writes one thing.

Conversely, if you find yourself authoring large new pages during a Doc-cleaner pass, stop. That is Doc-update's job. Doc-cleaner maintains.

## Boundaries — when *not* to use Doc-update

| Real need | Reach for |
|---|---|
| Stale-doc review, deduplication, frontmatter, routing, or doc governance | [[doc-cleaner]] |
| Broad orientation | [[scout]] |
| Scoping the change surface | [[scope]] |
| Defining the direction | [[vision]] |
| Planning or implementation | [[architect]] or [[implement]] |

## Related

- [[doc-cleaner]]
- [[implement]]
- source: `dot_config/ai_templates/skills/pa-sdlc/pa-doc-update/SKILL.md`
