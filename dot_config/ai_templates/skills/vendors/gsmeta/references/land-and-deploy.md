# Land and Deploy

> Merge the PR, wait for CI and deploy, verify production health -- the step after /ship that gets code live and confirmed.

## When to Use

- After `/ship` has created the PR and it's ready to merge
- User says "merge", "land", "deploy", "merge and verify", "land it", "ship it to production"
- Currently GitHub-only (GitLab: stop with "GitLab support for /land-and-deploy is not yet implemented. Merge manually via the GitLab web UI.")

## Arguments

- `/land-and-deploy` -- auto-detect PR from current branch, no post-deploy URL
- `/land-and-deploy <url>` -- auto-detect PR, verify deploy at this URL
- `/land-and-deploy #123` -- specific PR number
- `/land-and-deploy #123 <url>` -- specific PR + verification URL

## Inputs

- An open PR on GitHub (auto-detected from current branch, or specified as `#NNN`)
- Optional: production URL for canary verification (pass as argument)
- GitHub CLI authenticated (`gh auth login`)
- Optional: `## Deploy Configuration` section in CLAUDE.md with platform and production URL

## Methodology

### Step 0: Detect platform

Detect the base branch the same way as `/ship`. If platform is GitLab, stop immediately: "GitLab support for /land-and-deploy is not yet implemented. Merge manually via the GitLab web UI."

### Step 1: Pre-flight

1. Check `gh auth status`. If not authenticated, stop: "Run `gh auth login` to connect, then try `/land-and-deploy` again."
2. Parse arguments: save PR number (if specified) and production URL (if provided) for canary verification in Step 7.
3. Auto-detect from current branch: `gh pr view --json number,state,title,url,mergeStateStatus,mergeable,baseRefName,headRefName`. Tell the user: "Found PR #NNN -- '{title}' (branch → base)."
4. Validate PR state:
   - No PR: stop. "Run `/ship` first to create a PR."
   - MERGED: "This PR is already merged -- run `/canary <url>` to verify the deploy."
   - CLOSED: stop. "Reopen it on GitHub first."
   - OPEN: continue.

**Never stop for:** choosing merge method (auto-detect from repo settings), timeout warnings (warn and continue).

**Always stop for:** GH CLI not authenticated, no PR found, CI failures or merge conflicts, permission denied, deploy workflow failure (offer revert), production health issues detected by canary (offer revert).

### Step 1.5: First-run dry-run validation

Check `~/.gstack/projects/$SLUG/land-deploy-confirmed`. Detect config change by hashing the `## Deploy Configuration` section from CLAUDE.md + deploy/CD workflow files.

**If CONFIRMED (no config change):** "I've deployed this project before. Moving straight to readiness checks." Proceed to Step 2.

**If CONFIG_CHANGED:** "Your deploy configuration has changed since last time. Re-running dry run." Then run the FIRST_RUN flow.

**If FIRST_RUN:** Tell the user: "This is the first time I'm deploying this project, so I'm going to do a dry run first. I'll detect your deploy infrastructure, test that my commands work, and show you exactly what will happen -- before I touch anything. Deploys are irreversible once they hit production."

#### 1.5a: Deploy infrastructure detection

Check CLAUDE.md for a persisted `## Deploy Configuration` section (use platform and production URL from there if present). Auto-detect from config files: `fly.toml` (Fly), `render.yaml` (Render), `vercel.json`/`.vercel/` (Vercel), `netlify.toml` (Netlify), `Procfile` (Heroku), `railway.json`/`railway.toml` (Railway). Detect deploy workflows by scanning `.github/workflows/*.yml` for `deploy|release|production|cd`. Also detect staging workflows (`staging` keyword).

#### 1.5b: Command validation

Test each detected command. Build and display a validation table:

