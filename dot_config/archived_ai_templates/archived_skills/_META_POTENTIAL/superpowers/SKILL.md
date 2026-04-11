---
name: superpowers
description: Disciplined engineering workflow collection — planning, execution, TDD, debugging, subagents, git worktrees, code review, verification, shipping, and skill authoring. USE WHEN starting any task, brainstorming, writing or executing a plan, doing test-driven development, debugging systematically, dispatching subagents or parallel agents, using git worktrees, requesting or receiving code review, verifying completion before done, finishing a development branch, or authoring new skills.
---

# Superpowers

> A collection of disciplined engineering workflow skills. One entry point, many specialists.

## Problem

Good engineering requires different disciplines at different moments: brainstorming before planning, planning before execution, TDD while coding, systematic debugging when stuck, verification before declaring done, and review before shipping. Loading every discipline for every task is noisy; remembering to invoke the right one manually is unreliable.

## Solution

`superpowers` is a single entry point that dispatches to the right discipline based on what you're doing. You describe the task; the router loads the specialist.

## What's Included

| Phase | Sub-skill | Purpose |
|---|---|---|
| **Foundation** | `using-superpowers` | How to find and invoke skills — the discipline that makes the rest work |
| **Plan** | `brainstorming` | Explore and shape an idea before committing to a plan |
| **Plan** | `writing-plans` | Turn an idea into a concrete implementation plan |
| **Execute** | `executing-plans` | Work through a plan methodically |
| **Execute** | `test-driven-development` | Red → green → refactor discipline |
| **Execute** | `systematic-debugging` | Root-cause debugging instead of guess-and-check |
| **Execute** | `subagent-driven-development` | Delegate discrete tasks to subagents |
| **Execute** | `dispatching-parallel-agents` | Fan out independent work across agents |
| **Execute** | `using-git-worktrees` | Isolated workspaces for parallel branches |
| **Review & Ship** | `requesting-code-review` | Send work out for review |
| **Review & Ship** | `receiving-code-review` | Respond to review feedback productively |
| **Review & Ship** | `verification-before-completion` | Verify before claiming done |
| **Review & Ship** | `finishing-a-development-branch` | Wrap up and ship a branch cleanly |
| **Author** | `writing-skills` | Create new skills following best practices |

## Invocation

| Trigger | What happens |
|---|---|
| "start any task" / beginning of conversation | `using-superpowers` loads first |
| "let's brainstorm X" | `brainstorming` |
| "write a plan for X" | `writing-plans` |
| "execute the plan" | `executing-plans` |
| "do this TDD" | `test-driven-development` |
| "debug this" | `systematic-debugging` |
| "delegate to subagents" | `subagent-driven-development` |
| "run these in parallel" | `dispatching-parallel-agents` |
| "use a worktree" | `using-git-worktrees` |
| "request review" | `requesting-code-review` |
| "address review comments" | `receiving-code-review` |
| "verify it's done" | `verification-before-completion` |
| "finish the branch" | `finishing-a-development-branch` |
| "write a new skill" | `writing-skills` |

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.
