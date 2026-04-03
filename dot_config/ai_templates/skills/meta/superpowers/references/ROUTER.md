---
name: superpowers
description: "Superpowers methodology routing. USE WHEN superpowers, brainstorm, plan, debug, tdd, review, request-review, receive-review, code-reviewer, worktree, subagent, subagent-dev, verify, finish, parallel, execute, write-skill, intro, menu."
---

# Router

Use this table to map explicit Superpowers commands to the correct methodology file.

| Command | Read | Purpose |
|---|---|---|
| `>menu` | `../SKILL.md` | Show the available Superpowers commands |
| `>intro` | `using-superpowers.md` | Explain how the Superpowers workflow set is used |
| `>brainstorm` | `brainstorming.md` | Turn an idea into a reviewed design/spec before implementation |
| `>plan` | `writing-plans.md` | Write an implementation plan from an approved spec |
| `>subagent-dev` | `subagent-driven-development.md` | Execute a plan with a fresh subagent per task |
| `>execute` | `executing-plans.md` | Execute a plan inline in the current session |
| `>tdd` | `test-driven-development.md` | Apply RED-GREEN-REFACTOR discipline |
| `>debug` | `systematic-debugging.md` | Investigate root cause before attempting a fix |
| `>request-review` | `requesting-code-review.md` | Dispatch a code review against explicit scope and git range |
| `>receive-review` | `receiving-code-review.md` | Evaluate review feedback before implementing it |
| `>verify` | `verification-before-completion.md` | Verify the work before claiming success |
| `>worktree` | `using-git-worktrees.md` | Create or manage an isolated git worktree |
| `>finish` | `finishing-a-development-branch.md` | Close out the development branch and choose merge/PR/keep/discard |
| `>parallel` | `dispatching-parallel-agents.md` | Split independent work across parallel agents |
| `>write-skill` | `writing-skills.md` | Create or revise a skill using the Superpowers method |
| `>code-reviewer` | `code-reviewer-agent.md` | Load the standalone reviewer prompt reference |

## Selection Rules

1. Only use this router when the user explicitly asks for Superpowers or sends one of the `>` commands above.
2. If the user names a command directly, read that file and execute it.
3. If the user asks for the menu, show the `>menu` block from `../SKILL.md`.
4. If the methodology mentions harness-specific tools, read `harness-compat.md` before acting.
