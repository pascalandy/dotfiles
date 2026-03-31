# Git Commit, Push, and PR

> Go from working tree changes to an open pull request in a single workflow, or update an existing PR description with adaptive, value-first content proportional to the complexity of the change.

## When to Use

- User says "commit and PR", "push and open a PR", "ship this", "create a PR", "open a pull request", "commit push PR"
- User wants to go from working changes to an open pull request in one step
- User says "update the PR description", "refresh the PR description", "freshen the PR", or wants to rewrite an existing PR description

## Inputs

- A git repository with changes or unpushed commits
- `gh` CLI authenticated and configured
- Access to recent commit history for convention detection

## Methodology

### Mode Detection

If the user is asking to **update, refresh, or rewrite an existing PR description** (with no mention of committing or pushing), this is a **description-only update**. The user may also provide a focus for the update (e.g., "update the PR description and add the benchmarking results"). Note any focus instructions for use in DU-3.

For description-only updates, follow the **Description Update workflow** below. Otherwise, follow the **Full workflow**.

---

### Reusable PR Probe

When checking whether the current branch already has a PR, always use current-branch `gh pr view` semantics. Do **not** switch to `gh pr list --head "<branch>"` — that branch-name search can select the wrong PR in multi-fork repos.

Capture the output and exit code so "no PR for this branch" is treated as a normal workflow state (not an error):

```bash
if PR_VIEW_OUTPUT=$(gh pr view --json url,title,state 2>&1); then
  PR_VIEW_EXIT=0
else
  PR_VIEW_EXIT=$?
fi
printf '%s\n__GH_PR_VIEW_EXIT__=%s\n' "$PR_VIEW_OUTPUT" "$PR_VIEW_EXIT"
```

Interpret as:

| Condition | Meaning |
|---|---|
| Exit 0, JSON with `state: OPEN` | Open PR exists for current branch |
| Exit 0, JSON with non-OPEN state | Treat as no open PR |
| Non-zero exit + "no pull requests found for branch" | Normal no-PR state |
| Any other non-zero exit | Real error (auth, network, repo config) — report and stop |

---

## Description Update Workflow

### DU-1: Confirm intent

Ask the user to confirm: "Update the PR description for this branch?" Wait for the answer before proceeding. If the user declines, stop.

### DU-2: Find the PR

```bash
git branch --show-current
```

If empty (detached HEAD), report that there is no branch to update and stop.

Check for an existing open PR using the Reusable PR probe above.

- If it returns PR data with `state: OPEN` — an open PR exists.
- If it returns PR data with a non-OPEN state — report that no open PR exists for this branch and stop.
- If it exits non-zero indicating no PR — report that no open PR exists for this branch and stop.
- If it errors for another reason — report the error and stop.

### DU-3: Write and apply the updated description

Read the current PR description:

```bash
gh pr view --json body --jq '.body'
```

Follow the "Detect the base branch and remote" and "Gather the branch scope" sections (from Step 6 of the full workflow) to get the full branch diff. Then write a new description following the writing principles in Step 6. If the user provided a focus, incorporate it alongside the branch diff context.

Compare the new description against the current one and summarize the substantial changes for the user (e.g., "Added coverage of the new caching layer, updated test plan, removed outdated migration notes"). If the user provided a focus, confirm it was addressed. Ask the user to confirm before applying and wait for their answer.

If confirmed, apply:

```bash
gh pr edit --body "$(cat <<'EOF'
Updated description here
EOF
)"
```

Report the PR URL.

---

## Full Workflow

### Step 1: Gather context

```bash
git status
git diff HEAD
git branch --show-current
git log --oneline -10
git rev-parse --abbrev-ref origin/HEAD
```

The last command returns the remote default branch (e.g., `origin/main`). Strip the `origin/` prefix. If the command fails or returns a bare `HEAD`, try:

```bash
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
```

If both fail, fall back to `main`.

**Detached HEAD:** If `git branch --show-current` returns empty, explain that a branch is required before committing and pushing. Ask whether to create a feature branch now and wait for the answer.

- If the user agrees, derive a descriptive branch name from the change content, create it with `git checkout -b <branch-name>`, then run `git branch --show-current` again and use that result.
- If the user declines, stop.

**Clean working tree:** If `git status` shows no staged, modified, or untracked files, check whether there are unpushed commits or a missing PR before stopping:

