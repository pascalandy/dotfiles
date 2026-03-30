# Ship

> Fully automated pre-PR workflow: merge base branch, run tests, audit coverage, review diff, bump VERSION, update CHANGELOG, commit, push, create PR.

## When to Use

- User says "ship", "deploy", "push to main", "create a PR", "merge and push"
- Code is ready and needs to go out
- After implementing a feature or fix on a feature branch
- Proactively suggest when the user indicates code is ready

## Inputs

- An open feature branch (not the base branch)
- Uncommitted changes are fine -- they get included automatically
- Optional: a plan file in `.gstack/plans/` or `~/.gstack/projects/<slug>/` for plan completion audit
- Optional: existing test framework (bootstrapped if missing)

## Methodology

### Step 0: Detect platform and base branch

Detect the git hosting platform from the remote URL (github.com = GitHub, gitlab = GitLab). Determine the base branch: check `gh pr view --json baseRefName`, then `gh repo view --json defaultBranchRef`, then `git symbolic-ref refs/remotes/origin/HEAD`, then try `origin/main`, then `origin/master`. Use this branch name in all subsequent git commands.

### Step 1: Pre-flight

1. If on the base branch, abort: "Ship from a feature branch."
2. Run `git status`. Uncommitted changes are always included -- never ask about them.
3. Run `git diff <base>...HEAD --stat` and `git log <base>..HEAD --oneline` to understand scope.
4. Display the **Review Readiness Dashboard**.

**Auto-stop conditions:**
- On base branch
- Merge conflicts that can't be auto-resolved
- In-branch test failures
- AI-assessed coverage below minimum threshold (with user override option)
- Plan items NOT DONE with no user override
- Verification failures from plan steps

**Never stop for:** uncommitted changes, version bump choice (auto-pick MICRO/PATCH), CHANGELOG content, commit message, auto-fixable review findings.

#### Review Readiness Dashboard

Read the stored review log. Find the most recent entry for each skill: plan-eng-review, plan-ceo-review, plan-design-review, design-review-lite, adversarial-review, codex-review, codex-plan-review.

- Ignore entries older than 7 days.
- Eng Review: show whichever is more recent between `review` (diff-scoped) and `plan-eng-review` (plan-stage). Append "(DIFF)" or "(PLAN)" to status.
- Adversarial: show more recent of `adversarial-review` or `codex-review`.
- Design Review: show more recent of `plan-design-review` (full) or `design-review-lite`. Append "(FULL)" or "(LITE)".
- Outside Voice: show most recent `codex-plan-review`.
- If an entry has a `"via"` field, append it in parentheses: e.g., "CLEAR (PLAN via /autoplan)".

Display format:
```
+====================================================================+
|                    REVIEW READINESS DASHBOARD                       |
+====================================================================+
| Review          | Runs | Last Run            | Status    | Required |
|-----------------|------|---------------------|-----------|----------|
| Eng Review      |  1   | 2026-03-16 15:00    | CLEAR     | YES      |
| CEO Review      |  0   | --                  | --        | no       |
| Design Review   |  0   | --                  | --        | no       |
| Adversarial     |  0   | --                  | --        | no       |
| Outside Voice   |  0   | --                  | --        | no       |
+--------------------------------------------------------------------+
| VERDICT: CLEARED -- Eng Review passed                               |
+====================================================================+
```

**Review tiers:**
- **Eng Review (required by default):** Only review that gates shipping. Can be disabled globally with `gstack-config set skip_eng_review true`.
- **CEO Review (optional):** Recommend for product/business changes, new user-facing features. Skip for bug fixes, refactors, infra.
- **Design Review (optional):** Recommend for UI/UX changes. Skip for backend-only or infra.
- **Adversarial (automatic):** Auto-scales by diff size. <50 lines: skip. 50-199: Codex adversarial (or Claude subagent). 200+: all 4 passes.
- **Outside Voice (optional):** Never gates shipping.

**Verdict logic:**
- **CLEARED:** Eng Review has >= 1 entry within 7 days with status "clean", OR `skip_eng_review` is `true` (shows "SKIPPED (global)")
- **NOT CLEARED:** Eng Review missing, stale (>7 days), or has open issues

