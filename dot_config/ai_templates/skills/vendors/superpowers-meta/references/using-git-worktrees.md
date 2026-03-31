# Using Git Worktrees

> Create isolated git workspaces sharing the same repository — systematic directory selection plus safety verification gives reliable isolation.

## When to Use

- Before executing implementation plans (REQUIRED by subagent-driven-development and executing-plans)
- When starting feature work that needs isolation from the current workspace
- Any time a skill requires an isolated workspace

**Announce at start:** "I'm using the using-git-worktrees skill to set up an isolated workspace."

## Inputs

- A git repository
- A branch name for the new worktree
- User preference for worktree location (resolved via priority order below)

## Methodology

### Step 1: Directory Selection (follow priority order)

#### Priority 1 — Check Existing Directories

Check in this order:

```bash
ls -d .worktrees 2>/dev/null   # Preferred (hidden)
ls -d worktrees 2>/dev/null    # Alternative
```

- If `.worktrees/` exists → use it
- If `worktrees/` exists → use it
- If BOTH exist → `.worktrees/` wins

#### Priority 2 — Check Project Documentation

```bash
grep -i "worktree.*director" CLAUDE.md 2>/dev/null
```

If a preference is specified → use it without asking.

#### Priority 3 — Ask the User

If no directory exists and no documented preference:

```
No worktree directory found. Where should I create worktrees?

1. .worktrees/ (project-local, hidden)
2. ~/.config/superpowers/worktrees/<project-name>/ (global location)

Which would you prefer?
```

---

### Step 2: Safety Verification

#### For project-local directories (`.worktrees/` or `worktrees/`)

**MUST verify the directory is ignored before creating the worktree:**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**If NOT ignored:**

Per "fix broken things immediately" rule:
1. Add the appropriate line to `.gitignore`
2. Commit the change
3. Proceed with worktree creation

**Why critical:** Prevents accidentally committing worktree contents to the repository.

#### For global directory (`~/.config/superpowers/worktrees/`)

No `.gitignore` verification needed — the directory is entirely outside the project.

---

### Step 3: Create the Worktree

#### 3a. Detect project name

```bash
project=$(basename "$(git rev-parse --show-toplevel)")
```

#### 3b. Determine full path

```bash
case $LOCATION in
  .worktrees|worktrees)
    path="$LOCATION/$BRANCH_NAME"
    ;;
  ~/.config/superpowers/worktrees/*)
    path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"
    ;;
esac
```

#### 3c. Create worktree with new branch

```bash
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

---

### Step 4: Run Project Setup

Auto-detect and run the appropriate setup command:

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

If no recognized project file exists, skip dependency installation.

---

### Step 5: Verify Clean Baseline

Run the project test suite to confirm the worktree starts in a clean state:

```bash
# Use the project-appropriate command, e.g.:
npm test
cargo test
pytest
go test ./...
```

**If tests fail:** Report the failures and ask whether to proceed or investigate.

**If tests pass:** Report ready.

---

### Step 6: Report Location

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

---

## Quick Reference

| Situation | Action |
|-----------|--------|
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check project docs → Ask user |
| Directory not ignored | Add to `.gitignore` + commit first |
| Tests fail during baseline | Report failures + ask permission to proceed |
| No package.json/Cargo.toml/etc. | Skip dependency install |

---

## Common Mistakes

### Skipping ignore verification
- **Problem:** Worktree contents get tracked, pollute git status
- **Fix:** Always run `git check-ignore` before creating a project-local worktree

### Assuming directory location
- **Problem:** Creates inconsistency, violates project conventions
- **Fix:** Follow priority: existing directory > project docs > ask user

### Proceeding with failing tests
- **Problem:** Cannot distinguish new bugs from pre-existing issues
- **Fix:** Report failures and get explicit permission before proceeding

### Hardcoding setup commands
- **Problem:** Breaks on projects using different toolchains
- **Fix:** Auto-detect from project files (package.json, Cargo.toml, etc.)

---

## Quality Gates

**Never:**
- Create a project-local worktree without verifying it is ignored
- Skip baseline test verification
- Proceed with failing tests without asking
- Assume directory location when ambiguous
- Skip project documentation check

**Always:**
- Follow directory priority: existing > project docs > ask
- Verify directory is ignored for project-local locations
- Auto-detect and run project setup
- Verify clean test baseline before reporting ready

---

## Outputs

- Isolated git worktree on a new branch
- Dependencies installed
- Clean test baseline confirmed
- Full path reported to caller

## Feeds Into

- **subagent-driven-development** — REQUIRED before executing any tasks
- **executing-plans** — REQUIRED before executing any tasks
- **finishing-a-development-branch** — REQUIRED for cleanup after work is complete
- Any skill or workflow that needs an isolated workspace

## Harness Notes

The skill is called by brainstorming (Phase 4) when design is approved and implementation follows. It is a prerequisite gate — no implementation skill should start without it.
