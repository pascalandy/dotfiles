# Absurd Use Case: End-to-End Development Workflow

## At a glance

```
queues (flat, all peers):
  delivery-orchestrator   ← deliver-change (parent task)
  delivery-build          ← implement-from-plan
  delivery-review         ← run-lsp-and-lint, review-diff, qa-branch
  delivery-ops            ← commit-branch, open-pull-request, request-greptile-review,
                             wait-for-ci, merge-when-green

child tasks:
  implement-from-plan
  run-lsp-and-lint
  review-diff
  qa-branch
  commit-branch
  open-pull-request
  request-greptile-review
  wait-for-ci
  merge-when-green

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

What Absurd owns: queues, tasks, steps, checkpoints, retries, events, sleeps.
What you own: prompts, model selection, calling the model (e.g. `opencode run --agent`).

---

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

## The high-level shape

The cleanest way to model this in Absurd is as one parent task that orchestrates a set of durable phases.

Suggested top-level task name:

- `deliver-change`

Suggested queues:

- `delivery-build` for implementation work
- `delivery-review` for review and qa work
- `delivery-ops` for git, PR, CI, and merge operations

Why split queues:

- implementation and review often want different concurrency profiles
- child-task waits should happen cross-queue, which aligns well with Absurd `0.3.0`
- operations such as PR creation, CI waiting, and merge gating are easier to isolate

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

---

## How prompt management should work

This is the part that matters most for your question.

The main mistake would be to treat prompts as ad hoc strings assembled at runtime with no versioning.

A better approach is:

- treat prompts as versioned workflow assets
- give each step a prompt contract
- persist which prompt version was used
- persist which model was selected
- persist the important artifacts that were fed into the prompt

## Prompt model

Each prompt has three layers:

| Layer | Changes | Example |
|---|---|---|
| System behavior | rarely | "act as a TDD implementer" |
| Step instructions | per phase | "implement the smallest red/green slice from this plan" |
| Runtime context | every run | plan content, diff, PR URL, CI check list |

Each phase should define four contracts: input (what must be present), behavior (what the model may do), output (what shape it returns), escalation (when to stop and ask a human).

Persist provenance with every AI-backed step: prompt family, prompt version, model profile, concrete model, key input artifacts.

## Model profiles

Route by profile name in workflow code. Resolve to a concrete model in config.

| Child task | Model profile | Why |
|---|---|---|
| `implement-from-plan` | `builder-strong` | highest complexity, highest blast radius |
| `run-lsp-and-lint` | `builder-fast` | mostly tooling, model only for unfixable cases |
| `review-diff` | `reviewer-strong` | bad review blocks good code or misses bad code |
| `qa-branch` | `qa-browser` | observation and tool use, not deep reasoning |
| `commit-branch` | `summarizer-fast` | hard work already done |
| `open-pull-request` | `summarizer-fast` | clear communication, low creativity |
| `request-greptile-review` | n/a | external service, not your model |
| `wait-for-ci` | `ops-safe` | deterministic gate, minimal hallucination risk |
| `merge-when-green` | `ops-safe` | deterministic gate |

## Recommended prompt and model matrix

| Phase | Prompt style | Output style | Best model profile | Retry posture |
|---|---|---|---|---|
| Read plan and implement | TDD implementer | changed files, tests, residual risks | `builder-strong` | retry with same profile, escalate on ambiguity |
| LSP / lint | diagnostics fixer | fixed issues, remaining blockers | `builder-fast` | retry automatically after fixes |
| Code review | findings-first reviewer | severity-ordered findings | `reviewer-strong` | retry on transient tool failure only |
| QA | user-flow validator | pass/fail plus evidence | `qa-browser` | retry on flaky environment, escalate on product failure |
| Commit all | concise summarizer | commit message and git result | `summarizer-fast` | retry on hook or staging failure |
| Open PR | reviewer-facing summarizer | PR title/body and URL | `summarizer-fast` | retry on network or auth failure |
| Greptile review | external review orchestrator | findings ingested and normalized | `ops-safe` | wait durably for event |
| Wait for CI | operational gate checker | check matrix and final gate | `ops-safe` | sleep and retry, or event wait |
| Merge to main | strict gate enforcer | merge result | `ops-safe` | retry only on transient platform failure |

## How Absurd helps with prompts specifically

Absurd is not choosing prompts for you. That is your policy layer.

What Absurd gives you is durable execution around prompt-driven work.

That means:

- if an implementation run crashes after writing tests, you do not lose that checkpoint
- if Greptile takes 20 minutes, you wait durably
- if CI takes an hour, you wait durably
- if QA needs to be rerun after a fix, the workflow can loop back cleanly
- if you later change a prompt family, you can version the step or normalize the returned artifact shape

In other words, Absurd does for prompt-driven engineering workflows what it already does for business workflows: it turns long, failure-prone, multi-stage processes into resumable state machines.

## How this should look operationally

At a human level, you would see something like this:

- one delivery task starts for a plan
- implementation runs and checkpoints each TDD slice
- lint runs and cleans up
- review runs and either passes or sends the workflow back for repair
- QA runs and records evidence
- commit and PR steps produce durable metadata
- Greptile review is submitted and awaited
- CI is awaited without a long-lived in-memory worker
- merge runs only if all gates are green

Everything important has a durable trail:

- which prompt family was used
- which model profile and concrete model were used
- which artifacts were fed in
- which findings were returned
- which gates passed or failed

## Recommended design decisions

If you wanted this to work well in practice, I would recommend:

1. Keep prompts versioned outside the workflow code.
2. Route by model profile, not concrete model name, inside workflow logic.
3. Persist prompt version and model metadata with every AI-backed step.
4. Keep review, QA, and ops phases separate from implementation.
5. Use cross-queue child waits for major phases.
6. Make deploy and merge mostly deterministic, not model-driven.
7. Treat external systems such as Greptile and CI as event sources, not synchronous calls.
8. Version step names when prompt output shape or artifact meaning changes.

## Final takeaway

At high level, the use case is not “Absurd writes code.”

The use case is:

- Absurd coordinates a classic dev workflow as a durable multi-phase delivery pipeline
- prompts are first-class workflow assets with versions and contracts
- model choice is a policy decision per phase
- long waits, retries, review loops, and external gates become durable instead of fragile

That is what this style of workflow should look like if you want it to stay understandable and operable over time.