```
╔══════════════════════════════════════════════════════════╗
║         DEPLOY INFRASTRUCTURE VALIDATION                  ║
╠══════════════════════════════════════════════════════════╣
║  Platform:    {platform} (from {source})                  ║
║  App:         {app name or "N/A"}                         ║
║  Prod URL:    {url or "not configured"}                   ║
║                                                           ║
║  COMMAND VALIDATION                                       ║
║  ├─ gh auth status:     ✓ PASS                            ║
║  ├─ {platform CLI}:     ✓ PASS / ⚠ NOT INSTALLED / ✗ FAIL║
║  ├─ curl prod URL:      ✓ PASS (200 OK) / ⚠ UNREACHABLE  ║
║  └─ deploy workflow:    {file or "none detected"}         ║
║                                                           ║
║  STAGING DETECTION                                        ║
║  ├─ Staging URL:        {url or "not configured"}         ║
║  ├─ Staging workflow:   {file or "not found"}             ║
║  └─ Preview deploys:    {detected or "not detected"}      ║
║                                                           ║
║  WHAT WILL HAPPEN                                         ║
║  1. Run pre-merge readiness checks (reviews, tests, docs) ║
║  2. Wait for CI if pending                                ║
║  3. Merge PR via {merge method}                           ║
║  4. {Wait for deploy workflow / Wait 60s / Skip}          ║
║  5. {Run canary verification / Skip (no URL)}             ║
║                                                           ║
║  MERGE METHOD: {squash/merge/rebase} (from repo settings) ║
║  MERGE QUEUE:  {detected / not detected}                  ║
╚══════════════════════════════════════════════════════════╝
```

Validation failures are WARNINGS, not blockers (except gh auth which already stopped in Step 1). If curl fails, note it and explain the impact on verification. If platform CLI is missing, note you'll use HTTP health checks instead.

#### 1.5c: Staging detection

Check in order: CLAUDE.md persisted config, GitHub Actions workflows containing "staging", Vercel/Netlify preview URLs in PR checks (`gh pr checks --json name,targetUrl`). Record any staging targets found for Step 5.

#### 1.5d: Readiness preview

Preview review status without re-running tests: read the stored review log and show a summary of which reviews have run and how stale they are. Explain in plain English: "When I merge, I'll check: has the code been reviewed recently? Do the tests pass? Is the CHANGELOG updated? Is the PR description accurate?"

#### 1.5e: Dry-run confirmation

Present the full dry-run results and ask: that's right -- proceed (A), something's off -- stop (B), or configure more carefully with `/setup-deploy` (C).

If A: save the deploy config fingerprint (CLAUDE.md deploy section hash + workflow file hashes) to `~/.gstack/projects/$SLUG/land-deploy-confirmed`. "I've saved this configuration. Next time I'll skip the dry run. If your deploy setup changes, I'll automatically re-run it."

If B: STOP. "Tell me what's different and I'll adjust."

If C: STOP. "Run `/setup-deploy` to configure, then `/land-and-deploy` again."

### Step 2: Pre-merge checks

Run `gh pr checks --json name,state,status,conclusion`. 
- Any required checks FAILING: stop. "CI is failing. Fix before deploying -- I won't merge code that hasn't passed CI."
- Checks PENDING: tell user, proceed to wait.
- All pass: skip wait, go to readiness gate.

Check for merge conflicts: `gh pr view --json mergeable -q .mergeable`. If CONFLICTING: stop.

### Step 3: Wait for CI

If checks pending, run `gh pr checks --watch --fail-fast`. Timeout: 15 minutes.

- Passes: "CI passed after {duration}." Continue.
- Fails: stop. Show failures.
- Timeout (15 min): stop. "CI has been running over 15 minutes -- something may be stuck. Check the GitHub Actions tab."

### Step 3.5: Pre-merge readiness gate

**This is the last irreversible gate.** "CI is green. Now I'm running readiness checks -- this is the last gate before I merge. Once you approve, the merge is final."

