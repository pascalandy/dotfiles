---
name: pa-implement
description: Universal implementation meta-skill for executing bounded changes or repairing broken behavior across repositories, websites, content systems, project-management workspaces, knowledge systems, or personal contexts. USE WHEN implement, implementation, build, apply the change, execute this, make this update, make-the-change, fix this bug, repair this, debug this, troubleshoot this, broken behavior, unexpected behavior, regression, reproduce this issue, root cause, diagnose failure, vertical slices, horizontal layers, tdd, test driven development, red green refactor, website, content system, project management, knowledge system, personal context.
---

# Implement

## Routing

| Request Pattern | Route To |
|---|---|
| fix this bug, why is this broken, reproduce this issue, investigate this regression, diagnose this failure, debug this, troubleshoot this, root cause, broken behavior, unexpected behavior, repair this workflow, fix this publish failure, repair this automation | `RootCauseRepair/MetaSkill.md` |
| build this, implement this, apply this plan, make this change, execute this update, ship this slice, carry this out, do the work, apply this workflow change, update this page flow, carry out this content change, make this system update | `ChangeApplication/MetaSkill.md` |

## Routing Notes

- Apply the rows in this order: `RootCauseRepair`, then default to `ChangeApplication`.
- Use `RootCauseRepair` only when the request is explicitly bug-shaped, failure-shaped, or regression-shaped.
- Use `ChangeApplication` for all bounded execution requests that are ready to be applied.
- Before routing to `ChangeApplication`, confirm the outcome is specific enough to name one first slice, the execution surface is known enough to act, and the remaining uncertainty is execution detail rather than unresolved product or planning work.
- If the work is not ready because discovery, scope, direction, or planning is still unresolved, hand off to `pa-scout`, `pa-scope`, `pa-vision`, or `pa-architect` instead of forcing an Implement mode.
