---
name: Work
description: "Route debugging, browser inspection, implementation, review, QA, security, and performance requests to the right gstack execution skill. USE WHEN the work is in progress and needs inspection, fixes, or evidence before release. Keywords: debug, investigate, broken flow, inspect, browser, Chrome, review diff, review branch, QA, security review, threat model, benchmark, performance baseline."
---

## Status Update

Before routing, emit a brief status update such as:
`Routing through the **Work** sub-skill to pick the right gstack execution specialist...`

# Work

## Core Concept

Use this sub-skill while the product is being built, inspected, or hardened. It owns active execution work: diagnosing bugs, inspecting live behavior, reviewing diffs, QA testing, and checking risk. It should answer the question, "What must happen to prove or improve the work before release?"

## Workflow Routing

| Intent | Workflow | Use When |
|---|---|---|
| Debug or inspect behavior | `workflows/Debug.md` | The user needs root-cause analysis, browser inspection, or evidence capture |
| Review code or validate flows | `workflows/Validate.md` | The user needs branch review, QA, or UI polish before shipping |
| Check security or performance | `workflows/Risk.md` | The user needs security, threat, or benchmark analysis |

## Workflow Catalog

| Workflow | Purpose | Typical Downstream Skills |
|---|---|---|
| `Debug` | Diagnose broken behavior and inspect runtime state | `investigate`, `browse`, `connect-chrome`, `design-html` |
| `Validate` | Review code, QA the flow, or polish the live UI | `review`, `qa`, `qa-only`, `design-review` |
| `Risk` | Evaluate security posture or performance behavior | `cso`, `benchmark` |

## Output Format

Return:

1. Selected workflow, or ordered workflow sequence if more than one applies
2. Concrete gstack skill path or paths to load
3. Short reason tied to why the request is active execution work
4. Any follow-on recommendation if the request should later move to `Ship`

## Boundary Rules

1. Own in-flight execution, inspection, validation, and hardening.
2. Do not route ideation, scope definition, or architecture planning through this sub-skill.
3. Do not route release orchestration, safety controls, or documentation follow-through through this sub-skill.
4. If a request mixes debugging and QA, keep both in `Work` and preserve the user-requested order.

## Example

```text
User: debug the broken flow and inspect it in the browser.

Route:
- Workflow: `Debug`
- Load: `../../investigate/SKILL.md`
- Reason: the request is active debugging and runtime inspection work
```
