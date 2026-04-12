---
title: Superpowers Workflow
summary: Captures the Superpowers workflow entry, invocation scenarios, and router table linking requests to lifecycle specialists.
tags: []
keywords: []
importance: 53
recency: 1
maturity: draft
accessCount: 1
createdAt: '2026-04-12T19:35:06.738Z'
updatedAt: '2026-04-12T19:35:06.738Z'
---
## Reason
Document the harness-agnostic Superpowers meta-skill entrypoint and router tables.

## Raw Concept
**Task:**
Document the Superpowers meta-skill entrypoint, invocation phrases, and router dispatch table so the workflow can be applied harness-agnostically.

**Changes:**
- Added harness-agnostic routing rules with explicit instruction priority
- Captured 13 lifecycle specialists, their purposes, and example trigger phrases
- Documented router mappings from request patterns to each references/<skill>/MetaSkill.md file

**Files:**
- .agents/skills/meta/superpowers/SKILL.md
- .agents/skills/meta/superpowers/references/ROUTER.md

**Flow:**
User request -> Superpowers SKILL entry -> Router selection -> Delegate to the matched MetaSkill reference -> Specialist workflow execution

**Timestamp:** 2026-04-12

**Author:** ByteRover context engineer

## Narrative
### Structure
Root SKILL.md defines the collection description, core rule, and tables of lifecycle specialists plus invocation scenarios.

Lifecycle table:
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

Invocation scenarios table:
| Trigger Phrase | What Happens |
|---|---|
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

Routing table from references/ROUTER.md:
| Request Pattern | Route To |
|---|---|
| brainstorm, design, spec, requirements, scope, approaches, before coding | `brainstorming/MetaSkill.md` |
| plan, implementation plan, task breakdown, task-by-task execution plan | `writing-plans/MetaSkill.md` |
| worktree, isolated branch, isolated workspace, separate workspace | `using-git-worktrees/MetaSkill.md` |
| execute plan in this session, one worker per task, review loops, task-by-task delegation | `subagent-driven-development/MetaSkill.md` |
| multiple independent tasks, parallel workers, concurrent investigations, split independent work | `dispatching-parallel-agents/MetaSkill.md` |
| execute written plan inline, batch execution, separate session execution | `executing-plans/MetaSkill.md` |
| TDD, test first, red green refactor, implement feature, implement bugfix | `test-driven-development/MetaSkill.md` |
| debug, root cause, test failure, unexpected behavior, flaky behavior, build failure | `systematic-debugging/MetaSkill.md` |
| verify before claiming done, before commit, before PR, prove it passes | `verification-before-completion/MetaSkill.md` |
| request code review, review these changes, reviewer prompt, review before merge | `requesting-code-review/MetaSkill.md` |
| receiving review feedback, respond to review, evaluate reviewer suggestions, push back on review | `receiving-code-review/MetaSkill.md` |
| finish branch, merge or PR, wrap up implementation, clean up worktree | `finishing-a-development-branch/MetaSkill.md` |
| create skill, edit skill, test a skill, author a skill | `writing-skills/MetaSkill.md` |

### Dependencies
Node of the workflow is the references/ROUTER.md table; each route points to references/<skill>/MetaSkill.md, so related sub-skill artifacts must exist before relying on this router.

### Highlights
Single entry point with prioritized instructions, 13 lifecycle specialists organized by purpose, and exact trigger phrases for each helper route ensure a disciplined workflow.

### Rules
Core rules derived from design notes:
1. Load the router before acting.
2. Respect the instruction priority order: (1) Direct user instructions (2) Workspace and repository instructions (3) This workflow collection.
3. Treat the collection as additive: adding a specialist means creating one new subdirectory and router row.
4. Keep harness references removed, replace platform-specific tool mentions with neutral delegation language, and rewrite intra-skill links to local references/ paths.

## Facts
- **superpowers_router_usage**: The Superpowers router must be loaded before acting so the right specialist handles each workflow request. [convention]
- **superpowers_instruction_priority**: Instruction priority follows user instructions, workspace/repo instructions, then this workflow collection. [convention]
- **superpowers_router_table**: The router table lists 13 lifecycle request patterns linking to references/<skill>/MetaSkill.md documents. [project]
