# Absurd Use Case: End-to-End Development Workflow

## Goal

This document shows what a high-level, durable development workflow could look like with Absurd for a very common software-delivery path:

1. read plan and implement with red/green TDD
2. lsp / lint
3. code review
4. qa
5. commit all
6. open pr
7. pr review with Greptile
8. deploy and wait for ci
9. merge to main

The focus here is not code. The focus is:

- what the workflow looks like at a high level
- how prompts are managed across steps
- how model choice is decided per step
- how Absurd helps make the whole thing durable and resumable

## Prerequisites

- A detailed plan (PRD) provided by the user
- A git branch ready for the work (or branch creation as a step)
- A running Postgres instance with the Absurd schema installed
- Four queues created: `delivery-orchestrator`, `delivery-build`, `delivery-review`, `delivery-ops`
- Prompt files versioned on disk (the `prompts/` directory)
- Model profile config resolved (the `prompt-config.toml`)

## At a glance

The cleanest way to model this in Absurd is as one parent task that orchestrates a set of durable phases.

```txt
queues (flat, all peers):
  delivery-orchestrator   ← deliver-change (parent task)
  delivery-build          ← implement-from-plan
  delivery-review         ← run-lsp-and-lint, review-diff, qa-branch
  delivery-ops            ← commit-branch, open-pull-request, request-greptile-review,
                             wait-for-ci, merge-when-green

child tasks:
  implement-from-plan     ← delivery-build
  run-lsp-and-lint        ← delivery-review
  review-diff             ← delivery-review
  qa-branch               ← delivery-review
  commit-branch           ← delivery-ops
  open-pull-request       ← delivery-ops
  request-greptile-review ← delivery-ops
  wait-for-ci             ← delivery-ops
  merge-when-green        ← delivery-ops

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
```

Why split queues:

- implementation and review often want different concurrency profiles
- child-task waits should happen cross-queue, which aligns well with Absurd `0.3.0`
- operations such as PR creation, CI waiting, and merge gating are easier to isolate

What Absurd owns: queues, tasks, steps, checkpoints, retries, events, sleeps.
What you own: prompts, model selection, calling the model (e.g. `opencode run --agent`).

## What the parent workflow is responsible for

The parent task is not where all detailed work happens.

The parent task should:

- load the plan and metadata for the change
- decide the execution order
- spawn child tasks on the right queues
- await the terminal result of each child task
- stop early on hard failures
- persist all decision points and artifacts
- wait durably for external events such as CI completion or Greptile feedback

At this level, the parent task is a release manager.

## What the child tasks are responsible for

Each major stage becomes one child task with its own prompt policy, model policy, acceptance criteria, and output contract.

Suggested child tasks:

- `implement-from-plan`
- `run-lsp-and-lint`
- `review-diff`
- `qa-branch`
- `commit-branch`
- `open-pull-request`
- `request-greptile-review`
- `wait-for-ci`
- `merge-when-green`

This is useful because each child task can fail, retry, sleep, or wait independently without losing the whole workflow.

## Execution flow

The parent task (`deliver-change`) runs on `delivery-orchestrator` and drives the sequence. Each phase is a child task spawned on the appropriate queue. The parent awaits each result before deciding to continue or stop.

| Order | Child task | Queue | Absurd feature used |
|---|---|---|---|
| 1 | `implement-from-plan` | `delivery-build` | checkpointed steps (TDD slices survive crashes) |
| 2 | `run-lsp-and-lint` | `delivery-review` | retry (auto-fix then rerun) |
| 3 | `review-diff` | `delivery-review` | step result drives pass/fail gate; parent can loop back to build on failure |
| 4 | `qa-branch` | `delivery-review` | step result drives ship/no-ship gate |
| 5 | `commit-branch` | `delivery-ops` | step persists commit SHA |
| 6 | `open-pull-request` | `delivery-ops` | step persists PR URL |
| 7 | `request-greptile-review` | `delivery-ops` | durable event wait (external async system) |
| 8 | `wait-for-ci` | `delivery-ops` | durable sleep + periodic wake or webhook event |
| 9 | `merge-when-green` | `delivery-ops` | deterministic gate check, no model needed |

Key durability points:

- If a worker dies mid-implementation, Absurd resumes from the last checkpoint, not from zero.
- Greptile and CI waits are durable sleeps or event waits -- no long-lived in-memory poller.
- Review failures can loop the workflow back to implementation without losing execution history.
- The parent stops early on any hard failure.