1. Run `git branch --show-current`.
2. Run `git rev-parse --abbrev-ref --symbolic-full-name @{u}` to check whether an upstream is configured.
3. If the command succeeds, run `git log <upstream>..HEAD --oneline`.
4. Check for an existing PR using the method in Step 3.

Decision logic:
- **Current branch is `main`/`master`/default AND no upstream OR unpushed commits**: Explain that pushing would use the default branch directly. Ask whether to create a feature branch first. If user agrees, derive and create `git checkout -b <branch-name>` then continue from Step 5 (push). If user declines, stop.
- **No upstream configured**: Treat the branch as needing its first push. Skip Step 4 (commit) and continue from Step 5 (push).
- **Unpushed commits exist**: Skip Step 4 (commit) and continue from Step 5 (push).
- **All pushed + no open PR + current branch is default**: Report that there is no feature branch work to open as a PR and stop.
- **All pushed + no open PR + not default branch**: Skip Steps 4–5, continue from Step 6 (write description) and Step 7 (create PR).
- **All pushed + open PR exists**: Report that and stop — there is nothing to do.

### Step 2: Determine conventions

Priority order for commit messages *and* PR titles:

1. **Repo conventions already in context** — If project instructions (AGENTS.md, CLAUDE.md, or similar) are loaded and specify conventions, follow those. Do not re-read these files; they are loaded at session start.
2. **Recent commit history** — Match the pattern visible in the last 10 commits if no explicit convention exists.
3. **Default: conventional commits** — `type(scope): description` as the fallback.

### Step 3: Check for existing PR

Run `git branch --show-current`. If empty, report still in detached HEAD state and stop.

Check for an existing open PR using the Reusable PR probe above. Interpret as:

- **Open PR exists (`state: OPEN`)** — Note the URL. Continue to Step 4 (commit) and Step 5 (push). Then skip to Step 7 (existing PR flow) instead of creating a new PR.
- **Non-OPEN state (CLOSED, MERGED)** — Treat as no PR. Continue Steps 4–8 normally.
- **No pull request exists (non-zero + "no pull requests found")** — No PR. Continue Steps 4–8 normally.
- **Real error (auth, network, config)** — Report the error and stop.

### Step 4: Branch, stage, and commit

1. Run `git branch --show-current`. If it returns `main`, `master`, or the resolved default branch from Step 1, create a descriptive feature branch first: `git checkout -b <branch-name>` (derive name from change content).
2. Scan changed files for naturally distinct concerns. If modified files clearly group into separate logical changes, create separate commits for each group. Group at the **file level only** (no `git add -p`), split only when obvious, aim for **two or three logical commits at most**.
3. Stage relevant files by name. Avoid `git add -A` or `git add .` to prevent accidentally including sensitive files.
4. Commit following the conventions from Step 2. Use a heredoc for the message.

### Step 5: Push

```bash
git push -u origin HEAD
```

### Step 6: Write the PR description

Before writing, determine the **base branch** and gather the **full branch scope**. The working-tree diff from Step 1 only shows uncommitted changes at invocation time — the PR description must cover **all commits** that will appear in the PR.

#### Detect the base branch and remote

Resolve the base branch and the remote that hosts it. In fork-based PRs the base repository may correspond to a remote other than `origin` (commonly `upstream`).

Use this fallback chain — stop at the first that succeeds:

1. **PR metadata** (if an existing PR was found in Step 3):
   ```bash
   gh pr view --json baseRefName,url
   ```
   Extract `baseRefName` as the base branch name. The PR URL contains the base repository. Determine which local remote corresponds to that repository:
   ```bash
   git remote -v
   ```
   Match the `owner/repo` from the PR URL against the fetch URLs. Use the matching remote as the base remote. If no remote matches, fall back to `origin`.

2. **`origin/HEAD` symbolic ref:**
   ```bash
   git symbolic-ref --quiet --short refs/remotes/origin/HEAD
   ```
   Strip the `origin/` prefix. Use `origin` as the base remote.

3. **GitHub default branch metadata:**
   ```bash
   gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
   ```
   Use `origin` as the base remote.

4. **Common branch names** — check `main`, `master`, `develop`, `trunk` in order. Use the first that exists on the remote:
   ```bash
   git rev-parse --verify origin/<candidate>
   ```
   Use `origin` as the base remote.

