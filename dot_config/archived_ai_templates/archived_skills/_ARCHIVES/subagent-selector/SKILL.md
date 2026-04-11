---
name: subagent-selector
description: Show available subagents for task delegation in opencode CLI. Use when orchestrating tasks, selecting agents, planning delegations, or unsure which agent to use.
---

# Available Subagents

## Checklist

1. Verify running in opencode CLI and HOME user is `andy16` (run `if [[ "$(id -un)" == "andy16" ]]; then echo "true"; else echo "false"; fi`); otherwise ignore this skill and use default agent selection.
2. Choose the agent using the matrix below.
3. Apply the fallback when the primary agent is unavailable.
4. Use `@oracle` only after two failed attempts with `@abby` or `@build`.

## Agent Selection Matrix

| Task | Primary Agent(s) | Tier | Fallback |
|------|------------------|------|----------|
| Planning, orchestrating | `@build` | A-tier MAIN | `@abby` |
| Coding, architecture, multi-file refactoring, bugs | `@abby` | A-tier MAIN | `@build` |
| Code review | `@abby` + `@build` (parallel)<br>launch `@abby` and `@build` in parallel | A-tier MAIN | `@build` |
| Security review | `@abby` | A-tier MAIN | `@build` |
| Frontend/UI design, visual layout | `@build` | A-tier MAIN | `@abby` |
| Documentation/spec/changelog writing | `@abby` | A-tier MAIN | `@build` |
| Performance profiling, benchmark validation | `@abby` | A-tier MAIN | `@build` |
| Deep codebase exploration, repo mapping | `@explore` | B-tier MAIN | `@ben` |
| Codebase exploration, doc search, quick edits, deep-research Q&A | `@ben` | B-tier MAIN | `@general` |
| Tests, QA, validation, visual checks | `@charlie` | C-tier MAIN | `@carole` |
| After 2 failed attempts (from @abby or @build) | `@oracle` | A-tier ESCALATE | `@build` |
| Everything else | `@general` | B-tier FALLBACK | `@build` |
