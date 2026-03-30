# QA

> Systematically test a web application, fix all bugs found, and produce before/after health scores with commit-per-fix evidence.

## When to Use

- User says "qa", "QA", "test this site", "find bugs", "test and fix", or "fix what's broken"
- User says a feature is ready for testing or asks "does this work?"
- After shipping a branch — the most common trigger is `/qa` with no URL on a feature branch
- When you need the full test-fix-verify loop (for report-only, use `>qa-only`)

**Three tiers:**
- **Quick:** Fix critical + high severity only. 30-second smoke test.
- **Standard:** + medium severity (default).
- **Exhaustive:** + low/cosmetic severity.

## Inputs

- Running web application (local dev server or URL). If on a feature branch with no URL, the skill auto-detects a local server.
- Optional: auth credentials or cookie file for authenticated testing
- Optional: `--regression <baseline.json>` for comparison against a prior run
- Optional: `--quick` or `--exhaustive` tier flags
- Clean git working tree (required — the skill asks to commit/stash if dirty)

## Methodology

### Step 0: Platform and Base Branch Detection

Detect the git hosting platform from the remote URL:
- URL contains "github.com" → **GitHub**
- URL contains "gitlab" → **GitLab**
- Otherwise check CLI: `gh auth status` succeeds → GitHub (covers GHE); `glab auth status` succeeds → GitLab (covers self-hosted); neither → **unknown** (git-native only)

Determine which branch this PR/MR targets, or the repo's default branch:

**If GitHub:**
1. `gh pr view --json baseRefName -q .baseRefName`
2. `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`

**If GitLab:**
1. `glab mr view -F json 2>/dev/null` and extract `target_branch`
2. `glab repo view -F json 2>/dev/null` and extract `default_branch`

**Git-native fallback:**
1. `git symbolic-ref refs/remotes/origin/HEAD | sed 's|refs/remotes/origin/||'`
2. Check `origin/main`, then `origin/master`
3. Fall back to `main`

Print the detected base branch. Use it everywhere the instructions say "base branch" or "main".

### Setup

Check for a clean working tree. If dirty, ask the user: commit, stash, or abort. Require a clean tree before starting so each bug fix gets its own atomic commit.

Check for a Test Plan Context before using git diff heuristics:
1. Check `~/.gstack/projects/{slug}/` for recent `*-test-plan-*.md` files for this repo
2. Check if a prior plan-eng-review or plan-ceo-review produced test plan output in this conversation
3. Use whichever source is richer. Fall back to git diff analysis only if neither is available.

Detect test framework from config files (`jest.config.*`, `vitest.config.*`, `playwright.config.*`, `.rspec`, `pytest.ini`) and test directories. If no test framework exists and the user hasn't opted out, bootstrap one (see Test Framework Bootstrap below).

**CDP mode detection:** Before starting, check if the browser is connected to the user's real browser session. If in CDP mode: skip cookie import prompts (real auth sessions are available), skip user-agent overrides, skip headless detection workarounds.

### Test Framework Bootstrap (when no framework exists)

1. Detect project runtime from root files (`package.json`, `Gemfile`, `requirements.txt`, `go.mod`, etc.)
2. Research current best practices for the detected runtime. If web search is unavailable, use the built-in knowledge table:

| Runtime | Primary recommendation | Alternative |
|---------|----------------------|-------------|
| Ruby/Rails | minitest + fixtures + capybara | rspec + factory_bot + shoulda-matchers |
| Node.js | vitest + @testing-library | jest + @testing-library |
| Next.js | vitest + @testing-library/react + playwright | jest + cypress |
| Python | pytest + pytest-cov | unittest |
| Go | stdlib testing + testify | stdlib only |
| Rust | cargo test (built-in) + mockall | — |
| PHP | phpunit + mockery | pest |
| Elixir | ExUnit (built-in) + ex_machina | — |

