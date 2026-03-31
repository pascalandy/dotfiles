# Git Commit

> Create a single, well-crafted git commit from the current working tree changes, following repo conventions and producing clear, value-communicating messages.

## When to Use

- User says "commit", "commit this", "save my changes", "create a commit"
- User wants to commit staged or unstaged work
- Finalizing a unit of work before pushing or opening a PR

## Inputs

- A git repository with changes (staged, unstaged, or both)
- Access to recent commit history for convention detection

## Methodology

### Step 1: Gather context

Run these commands to understand the current state:

```bash
git status
git diff HEAD
git branch --show-current
git log --oneline -10
git rev-parse --abbrev-ref origin/HEAD
```

The last command returns the remote default branch (e.g., `origin/main`). Strip the `origin/` prefix to get the branch name. If the command fails or returns a bare `HEAD`, try:

```bash
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
```

If both fail, fall back to `main`.

**Clean working tree:** If `git status` shows no staged, modified, or untracked files, report that there is nothing to commit and stop.

**Detached HEAD:** Run `git branch --show-current`. If it returns an empty result, the repository is in detached HEAD state. Explain that a branch is required before committing if the user wants this work attached to a branch. Ask whether to create a feature branch now and wait for the answer before proceeding.

- If the user chooses to create a branch, derive the name from the change content, create it with `git checkout -b <branch-name>`, then run `git branch --show-current` again and use that result as the current branch name for the rest of the workflow.
- If the user declines, continue with the detached HEAD commit.

### Step 2: Determine commit message convention

Follow this priority order:

1. **Repo conventions already in context** — If project instructions (AGENTS.md, CLAUDE.md, or similar) are already loaded and specify commit message conventions, follow those. Do not re-read these files; they are loaded at session start.
2. **Recent commit history** — If no explicit convention is documented, examine the 10 most recent commits from Step 1. If a clear pattern emerges (e.g., conventional commits, ticket prefixes, emoji prefixes), match that pattern.
3. **Default: conventional commits** — If neither source provides a pattern, use: `type(scope): description` where type is one of `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `ci`, `style`, `build`.

### Step 3: Consider logical commits

Before staging everything together, scan the changed files for naturally distinct concerns. If modified files clearly group into separate logical changes (e.g., a refactor in one directory and a new feature in another, or test files for a different change than source files), create separate commits for each group.

Keep this lightweight:
- Group at the **file level only** — do not use `git add -p` or try to split hunks within a file.
- If the separation is obvious (different features, unrelated fixes), split. If it's ambiguous, one commit is fine.
- **Two or three logical commits is the sweet spot.** Do not over-slice into many tiny commits.

### Step 4: Stage and commit

Run `git branch --show-current`. If it returns `main`, `master`, or the resolved default branch from Step 1, **warn the user** and ask whether to continue committing here or create a feature branch first. Wait for the answer before proceeding.

- If the user chooses to create a branch, derive the name from the change content, create it with `git checkout -b <branch-name>`, then run `git branch --show-current` again and use that result as the current branch name for the rest of the workflow.

Stage the relevant files. **Prefer staging specific files by name** over `git add -A` or `git add .` to avoid accidentally including sensitive files (`.env`, credentials) or unrelated changes.

Write the commit message:
- **Subject line**: Concise, imperative mood, focused on *why* not *what*. Follow the convention determined in Step 2.
- **Body** (when needed): Add a body separated by a blank line for non-trivial changes. Explain motivation, trade-offs, or anything a future reader would need. Omit the body for obvious single-purpose changes.

Use a heredoc to preserve formatting:

```bash
git commit -m "$(cat <<'EOF'
type(scope): subject line here

Optional body explaining why this change was made,
not just what changed.
EOF
)"
```

### Step 5: Confirm

Run `git status` after the commit to verify success. Report the commit hash(es) and subject line(s).

## Quality Gates

- Working tree checked before attempting commit (stop if clean)
- Detached HEAD detected and resolved or acknowledged before committing
- Committing to `main`/`master`/default branch triggers a warning and user confirmation
- Convention detected and applied (repo docs > commit history > conventional commits)
- Files staged by name, not blindly with `git add -A`
- Subject line is imperative mood and communicates *why*
- `git status` run after commit to verify success

## Outputs

- One or more commits on the current branch
- Reported commit hash(es) and subject line(s)

## Feeds Into

- `git-commit-push-pr` — push commits and open a PR
- `ce:review` / `ce:review-beta` — review before pushing

## Harness Notes

- Blocking user questions (detached HEAD, default branch warning) use the harness's native question tool. If none available, present the options as text and wait for the user's reply before proceeding.
- Convention detection from AGENTS.md / CLAUDE.md assumes those files are already loaded into context at session start; do not re-read them.
