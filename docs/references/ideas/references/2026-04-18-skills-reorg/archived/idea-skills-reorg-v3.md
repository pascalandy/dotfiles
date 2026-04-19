# Reorganizing Skills — v3 (2026-04-18)

## Goal

rescans `dot_config/ai_templates/skills/` and closes gaps where v2 drifted: skills added since v2 are mapped, skills that no longer exist are flagged, and WIP stubs are confirmed. No skills are moved in this pass — only `(.)` comments are added inline so Pascal can decide.

- `0o0o` are flags for Pascal, he need to improve them
- ( ) are comment reserved for Pascal
- (.) are comments added by this v3 audit pass

## SLL (Skill Logical Layout)

dot_config/ai_templates/skills/###{title}

### pa-sdlc/
- pa-idea (entrypoint)
- pa-scout
- pa-scope
- pa-vision
- pa-architect
- pa-implement
- pa-postmortem
- pa-doc-update
- pa-doc-cleaner

### devtools/
- coding-standard
- coding-language
- pseudocode
- ask-questions
- grill-me-v2
- hunk-review
- eval-rubric
- headless
- changelog
- commit
- delegate-to-sub

### knowledge/
- wiki-map
- obsidian
- single-skill-creator
- meta-skill-creator
- qmd
- byterover
- nia-docs
- map-filesystem-abstract
- cass

### diagram/
- mermaid
- plantuml-ascii

### web/
- agent-browser
- browser-use
- tavily
- defuddle
- last30days
- investigation

### doc/
- liteparse

### ext-int/
- beads
- trello
- voxtral

### think/
- thinking (by daniel)
- council-five-v1
- council-five-v2
- game-theory

### distill/
- distill
- distill-prompt
- writer-sk
- simple-editor
- transcript-sk

### media/
- creative
- marketing
- color-palette
- nano-banana-sk

---

## unknown

placeholder

---

## Q&A

- Q) The current physical layout uses 4 top-level buckets (`pa-sdlc/`, `meta/`, `specs/`, `utils/`), while v2 proposes 13 logical buckets. Is v3 still a *logical* map (no physical move) or do you want the layout section to also describe the planned physical reorg?
- A) physical reorg
---

## stats

tbd