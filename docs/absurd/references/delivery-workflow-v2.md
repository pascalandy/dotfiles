---
name: Delivery Workflow Spec v2
description: Full spec for end-to-end development workflow in Absurd -- prompts, agents, queues, child tasks, gate logic, loop-back mechanics
tags:
  - area/ea
  - kind/plan
  - status/stable
date_updated: 2026-04-04
---

# Absurd Use Case v2: End-to-End Development Workflow -- Full Spec

## Goal

Model a common software-delivery path as a durable, resumable workflow in Absurd: plan to implementation to review to merge. This is the spec for building the actual workflow -- it defines every prompt, skill, agent, and Absurd primitive needed.

## Prerequisites

- A detailed plan (PRD) provided by the user
- A running Postgres instance with the Absurd schema installed
- Four queues created: `delivery-orchestrator`, `delivery-build`, `delivery-review`, `delivery-ops`
- Prompt files versioned on disk (the `prompts/` directory)
- Model profile config resolved (`prompt-config.toml`)
- OpenCode installed with agents configured (`opencode run --agent <name>`)

## Architecture at a glance

```
queues (flat, all peers):
  delivery-orchestrator   <- deliver-change (parent task)
  delivery-build          <- implement-from-plan
  delivery-review         <- run-lsp-and-lint, review-diff-pass1, review-diff-pass2, qa-branch
  delivery-ops            <- create-branch, uat-handoff, open-pull-request,
                             [optional] request-greptile-review, wait-for-ci,
                             merge-when-green
```

## Agent matrix

Each child task runs via `opencode run --agent <agent>`. Agent selection is per-task, defined in `prompt-config.toml`.

| Agent | Model | Speed | Cost | Intelligence | Use for |
|---|---|---|---|---|---|
| `1-kimi` | Kimi K2.5 Turbo | Fastest | Lowest | High | Default. Simple ops, lint, verification, summaries |
| `2-opus` | Claude Opus 4.6 | Slow | High | Highest | Complex reasoning, architecture, orchestration |
| `gpthigh` | GPT-5.4 High | Medium | Medium-high | Very high | Second-pass review, different reasoning perspective |
| `gemini` | Gemini 3.1 Pro | Medium | Medium | High | Fourth-pass review (only if explicitly requested) |
| `glm` | GLM 5.1 | Medium-fast | Low | High (coding) | Bulk implementation, batch tasks, cost-sensitive work |

---

## Parent task: `deliver-change`

**Queue:** `delivery-orchestrator`

**Role:** Release manager. Loads the plan, spawns child tasks on the right queues, awaits each result, passes results forward as params to downstream children, stops early on hard failure, waits durably for external events.

### Orchestrator design: hybrid gates

The parent uses **deterministic gates** for clear results and **invokes a model** only for ambiguous ones.

**Deterministic path (no model cost, fastest):**
- Child returns `status == "pass"` -> proceed to next step
- Child returns `status == "fail"` -> loop back to step 2 with `feedback_for_retry`
- UAT event has `approved == true` -> proceed to Phase 3
- UAT event has `approved == false` -> loop back to step 2 with human feedback

**Model-assisted path (invoked conditionally):**
- Child returns `status == "warn"` -> spawn a lightweight model call (`1-kimi`) to interpret the warnings and decide: proceed or loop back
- This only applies to `review-diff-pass1` / `review-diff-pass2` (warnings from review) and `qa-branch` (partial test failures)

**Prompt file:** `prompts/orchestrator-gate/v1.md`

### Loop-back rules

- On `review-diff-pass1` or `review-diff-pass2` failure or UAT rejection: replay steps 2-6 (implement -> lint -> review-pass1 -> review-pass2 -> qa)
- The replay passes the failure feedback as an optional param to `implement-from-plan`
- Maximum 3 loop iterations per feedback cycle
- After 3 failures: parent fails the workflow with a clear error message

### Result forwarding

The parent collects each child's result JSON and passes relevant fields forward:

```
create-branch.result.branch_name    -> implement-from-plan.params.branch_name
create-branch.result.worktree_path   -> implement-from-plan.params.worktree_path (and all downstream tasks)
create-branch.result.base_sha        -> review-diff-pass1.params.base_sha, review-diff-pass2.params.base_sha
implement-from-plan.result.files_changed -> review-diff-pass1.params.files_changed
implement-from-plan.result.head_sha  -> review-diff-pass1.params.head_sha, review-diff-pass2.params.head_sha
review-diff-pass1.result.criteria    -> review-diff-pass2.params.pass1_criteria
qa-branch.result (full object)       -> uat-handoff.params.qa_results
review-diff-pass1.result.criteria + review-diff-pass2.result.criteria -> uat-handoff.params.review_findings
qa-branch.result (full object)       -> open-pull-request.params.qa_results
review results (combined)            -> open-pull-request.params.review_findings
open-pull-request.result.pr_number   -> request-greptile-review.params.pr_number
open-pull-request.result.pr_url      -> request-greptile-review.params.pr_url
```

