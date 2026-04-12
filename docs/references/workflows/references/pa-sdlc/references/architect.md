---
name: Architect
description: `pa-architect` is the execution-design entry point — use it to turn settled direction into a plan
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - pa-sdlc
---

Architect is the fourth stage of `pa-sdlc`. Load it with the explicit entry point `pa-architect`.

Use Architect after the direction is settled (Vision is done) and before implementation starts (Implement has not begun). Architect owns the execution plan: phases, slices, spikes, and the stress test for a plan that already exists.

Source: `dot_config/ai_templates/skills/pa-sdlc/pa-architect/SKILL.md`.

## When to reach for Architect

| Situation | Why Architect |
|---|---|
| A meaningful plan already exists and needs a readiness review. | PlanStressTest mode hardens it before implementation. |
| One blocking unknown would make any plan fake until it is resolved. | DecisionSpike mode isolates the unknown and answers it first. |
| The main blocker is the target shape or boundary design, not sequencing. | StructuralDesign mode owns the target shape. |
| The direction is settled and the default next step is to plan execution. | RoadmapDesign mode is the default. |

Pick modes in the order above — stress-test existing plans before drafting new ones; resolve unknowns before planning around them; design shape before designing sequence; default to roadmap design only when the earlier blockers do not apply.

## Four internal modes

| Mode | Owns | Use when |
|---|---|---|
| `RoadmapDesign` | Default execution roadmap | You need sequencing, decisions, risks, and validation checkpoints |
| `DecisionSpike` | One bounded unknown | Planning would be fake without answering one specific question first |
| `StructuralDesign` | Target shape or boundaries | The problem is system structure, workflow shape, or interface design |
| `PlanStressTest` | Hardening an existing plan | A real plan exists and needs challenge before implementation |

## The vertical-slices planning principle

Architect defaults to **vertical slices over horizontal layers**. From the SKILL.md:

- Prefer slices that produce one user-recognizable outcome through every relevant layer.
- Sequence slices by risk and unknowns, not by layer dependency or implementation comfort.
- Treat plans framed as "build all the backend first" or "finish the UI later" as a warning sign unless the user explicitly needs a layer-isolated task.
- Make each planned slice independently demonstrable, reviewable, and safe to stop after.
- Use mocks only to preserve an end-to-end path inside the current slice, and name the later slice that replaces each mock.

A layer-first plan is *easier* to write and *harder* to verify, because no single completed layer produces a reviewable outcome. A slice-first plan forces every step to be demonstrable, which is what makes review possible in the first place.

## Default output shape

Architect routes to one primary mode, then uses that mode's specific output contract. In every mode, the output makes these easy to find:

1. **Framing goal** — the outcome this plan is designed to reach.
2. **Current constraint or blocker** — what is making this hard right now.
3. **Recommended structure, path, or conclusion** — the plan itself.
4. **What needs human review** — the decisions that are not the agent's to make.
5. **Recommended next phase** — usually Implement, sometimes another Architect pass or a return to Vision.

When a mode produces execution sequencing, slices are described as demonstrable outcomes rather than layer buckets.

## The "C header file" analogy

The SKILL.md compares Architect's output to a C header file: it defines signatures, new types, and high-level phases. Not the implementation, not the internal logic — just the interface. The implementation lives in Implement; Architect lives one level above.

This analogy is load-bearing. If your Architect output reads like code, you are doing Implement's job. If it reads like a ticket, you are doing Vision's job. A good Architect artifact reads like an interface definition: signatures + phases + checkpoints.

## Boundaries — when *not* to use Architect

| Real need | Reach for |
|---|---|
| Broad orientation or current-state research | [[scout]] |
| Identifying the change surface or blast radius | [[scope]] |
| Deciding whether the direction is right | [[vision]] |
| Building the work or debugging a failure | [[implement]] |
| Documenting a concrete outcome, decision, or artifact | [[doc-update]] |
| Refreshing, deduplicating, or repairing existing docs | [[doc-cleaner]] |

## Architect vs. Implement

| | Architect | Implement |
|---|---|---|
| Question | "How do we get there?" | "Let's get there." |
| Output | Roadmap, slices, checkpoints | Working code or explained fix |
| Owns code? | No — only signatures | Yes — actual implementation |
| Owns tests? | Names them in checkpoints | Writes them |

The transition from Architect to Implement is a handoff. Architect's last output is the first slice, described as a demonstrable outcome. Implement's first input is that slice.

## Related

- [[scout]]
- [[scope]]
- [[vision]]
- [[implement]]
- [[advisor]]
- source: `dot_config/ai_templates/skills/pa-sdlc/pa-architect/SKILL.md`
