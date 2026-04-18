---
name: RoadmapDesign
description: Default Frame mode for turning a settled direction into a concrete execution roadmap with phases, key decisions, risk-first sequencing, validation checkpoints, and explicit deferrals. USE WHEN the main need is to plan how to execute already-chosen work.
---

# RoadmapDesign

## Core Concept

RoadmapDesign owns the default Frame job: converting a settled direction into an execution path that is concrete enough to guide implementation without collapsing into brittle implementation detail.

The plan should be:

1. Outcome-focused rather than step-scripted.
2. Risk-first rather than comfort-first.
3. Explicit about durable decisions and explicit about deferrals.
4. Grounded enough for handoff, but flexible enough for implementation learning.
5. Structured as vertical slices through the full system, not horizontal completion of one layer at a time.

## When To Use

Use `RoadmapDesign` when:

- the direction is already good enough and the user now needs a roadmap
- the work needs phases, milestones, slices, or workstreams
- the user wants sequencing, dependencies, decisions, validation, and rollout logic
- the work spans multiple surfaces and needs a coherent execution path

Do not use `RoadmapDesign` when one blocking unknown should be isolated first, when the main problem is structural design, or when a plan already exists and needs review instead of creation.

## Source Patterns Absorbed

| Source skill | Contribution |
|--------------|--------------|
| `technical-planning` | Risk-first milestone planning, managed deferral, decision timing |
| `prd-to-plan` | Thin-slice conversion from settled requirements into phased execution |
| `gepetto` | Rich synthesis and handoff-ready plan structure |

## Workflow

1. Confirm the framing input.
The input may be a brief, PRD, direction draft, migration goal, workflow change, restructuring goal, or equivalent settled direction artifact.

2. Extract the execution-shaping facts.
Capture hard constraints, dependencies, success conditions, deadlines, coordination points, and irreversible decisions.

3. Identify durable decisions.
Call out high-level choices that later phases should treat as stable unless the user revisits them.

4. Sequence by risk and dependency.
Put the most dangerous unknowns and highest-leverage enabling work early. Avoid sequencing purely by convenience.

5. Define phases or workstreams.
Each phase should produce something verifiable, not just partial labor in one layer.
Name slices as user-recognizable outcomes that cut through every relevant layer, with mocks only where needed to keep the path end to end.

6. Mark deferrals explicitly.
Say what is intentionally out of scope for early phases and why that deferral is acceptable.

7. Add validation checkpoints.
Every roadmap needs concrete ways to tell whether progress is real.

8. End with human review points.
Surface the decisions, assumptions, or trade-offs that still need approval.

## Vertical-Slice Rules

Apply these rules whenever RoadmapDesign sequences work:

1. Slice first by outcome, not by architecture layer.
2. Make slice 1 touch every layer the final system will touch, even if some parts are mocked.
3. Define "done" for each slice as something that can be run, shown, or otherwise demonstrated.
4. Ensure no slice depends on a future slice to be runnable.
5. Name each mock and the later slice that replaces it.
6. Avoid planning items phrased as "build all X" or "set up all Y" unless that work is itself a complete demonstrable outcome.

## Output Contract

Use this shape by default:

1. `Request Or Framing Goal`
2. `Current Constraints`
3. `Target Structure Or Execution Shape`
4. `Key Decisions`
5. `Phases Or Workstreams`
6. `Critical Unknowns`
7. `Validation Strategy`
8. `Risks And Deferrals`
9. `What Needs Human Review`
10. `Recommended Next Phase`

For each phase or workstream, prefer:

- goal
- why it comes now
- what becomes true after it
- dependencies or blockers
- validation signal
- done means demonstrable
- mocks used and later replacement slice

## Subject Adaptation

Translate "phases" and "implementation" into the natural language of the subject:

- software: milestones, slices, rollout stages, integrations
- website/content: content migration steps, template rollout, publishing checkpoints
- PM/ops: workflow transition stages, automation rollout, approval checkpoints
- knowledge systems: taxonomy migration, canonicalization passes, navigation cutover
- personal context: staged experiments, review intervals, commitment sequencing

## Design Rules

1. Keep the roadmap concrete enough to execute, but not so specific that it freezes future implementation choices too early.
2. Prefer thin, verifiable slices over broad horizontal effort buckets.
3. Put irreversible or high-risk work early enough to learn from it.
4. Distinguish required phases from optional polish.
5. The first execution slice should cross every layer needed for the final outcome, even if some layers are lightly mocked.
6. Reject plans that postpone integration until the end unless the user explicitly accepts that risk.
7. If the work hinges on one major unknown, route to `DecisionSpike` instead of pretending confidence.
8. If the main challenge is the target structure itself, route to `StructuralDesign` first.
9. Export the roadmap artifact before recommending `pa-implement` or any other next phase.

## Non-Goals

RoadmapDesign does not own broad discovery, product-direction validation, detailed coding instructions, or post-implementation execution management.
