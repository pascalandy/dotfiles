---
name: Delivery Workflow Spec v2
description: Full spec for end-to-end development workflow in Absurd -- prompts, agents, queues, child tasks, gate logic, loop-back mechanics
tags:
  - area/ea
  - kind/plan
  - status/stable
date_updated: 2026-04-04
---

# Absurd Use Case v2: End-to-End Development Workflow — Full Spec

## Goal

Model a common software-delivery path as a durable, resumable workflow in Absurd: plan to implementation to review to merge. This is the spec for building the actual workflow — it defines every prompt, skill, agent, and Absurd primitive needed.

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
  delivery-orchestrator   ← deliver-change (parent task)
  delivery-build          ← implement-from-plan
  delivery-review         ← run-lsp-and-lint, review-diff-pass1, review-diff-pass2, qa-branch
  delivery-ops            ← create-branch, uat-handoff, open-pull-request,
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
- Child returns `status == "pass"` → proceed to next step
- Child returns `status == "fail"` → loop back to step 2 with `feedback_for_retry`
- UAT event has `approved == true` → proceed to Phase 3
- UAT event has `approved == false` → loop back to step 2 with human feedback

**Model-assisted path (invoked conditionally):**
- Child returns `status == "warn"` → spawn a lightweight model call (`1-kimi`) to interpret the warnings and decide: proceed or loop back
- This only applies to `review-diff-pass1` / `review-diff-pass2` (warnings from review) and `qa-branch` (partial test failures)

**Prompt file:** `prompts/orchestrator-gate/v1.md` (loaded only for `warn` status)

```markdown
## Task

A child task returned status "warn". All blocker criteria passed, but one or more
non-blocker criteria scored <= 2. Decide whether the workflow should proceed or loop back.

## Child task: {{ child_task_name }}
## Criteria results:

{{ child_criteria_json }}

## Rules

- "warn" means all blocker criteria passed. Only non-blocker criteria failed.
- Count the non-blocker criteria that scored <= 2 (decision = "no").
- Ignore criteria scored 0 (n/a) — they are excluded from the tally.
- If all failing non-blockers are cosmetic (naming, style, minor patterns): proceed.
- If any failing non-blocker has a justification citing a concrete runtime risk (data corruption, crash, wrong output): loop back.
- When in doubt, proceed. Non-blockers are non-blockers for a reason.

## Output

Return JSON:
{
  "decision": "proceed" | "loop_back",
  "reason": "one-line explanation citing the specific criteria IDs that drove the decision"
}
```

**Agent for gate decisions:** `1-kimi` (fast, cheap — this is a simple classification task)

**Why hybrid:** Most child tasks produce clear pass/fail, so the model is never invoked for the common case. The model is only needed when `review-diff-pass1` or `review-diff-pass2` returns `warn` (all blockers passed but some non-blocker criteria scored <= 2) or `qa-branch` has partial failures (e.g., "48/50 tests pass, 2 flaky").

### Loop-back rules

- On `review-diff-pass1` or `review-diff-pass2` failure or UAT rejection: replay steps 2-6 (implement → lint → review-pass1 → review-pass2 → qa)
- The replay passes the failure feedback as an optional param to `implement-from-plan`
- Maximum 3 loop iterations per feedback cycle
- After 3 failures: parent fails the workflow with a clear error message

### Result forwarding

The parent collects each child's result JSON and passes relevant fields forward:

```
create-branch.result.branch_name    → implement-from-plan.params.branch_name
create-branch.result.worktree_path   → implement-from-plan.params.worktree_path (and all downstream tasks)
create-branch.result.base_sha        → review-diff-pass1.params.base_sha, review-diff-pass2.params.base_sha
implement-from-plan.result.files_changed → review-diff-pass1.params.files_changed
implement-from-plan.result.head_sha  → review-diff-pass1.params.head_sha, review-diff-pass2.params.head_sha
review-diff-pass1.result.criteria    → review-diff-pass2.params.pass1_criteria
qa-branch.result (full object)       → uat-handoff.params.qa_results
review-diff-pass1.result.criteria + review-diff-pass2.result.criteria → uat-handoff.params.review_findings
qa-branch.result (full object)       → open-pull-request.params.qa_results
review results (combined)            → open-pull-request.params.review_findings
open-pull-request.result.pr_number   → request-greptile-review.params.pr_number
open-pull-request.result.pr_url      → request-greptile-review.params.pr_url
```

---

## Execution flow

### Phase 1 — Automated build

| Order | Child task | Queue | Agent | Skill | Sub-skill |
|---|---|---|---|---|---|
| 1 | `create-branch` | `delivery-ops` | `1-kimi` | superpowers | `>worktree` |
| 2 | `implement-from-plan` | `delivery-build` | `2-opus` (controller) | superpowers | `>subagent-dev` |
| 3 | `run-lsp-and-lint` | `delivery-review` | `1-kimi` | superpowers | `>verify` |
| 4 | `review-diff-pass1` | `delivery-review` | `1-kimi` | superpowers | `>request-review` |
| 5 | `review-diff-pass2` | `delivery-review` | `gpthigh` | superpowers | `>request-review` |
| 6 | `qa-branch` | `delivery-review` | `1-kimi` | superpowers | `>verify` + `>tdd` |

