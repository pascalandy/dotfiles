---
name: pa-architect
description: Universal execution-design meta-skill for designing how work should proceed before implementation begins across repositories, websites, content systems, project-management workspaces, knowledge systems, or personal contexts. USE WHEN architect, architecture, frame, framing, technical planning, execution plan, roadmap, implementation roadmap, phased plan, milestone plan, break this into phases, spike, technical spike, research this blocker, reduce uncertainty, architecture design, structure, boundaries, operating model, plan review, engineering review, stress test this plan, execution readiness.
---

# Architect

## Routing

| Request Pattern | Route To |
|---|---|
| plan this, turn this into a roadmap, break this into phases, how do we execute this, implementation roadmap, milestone plan, phased plan, tracer bullets | `RoadmapDesign/MetaSkill.md` |
| run a spike, research this blocker, validate this unknown, time-box this research, answer this before planning, reduce uncertainty first | `DecisionSpike/MetaSkill.md` |
| design the architecture, define the structure, rethink the boundaries, improve the operating model, redesign the flow before planning, shape the system first | `StructuralDesign/MetaSkill.md` |
| review this plan, stress-test this roadmap, lock in the plan, engineering review, execution readiness review, challenge this implementation plan | `PlanStressTest/MetaSkill.md` |

## Routing Notes

- Apply the rows in this order: `PlanStressTest`, `DecisionSpike`, `StructuralDesign`, then default to `RoadmapDesign`.
- Use `PlanStressTest` only when a meaningful execution plan already exists.
- Use `DecisionSpike` only when one named unknown blocks planning.
- Use `StructuralDesign` only when the design surface is already known and the unresolved problem is the structure itself.
- If no row clearly fits but the direction is settled enough to sequence, use `RoadmapDesign`.
- For compound asks, choose the earliest blocking architecting job first and recommend the next mode explicitly.
- When sequencing work, prefer vertical slices that cross all relevant layers over horizontal layer-by-layer plans.
- If a proposed plan is organized as backend-first, then frontend, then integration, treat that as a signal to route through `RoadmapDesign` for re-slicing or `PlanStressTest` for readiness review.
- When an Architect mode produces an artifact, export that artifact before recommending `pa-implement` or any other next phase.
- If the user really needs discovery, scoping, direction validation, or implementation, hand off to `pa-scout`, `pa-scope`, `pa-vision`, or `pa-implement` instead of forcing an Architect mode.
