# Git Worktree Manager

> Manage Git worktrees for isolated parallel development: create, list, switch, and clean up worktrees with env-file copying and dev-tool trust guardrails.

## When to Use

- **Code Review**: When NOT already on the target PR branch, offer a worktree for isolated review.
- **Feature Work**: When starting work, ask whether to use a new branch on the current worktree (live) or a new worktree (parallel).
- **Parallel Development**: Working on multiple features simultaneously.
- **Cleanup**: After completing work in a worktree.

## Inputs

- A branch name to create or operate on.
- Optionally a base branch (defaults to `main`).
- A `worktree-manager.sh` script (bundled at `scripts/worktree-manager.sh`).

## Methodology

### Critical Rule: Always Use the Manager Script

**Never call `git worktree add` directly.** Always invoke `worktree-manager.sh`. The script handles:
1. Copying `.env`, `.env.local`, `.env.test`, etc. from the main repo.
2. Trusting dev-tool configs with branch-aware safety rules:
   - **mise**: auto-trust only when config is unchanged from a trusted baseline branch.
   - **direnv**: auto-allow only for trusted base branches; review worktrees remain manual.
3. Ensuring `.worktrees` is added to `.gitignore`.
4. Creating a consistent directory structure.

```
# Correct
bash scripts/worktree-manager.sh create feature-name

# Wrong — never do this directly
git worktree add .worktrees/feature-name -b feature-name main
```

---

### Commands

#### `create <branch-name> [from-branch]`

Creates a new worktree with the given branch name.

- `branch-name` (required): Name for the new branch and worktree directory.
- `from-branch` (optional): Base branch (defaults to `main`).

**Steps performed:**
1. Check if worktree already exists.
2. Update the base branch from remote.
3. Create new worktree and branch.
4. Copy all `.env*` files from main repo (`.env`, `.env.local`, `.env.test`, etc.).
5. Trust dev-tool configs with branch-aware safety rules:
   - Trusted bases (`main`, `develop`, `dev`, `trunk`, `staging`, `release/*`) compare against themselves.
   - Other branches compare against the default branch.
   - `direnv` auto-allow is skipped on non-trusted bases because `.envrc` can source unchecked files.
6. Show the path for navigating to the worktree.

#### `list` / `ls`

Lists all worktrees with their branches, current status, and which is active (marked `✓`).

#### `switch <name>` / `go <name>`

Switches to an existing worktree. If name is omitted, lists available worktrees and prompts for selection.

#### `copy-env <name>`

Copies `.env*` files to an existing worktree (use when a worktree was created via raw git commands that skipped the script).

#### `cleanup` / `clean`

Interactively removes inactive worktrees:
1. Lists all inactive worktrees.
2. Asks for confirmation.
3. Removes selected worktrees and cleans up empty directories.

**Safety:** Will not remove the current worktree. Returns a clear error if attempted.

---

### Integration Decision Logic

#### In Code Review Workflows

```
1. Check current branch.
2. If ALREADY on the target branch (PR branch or requested branch)
   → stay there, no worktree needed.
3. If on a DIFFERENT branch than the review target
   → offer: "Use worktree for isolated review? (y/n)"
      yes → run worktree-manager.sh create <branch>
      no  → proceed with PR diff on current branch
```

#### In Feature Work Workflows

```
1. Ask: "How do you want to work?
   1. New branch on current worktree (live work)
   2. New worktree (parallel work)"
2. Choice 1 → create new branch normally
3. Choice 2 → run worktree-manager.sh create <branch> from main
```

---

### Directory Structure

```
.worktrees/
├── feature-login/          # Worktree 1
│   ├── .git
│   ├── app/
│   └── ...
├── feature-notifications/  # Worktree 2
│   ├── .git
│   ├── app/
│   └── ...
└── ...

.gitignore  (updated to include .worktrees/)
```

---

### Troubleshooting

| Problem | Solution |
|---------|----------|
| "Worktree already exists" | Script asks if you want to switch to it instead. |
| "Cannot remove: it is the current worktree" | Navigate to the main repo root first, then run cleanup. |
| `.env` files missing in worktree | Run `worktree-manager.sh copy-env <name>`. |
| Lost in a worktree | Run `worktree-manager.sh list` to see your position. |
| Navigate to main repo root | Run `cd $(git rev-parse --show-toplevel)`. |

---

### Technical Notes

- Worktrees are created with `git worktree add` — lightweight file-system links, no repository duplication.
- Each worktree has its own branch; changes do not affect other worktrees.
- All worktrees share git history and objects with the main repo.
- Changes can be pushed from any worktree.
- Worktrees are faster to create than clones and avoid stash/switch disruption.

## Quality Gates

- [ ] Worktree created via `worktree-manager.sh`, never raw `git worktree add`.
- [ ] `.env*` files present in new worktree.
- [ ] `.worktrees/` present in `.gitignore`.
- [ ] Confirmed before creating or removing any worktree (interactive prompt).
- [ ] Not attempting to remove the current (active) worktree.
- [ ] Dev-tool trust applied only for trusted base branches.

## Outputs

- A new isolated worktree at `.worktrees/<branch-name>/` with env files copied.
- Updated `.gitignore` entry.
- Terminal output showing the path to `cd` into.

## Feeds Into

- `ce:review` — isolated review environment.
- `ce:work` — parallel feature development.
- Cleanup step after review or feature completion.

## Harness Notes

The script path `scripts/worktree-manager.sh` is relative to the skill directory. Adapt the path resolution to the harness's plugin root convention. The script is a standard Bash script and can be run in any POSIX-compatible shell.
