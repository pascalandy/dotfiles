---
name: superpowers
description: "Use only when the user explicitly asks for superpowers workflows or sends a superpowers `>` command such as `>brainstorm`, `>plan`, `>debug`, or `>tdd`. Routes to the matching superpowers methodology."
keywords: [superpowers, brainstorm, plan, debug, tdd, review, request-review, receive-review, code-reviewer, worktree, subagent, subagent-dev, verify, finish, parallel, execute, write-skill, intro]
---

# Superpowers

> One explicit-entry meta skill for the Superpowers workflow set. It exposes the methodology documents without carrying the upstream plugin repo shape into the active `skills/meta/` tree.

## Routing

Load `references/ROUTER.md` to choose the right methodology.

## How It Works

1. Wait for an explicit user request for Superpowers, or for a `>` command listed in `references/ROUTER.md`.
2. Read the referenced methodology file in full.
3. If the methodology mentions harness-specific capabilities, read `references/harness-compat.md` and map the intent to the current platform.
4. Execute the methodology directly.
5. End with one of: `DONE`, `DONE_WITH_CONCERNS`, `BLOCKED`, `NEEDS_CONTEXT`.

## `>menu`

Show this command list when the user asks for `>menu`:

```text
SUPERPOWERS

THINK
  >intro          How the superpowers workflow set works
  >brainstorm     Refine an idea into a reviewed design/spec

PLAN
  >plan           Write an implementation plan from an approved spec

BUILD
  >subagent-dev   Execute a plan with fresh subagents per task
  >execute        Execute a plan inline in the current session
  >tdd            Apply RED-GREEN-REFACTOR discipline
  >worktree       Create an isolated git worktree for the work
  >parallel       Split independent work across parallel agents

REVIEW
  >request-review Request a code review with explicit context
  >receive-review Evaluate review feedback before implementing it
  >code-reviewer  Load the reviewer prompt reference

TEST
  >debug          Run systematic root-cause debugging
  >verify         Verify the work before claiming completion

SHIP
  >finish         Close out the development branch

META
  >write-skill    Write or revise a skill using the superpowers method
```

## Included References

- `references/using-superpowers.md`
- `references/brainstorming.md`
- `references/writing-plans.md`
- `references/subagent-driven-development.md`
- `references/executing-plans.md`
- `references/test-driven-development.md`
- `references/systematic-debugging.md`
- `references/requesting-code-review.md`
- `references/receiving-code-review.md`
- `references/verification-before-completion.md`
- `references/using-git-worktrees.md`
- `references/finishing-a-development-branch.md`
- `references/dispatching-parallel-agents.md`
- `references/writing-skills.md`
- `references/code-reviewer-agent.md`
- `references/harness-compat.md`

## Notes

- This meta skill is explicit-entry by design. Do not auto-trigger it from vague overlap with other planning or coding skills.
- The active directory intentionally contains only the runtime skill payload: `SKILL.md`, `references/`, and `UPSTREAM.lock`.
