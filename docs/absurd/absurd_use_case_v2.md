# Absurd Use Case v2: End-to-End Development Workflow — Full Spec

## Goal

Model a common software-delivery path as a durable, resumable workflow in Absurd: plan to implementation to review to merge. This document is the bonified spec for building the actual workflow — it defines every prompt, skill, agent, and Absurd primitive needed.

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
  delivery-review         ← run-lsp-and-lint, review-diff, qa-branch
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

### Orchestrator design

**Option C: Hybrid (recommended)**
- Deterministic gates for clear results: `status == "pass"` → proceed, `status == "fail"` → loop back
- Model invoked only when `status == "warn"` or result is ambiguous
- The orchestrator prompt is loaded conditionally — only for ambiguous gates
- Pro: Fast for the common case, smart for edge cases
- Con: Slightly more complex to implement

**Recommendation:** Option C. Most child tasks produce clear pass/fail. The model is only needed when `review-diff` returns warnings or `qa-branch` has partial failures.

### Loop-back rules

- On `review-diff` failure or UAT rejection: replay steps 2-5 (implement → lint → review → qa)
- The replay passes the failure feedback as an optional param to `implement-from-plan`
- Maximum 3 loop iterations per feedback cycle
- After 3 failures: parent fails the workflow with a clear error message

### Result forwarding

The parent collects each child's result JSON and passes relevant fields forward:

```
create-branch.result.branch_name → implement-from-plan.params.branch_name
implement-from-plan.result.files_changed → review-diff.params.files_changed
qa-branch.result.test_summary → uat-handoff.params.test_summary
review-diff.result.findings → uat-handoff.params.review_findings
```

---

## Execution flow

### Phase 1 — Automated build

| Order | Child task | Queue | Agent | Skill | Sub-skill |
|---|---|---|---|---|---|
| 1 | `create-branch` | `delivery-ops` | `1-kimi` | superpowers | `>worktree` |
| 2 | `implement-from-plan` | `delivery-build` | `gpthigh` (controller) | superpowers | `>subagent-dev` |
| 3 | `run-lsp-and-lint` | `delivery-review` | `1-kimi` | superpowers | `>verify` |
| 4 | `review-diff` | `delivery-review` | `1-kimi` then `gpthigh` | superpowers | `>request-review` (two-pass) |
| 5 | `qa-branch` | `delivery-review` | `1-kimi` | superpowers | `>verify` + `>tdd` |

### Phase 2 — User UAT gate

| Order | Child task | Queue | Agent | Skill | Sub-skill |
|---|---|---|---|---|---|
| 6 | `uat-handoff` | `delivery-ops` | `1-kimi` | compound-engineering | VerifyAndCompound → CaptureAndShare |

### Phase 3 — Automated delivery (optional tasks marked)

| Order | Child task | Queue | Agent | Skill | Sub-skill | Optional |
|---|---|---|---|---|---|---|
| 7 | `open-pull-request` | `delivery-ops` | `1-kimi` | compound-engineering | ExecuteWork → ManageDelivery | no |
| 8a | `request-greptile-review` | `delivery-ops` | `1-kimi` | gstack | review → greptile-triage | **yes** |
| 8b | `wait-for-ci` | `delivery-ops` | none | — (pure ops script) | — | **yes** |
| 9 | `merge-when-green` | `delivery-ops` | none | — (deterministic gate) | — | **yes** |

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

**Purpose:** Implement the plan with TDD discipline. Includes internal self-review per the subagent-dev methodology, but defers formal code review to `review-diff`.

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
by the separate `review-diff` task downstream.

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
| `feedback` | string? | Optional. From `review-diff` or `uat-handoff` on retry |
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

### 4. `review-diff`

**Purpose:** Two-pass code review. First pass with `1-kimi` (fast, catches obvious issues). Second pass with `gpthigh` (different reasoning perspective, catches what the first missed).

**Queue:** `delivery-review`
**Agent:** `1-kimi` (pass 1), then `gpthigh` (pass 2) — sequential within one Absurd task
**Skill:** superpowers → `>request-review` (requesting-code-review)
**Absurd feature:** Task result drives pass/fail gate. On failure, parent replays steps 2-5 with review feedback (max 3 loops).

**Prompt file:** `prompts/review-diff/v1.md`

**Prompt:**

```markdown
## Task

Run a two-pass code review on the implementation diff.

## Instructions

Load skill `superpowers` and use sub-skill `>request-review`.

This review runs in two sequential passes:

### Pass 1 (agent: 1-kimi)

Fast review for obvious issues:
- Spec compliance: does the diff match the plan?
- Code quality: clean separation, error handling, type safety
- Test coverage: tests verify behavior, not mocks
- Security: no obvious vulnerabilities

Use git range: `{{ base_sha }}..{{ head_sha }}`

### Pass 2 (agent: gpthigh)

Deep review from a different reasoning perspective:
- Architecture: sound design decisions, scalability
- Edge cases: what the first pass missed
- Production readiness: migration safety, backward compatibility
- Subtle bugs: race conditions, state management

Use the same git range. The second reviewer receives pass 1 findings to avoid
duplicate reporting.

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
  "pass1_findings": {
    "critical": ["file:line — description"],
    "important": ["file:line — description"],
    "minor": ["file:line — description"]
  },
  "pass2_findings": {
    "critical": ["file:line — description"],
    "important": ["file:line — description"],
    "minor": ["file:line — description"]
  },
  "combined_assessment": "Ready to merge | Fix critical issues | Needs rework",
  "feedback_for_retry": "string (populated when status is fail)"
}
```

