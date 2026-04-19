---
name: pa-idea
description: Idea-capture entry point — write down a rough idea into `docs/references/ideas/` while preserving voice and language
tags:
  - area/ea
  - kind/doc
  - status/open
  - bucket/pa-sdlc
date_created: 2026-04-18
date_updated: 2026-04-18
---

# pa-idea

**Entry point:** `pa-idea`
**Source:** `dot_config/ai_templates/skills/pa-sdlc/pa-idea/SKILL.md`

## What it does

Capture a rough idea as a durable artifact under `docs/references/ideas/references/YYYY-MM-DD-slug/idea-slug.md`. Small edits for clarity only — keeps the author's voice, original language (including mixed French/English), and intent intact.

## When to use

- You have a raw thought that should be written down and stored for future reference.
- The input is a brain-dump, not a plan or a decision.

## Workflow

1. Resolve `entry_slug`, `export_dir`, `export_file` before editing any text.
2. `simple-editor` pass — fix typos, remove duplicates, organize paragraphs. No voice change.
3. `writer-sk` pass — clarity and concision.
4. Write the final text to the resolved export path.
5. Return the folder path, file path, and final slug.

## Don't use for

- Deciding if the idea is worth pursuing → `pa-vision`
- Scoping or planning around the idea → `pa-scope` or `pa-architect`
- Capturing a shipped change → `pa-doc-update`
- Capturing lessons from completed work → `pa-postmortem`
