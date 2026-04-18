---
name: Vision — headless meta-skill
description: DirectionCheck on consolidating headless-claude, headless-codex, headless-opencode into one router-based meta-skill
tags:
  - area/skills
  - kind/vision
  - status/open
date_created: 2026-04-18
date_updated: 2026-04-18
---

# Vision — headless meta-skill

## Request Or Decision

Decide whether to consolidate the three existing standalone skills `headless-claude`, `headless-codex`, `headless-opencode` into a single router-based meta-skill `headless` at `dot_config/ai_templates/skills/utils/headless/`, following the pattern documented in `meta-skill-creator/SKILL.md` and mirroring the cross-reference shape used by `headless-delegation`.

## Problem Or Opportunity

Three near-identical primitives sit side by side in `utils/`. Each teaches the same shape of task — "how to run CLI X in non-interactive mode" — but the scanner indexes them as three separate skills. Symptoms:

- Three entries in `/help` and in the skill list, adding noise that grows linearly as more CLIs are added (droid, gemini-cli, etc.).
- Shared concerns (permission posture, PTY rules, workdir hygiene) already abstracted once into `headless-delegation` but duplicated in the primitives' bodies.
- The three `references/UPDATE.md` files are functionally copies of one another; maintenance drifts across them.

The opportunity is a single entry point `headless` that routes to a per-CLI `MetaSkill.md` via a small router, preserving all current content verbatim while giving future CLIs a clean slot (one new directory + one new router row).

## Who It Serves

- **Primary:** the user driving Claude Code / OpenCode / Codex who invokes `headless-<cli>` by muscle memory and currently sees three near-duplicate skill descriptions.
- **Secondary:** `headless-delegation` itself — its "Cross-references" block cites three paths today; one collapses the dependency surface.
- **Tertiary:** future CLIs. Adding `headless-droid` or `headless-gemini` becomes one directory instead of a new top-level skill.

## Why Now

- `headless-delegation` was just landed (commit `c0e988d`) and already points at the three primitives — the cross-reference cost of consolidation is paid once, right now, while the orchestrator is fresh.
- `meta-skill-creator` is stable and already documents the exact pattern (Collection → `ROUTER.md` → `MetaSkill.md` with scanner-hygiene rename). No invention required.
- None of the three `references/` directories hold anything heavy — each has only a 1.3k `UPDATE.md`. Migration is a rename + a move, not a rewrite.

## Anti-Goals

- **No content rewrite.** The three `SKILL.md` bodies migrate verbatim to `MetaSkill.md`. If the migration requires editing flag tables or permission matrices, stop and reconsider — that is a separate maintenance pass.
- **Not a rename of `headless-delegation`.** The orchestrator stays where it is and keeps its name. Only its cross-reference paths update.
- **No breakage of the strict trigger phrases.** `headless-claude`, `headless-codex`, `headless-opencode` must keep working as the user types them — the router's `USE WHEN` aggregates all three keyword sets.
- **No merge of distinct domains.** Claude print-mode, Codex exec, and OpenCode run stay as three separate sub-skills. The meta-skill is a directory layout change, not a content merge.

## Success Signals

1. Scanner registers exactly one new skill (`headless`) and the three old top-level entries are gone.
2. User typing "headless-claude" still loads the same content they saw before (via router dispatch), verified by reading the rendered sub-skill.
3. `headless-delegation`'s "Cross-references" section points at one path (`headless/references/<cli>/MetaSkill.md`) instead of three.
4. A new CLI can be added as a single directory + one row in `ROUTER.md`, no SKILL.md surgery.
5. No change to delegated-agent behavior when `headless-delegation` orchestrates a run — the primitives return the same flag tables and examples.

## Trade-Offs And Risks

| Trade-off | Lean |
|---|---|
| Progressive-disclosure win vs. migration cost | Migration is mechanical (move + rename), cost is one-shot. Win is permanent. |
| One entry point vs. three direct entries | User already types the CLI-specific phrase — the router dispatches invisibly. Net UX: same. Net noise: lower. |
| Sub-skill size — is 14k `headless-claude` too big for one `MetaSkill.md`? | Within the guide's "one `MetaSkill.md` is enough" threshold. The 1.3k `UPDATE.md` nests cleanly under `references/`. No further decomposition warranted. |

Risks to watch:

- **Trigger regression.** If the router's `USE WHEN` doesn't aggregate all three keyword sets, one of the three phrases stops firing. Mitigation: copy `description` fields verbatim into the aggregate before editing.
- **Cross-reference rot.** Anything outside `headless-delegation` that links to `utils/headless-claude/` will 404. Grep the repo once before migration and update in the same commit.
- **Scanner double-index.** If `MetaSkill.md` is left as `SKILL.md` in any sub-skill, the scanner registers it as a top-level skill — the exact problem we're solving. Strict adherence to the `MetaSkill.md` rename is the single must-not-miss step.

## Recommendation

**Proceed — revise scope to a mechanical migration only.**

The consolidation is the right shape: three near-duplicate primitives, one stable orchestrator already abstracting the shared concerns, one documented meta-skill pattern to apply. Do not treat this as an opportunity to edit flag tables or permission matrices — keep the content byte-identical and make the migration auditable.

Target structure:

```
dot_config/ai_templates/skills/pa-sdlc/headless
├── SKILL.md                              # collection + "Load references/ROUTER.md" bridge
└── references/
    ├── ROUTER.md                         # 3-row dispatch table
    ├── headless-delegation

    ├── headless-claude/
    ├── headless-codex/
    └── headless-opencode/
```

Router table (sketch, to be finalized in architect phase):

| Request Pattern | Route To |
|---|---|
| headless-claude, claude -p, claude print mode, claude --permission-mode | `claude/MetaSkill.md` |
| headless-codex, codex exec, codex --full-auto, codex --yolo | `codex/MetaSkill.md` |
| headless-opencode, opencode run, opencode --agent | `opencode/MetaSkill.md` |

After migration:

- Delete the three old `utils/headless-{claude,codex,opencode}/` directories in the same commit.
- Update `headless-delegation/SKILL.md` "Cross-references" block to point at the three `MetaSkill.md` paths under `headless/references/`.
- Grep the repo for any `headless-claude/`, `headless-codex/`, `headless-opencode/` string literals and rewrite them.

## Recommended Next Phase

`pa-architect` — produce the concrete migration plan: file-move map, exact router contents, cross-reference update list, and the single-commit vs. staged-commit decision. Do not jump to `pa-implement` until the architect phase confirms no in-flight references break.
