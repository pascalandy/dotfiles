# Reorganizing Skills — v2 (2026-04-18)

## Goal

rescans `dot_config/ai_templates/skills/` and closes gaps where v1 drifted: skills added since v1 are mapped, skills that no longer exist are removed, and WIP stubs are flagged.

- `0o0o` are flags for Pascal, he need to improve them
- ( ) are comment reserved for Pascal

## SLL (Skill Logical Layout)

### pa-sdlc/
- pa-idea (entrypoint)
- pa-scout
- pa-scope
- pa-vision
- pa-architect
- pa-implement
- pa-postmortem
- pa-doc-update
  - changelog
- pa-doc-cleaner

### dev-tooling/
- coding-standard
- coding-language
- pseudocode
- ask-questions (alt grill-me-v2)
- hunk-review
- eval-rubric (for reviews)
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
- office-docs (draft)
- liteparse

### integrations/
- beads
- trello

### think/
- thinking (by daniel)
- council
- five-council
- game-theory (0o0o)

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

`cm`, `shorthand-interpreter` get deleted, finished, or left as scaffolds?

---

## Counts

- Real skills mapped: 59
- WIP stubs excluded: 3
- Top-level buckets: 13 (entrypoint, dev, knowledge, web, system, harness, doc, integrations, think, diagram, distill, media) — 12 plus `dev` has two subfolders
