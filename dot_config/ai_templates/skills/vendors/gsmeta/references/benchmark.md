# Benchmark

> Performance regression detection: establishes baselines for page load times, Core Web Vitals, and resource sizes, then compares before/after on every branch and tracks performance trends over time.

## When to Use

- User says "performance", "benchmark", "page speed", "lighthouse", "web vitals", "bundle size", or "load time"
- Before making changes that could affect performance (capture baseline first)
- After shipping a PR — compare against the baseline to detect regressions
- When investigating why the app feels slow
- On a schedule to track performance trends across PRs

**Core insight:** Performance doesn't degrade in one big regression. It dies by a thousand paper cuts. Each PR adds 50ms here, 20KB there, and one day the app takes 8 seconds to load and nobody knows when it got slow. Measure every change.

## Inputs

- Running web application URL (required)
- Optional: `--baseline` to capture a new baseline (run before making changes)
- Optional: `--quick` for single-pass timing check without baseline comparison
- Optional: `--pages /,/dashboard,/api/health` to specify which pages to measure
- Optional: `--diff` to auto-detect pages affected by current branch
- Optional: `--trend` to show historical trends from saved benchmarks

## Methodology

### Phase 1: Setup

Create output directories:
```
.gstack/benchmark-reports/
.gstack/benchmark-reports/baselines/
```

Determine pages to benchmark:
- If `--pages` specified: use those paths
- If `--diff` mode: run `git diff <base-branch>...HEAD --name-only` and map changed files to affected routes
- Otherwise: auto-discover from site navigation

### Phase 2: Page Discovery

Auto-discover navigable pages from the site's navigation structure, or use the `--pages` list. For `--diff` mode, detect the base branch the same way `>qa` does (via `gh pr view` or `gh repo view` fallback to `main`).

### Phase 3: Performance Data Collection

For each page, navigate to the URL and collect comprehensive performance metrics.

**Core timing metrics** (via Navigation Timing API):
- **TTFB** (Time to First Byte): `responseStart - requestStart`
- **FCP** (First Contentful Paint): from paint entries
- **LCP** (Largest Contentful Paint): from PerformanceObserver
- **DOM Interactive**: `domInteractive - navigationStart`
- **DOM Complete**: `domComplete - navigationStart`
- **Full Load**: `loadEventEnd - navigationStart`

Collect via JavaScript evaluation:
```js
JSON.stringify(performance.getEntriesByType('navigation')[0])
```

**Resource analysis** (via Resource Timing API):

Top 15 slowest resources by duration:
```js
JSON.stringify(performance.getEntriesByType('resource').map(r => ({name: r.name.split('/').pop().split('?')[0], type: r.initiatorType, size: r.transferSize, duration: Math.round(r.duration)})).sort((a,b) => b.duration - a.duration).slice(0,15))
```

JS bundle sizes:
```js
JSON.stringify(performance.getEntriesByType('resource').filter(r => r.initiatorType === 'script').map(r => ({name: r.name.split('/').pop().split('?')[0], size: r.transferSize})))
```

CSS bundle sizes:
```js
JSON.stringify(performance.getEntriesByType('resource').filter(r => r.initiatorType === 'css').map(r => ({name: r.name.split('/').pop().split('?')[0], size: r.transferSize})))
```

Network summary:
```js
JSON.stringify((() => { const r = performance.getEntriesByType('resource'); return {total_requests: r.length, total_transfer: r.reduce((s,e) => s + (e.transferSize||0), 0), by_type: Object.entries(r.reduce((a,e) => { a[e.initiatorType] = (a[e.initiatorType]||0) + 1; return a; }, {})).sort((a,b) => b[1]-a[1])}})())
```

### Phase 4: Baseline Capture (`--baseline` mode)

Save metrics to `.gstack/benchmark-reports/baselines/baseline.json`:

```json
{
  "url": "<url>",
  "timestamp": "<ISO datetime>",
  "branch": "<branch name>",
  "pages": {
    "/": {
      "ttfb_ms": 120,
      "fcp_ms": 450,
      "lcp_ms": 800,
      "dom_interactive_ms": 600,
      "dom_complete_ms": 1200,
      "full_load_ms": 1400,
      "total_requests": 42,
      "total_transfer_bytes": 1250000,
      "js_bundle_bytes": 450000,
      "css_bundle_bytes": 85000,
      "largest_resources": [
        {"name": "main.js", "size": 320000, "duration": 180},
        {"name": "vendor.js", "size": 130000, "duration": 90}
      ]
    }
  }
}
```

### Phase 5: Comparison

If a baseline exists, compare current metrics against it and output a structured table per page:

```
PERFORMANCE REPORT — [url]
══════════════════════════
Branch: [current] vs baseline ([baseline-branch])

Page: /
Metric              Baseline    Current     Delta    Status
TTFB                120ms       135ms       +15ms    OK
FCP                 450ms       480ms       +30ms    OK
LCP                 800ms       1600ms      +800ms   REGRESSION
DOM Interactive     600ms       650ms       +50ms    OK
Full Load           1400ms      2100ms      +700ms   REGRESSION
JS Bundle           450KB       720KB       +270KB   REGRESSION

REGRESSIONS DETECTED: 3
  [1] LCP doubled — likely a large new image or blocking resource
  [2] Full Load +50% — check new JS bundles
  [3] JS bundle +60% — new dependency or missing tree-shaking
```

