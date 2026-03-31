# SLFG

> Full autonomous engineering workflow using swarm mode for parallel execution.

## When to Use

When the user wants a fully automated end-to-end engineering run — plan, build, review, test, fix, and ship — with maximum parallelism via swarm agents.

## Inputs

- Feature description or task argument (passed through to `ce:plan`)
- A working checkout with a dev server available (for browser testing)

## Methodology

Run these phases in order. Do not stop between phases — complete every step through to the end.

### Sequential Phase

1. **Optional:** If the `ralph-loop` skill is available, invoke it with prompt `"finish all slash commands"` and completion promise `"DONE"`. If not available or it fails, skip and continue to step 2 immediately.
2. Run `ce:plan $ARGUMENTS` — **record the plan file path** from `docs/plans/` for use in steps 4 and 6.
3. Run `ce:work` in **swarm mode**: create a task list and launch an army of parallel subagents to build the plan.

### Parallel Phase

After work completes, launch steps 4 and 5 as **parallel background subagents** (both only need code to be written; no checkout mutation):

4. Run `ce:review mode:report-only plan:<plan-path-from-step-2>` — spawn as background subagent.
5. Run `test-browser` — spawn as background subagent.

Wait for **both** to complete before continuing.

### Autofix Phase

6. Run `ce:review mode:autofix plan:<plan-path-from-step-2>` — run **sequentially** after the parallel phase so it can safely mutate the checkout, apply `safe_auto` fixes, and emit residual todos for step 7.

### Finalize Phase

7. Run `todo-resolve` — resolve findings, compound on learnings, clean up completed todos.
8. Run `feature-video` — record the final walkthrough and add to the PR.
9. Output `<promise>DONE</promise>` when video is in the PR.

## Quality Gates

- Steps 4 and 5 must both complete before entering the Autofix Phase.
- After step 6, verify autofix was applied and residual todos were emitted before proceeding to step 7.
- After step 7, verify todos are resolved and changes committed.
- After step 8, verify the video is attached to the PR before emitting the DONE promise.

## Outputs

- A merged or PR-ready branch with the planned feature implemented.
- Code review findings resolved (safe_auto applied, residuals captured as todos).
- Browser test results.
- Lessons documented via `ce:compound`.
- Feature walkthrough video attached to the PR.

## Feeds Into

- `todo-triage` — if pending todos remain after `todo-resolve`.
- `ce:compound` — called internally during `todo-resolve`.
