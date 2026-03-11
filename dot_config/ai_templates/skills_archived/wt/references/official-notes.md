# Worktrunk official notes

A compact reference distilled from the official Worktrunk docs and FAQ.
Use local CLI help when exact syntax matters.

## Core idea

Worktrunk is a CLI for Git worktree management built for parallel AI agent workflows.

Official positioning:

- branch switching keeps one working directory
- worktrees isolate work into separate directories and indexes
- Worktrunk wraps that workflow with better switching, status, hooks, and cleanup

## Why this skill pushes work off `main` / `master`

From the FAQ's comparison with branch switching:

- uncommitted changes from one task can leak into the next when you reuse one directory
- switching branches can be blocked by local changes
- worktrees avoid that by giving each task its own directory

That matches the rule this skill enforces: if you are on `main` or `master`, move to a feature worktree before editing.

## Key commands

### Create or switch

```bash
wt switch --create <branch>
wt switch <branch>
wt switch ^
```

Docs-backed notes:

- `wt switch --create <branch>` creates a new branch and worktree
- without `--create`, the branch must already exist
- `^` is the shortcut for the default branch worktree
- if a worktree already exists for that branch, `wt switch` goes there instead of creating another one

### Confirm status

```bash
wt list
wt list --full
wt list --format=json
```

Docs-backed notes:

- `wt list` shows worktrees and their status
- `--full` adds slower or richer info like CI, diff analysis, and optional summaries
- JSON output is available for scripting

### Merge and clean up

```bash
wt merge
wt merge main
wt merge master
```

Docs-backed notes:

- `wt merge` merges the current branch into the target branch
- target defaults to the repo's default branch
- default behavior is squash + rebase + fast-forward target + remove worktree
- this behaves more like a local “merge PR” action than raw `git merge`

## Helpful config facts

### Shell integration

```bash
wt config shell install
```

If shell integration is missing, Worktrunk can report the target directory but cannot change the parent shell's directory automatically.

### Show config

```bash
wt config show
wt config show --full
```

Use this to inspect user config, project config, and diagnostics.

### Default branch detection cache

If the remote default branch changes, for example from `master` to `main`, clear cached detection with:

```bash
wt config state default-branch clear
```

## FAQ takeaways relevant to this skill

- Worktrunk can be used alongside Git TUIs; the TUIs operate inside each worktree
- worktree paths are configurable via `worktree-path`
- `wt remove` removes worktrees and branch cleanup has safeguards
- Worktrunk creates worktree directories plus config/state files; it is not just a thin alias for `git worktree`

## Source URLs

- https://worktrunk.dev/
- https://worktrunk.dev/faq/
- https://worktrunk.dev/switch/
- https://worktrunk.dev/list/
- https://worktrunk.dev/merge/
- https://worktrunk.dev/config/
