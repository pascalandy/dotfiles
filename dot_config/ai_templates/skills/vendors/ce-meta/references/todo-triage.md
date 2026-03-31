# Todo Triage

> Interactive workflow for reviewing pending todos one by one and deciding whether to approve, skip, or modify each.

## When to Use

- Reviewing pending todos for approval
- Prioritizing code review findings
- Interactively categorizing work items before implementation

## Inputs

- Pending todo files in `.context/compound-engineering/todos/` and legacy `todos/` directories

## Methodology

**Do not write code during triage.** This is purely for review and prioritization — implementation happens in `todo-resolve`.

### 1. Setup

Use a lightweight/fast model for this workflow. Read all pending todos from `.context/compound-engineering/todos/` and legacy `todos/` directories.

### 2. Present Each Finding

For each pending todo, present it clearly with:
- Severity
- Category
- Description
- Location
- Problem scenario
- Proposed solution
- Effort estimate

Use severity levels: 🔴 P1 (CRITICAL), 🟡 P2 (IMPORTANT), 🔵 P3 (NICE-TO-HAVE).

Include progress tracking in each header: `Progress: 3/10 completed`

Then prompt the user:

```
Do you want to add this to the todo list?
1. yes - approve and mark ready
2. next - skip (deletes the todo file)
3. custom - modify before approving
```

### 3. Handle Decision

**yes:** Rename file from `pending` → `ready` in both filename and frontmatter. Fill the Recommended Action section. If creating a new todo (not updating existing), use the naming convention from the `todo-create` skill.

Priority mapping:
- 🔴 P1 → `p1`
- 🟡 P2 → `p2`
- 🔵 P3 → `p3`

Confirm: `✅ Approved: {filename} (Issue #{issue_id}) - Status: **ready**`

**next:** Delete the todo file. Log as skipped for the final summary.

**custom:** Ask what to modify, update the todo, re-present it, ask again.

### 4. Final Summary

After all items are processed, output:

```markdown
## Triage Complete

**Total Items:** [X] | **Approved (ready):** [Y] | **Skipped:** [Z]

### Approved Todos (Ready for Work):
- `042-ready-p1-transaction-boundaries.md` - Transaction boundary issue

### Skipped (Deleted):
- Item #5: [reason]
```

### 5. Next Steps

Prompt the user:

```markdown
What would you like to do next?

1. run todo-resolve to resolve the todos
2. commit the todos
3. nothing, go chill
```

## Quality Gates

- Every pending todo must receive an explicit decision (yes / next / custom) — no silent skips
- Approved todos must have status updated in both filename and frontmatter
- Recommended Action section must be filled before marking ready
- Final summary must account for all items processed

## Outputs

- Todo files renamed from `pending` → `ready` (approved items)
- Deleted todo files (skipped items)
- Final triage summary with counts and lists
- Next-step prompt for the user

## Feeds Into

- `todo-resolve` — executes the approved ready todos
- Git commit of triaged todo files