**Staleness detection:** For each review entry with a `commit` field, compare against HEAD with `git rev-list --count STORED_COMMIT..HEAD`. Display: "Note: {skill} review from {date} may be stale -- {N} commits since review." For entries without a `commit` field: "has no commit tracking -- consider re-running."

If Eng Review is NOT CLEARED: print "No prior eng review found -- ship will run its own pre-landing review in Step 3.5." If diff is >200 lines, add a note to consider running `/plan-eng-review` first. If CEO Review is missing, mention as informational only -- never block. If frontend files changed and no design review exists, mention informational only -- never block.

### Step 1.5: Distribution pipeline check

If the diff adds a new binary/CLI entry point (`cmd/`, `bin/`, `main.go`, `Cargo.toml`, `setup.py`, `package.json` with a new `bin` entry) and no CI release workflow exists (check `.github/workflows/` for `release|publish|dist`), ask: add one now, defer to TODOS.md, or mark as not needed. If no new artifact detected, skip silently.

### Step 2: Merge base branch (before tests)

```
git fetch origin <base> && git merge origin/<base> --no-edit
```

Auto-resolve simple conflicts (VERSION, schema.rb, CHANGELOG ordering). Stop for complex ones.

### Step 2.5: Test framework bootstrap

Detect existing test framework from config files (`jest.config.*`, `vitest.config.*`, `.rspec`, `pytest.ini`, etc.) and test directories. If found, read 2-3 test files to learn conventions. Skip the rest of bootstrap. If `.gstack/no-test-bootstrap` exists, skip silently.

If no runtime detected, ask. If runtime detected but no framework and not declined:

1. Search for current best practices for the detected runtime.
2. Offer framework choice with rationale:

| Runtime | Primary | Alternative |
|---------|---------|-------------|
| Ruby/Rails | minitest + fixtures + capybara | rspec + factory_bot |
| Node.js | vitest + @testing-library | jest + @testing-library |
| Next.js | vitest + @testing-library/react + playwright | jest + cypress |
| Python | pytest + pytest-cov | unittest |
| Go | stdlib testing + testify | stdlib only |
| Rust | cargo test + mockall | -- |
| PHP | phpunit + mockery | pest |
| Elixir | ExUnit + ex_machina | -- |

If user declines, write `.gstack/no-test-bootstrap`. After installing: create config, generate 3-5 real tests for recently changed files (prioritize: error handlers > business logic > API endpoints > pure functions), run each test and keep passing ones, create TESTING.md, append `## Testing` to CLAUDE.md, create `.github/workflows/test.yml`. If installation fails, debug once, then revert and warn.

### Step 3: Run tests

Run all test suites (parallel if possible). Check output.

**Test Failure Ownership Triage:**

1. Classify each failure: **in-branch** if the failing test or the code it tests was changed on this branch. **Pre-existing** if neither was touched. When ambiguous, default to in-branch -- safer to stop than to let a broken test ship.
2. In-branch failures: **STOP**. The developer must fix their own tests before shipping.
3. Pre-existing failures:
   - Solo repo: offer to fix now (fix separately as `fix: pre-existing test failure in <file>`), add P0 TODO, or skip.
   - Collaborative repo: offer to fix, blame + assign GitHub/GitLab issue to the author who last touched the production file (check both test file and source file, prefer production code author), add P0 TODO, or skip.
4. If no in-branch failures remain, continue.

### Step 3.25: Eval suites (conditional)

If the diff touches prompt-related files (`*_prompt_builder.rb`, `*_generation_service.rb`, `config/system_prompts/*.txt`, `test/evals/**/*`, etc.), identify affected eval suites by reading `PROMPT_SOURCE_FILES` declarations in each eval runner, then run them at `EVAL_JUDGE_TIER=full` (Sonnet structural + Opus persona judges). If any eval fails, stop. Save results for PR body.

Tier reference:
| Tier | Speed (cached) | Cost |
|------|----------------|------|
| `fast` (Haiku) | ~5s | ~$0.07/run |
| `standard` (Sonnet) | ~17s | ~$0.37/run |
| `full` (Opus persona) | ~72s | ~$1.27/run |

### Step 3.4: Test coverage audit

100% coverage is the goal -- every untested path is where bugs hide and vibe coding becomes yolo coding.

