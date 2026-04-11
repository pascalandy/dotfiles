---
name: DecisionSpike
description: Frame mode for reducing one blocking unknown through a bounded, time-boxed spike before full planning proceeds. USE WHEN the main need is to answer one critical question, validate feasibility, or gather decision-grade evidence.
---

# DecisionSpike

## Core Concept

DecisionSpike owns the uncertainty-reduction job inside Frame.

When one question can invalidate or materially reshape the plan, the right move is not to draft a full roadmap with fake certainty. The right move is to isolate the unknown, time-box the investigation, define exit criteria, and come back with a recommendation.

The spike should answer:

- what must be learned
- why it matters
- how far to investigate
- what evidence is enough to decide
- what happens next depending on the result

## When To Use

Use `DecisionSpike` when:

- one technical, structural, operational, or workflow unknown blocks planning
- the user wants a spike, proof-of-concept, validation pass, or research brief
- feasibility, compatibility, risk, or capability is unclear
- the blocking question is specific enough to name in one sentence and answer with bounded work
- it would be irresponsible to produce a full roadmap before answering a specific question

Do not use `DecisionSpike` when broad discovery is still needed, the affected surface is still unclear, the user already knows enough to sequence the work, or the main need is broad plan review rather than a bounded investigation.

## Source Patterns Absorbed

| Source skill | Contribution |
|--------------|--------------|
| `create-technical-spike` | Time-boxed spike structure, research tasks, success criteria, explicit recommendation |
| `technical-planning` | Risk prioritization and decision timing |
| `gepetto` | Research synthesis discipline |

## Workflow

1. Name the blocking unknown clearly.
Frame it as a decision question, not a vague area of curiosity.

If the unknown cannot be stated cleanly yet, the user probably needs Scout or Scope before a spike is justified.

2. Explain why it matters.
State what planning or execution decision depends on the answer.

3. Bound the spike.
Define timebox, scope, research depth, and what is deliberately out of scope.

4. Define investigation tasks.
Include only the work needed to answer the question with decision-grade evidence.

5. Define exit criteria.
Be explicit about what evidence is sufficient to conclude the spike.

6. Capture likely decision paths.
Show what happens if the result is positive, negative, or inconclusive.

7. Produce a recommendation.
Do not stop at raw findings if the evidence supports a decision.

## Output Contract

Prefer this compact shape:

1. `Request Or Framing Goal`
2. `Blocking Unknown`
3. `Why This Must Be Answered Now`
4. `Spike Boundaries And Timebox`
5. `Investigation Tasks`
6. `Exit Criteria`
7. `Decision Paths`
8. `Recommendation`
9. `What Needs Human Review`
10. `Recommended Next Phase`

## Subject Adaptation

This is not only for software. A spike can also validate:

- whether a content migration path is viable
- whether a PM automation model can support the intended workflow
- whether a knowledge-system taxonomy can survive the transition
- whether a personal routine experiment is realistic under real constraints

## Design Rules

1. One spike should answer one main question.
2. Time-box the investigation so it does not become broad discovery.
3. Ask for evidence strong enough to decide, not evidence for its own sake.
4. Tie the spike back to the blocked planning decision.
5. If many unknowns appear, create a short prioritized list rather than hiding them inside one bloated spike.
6. If the unknown is no longer blocking, route back to `RoadmapDesign`.
7. If the main issue becomes designing the target structure rather than validating one question, route to `StructuralDesign`.

## Non-Goals

DecisionSpike does not own full roadmap construction, broad onboarding research, architecture redesign across the whole system, or implementation itself.
