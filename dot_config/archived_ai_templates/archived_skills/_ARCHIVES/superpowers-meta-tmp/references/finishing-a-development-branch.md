# Finishing a Development Branch

> Guide completion of development work by verifying tests, presenting structured integration options, and executing the chosen workflow.

## When to Use

Use when implementation is complete, all tasks are done, and you need to decide how to integrate the work — merge locally, create a PR, keep the branch, or discard it.

## Inputs

- A completed feature branch with committed work
- A passing test suite (or knowledge of what's failing)
- Access to the base branch (main/master or equivalent)

## Methodology

### Announce at Start

State: "I'm using the finishing-a-development-branch skill to complete this work."

### Step 1: Verify Tests

Run the project's test suite before doing anything else:

```bash
npm test
# or: cargo test / pytest / go test ./...
```

**If tests fail:**
```
Tests failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until tests pass.
```

Stop. Do NOT proceed to Step 2 until tests pass.

**If tests pass:** Continue to Step 2.

### Step 2: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

Or ask: "This branch split from main - is that correct?"

### Step 3: Present Options

Present **exactly these 4 options** (no more, no less, no added explanation):

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

Do NOT add explanation — keep options concise.

### Step 4: Execute Choice

#### Option 1: Merge Locally

```bash
# Switch to base branch
git checkout <base-branch>

# Pull latest
git pull

# Merge feature branch
git merge <feature-branch>

# Verify tests on merged result
<test command>

# If tests pass
git branch -d <feature-branch>
```

Then proceed to Step 5 (Cleanup Worktree).

#### Option 2: Push and Create PR

```bash
# Push branch
git push -u origin <feature-branch>

# Create PR
gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <verification steps>
EOF
)"
```

Then proceed to Step 5 (Cleanup Worktree).

#### Option 3: Keep As-Is

Report: "Keeping branch <name>. Worktree preserved at <path>."

**Do NOT cleanup worktree.**

#### Option 4: Discard

**Confirm first — require typed confirmation:**

```
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for the exact word "discard". Do not proceed without it.

If confirmed:
```bash
git checkout <base-branch>
git branch -D <feature-branch>
```

Then proceed to Step 5 (Cleanup Worktree).

### Step 5: Cleanup Worktree

**For Options 1, 2, 4:** Check if currently in a worktree:
```bash
git worktree list | grep $(git branch --show-current)
```

If yes, remove it:
```bash
git worktree remove <worktree-path>
```

**For Option 3:** Keep the worktree — do NOT remove it.

---

## Quick Reference

| Option          | Merge | Push | Keep Worktree | Cleanup Branch |
|-----------------|-------|------|---------------|----------------|
| 1. Merge locally | ✓    | -    | -             | ✓              |
| 2. Create PR    | -     | ✓    | ✓             | -              |
| 3. Keep as-is   | -     | -    | ✓             | -              |
| 4. Discard      | -     | -    | -             | ✓ (force)      |

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Skipping test verification | Merge broken code, create failing PR | Always verify tests before offering options |
| Open-ended questions | "What should I do next?" is ambiguous | Present exactly 4 structured options |
| Automatic worktree cleanup | Remove worktree when it might still be needed | Only cleanup for Options 1 and 4 |
| No confirmation for discard | Accidentally delete work | Require typed "discard" confirmation |

---

## Red Flags

**Never:**
- Proceed with failing tests
- Merge without verifying tests on the merged result
- Delete work without typed "discard" confirmation
- Force-push without explicit request from the user

**Always:**
- Verify tests before offering options
- Present exactly 4 options
- Get typed "discard" confirmation for Option 4
- Clean up worktree for Options 1 & 4 only

## Quality Gates

- [ ] Test suite run before presenting options
- [ ] Tests passing (or user explicitly acknowledged failures)
- [ ] Base branch identified correctly
- [ ] Exactly 4 options presented with no extraneous content
- [ ] For Option 1: tests re-verified on merged result
- [ ] For Option 4: typed "discard" confirmation received before any deletion
- [ ] Worktree cleaned up for Options 1 and 4; preserved for Options 2 and 3

## Outputs

- Branch integrated according to chosen option (merged, PR created, kept, or discarded)
- Worktree cleaned up (Options 1 and 4) or preserved (Options 2 and 3)

## Feeds Into

- For Option 2: PR review process
- For Options 1/3: continued development or project closure

## Harness Notes

Option 2 uses the `gh` CLI to create pull requests. If `gh` is not available, provide the push command and instruct the user to create the PR manually. The PR body template uses a heredoc; adapt the syntax if the shell does not support it.
