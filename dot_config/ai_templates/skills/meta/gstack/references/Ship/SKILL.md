---
name: Ship
description: "Route release, deployment, docs, retros, safety, setup, and maintenance requests to the right gstack shipping skill. USE WHEN the work is ready to leave development or the operating controls around it need attention. Keywords: ship, open PR, push, release, deploy, canary, setup deploy, safety mode, freeze, guard, unfreeze, import cookies, docs, retro, learn, upgrade gstack."
---

## Status Update

Before routing, emit a brief status update such as:
`Routing through the **Ship** sub-skill to pick the right gstack release or operations specialist...`

# Ship

## Core Concept

Use this sub-skill for release work and the operating tasks around it. It owns shipping, deployment, rollout observation, safety controls, and post-ship maintenance. It should answer the question, "How do we release this safely and handle the operational follow-through?"

## Workflow Routing

| Intent | Workflow | Use When |
|---|---|---|
| Release or deploy | `workflows/Release.md` | The user wants to ship, deploy, observe rollout, or configure deploy flow |
| Add or remove safety controls | `workflows/Safety.md` | The user wants destructive-action safeguards or auth-testing setup |
| Sync docs or maintain the environment | `workflows/Maintain.md` | The user wants docs, retros, learnings, or upgrade work |

## Workflow Catalog

| Workflow | Purpose | Typical Downstream Skills |
|---|---|---|
| `Release` | Ship code, deploy it, and observe rollout quality | `ship`, `land-and-deploy`, `canary`, `setup-deploy` |
| `Safety` | Turn operating controls on or off before risky work | `careful`, `freeze`, `guard`, `unfreeze`, `setup-browser-cookies` |
| `Maintain` | Keep docs, learnings, and the gstack environment current | `document-release`, `retro`, `learn`, `gstack-upgrade` |

## Output Format

Return:

1. Selected workflow, or ordered workflow sequence if more than one applies
2. Concrete gstack skill path or paths to load
3. Short reason tied to why the request is release or operations work
4. Any sequence note if release, safety, and maintenance should run in order

## Boundary Rules

1. Own release orchestration, deploy controls, safety controls, and post-ship follow-through.
2. Do not route product framing, architecture review, or design direction through this sub-skill.
3. Do not route debugging, code review, or QA through this sub-skill.
4. If a request mixes release and docs, keep both in `Ship` and preserve the requested order.

## Example

```text
User: create the PR, deploy it, then sync the docs.

Route:
- Workflow: `Release`, then `Maintain`
- Load: `../../ship/SKILL.md`, `../../document-release/SKILL.md`
- Reason: the request is release work plus cleanup
```