**Before-count:** count test files before any generation.

**1. Trace every changed codepath.** Read each changed file in full (not just diff hunks). For each file, trace data flow from every entry point through every branch: where does input come from, what transforms it, where does it go, what can go wrong at each step (null/undefined, invalid input, network failure, empty collection).

**2. Map user flows and interactions.** For each changed feature: complete user journeys, interaction edge cases (double-click/rapid resubmit, navigate away mid-operation, submit with stale data, slow connection, concurrent actions), error states the user sees, empty/zero/boundary states.

**3. Check each branch against existing tests.** Quality scoring rubric:
- ★★★ Tests behavior with edge cases AND error paths
- ★★ Tests correct behavior, happy path only
- ★ Smoke test / trivial assertion

**E2E vs unit decision matrix:**
- **Use E2E for:** common user flows spanning 3+ components, auth/payment/data-destruction, integration points where mocking hides real failures.
- **Use eval for:** critical LLM calls, prompt template changes.
- **Use unit tests for:** pure functions, internal helpers, single-function edge cases.

Mark paths in the diagram as [→E2E] or [→EVAL] accordingly.

**4. Output ASCII coverage diagram:**

```
CODE PATH COVERAGE
===========================
[+] src/services/billing.ts
    ├── processPayment()
    │   ├── [★★★ TESTED] Happy path + card declined -- billing.test.ts:42
    │   ├── [GAP]         Network timeout -- NO TEST
    │   └── [GAP]         Invalid currency -- NO TEST
    └── refundPayment()
        ├── [★★  TESTED] Full refund -- billing.test.ts:89
        └── [★   TESTED] Partial refund (non-throw only) -- billing.test.ts:101

USER FLOW COVERAGE
===========================
[+] Payment checkout flow
    ├── [★★★ TESTED] Complete purchase -- checkout.e2e.ts:15
    ├── [GAP] [→E2E] Double-click submit
    └── [GAP]         Navigate away during payment

─────────────────────────────────
COVERAGE: 5/13 paths tested (38%)
  Code paths: 3/5 (60%)
  User flows: 2/8 (25%)
QUALITY:  ★★★: 2  ★★: 2  ★: 1
GAPS: 8 paths need tests (2 need E2E, 1 needs eval)
─────────────────────────────────
```

**Fast path:** all paths covered → "Step 3.4: All new code paths have test coverage." Continue.

**5. REGRESSION RULE (mandatory, no user confirmation):** When the coverage audit finds a regression -- code that previously worked but the diff modifies, and the existing tests don't cover the changed path -- write a regression test immediately. No asking. No skipping. Commit as `test: regression test for {what broke}`.

A regression is: the diff modifies existing behavior (not new code), the existing test suite doesn't cover the changed path, or the change introduces a new failure mode for existing callers. When uncertain, err on writing the test.

**6. Generate tests for uncovered paths.** Prioritize error handlers and edge cases. Read existing tests to match conventions exactly. Mock all external dependencies. Generate E2E tests for [→E2E] paths, eval tests for [→EVAL] paths. Run each generated test. Commit passing ones as `test: coverage for {feature}`. Caps: 30 code paths max, 20 tests generated max, 2-minute per-test exploration cap.

**7. After-count:** count test files after generation. For PR body: `Tests: {before} → {after} (+{delta} new)`.

**8. Coverage gate:** check CLAUDE.md for `## Test Coverage` section with `Minimum:` and `Target:` fields. Defaults: minimum = 60%, target = 80%.

- >= target: PASS. Continue.
- >= minimum, < target: ask -- generate more (max 2 passes), ship with risk acknowledgment, or mark intentionally uncovered.
- < minimum: ask -- generate more (max 2 passes) or override with explicit acknowledgment. Include "Coverage gate: OVERRIDDEN at X%" in PR body.
- If coverage percentage can't be determined: skip gate with note. Never default to 0%.
- Test-only diffs: skip gate entirely.

**9. Write test plan artifact** to `~/.gstack/projects/{slug}/{user}-{branch}-ship-test-plan-{datetime}.md` for `/qa` to consume. Include: affected pages/routes, key interactions to verify, edge cases, critical paths.

