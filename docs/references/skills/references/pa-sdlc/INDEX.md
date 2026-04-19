---
name: pa-sdlc
description: The Pascal Andy Software Development Lifecycle — eight `pa-*` skills that structure discovery, scoping, direction, architecture, implementation, and documentation
aliases:
  - pa-sdlc
  - sdlc
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-18
---

# pa-sdlc

<scope>
Load this wiki when the task involves choosing the right `pa-*` skill, sequencing them, or understanding why this repo separates "what exists" from "what is in play" from "where we're going" from "how we get there" from "how we build it" from "how we document it".

**pa-sdlc** stands for **Pascal Andy Software Development Lifecycle**. It is one operator's opinion about how to move from a vague request to a shipped and documented change, encoded as a family of eight skills under `dot_config/ai_templates/skills/pa-sdlc/`. This wiki is the narrative layer: when and why to reach for each stage, how they connect, and which failures each stage is designed to prevent.

For the authoritative entry points, read the `SKILL.md` files under the `pa-sdlc/` directory. This wiki points at them and explains how they fit together.
</scope>

<workflow>
1. Identify the stage the task is actually in, not the stage it feels like:
   - **Not sure what exists yet?** → [scout.md](references/scout.md)
   - **Know what exists, not sure what a change touches?** → [scope.md](references/scope.md)
   - **Know the touch surface, not sure the direction is worth it?** → [vision.md](references/vision.md)
   - **Direction settled, need an execution plan?** → [architect.md](references/architect.md)
   - **Plan is in hand, ready to build or something is broken?** → [implement.md](references/implement.md)
   - **Change is done, need to capture it?** → [doc-update.md](references/doc-update.md)
   - **Docs already exist, need maintenance?** → [doc-cleaner.md](references/doc-cleaner.md)
   - **Need a second opinion mid-task?** → [advisor.md](references/advisor.md)

2. Do not skip stages just because the next one feels easier. Skipping Scout before Scope means scoping without a map. Skipping Vision before Architect means planning execution for the wrong target. Every stage exists because the previous one was empirically necessary.

3. Every stage's own `SKILL.md` owns the authoritative details. This wiki is a summary and a connector — not a replacement.
</workflow>

<checklist>
Before starting any non-trivial change in this repo:
- the right stage was picked — the first tab in [stage-picker](#stage-picker) below is the fastest way
- the boundaries of that stage are respected (Scout does not own scoping, Architect does not own implementation, etc.)
- the output shape expected by the stage is produced before moving to the next one
- if stuck or uncertain, [advisor.md](references/advisor.md) is an option at any stage
</checklist>

<references>
Load only what the task needs:
- [scout.md](references/scout.md) — `pa-scout`: discovery and orientation, "what is this and where should I look"
- [scope.md](references/scope.md) — `pa-scope`: what is in play for a requested change, blast radius
- [vision.md](references/vision.md) — `pa-vision`: direction and end state, pressure-test the target
- [architect.md](references/architect.md) — `pa-architect`: execution design, vertical slices, plan stress-test
- [implement.md](references/implement.md) — `pa-implement`: bounded change application and root-cause repair
- [doc-update.md](references/doc-update.md) — `pa-doc-update`: document one concrete change, decision, or artifact
- [doc-cleaner.md](references/doc-cleaner.md) — `pa-doc-cleaner`: drift review, deduplication, structural doc hygiene
- [advisor.md](references/advisor.md) — `pa-advisor`: executor → advisor delegation via `claude -p`
</references>

---

> Content catalog. Every wiki page is listed here with a one-line summary.
> **Total pages:** 9 | **Last updated:** 2026-04-11

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/doc

| File | Description |
|------|-------------|
| `references/scout.md` | `pa-scout`: discovery entry point, four modes for orientation, onboarding, focused research, and archaeology |
| `references/scope.md` | `pa-scope`: scoping entry point, three modes for change surface, impact tracing, and artifact clarification |
| `references/vision.md` | `pa-vision`: direction entry point, three modes for direction check, alignment draft, and brief authoring |
| `references/architect.md` | `pa-architect`: execution planning entry point, four modes, vertical-slices planning principle |
| `references/implement.md` | `pa-implement`: execution entry point, change application and root-cause repair, TDD posture |
| `references/doc-update.md` | `pa-doc-update`: one bounded documentation job — change, rationale, or artifact |
| `references/doc-cleaner.md` | `pa-doc-cleaner`: documentation maintenance, three modes for drift, consolidation, and structure governance |
| `references/advisor.md` | `pa-advisor`: client-side executor→advisor delegation pattern via `claude -p` |

## Stage Picker

Pick the stage that answers your *current* question, not the stage that describes your overall goal.

| Current question | Stage | Typical output |
|---|---|---|
| "What is this?" | `pa-scout` | Concise map, next place to look |
| "What does this change touch?" | `pa-scope` | Primary scope + adjacent areas + risks |
| "Is this the right thing to build?" | `pa-vision` | Current state → end state → decisions |
| "How do we get there?" | `pa-architect` | Roadmap, slices, checkpoints |
| "Let's build it." / "It's broken." | `pa-implement` | Working code or explained fix |
| "What did we just change?" | `pa-doc-update` | One scoped doc update |
| "Are the docs still true?" | `pa-doc-cleaner` | Maintenance brief, actions |
| "Am I off track?" | `pa-advisor` | Enumerated strategic advice |

## The full lifecycle

A full non-trivial change moves through most of these stages in order, though not all of them are required for every task. The happy path:

```
pa-scout   →  pa-scope   →  pa-vision   →  pa-architect   →  pa-implement   →  pa-doc-update
   ↑                                            ↓
   └────────── pa-advisor (any time) ──────────┘
                                                                     ↓
                                                              pa-doc-cleaner (periodic)
```

Smaller tasks skip stages: a focused bug fix might go `pa-scope → pa-implement → pa-doc-update`. A doc cleanup job might be `pa-doc-cleaner` alone. A research question might be `pa-scout` alone. The sequence is a scaffold, not a mandate.

## Why the stages do not collapse

Every stage is a defense against one specific failure mode:

- **Scout defends against "starting work on the wrong surface"** — you thought the bug was in the auth layer and it turned out to be in the session store.
- **Scope defends against "underestimating blast radius"** — you changed one function and broke three callers you did not know existed.
- **Vision defends against "building the right thing poorly"** — you had a clear plan but the plan solved the wrong problem.
- **Architect defends against "planning by layer when you should plan by slice"** — you built the whole backend first, then discovered the UX did not match.
- **Implement defends against "coding without reproducing the failure"** — the fix made the test pass but did not address the defect.
- **Doc-update defends against "losing context"** — you shipped a decision and a month later nobody remembers why.
- **Doc-cleaner defends against "doc drift"** — every doc was true when it was written, and together they are now a contradictory mess.
- **Advisor defends against "silently committing to a wrong branch"** — you made a judgment call and nobody pressure-tested it before the work hardened.

Collapsing stages is fine when the failure mode they defend against is not present. Collapsing them *by habit* is the failure mode.

## Source material

This wiki absorbs `docs/about-pa-sdlc.md` (brainstorm). The brainstorm listed four stages (scout, scope, vision, architect). This wiki expands to the eight skills actually present under `dot_config/ai_templates/skills/pa-sdlc/` as of 2026-04-11.

## Related

- [[docs/INDEX.md]] — root catalog
- [[how-to-configure-opencode]] — skills and commands surface per agent
- [[how-ai-templates-are-distributed]] — how `pa-sdlc/` skills fan out to every agent home (note the Claude Code exception flagged there)