3. Ask the user to choose a framework (with a clear recommendation). If they decline, write `.gstack/no-test-bootstrap` and continue without tests.
4. Install packages, create config, create directory structure, create one example test.
5. **Generate 3-5 real tests for existing code (B4.5):**
   - Find recently changed files: `git log --since=30.days --name-only --format="" | sort | uniq -c | sort -rn | head -10`
   - Prioritize by risk: error handlers > business logic with conditionals > API endpoints > pure functions
   - For each file: write one test asserting real behavior — never `expect(x).toBeDefined()`
   - Run each test. Passes → keep. Fails → fix once. Still fails → delete silently.
   - Generate at least 1 test, cap at 5. Never import secrets or API keys in test files.
6. Run the full test suite to verify setup. If failing, debug once, then revert all bootstrap changes if still failing.
7. **Create CI/CD pipeline (B5.5):** If `.github/` exists (or no CI detected — default to GitHub Actions), create `.github/workflows/test.yml` with `runs-on: ubuntu-latest`, appropriate setup action for the runtime, the verified test command, and trigger: push + pull_request. If non-GitHub CI detected, skip and note: "Detected {provider} — CI pipeline generation supports GitHub Actions only."
8. **Create TESTING.md (B6):** If it already exists, update/append rather than overwrite. Include philosophy: *"100% test coverage is the key to great vibe coding. Tests let you move fast, trust your instincts, and ship with confidence — without them, vibe coding is just yolo coding. With tests, it's a superpower."* Include framework name, how to run tests, test layers (unit/integration/smoke/e2e), and conventions.
9. **Update CLAUDE.md (B7):** If `## Testing` section already exists, skip. Otherwise append with run command, reference to TESTING.md, and these expectations:
   - 100% test coverage is the goal — tests make vibe coding safe
   - When writing new functions, write a corresponding test
   - When fixing a bug, write a regression test
   - When adding error handling, write a test that triggers the error
   - When adding a conditional (if/else, switch), write tests for BOTH paths
   - Never commit code that makes existing tests fail
10. Commit bootstrap files: `chore: bootstrap test framework ({name})`

## Modes

### Full (default when URL is provided)
Systematic exploration. Visit every reachable page. Document 5-10 well-evidenced issues. Produce health score. Takes 5-15 minutes depending on app size.

### Quick (`--quick`)
30-second smoke test. Visit homepage + top 5 navigation targets. Check: page loads? Console errors? Broken links? Produce health score. No detailed issue documentation.

### Regression (`--regression <baseline>`)
Run full mode, then load `baseline.json` from a previous run. Diff: which issues are fixed? Which are new? What's the score delta? Append regression section to report.

### Phase 1: Initialize

Find the browser binary. Start timer for duration tracking. Create output directories at `.gstack/qa-reports/screenshots/`. Copy report template from `qa/templates/qa-report-template.md` to the output directory.

### Phase 2: Authenticate (if needed)

Navigate to login URL, fill the form (never include real passwords in the report — use `[REDACTED]`), submit, and verify login succeeded.

If cookie file provided, import it. If 2FA required, ask the user for the code and wait. If CAPTCHA appears, tell the user to complete it and say to continue.

### Phase 3: Orient

Navigate to the target URL. Take an annotated screenshot. Get a list of links to map navigation structure. Check console for errors on landing.

Detect framework from page source: `__next` or `_next/data` → Next.js, `csrf-token` meta → Rails, `wp-content` URLs → WordPress, client-side routing → SPA.

For SPAs, use interactive element discovery instead of link listing — client-side navigation won't appear in anchor tags.

### Diff-Aware Mode (automatic on feature branch with no URL)

This is the primary mode. When invoked without a URL on a feature branch:

1. Run `git diff main...HEAD --name-only` and `git log main..HEAD --oneline` to understand what changed
2. Map changed files to affected pages/routes: controller/route files → URL paths, view/component files → pages that render them, model/service files → pages that use them, CSS files → pages that include them
3. Auto-detect running app on common ports (3000, 4000, 8080). If not found, check for a staging/preview URL. If nothing, ask the user.
4. Test each affected page: navigate, screenshot, check console, test interactions end-to-end
5. Cross-reference with commit messages and PR description to understand intent — does the change do what it says?
6. Check `TODOS.md` for known bugs related to changed files

**If no pages are identifiable from the diff:** Still open the browser. Backend, config, and infrastructure changes affect app behavior. Fall back to Quick mode — homepage + top 5 navigation targets + console check.

### Phase 4: Explore