### Step 3.45: Plan completion audit

**Plan file discovery:** first check conversation context for an active plan file (most reliable). Fallback: search `~/.gstack/projects/<slug>/`, `~/.claude/plans/`, `~/.codex/plans/`, `.gstack/plans/` for a file matching the branch or repo name, or most recently modified within 24 hours. If found via search, read first 20 lines to validate relevance. If no plan file, skip with "No plan file detected -- skipping."

**Actionable item extraction (cap: 50 items):** extract checkboxes, numbered steps under implementation headings, imperative statements, file-level specifications, test requirements, data model changes. Ignore: context/background sections, open questions (TBD, ?), deferred items (Future:, Out of scope:, P2-P4:), review report sections.

Assign each item a category: CODE | TEST | MIGRATION | CONFIG | DOCS.

**Cross-reference against diff.** Classify each item:
- **DONE** -- clear evidence in diff (cite specific files). Require clear evidence, not just a file being touched.
- **PARTIAL** -- some work exists but incomplete.
- **NOT DONE** -- no evidence in diff.
- **CHANGED** -- different approach, same goal achieved. Be generous with CHANGED.

**Output format:**
```
PLAN COMPLETION AUDIT
═══════════════════════════════
Plan: {plan file path}

## Implementation Items
  [DONE]      Create UserService -- src/services/user_service.rb (+142 lines)
  [PARTIAL]   Add validation -- model validates but missing controller checks
  [NOT DONE]  Add caching layer -- no cache-related changes in diff
  [CHANGED]   "Redis queue" → implemented with Sidekiq instead

─────────────────────────────────
COMPLETION: 4/7 DONE, 1 PARTIAL, 1 NOT DONE, 1 CHANGED
─────────────────────────────────
```

**Gate logic:**
- All DONE or CHANGED: PASS. Continue.
- Only PARTIAL (no NOT DONE): continue with note in PR body.
- Any NOT DONE: ask -- stop and implement, ship with P1 TODOs for each deferred item (created in Step 5.5 as "Deferred from plan: {path}"), or mark as intentionally dropped.

Include a `## Plan Completion` section in the PR body.

### Step 3.47: Plan verification

Using the plan file from 3.45, look for a verification section (`## Verification`, `## Test plan`, `## How to test`, `## Manual testing`, etc.).

Check if a dev server is reachable: try localhost:3000, :8080, :5173, :4000.

If no plan file, no verification section, or no dev server: skip ("No dev server detected -- skipping plan verification.").

If both exist: read the `/qa-only` skill from disk and follow its workflow with modifications -- skip the preamble, use the plan's verification section as test input, use detected dev server URL, skip the fix loop, cap at plan verification items only (no general site QA).

Gate: all PASS → continue. Any FAIL → ask to fix or ship with known issues. Include `## Verification Results` in PR body (N PASS, M FAIL, K SKIPPED, or reason for skipping).

### Step 3.5: Prior learnings check

Search for relevant learnings from previous sessions. If `cross_project_learnings` config is unset (first time), ask whether to enable cross-project learning search (recommended for solo devs) or keep project-scoped only. When learnings match a review finding, display: "Prior learning applied: [key] (confidence N/10, from [date])".

### Step 3.5: Pre-landing review

Read the review checklist from disk (`~/.claude/skills/review/checklist.md`). If unreadable, STOP. Run `git diff origin/<base>` for the full diff.

**Two passes:**
- **Pass 1 (CRITICAL):** SQL & Data Safety, LLM Output Trust Boundary
- **Pass 2 (INFORMATIONAL):** All remaining categories

**Confidence calibration:** every finding includes a confidence score (1-10):

| Score | Meaning | Display rule |
|-------|---------|-------------|
| 9-10 | Verified by reading specific code. Concrete bug demonstrated. | Show normally |
| 7-8 | High confidence pattern match. Very likely correct. | Show normally |
| 5-6 | Moderate. Could be a false positive. | Show with caveat: "Medium confidence, verify" |
| 3-4 | Low confidence. Suspicious but may be fine. | Suppress from main report, appendix only |
| 1-2 | Speculation. | Only report if severity would be P0 |

Finding format: `[SEVERITY] (confidence: N/10) file:line -- description`

