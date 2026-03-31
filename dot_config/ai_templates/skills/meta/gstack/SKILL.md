---
name: gstack
description: "Unified gstack workflow routing across planning, active execution, and shipping. Use when the user wants one entry point that automatically delegates to the right gstack specialist skill."
keywords: [gstack, idea, brainstorm, wedge, founder-review, office-hours, plan, architecture, design, debug, investigate, browser, review, qa, security, benchmark, ship, release, deploy, canary, docs, retro, safety, freeze, guard, setup, learn, upgrade]
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — do not edit directly -->
<!-- Regenerate: bun run gen:skill-docs -->

# gstack

> One entry point for the full gstack engineering lifecycle. The collection routes to the right phase specialist, and that specialist routes to the concrete skill.

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

## The Problem

gstack contains many specialized skills across ideation, implementation, validation, release, and operational follow-through. That breadth is useful, but it creates a usability problem: the user should not need to know whether a request belongs to `office-hours`, `plan-eng-review`, `investigate`, `qa`, `ship`, `document-release`, or one of the safety tools before they can ask for help.

Without a meta-skill, the assistant has to remember the whole catalog and manually pick a route every time. That makes routing harder to maintain, easier to overlap, and more likely to drift as new specialists are added.

## The Solution

`gstack` is a hierarchical meta-skill with three layers:

1. The collection `SKILL.md` is the user-facing entry point.
2. `references/ROUTER.md` is the minimal dispatcher that selects the right lifecycle specialist.
3. Each lifecycle specialist owns one distinct domain and routes into the final concrete gstack skill.

This gives the user a single invocation surface while keeping routing logic isolated, additive, and easy to extend.

## How Routing Works

1. Read `references/ROUTER.md`.
2. Route into one of the three lifecycle specialists: `Plan`, `Work`, or `Ship`.
3. Let that specialist select one or more workflows inside its domain.
4. Let the workflow choose the concrete gstack skill path to load.

## Included Phases

This collection owns three non-overlapping lifecycle phases:

1. `Plan` for pre-implementation framing and direction.
2. `Work` for in-flight implementation, inspection, validation, and hardening.
3. `Ship` for release orchestration, safety controls, and post-ship maintenance.

## What's Included

| Component | Path | Purpose | Workflows | Delegates To |
|---|---|---|---|---|
| Collection entry point | `SKILL.md` | User-facing overview, lifecycle framing, and examples | N/A | `references/ROUTER.md` |
| Router | `references/ROUTER.md` | Minimal top-level dispatch table | N/A | `references/Plan/SKILL.md`, `references/Work/SKILL.md`, `references/Ship/SKILL.md` |
| Planning specialist | `references/Plan/SKILL.md` | Pre-build framing, architecture review, and design direction | `Scope`, `Architecture`, `Design` | `office-hours`, `plan-ceo-review`, `autoplan`, `plan-eng-review`, `plan-design-review`, `design-consultation`, `design-shotgun` |
| Execution specialist | `references/Work/SKILL.md` | Debugging, inspection, validation, QA, security, and performance | `Debug`, `Validate`, `Risk` | `investigate`, `browse`, `connect-chrome`, `design-html`, `review`, `qa`, `qa-only`, `design-review`, `cso`, `benchmark` |
| Shipping specialist | `references/Ship/SKILL.md` | Release work, deploy controls, safety controls, and post-ship maintenance | `Release`, `Safety`, `Maintain` | `ship`, `land-and-deploy`, `canary`, `setup-deploy`, `careful`, `freeze`, `guard`, `unfreeze`, `setup-browser-cookies`, `document-release`, `retro`, `learn`, `gstack-upgrade` |

## Invocation Scenarios

| Trigger Phrase | What Happens |
|---|---|
| "help me think through this idea" | Routes to `Plan`, then `Scope`, then to `office-hours/SKILL.md` |
| "challenge the scope like a founder" | Routes to `Plan`, then `Scope`, then to `plan-ceo-review/SKILL.md` |
| "review the architecture before we build" | Routes to `Plan`, then `Architecture`, then to `plan-eng-review/SKILL.md` |
| "design system for this product" | Routes to `Plan`, then `Design`, then to `design-consultation/SKILL.md` |
| "debug this broken flow" | Routes to `Work`, then `Debug`, then to `investigate/SKILL.md` |
| "inspect the live page and capture evidence" | Routes to `Work`, then `Debug`, then to `browse/SKILL.md` |
| "review the branch and QA the app" | Routes to `Work`, then `Validate`, then to `review/SKILL.md` or `qa/SKILL.md` |
| "run a security check" | Routes to `Work`, then `Risk`, then to `cso/SKILL.md` |
| "ship this and open the PR" | Routes to `Ship`, then `Release`, then to `ship/SKILL.md` |
| "watch the rollout after deploy" | Routes to `Ship`, then `Release`, then to `canary/SKILL.md` |
| "lock this directory before I debug" | Routes to `Ship`, then `Safety`, then to `freeze/SKILL.md` or `guard/SKILL.md` |
| "update docs after deploy" | Routes to `Ship`, then `Maintain`, then to `document-release/SKILL.md` |

## Example Usage

### Plan

```text
User: I have a rough product idea and need help narrowing the wedge.

AI routes to Plan and returns:
- Workflow: `Scope`
- Downstream skill: `office-hours/SKILL.md`
- Reason: the request is still deciding what to build
```

### Work

```text
User: the feature is implemented, now debug the flaky part and QA the flow.

AI routes to Work and returns:
- Workflow: `Debug` followed by `Validate`
- Downstream skills: `investigate/SKILL.md`, `qa/SKILL.md`
- Reason: the feature exists but still needs diagnosis and evidence
```

### Ship

```text
User: create the PR, deploy it, then update the docs.

AI routes to Ship and returns:
- Workflow: `Release` followed by `Maintain`
- Downstream skills: `ship/SKILL.md`, `land-and-deploy/SKILL.md`, `document-release/SKILL.md`
- Reason: the request is release work plus cleanup
```

## Design Guardrails

1. Single entry point: users invoke `gstack`, not the phase specialist.
2. Invisible delegation: routing is automatic and does not burden the user.
3. No domain overlap: `Plan`, `Work`, and `Ship` own distinct lifecycle territory.
4. Consistent interface: each sub-skill follows the same routing and output shape.
5. Additive scaling: a new specialist phase means one new directory plus one router row.

## Harness Agnostic Notes

1. Use only relative skill paths.
2. Do not assume assistant-specific hooks, internal directories, or path conventions.
3. Describe actions in portable terms such as read, route, search, load, run, or verify.

## Customization

| Change | Edit |
|---|---|
| Top-level lifecycle routing | `references/ROUTER.md` |
| Planning routes | `references/Plan/workflows/*.md` |
| Execution routes | `references/Work/workflows/*.md` |
| Shipping routes | `references/Ship/workflows/*.md` |
| User-facing collection copy | `SKILL.md.tmpl`, then regenerate `SKILL.md` |

## Maintenance Notes

1. Add a new downstream skill by attaching it to exactly one workflow in exactly one phase.
2. Add a new phase only if the request domain cannot fit cleanly into `Plan`, `Work`, or `Ship`.
3. Keep `references/ROUTER.md` minimal and keep detailed routing logic inside the sub-skills.

## Notes

- `gstack` is a routing layer, not a replacement for the concrete gstack skills
- Keep the router minimal and keep routing detail inside the sub-skills