**Gate logic:**
- `status == "pass"` → proceed to `qa-branch`
- `status == "warn"` → if orchestrator is Option C, invoke model to decide; otherwise proceed
- `status == "fail"` → parent loops back to step 2 with `feedback_for_retry` as the feedback param

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
  "pass1_findings": {
    "critical": ["string"],
    "important": ["string"],
    "minor": ["string"]
  },
  "pass2_findings": {
    "critical": ["string"],
    "important": ["string"],
    "minor": ["string"]
  },
  "combined_assessment": "string",
  "feedback_for_retry": "string"
}
```

---

### 5. `qa-branch`

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
  "status": "pass" | "fail",
  "tests_run": <count>,
  "tests_passed": <count>,
  "tests_failed": <count>,
  "test_failures": ["test name — error"],
  "coverage_percentage": <number>,
  "coverage_gaps": ["description of untested path"],
  "plan_items_verified": <count>,
  "plan_items_total": <count>
}
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
  "status": "pass | fail",
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

### 6. `uat-handoff`

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
3. **Review findings** — what `review-diff` found, any warnings
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
absurdctl emit-event "uat-approved:<task-id>" -q delivery-orchestrator -P approved=true

# Human rejects with feedback
absurdctl emit-event "uat-approved:<task-id>" -q delivery-orchestrator -P approved=false -P feedback="description of issue"
```

**On rejection:** The parent replays steps 2-5 with `feedback` passed as the optional feedback param to `implement-from-plan`. The `retry_count` is incremented. Max 3 loops.

**On approval:** Proceed to Phase 3.

**Input params:**

| Param | Type | Source |
|---|---|---|
| `plan_content` | string | Original plan text |
| `branch_name` | string | From `create-branch` result |
| `worktree_path` | string | From `create-branch` result |
| `qa_results` | object | From `qa-branch` result |
| `review_findings` | object | From `review-diff` result |
| `files_changed` | string[] | From `implement-from-plan` result |

---

### 7. `open-pull-request`

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
| `review_findings` | object | From `review-diff` result |
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

### 8a. `request-greptile-review` (OPTIONAL — disabled by default)

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

### 8b. `wait-for-ci` (OPTIONAL — disabled by default)

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

### 9. `merge-when-green` (OPTIONAL — disabled by default)

**Purpose:** Deterministic gate check — merge if all conditions are met.

**Queue:** `delivery-ops`
**Agent:** none (deterministic logic, no model needed)
**Skill:** none
**Absurd feature:** Deterministic gate check on 8a + 8b results.
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
  review-diff/
    v1.md
  qa-branch/
    v1.md
  uat-handoff/
    v1.md
  open-pull-request/
    v1.md
  request-greptile-review/
    v1.md                     ← only used when optional task is activated
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

[steps.review-diff]
prompt = "prompts/review-diff/v1.md"
agent = ["1-kimi", "gpthigh"]    # Sequential two-pass
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
# Steps replayed on failure: implement-from-plan → run-lsp-and-lint → review-diff → qa-branch
replay_steps = ["implement-from-plan", "run-lsp-and-lint", "review-diff", "qa-branch"]
```

---

## Loop-back mechanics

### How feedback flows

When `review-diff` or `uat-handoff` rejects the implementation, the parent orchestrator replays steps 2-5 with feedback injected.

```
review-diff fails
  → parent reads review-diff.result.feedback_for_retry
  → parent increments retry_count (0 → 1 → 2 → max 3)
  → parent spawns implement-from-plan with:
      params.feedback = review-diff.result.feedback_for_retry
      params.retry_count = <incremented>
  → implement-from-plan prompt renders the "Prior feedback" section
  → pipeline continues: lint → review → qa

uat-handoff rejected
  → human emits event with feedback="description of issue"
  → parent reads event payload
  → parent spawns implement-from-plan with:
      params.feedback = event.feedback
      params.retry_count = <incremented>
  → pipeline continues: implement → lint → review → qa → uat-handoff (re-enters gate)
```

### Same prompt, optional field

The `implement-from-plan` and `review-diff` prompts use conditional sections:

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
    { "cycle": 1, "source": "review-diff", "feedback": "..." },
    { "cycle": 2, "source": "review-diff", "feedback": "..." },
    { "cycle": 3, "source": "uat-handoff", "feedback": "..." }
  ]
}
```

---

## UAT human interaction

### The human experience

1. Workflow reaches step 6 (`uat-handoff`)
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
  -q delivery-orchestrator \
  -P approved=true

# Reject with feedback — workflow loops back to step 2
absurdctl emit-event "uat-approved:<task-id>" \
  -q delivery-orchestrator \
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
opencode run --agent gpthigh "$(cat prompts/implement-from-plan/v1.md | render_template --feedback='fix the email validation' --retry_count=1)"

# Example: review-diff pass 1
opencode run --agent 1-kimi "$(cat prompts/review-diff/v1.md | render_template --pass=1)"

# Example: review-diff pass 2
opencode run --agent gpthigh "$(cat prompts/review-diff/v1.md | render_template --pass=2 --pass1_findings='...')"
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
- Orchestrator gate logic (Option A, B, or C)