### Phase 2 — User UAT gate

| Order | Child task | Queue | Agent | Skill | Sub-skill |
|---|---|---|---|---|---|
| 7 | `uat-handoff` | `delivery-ops` | `1-kimi` | compound-engineering | VerifyAndCompound → CaptureAndShare |

### Phase 3 — Automated delivery (optional tasks marked)

| Order | Child task | Queue | Agent | Skill | Sub-skill | Optional |
|---|---|---|---|---|---|---|
| 8 | `open-pull-request` | `delivery-ops` | `1-kimi` | compound-engineering | ExecuteWork → ManageDelivery | no |
| 9a | `request-greptile-review` | `delivery-ops` | `1-kimi` | gstack | review → greptile-triage | **yes** |
| 9b | `wait-for-ci` | `delivery-ops` | none | — (pure ops script) | — | **yes** |
| 10 | `merge-when-green` | `delivery-ops` | none | — (deterministic gate) | — | **yes** |

---

## Child task specs

### 1. `create-branch`

**Purpose:** Create an isolated git worktree for the feature work.

**Queue:** `delivery-ops`
**Agent:** `1-kimi`
**Skill:** superpowers → `>worktree` (using-git-worktrees)
**Absurd feature:** Step persists branch name; basic model selection.

**Prompt file:** `prompts/create-branch/v1.md`

**Prompt:**

```markdown
## Task

Create an isolated git worktree for implementing a feature from a plan.

## Instructions

Load skill `superpowers` and use sub-skill `>worktree`.

Create a worktree branching from `{{ base_branch }}` with branch name `{{ branch_name }}`.
The worktree path should be `{{ worktree_path }}`.

## Params

- `plan_title`: {{ plan_title }}
- `base_branch`: {{ base_branch }}
- `branch_name`: {{ branch_name }}

## Output

Return JSON:
{
  "status": "pass" | "fail",
  "branch_name": "<created branch>",
  "worktree_path": "<absolute path>",
  "base_sha": "<SHA of base>"
}
```

**Input params:**

| Param | Type | Source |
|---|---|---|
| `plan_title` | string | User-provided plan |
| `base_branch` | string | Defaults to `main` |
| `branch_name` | string | Derived from plan title or user-specified |
| `worktree_path` | string | Derived convention, e.g. `../worktrees/<branch_name>` |

**Output schema:**

```json
{
  "status": "pass | fail",
  "branch_name": "string",
  "worktree_path": "string",
  "base_sha": "string"
}
```

---

### 2. `implement-from-plan`

**Purpose:** Implement the plan with TDD discipline. Includes internal self-review per the subagent-dev methodology, but defers formal code review to `review-diff-pass1` and `review-diff-pass2`.

**Queue:** `delivery-build`
**Agent:** `2-opus` (as controller); the controller may dispatch `glm` workers for mechanical sub-tasks
**Skill:** superpowers → `>subagent-dev` (subagent-driven-development)
**Absurd feature:** Checkpointed steps. Each TDD slice is a step — survives crashes.

**Prompt file:** `prompts/implement-from-plan/v1.md`

**Prompt:**

```markdown
## Task

Implement a feature from a detailed plan using subagent-driven development.

## Instructions

Load skill `superpowers` and use sub-skill `>subagent-dev`.

You are the controller. The plan is provided below. Extract all tasks, track them,
and dispatch a fresh subagent per task. Each subagent must:
1. Implement the task with TDD (red-green-refactor)
2. Self-review before reporting back
3. Report status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT

**Internal review:** Run implementer self-review only. Do NOT run the full two-stage
spec compliance + code quality review from subagent-dev. Formal review is handled
by the separate `review-diff-pass1` and `review-diff-pass2` tasks downstream.

**Model selection for subagents:**
- Mechanical tasks (1-2 files, clear spec): use `glm`
- Integration tasks (multi-file, pattern matching): use `1-kimi`
- Architecture/design tasks: use `2-opus`

Work from: `{{ worktree_path }}`

{{ #if feedback }}
## Prior feedback (retry cycle {{ retry_count }}/3)

The previous implementation was rejected. Address this feedback:

{{ feedback }}

Focus on the feedback items. Do not redo work that was already accepted.
{{ /if }}

## Plan

{{ plan_content }}

## Output

Return JSON:
{
  "status": "pass" | "fail",
  "tasks_completed": <count>,
  "tasks_total": <count>,
  "files_changed": ["path1", "path2"],
  "head_sha": "<SHA after all commits>",
  "concerns": ["any concerns from subagents"]
}
```

**Input params:**

| Param | Type | Source |
|---|---|---|
| `plan_content` | string | Full plan text |
| `worktree_path` | string | From `create-branch` result |
| `branch_name` | string | From `create-branch` result |
| `base_sha` | string | From `create-branch` result |
| `feedback` | string? | Optional. From `review-diff-pass1`, `review-diff-pass2`, or `uat-handoff` on retry |
| `retry_count` | int | 0 on first run, incremented on loop-back (max 3) |

**Output schema:**

