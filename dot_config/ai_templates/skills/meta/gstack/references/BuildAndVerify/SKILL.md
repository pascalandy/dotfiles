---
name: gstack-build-and-verify
description: "Route implementation-adjacent execution, debugging, testing, review, browser, security, and performance requests to the right concrete gstack skill. Use when work is in flight and needs inspection, correction, or proof."
---

# Build And Verify

## Core Concept

This specialist owns the high-leverage work that happens while code or UI is being built, inspected, or hardened.

- Inspect and debug live behavior
- Review diffs and test real flows
- Generate or refine implementation-adjacent outputs such as HTML from approved designs
- Validate security and performance before release

This specialist does not own ideation, high-level scope setting, release orchestration, deployment, or post-ship maintenance.

## Workflow Routing

| Intent | Workflow |
|---|---|
| Build from an approved design or inspect a browser-driven flow | `workflows/BuildAndInspect.md` |
| Review code, QA the app, or run design fix loops | `workflows/ReviewAndTest.md` |
| Check security posture or performance baselines | `workflows/RiskAndPerformance.md` |

## Output Format

Return:

1. The selected workflow name
2. The downstream concrete gstack skill path to load
3. A one-sentence reason for the choice
4. The expected evidence or artifact from that downstream skill

## Examples

```text
User: this flow is broken in staging, inspect it in the browser and debug it.

Route:
- Workflow: `BuildAndInspect`
- Load: `../../investigate/SKILL.md`
- Reason: the request is about root-cause analysis during active development
- Expected artifact: a diagnosis with verified fix steps
```

```text
User: review this branch and QA the signup flow.

Route:
- Workflow: `ReviewAndTest`
- Load: `../../review/SKILL.md` and `../../qa/SKILL.md`
- Reason: the user is asking for proof that the work is correct before shipping
- Expected artifact: findings, fixes, and QA evidence
```
