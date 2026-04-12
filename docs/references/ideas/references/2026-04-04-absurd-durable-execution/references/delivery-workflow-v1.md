---
name: Delivery Workflow v1 (High-Level)
description: High-level use case for end-to-end development workflow in Absurd -- superseded by v2
tags:
  - area/ea
  - kind/plan
  - status/stable
  - status/closed
date_updated: 2026-04-04
---

# Absurd Use Case: End-to-End Development Workflow

## Goal

Model a common software-delivery path as a durable, resumable workflow in Absurd: plan to implementation to review to merge.

## Prerequisites

- A detailed plan (PRD) provided by the user
- A running Postgres instance with the Absurd schema installed
- Four queues created: `delivery-orchestrator`, `delivery-build`, `delivery-review`, `delivery-ops`
- Prompt files versioned on disk (the `prompts/` directory)
- Model profile config resolved (the `prompt-config.toml`)

## At a glance

```
queues (flat, all peers):
  delivery-orchestrator   ← deliver-change (parent task)
  delivery-build          ← implement-from-plan
  delivery-review         ← run-lsp-and-lint, review-diff, qa-branch
  delivery-ops            ← create-branch, uat-handoff, open-pull-request,
                             request-greptile-review, wait-for-ci,
                             merge-when-green
```

## Parent task: `deliver-change`

Runs on `delivery-orchestrator`.

Acts as a release manager: loads the plan, spawns child tasks on the right queues, awaits each result, stops early on hard failure, waits durably for external events (CI, Greptile, human UAT approval).

The parent collects each child result and passes them forward as params to downstream tasks (e.g. qa-branch results fed to uat-handoff).

### Loop-back rules

- On `review-diff` failure or UAT rejection, the parent replays steps 2-5 (implement → lint → review → qa), not just implementation alone.
- Maximum 3 loop iterations per feedback cycle. After 3 failures, the parent fails the workflow with a clear message instead of spawning another attempt.

## Execution flow

The workflow runs in three phases: automated build, human validation, automated delivery.

### Phase 1 -- automated, runs to completion

| Order | Child task | Queue | Absurd feature used |
|---|---|---|---|
| 1 | `create-branch` | `delivery-ops` | step persists branch name; basic model selection |
| 2 | `implement-from-plan` | `delivery-build` | checkpointed steps (TDD slices survive crashes) |
| 3 | `run-lsp-and-lint` | `delivery-review` | retry (auto-fix then rerun) |
| 4 | `review-diff` | `delivery-review` | task result drives pass/fail gate; on failure, parent replays steps 2-5 with review feedback (max 3 loops) |
| 5 | `qa-branch` | `delivery-review` | task result drives pass/fail gate |

After step 5 completes, the code is implemented, linted, reviewed, and tested -- but not committed. The working tree is what the human validates.

### Phase 2 -- human UAT gate

| Order | Child task | Queue | Absurd feature used |
|---|---|---|---|
| 6 | `uat-handoff` | `delivery-ops` | durable event wait for human approval signal |

The parent spawns `uat-handoff`, which produces a UAT brief (see details below), then enters a durable event wait. The workflow is now sleeping in Postgres -- no worker, no poller, no resources consumed -- until the human signals approval or rejection.

On rejection, the parent replays steps 2-5 with the human's feedback (max 3 loops), then re-enters this gate. On approval, the workflow advances to Phase 3.

### Phase 3 -- automated delivery

| Order | Child task | Queue | Absurd feature used |
|---|---|---|---|
| 7 | `open-pull-request` | `delivery-ops` | checkpointed steps: step 1 commits (persists SHA), step 2 opens PR (persists URL) |
| 8a | `request-greptile-review` | `delivery-ops` | durable event wait (external async system) |
| 8b | `wait-for-ci` | `delivery-ops` | durable sleep (poll CI status) or webhook event |
| 9 | `merge-when-green` | `delivery-ops` | deterministic gate check on 8a + 8b results, no model needed |

Steps 8a and 8b run in parallel -- Greptile and CI are independent external systems. The parent spawns both and awaits both results before proceeding to step 9.

### UAT handoff details

`uat-handoff` produces a brief for the human containing:

- Summary of what was implemented (from the plan params)
- What `qa-branch` tested and its results (passed/failed tests, coverage)
- What `review-diff` found (any warnings, the pass result)
- The branch name and how to check it out locally
- Exact commands to run the app/tests locally
- What the human should manually verify (derived from the plan)

The parent durably waits for one of:

```bash
# approve
absurdctl emit-event "uat-approved:<task-id>" -q delivery-orchestrator -P approved=true

# reject with feedback
absurdctl emit-event "uat-approved:<task-id>" -q delivery-orchestrator -P approved=false -P feedback="description of issue"
```

## Prompt management

````txt
prompt layer (application code, not Absurd):
  prompts/
    implement-from-plan/
      v1.md
      v2.md
    review-diff/
      v1.md
    qa-branch/
      v1.md
    uat-handoff/
      v1.md
    ...
  prompt-config.toml        ← maps step → prompt version + model profile
````

## Keep in mind

The focus is not code. The focus is:

- what the workflow looks like at a high level
- how prompts are managed across steps
- how model choice is decided per step
- how Absurd helps make the whole thing durable and resumable

What Absurd owns:

- queues, tasks, steps, checkpoints, retries, events, sleeps.

What you own:

- prompts, model selection, calling the model (e.g. `opencode run --agent`).

Key durability points:

- If a worker dies mid-implementation, Absurd resumes from the last checkpoint, not from zero.
- Greptile and CI waits are durable sleeps or event waits -- no long-lived in-memory poller.
- Review and UAT failures can loop the workflow back to implementation without losing execution history (max 3 loops per feedback cycle).
- The parent stops early on any hard failure or after exhausting loop retries.
- If merge fails due to conflicts, the workflow fails cleanly -- no automatic rebase.