Visit pages systematically. For each page:
1. Navigate and take an annotated screenshot
2. Check console for errors
3. Per-page checklist:
   - Visual scan: layout issues visible in screenshot?
   - Interactive elements: click buttons, links, controls — do they respond?
   - Forms: fill and submit, test empty, invalid, edge case inputs
   - Navigation: check all paths in and out
   - States: empty state, loading, error, overflow
   - Console: any new JS errors after interactions?
   - Responsiveness: check mobile viewport (375x812) if relevant
4. Spend more time on core features (dashboard, checkout, search), less on secondary pages (about, terms)

**Framework-specific checks:**
- **Next.js:** Hydration errors, `_next/data` 404s, CLS on dynamic content
- **Rails:** N+1 query warnings, CSRF token presence, Turbo/Stimulus transitions, flash messages
- **WordPress:** Plugin conflicts, admin bar visibility, `/wp-json/` endpoints, mixed content
- **SPAs:** Stale state after navigation, browser back/forward history handling

### Phase 5: Document

Document each issue immediately when found — do not batch.

**Interactive bugs** (broken flows, dead buttons, form failures):
- Screenshot before the action
- Perform the action
- Screenshot showing the result
- Diff view to show what changed
- Write repro steps referencing screenshots

**Static bugs** (typos, layout issues, missing images):
- Single annotated screenshot showing the problem
- Description of what's wrong

Write each issue to the report as you find it using the standard issue template.

### Phase 6: Wrap Up

Compute the health score. Write "Top 3 Things to Fix." Summarize console errors across all pages. Fill in report metadata (date, duration, pages visited, screenshot count, framework).

**Health Score Rubric** (weighted average):

| Category | Weight | Scoring |
|----------|--------|---------|
| Console | 15% | 0 errors=100, 1-3=70, 4-10=40, 10+=10 |
| Links | 10% | 0 broken=100, each broken link -15 |
| Visual | 10% | Start 100, Critical -25, High -15, Medium -8, Low -3 |
| Functional | 20% | Same deduction scale |
| UX | 15% | Same deduction scale |
| Performance | 10% | Same deduction scale |
| Content | 5% | Same deduction scale |
| Accessibility | 15% | Same deduction scale |

Save `baseline.json` for regression mode comparison.

### Phase 7: Triage

Sort all discovered issues by severity. Decide which to fix based on tier:
- **Quick:** Fix critical + high only
- **Standard:** Fix critical + high + medium
- **Exhaustive:** Fix all

Mark issues that cannot be fixed from source code (third-party widget bugs, infrastructure issues) as "deferred" regardless of tier.

### Phase 8: Fix Loop

For each fixable issue in severity order:

**8a. Locate source:** Search for error messages, component names, route definitions. Find the specific source file(s).

**8b. Fix:** Make the minimal fix — smallest change that resolves the issue. Do NOT refactor surrounding code, add features, or improve unrelated things.

**8c. Commit:** `git commit -m "fix(qa): ISSUE-NNN — short description"`. One commit per fix. Never bundle multiple fixes.

**8d. Re-test:** Navigate back to the affected page. Take before/after screenshot pair. Check console for errors.

**8e. Classify:**
- **verified** — re-test confirms the fix works, no new errors
- **best-effort** — fix applied but couldn't fully verify (needs auth state, external service)
- **reverted** — regression detected, run `git revert HEAD`, mark issue as "deferred"

**8e.5. Regression Test (for verified non-CSS fixes):**

Before writing the test, trace the bug's codepath:
- What input/state triggered the bug?
- What codepath did it follow?
- Where did it break?
- What other inputs could hit the same codepath?

The test MUST set up the exact precondition that triggered the bug, perform the action that exposed it, and assert correct behavior — not just "it renders" or "it doesn't throw."

Match the project's existing test patterns exactly (file naming, imports, assertion style, describe/it nesting). Read 2-3 nearby test files first.

Include attribution comment:
```
// Regression: ISSUE-NNN — {what broke}
// Found by /qa on {YYYY-MM-DD}
// Report: .gstack/qa-reports/qa-report-{domain}-{date}.md
```

Run only the new test file. If it passes, commit: `test(qa): regression test for ISSUE-NNN`. If it fails after one fix attempt, delete it and defer.

