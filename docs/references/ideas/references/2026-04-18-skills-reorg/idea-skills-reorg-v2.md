# Reorganizing Skills — v2 (2026-04-18)


## Goal

rescans `dot_config/ai_templates/skills/` and closes gaps where v1 drifted: skills added since v1 are mapped, skills that no longer exist are removed, and WIP stubs are flagged.

0o0o are flags for Pascal, he need to  are note for Pascal

## Proposed Layout v2

### entrypoint/
- pa-idea

### dev/

**pa-sdlc**
- pa-scout
- pa-scope
- pa-vision
- pa-architect
- pa-implement
- pa-postmortem
- pa-doc-update
  - changelog
- pa-doc-cleaner

**dev-tools**
- coding-standard
- coding-language
- pseudocode
- ask-questions
  - grill-me-v2
- hunk-review
- eval-rubric
- commit
- headless-claude
- headless-codex
- headless-opencode

### knowledge/
- wiki-map
- obsidian
- qmd
- byterover
- nia-docs
- map-filesystem-abstract
- cass

### web/
- agent-browser
- browser-use
- tavily
- defuddle
- last30days
- investigation

### system/
- single-skill-creator
- meta-skill-creator

### harness/
- delegate
  - pa-advisor

### doc/
- liteparse

### integrations/
- beads
- trello

### think/ (0o0o)
- thinking
- council
- five-council

### diagram/
- mermaid
- mermaid-og
- plantuml-ascii

### distill/
- distill
- distill-prompt
- writer-sk
- simple-editor
- transcript-sk

### media/
- creative
- marketing
- ContentAnalysis
- color-palette
- voxtral
- nano-banana-sk

---

## Open questions (decide before architect phase)

1. **`superpowers` placement** — it's a router/workflow collection. Put in `entrypoint/` (alongside `pa-idea`) or demote to `dev/sdlc/`?
2. **`pa-doc-cleaner` placement** — v1 put it in `dev-tools`; v2 moves it next to `pa-doc-update` under `sdlc` since both are doc-maintenance. Confirm.
3. **`defuddle` placement** — v1 put it in `system/`; v2 moves to `web/` (it's a web-page reader). Confirm.
4. **`write-down-postmortem` pairing** — v2 nests it under `postmortem` in `think/`. Alternative: move both to a dedicated `postmortem/` top-level.
5. **WIP stubs** — do `game-theory`, `cm`, `shorthand-interpreter` get deleted, finished, or left as scaffolds?

---

## Counts

- Real skills mapped: 59
- WIP stubs excluded: 3
- Top-level buckets: 13 (entrypoint, dev, knowledge, web, system, harness, doc, integrations, think, diagram, distill, media) — 12 plus `dev` has two subfolders