```json
{
  "status": "pass | fail",
  "tasks_completed": "int",
  "tasks_total": "int",
  "files_changed": ["string"],
  "head_sha": "string",
  "concerns": ["string"]
}
```

---

### 3. `run-lsp-and-lint`

**Purpose:** Run linters, LSP checks, type checkers. Auto-fix what can be fixed, then rerun.

**Queue:** `delivery-review`
**Agent:** `1-kimi`
**Skill:** superpowers → `>verify` (verification-before-completion)
**Absurd feature:** Retry (auto-fix then rerun).

**Prompt file:** `prompts/run-lsp-and-lint/v1.md`

**Prompt:**

```markdown
## Task

Run all linters, type checkers, and LSP diagnostics on the branch. Auto-fix what
is fixable, then rerun to verify.

## Instructions

Load skill `superpowers` and use sub-skill `>verify`.

Work from: `{{ worktree_path }}`

Steps:
1. Detect the project's lint/type-check commands (check package.json, Makefile, justfile, etc.)
2. Run all checks
3. For fixable errors: apply auto-fix (e.g., `eslint --fix`, `rubocop -A`, `ruff format`)
4. Rerun checks to verify fixes
5. Report remaining unfixable errors

Follow the verification-before-completion iron law: no claims without fresh evidence.

## Output

Return JSON:
{
  "status": "pass" | "fail",
  "errors_found": <count>,
  "errors_fixed": <count>,
  "errors_remaining": <count>,
  "remaining_details": ["file:line — description"],
  "commands_run": ["command1", "command2"]
}
```

**Input params:**

| Param | Type | Source |
|---|---|---|
| `worktree_path` | string | From `create-branch` result |
| `branch_name` | string | From `create-branch` result |

**Output schema:**

```json
{
  "status": "pass | fail",
  "errors_found": "int",
  "errors_fixed": "int",
  "errors_remaining": "int",
  "remaining_details": ["string"],
  "commands_run": ["string"]
}
```

---

### 4. `review-diff-pass1`

**Purpose:** First-pass code review. Fast scan using structured rubric scoring. Each criterion is evaluated independently with the `eval-rubric` skill.

**Queue:** `delivery-review`
**Agent:** `1-kimi`
**Skill:** superpowers → `>request-review` (requesting-code-review) + `eval-rubric`
**Absurd feature:** Task result drives pass/fail gate. On failure, parent replays steps 2-6 with review feedback (max 3 loops).

**Prompt file:** `prompts/review-diff-pass1/v1.md`

**Prompt:**

```markdown
## Task

Run a first-pass code review on the implementation diff using structured rubric scoring.

## Instructions

Load skill `superpowers` and use sub-skill `>request-review`.
Load skill `eval-rubric` for the scoring methodology.

You are the first reviewer. Evaluate the diff against the rubric below.
Score each criterion independently using the eval-rubric rating system (0-4).
Only inspect observable evidence in the diff. Do not reward intent or effort.

Use git range: `{{ base_sha }}..{{ head_sha }}`

## Rubric

| ID | Criterion | Blocker | What to check |
|----|-----------|---------|---------------|
| P1-1 | Spec compliance | yes | Every plan item has a corresponding code change. No plan item is missing or only partially implemented. |
| P1-2 | Error handling | yes | All new public functions handle error paths. No swallowed exceptions, no missing error returns. |
| P1-3 | Type safety | no | No `any` types, no unchecked casts, no missing null checks in new code. Score 0 if the language has no static type system. |
| P1-4 | Test behavior coverage | yes | Every new behavior has at least one test that asserts the behavior through the public interface. No test-free features. |
| P1-5 | Security basics | no | No hardcoded secrets, no unsanitized user input in queries/commands, no new endpoints without auth checks. Score 0 if the diff has no user-facing input paths. |

**Scoring rules (from eval-rubric):**

1. Does this criterion apply to this diff? If not applicable → score `0`, decision `n/a`.
2. Does the diff clearly fail this criterion? → score `1`, decision `no`.
3. Is evidence partial, ambiguous, or missing? → score `2`, decision `no`.
4. Meets the criterion with only minor non-material issues? → score `3`, decision `yes`.
5. Meets the criterion with strong, clean evidence? → score `4`, decision `yes`.

**Status derivation:**

- `pass`: all applicable criteria score >= 3
- `fail`: any **blocker** criterion scores <= 2
- `warn`: only **non-blocker** criteria score <= 2, all blockers pass

## Params

- `base_sha`: {{ base_sha }}
- `head_sha`: {{ head_sha }}
- `plan_content`: {{ plan_content }}
- `files_changed`: {{ files_changed }}

{{ #if feedback }}
## Prior feedback (retry cycle {{ retry_count }}/3)

This is a re-review after implementation was revised. Previous feedback:

{{ feedback }}

Focus on whether the feedback items were addressed.
{{ /if }}

## Output

Return JSON:
{
  "status": "pass" | "warn" | "fail",
  "criteria": [
    {
      "id": "P1-1",
      "name": "Spec compliance",
      "blocker": true,
      "score": 0-4,
      "decision": "yes" | "no" | "n/a",
      "justification": "one sentence citing observable evidence"
    }
  ],
  "blockers_failed": ["P1-1 — justification"],
  "feedback_for_retry": "string (populated when status is fail — list each failed blocker and what must change)"
}
```