**Design review (conditional):** If the diff touches frontend files (detected via `gstack-diff-scope`): read `DESIGN.md` if present (patterns in it are not flagged), read the design checklist, apply against changed files. AUTO-FIX mechanical CSS issues (outline:none, !important, font-size<16px). Flag design judgment issues as ASK. Log result to review log as `design-review-lite`. If Codex is available, run a Codex design voice check (7 litmus checks + 7 hard rejection patterns, 5-minute timeout, non-blocking).

**Fix-First flow:** auto-fix all AUTO-FIX items (output one line per fix: `[AUTO-FIXED] file:line Problem → what you did`). Batch remaining ASK items into one question. If 3 or fewer ASK items, individual questions are acceptable.

If ANY fixes were applied: commit fixed files (`fix: pre-landing review fixes`), then **STOP** and tell user to re-run `/ship`.

Log the result: `{"skill":"review","timestamp":"...","status":"clean|issues_found","issues_found":N,"critical":N,"informational":N,"commit":"...","via":"ship"}`

Save review output for Step 8 PR body.

### Step 3.75: Address Greptile review comments

Read `~/.claude/skills/review/greptile-triage.md`. If no PR exists, `gh` fails, or zero Greptile comments: skip silently.

If comments found, run **Escalation Detection** from greptile-triage.md to choose reply tier (friendly vs firm). Triage each comment:

- **VALID & ACTIONABLE:** ask to fix, acknowledge, or call false positive. If fixed: commit (`fix: address Greptile review -- <desc>`), reply with Fix template (inline diff + explanation), save to greptile-history as `type: fix`.
- **VALID BUT ALREADY FIXED:** reply with Already Fixed template (no question needed), save as `type: already-fixed`.
- **FALSE POSITIVE:** ask to reply explaining why, fix anyway, or ignore. If replying: use FP template (evidence + re-rank suggestion), save as `type: fp`.
- **SUPPRESSED:** skip silently.

If any fixes applied: re-run tests (Step 3) before continuing.

### Step 3.8: Adversarial review (auto-scaled)

Detect diff size: `git diff origin/<base> --stat | tail -1`. Respect `codex_reviews=disabled` config (skip entirely if set). Honor explicit user tier override (e.g., "run all passes").

**Auto-select tier:**
- **Small (< 50 lines):** skip. Print: "Small diff (N lines) -- adversarial review skipped."
- **Medium (50-199 lines):** Claude structured review already ran. Add one cross-model adversarial challenge. If Codex available: run `codex exec` with adversarial prompt (5-minute timeout, non-blocking). If Codex unavailable or errors: fall back to Claude adversarial subagent (Agent dispatch with adversarial prompt). Persist result as `{"skill":"adversarial-review","tier":"medium","source":"codex|claude","status":"...","commit":"..."}`.
- **Large (200+ lines):** run all three remaining passes: (1) Codex structured review (`codex review --base <base>`, 5-minute timeout, check for `[P1]` markers -- if found, ask to fix or continue), (2) Claude adversarial subagent (always runs), (3) Codex adversarial challenge (if available). Persist as `{"tier":"large","source":"both|claude","gate":"pass|fail|informational","..."}`.

**Cross-model synthesis** (medium and large tiers):
```
ADVERSARIAL REVIEW SYNTHESIS (auto: TIER, N lines):
════════════════════════════════════════════════════
  High confidence (found by multiple sources): [agreed-on findings]
  Unique to Claude structured: [...]
  Unique to Claude adversarial: [...]
  Unique to Codex: [...]
  Models used: Claude structured ✓  Claude adversarial ✓/✗  Codex ✓/✗
════════════════════════════════════════════════════
```

Prioritize high-confidence findings (agreed by multiple sources) for fixes.

### Step 4: VERSION bump (auto-decide)

Read the current `VERSION` file (4-digit format: MAJOR.MINOR.PATCH.MICRO). Auto-decide based on diff size:
- **MICRO** (4th digit): < 50 lines changed, trivial tweaks, typos, config
- **PATCH** (3rd digit): 50+ lines changed, bug fixes, small-medium features
- **MINOR** (2nd digit): ASK the user -- major features or significant architectural changes
- **MAJOR** (1st digit): ASK the user -- milestones or breaking changes