---

## Execution flow

### Phase 1 -- Automated build

| Order | Child task | Queue | Agent | Skill | Sub-skill |
|---|---|---|---|---|---|
| 1 | `create-branch` | `delivery-ops` | `1-kimi` | superpowers | `>worktree` |
| 2 | `implement-from-plan` | `delivery-build` | `2-opus` (controller) | superpowers | `>subagent-dev` |
| 3 | `run-lsp-and-lint` | `delivery-review` | `1-kimi` | superpowers | `>verify` |
| 4 | `review-diff-pass1` | `delivery-review` | `1-kimi` | superpowers | `>request-review` |
| 5 | `review-diff-pass2` | `delivery-review` | `gpthigh` | superpowers | `>request-review` |
| 6 | `qa-branch` | `delivery-review` | `1-kimi` | superpowers | `>verify` + `>tdd` |

### Phase 2 -- User UAT gate

| Order | Child task | Queue | Agent | Skill | Sub-skill |
|---|---|---|---|---|---|
| 7 | `uat-handoff` | `delivery-ops` | `1-kimi` | compound-engineering | VerifyAndCompound -> CaptureAndShare |

### Phase 3 -- Automated delivery (optional tasks marked)

| Order | Child task | Queue | Agent | Skill | Sub-skill | Optional |
|---|---|---|---|---|---|---|
| 8 | `open-pull-request` | `delivery-ops` | `1-kimi` | compound-engineering | ExecuteWork -> ManageDelivery | no |
| 9a | `request-greptile-review` | `delivery-ops` | `1-kimi` | gstack | review -> greptile-triage | **yes** |
| 9b | `wait-for-ci` | `delivery-ops` | none | -- (pure ops script) | -- | **yes** |
| 10 | `merge-when-green` | `delivery-ops` | none | -- (deterministic gate) | -- | **yes** |

---

## Child task specs

See the full prompt templates and I/O schemas for each child task in this document's source. Key tasks:

1. **`create-branch`** -- Creates isolated git worktree
2. **`implement-from-plan`** -- TDD implementation with subagent dispatch
3. **`run-lsp-and-lint`** -- Lint/type-check with auto-fix
4. **`review-diff-pass1`** -- First-pass rubric review (spec compliance, error handling, type safety, test coverage, security)
5. **`review-diff-pass2`** -- Second-pass rubric review (pattern conformance, edge cases, migration safety, concurrency, API compat)
6. **`qa-branch`** -- Full test suite + plan verification
7. **`uat-handoff`** -- UAT brief for human + durable wait
8. **`open-pull-request`** -- Commit, push, open PR
9. **`request-greptile-review`** -- External review triage (optional)
10. **`wait-for-ci`** -- CI polling (optional)
11. **`merge-when-green`** -- Deterministic merge gate (optional)

---

## Prompt management

```
prompts/
  create-branch/v1.md
  implement-from-plan/v1.md
  run-lsp-and-lint/v1.md
  review-diff-pass1/v1.md
  review-diff-pass2/v1.md
  qa-branch/v1.md
  uat-handoff/v1.md
  open-pull-request/v1.md
  request-greptile-review/v1.md
  orchestrator-gate/v1.md
prompt-config.toml
```

---

## Durability points

| Scenario | What Absurd does |
|---|---|
| Worker dies mid-implementation | Resumes from last checkpointed TDD slice, not from zero |
| Greptile/CI waits | Durable sleep or event wait -- no long-lived in-memory poller |
| Review/UAT rejects implementation | Parent loops back with feedback, execution history preserved |
| Parent exhausts 3 retries | Workflow fails cleanly with full retry history |
| Merge fails due to conflicts | Workflow fails cleanly -- no automatic rebase |
| Human takes hours to UAT | Workflow sleeps in Postgres -- zero resource consumption |

---

## What Absurd owns vs what you own

**Absurd owns:**
- Queues, tasks, steps, checkpoints, retries, events, sleeps
- Durable execution and crash recovery
- Task result persistence and forwarding

**You own:**
- Prompts (versioned markdown files in `prompts/`)
- Model selection (`prompt-config.toml` -> agent mapping)
- Calling the model (`opencode run --agent <name> "<prompt>"`)
- Template rendering (resolving params into prompts)
- Optional task activation flags
- Orchestrator hybrid gate logic (deterministic for pass/fail, model for warn)

## Related

- [[absurd-skill-draft]]
- [[delivery-workflow-v1]]
- [[prompts-history]]
