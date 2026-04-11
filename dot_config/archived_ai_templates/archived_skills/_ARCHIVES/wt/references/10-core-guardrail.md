# Core guardrail

Use this file when the task is about whether to stay on the current branch or move work into a Worktrunk worktree.

## Rule

Do not start implementation work on `main` or `master`.

Check first:

```bash
git rev-parse --show-toplevel
git branch --show-current
```

## Decision table

| Current state | Action |
| --- | --- |
| Not in a Git repo | This skill does not apply |
| `main` or `master` | Create or switch to a feature worktree before editing |
| Feature branch with a worktree | Stay there and continue |
| Existing branch without a worktree | `wt switch <branch>` |
| Detached HEAD | Pause and clarify before editing |

## When on `main` or `master`

Use a clear kebab-case branch name that matches the task.

```bash
wt switch --create <feature-name>
wt list
```

If the task must branch from something other than the default branch:

```bash
wt switch --create <feature-name> --base <branch>
wt list
```

## When already on a feature branch

Usually continue in place.
Only propose a new worktree if:

- the user wants isolated parallel work
- the current branch is the wrong branch for the task
- the branch has become a dumping ground for unrelated changes

## Detached HEAD

If `git branch --show-current` returns nothing, avoid making edits until the user confirms the desired branch strategy.

Good response shape:

- say you are in detached HEAD
- avoid making changes yet
- ask whether to create a new feature branch with `wt switch --create <feature-name>` or switch to an existing one

## If the user asks for raw Git commands

This environment prefers `wt`.
If the user explicitly asks for `git worktree` commands, answer directly, but note that Worktrunk is the standard local workflow because it adds status, hooks, and cleanup.