**Regression thresholds:**
- Timing: >50% increase OR >500ms absolute increase = **REGRESSION**
- Timing: >20% increase = **WARNING**
- Bundle size: >25% increase = **REGRESSION**
- Bundle size: >10% increase = **WARNING**
- Request count: >30% increase = **WARNING**

### Phase 6: Slowest Resources

```
TOP 10 SLOWEST RESOURCES
═════════════════════════
#   Resource                  Type      Size      Duration
1   vendor.chunk.js          script    320KB     480ms
2   main.js                  script    250KB     320ms
3   hero-image.webp          img       180KB     280ms
4   analytics.js             script    45KB      250ms    ← third-party
5   fonts/inter-var.woff2    font      95KB      180ms
...

RECOMMENDATIONS:
- vendor.chunk.js: Consider code-splitting — 320KB is large for initial load
- analytics.js: Load async/defer — blocks rendering for 250ms
- hero-image.webp: Add width/height to prevent CLS, consider lazy loading
```

Flag third-party scripts with `← third-party` annotation (can't be fixed by the developer, but worth knowing). Include actionable recommendations per resource:
- Large JS chunks → consider code-splitting
- Third-party analytics → load async/defer, blocks rendering
- Images without dimensions → add width/height to prevent CLS, consider lazy loading

### Phase 7: Performance Budget Check

Compare against industry budgets:

| Metric | Budget |
|--------|--------|
| FCP | < 1.8s |
| LCP | < 2.5s |
| Total JS | < 500KB |
| Total CSS | < 100KB |
| Total Transfer | < 2MB |
| HTTP Requests | < 50 |

Output PASS/FAIL/WARNING per metric with actual values. Give an overall grade based on passing count:

| Passing | Grade |
|---------|-------|
| 6/6 | A |
| 5/6 | A |
| 4/6 | B |
| 3/6 | C |
| 2/6 | D |
| 0-1/6 | F |

Example: `Grade: B (4/6 passing)`

### Phase 8: Trend Analysis (`--trend` mode)

Load all historical baseline files from `.gstack/benchmark-reports/baselines/`. Show a table of the last 5 benchmarks:

```
PERFORMANCE TRENDS (last 5 benchmarks)
═══════════════════════════════════════
Date        FCP     LCP     Bundle    Requests    Grade
2026-03-10  420ms   750ms   380KB     38          A
2026-03-18  480ms   1600ms  720KB     58          B

TREND: Performance degrading. LCP doubled in 8 days. JS bundle growing 50KB/week.
```

Identify the direction: improving, stable, or degrading. Flag the rate of change for bundle size specifically.

### Phase 9: Save Report

Write to:
- `.gstack/benchmark-reports/{date}-benchmark.md` — human-readable report
- `.gstack/benchmark-reports/{date}-benchmark.json` — structured data for future trend analysis

## Quality Gates

- **Measure, don't guess.** Use actual `performance.getEntries()` data, not estimates.
- **Baseline is essential.** Without a baseline, you can report absolute numbers but cannot detect regressions. Always encourage capturing a baseline before making changes.
- **Relative thresholds, not absolute.** 2000ms load is fine for a complex dashboard, terrible for a landing page. Compare against YOUR baseline.
- **Third-party scripts are context.** Flag them, but focus recommendations on first-party resources.
- **Bundle size is the leading indicator.** Load time varies with network. Bundle size is deterministic. Track it religiously.
- **Read-only.** Produce the report. Do not modify code unless explicitly asked.

**Done when:**
- All pages measured and metrics collected
- Comparison against baseline (if available) with clear PASS/WARNING/REGRESSION per metric
- Slowest resources identified with actionable recommendations
- Performance budget check complete
- Report saved (markdown + JSON)

## Outputs

```
.gstack/benchmark-reports/
├── {date}-benchmark.md       # Human-readable report
├── {date}-benchmark.json     # Structured data for trend tracking
└── baselines/
    └── baseline.json         # Latest baseline snapshot
```

## Feeds Into

- `>qa` — performance data collected, run functional QA next
- `>ship` — benchmark before shipping to confirm no regressions
- `>cso` — performance issues sometimes reveal security issues (e.g., unbounded LLM calls)

## Harness Notes

**Browser automation is a hard dependency.** This skill requires the `browse` daemon (`$B`) for navigation and JavaScript evaluation (`$B eval`). The `perf` command provides high-level timing; `$B eval` with the Performance API gives the detailed resource breakdown.

All metric collection happens via JavaScript execution in the page context — no external services, no network requests beyond the app itself.

See `harness-compat.md: "Browse daemon setup"` and `"JavaScript evaluation patterns"`.