**8f. Self-Regulation (every 5 fixes):**

Compute WTF-likelihood:
```
Start at 0%
Each revert:                +15%
Each fix touching >3 files: +5%
After fix 15:               +1% per additional fix
All remaining Low severity: +10%
Touching unrelated files:   +20%
```

If WTF > 20%: STOP. Show the user what's been done. Ask whether to continue.

Hard cap: 50 fixes total.

### Phase 9: Final QA

Re-run QA on all affected pages after fixes are applied. Compute final health score. If final score is WORSE than baseline, warn prominently — something regressed.

### Phase 10: Report

Write report to `.gstack/qa-reports/qa-report-{domain}-{YYYY-MM-DD}.md`.

Per-issue additions: Fix Status, Commit SHA, Files Changed, Before/After screenshots.

Summary section: total issues found, fixes applied (verified/best-effort/reverted), deferred issues, health score delta (baseline → final).

PR summary line: "QA found N issues, fixed M, health score X → Y."

### Phase 11: TODOS.md Update

If the repo has a `TODOS.md`:
- Add new deferred bugs as TODOs with severity, category, and repro steps
- Annotate fixed bugs that were in TODOS.md: "Fixed by /qa on {branch}, {date}"

## Quality Gates

**Non-negotiable rules:**
1. Repro is everything. Every issue needs at least one screenshot. No exceptions.
2. Verify before documenting. Retry the issue once to confirm reproducibility.
3. Never include credentials. Write `[REDACTED]` for passwords in repro steps.
4. Write incrementally. Append each issue to the report as you find it. Do not batch.
5. Never read source code. Test as a user, not a developer.
6. Check console after every interaction. JS errors that don't surface visually are still bugs.
7. Test like a user. Use realistic data. Walk through complete workflows end-to-end.
8. Depth over breadth. 5-10 well-documented issues > 20 vague descriptions.
9. Never delete output files. Screenshots and reports accumulate — that's intentional.
10. Use `snapshot -C` for tricky UIs. Finds clickable divs that the accessibility tree misses.
11. Display screenshots inline for the user. After every screenshot command, read the output file so the user can see it. For responsive screenshots (3 files), read all three. Without this, screenshots are invisible.
12. Never refuse to use the browser. `/qa` means browser-based testing. No substitutes — not evals, not unit tests.
13. Only modify tests when generating regression tests in Phase 8e.5. Never modify CI configuration. Never modify existing tests — only create new test files.
14. Revert on regression. If a fix makes things worse, `git revert HEAD` immediately.
15. Self-regulate. Follow the WTF-likelihood heuristic. When in doubt, stop and ask.

**Done when:**
- Health score computed (baseline and final)
- All tier-appropriate issues either fixed, best-effort, reverted, or deferred
- Before/after screenshot evidence for every fixed issue
- Regression tests committed for verified non-CSS fixes
- Report written and TODOS.md updated

## Outputs

```
.gstack/qa-reports/
├── qa-report-{domain}-{YYYY-MM-DD}.md   # Structured report
├── screenshots/
│   ├── initial.png                       # Landing page
│   ├── issue-001-step-1.png              # Per-issue evidence
│   ├── issue-001-result.png
│   ├── issue-001-before.png              # Before fix
│   ├── issue-001-after.png               # After fix
│   └── ...
└── baseline.json                         # For regression mode
```

Also writes `~/.gstack/projects/{slug}/{user}-{branch}-test-outcome-{datetime}.md` for cross-session context.

## Feeds Into

- `>ship` — QA is the natural gate before shipping
- `>design-review` — functional QA done, visual polish next
- `>cso` — security audit on the same codebase

## Harness Notes

**Browser automation is a hard dependency.** This skill requires the `browse` daemon (`$B`) for navigation, screenshots, console access, and interaction testing. The browser binary needs a one-time build before first use.

**CDP mode detection:** Check if the browser is connected to the user's real browser session (`$B status | grep "Mode: cdp"`). If in CDP mode, skip cookie import and headless detection workarounds — real auth sessions are already available.

See `harness-compat.md: "Browse daemon setup"` and `"CDP vs headless mode"`.