Collect evidence for each check. Track warnings (yellow) and blockers (red).

#### 3.5a: Review staleness check

Read the stored review log. For each review skill, find the most recent entry within 7 days and compare its `commit` field against HEAD with `git rev-list --count STORED_COMMIT..HEAD`.

**Staleness rules:**
- 0 commits since review: CURRENT
- 1-3 commits since review: RECENT (flag yellow if those commits touch code, not just docs)
- 4+ commits since review: STALE (red -- review may not reflect current code)
- No review found: NOT RUN

**Critical check:** run `git log --oneline STORED_COMMIT..HEAD`. If commits after the review contain "fix", "refactor", "rewrite", "overhaul", or touch more than 5 files -- flag as STALE (significant changes since review).

Also check adversarial review (`codex-review`). If current, mention as an extra confidence signal.

**Inline review offer (if STALE or NOT RUN):** Ask -- run a quick review (~2 min, scan diff for SQL safety/race conditions/security gaps, Completeness: 7/10), stop and run full `/review` (Completeness: 10/10), or skip (user reviewed themselves, Completeness: 3/10).

If quick review chosen: read the review checklist, apply to the diff, auto-fix trivial issues, ask about critical findings. If any code changes made: commit fixes, **STOP**, tell user to re-run `/land-and-deploy`.

If review CURRENT: skip this sub-step entirely.

#### 3.5b: Test results

Run the test command from CLAUDE.md (or `bun test`). Failing tests = BLOCKER.

Check E2E results from today: look for recent eval files in `~/.gstack-dev/evals/*-e2e-*-{today}*.json`. If none: WARNING. If failures exist: WARNING with list.

Check LLM judge evals from today: `~/.gstack-dev/evals/*-llm-judge-*-{today}*.json`. If none: note "No LLM evals run today."

#### 3.5c: PR body accuracy check

Read current PR body and compare against `git log <base>..HEAD --oneline`. Flag:
1. Missing features -- commits that add significant functionality not mentioned in PR
2. Stale descriptions -- PR body mentions things that were later changed or reverted
3. Wrong version -- PR references a version that doesn't match VERSION file

If stale or incomplete: WARNING.

#### 3.5d: Document-release check

Check if CHANGELOG.md and VERSION were modified on this branch. If not modified and the diff includes new features: WARNING -- "/document-release likely not run. CHANGELOG and VERSION not updated despite new features."

If docs-only change: skip.

#### 3.5e: Readiness report and confirmation

```
╔══════════════════════════════════════════════════════════╗
║              PRE-MERGE READINESS REPORT                  ║
╠══════════════════════════════════════════════════════════╣
║  PR: #NNN -- title                                       ║
║  Branch: feature → main                                  ║
║                                                          ║
║  REVIEWS                                                 ║
║  ├─ Eng Review:    CURRENT / STALE (N commits) / --      ║
║  ├─ CEO Review:    CURRENT / -- (optional)               ║
║  ├─ Design Review: CURRENT / -- (optional)               ║
║  └─ Codex Review:  CURRENT / -- (optional)               ║
║                                                          ║
║  TESTS                                                   ║
║  ├─ Free tests:    PASS / FAIL (blocker)                 ║
║  ├─ E2E tests:     52/52 pass (25 min ago) / NOT RUN     ║
║  └─ LLM evals:     PASS / NOT RUN                        ║
║                                                          ║
║  DOCUMENTATION                                           ║
║  ├─ CHANGELOG:     Updated / NOT UPDATED (warning)       ║
║  ├─ VERSION:       0.9.8.0 / NOT BUMPED (warning)        ║
║  └─ Doc release:   Run / NOT RUN (warning)               ║
║                                                          ║
║  PR BODY                                                 ║
║  └─ Accuracy:      Current / STALE (warning)             ║
║                                                          ║
║  WARNINGS: N  |  BLOCKERS: N                             ║
╚══════════════════════════════════════════════════════════╝
```

