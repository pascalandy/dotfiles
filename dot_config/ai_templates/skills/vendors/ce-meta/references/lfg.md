# LFG (Let's F***ing Go)

> Full autonomous engineering workflow: plan → implement → review → resolve todos → browser-test → feature video, in strict sequential order.

## When to Use

When the user provides a feature description and wants end-to-end autonomous delivery without manual step progression. Triggers on "lfg", "ship this", or any request for a full autonomous engineering cycle.

## Inputs

- Feature description or task arguments passed to the workflow (`$ARGUMENTS`).
- A working repository with compound-engineering skills available.

## Methodology

**CRITICAL: Execute every step IN ORDER. Do NOT skip any step. Do NOT jump to coding before the plan is verified in writing.**

---

### Step 1 (Optional): ralph-loop

If the `ralph-loop` skill is available, run:

```
/ralph-loop:ralph-loop "finish all slash commands" --completion-promise "DONE"
```

If `ralph-loop` is not available or fails, skip immediately and proceed to Step 2.

---

### Step 2: Plan

Run:

```
/ce:plan <ARGUMENTS>
```

**GATE — STOP and verify:**
- A plan file has been written to `docs/plans/`.
- If no plan file exists, re-run `/ce:plan <ARGUMENTS>`.
- **Record the plan file path** — it is required for Step 4.
- Do NOT proceed to Step 3 until a written plan file exists on disk.

---

### Step 3: Work

Run:

```
/ce:work
```

**GATE — STOP and verify:**
- Implementation was performed: files were created or modified beyond the plan document itself.
- If no code changes were made, do not proceed to Step 4.

---

### Step 4: Review

Run:

```
/ce:review mode:autofix plan:<plan-path-from-step-2>
```

Pass the plan file path recorded in Step 2 so the review can verify requirements completeness against the written plan.

---

### Step 5: Resolve TODOs

Run:

```
/compound-engineering:todo-resolve
```

---

### Step 6: Browser Test

Run:

```
/compound-engineering:test-browser
```

---

### Step 7: Feature Video

Run:

```
/compound-engineering:feature-video
```

---

### Step 8: Completion Signal

Output:

```
<promise>DONE</promise>
```

Only after the feature video has been added to the PR.

---

### Order Enforcement Summary

```
[Optional] ralph-loop
      |
      v
  ce:plan  ──── GATE: plan file exists in docs/plans/
      |
      v
  ce:work  ──── GATE: code changes made
      |
      v
  ce:review (mode:autofix, plan:<path>)
      |
      v
  todo-resolve
      |
      v
  test-browser
      |
      v
  feature-video
      |
      v
  <promise>DONE</promise>
```

## Quality Gates

- [ ] Plan file exists at `docs/plans/` before work begins.
- [ ] Code files created or modified before review begins.
- [ ] Review run with `mode:autofix` and correct plan path.
- [ ] TODOs resolved.
- [ ] Browser tests passed.
- [ ] Feature video recorded and added to PR.
- [ ] `<promise>DONE</promise>` emitted only after video is in PR.

## Outputs

- A written plan in `docs/plans/`.
- Implemented code changes.
- A reviewed, auto-fixed codebase.
- Resolved TODOs.
- Passing browser tests.
- Feature video in PR.
- Completion signal.

## Feeds Into

- PR merge / ship workflow.
- `ce:compound` for capturing learnings from the work session.
