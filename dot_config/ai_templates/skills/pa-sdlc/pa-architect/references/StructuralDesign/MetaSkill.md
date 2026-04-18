---
name: StructuralDesign
description: Frame mode for defining the target structure, boundaries, interfaces, flows, or operating model before sequencing execution. USE WHEN the main challenge is the shape of the system or workflow, not just the order of work.
---

# StructuralDesign

## Core Concept

StructuralDesign owns the shape-making job inside Frame.

Some work is blocked because the team does not yet agree on the right boundaries, interface shape, ownership model, workflow design, or system structure. In those cases, sequencing tasks too early creates fake progress. The design of the structure must come first.

StructuralDesign should:

- identify the core structural friction
- surface multiple viable shapes when helpful
- compare trade-offs clearly
- recommend the strongest design
- leave behind a structure solid enough for later roadmap planning

## When To Use

Use `StructuralDesign` when:

- the user asks for architecture design, system shape, interface design, or workflow redesign
- the main challenge is coupling, boundary confusion, or shallow structure
- an operating model or transition model needs to be defined before tasks can be sequenced
- the design surface is already known well enough that the job is to shape it rather than discover it
- the current shape of the system is the core blocker to planning

Do not use `StructuralDesign` when the affected surface is still unclear, when the structure is already settled and the work mainly needs sequencing, or when the user only wants critique of an existing plan.

## Source Patterns Absorbed

| Source skill | Contribution |
|--------------|--------------|
| `improve-codebase-architecture` | Structural-friction detection, interface alternatives, trade-off reasoning |
| `technical-planning` | Decision timing and risk framing |
| `plan-eng-review` (secondary) | Engineering judgment about architecture, data flow, edge cases, and performance once a candidate shape exists |

## Workflow

1. Define the structural problem.
State what is wrong or unclear in the current shape.

2. Identify the key constraints.
Capture dependencies, boundaries, ownership constraints, migration realities, and performance or coordination implications.

3. Describe viable options.
Where useful, present more than one structural shape rather than assuming one answer.

4. Compare trade-offs.
Evaluate clarity, flexibility, coupling, migration cost, operability, and future extensibility as relevant to the subject.

5. Recommend a target shape.
Take a position instead of presenting a menu without judgment.

6. Define what the later roadmap should treat as durable.
Name the boundaries, concepts, interfaces, or operating rules that later phases can build around.
Prefer structures that can be validated through thin vertical slices rather than requiring full horizontal layer completion before the first real checkpoint.

## Output Contract

Prefer this shape:

1. `Request Or Framing Goal`
2. `Current Constraints`
3. `Structural Problem`
4. `Candidate Shapes`
5. `Trade-Offs`
6. `Recommended Structure`
7. `Critical Unknowns`
8. `Validation Strategy`
9. `What Needs Human Review`
10. `Recommended Next Phase`

## Subject Adaptation

Examples of structural design outside software:

- website/content: page model, ownership boundaries, publishing stages, editorial control points
- PM/ops: approval model, state machine, role handoffs, automation boundaries
- knowledge systems: taxonomy shape, canonical-note pattern, routing rules, migration structure
- personal context: routine design, review cadence, decision checkpoints, commitment boundaries

## Design Rules

1. Focus on the shape of the system or workflow before sequencing execution.
2. Prefer fewer, deeper, clearer boundaries over sprawling shallow structures.
3. Show trade-offs explicitly when more than one viable shape exists.
4. Recommend one structure unless the evidence is genuinely too weak.
5. Do not drift into a full execution roadmap; hand off to `RoadmapDesign` once the structure is stable enough.
6. If the user mainly wants critique of an existing plan, route to `PlanStressTest`.
7. If the user mainly needs to validate one candidate structure or blocker rather than define the shape, route to `DecisionSpike`.
8. Export the structural-design artifact before recommending `RoadmapDesign`, `pa-implement`, or any other next phase.

## Non-Goals

StructuralDesign does not own broad discovery, product strategy, implementation sequencing in detail, or coding.