**Gate logic (hybrid):**
- `status == "pass"` → proceed to `review-diff-pass2` (deterministic, no model)
- `status == "warn"` → parent loads `orchestrator-gate/v1.md` and invokes `1-kimi` to classify: proceed or loop back
- `status == "fail"` → parent loops back to step 2 with `feedback_for_retry` (deterministic, no model)

**Input params:**

| Param | Type | Source |
|---|---|---|
| `base_sha` | string | From `create-branch` result |
| `head_sha` | string | From `implement-from-plan` result |
| `plan_content` | string | Original plan text |
| `files_changed` | string[] | From `implement-from-plan` result |
| `feedback` | string? | Optional. From prior review cycle |
| `retry_count` | int | 0 on first run |

**Output schema:**

```json
{
  "status": "pass | warn | fail",
  "criteria": [
    {
      "id": "string",
      "name": "string",
      "blocker": "bool",
      "score": "int (0-4)",
      "decision": "yes | no | n/a",
      "justification": "string"
    }
  ],
  "blockers_failed": ["string"],
  "feedback_for_retry": "string"
}
```

---

### 5. `review-diff-pass2`

**Purpose:** Second-pass code review. Deep review from a different model using structured rubric scoring. Catches what the first pass missed. Each criterion is evaluated independently with the `eval-rubric` skill.

**Queue:** `delivery-review`
**Agent:** `gpthigh`
**Skill:** superpowers → `>request-review` (requesting-code-review) + `eval-rubric`
**Absurd feature:** Task result drives pass/fail gate. On failure, parent replays steps 2-6 with review feedback (max 3 loops).

**Prompt file:** `prompts/review-diff-pass2/v1.md`

**Prompt:**

```markdown
## Task

Run a second-pass code review on the implementation diff using structured rubric scoring.

## Instructions

Load skill `superpowers` and use sub-skill `>request-review`.
Load skill `eval-rubric` for the scoring methodology.

You are the second reviewer, providing a different reasoning perspective.
A first-pass review has already been completed. Its criteria results are below —
do NOT re-evaluate pass-1 criteria. Your rubric is different.

Evaluate the diff against the rubric below.
Score each criterion independently using the eval-rubric rating system (0-4).
Only inspect observable evidence in the diff. Do not reward intent or effort.

Use git range: `{{ base_sha }}..{{ head_sha }}`

## First-pass results (already evaluated, do not duplicate)

{{ pass1_criteria }}

## Rubric

| ID | Criterion | Blocker | What to check |
|----|-----------|---------|---------------|
| P2-1 | Codebase pattern conformance | no | Changes follow existing module boundaries, naming conventions, and architectural patterns in the repo. |
| P2-2 | Edge case handling | yes | Boundary conditions (empty collections, zero/negative values, max-length inputs, null/undefined) are handled explicitly. |
| P2-3 | Migration & data safety | yes | Schema changes are backward-compatible. No data loss paths. Migrations are reversible or additive-only. Score 0 if the diff contains no schema changes or data migrations. |
| P2-4 | Concurrency correctness | no | Shared state access is synchronized. No race conditions in async paths. No unguarded concurrent mutations. Score 0 if the diff has no concurrent or async code paths. |
| P2-5 | API backward compatibility | no | Existing public interfaces, return types, and API contracts are preserved or versioned. Score 0 if the diff does not modify any public API surface. |

**Scoring rules (from eval-rubric):**

1. Does this criterion apply to this diff? If not applicable → score `0`, decision `n/a`.
2. Does the diff clearly fail this criterion? → score `1`, decision `no`.
3. Is evidence partial, ambiguous, or missing? → score `2`, decision `no`.
4. Meets the criterion with only minor non-material issues? → score `3`, decision `yes`.
5. Meets the criterion with strong, clean evidence? → score `4`, decision `yes`.

**Status derivation:**

- `pass`: all applicable criteria score >= 3
- `fail`: any **blocker** criterion scores <= 2
- `warn`: only **non-blocker** criteria score <= 2, all blockers pass

## Params

- `base_sha`: {{ base_sha }}
- `head_sha`: {{ head_sha }}
- `plan_content`: {{ plan_content }}
- `files_changed`: {{ files_changed }}

{{ #if feedback }}
## Prior feedback (retry cycle {{ retry_count }}/3)

This is a re-review after implementation was revised. Previous feedback:

{{ feedback }}

Focus on whether the feedback items were addressed.
{{ /if }}

## Output

Return JSON:
{
  "status": "pass" | "warn" | "fail",
  "criteria": [
    {
      "id": "P2-1",
      "name": "Codebase pattern conformance",
      "blocker": false,
      "score": 0-4,
      "decision": "yes" | "no" | "n/a",
      "justification": "one sentence citing observable evidence"
    }
  ],
  "blockers_failed": ["P2-2 — justification"],
  "feedback_for_retry": "string (populated when status is fail — list each failed blocker and what must change)"
}
```