Translate warnings to plain English (not jargon). Example: "The engineering review was done 6 commits ago -- the code has changed since then."

If BLOCKERS (failing free tests): cannot merge. Ask to hold and fix.

User chooses: merge (A, green or minor warnings), hold and fix (B, with specific next steps given), or merge anyway with acknowledged warnings (C, Completeness: 3/10).

If B: give specific next steps:
- Stale reviews: "Run `/review` or `/autoplan`, then `/land-and-deploy` again."
- E2E not run: "Run your E2E tests, then come back."
- Docs not updated: "Run `/document-release` to update CHANGELOG and docs."
- PR body stale: "Update the PR description on GitHub."

If A or C: "Merging now." Continue.

### Step 4: Merge the PR

Record start timestamp and merge path.

Try auto-merge first (respects repo merge settings and merge queues):
```
gh pr merge --auto --delete-branch
```

If `--auto` unavailable, merge directly:
```
gh pr merge --squash --delete-branch
```

If permission denied: stop. "I don't have permission to merge. Check branch protection rules."

**Merge queue detection:** If `MERGE_PATH=auto` and PR doesn't immediately become MERGED, it's in a merge queue. Tell user: "Your repo uses a merge queue -- GitHub will run CI one more time on the final merge commit. I'll keep checking." Poll `gh pr view --json state -q .state` every 30 seconds, up to 30 minutes. Show progress every 2 minutes: "Still in the merge queue... ({X}m so far)."

If PR state changes to MERGED: capture merge commit SHA. If PR removed from queue (back to OPEN): stop and explain. If timeout (30 min): stop.

**CI auto-deploy detection:** After merge, run `gh run list --branch <base> --limit 5 --json name,status,workflowName,headSha`. If deploy workflow found: tell user. If not found: tell user and explain the next step will figure out verification strategy.

### Step 5: Deploy strategy detection

Read CLAUDE.md for persisted deploy config. Auto-detect platform from files and GitHub Actions workflows. Run `gstack-diff-scope` to classify the diff (FRONTEND, BACKEND, DOCS, CONFIG).

**Decision tree (in order):**
1. User provided production URL: use for canary, also check for deploy workflows.
2. GitHub Actions deploy workflow detected (`deploy|release|production|cd` in workflow names): poll in Step 6, then run canary.
3. Diff is SCOPE_DOCS only (no frontend, backend, or config): skip verification entirely. "Docs-only change -- nothing to deploy or verify. You're all set." Go to Step 9.
4. No workflow and no URL: ask once -- provide URL or confirm no deploy needed (library/CLI).

**Staging-first option:** If staging was detected in Step 1.5c and changes include code, offer staging-first:
- A) Deploy to staging first, verify, then go to production automatically (Completeness: 10/10)
- B) Skip staging -- go straight to production (Completeness: 7/10)
- C) Deploy to staging only -- check production later (Completeness: 8/10)

If A: run Steps 6-7 against staging first, then automatically against production.
If C: run Steps 6-7 against staging only. Print deploy report with "STAGING VERIFIED -- production deploy pending." Stop -- user can re-run later.
If no staging detected: skip this sub-step silently.

### Step 6: Wait for deploy

**Strategy A -- GitHub Actions workflow:** match run by merge commit SHA. Poll `gh run view <run-id> --json status,conclusion` every 30 seconds. Timeout: 20 minutes.

**Strategy B -- Platform CLI:**
- Fly.io: `fly status --app {app}` -- check for `started` machines.
- Render: poll production URL with `curl -sf {url} -o /dev/null -w "%{http_code}"` every 30 seconds (deploys take 2-5 minutes).
- Heroku: `heroku releases --app {app} -n 1`.

**Strategy C -- Auto-deploy platforms (Vercel, Netlify):** wait 60 seconds, proceed directly to canary.

