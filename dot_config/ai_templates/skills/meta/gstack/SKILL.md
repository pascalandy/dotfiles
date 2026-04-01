---
name: gstack
description: "Unified gstack workflow routing across planning, active execution, and shipping. Use when the user wants one entry point that automatically delegates to the right gstack specialist skill."
keywords: [gstack, idea, brainstorm, wedge, founder-review, office-hours, plan, architecture, design, debug, investigate, browser, review, qa, security, benchmark, ship, release, deploy, canary, docs, retro, safety, freeze, guard, setup, learn, upgrade]
---

# gstack

> One entry point for the full gstack engineering lifecycle. The collection keeps the lifecycle organized into `Plan`, `Work`, and `Ship`, but the router dispatches directly to the concrete skill in a single hop.

## Routing

Load `references/ROUTER.md` to determine which concrete sub-skill handles this request.

## The Problem

gstack contains many specialized skills across ideation, implementation, validation, release, and operational follow-through. That breadth is useful, but the user should not need to know whether a request belongs to `office-hours`, `plan-eng-review`, `investigate`, `qa`, `ship`, `document-release`, or one of the safety tools before asking for help.

Without a meta-skill, the assistant has to remember the whole catalog and manually pick a route every time. That makes routing harder to maintain, easier to overlap, and more likely to drift as the skill pack grows.

## The Solution

`gstack` is a single-entry meta-skill with one routing layer:

1. The collection `SKILL.md` is the user-facing overview.
2. `references/ROUTER.md` matches the request directly to the concrete skill to load.
3. `Plan`, `Work`, and `Ship` remain as conceptual lifecycle buckets, not extra routing steps.

This keeps the lifecycle clear without forcing the AI through a second dispatch layer.

## How Routing Works

1. Read `references/ROUTER.md`.
2. Match the request to one concrete skill.
3. Use the phase label in the router only as organizational context.

## Included Phases

This collection owns three non-overlapping lifecycle phases:

1. `Plan` for pre-implementation framing and direction.
2. `Work` for in-flight implementation, inspection, validation, and hardening.
3. `Ship` for release orchestration, safety controls, and post-ship maintenance.

## What's Included

| Component | Path | Purpose | Includes |
|---|---|---|---|
| Collection entry point | `SKILL.md` | User-facing overview, lifecycle framing, and examples | `references/ROUTER.md` |
| Core router | `references/ROUTER.md` | Direct one-hop routing to concrete skills | All concrete skills under `references/` |
| Plan phase | `SKILL.md` and `references/ROUTER.md` | Organize pre-build requests without adding another routing hop | `office-hours`, `plan-ceo-review`, `autoplan`, `plan-eng-review`, `plan-design-review`, `design-consultation`, `design-shotgun` |
| Work phase | `SKILL.md` and `references/ROUTER.md` | Organize active implementation and validation requests without adding another routing hop | `investigate`, `browse`, `connect-chrome`, `design-html`, `review`, `qa`, `qa-only`, `design-review`, `cso`, `benchmark` |
| Ship phase | `SKILL.md` and `references/ROUTER.md` | Organize release and operational follow-through without adding another routing hop | `ship`, `land-and-deploy`, `canary`, `setup-deploy`, `careful`, `freeze`, `guard`, `unfreeze`, `setup-browser-cookies`, `document-release`, `retro`, `learn`, `gstack-upgrade` |

## Invocation Scenarios

| Trigger Phrase | What Happens |
|---|---|
| "help me think through this idea" | Routes directly to `references/office-hours/SKILL.md` in the `Plan` phase |
| "challenge the scope like a founder" | Routes directly to `references/plan-ceo-review/SKILL.md` in the `Plan` phase |
| "review the architecture before we build" | Routes directly to `references/plan-eng-review/SKILL.md` in the `Plan` phase |
| "design system for this product" | Routes directly to `references/design-consultation/SKILL.md` in the `Plan` phase |
| "debug this broken flow" | Routes directly to `references/investigate/SKILL.md` in the `Work` phase |
| "inspect the live page and capture evidence" | Routes directly to `references/browse/SKILL.md` in the `Work` phase |
| "review the branch and QA the app" | Routes directly to `references/review/SKILL.md` or `references/qa/SKILL.md` in the `Work` phase |
| "run a security check" | Routes directly to `references/cso/SKILL.md` in the `Work` phase |
| "ship this and open the PR" | Routes directly to `references/ship/SKILL.md` in the `Ship` phase |
| "watch the rollout after deploy" | Routes directly to `references/canary/SKILL.md` in the `Ship` phase |
| "lock this directory before I debug" | Routes directly to `references/freeze/SKILL.md` or `references/guard/SKILL.md` in the `Ship` phase |
| "update docs after deploy" | Routes directly to `references/document-release/SKILL.md` in the `Ship` phase |

## Example Usage

### Plan

```text
User: I have a rough product idea and need help narrowing the wedge.

AI routes directly to:
- Skill: `references/office-hours/SKILL.md`
- Phase: `Plan`
- Reason: the request is still deciding what to build
```

### Work

```text
User: the feature is implemented, now debug the flaky part and QA the flow.

AI routes directly to:
- Skills: `references/investigate/SKILL.md`, `references/qa/SKILL.md`
- Phase: `Work`
- Reason: the feature exists but still needs diagnosis and evidence
```

### Ship

```text
User: create the PR, deploy it, then update the docs.

AI routes directly to:
- Skills: `references/ship/SKILL.md`, `references/land-and-deploy/SKILL.md`, `references/document-release/SKILL.md`
- Phase: `Ship`
- Reason: the request is release work plus cleanup
```

## Design Guardrails

1. Single entry point: users invoke `gstack`, not a phase wrapper.
2. Single routing layer: `references/ROUTER.md` routes directly to the concrete skill.
3. Invisible delegation: routing is automatic and does not burden the user.
4. No domain overlap: `Plan`, `Work`, and `Ship` own distinct lifecycle territory.
5. Additive scaling: add a new concrete skill by adding one new router row.

## Harness Agnostic Notes

1. Use only relative skill paths.
2. Do not assume assistant-specific hooks, internal directories, or path conventions.
3. Describe actions in portable terms such as read, route, search, load, run, or verify.

## Customization

| Change | Edit |
|---|---|
| Direct routing rules | `references/ROUTER.md` |
| Concrete skill instructions | `references/<skill>/SKILL.md` |
| User-facing collection copy | `SKILL.md` |

## Maintenance Notes

1. Keep `Plan`, `Work`, and `Ship` as labels, not extra router layers.
2. Add a new concrete skill by attaching it to exactly one phase in `references/ROUTER.md`.
3. Keep the router detailed enough to dispatch directly.

## Notes

- `gstack` is a routing layer, not a replacement for the concrete skills.
- The phase model is preserved for clarity, but the dispatch model stays single-hop.
