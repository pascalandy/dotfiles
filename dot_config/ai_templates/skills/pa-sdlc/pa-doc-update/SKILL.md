---
name: pa-doc-update
description: Concrete documentation entry point for a recent change, a settled rationale, or one current-state artifact. Use `pa-doc-update` when the documentation job is specific and bounded.
keywords: [pa-doc-update, doc-update, doc, change-capture, rationale-capture, artifact-documenter]
---

# Doc

Explicit entry point: `pa-doc-update`.

Use Doc for one bounded documentation job after the relevant change, decision, incident, or artifact already exists.

## Route

Load `references/ROUTER.md`.

## Use This When

- You need to capture what changed while context is fresh.
- You need to record why something was decided or why something happened.
- You need current-state documentation for one concrete artifact.

## Internal Modes

| Mode | Owns | Use when |
|---|---|---|
| `ChangeCapture` | Recent change documentation | The anchor is what changed and where that update belongs |
| `RationaleCapture` | Decision, incident, or lesson | The anchor is why something was chosen or what was learned |
| `ArtifactDocumenter` | One current-state artifact | The anchor is one module, page, workflow, board, or note set as it exists now |

## Boundaries

| If the real need is... | Use instead |
|---|---|
| stale-doc review, deduplication, frontmatter, routing, or doc governance | `pa-doc-cleaner` |
| broad orientation | `pa-scout` |
| scoping the change surface | `pa-scope` |
| defining the direction | `pa-vision` |
| planning or implementation | `pa-architect` or `pa-implement` |

## Default Output

Default to a concise documentation brief that covers:

1. documentation objective
2. primary target
3. evidence used
4. key content to capture
5. canonical placement or output shape
6. dependencies and unknowns
7. recommended next step

## Non-Goals

Doc does not own discovery, scoping, product definition, technical planning, implementation, or documentation maintenance.
