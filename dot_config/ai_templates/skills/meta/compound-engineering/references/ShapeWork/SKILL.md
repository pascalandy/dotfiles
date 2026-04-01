---
name: ShapeWork
description: "Shape compound-engineering work before implementation by clarifying the problem, writing requirements, creating plans, and choosing architectural patterns. USE WHEN the request is still about what to build, how to scope it, how to plan it, or which design approach fits best."
---

# ShapeWork

ShapeWork owns pre-implementation thinking. It works standalone or via the meta-skill router. Use it when the work still needs to be framed, scoped, turned into a plan, or aligned to a specific architectural or framework pattern.

## Core Concept

Do not jump into execution when the real need is decision quality. ShapeWork narrows ambiguity first, produces a durable artifact when needed, and then hands off to the right execution path.

## Workflow Routing

| User Intent | Load |
|---|---|
| Need ideas, requirements, product framing, or repo orientation | `workflows/DiscoverDirection.md` |
| Need a technical plan or a plan-strengthening pass | `workflows/DesignTheApproach.md` |
| Need an architecture, style, or framework-specific direction before coding | `workflows/ChooseSpecializedPatterns.md` |

## Output Format

Return a short routing decision with:

1. Selected workflow
2. Downstream skill path
3. Why this route fits the request
4. Expected artifact or next handoff

## Examples

```text
User: brainstorm the safest way to roll out this billing feature

Route:
- Workflow: `DiscoverDirection`
- Downstream skill: `../ce-brainstorm/SKILL.md`
- Why: product framing and scope need to be clarified before planning
- Expected artifact: requirements document with success criteria and scope boundaries
```

```text
User: deepen this implementation plan and pressure-test the risks

Route:
- Workflow: `DesignTheApproach`
- Downstream skill: `../ce-plan/SKILL.md`
- Why: the request is about improving the implementation plan rather than writing code
- Expected artifact: revised plan with stronger sequencing, files, risks, and verification
```
