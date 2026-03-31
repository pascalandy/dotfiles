# Todo Resolve

> Batch-resolve approved todos using parallel processing, document lessons learned, then clean up.

## When to Use

- After a code review or triage session has produced a set of `ready` todos.
- After `ce:review mode:autofix` has applied safe fixes and emitted residual todos.
- When the user wants to clear a backlog of approved work items in one automated pass.
- As the final step of the `slfg` workflow (step 7).

## Inputs

- Todo files in `.context/compound-engineering/todos/` and/or legacy `todos/`.
- Optionally: a specific todo ID or pattern to filter which todos to resolve.

## Methodology

### Step 1 — Analyze

Scan `.context/compound-engineering/todos/*.md` and legacy `todos/*.md`. Partition by status:

| Status | Action |
|---|---|
| `ready` (status field or `-ready-` in filename) | Resolve these |
| `pending` | Skip — not yet triaged. Report at end. |
| `complete` | Ignore — already done. |

If a specific todo ID or pattern was passed as an argument, filter to matching todos only (they must still be `ready`).

Residual actionable work from `ce:review mode:autofix` after its `safe_auto` pass will already be `ready`.

**Skip any todo that recommends deleting, removing, or gitignoring files in `docs/brainstorms/`, `docs/plans/`, or `docs/solutions/`** — these are intentional pipeline artifacts.

### Step 2 — Plan

Create a task list grouped by type. Analyze dependencies — items that others depend on must run first. Output a Mermaid diagram showing execution order and parallelism.

### Step 3 — Implement (PARALLEL)

Spawn a `pr-comment-resolver` subagent per item. Prefer parallel execution; fall back to sequential respecting dependency order.

**Batching rules:**
- **1–4 items:** direct parallel execution, full return values.
- **5+ items:** batches of 4; each subagent returns only a short status summary (todo handled, files changed, tests run/skipped, blockers).

For large sets, use a scratch directory at `.context/compound-engineering/todo-resolve/<run-id>/` for per-resolver artifacts. Return only completion summaries to the parent agent.

### Step 4 — Commit & Resolve

Commit all changes, mark todos resolved (rename `ready` → `complete` in filename and frontmatter), push to remote.

**GATE: STOP.** Verify todos are resolved and changes are committed before proceeding.

### Step 5 — Compound on Lessons Learned

Load the `ce:compound` skill to document what was learned. Todo resolutions often surface patterns and architectural insights worth capturing.

**GATE: STOP.** Verify the compound skill produced a solution document in `docs/solutions/`. If none (user declined or no learnings), continue.

### Step 6 — Clean Up

Delete completed/resolved todo files from both paths. If a scratch directory was created at `.context/compound-engineering/todo-resolve/<run-id>/`, delete it (unless the user asked to inspect it).

Present final summary:

```
Todos resolved: [count]
Pending (skipped): [count, or "none"]
Lessons documented: [path to solution doc, or "skipped"]
Todos cleaned up: [count deleted]
```

If pending todos were skipped, list them:

```
Skipped pending todos (run /todo-triage to approve):
  - 003-pending-p2-missing-index.md
  - 005-pending-p3-rename-variable.md
```

## Quality Gates

- Only `ready` todos are resolved. Never resolve `pending` todos.
- Gate after Step 4: changes committed and todos marked complete before proceeding.
- Gate after Step 5: compound skill ran (or was explicitly skipped) before cleanup.
- Never delete files in `docs/brainstorms/`, `docs/plans/`, or `docs/solutions/`.

## Outputs

- All resolved `ready` todos renamed to `complete` and deleted from the directory.
- Changes committed and pushed.
- A solution document in `docs/solutions/` (via `ce:compound`), if learnings were captured.
- A final summary of resolved, skipped, and cleaned-up counts.

## Feeds Into

- `todo-triage` — to approve any pending todos that were skipped.
- `ce:compound` — called internally in Step 5 to document learnings.