**Gate logic (hybrid):**
- `status == "pass"` → proceed to `qa-branch` (deterministic, no model)
- `status == "warn"` → parent loads `orchestrator-gate/v1.md` and invokes `1-kimi` to classify: proceed or loop back
- `status == "fail"` → parent loops back to step 2 with `feedback_for_retry` (deterministic, no model)

**Input params:**

| Param | Type | Source |
|---|---|---|
| `base_sha` | string | From `create-branch` result |
| `head_sha` | string | From `implement-from-plan` result |
| `plan_content` | string | Original plan text |
| `files_changed` | string[] | From `implement-from-plan` result |
| `pass1_criteria` | array | From `review-diff-pass1` result `.criteria` |
| `feedback` | string? | Optional. From prior review cycle |
| `retry_count` | int | 0 on first run |

**Output schema:**

```json
{
  "status": "pass | warn | fail",
  "criteria": [
    {
      "id": "string",
      "name": "string",
      "blocker": "bool",
      "score": "int (0-4)",
      "decision": "yes | no | n/a",
      "justification": "string"
    }
  ],
  "blockers_failed": ["string"],
  "feedback_for_retry": "string"
}
```

---

### 6. `qa-branch`

**Purpose:** Run the full test suite and verify behavior matches the plan.

**Queue:** `delivery-review`
**Agent:** `1-kimi`
**Skill:** superpowers → `>verify` (verification-before-completion) + `>tdd` (test-driven-development)
**Absurd feature:** Task result drives pass/fail gate.

**Prompt file:** `prompts/qa-branch/v1.md`

**Prompt:**

```markdown
## Task

Run the full test suite and verify the implementation matches the plan.

## Instructions

Load skill `superpowers` and use sub-skills `>verify` and `>tdd`.

Work from: `{{ worktree_path }}`

Steps:
1. Run the full test suite. Follow the `>verify` iron law: no claims without evidence.
2. If tests fail, report the failures — do NOT attempt to fix them.
3. Cross-check the plan requirements against what was implemented.
4. Verify each plan item has corresponding test coverage.
5. Report coverage gaps.

## Params

- `plan_content`: {{ plan_content }}
- `files_changed`: {{ files_changed }}

## Output

Return JSON:
{
  "status": "pass" | "warn" | "fail",
  "tests_run": <count>,
  "tests_passed": <count>,
  "tests_failed": <count>,
  "test_failures": ["test name — error"],
  "coverage_percentage": <number>,
  "coverage_gaps": ["description of untested path"],
  "plan_items_verified": <count>,
  "plan_items_total": <count>
}

Status derivation:
- `pass`: all tests pass, all plan items verified, no coverage gaps
- `warn`: all tests pass but coverage gaps exist, OR a small number of known-flaky tests fail (< 5% of total)
- `fail`: any non-flaky test fails, OR plan items are missing implementation
```

**Input params:**

| Param | Type | Source |
|---|---|---|
| `worktree_path` | string | From `create-branch` result |
| `plan_content` | string | Original plan text |
| `files_changed` | string[] | From `implement-from-plan` result |

**Output schema:**

```json
{
  "status": "pass | warn | fail",
  "tests_run": "int",
  "tests_passed": "int",
  "tests_failed": "int",
  "test_failures": ["string"],
  "coverage_percentage": "number",
  "coverage_gaps": ["string"],
  "plan_items_verified": "int",
  "plan_items_total": "int"
}
```

---

### 7. `uat-handoff`

**Purpose:** Produce a UAT brief for the human, then durably wait for approval or rejection.

**Queue:** `delivery-ops`
**Agent:** `1-kimi`
**Skill:** compound-engineering → VerifyAndCompound → CaptureAndShare
**Absurd feature:** Durable event wait for human approval signal.

**Prompt file:** `prompts/uat-handoff/v1.md`

**Prompt:**

```markdown
## Task

Produce a UAT brief for the human reviewer, summarizing what was built,
tested, and reviewed.

## Instructions

Load skill `compound-engineering` and use VerifyAndCompound → CaptureAndShare.

Generate a clear, actionable UAT brief containing:

1. **Summary of what was implemented** (from the plan)
2. **QA results** — what `qa-branch` tested, pass/fail counts, coverage
3. **Review findings** — what `review-diff-pass1` and `review-diff-pass2` found, any warnings
4. **Branch checkout instructions** — branch name and exact commands
5. **How to run locally** — exact commands to run the app and tests
6. **What to manually verify** — derived from the plan, specific user flows to check

## Params

- `plan_content`: {{ plan_content }}
- `branch_name`: {{ branch_name }}
- `worktree_path`: {{ worktree_path }}
- `qa_results`: {{ qa_results }}
- `review_findings`: {{ review_findings }}
- `files_changed`: {{ files_changed }}

## Output

Return the UAT brief as a structured JSON:
{
  "status": "pass",
  "brief_markdown": "<full UAT brief in markdown>",
  "checkout_command": "git checkout {{ branch_name }}",
  "test_commands": ["command1", "command2"],
  "manual_checks": ["check1", "check2"]
}
```

**After the brief is produced, the parent task durably waits for a human signal:**

