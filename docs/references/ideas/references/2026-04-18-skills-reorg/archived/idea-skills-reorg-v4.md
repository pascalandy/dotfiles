# Reorganizing Skills — v4 (2026-04-18)

> **Outcome (2026-04-18):** executed per [`plan-skills-reorg.md`](./plan-skills-reorg.md) on branch `reorg/skills-v4`. 45 skills moved, 9 stayed, 3 old buckets removed, 7 new buckets created. All 8 agent homes verified at 54 flat skills.

## Goal

v4 rescans `dot_config/ai_templates/skills/` against v3 and closes the audit loop: every skill on disk is confirmed present in the v3 target map, stubs/meta-skills are flagged, and open questions for Pascal are collected. No skills are moved in this pass — only `(.)` comments are added inline.

- `0o0o` are flags for Pascal, he need to improve them
- ( ) are comment reserved for Pascal
- (.) are comments added by this v4 audit pass

Scan scope: `fd SKILL.md` under `dot_config/ai_templates/skills/` → **54 SKILL.md files** across 4 physical buckets (`pa-sdlc/`, `meta/`, `specs/`, `utils/`). v4 maps **54 skills** across 8 logical buckets. Counts match 1:1.

Bucket order below follows a workflow arc: lifecycle spine → code-adjacent tooling → reasoning → memory → external research → transformation → visualization → creative output.

## SLL (Skill Logical Layout)

dot_config/ai_templates/skills/###{title}

### pa-sdlc/
- pa-idea (entrypoint) (. currently pa-sdlc/pa-idea — stay)
- pa-scout (. currently pa-sdlc/pa-scout — stay)
- pa-scope (. currently pa-sdlc/pa-scope — stay)
- pa-vision (. currently pa-sdlc/pa-vision — stay)
- pa-architect (. currently pa-sdlc/pa-architect — stay)
- pa-implement (. currently pa-sdlc/pa-implement — stay)
- pa-postmortem (. currently pa-sdlc/pa-postmortem — stay)
- pa-doc-update (. currently pa-sdlc/pa-doc-update — stay)
- pa-doc-cleaner (. currently pa-sdlc/pa-doc-cleaner — stay)

### devtools/
- coding-standard (. currently pa-sdlc/coding-standard — MOVE)
- coding-language (. currently pa-sdlc/coding-language — MOVE)
- pseudocode (. currently pa-sdlc/pseudocode — MOVE)
- ask-questions (. currently pa-sdlc/ask-questions — MOVE)
- grill-me-v2 (. currently specs/grill-me-v2 — MOVE)
- hunk-review (. currently utils/hunk-review — MOVE)
- eval-rubric (. currently specs/eval-rubric — MOVE)
- headless (. currently pa-sdlc/headless — MOVE; META-SKILL with ROUTER.md + references/{claude,codex,opencode,delegation})
- changelog (. currently specs/changelog — MOVE)
- commit (. currently utils/commit — MOVE)
- delegate-to-sub (. currently pa-sdlc/delegate-to-sub — MOVE)
- beads (. currently utils/beads — MOVE)

### think/
- thinking (by daniel) (. currently meta/thinking — MOVE)
- council-five-v1 (. currently specs/council-five-v1 — MOVE)
- council-five-v2 (. currently specs/council-five-v2 — MOVE)
- game-theory (. currently meta/game-theory — MOVE)

### knowledge/
- wiki-map (. currently pa-sdlc/wiki-map — MOVE)
- obsidian (. currently utils/obsidian — MOVE)
- single-skill-creator (. currently utils/single-skill-creator — MOVE)
- meta-skill-creator (. currently utils/meta-skill-creator — MOVE)
- qmd (. currently pa-sdlc/qmd — MOVE)
- byterover (. currently utils/byterover — MOVE)
- nia-docs (. currently utils/nia-docs — MOVE)
- map-filesystem-abstract (. currently utils/map-filesystem-abstract — MOVE)
- cass (. currently utils/cass — MOVE)

### web/
- agent-browser (. currently utils/agent-browser — MOVE)
- browser-use (. currently utils/browser-use — MOVE)
- tavily (. currently utils/tavily — MOVE)
- defuddle (. currently utils/defuddle — MOVE)
- last30days (. currently utils/last30days — MOVE)
- investigation (. currently meta/investigation — MOVE)
- trello (. currently utils/trello — MOVE)

### distill/
- distill (. currently pa-sdlc/distill — MOVE)
- distill-prompt (. currently pa-sdlc/distill-prompt — MOVE; META-SKILL with ROUTER.md + references/{extract-wisdom,follow-along-note,short-summary,summary-with-quotes})
- writer-sk (. currently utils/writer-sk — MOVE)
- simple-editor (. currently utils/simple-editor — MOVE)
- transcript-sk (. currently utils/transcript-sk — MOVE)
- liteparse (. currently meta/liteparse — MOVE)

### diagram/
- mermaid (. currently utils/mermaid — MOVE)
- plantuml-ascii (. currently utils/plantuml-ascii — MOVE)

### media/
- creative (. currently meta/creative — MOVE)
- marketing (. currently meta/marketing — MOVE)
- color-palette (. currently specs/color-palette — MOVE)
- nano-banana-sk (. currently utils/nano-banana-sk — MOVE)
- voxtral (. currently utils/voxtral — MOVE)

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
