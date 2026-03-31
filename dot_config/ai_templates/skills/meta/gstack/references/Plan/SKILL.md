---
name: Plan
description: "Route idea, scope, architecture, and design-direction requests to the right gstack planning skill. USE WHEN the user is still deciding what to build, how to structure it, or which direction to choose before implementation. Keywords: idea, brainstorm, wedge, founder review, office hours, architecture review, test plan, data flow, design system, visual direction."
---

## Status Update

Before routing, emit a brief status update such as:
`Routing through the **Plan** sub-skill to pick the right gstack planning specialist...`

# Plan

## Core Concept

Use this sub-skill before the main build starts. It owns pre-implementation work: problem framing, scope control, architecture review, and design direction. It should answer the question, "What should we build, and what should the shape of the work be before execution begins?"

## Workflow Routing

| Intent | Workflow | Use When |
|---|---|---|
| Shape the product or narrow the wedge | `workflows/Scope.md` | The user is still defining the problem, scope, or product angle |
| Review the implementation plan or architecture | `workflows/Architecture.md` | The user has a direction and wants structural review before coding |
| Pick or critique design direction | `workflows/Design.md` | The user wants visual, UX, or design-system guidance before implementation |

## Workflow Catalog

| Workflow | Purpose | Typical Downstream Skills |
|---|---|---|
| `Scope` | Clarify wedge, ambition, and planning depth | `office-hours`, `plan-ceo-review`, `autoplan` |
| `Architecture` | Stress-test data flow, edge cases, and technical shape | `plan-eng-review`, `plan-design-review` |
| `Design` | Set or critique visual and UX direction | `design-consultation`, `design-shotgun`, `plan-design-review` |

## Output Format

Return:

1. Selected workflow, or ordered workflow sequence if more than one applies
2. Concrete gstack skill path or paths to load
3. Short reason tied to why the request is still in the planning phase
4. Any handoff note if execution should later move to `Work` or `Ship`

## Boundary Rules

1. Own all pre-implementation framing.
2. Do not route debugging, QA, validation, or live inspection through this sub-skill.
3. Do not route release, deployment, safety controls, or post-ship maintenance through this sub-skill.
4. If a request mixes planning and execution, route the planning portion first and note the later handoff to `Work`.

## Example

```text
User: help me narrow the wedge for this idea.

Route:
- Workflow: `Scope`
- Load: `../../office-hours/SKILL.md`
- Reason: the request is still product framing before implementation
```