```bash
# Human approves
absurdctl emit-event "uat-approved:<task-id>" --queue delivery-orchestrator -P approved=true

# Human rejects with feedback
absurdctl emit-event "uat-approved:<task-id>" --queue delivery-orchestrator -P approved=false -P feedback="description of issue"
```

**On rejection:** The parent replays steps 2-6 with `feedback` passed as the optional feedback param to `implement-from-plan`. The `retry_count` is incremented. Max 3 loops.

**On approval:** Proceed to Phase 3.

**Input params:**

| Param | Type | Source |
|---|---|---|
| `plan_content` | string | Original plan text |
| `branch_name` | string | From `create-branch` result |
| `worktree_path` | string | From `create-branch` result |
| `qa_results` | object | From `qa-branch` result |
| `review_findings` | object | From `review-diff-pass1` + `review-diff-pass2` results |
| `files_changed` | string[] | From `implement-from-plan` result |

**Output schema:**

```json
{
  "status": "pass",
  "brief_markdown": "string (full UAT brief in markdown)",
  "checkout_command": "string",
  "test_commands": ["string"],
  "manual_checks": ["string"]
}
```

---

### 8. `open-pull-request`

**Purpose:** Commit the work and open a pull request.

**Queue:** `delivery-ops`
**Agent:** `1-kimi`
**Skill:** compound-engineering → ExecuteWork → ManageDelivery (git-commit-push-pr)
**Absurd feature:** Checkpointed steps: step 1 commits (persists SHA), step 2 opens PR (persists URL).

**Prompt file:** `prompts/open-pull-request/v1.md`

**Prompt:**

```markdown
## Task

Commit all changes and open a pull request.

## Instructions

Load skill `compound-engineering` and use ExecuteWork → ManageDelivery.
Specifically, use the `git-commit-push-pr` sub-skill.

Work from: `{{ worktree_path }}`

Steps:
1. Stage all changes
2. Create a commit with a clear, value-communicating message
3. Push the branch to origin
4. Open a PR targeting `{{ base_branch }}` with:
   - Title derived from the plan
   - Body summarizing changes, test plan, and review results

Use the plan title and QA results to craft the PR description.

## Params

- `plan_title`: {{ plan_title }}
- `branch_name`: {{ branch_name }}
- `base_branch`: {{ base_branch }}
- `worktree_path`: {{ worktree_path }}
- `qa_results`: {{ qa_results }}
- `review_findings`: {{ review_findings }}
- `files_changed`: {{ files_changed }}

## Output

Return JSON:
{
  "status": "pass" | "fail",
  "commit_sha": "<SHA>",
  "pr_url": "<URL>",
  "pr_number": <number>
}
```

**Input params:**

| Param | Type | Source |
|---|---|---|
| `plan_title` | string | User-provided plan |
| `branch_name` | string | From `create-branch` result |
| `base_branch` | string | Defaults to `main` |
| `worktree_path` | string | From `create-branch` result |
| `qa_results` | object | From `qa-branch` result |
| `review_findings` | object | From `review-diff-pass1` + `review-diff-pass2` results |
| `files_changed` | string[] | From `implement-from-plan` result |

**Output schema:**

```json
{
  "status": "pass | fail",
  "commit_sha": "string",
  "pr_url": "string",
  "pr_number": "int"
}
```

---

### 9a. `request-greptile-review` (OPTIONAL — disabled by default)

**Purpose:** Request an external Greptile code review on the PR, then durably wait for results.

**Queue:** `delivery-ops`
**Agent:** `1-kimi`
**Skill:** gstack → review → greptile-triage
**Absurd feature:** Durable event wait (external async system).
**Activation flag:** `optional_tasks.greptile_review = true` in `prompt-config.toml`

**Prompt file:** `prompts/request-greptile-review/v1.md`

**Prompt:**

```markdown
## Task

Fetch and triage Greptile review comments on the pull request.

## Instructions

Load skill `gstack` and use the review → greptile-triage reference.

Follow the greptile-triage methodology:
1. Fetch Greptile comments (line-level and top-level)
2. Check suppressions history
3. Classify each comment: VALID & ACTIONABLE | VALID BUT ALREADY FIXED | FALSE POSITIVE | SUPPRESSED
4. Reply to each comment using the tiered templates
5. Write triage outcomes to history file

## Params

- `pr_number`: {{ pr_number }}
- `pr_url`: {{ pr_url }}

## Output

Return JSON:
{
  "status": "pass" | "warn" | "fail",
  "total_comments": <count>,
  "valid_actionable": <count>,
  "valid_fixed": <count>,
  "false_positives": <count>,
  "suppressed": <count>,
  "actionable_items": ["file:line — description"]
}
```

**Note:** If Greptile is not configured or returns no comments, the task completes with status `pass` and zero counts. This task is purely additive.

---

### 9b. `wait-for-ci` (OPTIONAL — disabled by default)

**Purpose:** Wait for CI pipeline to complete.

**Queue:** `delivery-ops`
**Agent:** none (pure ops script, no model needed)
**Skill:** none
**Absurd feature:** Durable sleep (poll CI status) or webhook event.
**Activation flag:** `optional_tasks.wait_for_ci = true` in `prompt-config.toml`

