# FAQ and troubleshooting

Use this file when the task is about why Worktrunk exists, how it compares to branch switching, or how to handle common problems.

## Why Worktrunk instead of plain branch switching?

The docs and FAQ make the same core point:

- branch switching reuses one working directory
- uncommitted changes from one task can block or pollute the next task
- worktrees give each task its own directory and index

That is the main reason this skill pushes work off `main` and `master` before editing.

## Why Worktrunk instead of raw `git worktree`?

Plain `git worktree` works, but Worktrunk adds:

- predictable switching and naming
- `wt list` status across worktrees
- hooks and automation
- merge-and-cleanup workflow with `wt merge`
- safer removal behavior

## Common issues

### `wt switch` did not change directories

Likely shell integration is missing.

```bash
wt config shell install
```

### The default branch changed from `master` to `main`

Clear cached default-branch detection:

```bash
wt config state default-branch clear
```

### The branch exists but has no worktree yet

```bash
wt switch <branch>
```

### Need richer diagnostics before merging

```bash
wt list --full
wt config show --full
```

### Need machine-readable status

```bash
wt list --format=json
```

## Related docs worth consulting

- `tips-patterns` for broader workflow ideas
- `claude-code` integration for agent launch patterns
- `llm-commits` if the user asks how commit messages are generated during merge

## Source URLs

- https://worktrunk.dev/
- https://worktrunk.dev/faq/
- https://worktrunk.dev/tips-patterns/
- https://worktrunk.dev/claude-code/
- https://worktrunk.dev/llm-commits/
