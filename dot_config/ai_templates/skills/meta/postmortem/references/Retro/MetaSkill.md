---
name: Retro
description: Engineering retrospective analyzing git history, commit patterns, work sessions, hotspots, and team contributions with trend tracking. USE WHEN retro, retrospective, weekly review, what did we ship, engineering retro, sprint review, commit analysis, team velocity, shipping streak.
---

# Retro

Generate a comprehensive engineering retrospective analyzing commit history, work patterns, and code quality metrics. Team-aware: identifies the current user, then analyzes every contributor with per-person praise and growth areas.

## Arguments

- `retro` -- last 7 days (default)
- `retro 24h` -- last 24 hours
- `retro 14d` -- last 14 days
- `retro 30d` -- last 30 days
- `retro compare` -- compare current window vs prior same-length window

## Execution

### Step 1: Gather Raw Data

Identify the current user and fetch origin:

```bash
git config user.name
git config user.email
git fetch origin <default-branch> --quiet
```

Run these git commands in parallel:

1. All commits in window: `git log origin/<default> --since="<window>" --format="%H|%aN|%ae|%ai|%s" --shortstat`
2. Per-commit file stats: `git log origin/<default> --since="<window>" --format="COMMIT:%H|%aN" --numstat`
3. Commit timestamps for session detection: `git log origin/<default> --since="<window>" --format="%at|%aN|%ai|%s" | sort -n`
4. File hotspots: `git log origin/<default> --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn`
5. Per-author file hotspots: `git log origin/<default> --since="<window>" --format="AUTHOR:%aN" --name-only`
6. Per-author commit counts: `git shortlog origin/<default> --since="<window>" -sn --no-merges`

### Step 2: Compute Metrics

| Metric | Value |
|--------|-------|
| Commits to default | N |
| Contributors | N |
| Total insertions | N |
| Total deletions | N |
| Net LOC added | N |
| Test LOC ratio | N% |
| Active days | N |
| Detected sessions | N |
| Avg LOC/session-hour | N |

Show a **per-author leaderboard** sorted by commits descending.

### Step 3: Session Detection

Detect sessions using a 45-minute gap threshold between consecutive commits. Classify:

- **Deep sessions** (50+ min) -- sustained focus
- **Medium sessions** (20-50 min) -- normal work
- **Micro sessions** (<20 min) -- fire-and-forget commits

### Step 4: Commit Type Breakdown

Categorize by conventional commit prefix (feat/fix/refactor/test/chore/docs). Show as percentages. Flag if fix ratio exceeds 50% -- signals "ship fast, fix fast" pattern.

### Step 5: Hotspot Analysis

Top 10 most-changed files. Flag:
- Files changed 5+ times (churn hotspots)
- Test files vs production files in hotspot list

### Step 6: Focus Score and Ship of the Week

**Focus score:** percentage of commits touching the single most-changed top-level directory. Higher = deeper focused work.

**Ship of the week:** the single highest-LOC change in the window. Highlight what it was, why it matters.

### Step 7: Team Member Analysis

For each contributor, compute:
1. Commits and LOC
2. Areas of focus (top 3 directories)
3. Commit type mix (their personal breakdown)
4. Session patterns (peak hours, session count)
5. Test discipline (their test LOC ratio)
6. Biggest ship

For teammates: write 2-3 sentences covering their work, then:
- **Praise** (1-2 specific things anchored in commits)
- **Opportunity for growth** (1 constructive suggestion framed as investment)

For the current user: deepest treatment with personal session analysis.

### Step 8: Streak Tracking

```bash
# Team streak
git log origin/<default> --format="%ad" --date=format:"%Y-%m-%d" | sort -u

# Personal streak
git log origin/<default> --author="<user>" --format="%ad" --date=format:"%Y-%m-%d" | sort -u
```

Count consecutive days with commits going backward from today.

### Step 9: Save and Compare

Save a JSON snapshot to `.context/retros/` for trend tracking. If prior retros exist, load the most recent one and compute deltas for key metrics.

### Step 10: Write Narrative

Read `references/narrative-template.md` for the output structure. Produce:

1. **Tweetable summary** (first line)
2. **Summary table** (from Step 2)
3. **Trends vs Last Retro** (if prior exists)
4. **Time and Session Patterns** (from Steps 3)
5. **Shipping Velocity** (from Step 4)
6. **Code Quality Signals** (test ratio, hotspots)
7. **Focus and Highlights** (from Step 6)
8. **Your Week** (personal deep-dive)
9. **Team Breakdown** (if multiple contributors)
10. **Top 3 Wins** and **3 Things to Improve**
11. **3 Habits for Next Week** (small, practical, <5 min each)
