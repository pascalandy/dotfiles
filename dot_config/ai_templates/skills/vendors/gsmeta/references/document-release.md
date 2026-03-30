# Document Release

> Post-ship documentation update: reads all project docs, cross-references the diff, updates README/ARCHITECTURE/CONTRIBUTING/CLAUDE.md to match what shipped, polishes CHANGELOG voice, cleans up TODOS, and optionally bumps VERSION.

## When to Use

- After a PR is merged or code is shipped
- User says "update the docs", "sync documentation", "post-ship docs"
- Proactively suggest after `/ship` creates a PR or code lands
- Auto-invoked by `/ship` in Step 8.5 (no user confirmation needed)

## Inputs

- A feature branch (not the base branch) with committed changes
- All markdown files discoverable in the repo root and up to one level deep
- The diff between feature branch and base branch

## Stop/Auto Rules

**Only stop for:**
- Risky/questionable doc changes (narrative, philosophy, security model changes, removals, large rewrites >~10 lines in one section)
- VERSION bump decision (if not already bumped)
- New TODOS items to capture
- Cross-doc narrative contradictions

**Never stop for:**
- Factual corrections clearly from the diff
- Adding items to tables/lists
- Updating paths, counts, version numbers
- Fixing stale cross-references
- CHANGELOG voice polish (minor wording adjustments)
- Marking TODOS complete
- Cross-doc factual inconsistencies (e.g., version number mismatch)

**NEVER do:**
- Overwrite, replace, or regenerate CHANGELOG entries -- polish wording only, preserve all content
- Bump VERSION without asking -- always ask. Even if already bumped, check whether it covers the full scope.
- Use Write to overwrite CHANGELOG.md -- always use Edit with exact string matches

## Methodology

### Step 1: Pre-flight and diff analysis

1. If on the base branch, abort: "Run from a feature branch."
2. Run `git diff <base>...HEAD --stat`, `git log <base>..HEAD --oneline`, `git diff <base>...HEAD --name-only`.
3. Discover all documentation files: `find . -maxdepth 2 -name "*.md" -not -path "./.git/*" -not -path "./node_modules/*" -not -path "./.gstack/*" -not -path "./.context/*"`.
4. Classify changes into categories: new features, changed behavior, removed functionality, infrastructure.
5. Summarize: "Analyzing N files changed across M commits. Found K documentation files to review."

### Step 2: Per-file documentation audit

Read each documentation file and cross-reference against the diff. Classify needed updates as auto-update or ask user.

**README.md:**
- Does it describe all features and capabilities visible in the diff?
- Are install/setup instructions consistent with the changes?
- Are examples, demos, and usage descriptions still valid?
- Are troubleshooting steps still accurate?

**ARCHITECTURE.md:**
- Do ASCII diagrams and component descriptions match the current code?
- Are design decisions and "why" explanations still accurate?
- Be conservative: only update things clearly contradicted by the diff. Architecture docs change infrequently.

**CONTRIBUTING.md -- new contributor smoke test:**
- Walk through the setup instructions as a brand new contributor would. Are listed commands accurate? Would each step succeed?
- Do test tier descriptions match the current test infrastructure?
- Are workflow descriptions current?
- Flag anything that would fail or confuse a first-time contributor.

**CLAUDE.md / project instructions:**
- Does the project structure section match the actual file tree?
- Are listed commands and scripts accurate?
- Do build/test instructions match what's in the package manifest?

**Other .md files:** read, determine purpose and audience, cross-reference against diff.

**Classification rules:**
- **Auto-update:** adding an item to a table, updating a file path, fixing a count, updating a version number, fixing a cross-reference. Clear factual correction warranted by the diff.
- **Ask user:** narrative changes, section removal, security model changes, large rewrites (>10 lines in one section), ambiguous relevance, adding entirely new sections.

**Never auto-update:** README introduction or project positioning, ARCHITECTURE philosophy or design rationale, security model descriptions. Never remove entire sections from any document.

### Step 3: Apply auto-updates

Make all clear, factual updates directly using file editing. For each file modified, output a one-line summary of what specifically changed: not "Updated README.md" but "README.md: added /new-skill to skills table, updated skill count from 9 to 10."

### Step 4: Ask about risky/questionable changes

For each risky or questionable update, ask with:
- Context (project, branch, which file, what's under review)
- The specific documentation decision
- RECOMMENDATION with rationale
- Options including C) Skip

Apply approved changes immediately after each answer.

### Step 5: CHANGELOG voice polish

**CRITICAL: never clobber CHANGELOG entries.** A real incident occurred where an agent replaced existing CHANGELOG entries. This skill must NEVER do that.

Rules:
1. Read the entire CHANGELOG.md first. Understand what is already there.
2. Only modify wording within existing entries. Never delete, reorder, or replace entries.
3. Never regenerate a CHANGELOG entry from scratch -- the entry was written from actual diff and commit history and is the source of truth.
4. If an entry looks wrong or incomplete, use ask the user -- do NOT silently fix it.
5. Always use Edit with exact string matches, never Write to overwrite CHANGELOG.md.

If CHANGELOG was not modified on this branch: skip this step.