**Strategy D -- Custom deploy hooks:** run the command from CLAUDE.md `Custom deploy hooks` section.

Show progress every 2 minutes: "Deploy is still running... ({X}m so far). This is normal."

If deploy succeeds: "Deploy finished. Took {duration}. Now verifying the site." Record deploy duration.

If deploy fails: ask to investigate logs (A), revert immediately (B), or continue to health checks anyway (C).

If timeout (20 min): ask whether to continue waiting or skip verification.

### Step 7: Canary verification (conditional depth)

Depth scales with diff scope:

| Diff Scope | Canary Depth |
|------------|-------------|
| SCOPE_DOCS only | Already skipped in Step 5 |
| SCOPE_CONFIG only | Smoke: load URL + verify 200 status |
| SCOPE_BACKEND only | Console errors + perf check |
| SCOPE_FRONTEND (any) | Full: console + perf + screenshot |
| Mixed scopes | Full canary |

**Full canary sequence:**
1. Load the URL, verify 200 status.
2. Check console for critical errors (Error, Uncaught, Failed to load, TypeError, ReferenceError). Ignore warnings.
3. Verify page load time under 10 seconds.
4. Check page has real content (not blank, not generic error page).
5. Take an annotated screenshot and save to `.gstack/deploy-reports/post-deploy.png`.

**Health assessment:** all four checks pass → HEALTHY. Continue to Step 9.

If any fail: show evidence (screenshot path, console errors, perf numbers). Ask:
- A) That's expected -- still warming up. Mark as healthy.
- B) That's broken -- revert the merge and roll back.
- C) Let me investigate more -- open the site and look at logs.

### Step 8: Revert (if needed)

Tell user: "Reverting now. This creates a new commit that undoes all changes. The previous version will be restored once the revert deploys."

```
git fetch origin <base>
git checkout <base>
git revert <merge-commit-sha> --no-edit
git push origin <base>
```

If revert has conflicts: explain and show the SHA for manual resolution.

If base branch has push protections: create a revert PR instead (`gh pr create --title 'revert: <original PR title>'`).

After successful revert: "Revert pushed. Deploy should roll back automatically once CI passes. Keep an eye on the site." Note revert commit SHA. Continue to Step 9 with status REVERTED.

### Step 9: Deploy report

Create `.gstack/deploy-reports/` directory. Display the ASCII summary:

```
LAND & DEPLOY REPORT
═════════════════════
PR:           #<number> -- <title>
Branch:       <head-branch> → <base-branch>
Merged:       <timestamp> (<merge method>)
Merge SHA:    <sha>
Merge path:   <auto-merge / direct / merge queue>
First run:    <yes (dry-run validated) / no (previously confirmed)>

Timing:
  Dry-run:    <duration or "skipped (confirmed)">
  CI wait:    <duration>
  Queue:      <duration or "direct merge">
  Deploy:     <duration or "no workflow detected">
  Staging:    <duration or "skipped">
  Canary:     <duration or "skipped">
  Total:      <end-to-end duration>

Reviews:
  Eng review: <CURRENT / STALE / NOT RUN>
  Inline fix: <yes (N fixes) / no / skipped>

CI:           <PASSED / SKIPPED>
Deploy:       <PASSED / FAILED / NO WORKFLOW / CI AUTO-DEPLOY>
Staging:      <VERIFIED / SKIPPED / N/A>
Verification: <HEALTHY / DEGRADED / SKIPPED / REVERTED>
  Scope:      <FRONTEND / BACKEND / CONFIG / DOCS / MIXED>
  Console:    <N errors or "clean">
  Load time:  <Xs>
  Screenshot: <path or "none">

VERDICT: <DEPLOYED AND VERIFIED / DEPLOYED (UNVERIFIED) / STAGING VERIFIED / REVERTED>
```

Save to `.gstack/deploy-reports/{date}-pr{number}-deploy.md`.