**No prompt file.** This is a code-only task.

**Implementation:**

```typescript
app.registerTask({ name: "wait-for-ci" }, async (params, ctx) => {
  // Poll CI status every 30 seconds using gh CLI
  while (true) {
    const ciStatus = await ctx.step(`ci-check-${Date.now()}`, async () => {
      const result = await exec(`gh pr checks ${params.pr_number} --json state`);
      return JSON.parse(result);
    });

    if (ciStatus.every(check => check.state === "SUCCESS")) {
      return { status: "pass", checks: ciStatus };
    }
    if (ciStatus.some(check => check.state === "FAILURE")) {
      return { status: "fail", checks: ciStatus };
    }

    await ctx.sleepFor("ci-poll", 30);
  }
});
```

**Alternative:** Use durable event wait if CI can send a webhook:

```typescript
const ciResult = await ctx.awaitEvent(`ci-complete:${params.pr_number}`, {
  stepName: "wait-for-ci",
  timeout: 3600, // 1 hour max
});
```

---

### 10. `merge-when-green` (OPTIONAL — disabled by default)

**Purpose:** Deterministic gate check — merge if all conditions are met.

**Queue:** `delivery-ops`
**Agent:** none (deterministic logic, no model needed)
**Skill:** none
**Absurd feature:** Deterministic gate check on 9a + 9b results.
**Activation flag:** `optional_tasks.auto_merge = true` in `prompt-config.toml`

**No prompt file.** This is a code-only task.

**Implementation:**

```typescript
app.registerTask({ name: "merge-when-green" }, async (params, ctx) => {
  const canMerge = await ctx.step("check-gates", async () => {
    const greptileOk = !params.greptile_result ||
      params.greptile_result.status !== "fail";
    const ciOk = !params.ci_result ||
      params.ci_result.status === "pass";
    return greptileOk && ciOk;
  });

  if (!canMerge) {
    return { status: "fail", reason: "Gate checks failed" };
  }

  const merged = await ctx.step("merge", async () => {
    await exec(`gh pr merge ${params.pr_number} --squash --auto`);
    return { merged: true };
  });

  return { status: "pass", merged: true, pr_number: params.pr_number };
});
```

---

## Prompt management

```
prompts/
  create-branch/
    v1.md
  implement-from-plan/
    v1.md
  run-lsp-and-lint/
    v1.md
  review-diff-pass1/
    v1.md
  review-diff-pass2/
    v1.md
  qa-branch/
    v1.md
  uat-handoff/
    v1.md
  open-pull-request/
    v1.md
  request-greptile-review/
    v1.md                     ← only used when optional task is activated
  orchestrator-gate/
    v1.md                     ← only loaded when a child returns status "warn"
prompt-config.toml
```

---

## `prompt-config.toml`

```toml
[defaults]
base_branch = "main"

# ──────────────────────────────────────────────
# Step → prompt version + agent mapping
# ──────────────────────────────────────────────

[steps.create-branch]
prompt = "prompts/create-branch/v1.md"
agent = "1-kimi"
queue = "delivery-ops"

[steps.implement-from-plan]
prompt = "prompts/implement-from-plan/v1.md"
agent = "2-opus"
queue = "delivery-build"
# Controller agent. May dispatch glm/1-kimi as subagent workers.

[steps.run-lsp-and-lint]
prompt = "prompts/run-lsp-and-lint/v1.md"
agent = "1-kimi"
queue = "delivery-review"

[steps.review-diff-pass1]
prompt = "prompts/review-diff-pass1/v1.md"
agent = "1-kimi"
queue = "delivery-review"

[steps.review-diff-pass2]
prompt = "prompts/review-diff-pass2/v1.md"
agent = "gpthigh"
queue = "delivery-review"

[steps.qa-branch]
prompt = "prompts/qa-branch/v1.md"
agent = "1-kimi"
queue = "delivery-review"

[steps.uat-handoff]
prompt = "prompts/uat-handoff/v1.md"
agent = "1-kimi"
queue = "delivery-ops"

[steps.open-pull-request]
prompt = "prompts/open-pull-request/v1.md"
agent = "1-kimi"
queue = "delivery-ops"

[steps.request-greptile-review]
prompt = "prompts/request-greptile-review/v1.md"
agent = "1-kimi"
queue = "delivery-ops"

# Orchestrator gate — loaded conditionally when a child returns status "warn"
[steps.orchestrator-gate]
prompt = "prompts/orchestrator-gate/v1.md"
agent = "1-kimi"
queue = "delivery-orchestrator"

# No prompt entries for wait-for-ci and merge-when-green (code-only tasks)

# ──────────────────────────────────────────────
# Optional tasks — disabled by default
# ──────────────────────────────────────────────

[optional_tasks]
greptile_review = false
wait_for_ci = false
auto_merge = false

# ──────────────────────────────────────────────
# Loop-back configuration
# ──────────────────────────────────────────────

[loopback]
max_retries = 3
# Steps replayed on failure: implement → lint → review-pass1 → review-pass2 → qa
replay_steps = ["implement-from-plan", "run-lsp-and-lint", "review-diff-pass1", "review-diff-pass2", "qa-branch"]
```

