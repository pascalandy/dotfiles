# Retro

> Weekly engineering retrospective: analyzes commit history, work patterns, and code quality metrics with persistent history and trend tracking. Team-aware: breaks down per-person contributions with specific praise and growth opportunities.

## When to Use

- User says "weekly retro", "what did we ship", "engineering retrospective"
- End of a work week or sprint
- Proactively suggest on Fridays or after a sprint boundary

## Arguments

- `/retro` -- default: last 7 days
- `/retro 24h` -- last 24 hours
- `/retro 14d` -- last 14 days
- `/retro 30d` -- last 30 days
- `/retro compare` -- compare current window vs prior same-length window
- `/retro compare 14d` -- compare with explicit window
- `/retro global` -- cross-project retro across all AI coding tools (7d default)
- `/retro global 14d` -- cross-project retro with explicit window

## Inputs

- A git repo on the current branch (required for standard retro, not required for `global` mode)
- Time window: default 7 days. Accepts `24h`, `14d`, `30d`, `2w`, etc.
- Optional: `compare` for week-over-week trend analysis
- Optional: `global` for cross-project retro across all repos/AI tools on the machine

## Methodology

### Setup

Parse the time window argument. **Midnight-aligned windows:** for day (`d`) and week (`w`) units, compute an absolute start date at local midnight -- use `--since="<date>T00:00:00"` in all git log commands. The explicit `T00:00:00` suffix is required: without it, git uses the current wall-clock time (e.g., `--since="2026-03-11"` at 11pm means 11pm, not midnight). For hour (`h`) units, use `--since="N hours ago"` since midnight alignment doesn't apply to sub-day windows. For week units, multiply by 7 to get days.

**Argument validation:** if the argument doesn't match a number followed by `d`, `h`, or `w`, the word `compare` (optionally followed by a window), or `global` (optionally followed by a window), show usage and stop.

If the first argument is `global`: skip Steps 1-14 and follow the **Global Retrospective** flow. Global mode does NOT require being inside a git repo.

Identify the current user from `git config user.name` -- that person is "you" in all narrative. All other authors are teammates.

Fetch origin before running git log commands.

### Step 1: Gather raw data (run all in parallel)

