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

### dev-tooling/
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

### unknown/


- `shorthand-interpreter` → directory is empty (. confirmed empty scaffold — delete or finish)
- `mermaid-og` → already deleted from disk on 2026-04-18 (. v2 entry is stale)
- `office-docs` → no folder exists yet (. v2 marked it draft; confirm intent — create or drop)

## Q&A

1. `commit` and `delegate-to-sub` were missing from v2 entirely. Do you want them under `dev-tooling/`, or do they belong elsewhere (e.g. `commit` next to `changelog` in a future `release/` bucket, `delegate-to-sub` in `system/`)?
2. `changelog` is listed in v2 as a child of `pa-doc-update`, but on disk it lives at `specs/changelog/`. Do you want it nested under `pa-doc-update/` physically, or kept standalone and only logically grouped?
3. Should `mermaid-og` simply be removed from the v3 layout now that the directory is gone, or do you want to keep a placeholder line as a reminder?
4. `office-docs` — keep as a planned slot, or drop until the skill actually exists?
5. For `cm` and `shorthand-interpreter`: delete the scaffolds, or are these planned skills you want to revive?
6. The current physical layout uses 4 top-level buckets (`pa-sdlc/`, `meta/`, `specs/`, `utils/`), while v2 proposes 13 logical buckets. Is v3 still a *logical* map (no physical move) or do you want the layout section to also describe the planned physical reorg?

---

## stats

- Real skills on disk: 56 (54 with `SKILL.md` or content + 2 scaffolds: `cm`, `shorthand-interpreter`)
- v2 entries that no longer exist on disk: 2 (`mermaid-og`, `office-docs`)
- Skills on disk missing from v2: 2 (`commit`, `delegate-to-sub`)
- WIP stubs flagged: 2 (`cm`, `shorthand-interpreter`)
- Top-level buckets: 13 (entrypoint, dev, knowledge, web, system, harness, doc, integrations, think, diagram, distill, media) — 12 plus `dev` has two subfolders