If CHANGELOG was modified, review each entry for voice:
- **Sell test:** would a user reading this bullet want to try the feature? If not, rewrite wording (not content).
- Lead with what the user can now **do**: "You can now..." not "Refactored the..."
- Flag and rewrite entries that read like commit messages.
- Internal/contributor changes go under `### For contributors` subsection.
- Auto-fix minor voice adjustments. Ask if a rewrite would alter meaning.

### Step 6: Cross-doc consistency and discoverability check

After auditing each file individually:

1. Does the README's feature list match what CLAUDE.md describes?
2. Does ARCHITECTURE's component list match CONTRIBUTING's project structure description?
3. Does CHANGELOG's latest version match the VERSION file?
4. **Discoverability:** is every documentation file reachable from README.md or CLAUDE.md? If ARCHITECTURE.md exists but neither entry-point file links to it, flag it. Every doc should be discoverable from one of the two entry-point files.
5. Auto-fix clear factual inconsistencies (e.g., version number mismatch). Ask for narrative contradictions.

### Step 7: TODOS.md cleanup

This is a second pass that complements `/ship`'s TODOS step. Read `review/TODOS-format.md` (if available) for the canonical TODO item format.

If TODOS.md doesn't exist: skip.

1. **Completed items not yet marked:** cross-reference diff against open TODO items. If clearly completed by changes in this branch, move to the Completed section with `**Completed:** vX.Y.Z.W (YYYY-MM-DD)`. Be conservative -- require clear evidence.
2. **Items needing description updates:** if a TODO references files or components that were significantly changed, ask whether to update, complete, or leave as-is.
3. **New deferred work:** check diff for `TODO`, `FIXME`, `HACK`, `XXX` comments. For each that represents meaningful deferred work (not a trivial inline note), ask whether to capture in TODOS.md.

### Step 8: VERSION bump question

**CRITICAL: never bump VERSION without asking.**

If VERSION doesn't exist: skip silently.

Check if VERSION was modified on this branch: `git diff <base>...HEAD -- VERSION`.

**If NOT bumped:** ask with RECOMMENDATION to skip (docs-only changes rarely warrant a version bump):
- A) Bump PATCH (X.Y.Z+1) -- if doc changes ship alongside code changes
- B) Bump MINOR (X.Y+1.0) -- if this is a significant standalone release
- C) Skip -- no version bump needed

**If already bumped:** do NOT skip silently. Check whether the bump covers the full scope:
1. Read the CHANGELOG entry for the current VERSION. What features does it describe?
2. Read the full diff. Are there significant changes (new features, new skills, major refactors) NOT mentioned in the current CHANGELOG entry?
3. If CHANGELOG entry covers everything: "VERSION: Already bumped to vX.Y.Z, covers all changes." Skip.
4. If uncovered significant changes exist: ask whether to bump to next patch (give new changes their own version) or keep current version (absorb new changes into the existing entry). A VERSION bump set for "feature A" should not silently absorb "feature B" if B is substantial.

### Step 9: Commit and output

Run `git status`. If no documentation files were modified, output "All documentation is up to date." and exit without committing.

Stage modified documentation files by name (never `git add -A`). Commit:
```
docs: update project documentation for vX.Y.Z.W

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Push to the current branch.

**PR/MR body update (idempotent, race-safe):**
1. Read existing PR body into a PID-unique tempfile:
   - GitHub: `gh pr view --json body -q .body > /tmp/gstack-pr-body-$$.md`
   - GitLab: extract via `glab mr view -F json` + python3 json parse
2. If body already contains `## Documentation` section: replace it. If not: append.
3. The Documentation section includes a **doc diff preview**: for each file modified, describe what specifically changed.
4. Write the updated body back:
   - GitHub: `gh pr edit --body-file /tmp/gstack-pr-body-$$.md`
   - GitLab: `glab mr update -d "$(cat /tmp/gstack-pr-body-$$.md)"`
5. Clean up: `rm -f /tmp/gstack-pr-body-$$.md`
6. If no PR/MR exists: skip with "No PR/MR found -- skipping body update."
7. If update fails: warn and continue. Documentation changes are in the commit.

**Structured doc health summary (final output):**

```
Documentation health:
  README.md       [Updated -- added /new-skill to skills table]
  ARCHITECTURE.md [Current -- no changes needed]
  CONTRIBUTING.md [Updated -- fixed setup step 3 command]
  CHANGELOG.md    [Voice polished -- 2 entries reworded]
  TODOS.md        [Updated -- 1 item marked complete]
  VERSION         [Already bumped to v1.2.0]
```

Status values: Updated, Current, Voice polished, Not bumped, Already bumped, Skipped.

## Quality Gates

- **Never merge docs with stale cross-references** (auto-fixed when factual)
- **CHANGELOG integrity:** every entry preserved, wording may be polished but content never changed
- **VERSION:** never bumped without explicit user confirmation
- **Discoverability:** every doc file reachable from README or CLAUDE.md
- **New contributor smoke test:** setup instructions in CONTRIBUTING.md must be accurate
- **Read before editing:** always read the full content of a file before modifying it

## Outputs

- Updated markdown files committed to feature branch
- PR/MR body updated with `## Documentation` section (doc diff preview per file)
- Documentation health summary printed to output

## Feeds Into

- >ship (run document-release before ship creates the PR, or after on the same branch; auto-invoked by ship Step 8.5)
- >land-and-deploy (the readiness gate checks for document-release evidence: CHANGELOG and VERSION updated)
- >retro (documentation health patterns surface in the retro)
