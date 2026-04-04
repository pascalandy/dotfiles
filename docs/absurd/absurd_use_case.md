# Absurd Use Case: End-to-End Development Workflow

## Goal

Model a common software-delivery path as a durable, resumable workflow in Absurd: plan to implementation to review to merge.

## Prerequisites

- A detailed plan (PRD) provided by the user
- A git branch ready for the work (or branch creation as a step)
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
  delivery-ops            ← commit-branch, open-pull-request, request-greptile-review,
                             wait-for-ci, merge-when-green
```

## Parent task: `deliver-change`

Runs on `delivery-orchestrator`. 

Acts as a release manager: loads the plan, spawns child tasks on the right queues, awaits each result, stops early on hard failure, waits durably for external events (CI, Greptile).

## Execution flow

Each phase is a child task. The parent awaits each result before deciding to continue or stop. Each child can fail, retry, sleep, or wait independently without losing the whole workflow.

| Order | Child task | Queue | Absurd feature used |
|---|---|---|---|
| 1 | `implement-from-plan` | `delivery-build` | checkpointed steps (TDD slices survive crashes) |
| 2 | `run-lsp-and-lint` | `delivery-review` | retry (auto-fix then rerun) |
| 3 | `review-diff` | `delivery-review` | task result drives pass/fail gate; on failure, parent re-spawns `implement-from-plan` with review feedback |
| 4 | `qa-branch` | `delivery-review` | task result drives pass/fail gate |
| 5 | `commit-branch` | `delivery-ops` | step persists commit SHA |
| 6 | `open-pull-request` | `delivery-ops` | step persists PR URL |
| 7 | `request-greptile-review` | `delivery-ops` | durable event wait (external async system) |
| 8 | `wait-for-ci` | `delivery-ops` | durable sleep (poll CI status) or webhook event |
| 9 | `merge-when-green` | `delivery-ops` | deterministic gate check, no model needed |

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
- Review failures can loop the workflow back to implementation without losing execution history.
- The parent stops early on any hard failure.
