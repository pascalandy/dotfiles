---
name: pa-doc-update
description: Documentation entry point — capture one concrete change, decision, or artifact before context fades
tags:
  - area/ea
  - kind/doc
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-11
date_updated: 2026-04-18
---

# pa-doc-update

**Entry point:** `pa-doc-update`
**Source:** `dot_config/ai_templates/skills/pa-sdlc/pa-doc-update/SKILL.md`

## What it does

Write or update one bounded piece of documentation anchored to something that already exists — a shipped change, a settled decision, or one current-state artifact.

## When to use

- A change was just made and needs capturing while context is fresh.
- A decision was reached, or an incident happened, or a lesson was learned.
- One current-state artifact (module, page, workflow, board, note set) needs its doc.

## Modes

| Mode | Use when |
|---|---|
| `ChangeCapture` | Recent change, post-ship docs, release notes, changelog sync |
| `RationaleCapture` | ADR, decision record, incident review, lessons learned |
| `ArtifactDocumenter` | One module, page, workflow, or note set documented as it is today |

## Don't use for

- Drift review, dedup, frontmatter, routing, doc governance → `pa-doc-cleaner`
- Retrospectives or durable lesson capture → `pa-postmortem`
- Broad orientation → `pa-scout`
- Scoping a change → `pa-scope`
- Planning or implementation → `pa-architect` or `pa-implement`
