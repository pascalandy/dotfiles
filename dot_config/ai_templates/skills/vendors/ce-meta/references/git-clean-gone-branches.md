# Git Clean Gone Branches

> Delete local branches whose remote tracking branch has been deleted, including any associated worktrees.

## When to Use

- User says "clean up branches", "delete gone branches", "prune local branches", "clean gone"
- Removing stale local branches that no longer exist on the remote
- After a sprint or project phase when many feature branches have been merged and deleted remotely

## Inputs

- A git repository with at least one remote configured
- (Optional) worktrees associated with branches to be cleaned

## Methodology

### Step 1: Discover gone branches

Run the following script to fetch the latest remote state and identify gone branches:

```bash
#!/usr/bin/env bash
# List local branches whose remote tracking branch is gone.
# Outputs one branch name per line, or __NONE__ if none found.

set -euo pipefail

# Ensure we have current remote state
git fetch --prune 2>/dev/null

# Find branches marked [gone] in tracking info.
# `git branch -vv` output format:
#   * main           abc1234 [origin/main] commit msg
#   + feature-x      def5678 [origin/feature-x: gone] commit msg
#     old-branch     789abcd [origin/old-branch: gone] commit msg
#
# The leading column can be: ' ' (normal), '*' (current), '+' (worktree).
# We match lines containing ": gone]" to find branches whose remote is deleted.

gone_branches=()

while IFS= read -r line; do
  # Skip the currently checked-out branch (marked with '*').
  # git branch -D cannot delete the active branch.
  if [[ "$line" =~ ^\* ]]; then
    continue
  fi

  # Strip the leading marker character(s) and whitespace.
  # The branch name is the first non-whitespace token after the marker.
  branch_name=$(echo "$line" | sed 's/^[+* ]*//' | awk '{print $1}')

  # Validate: skip empty, skip if it looks like a hash or flag, skip HEAD
  if [[ -z "$branch_name" ]] || [[ "$branch_name" =~ ^[0-9a-f]{7,}$ ]] || [[ "$branch_name" == "HEAD" ]]; then
    continue
  fi

  gone_branches+=("$branch_name")
done < <(git branch -vv 2>/dev/null | grep ': gone]')

if [[ ${#gone_branches[@]} -eq 0 ]]; then
  echo "__NONE__"
  exit 0
fi

for branch in "${gone_branches[@]}"; do
  echo "$branch"
done
```

If the script outputs `__NONE__`, report that no stale branches were found and stop.

### Step 2: Present branches and ask for confirmation

Show the user the list of branches that will be deleted. Format as a simple list:

```
These local branches have been deleted from the remote:

  - feature/old-thing
  - bugfix/resolved-issue
  - experiment/abandoned

Delete all of them? (y/n)
```

Prompt the user for confirmation and wait for their answer before proceeding.

This is a **yes-or-no decision on the entire list** — do not offer multi-selection or per-branch choices.

### Step 3: Delete confirmed branches

If the user confirms, delete each branch. For each branch:

1. Check if it has an associated worktree:
   ```bash
   git worktree list | grep "\[$branch\]"
   ```
2. If a worktree exists and is **not** the main repo root, remove it first:
   ```bash
   git worktree remove --force "$worktree_path"
   ```
3. Delete the branch:
   ```bash
   git branch -D "$branch"
   ```

Report results as you go:

```
Removed worktree: .worktrees/feature/old-thing
Deleted branch: feature/old-thing
Deleted branch: bugfix/resolved-issue
Deleted branch: experiment/abandoned

Cleaned up 3 branches.
```

If the user declines, acknowledge and stop without deleting anything.

## Quality Gates

- `git fetch --prune` was run to ensure remote state is current
- User explicitly confirmed before any deletion
- Worktrees removed before their associated branch is deleted
- Currently checked-out branch is never included in the deletion list

## Outputs

- Summary of deleted branches (and removed worktrees, if any)
- "No stale branches found" message if none exist
- No-op confirmation if user declines

## Feeds Into

- `git-commit` / `git-commit-push-pr` — after cleanup, fresh branch work can begin
- Any workflow that benefits from a tidy local branch list

## Harness Notes

- The discovery script is a self-contained bash script; run it in the terminal.
- User confirmation uses the harness's native blocking question tool. If none is available, present the list and wait for the user's reply in the conversation before proceeding.