1. All commits in window: `git log origin/<default> --since="<window>" --format="%H|%aN|%ae|%ai|%s" --shortstat`
2. Per-commit numstat breakdown with author (separate test files matching `test/|spec/|__tests__/` from production files): `git log origin/<default> --since="<window>" --format="COMMIT:%H|%aN" --numstat`
3. Commit timestamps for session detection and hourly distribution: `git log origin/<default> --since="<window>" --format="%at|%aN|%ai|%s" | sort -n`
4. Files most frequently changed (hotspot analysis): `git log origin/<default> --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn`
5. PR/MR numbers from commit messages (GitHub #NNN, GitLab !NNN)
6. Per-author file hotspots: `git log origin/<default> --since="<window>" --format="AUTHOR:%aN" --name-only`
7. Per-author commit counts: `git shortlog origin/<default> --since="<window>" -sn --no-merges`
8. Greptile triage history: `cat ~/.gstack/greptile-history.md 2>/dev/null || true`
9. TODOS.md backlog: `cat TODOS.md 2>/dev/null || true`
10. Test file count: `find . -name '*.test.*' -o -name '*.spec.*' -o -name '*_test.*' -o -name '*_spec.*' 2>/dev/null | grep -v node_modules | wc -l`
11. Regression test commits: `git log origin/<default> --since="<window>" --oneline --grep="test(qa):" --grep="test(design):" --grep="test: coverage"`
12. gstack skill usage telemetry: `cat ~/.gstack/analytics/skill-usage.jsonl 2>/dev/null || true`
13. Test files changed in window: `git log origin/<default> --since="<window>" --format="" --name-only | grep -E '\.(test|spec)\.' | sort -u | wc -l`

### Step 2: Compute metrics

Present a summary table:

| Metric | Value |
|--------|-------|
| Commits to main | N |
| Contributors | N |
| PRs merged | N |
| Total insertions | N |
| Total deletions | N |
| Net LOC added | N |
| Test LOC (insertions) | N |
| Test LOC ratio | N% |
| Version range | vX.Y.Z.W → vX.Y.Z.W |
| Active days | N |
| Detected sessions | N |
| Avg LOC/session-hour | N |
| Greptile signal | N% (Y catches, Z FPs) |
| Test Health | N total tests, M added, K regression commits |
| Backlog Health | N open (X P0/P1, Y P2), Z completed |
| Skill Usage | /ship(12) /qa(8) /review(5) -- 3 safety hook fires |
| Eureka Moments | N this period |

Show **per-author leaderboard** sorted by commits descending. Current user always appears first as "You (name)":
```
Contributor         Commits   +/-          Top area
You (garry)              32   +2400/-300   browse/
alice                    12   +800/-150    app/services/
bob                       3   +120/-40     tests/
```

**Greptile signal:** if `~/.gstack/greptile-history.md` has entries in the window, compute `(fix + already-fixed) / (fix + already-fixed + fp)`. Skip row if no entries.

**Backlog health:** from TODOS.md -- total open (excluding Completed section), P0/P1 count, P2 count, completed this period (items with dates in window), added this period (cross-reference git log for TODOS.md commits). Skip row if TODOS.md doesn't exist.

**Skill usage:** from `~/.gstack/analytics/skill-usage.jsonl` -- filter by `ts` field in window, separate skill activations from hook fires (`event: "hook_fire"`), aggregate by skill name. Skip row if file doesn't exist or no entries in window.

**Eureka moments:** from `~/.gstack/analytics/eureka.jsonl` -- filter by `ts` field in window. List skill, branch, and insight for each:
```
  EUREKA /plan-eng-review (branch: garrytan/cache-layer): "Redis isn't needed here -- Bun's built-in LRU cache handles this workload"
```
Skip row if file doesn't exist or no entries in window.

### Step 3: Commit time distribution

Show hourly histogram in local time (bar chart, do NOT override `TZ`). Call out peak hours, dead zones, bimodal patterns (morning/evening), late-night clusters (after 10pm).

### Step 4: Work session detection

Detect sessions using a **45-minute gap** threshold between consecutive commits.

Classify:
- **Deep sessions:** 50+ minutes
- **Medium sessions:** 20-50 minutes
- **Micro sessions:** <20 minutes (single-commit fire-and-forget)

Calculate: total active coding time (sum of session durations), average session length, LOC per active hour.

### Step 5: Commit type breakdown

Categorize by conventional commit prefix (feat/fix/refactor/test/chore/docs). Show as percentage bar:
```
feat:     20  (40%)  ████████████████████
fix:      27  (54%)  ███████████████████████████
refactor:  2  ( 4%)  ██
```

Flag if fix ratio exceeds 50% -- signals "ship fast, fix fast" pattern that may indicate review gaps.

### Step 6: Hotspot analysis

Top 10 most-changed files. Flag:
- Files changed 5+ times (churn hotspots)
- Test vs production files in the list
- VERSION/CHANGELOG frequency (version discipline indicator)

### Step 7: PR size distribution

Bucket PRs by LOC: Small (<100), Medium (100-500), Large (500-1500), XL (1500+).

### Step 8: Focus score and ship of the week

**Focus score:** percentage of commits touching the single most-changed top-level directory (e.g., `app/services/`). Higher = deeper focused work. Lower = scattered context-switching. Report as: "Focus score: 62% (app/services/)"

**Ship of the week:** highest-LOC PR in the window -- PR number/title, LOC changed, why it matters (inferred from commit messages and files touched).

### Step 9: Team member analysis

For each contributor (including the current user):
1. Commits and LOC (total commits, insertions, deletions, net)
2. Areas of focus (top 3 directories/files)
3. Commit type mix (personal feat/fix/refactor/test breakdown)
4. Session patterns (peak hours, session count)
5. Test discipline (personal test LOC ratio)
6. Biggest ship (highest-impact commit or PR in the window)

**For the current user ("You"):** deepest treatment. Full session analysis, time patterns, focus score. Frame in first person. This is the section the user cares most about. Include:
- Personal commit count, LOC, test ratio
- Session patterns and peak hours
- Focus areas and biggest ship
- **What you did well** (2-3 specific things anchored in commits)
- **Where to level up** (1-2 specific, actionable suggestions)

**For each teammate:** 2-3 sentences on what they worked on and their pattern. Then:
- **Praise (1-2 specific things):** anchor in actual commits. Not "great work" -- say exactly what was good. Example: "Shipped the entire auth middleware rewrite in 3 focused sessions with 45% test coverage."
- **Opportunity for growth (1 specific thing):** frame as leveling-up, not criticism. Anchor in actual data. Example: "Test ratio was 12% this week -- adding test coverage to the payment module before it gets more complex would pay off."

If only one contributor: skip team breakdown.

**AI co-authored commits:** parse `Co-Authored-By:` trailers. Credit human co-authors alongside primary author. Track AI co-authors (noreply@anthropic.com, etc.) as "AI-assisted commits" metric, not as team members.

### Step 10: Week-over-week trends (if window >= 14d)

Split into weekly buckets and show: commits per week (total and per-author), LOC per week, test ratio per week, fix ratio per week, session count per week.

### Step 11: Streak tracking

Count consecutive days with at least 1 commit to `origin/<default>`, going back from today using the **full git history** (no cutoff -- queries must not cap at the retro window). Track both team streak and personal streak (filter by current user's commits). Display:
- "Team shipping streak: 47 consecutive days"
- "Your shipping streak: 32 consecutive days"

### Step 12: Load history and compare

Check `.context/retros/*.json` for prior retro snapshots. If found, load the most recent and calculate deltas:

```
                    Last        Now         Delta
Test ratio:         22%    →    41%         +19pp
Sessions:           10     →    14          +4
LOC/hour:           200    →    350         +75%
Fix ratio:          54%    →    30%         -24pp (improving)
Commits:            32     →    47          +47%
Deep sessions:      3      →    5           +2
```

If no prior retros: "First retro recorded -- run again next week to see trends."

### Step 13: Save retro history

Create `.context/retros/`. Determine next sequence number for today: count existing `{date}-*.json` files.

Save JSON snapshot to `.context/retros/{date}-{N}.json`:
```json
{
  "date": "2026-03-08",
  "window": "7d",
  "metrics": {
    "commits": 47,
    "contributors": 3,
    "prs_merged": 12,
    "insertions": 3200,
    "deletions": 800,
    "net_loc": 2400,
    "test_loc": 1300,
    "test_ratio": 0.41,
    "active_days": 6,
    "sessions": 14,
    "deep_sessions": 5,
    "avg_session_minutes": 42,
    "loc_per_session_hour": 350,
    "feat_pct": 0.40,
    "fix_pct": 0.30,
    "peak_hour": 22,
    "ai_assisted_commits": 32
  },
  "authors": {
    "Garry Tan": { "commits": 32, "insertions": 2400, "deletions": 300, "test_ratio": 0.41, "top_area": "browse/" }
  },
  "version_range": ["1.16.0.0", "1.16.1.0"],
  "streak_days": 47,
  "tweetable": "Week of Mar 1: 47 commits (3 contributors), 3.2k LOC, 38% tests, 12 PRs, peak: 10pm"
}
```

Include optional fields only when data exists:
- `greptile`: only if greptile-history.md has in-window entries
- `backlog`: only if TODOS.md exists
- `test_health`: only if test files found (`total_test_files`, `tests_added_this_period`, `regression_test_commits`, `test_files_changed`)

### Capture Learnings

If a non-obvious pattern, pitfall, or architectural insight was discovered, log it:

Log schema: `{"skill":"retro","type":"TYPE","key":"SHORT_KEY","insight":"DESCRIPTION","confidence":N,"source":"SOURCE","files":["path/to/relevant/file"]}`

**Types:** `pattern` (reusable approach), `pitfall` (what NOT to do), `preference` (user stated), `architecture` (structural decision), `tool` (library/framework insight).

**Sources:** `observed` (found in code), `user-stated` (user told you), `inferred` (AI deduction), `cross-model` (both Claude and Codex agree).

**Confidence:** 1-10. Observed pattern verified in code = 8-9. Inference uncertain = 4-5. Explicit user preference = 10.

**files:** include specific file paths this learning references -- enables staleness detection if files are later deleted.

Only log genuine discoveries. A good test: would this insight save time in a future session?

### Step 14: Write the narrative

Structure:

1. **Tweetable summary** (first line, before everything else): `Week of Mar 1: 47 commits (3 contributors), 3.2k LOC, 38% tests, 12 PRs, peak: 10pm | Streak: 47d`
2. **Summary table** (Step 2)
3. **Trends vs Last Retro** (Step 12, skip if first retro)
4. **Time and Session Patterns** (Steps 3-4): when the most productive hours are, session length trends, estimated active hours per day, team coordination patterns (code at same time or in shifts?)
5. **Shipping Velocity** (Steps 5-7): commit type mix interpretation, PR size distribution, fix-chain detection (sequences of fix commits on same subsystem), version bump discipline
6. **Code Quality Signals:** test LOC ratio trend, hotspot analysis, Greptile signal ratio and trend
7. **Test Health:** total test files, tests added this period, regression test commits (list `test(qa):`, `test(design):`, `test: coverage` commits), delta from last retro. If test ratio < 20%: flag as growth area -- "100% test coverage is the goal. Tests make vibe coding safe."
8. **Plan Completion:** read review JSONL logs for plan completion data from /ship runs this period (`~/.gstack/projects/$SLUG/*-reviews.jsonl`). If data exists: count branches shipped with plans, average completion %, most-skipped item category. If no data: skip silently.
9. **Focus and Highlights** (Step 8): focus score with interpretation, ship of the week callout
10. **Your Week** (Step 9, personal deep-dive for current user)
11. **Team Breakdown** (Step 9, per teammate sorted by commits, skip if solo): for each teammate -- what they shipped, **Praise** (1-2 specific, earned, genuine -- what you'd actually say in a 1:1), **Opportunity for growth** (1 specific, constructive, framed as investment)
12. **Top 3 Team Wins:** highest-impact ships across the whole team -- what it was, who shipped it, why it matters
13. **3 Things to Improve:** specific, anchored in actual commits, mix personal and team-level, phrased as "to get even better..."
14. **3 Habits for Next Week:** small, practical, each <5 minutes to adopt, at least one team-oriented
15. **Week-over-Week Trends** (Step 10, if applicable)

**AI collaboration note:** if many commits have Co-Authored-By AI trailers, note the AI-assisted commit percentage as a team metric. Frame neutrally.

Never compare teammates against each other negatively. Each person's section stands on its own. Keep total output around 3000-4500 words.

### Compare Mode (/retro compare)

1. Compute metrics for the current window using midnight-aligned start date.
2. Compute metrics for the immediately prior same-length window using both `--since` and `--until` with midnight-aligned dates to avoid overlap.
3. Show side-by-side comparison table with deltas and arrows.
4. Write a brief narrative highlighting biggest improvements and regressions.
5. Save only the current-window snapshot to `.context/retros/` -- do NOT persist the prior-window metrics.

### Global Retrospective Mode (/retro global)

Runs without a git repo. Works from any directory.

**Global Step 1:** Compute time window (same midnight-aligned logic, default 7d).

**Global Step 2:** Run discovery script (`gstack-global-discover --since "<window>" --format json`). If no sessions found, say so and suggest a longer window.

**Global Step 3:** For each discovered repo, find a valid path with `.git/`. For local-only repos (remote starts with `local:`): skip git fetch, use `git log HEAD`. For remote repos: `git fetch origin --quiet`. Detect default branch for each repo. Run: commits with stats, commit timestamps, per-author counts, PR/MR numbers from commit messages.

**Global Step 4: Compute global shipping streak.** For each repo, get commit dates (capped at 365 days: `git log origin/$DEFAULT --since="365 days ago" --format="%ad" --date=format:"%Y-%m-%d"`). Union all dates across all repos. Count consecutive days from today with at least one commit to ANY repo. If streak hits 365 days, display as "365+ days".

**Global Step 5: Context switching metric.** From commit timestamps grouped by date: average repos/day, max repos/day, focused days (1 repo) vs fragmented days (3+ repos).

**Global Step 6: Per-tool productivity patterns.** From discovery JSON: which AI tool is used for which repos (exclusive vs shared), session count per tool, behavioral patterns.

**Global Step 7: Generate narrative.** Structure: **shareable personal card first**, then full team/project breakdown.

Personal card (screenshot-friendly, current user's stats only across all repos):
```
╔═══════════════════════════════════════════════════════════════
║  [USER NAME] -- Week of [date]
╠═══════════════════════════════════════════════════════════════
║
║  [N] commits across [M] projects
║  +[X]k LOC added · [Y]k LOC deleted · [Z]k net
║  [N] AI coding sessions (CC: X, Codex: Y, Gemini: Z)
║  [N]-day shipping streak 🔥
║
║  PROJECTS
║  ─────────────────────────────────────────────────────────
║  [repo_name_full]        [N] commits    +[X]k LOC    [solo/team]
║
║  SHIP OF THE WEEK
║  [PR title] -- [LOC] lines across [N] files
║
║  TOP WORK
║  • [1-line description of biggest theme]
║  • [1-line description of second theme]
║  • [1-line description of third theme]
║
║  Powered by gstack
╚═══════════════════════════════════════════════════════════════
```

Personal card rules:
- Show only repos where the user has commits. Skip repos with 0 commits.
- Sort repos by user's commit count descending.
- **Never truncate repo names.** Use the full repo name. Pad to the longest name so columns align. Widen the box if names are long -- box width adapts to content.
- Use "k" formatting for thousands (e.g., "+64.0k" not "+64010").
- Role: "solo" if user is the only contributor, "team" if others contributed.
- Ship of the Week: user's single highest-LOC PR across ALL repos.
- Top Work: 3 bullets synthesizing user's major themes from commit messages. Not individual commits -- synthesize into themes.
- Do NOT include team members, project totals, or context switching data in the card.
- The card must be self-contained. Someone seeing ONLY this block should understand the user's week.

Full analysis (below the card):

**All Projects Overview table:** projects active, total commits, total LOC, AI coding sessions, active days, global shipping streak, context switches/day.

**Per-Project Breakdown** (sorted by commits descending): repo name with % of total commits, commits, LOC, PRs merged, top contributor, key work, AI sessions by tool. Plus **Your Contributions** sub-section for each project:
```
**Your contributions:** 47/244 commits (19%), +4.2k/-0.3k LOC
  Key work: Writer Chat, email blocking, security hardening
  Biggest ship: PR #605 -- Writer Chat eats the admin bar (2,457 ins, 46 files)
  Mix: feat(3) fix(2) chore(1)
```

If user is the only contributor: "Solo project -- all commits are yours."
If user has 0 commits in a repo: "No commits this period -- [N] AI sessions only." Skip breakdown.

**Cross-Project Patterns:** time allocation across projects (% breakdown, use YOUR commits not total), peak productivity hours aggregated, focused vs fragmented days, context switching trends.

**Tool Usage Analysis:** per-tool breakdown with behavioral patterns.

**Ship of the Week (Global):** highest-impact PR across ALL projects (by LOC and commit messages).

**3 Cross-Project Insights:** what the global view reveals that no single-repo retro could show.

**3 Habits for Next Week:** considering the full cross-project picture.

**Global Step 8: Load history and compare.** Check `~/.gstack/retros/global-*.json`. **Only compare against a prior retro with the same `window` value.** If most recent prior retro has a different window, skip comparison with note. If matching prior exists, show Trends vs Last Global Retro table.

**Global Step 9: Save snapshot** to `~/.gstack/retros/global-{date}-{N}.json`. JSON schema includes: type, date, window, projects array (name, remote normalized to HTTPS, commits, insertions, deletions, sessions by tool), totals (commits, insertions, deletions, projects, active days, sessions by tool, global streak days, avg context switches/day), tweetable summary.

## Important Rules

- ALL narrative output goes directly to the user in the conversation. The ONLY file written is the `.context/retros/` JSON snapshot (or `~/.gstack/retros/` for global mode).
- Use `origin/<default>` for all git queries (not local main which may be stale).
- Display all timestamps in the user's local timezone (do not override `TZ`).
- If the window has zero commits, say so and suggest a different window.
- Round LOC/hour to nearest 50.
- Treat merge commits as PR boundaries.
- Do not read CLAUDE.md or other project docs -- this skill is self-contained.
- On first run (no prior retros), skip comparison sections gracefully.
- **Global mode:** does NOT require being inside a git repo. Saves snapshots to `~/.gstack/retros/`. Gracefully skip AI tools that aren't installed. Only compare against prior global retros with the same window value. If streak hits 365d cap, display as "365+ days".
- **Praise and growth:** must be anchored in actual commits, never generic. Praise should feel like something you'd actually say in a 1:1. Growth suggestions should feel like investment advice: "this is worth your time because..." not "you failed at..."

## Quality Gates

- **Time window precision:** always use midnight-aligned absolute dates, never relative strings for day/week windows
- **Attribution accuracy:** correctly identify current user as "you", distinguish from teammates
- **Praise and growth:** must be anchored in actual commits, never generic
- **Streak accuracy:** queries full git history (no cutoff) so streaks of any length are reported accurately
- **Tweetable summary:** first line, before everything, formatted for sharing

## Outputs

- Retro report printed to screen (full narrative, ~3000-4500 words)
- JSON snapshot saved to `.context/retros/{date}-{N}.json` (or `~/.gstack/retros/global-{date}-{N}.json` for global mode)
- Week-over-week comparison if prior history exists (same window size only for global mode)
- Learnings logged if non-obvious insights discovered

## Feeds Into

- >ship (retro surfacing quality trends informs what to fix before next ship)
- >canary (canary HEALTHY/DEGRADED/BROKEN verdicts and alert counts feed into retro code quality signals)
