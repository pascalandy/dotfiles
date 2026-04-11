---
name: PlanStressTest
description: Frame mode for reviewing and hardening a meaningful execution plan before implementation starts. USE WHEN a roadmap, implementation plan, design brief, or operating plan already proposes enough execution detail to challenge, tighten, and review for readiness.
---

# PlanStressTest

## Core Concept

PlanStressTest owns the hardening pass inside Frame.

Once a plan exists, the highest-value framing work is often not writing more plan text. It is challenging the existing plan from multiple angles so weak assumptions, missing edges, contradictory sections, and execution risks get surfaced before implementation starts.

PlanStressTest should help answer:

- what is missing
- what is contradictory
- what will fail on contact with reality
- what decisions are still too weak
- what must be corrected before execution begins

## When To Use

Use `PlanStressTest` when:

- a meaningful execution plan already exists, whether the artifact is called a roadmap, implementation brief, design brief, or operating plan
- the user asks for review, challenge, readiness, or engineering lock-in
- the concern is completeness, feasibility, execution scope discipline inside that plan, or execution risk
- a human wants confidence before handing the work to implementation

Do not use `PlanStressTest` when no meaningful plan exists yet, when the main need is to create the first roadmap from scratch, or when the real need is generic document review outside execution readiness.

## Source Patterns Absorbed

| Source skill | Contribution |
|--------------|--------------|
| `document-review` | Multi-lens execution-plan review, coherence checks, feasibility checks, and scope pressure applied to execution plans |
| `plan-eng-review` | Engineering lock-in around architecture, data flow, tests, edge cases, and performance |
| `gepetto` | External review and synthesis discipline |

## Workflow

1. Read the existing plan as the source of truth.
Review the actual artifact, not a paraphrase.

If there is no meaningful plan artifact yet, say so plainly and route back to `RoadmapDesign` or `StructuralDesign` as appropriate.

2. Classify the likely risk areas.
Look for coherence gaps, feasibility gaps, hidden scope creep, design weakness, missing edge cases, poor validation design, and horizontal layer planning disguised as progress.

3. Challenge the plan from multiple lenses.
Use only the strongest relevant lenses for execution readiness, not general document polish.

4. Distinguish fixable gaps from decision gaps.
Some issues can be corrected directly in the plan. Others need explicit human judgment.

5. Produce a readiness-oriented synthesis.
Do not merely list observations. Say what most threatens successful execution and what to do before starting.

## Output Contract

Prefer this shape:

1. `Request Or Framing Goal`
2. `Plan Strengths`
3. `Findings`
4. `Contradictions Or Missing Areas`
5. `Execution Risks`
6. `Validation Gaps`
7. `What Needs Human Review`
8. `Recommended Revisions`
9. `Readiness Verdict`
10. `Recommended Next Phase`

Present findings in severity order when possible.

When sequencing is part of the plan, explicitly check whether slices are user-recognizable, end to end, independently runnable, and ordered by risk rather than by layer.

## Subject Adaptation

Stress tests can apply to:

- software implementation plans
- website rollout plans
- PM operating-model changes
- knowledge-base restructuring plans
- personal operating plans with strong constraints and trade-offs

The review should adapt its lenses, but the core job is the same: harden the plan before execution.

## Design Rules

1. Review the plan that exists, not the one you wish had been written.
2. Focus on issues that threaten execution quality or outcome quality.
3. Distinguish weak evidence from genuine contradiction.
4. Surface missing validation early.
5. Say plainly when a plan is not ready.
6. If the review shows there is no real plan yet, route back to `RoadmapDesign` or `StructuralDesign` as appropriate.
7. Review execution substance, not writing polish or general documentation hygiene.
8. Treat backend-first, frontend-later, or integration-at-the-end planning as a substantive execution risk unless clearly justified.

## Non-Goals

PlanStressTest does not own initial discovery, product-direction definition, broad scoping, generic document review, release documentation, documentation cleanup, or implementation execution.
