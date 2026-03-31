---
name: compound-engineering
description: "Unified compound-engineering meta-skill for shaping work, executing delivery, and reviewing or compounding results. Use when the user needs help deciding what to build, planning implementation, executing code changes, validating work, or capturing reusable learnings through one entry point."
keywords: [compound-engineering, ideate, brainstorm, requirements, plan, architecture, onboarding, implement, execute, code, frontend, rails, ruby, dspy, agent, browser, image, git, worktree, commit, pull request, review, qa, bug, todo, changelog, documentation, learnings, compound]
---

# Compound Engineering

> One entry point for compound-engineering work. Describe the outcome needed, and the router loads the specialist for shaping the work, executing it, or validating and compounding the result.

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

## The Problem

The existing compound-engineering pack already contains a large set of strong, focused skills. The friction is entry-point sprawl:

- Users must know whether to start with ideation, planning, execution, review, or knowledge capture
- Related workflows are easy to miss because they are distributed across many standalone skills
- The skill pack is rich, but its top-level interface is not progressive by default

## The Solution

This meta-skill groups the pack into three non-overlapping lifecycle specialists:

1. `ShapeWork` owns discovery, requirements, planning, and architectural direction before implementation starts.
2. `ExecuteWork` owns implementation, focused builders, automation, and delivery mechanics while work is in flight.
3. `VerifyAndCompound` owns review, validation, feedback resolution, documentation polish, and knowledge capture after or around implementation.

The collection stays readable, the router stays minimal, and each specialist stays standalone.

## What's Included

| Component | Path | Purpose | Workflows |
|---|---|---|---|
| Collection entry point | `SKILL.md` | User-facing overview and invocation guide | N/A |
| Router | `references/ROUTER.md` | Maps requests to the right lifecycle specialist | N/A |
| Shaping specialist | `references/ShapeWork/SKILL.md` | Discovery, requirements, planning, and architecture | `DiscoverDirection`, `DesignTheApproach`, `ChooseSpecializedPatterns` |
| Execution specialist | `references/ExecuteWork/SKILL.md` | Implementation, focused builders, automation, and delivery mechanics | `ImplementFromPlan`, `UseFocusedBuilders`, `ManageDelivery` |
| Verification and knowledge specialist | `references/VerifyAndCompound/SKILL.md` | Review, QA, feedback handling, docs polish, and learnings | `ReviewAndValidate`, `ResolveFeedbackAndTrack`, `CaptureAndShare` |

## Invocation Scenarios

| Trigger Phrase | What Happens |
|---|---|
| "help me think through this feature" | Routes to `ShapeWork`, then runs `DiscoverDirection` |
| "plan this implementation" | Routes to `ShapeWork`, then runs `DesignTheApproach` |
| "what pattern should we use for this agent system" | Routes to `ShapeWork`, then runs `ChooseSpecializedPatterns` |
| "implement this plan" | Routes to `ExecuteWork`, then runs `ImplementFromPlan` |
| "design the frontend for this flow" | Routes to `ExecuteWork`, then runs `UseFocusedBuilders` |
| "create a branch, commit, and open a PR" | Routes to `ExecuteWork`, then runs `ManageDelivery` |
| "review these changes before I ship" | Routes to `VerifyAndCompound`, then runs `ReviewAndValidate` |
| "resolve PR feedback and clean up the todo backlog" | Routes to `VerifyAndCompound`, then runs `ResolveFeedbackAndTrack` |
| "document what we learned from this fix" | Routes to `VerifyAndCompound`, then runs `CaptureAndShare` |

## Example Usage

### Shaping Work

```text
User: we have a vague idea for improving onboarding. help me figure out what to build first.

AI routes to ShapeWork and returns:
- Workflow: `DiscoverDirection`
- Downstream skill: `skills/ce-brainstorm/SKILL.md`
- Reason: the request is still framing the problem and narrowing scope
- Expected artifact: a requirements document or a clear recommended direction
```

### Executing Work

```text
User: implement the approved plan and use the existing Rails style in this repo.

AI routes to ExecuteWork and returns:
- Workflow: `ImplementFromPlan`
- Downstream skill: `skills/ce-work/SKILL.md`
- Supporting specialized pattern: `skills/dhh-rails-style/SKILL.md`
- Expected artifact: finished code changes with verification completed during execution
```

### Verifying and Compounding

```text
User: review the branch, fix the feedback, then write up the learning.

AI routes to VerifyAndCompound and returns:
- Workflow: `ReviewAndValidate` followed by `ResolveFeedbackAndTrack` and `CaptureAndShare`
- Downstream skills: `skills/ce-review/SKILL.md`, `skills/resolve-pr-feedback/SKILL.md`, `skills/ce-compound/SKILL.md`
- Expected artifact: findings resolved, branch hardened, and a reusable solution document captured
```

## Customization

| Area | Location | Purpose |
|---|---|---|
| Root routing keywords | `references/ROUTER.md` | Add a new lifecycle trigger or a new specialist |
| Shaping routes | `references/ShapeWork/workflows/` | Expand pre-implementation guidance |
| Execution routes | `references/ExecuteWork/workflows/` | Expand implementation and delivery routing |
| Verification routes | `references/VerifyAndCompound/workflows/` | Expand review, QA, and knowledge workflows |

## Acceptance Checklist

- [x] Single user-facing entry point
- [x] Router isolated in `references/ROUTER.md`
- [x] Three distinct, non-overlapping lifecycle specialists
- [x] Standalone sub-skills with consistent anatomy
- [x] Additive structure for future compound-engineering modes
