# Worktrunk quickstart

Use this file first when the task is simply: check the branch, avoid `main` or `master`, create a worktree, and proceed.

## Safe default workflow

```bash
git rev-parse --show-toplevel
git branch --show-current
wt switch --create <feature-name>
wt list
# do the work in that worktree
wt merge main
wt list
```

If the repo still uses `master`, merge to `master` instead.

## What to check first

```bash
git rev-parse --show-toplevel
git branch --show-current
```

Interpretation:

- repo check fails → this skill does not apply
- branch is `main` or `master` → leave it before editing
- branch is a feature branch → stay there unless the user wants a new worktree
- branch output is empty → detached HEAD; pause and clarify

## Core commands

### Create or switch to a feature worktree

```bash
wt switch --create <feature-name>
wt switch <branch>
wt switch ^
```

- `--create` creates a new branch and worktree
- without `--create`, the branch must already exist
- `^` switches to the default branch worktree

### Confirm where you are

```bash
wt list
wt list --full
wt list --format=json
```

- `wt list` is the normal confirmation step
- `--full` adds richer status like CI and diff details
- `--format=json` is useful for scripts and automation

### Merge back and clean up

```bash
wt merge
wt merge main
wt merge master
```

`wt merge` merges the current branch into the target branch and usually removes the worktree after success.

## Triage

- Need the guardrail rules? Read `10-core-guardrail.md`
- Need switch and list details? Read `20-switch-and-list.md`
- Need merge or remove behavior? Read `30-merge-and-remove.md`
- Need config, hooks, or shell integration? Read `40-config-hooks-and-automation.md`
- Need rationale or troubleshooting? Read `50-faq-and-troubleshooting.md`
