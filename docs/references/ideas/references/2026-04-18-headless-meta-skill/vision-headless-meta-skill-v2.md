---
name: Vision — headless meta-skill (v2)
description: DirectionCheck on packaging headless-delegation (PTY orchestrator) + headless-claude/codex/opencode (flag references) as a single meta-skill built via meta-skill-creator
tags:
  - area/skills
  - kind/vision
  - status/open
date_created: 2026-04-18
date_updated: 2026-04-18
---

# Vision — headless meta-skill (v2)

## Request Or Decision

Decide whether to package four existing standalone skills into one router-based meta-skill named `headless`, with **`delegation` as the core sub-skill** (PTY orchestration, permission posture, workdir hygiene) and **`claude` / `codex` / `opencode` as three flag-reference sub-skills** that `delegation` cites. Follow the `meta-skill-creator/SKILL.md` contract exactly: one root `SKILL.md`, one `ROUTER.md`, every sub-skill renamed to `MetaSkill.md`.

This revises v1. v1 treated `headless-delegation` as an external orchestrator that links to three peer primitives. v2 treats `delegation` as the **beating heart of the collection** — the PTY / permission / workdir logic *is* the capacity the user reaches for — and demotes the three CLI skills to reference material that `delegation` dispatches to for flag detail.

## Problem Or Opportunity

Four skills in `utils/` cover one capacity:

- `headless-delegation` owns the pty matrix, permission posture, workdir refusal list, and background/foreground recipes. This is the **core capacity**.
- `headless-claude`, `headless-codex`, `headless-opencode` are near-duplicate primitives documenting the flag surface of each CLI. Each is a lookup table.

Symptoms today:

- Four top-level entries in the skill list; three of them are flag references that only make sense when the user already decided to delegate.
- `delegation` cites the three primitives by path, creating a cross-reference tax every time a primitive moves, renames, or grows a new flag.
- The three `references/UPDATE.md` files share 80% of their shape; drift is inevitable.
- A new CLI (droid, gemini-cli, pi) means **two** new skills — one primitive + one orchestrator update — instead of one structural addition.

The opportunity: collapse to one registered skill (`headless`) where the router dispatches on intent. "I want to delegate work" → `delegation/MetaSkill.md`. "Show me Claude's flags" → `claude/MetaSkill.md`. Future CLI = one new sub-skill directory + one router row. `delegation`'s cross-references become relative paths inside the same collection, not cross-skill paths.

## Who It Serves

- **Primary:** the user who types "use headless-delegation with codex to ..." and expects the PTY pattern to fire. After v2, the same phrase still works — the router aggregates delegation's strict trigger into the collection's `USE WHEN`.
- **Secondary:** the user who types `headless-claude` out of muscle memory expecting a flag reference. Router dispatches to `claude/MetaSkill.md` with byte-identical content.
- **Tertiary:** future CLIs. Adding `headless-droid` becomes one subdirectory + one router row + one line in delegation's matrix — no new top-level skill, no new cross-reference surface.
- **Quaternary:** `meta-skill-creator` itself — this migration is a real-world pressure test of its contract on an asymmetric collection (one heavy core + three thin references), unlike the symmetric examples it documents today.

## Why Now

- `headless-delegation` just landed (commit `c0e988d`) and the cross-reference block is fresh. Rewriting three path literals into one relative scheme is cheap now, expensive later.
- `meta-skill-creator` is stable and documents the exact scanner-hygiene rename (`SKILL.md` → `MetaSkill.md`). No contract invention needed.
- No heavy content under any of the four `references/` trees — the biggest is `headless-claude/SKILL.md` at 14k, still under the "one `MetaSkill.md` is enough" threshold.
- The asymmetric shape (one core, three references) is unusual enough to be worth getting right before a second meta-skill copies the pattern.

## Anti-Goals

