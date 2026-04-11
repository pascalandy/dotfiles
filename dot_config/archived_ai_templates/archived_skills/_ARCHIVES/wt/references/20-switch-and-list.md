# Switch and list

Use this file when the task is about creating worktrees, switching between them, or confirming status.

## `wt switch`

Key commands:

```bash
wt switch --create <branch>
wt switch <branch>
wt switch ^
wt switch --create <branch> --base <base>
```

## Important behavior

- `wt switch --create <branch>` creates a new branch and worktree
- without `--create`, the branch must already exist
- if the branch already has a worktree, `wt switch <branch>` goes there
- `^` means the default branch worktree
- `-` means the previous worktree
- `@` means the current branch or worktree

## Helpful options

```bash
wt switch --create <branch> --base <base>
wt switch --create <branch> --no-verify
wt switch --create <branch> --clobber
wt switch --create <branch> -x '<command>'
```

Use cases:

- `--base` to branch from something other than the default branch
- `--no-verify` to skip hooks
- `--clobber` to remove a stale non-worktree directory at the target path
- `-x` to launch a tool after switching, such as an editor or agent

Example from the docs:

```bash
wt switch --create feature-auth -x claude
```

## `wt list`

Key commands:

```bash
wt list
wt list --full
wt list --format=json
wt list --branches
wt list --remotes
```

Use `wt list` to confirm where you are and what else exists.

## Why `wt list` matters

It shows:

- branch name
- worktree path
- relation to the default branch
- remote status
- optional CI and summary data with `--full`

For scripting:

```bash
wt list --format=json
```

## Common patterns

### Create then confirm

```bash
wt switch --create add-theme-toggle
wt list
```

### Switch back to default branch worktree

```bash
wt switch ^
wt list
```

### Inspect all branches, even without worktrees

```bash
wt list --branches --full
```

## If `wt switch` does not move the shell

That usually means shell integration is missing.
See `40-config-hooks-and-automation.md`.
