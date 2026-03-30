# QA-Only

> Report-only QA testing: systematically tests a web application and produces a structured report with health score, screenshots, and repro steps — but never fixes anything.

## When to Use

- User says "just report bugs", "qa report only", or "test but don't fix"
- When you want a bug report without any code changes
- When you need a QA audit to hand off to someone else to fix
- Pre-meeting snapshot of current app state
- For the full test-fix-verify loop, use `>qa` instead

## Inputs

- Running web application (local dev server or URL). If on a feature branch with no URL, the skill auto-detects a local server.
- Optional: auth credentials or cookie file for authenticated testing
- Optional: `--quick` for 30-second smoke test
- Optional: `--regression <baseline.json>` for comparison against a prior run

No clean working tree requirement (this skill never touches source code).

## Methodology

### Setup

Parse the user's request for: target URL, mode (full/quick/regression), output directory, scope, auth.

Auto-detect the browser binary. If on a feature branch with no URL, auto-enter diff-aware mode.

**Test Plan Context:** Before falling back to git diff heuristics, check for richer test plan sources:
1. Check `~/.gstack/projects/{slug}/` for recent `*-test-plan-*.md` files for this repo
2. Check if a prior plan-eng-review or plan-ceo-review produced test plan output in this conversation
3. Use whichever source is richer. Fall back to git diff analysis only if neither is available.

Create output directories: `.gstack/qa-reports/screenshots/`.

### Diff-Aware Mode (automatic on feature branch with no URL)

1. Run `git diff main...HEAD --name-only` and `git log main..HEAD --oneline`
2. Map changed files to affected pages/routes: controllers → URL paths, views/components → pages they render, models/services → pages that use them, CSS → pages that include it, API endpoints → direct browser fetch tests
3. Auto-detect running app on common ports (3000, 4000, 8080). If not found, check for staging/preview URL. If nothing, ask the user.
4. Test each affected page: navigate, screenshot, check console, test interactions end-to-end for interactive changes
5. Cross-reference with commit messages and PR description to verify the change does what it claims
6. Check `TODOS.md` for known bugs related to changed files. Note new bugs not in TODOS.md.

**If no pages are identifiable from the diff:** Still open the browser. Backend/config/infrastructure changes affect app behavior. Fall back to Quick mode — homepage + top 5 navigation targets + console check.

### Full (default when URL is provided)
Systematic exploration. Visit every reachable page. Document 5-10 well-evidenced issues. Produce health score. Takes 5-15 minutes depending on app size.

### Quick (`--quick`)
30-second smoke test. Visit homepage + top 5 navigation targets. Check: page loads? Console errors? Broken links? Produce health score. No detailed issue documentation.

### Regression (`--regression <baseline>`)
Run full mode, then load `baseline.json` from a previous run. Diff: which issues are fixed? Which are new? What's the score delta? Append regression section to report.

### Phase 1: Initialize

Find browse binary. Start timer. Create output directories. Copy report template from `qa/templates/qa-report-template.md` to the output directory.

### Phase 2: Authenticate (if needed)

Navigate to login URL, fill form, submit, verify login succeeded. Write `[REDACTED]` for any passwords in repro steps. Import cookie file if provided. Pause for 2FA/OTP or CAPTCHA as needed.

### Phase 3: Orient

Navigate to target URL. Take annotated screenshot. Get link list to map navigation structure. Check console for errors on landing.

Detect framework: `__next` or `_next/data` → Next.js, `csrf-token` meta → Rails, `wp-content` → WordPress, client-side routing → SPA. For SPAs, use interactive element discovery instead of link listing.

### Phase 4: Explore

Visit pages systematically. For each page:
1. Navigate and take an annotated screenshot
2. Check console for errors
3. Per-page checklist:
   - Visual scan: layout issues?
   - Interactive elements: click buttons, links, controls — do they respond?
   - Forms: fill and submit, test empty/invalid/edge cases
   - Navigation: check all paths in and out
   - States: empty state, loading, error, overflow
   - Console: new JS errors after interactions?
   - Responsiveness: check mobile viewport (375x812) if relevant
4. Spend more time on core features (dashboard, checkout, search), less on secondary pages