Log a JSONL entry to `~/.gstack/projects/$SLUG/`:
```json
{"skill":"land-and-deploy","timestamp":"...","status":"SUCCESS|REVERTED","pr":N,"merge_sha":"...","merge_path":"auto|direct|queue","first_run":true,"deploy_status":"HEALTHY|DEGRADED|SKIPPED","staging_status":"VERIFIED|SKIPPED","review_status":"CURRENT|STALE|NOT_RUN|INLINE_FIX","ci_wait_s":N,"queue_s":N,"deploy_s":N,"staging_s":N,"canary_s":N,"total_s":N}
```

### Step 10: Suggest follow-ups

- DEPLOYED AND VERIFIED: "Your changes are live and verified. Nice ship."
- DEPLOYED (UNVERIFIED): "Your changes are merged and should be deploying. Check it manually when you get a chance."
- REVERTED: "The merge was reverted. Your changes are no longer on {base}. The PR branch is still available."

Suggest follow-ups:
- If production URL was verified: "Want extended monitoring? Run `/canary <url>` to watch the site for 10 minutes."
- If performance data collected: "Want a deeper performance analysis? Run `/benchmark <url>`."
- "Need to update docs? Run `/document-release` to sync README, CHANGELOG, and other docs with what you shipped."

## Important Rules

- **Never force push.** Use `gh pr merge` only.
- **Never skip CI.** If checks are failing, stop and explain.
- **Narrate the journey.** User should always know: what just happened, what's happening now, what's about to happen next. No silent gaps.
- **Auto-detect everything.** PR number, merge method, deploy strategy, project type, merge queues, staging environments. Ask only when information genuinely can't be inferred.
- **Poll with backoff.** 30-second intervals for CI/deploy, with reasonable timeouts. Don't hammer the GitHub API.
- **Revert is always an option.** At every failure point, offer revert. Explain what reverting does in plain English.
- **Single-pass verification, not continuous monitoring.** `/land-and-deploy` checks once. `/canary` does the extended monitoring loop.
- **Clean up.** Delete the feature branch after merge (via `--delete-branch`).
- **First run = teacher mode.** Walk the user through everything. Explain what each check does. Let them confirm before proceeding. Build trust through transparency.
- **Subsequent runs = efficient mode.** Brief status updates, no re-explanations. Just do the job and report results.
- **Goal: first-timers think "wow, this is thorough -- I trust it." Repeat users think "that was fast -- it just works."**

## Quality Gates

- **Hard stops:** no GH CLI auth, no PR found, CI failing, merge conflicts, deploy workflow failure (with revert option), production health issues (with revert option).
- **Soft gates (user decides):** stale reviews, missing docs update, PR body inaccurate, deploy warning states.
- **First-run confirmation required:** before first merge on a project, always show full dry-run validation and wait for explicit user approval.

## Outputs

- Merged PR (branch deleted)
- Deploy verified at production URL (if applicable)
- Post-deploy screenshot at `.gstack/deploy-reports/post-deploy.png`
- Deploy report at `.gstack/deploy-reports/{date}-pr{number}-deploy.md`
- JSONL log entry for the review dashboard

## Feeds Into

- >canary (extended production monitoring after deploy)
- >document-release (update docs after landing)

## Harness Notes

**Browse dependency:** Canary verification uses headless browser (`goto`, `console --errors`, `perf`, `snapshot`). Without browser support, canary runs as smoke-only (HTTP status check). Deploy report shows "DEPLOYED (UNVERIFIED)" instead of "DEPLOYED AND VERIFIED."

**GitHub-only:** GitLab MR merge is not implemented. Skill stops with instructions to merge manually if GitLab is detected.

**Persistent state:** Deploy config fingerprint stored at `~/.gstack/projects/$SLUG/land-deploy-confirmed` to skip dry-run on subsequent invocations. In stateless harnesses, dry-run runs every time.
