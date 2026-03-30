# Canary

> Post-deploy production monitoring: watches the live app for console errors, performance regressions, and page failures using browser automation, compares against pre-deploy baselines, and alerts on anomalies.

## When to Use

- Right after a deploy, to verify production is healthy
- User says "monitor deploy", "canary", "post-deploy check", "watch production", "verify deploy"
- After `/land-and-deploy` completes -- it suggests `/canary` for extended monitoring
- Before deploying, with `--baseline`, to capture a reference snapshot

## Arguments

- `/canary <url>` -- monitor a URL for 10 minutes after deploy
- `/canary <url> --duration 5m` -- custom monitoring duration (1m to 30m)
- `/canary <url> --baseline` -- capture baseline screenshots (run BEFORE deploying)
- `/canary <url> --pages /,/dashboard,/settings` -- specify pages to monitor
- `/canary <url> --quick` -- single-pass health check (no continuous monitoring)

## Inputs

- A production (or staging) URL
- Optional: `--baseline` to capture pre-deploy snapshot
- Optional: `--duration Nm` to set monitoring window (default 10 minutes, 1-30 min range)
- Optional: `--pages /path1,/path2,...` to specify pages
- Optional: `--quick` for a single-pass health check instead of continuous monitoring

## Methodology

### Setup (before any browse commands)

Check that the headless browser binary is available. If `NEEDS_SETUP`: tell the user "gstack browse needs a one-time build (~10 seconds). OK to proceed?" Stop and wait for confirmation before building.

Parse arguments. Set default duration to 10 minutes. Create directories for reports, baselines, and screenshots at `.gstack/canary-reports/`, `.gstack/canary-reports/baselines/`, `.gstack/canary-reports/screenshots/`.

### Phase 1: Baseline capture (--baseline mode only)

Run this BEFORE deploying to establish a reference state. For each page specified (or the homepage):
1. Load the page.
2. Take an annotated screenshot.
3. Collect console errors.
4. Collect page load time.
5. Collect page text content.

Save to `.gstack/canary-reports/baseline.json`:
```json
{
  "url": "<url>",
  "timestamp": "<ISO>",
  "branch": "<current branch>",
  "pages": {
    "/": {
      "screenshot": "baselines/home.png",
      "console_errors": 0,
      "load_time_ms": 450
    }
  }
}
```

Stop and tell user: "Baseline captured. Deploy your changes, then run `/canary <url>` to monitor."

### Phase 2: Page discovery (if no --pages specified)

Load the root URL. Extract navigation links. Present the top 5 internal links to the user and confirm which pages to monitor. Always include the homepage.

Options: use these discovered pages (recommended), add more pages, or monitor homepage only.

### Phase 3: Pre-deploy snapshot (if no baseline exists)

If no `baseline.json` exists, take a quick snapshot of the current state as a reference point. For each page: screenshot (numbered `pre-<page-name>.png`), console error count, page load time. These become the regression detection baseline for the monitoring loop.

### Phase 4: Continuous monitoring loop

Every 60 seconds, for each page:
1. Load the page.
2. Take an annotated screenshot (numbered by check: `<page-name>-<check-number>.png`).
3. Collect console errors.
4. Collect performance data.

After each check, compare against baseline (or pre-deploy snapshot):

| Change type | Severity |
|-------------|----------|
| Page load failure (error or timeout) | CRITICAL |
| New console errors not in baseline | HIGH |
| Load time exceeds 2x baseline | MEDIUM |
| New 404s not in baseline | LOW |

**Alert on changes, not absolutes.** A page with 3 baseline console errors is fine at 3. One new error is a HIGH alert. A page that was slow before is not flagged for being slow now.

**Transient tolerance.** Only alert on patterns that persist across 2+ consecutive checks. A single blip is not an alert.

**On CRITICAL or HIGH alert:** immediately notify the user with:

```
CANARY ALERT
════════════
Time:     [timestamp, e.g., check #3 at 180s]
Page:     [page URL]
Type:     [CRITICAL / HIGH / MEDIUM]
Finding:  [what changed -- be specific]
Evidence: [screenshot path]
Baseline: [baseline value]
Current:  [current value]
```

Ask:
- A) Investigate now -- stop monitoring, focus on this issue
- B) Continue monitoring -- this might be transient (wait for next check)
- C) Rollback -- revert the deploy immediately
- D) Dismiss -- false positive, continue monitoring

### Phase 5: Health report

After monitoring completes (or user stops early):

```
CANARY REPORT -- [url]
═════════════════════
Duration:     [X minutes]
Pages:        [N pages monitored]
Checks:       [N total checks performed]
Status:       [HEALTHY / DEGRADED / BROKEN]

Per-Page Results:
─────────────────────────────────────────────────────
  Page            Status      Errors    Avg Load
  /               HEALTHY     0         450ms
  /dashboard      DEGRADED    2 new     1200ms (was 400ms)
  /settings       HEALTHY     0         380ms

Alerts Fired:  [N] (X critical, Y high, Z medium)
Screenshots:   .gstack/canary-reports/screenshots/

VERDICT: [DEPLOY IS HEALTHY / DEPLOY HAS ISSUES -- details above]
```

Save report to `.gstack/canary-reports/{date}-canary.md` and `{date}-canary.json`.

Log a JSONL entry to `~/.gstack/projects/$SLUG/`:
```json
{"skill":"canary","timestamp":"<ISO>","status":"HEALTHY|DEGRADED|BROKEN","url":"<url>","duration_min":N,"alerts":N}
```

### Phase 6: Baseline update

If the deploy is healthy, offer to update the baseline with current screenshots. If user accepts, copy latest screenshots to baselines directory and update `baseline.json`.

## Quality Gates

**Alert thresholds:**
- CRITICAL: page fails to load (error or timeout)
- HIGH: new console errors compared to baseline
- MEDIUM: load time > 2x baseline
- LOW: new 404s not in baseline

**Transient rule:** alert only after 2+ consecutive checks confirm the issue.

**Verdict criteria:**
- HEALTHY: all pages loaded, no new errors, performance within 2x baseline
- DEGRADED: some pages have new errors or performance regressions
- BROKEN: one or more pages fail to load

## Important Rules

- **Speed matters.** Start monitoring within 30 seconds of invocation. Don't over-analyze before starting.
- **Alert on changes, not absolutes.** Compare against baseline, not industry standards.
- **Screenshots are evidence.** Every alert includes a screenshot path. No exceptions.
- **Transient tolerance.** Only alert on patterns that persist across 2+ consecutive checks.
- **Baseline is king.** Without a baseline, canary is a health check. Encourage `--baseline` before deploying.
- **Performance thresholds are relative.** 2x baseline = regression. 1.5x might be normal variance.
- **Read-only.** Observe and report. Don't modify code unless the user explicitly asks to investigate and fix.

## Outputs

- Per-page health status with before/after metrics
- Annotated screenshots at `.gstack/canary-reports/screenshots/`
- CANARY REPORT summary (`.md` + `.json`)
- JSONL log entry for the project dashboard
- Updated baseline (optional, user-confirmed)

## Feeds Into

- >retro (canary verdict and alert counts feed into code quality signals section)

## Harness Notes

**Browse dependency:** This skill is entirely browser-dependent. Every check (goto, console errors, perf, screenshot, text extraction) requires headless browser automation. Without a browser, substitute with `curl` for basic HTTP health checks only -- console error detection and screenshot evidence are unavailable. The setup check (READY/NEEDS_SETUP) must pass before any Phase starts.

**Read-only by default.** Canary observes and reports. It never modifies code. If investigation is needed after a CRITICAL alert, that's a separate debugging workflow.