**Framework-specific checks:**
- **Next.js:** Hydration errors, `_next/data` 404s, CLS on dynamic content, client-side navigation (click links, don't just navigate directly)
- **Rails:** N+1 query warnings, CSRF token presence, Turbo/Stimulus transitions, flash messages
- **WordPress:** Plugin conflicts, admin bar visibility, `/wp-json/` endpoints, mixed content warnings
- **SPAs:** Stale state after navigation, browser back/forward history, memory leaks after extended use

**Quick mode:** Only visit homepage + top 5 navigation targets. Check: loads? Console errors? Broken links visible? No detailed per-page checklist.

### Phase 5: Document

Document each issue immediately when found — do not batch.

**Interactive bugs** (broken flows, dead buttons, form failures):
- Screenshot before the action
- Perform the action
- Screenshot showing the result
- Diff to show what changed
- Write repro steps referencing screenshots

**Static bugs** (typos, layout issues, missing images):
- Single annotated screenshot showing the problem
- Description of what's wrong

Write each issue to the report as you find it.

### Phase 6: Wrap Up

Compute the health score. Write "Top 3 Things to Fix." Summarize console errors across all pages. Fill in report metadata.

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

Final score: weighted average of all categories.

Save `baseline.json` for regression comparisons:
```json
{
  "date": "YYYY-MM-DD",
  "url": "<target>",
  "healthScore": N,
  "issues": [{"id": "ISSUE-001", "title": "...", "severity": "...", "category": "..."}],
  "categoryScores": {"console": N, "links": N, ...}
}
```

**Regression mode:** Load the baseline file. Compare health score delta, issues fixed (in baseline but not current), new issues (in current but not baseline). Append regression section to report.

## Quality Gates

**Non-negotiable rules:**
1. Repro is everything. Every issue needs at least one screenshot. No exceptions.
2. Verify before documenting. Retry the issue once to confirm reproducibility.
3. Never include credentials. Write `[REDACTED]` for passwords.
4. Write incrementally. Append each issue to the report as you find it.
5. Never read source code. Test as a user, not a developer.
6. Check console after every interaction. JS errors that don't surface visually are still bugs.
7. Test like a user. Use realistic data. Walk through complete workflows.
8. Depth over breadth. 5-10 well-documented issues > 20 vague descriptions.
9. Never delete output files. Screenshots and reports accumulate — that's intentional.
10. Use `snapshot -C` for tricky UIs. Finds clickable divs that the accessibility tree misses.
11. Display screenshots inline for the user. After every screenshot command, read the output file so the user can see it. For responsive screenshots (3 files), read all three. Without this, screenshots are invisible.
12. Never refuse to use the browser. `/qa-only` means browser-based testing. No substitutes.
13. **Never fix bugs.** Find and document only. Do not read source code, edit files, or suggest fixes in the report.

**Done when:**
- Health score computed
- All discovered issues documented with screenshot evidence
- Report written with "Top 3 Things to Fix" section
- `baseline.json` saved

If the project has no test framework, include a note in the report summary: "No test framework detected. Run `/qa` to bootstrap one and enable regression test generation."

## Outputs

```
.gstack/qa-reports/
├── qa-report-{domain}-{YYYY-MM-DD}.md    # Structured report
├── screenshots/
│   ├── initial.png                        # Landing page annotated
│   ├── issue-001-step-1.png               # Per-issue evidence
│   ├── issue-001-result.png
│   └── ...
└── baseline.json                          # For regression mode
```

Also writes `~/.gstack/projects/{slug}/{user}-{branch}-test-outcome-{datetime}.md` for cross-session context.

Report filename format: `qa-report-myapp-com-2026-03-12.md`

## Feeds Into

- `>qa` — when the user is ready to fix the bugs found in this report
- `>design-review` — functional bugs documented, visual polish next
- `>cso` — functional QA done, security audit next

## Harness Notes

**Browser automation is a hard dependency.** This skill requires the `browse` daemon for navigation, screenshots, and interaction testing. The browser binary needs a one-time build before first use.

**CDP mode:** If the browser is connected to the user's real browser session, skip cookie import and headless detection workarounds — real auth sessions are already available.

See `harness-compat.md: "Browse daemon setup"` and `"CDP vs headless mode"`.
