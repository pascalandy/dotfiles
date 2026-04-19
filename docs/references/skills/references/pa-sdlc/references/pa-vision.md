---
name: Vision
description: `pa-vision` is the direction-setting entry point — use it to decide where the work is going before planning execution
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - pa-sdlc
---

Vision is the third stage of `pa-sdlc`. Load it with the explicit entry point `pa-vision`.

Use Vision when the question is "where are we going?" — before planning execution and before any implementation. Vision owns the pressure test for direction and the explicit alignment artifact that the later stages will plan against.

Source: `dot_config/ai_templates/skills/pa-sdlc/pa-vision/SKILL.md`.

## When to reach for Vision

| Situation | Why Vision |
|---|---|
| You are not sure the direction is worth pursuing. | DirectionCheck mode gives a go/revise/defer/stop recommendation. |
| The target state is implicit and you need to make it explicit before Architect starts. | AlignmentDraft mode is the default pre-planning artifact. |
| The direction is settled and needs a durable brief for future reference. | BriefAuthoring mode owns the PRD-style output. |

Vision is the highest-leverage stage for non-trivial work. The SKILL.md describes it as where "the agent brain-dumps its understanding" into a document covering current state, desired end state, and design decisions — so that a human can redirect the work before any code is planned.

## Three internal modes

| Mode | Owns | Use when |
|---|---|---|
| `DirectionCheck` | Direction pressure test | You need a go, revise, defer, or stop recommendation |
| `AlignmentDraft` | Default pre-planning artifact | You need the current state, end state, and pattern choices made explicit |
| `BriefAuthoring` | Durable brief or PRD | The direction is settled and the main job is packaging it cleanly |

Pick DirectionCheck when you are *not yet sure*. Pick AlignmentDraft as the default mode when a non-trivial change is about to enter Architect. Pick BriefAuthoring only when the direction is already settled — otherwise you are just packaging an opinion without pressure-testing it.

## Default output shape

A Vision artifact makes these easy to find:

1. **Request or decision** — what triggered this work.
2. **Current state** — an honest description of how things are today.
3. **Desired end state** — a concrete picture of the target.
4. **Key decisions or pattern choices** — the architectural choices this direction commits to.
5. **Success signals** — how you will know it worked.
6. **Risks and review points** — what could go wrong, where a human should be asked.
7. **Recommended next phase** — usually Architect.

The alignment draft mode produces the full seven-item artifact. DirectionCheck and BriefAuthoring collapse some items depending on context.

## The "brain surgery" moment

The SKILL.md calls out a specific pattern: during AlignmentDraft, the agent may propose a pattern that the team has moved away from (a legacy approach, a deprecated API, a discouraged shape). The human reviewing the draft performs "brain surgery" — redirecting the agent toward the correct architectural standard before Architect starts planning.

This redirection happens *explicitly*, in the Vision draft, not implicitly during Architect or Implement. The entire reason Vision exists as a separate stage is to make the redirection a first-class review point rather than something the human has to catch later in a code review.

## Boundaries — when *not* to use Vision

| Real need | Reach for |
|---|---|
| Understanding what exists today | [[scout]] |
| Identifying what is in play for a change | [[scope]] |
| Designing execution, structure, or sequencing | [[architect]] |
| Building the change or fixing a bug | [[implement]] |
| Documenting an already-made change, decision, or artifact | [[doc-update]] |
| Refreshing, deduplicating, or repairing existing docs | [[doc-cleaner]] |

If you find yourself designing signatures or laying out phases in a Vision output, stop — that is Architect. Vision ends at "which pattern do we commit to". Architect starts at "how do we execute that pattern".

## Vision vs. Architect

| | Vision | Architect |
|---|---|---|
| Question | "Where are we going?" | "How do we get there?" |
| Output | Current → end state + decisions | Roadmap + slices + checkpoints |
| Owns signatures? | No — only pattern choices | Yes — signatures, phases, interfaces |
| Success signal | Human says "yes, that is the right direction" | Human says "yes, that is a workable plan" |

The transition from Vision to Architect is a handoff. Vision says "we are going here". Architect says "we get there like this".

## Related

- [[scout]]
- [[scope]]
- [[architect]]
- [[advisor]]
- source: `dot_config/ai_templates/skills/pa-sdlc/pa-vision/SKILL.md`