Bumping a digit resets all digits to its right to 0. Example: `0.19.1.0` + PATCH → `0.19.2.0`. Write the new version to the VERSION file.

### Step 5: CHANGELOG (auto-generate)

1. Read `CHANGELOG.md` header to learn format.
2. Enumerate every commit on the branch: `git log <base>..HEAD --oneline`. This is a checklist -- every commit must map to a bullet.
3. Read the full diff to understand what each commit changed.
4. Group commits by theme: new features, performance, bug fixes, dead code, infrastructure, refactoring.
5. Write the CHANGELOG entry covering ALL themes. Categorize under `### Added`, `### Changed`, `### Fixed`, `### Removed`. Internal/contributor changes go under `### For contributors`. Format: `## [X.Y.Z.W] - YYYY-MM-DD`. Insert after file header.
6. Cross-check: every commit must map to at least one bullet. If any is missing, add it.

Do NOT ask the user to describe changes. Infer from diff and commit history.

### Step 5.5: TODOS.md (auto-update)

Read `~/.claude/skills/review/TODOS-format.md` for canonical format.

If TODOS.md doesn't exist: ask to create one (skeleton: `# TODOS` heading + `## Completed` section) or skip.

If TODOS.md exists but is disorganized (missing priority fields P0-P4, no component groupings, no Completed section): ask to reorganize (preserve all content, restructure only) or leave as-is.

**Auto-detect completed items** (no user interaction): cross-reference diff against open items. Only mark items as completed when there is clear evidence. Move to `## Completed` section with `**Completed:** vX.Y.Z.W (YYYY-MM-DD)`.

**Scan for new deferred work:** check diff for `TODO`, `FIXME`, `HACK`, `XXX` comments. If meaningful deferred work found, ask whether to capture in TODOS.md.

If deferred plan items exist from Step 3.45, add them as P1 TODOs: "Deferred from plan: {path}".

Output summary: `TODOS.md: N items marked complete. M items remaining.`

### Step 6: Commit (bisectable chunks)

Group changes into logical commits. Each commit = one coherent change (not one file).

**Commit ordering:**
1. Infrastructure: migrations, config changes, route additions
2. Models & services: with their test files
3. Controllers & views: controllers, views, JS components, with tests
4. VERSION + CHANGELOG + TODOS.md: always the final commit

Rules: model + its test file → same commit. Service + test → same commit. Controller + views + test → same commit. Migrations are their own commit. If total diff is small (<50 lines, <4 files), a single commit is fine. Each commit must be independently valid -- no broken imports.

Final commit format:
```
chore: bump version and changelog (vX.Y.Z.W)

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

Stage files explicitly by name. Never `git add -A` or `git add .`.

### Step 6.5: Verification gate (Iron Law)

**IRON LAW: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**

Before pushing, re-verify if code changed during Steps 4-6 (review fixes, CHANGELOG edits don't count):

1. **Test verification:** if ANY code changed after Step 3's test run, re-run the test suite. Paste fresh output. Stale output from Step 3 is NOT acceptable.
2. **Build verification:** if the project has a build step, run it. Paste output.

**Rationalization prevention:**
- "Should work now" → RUN IT.
- "I'm confident" → Confidence is not evidence.
- "I already tested earlier" → Code changed since then. Test again.
- "It's a trivial change" → Trivial changes break production.

If tests fail here: STOP. Do not push. Fix the issue and return to Step 3.

### Step 7: Push

```
git push -u origin <branch-name>
```

### Step 8: Create PR/MR

Create PR (GitHub: `gh pr create`) or MR (GitLab: `glab mr create`) using the platform detected in Step 0.

PR body sections:
- `## Summary` -- summarize ALL changes, enumerate every commit, group into themes. Every substantive commit must appear.
- `## Test Coverage` -- coverage diagram or "All new code paths have test coverage." Include before/after test count.
- `## Pre-Landing Review` -- findings from Step 3.5 or "No issues found."
- `## Design Review` -- if design review ran: N findings, M auto-fixed, K skipped. If no frontend files changed: omit.
- `## Eval Results` -- if evals ran: suite names, pass/fail, cost. If skipped: reason.
- `## Greptile Review` -- if comments found: [FIXED]/[FALSE POSITIVE]/[ALREADY FIXED] per comment. If none: "No Greptile comments."
- `## Plan Completion` -- completion checklist from Step 3.45, or "No plan file detected."
- `## Verification Results` -- from Step 3.47, or reason for skipping.
- `## TODOS` -- completed items with version, or "No TODO items completed."
- `## Test plan` -- checklist of test suites run and results.

