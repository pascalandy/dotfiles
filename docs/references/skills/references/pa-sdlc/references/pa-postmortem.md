---
name: pa-postmortem
description: Retrospective entry point — session review, blameless incident review, or durable feedback capture after work is done
tags:
  - area/ea
  - kind/doc
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-18
date_updated: 2026-04-18
---

# pa-postmortem

**Entry point:** `pa-postmortem`
**Source:** `dot_config/ai_templates/skills/pa-sdlc/pa-postmortem/SKILL.md`

## What it does

Preserve what is worth remembering from completed work. Routes to one of three retrospective shapes and always exports the final artifact to `docs/references/ideas/references/YYYY-MM-DD-slug/postmortem-slug.md`.

## When to use

- A conversation or session ended and needs reverse-engineering into memory, lessons, fixes, and feedback.
- A real operational or delivery incident needs a blameless review with impact, timeline, causes, and follow-ups.
- Completed work, a fix, or a decision is done and only the transferable lessons should survive.

## Modes

| Mode | Use when |
|---|---|
| `SessionReview` | Reverse-engineer a conversation or work session |
| `IncidentReview` | Blameless incident review (standard, quick, or 5 Whys) |
| `FeedbackCapture` | Durable lessons from a completed fix, decision, or piece of work |

## Don't use for

- Capturing a rough idea → `pa-idea`
- Documenting a shipped change → `pa-doc-update`
- Doc drift, dedup, or governance → `pa-doc-cleaner`
- Planning or implementation → `pa-architect` or `pa-implement`
