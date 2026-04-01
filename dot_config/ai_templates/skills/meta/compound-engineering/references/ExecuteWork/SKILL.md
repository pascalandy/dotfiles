---
name: ExecuteWork
description: "Execute compound-engineering work by implementing code, using focused builder skills, and handling delivery mechanics. USE WHEN the request is to make changes, generate assets, automate work, or move a completed change through branch, commit, and PR steps."
---

# ExecuteWork

ExecuteWork owns in-flight delivery. It works standalone or via the meta-skill router. Use it when the path is understood and the main job is to change code, build assets, automate implementation, or move work through branch and PR mechanics.

## Core Concept

Prefer direct execution once the scope is clear. Keep the router thin, then hand the task to the most specific implementation or delivery skill already present in the pack.

## Workflow Routing

| User Intent | Load |
|---|---|
| Need to implement work from a prompt, todo, or plan | `workflows/ImplementFromPlan.md` |
| Need a focused builder for frontend, browser, media, or specialized generation work | `workflows/UseFocusedBuilders.md` |
| Need branch, commit, PR, or documentation publication mechanics around the change | `workflows/ManageDelivery.md` |

## Output Format

Return a short routing decision with:

1. Selected workflow
2. Downstream skill path
3. Why this route fits the request
4. Expected artifact or next handoff

## Examples

```text
User: execute this plan and finish the feature end to end

Route:
- Workflow: `ImplementFromPlan`
- Downstream skill: `../ce-work/SKILL.md`
- Why: the work is implementation-focused and already scoped
- Expected artifact: completed code changes with verification performed during execution
```

```text
User: create the UI for this onboarding flow and keep the design quality high

Route:
- Workflow: `UseFocusedBuilders`
- Downstream skill: `../frontend-design/SKILL.md`
- Why: the request is a specialized implementation task with a strong design requirement
- Expected artifact: production-ready frontend changes and validation guidance
```