If none resolve, ask the user to specify the target branch and wait for the answer.

#### Gather the branch scope

Once the base branch and remote are known:

1. Verify the remote-tracking ref exists locally and fetch if needed:
   ```bash
   git rev-parse --verify <base-remote>/<base-branch>
   # If this fails:
   git fetch --no-tags <base-remote> <base-branch>
   ```
2. Find the merge base:
   ```bash
   git merge-base <base-remote>/<base-branch> HEAD
   ```
3. List all commits unique to this branch:
   ```bash
   git log --oneline <merge-base>..HEAD
   ```
4. Get the full diff a reviewer will see:
   ```bash
   git diff <merge-base>...HEAD
   ```

Use the full branch diff and commit list as the basis for the PR description — not the working-tree diff from Step 1.

#### Sizing the change

Assess the PR along two axes based on the full branch diff:

- **Size**: How many files changed? How large is the diff?
- **Complexity**: Is this a straightforward change (rename, dependency bump, typo fix) or does it involve design decisions, trade-offs, new patterns, or cross-cutting concerns?

| Change profile | Description approach |
|---|---|
| Small + simple (typo, config, dep bump) | 1–2 sentences, no headers. Total body under ~300 characters. |
| Small + non-trivial (targeted bugfix, behavioral change) | Short "Problem / Fix" narrative, ~3–5 sentences. Enough for a reviewer to understand *why* without reading the diff. No headers needed unless there are two distinct concerns. |
| Medium feature or refactor | Summary paragraph, then a section explaining what changed and why. Call out design decisions. |
| Large or architecturally significant | Full narrative: problem context, approach chosen (and why), key decisions, migration notes or rollback considerations if relevant. |
| Performance improvement | Include before/after measurements if available. A markdown table is effective here. |

**Brevity matters for small changes.** A 3-line bugfix with a 20-line PR description signals the author didn't calibrate. When in doubt, shorter is better — reviewers can read the diff.

#### Writing principles

- **Lead with value**: The first sentence should tell the reviewer *why this PR exists*, not *what files changed*. "Fixes timeout errors during batch exports" beats "Updated export_handler.py and config.yaml".
- **No orphaned opening paragraphs**: If the description uses `##` section headings anywhere, the opening summary must also be under a heading (e.g., `## Summary`). An untitled paragraph followed by titled sections looks like a missing heading. For short descriptions with no sections, a bare paragraph is fine.
- **Describe the net result, not the journey**: Do not include work-product details like bugs found and fixed during development, intermediate failures, debugging steps, iteration history, or refactoring done along the way. Exception: include process details only when they are critical for a reviewer to understand a design choice (e.g., "tried approach X first but it caused Y, so went with Z instead").
- **When commits conflict, trust the final diff**: If commit messages describe intermediate steps that were later revised or reverted, describe the end state shown by the full branch diff. Do not narrate contradictory commit history as if all of it shipped.
- **Explain the non-obvious**: If the diff is self-explanatory, don't narrate it. Spend description space on things the diff *doesn't* show: why this approach, what was considered and rejected, what the reviewer should pay attention to.
- **Use structure when it earns its keep**: Headers, bullet lists, and tables are tools — use them when they aid comprehension, not as mandatory template sections.
- **No empty sections**: If a section (like "Breaking Changes" or "Migration Guide") doesn't apply, omit it entirely. Do not include it with "N/A" or "None".
- **Test plan — only when it adds value**: Include a test plan section only when the testing approach is non-obvious (edge cases, verification steps for behavior hard to see in the diff, scenarios requiring specific setup). Omit it for straightforward changes.
- **Markdown tables for data**: When there are before/after comparisons, performance numbers, or option trade-offs, use a table:
  ```markdown
  | Metric | Before | After |
  |--------|--------|-------|
  | p95 latency | 340ms | 120ms |
  | Memory (peak) | 2.1GB | 1.4GB |
  ```

#### Visual communication

Include a visual aid when the PR changes something structurally complex enough that a reviewer would struggle to reconstruct the mental model from prose alone. The bar is higher than in brainstorms or plans — visuals must earn their space quickly.

**When to include:**

