# Merge and remove

Use this file when the task is about merging a feature branch back, removing worktrees, or understanding cleanup behavior.

## `wt merge`

Key commands:

```bash
wt merge
wt merge main
wt merge master
```

## Core meaning

`wt merge` merges the current branch into the target branch.
That is different from raw `git merge`, where you usually stand on the target branch and merge another branch into it.

Think of `wt merge` as a local version of clicking a platform merge button.

## Default behavior

By default, `wt merge`:

- squashes commits
- rebases onto the target when needed
- fast-forwards the target branch
- removes the worktree after success

Useful flags:

```bash
wt merge --no-remove
wt merge --no-squash
wt merge --no-commit
wt merge --no-rebase
```

## Normal end-of-task flow

```bash
wt merge main
wt list
```

If the repo still uses `master`, use `wt merge master`.

## `wt remove`

Use `wt remove` when you want cleanup without merging.

```bash
wt remove
wt remove <branch>
wt remove --no-delete-branch <branch>
wt remove --force <branch>
wt remove -D <branch>
```

## Force flags

Two different force concepts matter:

- `--force` or `-f` removes a worktree that has untracked files
- `--force-delete` or `-D` deletes a branch with unmerged commits

Do not conflate them.

## Branch cleanup logic

Docs-backed branch deletion is conservative.
Worktrunk can detect branches that are effectively integrated even when history differs, such as squash-merge or rebase workflows.

That is why `wt remove` is often safer than manually deleting worktree directories and branches.

## When to read more

- Need hooks that run during merge or remove? Read `40-config-hooks-and-automation.md`
- Need rationale or troubleshooting? Read `50-faq-and-troubleshooting.md`