- **No content rewrite.** Every `SKILL.md` body migrates verbatim to `MetaSkill.md`. No flag-table edits, no permission-matrix revisions, no trigger-phrase tuning. If migration needs a content change, stop and split it into a separate pass.
- **No rename of the user-facing trigger phrases.** `use headless-delegation with <cli> to <task>`, `headless-claude`, `headless-codex`, `headless-opencode` all keep working. The router aggregates all four keyword sets into one `USE WHEN`.
- **No merge of distinct CLI domains.** Claude print-mode, Codex exec, OpenCode run stay as three separate flag-reference sub-skills. The meta-skill is a directory layout change, not a content merge.
- **No promotion of `delegation` to the root `SKILL.md`.** The root stays as a thin collection file per the meta-skill-creator contract. `delegation` is a sub-skill, equal in file shape to the other three, unequal only in content weight.
- **No new capability.** v2 is layout + rename. Feature work (new CLI support, new permission mode) is out of scope.

## Success Signals

1. Scanner registers exactly one new skill (`headless`). The four old top-level entries (`headless-delegation`, `headless-claude`, `headless-codex`, `headless-opencode`) are gone from the skill list.
2. User typing `use headless-delegation with codex to ...` triggers the meta-skill, router dispatches to `delegation/MetaSkill.md`, and the bash command emitted is byte-identical to what pre-migration `headless-delegation` produced.
3. User typing `headless-claude` triggers the meta-skill, router dispatches to `claude/MetaSkill.md`, and the flag reference rendered is byte-identical to pre-migration.
4. `delegation/MetaSkill.md`'s "Cross-references" block uses relative paths (`../claude/MetaSkill.md`, `../codex/MetaSkill.md`, `../opencode/MetaSkill.md`) — no cross-skill path literals.
5. A repo-wide grep for `headless-claude/`, `headless-codex/`, `headless-opencode/`, `headless-delegation/` returns zero live references (only git history mentions).
6. Adding a hypothetical `droid` sub-skill requires one `references/droid/MetaSkill.md` + one router row + one line added to `delegation/MetaSkill.md`'s matrix — no changes elsewhere.

## Trade-Offs And Risks

| Trade-off | Lean |
|---|---|
| Asymmetric sub-skill weights (delegation 9.6k vs. opencode 4.9k) — does the meta-skill pattern fit? | Yes. The pattern constrains shape (one `MetaSkill.md` per sub-skill), not size. The contract tolerates asymmetry. |
| Four sub-skills vs. three + delegation at root | Four. Keeping delegation as a sub-skill preserves the "additive scaling" rule: a new CLI is one directory, not a delegation edit. |
| One-shot migration vs. staged commits | One-shot. Halfway states (delegation migrated, primitives not, or vice versa) break cross-references and leave the scanner in an inconsistent state. |
| Progressive-disclosure win vs. migration cost | Migration is mechanical (move + rename + relink). Cost is one-shot. Win is permanent and compounds with every new CLI. |

Risks to watch:

- **Trigger regression on the strict delegation phrase.** `headless-delegation`'s `USE WHEN` is "only when the user explicitly says `use headless-delegation with <cli> to ...`". If the router's aggregated `USE WHEN` dilutes that strictness, delegation could fire on loose triggers. **Mitigation:** keep the strict phrase literal in the router's routing-table row for delegation, not just in the aggregate `USE WHEN` line.
- **Cross-reference rot outside the collection.** Anything in the repo that links to `utils/headless-*/SKILL.md` (docs, other skills, LOG entries) 404s after migration. **Mitigation:** `rg "headless-(claude|codex|opencode|delegation)/"` before the commit; rewrite every hit in the same commit.
- **Scanner double-index from a missed rename.** If any sub-skill file stays `SKILL.md` instead of `MetaSkill.md`, the scanner registers it as a top-level skill — re-creating the exact problem we're solving. **Mitigation:** `fd "^SKILL\.md$" references/` under the new meta-skill should return nothing except the collection root.
- **Delegation's internal path references break.** Delegation's body cites `headless-claude/SKILL.md` etc. These paths must become `../claude/MetaSkill.md` — both the file name and the `../` prefix change. **Mitigation:** single sed pass + visual diff before commit.
- **The collection `SKILL.md` gets too thin to be useful.** Per meta-skill-creator, the root is a collection with "What's Included" and invocation scenarios. If the four sub-skills are listed without context, the root becomes a bare index. **Mitigation:** the collection `SKILL.md` should briefly explain *why delegation is the core* and *why the three CLI references exist to serve it* — one paragraph, not a rewrite.

