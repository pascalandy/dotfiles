---
name: superpowers
description: Workflow collection for software development that establishes workflow discipline first, then routes design, planning, execution, debugging, review, verification, and skill-authoring requests to the right specialist. USE WHEN starting a task, deciding which workflow applies, refining requirements, writing a plan, executing a plan, using worktrees, enforcing TDD, debugging bugs, verifying completion, handling code review, or creating skills.
---

# Superpowers

One entry point for a disciplined software-delivery workflow. This collection establishes how to use workflow skills, then routes requests to the right specialist for design, planning, implementation, debugging, review, verification, branch completion, and skill authoring.

## Core Rule

When a workflow skill may apply, use this entrypoint to apply startup discipline first, then load the router before acting. User instructions and repository-specific instructions still win.

Priority order:

1. Direct user instructions
2. Workspace and repository instructions
3. This workflow collection

## What's Included

| Lifecycle | Skill | Purpose |
|---|---|---|
| Design | `brainstorming` | Turn rough requests into an approved design before implementation |
| Planning | `writing-plans` | Convert an approved design into a precise implementation plan |
| Execution | `using-git-worktrees` | Set up an isolated workspace before implementation |
| Execution | `subagent-driven-development` | Execute plans with one worker per task and review loops |
| Execution | `dispatching-parallel-agents` | Split truly independent work across multiple workers |
| Execution | `executing-plans` | Execute a written plan inline when worker delegation is not the right fit |
| Engineering Discipline | `test-driven-development` | Enforce red-green-refactor before writing implementation code |
| Engineering Discipline | `systematic-debugging` | Find root cause before proposing fixes |
| Engineering Discipline | `verification-before-completion` | Require fresh evidence before claiming success |
| Review | `requesting-code-review` | Package context and request a focused code review |
| Review | `receiving-code-review` | Evaluate review feedback rigorously before acting |
| Closure | `finishing-a-development-branch` | Verify, choose merge/PR/keep/discard, and clean up |
| Skill Authoring | `writing-skills` | Create or revise skills using test-first discipline |

## Invocation Scenarios

| Trigger Phrase | What Happens |
|---|---|
| "start this task" / "which workflow applies" | Uses this entrypoint to apply startup rules, then consults the router |
| "help me think through this feature" | Routes to `brainstorming` |
| "write an implementation plan" | Routes to `writing-plans` |
| "set up a worktree" | Routes to `using-git-worktrees` |
| "execute this plan task by task" | Routes to `subagent-driven-development` or `executing-plans` |
| "these three tasks are independent" | Routes to `dispatching-parallel-agents` |
| "fix this bug" | Routes to `systematic-debugging` |
| "implement this change" | Routes to `test-driven-development` |
| "before I say this is done" | Routes to `verification-before-completion` |
| "review these changes" | Routes to `requesting-code-review` |
| "I got review feedback" | Routes to `receiving-code-review` |
| "we're done, how should I wrap this up" | Routes to `finishing-a-development-branch` |
| "create a new skill" | Routes to `writing-skills` |

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

## Startup Behavior

Before taking workflow action:

1. Respect direct user instructions and repository-specific rules first.
2. If any superpowers workflow might apply, load the router before acting.
3. If the task is about workflow selection, discipline, or skill priority, resolve it here in the root entrypoint before choosing a specialist.
4. Prefer process skills before execution skills when multiple specialists might apply.

## Workflow Selection

Use the root `SKILL.md` as the foundation layer for:

1. Starting a task.
2. Deciding which superpowers workflow applies.
3. Establishing instruction priority before any specialist workflow begins.

When several specialists could apply, prefer this order:

1. `brainstorming` for shaping the work before code changes.
2. `writing-plans` for turning approved direction into executable tasks.
3. Execution, debugging, review, and closure skills once the task is ready for that stage.

## Design Notes

- Single entry point: users ask for an outcome, not an internal sub-skill.
- Distinct specialists: each sub-skill owns a separate part of the workflow.
- Foundation behavior lives in the root entrypoint, not in a separate sub-skill.
- Harness agnostic: no platform-specific loading rules, plugin references, or assistant-specific paths.
- Additive structure: adding a new specialist means one new subdirectory and one new router row.