| PR changes... | Visual aid | Placement |
|---|---|---|
| Architecture touching 3+ interacting components or services | Mermaid component or interaction diagram | Within the approach or changes section |
| A multi-step workflow, pipeline, or data flow with non-obvious sequencing | Mermaid flow diagram | After the summary or within the changes section |
| 3+ behavioral modes, states, or variants being introduced or changed | Markdown comparison table | Within the relevant section |
| Before/after performance data, behavioral differences, or option trade-offs | Markdown table | Inline with the data |
| Data model changes with 3+ related entities or relationship changes | Mermaid ERD or relationship diagram | Within the changes section |

**When to skip:**
- The change is trivial (sizing table routes to "1–2 sentences")
- Prose already communicates the change clearly
- The diagram would just restate the diff in visual form without adding comprehension value
- The change is mechanical (renames, dependency bumps, config changes, formatting)
- The PR description is already short enough that a diagram would be heavier than the prose around it

**Format selection:**
- **Mermaid** (default) for flow diagrams, interaction diagrams, and dependency graphs — 5–10 nodes typical, up to 15 only for genuinely complex changes. Use `TB` (top-to-bottom) direction so diagrams stay narrow. Source should be readable as fallback in diff views, email notifications, and Slack previews.
- **ASCII/box-drawing diagrams** for annotated flows that need rich in-box content — decision logic branches, file path layouts, step-by-step transformations with annotations. Follow 80-column max for code blocks, use vertical stacking.
- **Markdown tables** for mode/variant comparisons, before/after data, and decision matrices.
- Place inline at the point of relevance within the description, not in a separate "Diagrams" section.
- Prose is authoritative: when a visual aid and surrounding description prose disagree, the prose governs.
- After generating a visual aid, verify it accurately represents the change — correct components, no missing interactions, no merged steps.

#### Numbering and references

**Never prefix list items with `#`** in PR descriptions. GitHub interprets `#1`, `#2`, etc. as issue/PR references.

Instead of:
```markdown
#1. Updated the parser
#2. Fixed the validation
```

Write:
```markdown
1. Updated the parser
2. Fixed the validation
```

When referencing actual GitHub issues or PRs, use the full format: `org/repo#123` or the full URL. Never use bare `#123` unless you have verified it refers to the correct issue in the current repository.

### Step 7: Create or update the PR

#### New PR (no existing PR from Step 3)

```bash
gh pr create --title "the pr title" --body "$(cat <<'EOF'
PR description here
EOF
)"
```

Keep the PR title under 72 characters. The title follows the same convention as commit messages (Step 2).

#### Existing PR (found in Step 3)

The new commits are already on the PR from the push in Step 5. Report the PR URL, then ask the user whether they want the PR description updated to reflect the new changes. Wait for the answer before proceeding.

- If **yes** — write a new description following the same principles in Step 6 (size the full PR, not just the new commits). Apply it:
  ```bash
  gh pr edit --body "$(cat <<'EOF'
  Updated description here
  EOF
  )"
  ```
- If **no** — done. The push was all that was needed.

### Step 8: Report

Output the PR URL so the user can navigate to it directly.

## Quality Gates

- Working tree, branch state, and upstream checked in Step 1; all edge cases handled before proceeding
- Conventions detected before committing or titling (repo docs > commit history > conventional commits)
- Default branch protected: feature branch created before staging if on `main`/`master`
- Files staged by name (not `git add -A`)
- Base branch detection uses full fallback chain; merge base computed correctly
- PR description depth matches change complexity (sizing table applied)
- No `#N.` list prefixes in PR description
- PR title ≤ 72 characters
- No empty sections in PR description
- Visual aids only included when the inclusion bar is met
- PR URL reported to user

## Outputs

- One or more commits on the feature branch
- Pushed branch with upstream set
- Open pull request (new or updated) with adaptive description
- PR URL reported

## Feeds Into

- `ce:review` / `ce:review-beta` — code review after PR is opened
- `resolve-pr-parallel` — address review feedback on the opened PR
- `feature-video` — add a video walkthrough to the PR description

## Harness Notes

- All blocking user questions (detached HEAD, default branch warning, PR description update confirmation, etc.) use the harness's native question tool. If none is available, present the options as text and wait for the user's reply before proceeding.
- Convention detection from AGENTS.md / CLAUDE.md assumes those files are already loaded into context at session start; do not re-read them.
- The Compound Engineering badge footer referenced in the original skill is harness-specific and intentionally omitted here as a harness-agnostic reference. Add it back in harness-specific skill versions that know the plugin version and model metadata.