## Recommendation

**Proceed — revise scope from v1 to reflect delegation as the core sub-skill.**

v1 correctly identified the consolidation opportunity but framed `headless-delegation` as external. v2 corrects the frame: delegation is the heart of the collection, and the three CLI skills are its flag-lookup tables. This changes three concrete things from v1:

1. **Sub-skill count: 4, not 3.** `delegation/` joins `claude/`, `codex/`, `opencode/` under `references/`.
2. **Router: 4 rows, not 3.** The first row routes the strict `use headless-delegation with <cli> to ...` phrase to `delegation/MetaSkill.md`.
3. **Cross-references: relative, not cross-skill.** Delegation's "flag details" citations become `../claude/MetaSkill.md` style, not `headless-claude/SKILL.md`.

Target structure:

```
dot_config/ai_templates/skills/pa-sdlc/headless/
├── SKILL.md                              # Collection — thin, bridges to ROUTER
└── references/
    ├── ROUTER.md                         # 4-row dispatch table
    ├── delegation/                       # Core sub-skill (PTY, permissions, workdir)
    │   ├── MetaSkill.md
    │   └── references/
    │       └── UPDATE.md
    ├── claude/                           # Flag reference
    │   ├── MetaSkill.md
    │   └── references/
    │       └── UPDATE.md
    ├── codex/
    │   ├── MetaSkill.md
    │   └── references/
    │       └── UPDATE.md
    └── opencode/
        ├── MetaSkill.md
        └── references/
            └── UPDATE.md
```

Router table (sketch, finalized in architect phase):

| Request Pattern | Route To |
|---|---|
| use headless-delegation with claude\|codex\|opencode to ... (strict literal) | `delegation/MetaSkill.md` |
| headless-claude, claude -p, claude --print, claude --permission-mode | `claude/MetaSkill.md` |
| headless-codex, codex exec, codex --full-auto, codex --yolo | `codex/MetaSkill.md` |
| headless-opencode, opencode run, opencode --agent | `opencode/MetaSkill.md` |

Collection `SKILL.md` contract (per `meta-skill-creator`):

- Frontmatter: `name: headless`, aggregated `description` with every trigger from all four sub-skills.
- Body: one paragraph framing ("delegation is the core; the three CLI sub-skills are flag references delegation dispatches to"), a "What's Included" table, and the mandatory bridge line: `Load references/ROUTER.md to determine which sub-skill handles this request.`
- No duplication of delegation's PTY matrix or any CLI's flag table in the root.

After migration, in the same commit:

- Delete `utils/headless-delegation/`, `utils/headless-claude/`, `utils/headless-codex/`, `utils/headless-opencode/`.
- Update `delegation/MetaSkill.md`'s "Cross-references" to relative sibling paths.
- `rg "headless-(claude|codex|opencode|delegation)/"` across the repo and rewrite every live hit. Git history links are fine to leave.
- Verify: `fd "^SKILL\.md$" dot_config/ai_templates/skills/pa-sdlc/headless/references/` returns nothing.

## Recommended Next Phase

`pa-architect` — produce the concrete migration plan:

1. Exact file-move map (source path → destination path) for every file under the four old directories.
2. The full contents of the new root `SKILL.md` and `ROUTER.md` (not a sketch).
3. The sed / manual edits needed inside `delegation/MetaSkill.md` to rewrite `headless-{claude,codex,opencode}/SKILL.md` references into `../{claude,codex,opencode}/MetaSkill.md`.
4. A complete list of repo-wide cross-references that must be rewritten, gathered from one `rg` pass.
5. Decision: single commit vs. staged (delegation-first, then primitives). Recommendation default is single-commit, but architect validates.

Do not jump to `pa-implement` until architect confirms the cross-reference sweep is complete and the rename produces zero scanner ambiguity.
