---
name: gstack-shape-the-work
description: "Route pre-implementation product, planning, architecture, and design-direction requests to the right concrete gstack skill. Use when the user is still deciding what to build, how it should work, or how ambitious it should be."
---

# Shape The Work

## Core Concept

This specialist owns the decisions that should happen before the main build, debug, QA, or release work starts.

- Frame the problem before solutioning
- Lock scope and architecture before implementation
- Choose design direction before polishing or generating UI code

This specialist does not own debugging, QA, PR creation, deployment, or safety controls.

## Workflow Routing

| Intent | Workflow |
|---|---|
| Clarify the product, wedge, or scope | `workflows/ProductAndScope.md` |
| Review architecture, sequencing, or implementation plan | `workflows/ArchitectureAndPlan.md` |
| Set or critique design direction before building | `workflows/DesignDirection.md` |

## Output Format

Return:

1. The selected workflow name
2. The downstream concrete gstack skill path to load
3. A one-sentence reason for the choice
4. The expected artifact from that downstream skill

## Examples

```text
User: help me think through whether this is worth building.

Route:
- Workflow: `ProductAndScope`
- Load: `../../office-hours/SKILL.md`
- Reason: the user is still shaping the problem and wedge
- Expected artifact: sharper framing and a recommended direction
```

```text
User: review the architecture and test plan before coding.

Route:
- Workflow: `ArchitectureAndPlan`
- Load: `../../plan-eng-review/SKILL.md`
- Reason: the request is about implementation structure before execution
- Expected artifact: architecture review with edge cases and verification guidance
```