Output the PR/MR URL.

### Step 8.5: Auto-invoke document-release

After the PR is created, automatically sync project documentation. Read the `document-release` skill (adjacent skill directory) and execute its full workflow. This step is automatic -- do not ask for confirmation.

If any docs were updated, commit the changes and push to the same branch. If no docs needed updating: "Documentation is current -- no updates needed."

Goal: user runs `/ship` and documentation stays current without a separate command.

### Step 8.75: Persist ship metrics

Log coverage and plan completion data for `/retro` to track trends. Append to `~/.gstack/projects/$SLUG/$BRANCH-reviews.jsonl`:

```json
{"skill":"ship","timestamp":"...","coverage_pct":N,"plan_items_total":N,"plan_items_done":N,"verification_result":"pass|fail|skipped","version":"...","branch":"..."}
```

- `coverage_pct`: integer from Step 3.4 diagram, or -1 if undetermined
- `plan_items_total`: 0 if no plan file
- `plan_items_done`: count of DONE + CHANGED from Step 3.45
- `verification_result`: from Step 3.47

This step is automatic -- never skip, never ask for confirmation.

## Quality Gates

- **Hard stops:** on base branch, merge conflicts, in-branch test failures, plan NOT DONE items (with override), coverage below minimum (with override), verification failures.
- **Auto-proceed:** pre-existing test failures (triaged), coverage above minimum, auto-fixed review findings.
- **Evidence required:** every claim in the PR body is backed by concrete data (test counts, diff stats, coverage percentages).

## Important Rules

- Never skip tests. If tests fail, stop.
- Never skip the pre-landing review. If checklist.md is unreadable, stop.
- Never force push. Regular `git push` only.
- Never ask for trivial confirmations. DO stop for MINOR/MAJOR version bumps, ASK review findings, Codex [P1] findings.
- Always use the 4-digit version format from the VERSION file.
- Date format in CHANGELOG: `YYYY-MM-DD`.
- Split commits for bisectability -- each commit = one logical change.
- TODOS.md completion detection must be conservative. Only mark items completed when diff clearly shows the work is done.
- Use Greptile reply templates from greptile-triage.md. Every reply includes evidence.
- Never push without fresh verification evidence. If code changed after Step 3 tests, re-run before pushing.
- Step 3.4 generates coverage tests. They must pass before committing. Never commit failing tests.
- Goal: user says `/ship`, next thing they see is the review + PR URL + auto-synced docs.

## Outputs

- Merged base branch (tests run against merged state)
- Test framework (bootstrapped if needed)
- Generated test files committed (`test: coverage for {feature}`)
- VERSION file bumped
- CHANGELOG entry added
- TODOS.md updated
- All changes committed and pushed
- PR created with comprehensive body (PR URL printed at end)
- Documentation synced via auto-invoked document-release
- Ship metrics logged for retro

## Feeds Into

- >land-and-deploy (merges the PR, deploys, verifies production)
- >document-release (auto-invoked in Step 8.5; also run manually for post-land sync)
- >canary (extended production monitoring)
- >retro (ship metrics JSONL feeds plan completion and coverage trend sections)

## Harness Notes

**Browse dependency:** Plan verification step (3.47) requires headless browser for `/qa-only` against local dev server. If unavailable, step skips gracefully.

**Subagent delegation:** Adversarial review uses subagent delegation for Claude adversarial pass. In harnesses without subagent support, this pass is skipped.

**Codex dependency:** Adversarial review and design voice steps use Codex CLI if available. Both skip gracefully when Codex is not installed.

**File path assumptions:** Several steps read skill files from disk (`~/.claude/skills/review/checklist.md`, `review/TODOS-format.md`, `review/greptile-triage.md`). In non-GStack harnesses, substitute with inline checklist logic or skip.