---

## Loop-back mechanics

### How feedback flows

When `review-diff-pass1`, `review-diff-pass2`, or `uat-handoff` rejects the implementation, the parent orchestrator replays steps 2-6 with feedback injected.

```
review-diff-pass1 or review-diff-pass2 fails
  → parent reads the failing task's result.feedback_for_retry
  → parent increments retry_count (0 → 1 → 2 → max 3)
  → parent spawns implement-from-plan with:
      params.feedback = <failing review>.result.feedback_for_retry
      params.retry_count = <incremented>
  → implement-from-plan prompt renders the "Prior feedback" section
  → pipeline continues: lint → review-pass1 → review-pass2 → qa

uat-handoff rejected
  → human emits event with feedback="description of issue"
  → parent reads event payload
  → parent spawns implement-from-plan with:
      params.feedback = event.feedback
      params.retry_count = <incremented>
  → pipeline continues: implement → lint → review-pass1 → review-pass2 → qa → uat-handoff (re-enters gate)
```

### Same prompt, optional field

The `implement-from-plan`, `review-diff-pass1`, and `review-diff-pass2` prompts use conditional sections:

```markdown
{{ #if feedback }}
## Prior feedback (retry cycle {{ retry_count }}/3)

The previous implementation was rejected. Address this feedback:

{{ feedback }}
{{ /if }}
```

On first run, `feedback` is null/empty and the section is not rendered. On retry, the feedback from the review or UAT is injected.

### Max retries

After 3 failed loops, the parent fails the workflow:

```json
{
  "status": "fail",
  "reason": "Maximum retry count (3) exceeded",
  "last_feedback": "<feedback from last review/UAT>",
  "retry_history": [
    { "cycle": 1, "source": "review-diff-pass2", "feedback": "..." },
    { "cycle": 2, "source": "review-diff-pass1", "feedback": "..." },
    { "cycle": 3, "source": "uat-handoff", "feedback": "..." }
  ]
}
```

---

## UAT human interaction

### The human experience

1. Workflow reaches step 7 (`uat-handoff`)
2. The UAT brief is produced and displayed (console, Habitat dashboard, or notification)
3. The workflow **sleeps** — no worker, no poller, no resources consumed
4. The human reviews:
   - Reads the brief
   - Checks out the branch locally
   - Runs the app
   - Verifies manually
5. The human signals:

```bash
# Approve — workflow advances to Phase 3
absurdctl emit-event "uat-approved:<task-id>" \
  --queue delivery-orchestrator \
  -P approved=true

# Reject with feedback — workflow loops back to step 2
absurdctl emit-event "uat-approved:<task-id>" \
  --queue delivery-orchestrator \
  -P approved=false \
  -P feedback="The login form doesn't validate email format. Also the loading spinner is missing on the submit button."
```

The feedback field is free-text. The human writes whatever they observed. This becomes the `feedback` param in the next `implement-from-plan` run.

---

## Execution via OpenCode

Each child task that requires a model runs via headless OpenCode:

```bash
# General pattern
opencode run --agent <agent> "<rendered prompt>"

# Example: create-branch
opencode run --agent 1-kimi "$(cat prompts/create-branch/v1.md | render_template)"

# Example: implement-from-plan (with feedback on retry)
opencode run --agent 2-opus "$(cat prompts/implement-from-plan/v1.md | render_template --feedback='fix the email validation' --retry_count=1)"

# Example: review-diff-pass1
opencode run --agent 1-kimi "$(cat prompts/review-diff-pass1/v1.md | render_template)"

# Example: review-diff-pass2 (receives pass1 findings)
opencode run --agent gpthigh "$(cat prompts/review-diff-pass2/v1.md | render_template --pass1_criteria='...')"
```

The `render_template` function is application code that:
1. Reads the prompt file
2. Resolves `{{ param }}` placeholders from task params
3. Handles conditional `{{ #if }}` blocks
4. Returns the rendered prompt string

---

## Durability points

| Scenario | What Absurd does |
|---|---|
| Worker dies mid-implementation | Resumes from last checkpointed TDD slice, not from zero |
| Greptile/CI waits | Durable sleep or event wait — no long-lived in-memory poller |
| Review/UAT rejects implementation | Parent loops back with feedback, execution history preserved |
| Parent exhausts 3 retries | Workflow fails cleanly with full retry history |
| Merge fails due to conflicts | Workflow fails cleanly — no automatic rebase |
| Human takes hours to UAT | Workflow sleeps in Postgres — zero resource consumption |

---

## What Absurd owns vs what you own

**Absurd owns:**
- Queues, tasks, steps, checkpoints, retries, events, sleeps
- Durable execution and crash recovery
- Task result persistence and forwarding

**You own:**
- Prompts (versioned markdown files in `prompts/`)
- Model selection (`prompt-config.toml` → agent mapping)
- Calling the model (`opencode run --agent <name> "<prompt>"`)
- Template rendering (resolving params into prompts)
- Optional task activation flags
- Orchestrator hybrid gate logic (deterministic for pass/fail, model for warn)
