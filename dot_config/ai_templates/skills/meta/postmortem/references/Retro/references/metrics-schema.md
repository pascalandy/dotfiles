# Retro Metrics Schema

```json
{
  "date": "YYYY-MM-DD",
  "window": "7d",
  "metrics": {
    "commits": 0,
    "contributors": 0,
    "insertions": 0,
    "deletions": 0,
    "net_loc": 0,
    "test_loc": 0,
    "test_ratio": 0.0,
    "active_days": 0,
    "sessions": 0,
    "deep_sessions": 0,
    "avg_session_minutes": 0,
    "loc_per_session_hour": 0,
    "feat_pct": 0.0,
    "fix_pct": 0.0,
    "peak_hour": 0
  },
  "authors": {
    "Name": {
      "commits": 0,
      "insertions": 0,
      "deletions": 0,
      "test_ratio": 0.0,
      "top_area": ""
    }
  },
  "streak_days": 0,
  "tweetable": ""
}
```

## Metric Definitions

| Metric | How to Compute |
|--------|---------------|
| commits | Count of non-merge commits in window |
| contributors | Unique author names |
| insertions/deletions | Sum of `--shortstat` lines |
| net_loc | insertions - deletions |
| test_loc | Sum of insertions in files matching `test/`, `spec/`, `__tests__/`, `*.test.*`, `*.spec.*` |
| test_ratio | test_loc / (test_loc + production_loc) |
| active_days | Unique dates with commits |
| sessions | Groups of commits with <45 min gaps |
| deep_sessions | Sessions >= 50 min |
| peak_hour | Hour (0-23) with most commits in local time |
| streak_days | Consecutive days with commits, counting back from today |

## Session Detection Algorithm

1. Sort commits by timestamp (ascending)
2. For each consecutive pair, compute time gap
3. If gap > 45 minutes, start a new session
4. Session duration = last commit time - first commit time (minimum 5 min)
