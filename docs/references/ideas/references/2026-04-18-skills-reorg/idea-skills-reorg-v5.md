# Skills

## SLL (Skill Logical Layout)

dot_config/ai_templates/skills/{title}

### pa-sdlc
- 1) /pa-idea
- 2) /pa-scout
- 3) /pa-scope
- 4) /pa-vision
- 5) /pa-architect
- 6) /pa-implement
- 7) /pa-postmortem
- 8) /pa-doc-update
- 9) /pa-doc-cleaner

### devtools
- coding-standard
- coding-language
- grill-me-v2
- ask-questions
- pseudocode
- eval-rubric
- headless
- commit
- delegate-to-sub
- beads
- hunk-review
- changelog

### think
- thinking (by daniel)
- council-five-v1
- council-five-v2
- game-theory

### knowledge
- wiki-map
- obsidian
- single-skill-creator
- meta-skill-creator
- qmd
- byterover
- nia-docs
- map-filesystem-abstract
- cass

### web
- agent-browser
- browser-use
- tavily
- defuddle
- last30days
- investigation
- trello

### distill
- distill
- distill-prompt (META-SKILL with ROUTER.md + references/{extract-wisdom,follow-along-note,short-summary,summary-with-quotes})
- writer-sk
- simple-editor
- transcript-sk
- liteparse

### diagram
- mermaid
- plantuml-ascii

### media
- creative
- marketing
- color-palette
- nano-banana-sk
- voxtral

---

## unknown

n/a

---

## Q&A

- Q) `headless/` on disk is a meta-skill (ROUTER.md + `references/{claude,codex,opencode,delegation}`). In v3 it lands in `devtools/` as a single entry, which matches reality — just flagging so the migration preserves the whole tree (ROUTER.md + all 4 sub-dirs), not just `SKILL.md`.
- A) yes keep the whole metaskill

- Q) Same pattern for `distill-prompt/` — ROUTER.md + 4 sub-skill dirs (`extract-wisdom`, `follow-along-note`, `short-summary`, `summary-with-quotes`). Confirming the meta-skill stays intact as one unit under `distill/` in the new layout.
- A) yes keep the whole metaskill

- Q) `delegate-to-sub` lands in `devtools/`. 
- A) ok

- Q) `ask-questions` lands in `devtools/`. 
- A) ok

- Q) `council-five-v1` and `council-five-v2` both live in `think/`
- A) status quo, it's ok

---

## stats

- SKILL.md on disk: **54**
- Skills mapped in v4: **54**
- Drift: **0** (no orphans on disk, no phantom entries in v4)
- Meta-skills flagged: **2** (`headless`, `distill-prompt`) — both stay intact under their target bucket
- Physical buckets today: 4 (`pa-sdlc/`, `meta/`, `specs/`, `utils/`)
- Physical buckets after reorg: **8** (`pa-sdlc/`, `devtools/`, `think/`, `knowledge/`, `web/`, `distill/`, `diagram/`, `media/`)
- Per-bucket counts: pa-sdlc 9 · devtools 12 · think 4 · knowledge 9 · web 7 · distill 6 · diagram 2 · media 5
- Moves required: **45** (9 pa-sdlc skills stay, 45 skills move to a new bucket)
