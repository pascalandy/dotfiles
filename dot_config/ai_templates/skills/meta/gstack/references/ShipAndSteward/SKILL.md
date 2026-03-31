---
name: gstack-ship-and-steward
description: "Route release, deployment, docs, retros, safety, setup, and learning-maintenance requests to the right concrete gstack skill. Use when the work is leaving development or when the surrounding operating controls need attention."
---

# Ship And Steward

## Core Concept

This specialist owns everything around release and ongoing operating hygiene.

- Ship and deploy safely
- Control risk with safety boundaries and setup steps
- Bring docs, retros, and learnings back in sync after the work lands

This specialist does not own idea shaping, architecture review, debugging, or primary QA execution.

## Workflow Routing

| Intent | Workflow |
|---|---|
| Create the PR, release, deploy, or monitor rollout | `workflows/ReleaseAndDeploy.md` |
| Add or remove safety controls, restrict scope, or prep sensitive sessions | `workflows/SafetyAndControl.md` |
| Update docs, review learnings, run retros, or maintain the gstack environment | `workflows/OperateAndImprove.md` |

## Output Format

Return:

1. The selected workflow name
2. The downstream concrete gstack skill path to load
3. A one-sentence reason for the choice
4. The expected release, control, or maintenance artifact

## Examples

```text
User: ship this branch, deploy it, and watch the rollout.

Route:
- Workflow: `ReleaseAndDeploy`
- Load: `../../ship/SKILL.md`, then `../../land-and-deploy/SKILL.md`, then `../../canary/SKILL.md`
- Reason: the request is explicitly release and post-deploy verification work
- Expected artifact: PR, deploy status, and rollout evidence
```

```text
User: freeze edits to this folder, then update the docs after we land.

Route:
- Workflow: `SafetyAndControl`, then `OperateAndImprove`
- Load: `../../freeze/SKILL.md`, then `../../document-release/SKILL.md`
- Reason: the user is asking for operating controls and post-ship upkeep
- Expected artifact: active safety boundary and synchronized documentation
```
