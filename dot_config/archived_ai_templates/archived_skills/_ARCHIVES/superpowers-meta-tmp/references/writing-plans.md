# Writing Plans

> Write comprehensive implementation plans — before touching code — with bite-sized TDD tasks, exact file paths, complete code, and execution options.

## When to Use

- You have a spec or requirements for a multi-step task
- Before touching any code
- In a dedicated worktree (created by brainstorming skill)

## Inputs

- A completed spec or requirements document
- Understanding of the codebase structure (or ability to explore it)
- Save location: `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` (user preference overrides)

## Methodology

### Announce

At start: `"I'm using the writing-plans skill to create the implementation plan."`

### Step 1: Scope Check

If the spec covers multiple independent subsystems, it should have been broken into sub-project specs during brainstorming. If it wasn't, suggest breaking into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

### Step 2: File Structure Mapping

Before defining tasks, map out which files will be created or modified and what each is responsible for. Lock in decomposition decisions here.

Rules:
- Design units with clear boundaries and well-defined interfaces
- Each file should have one clear responsibility
- Prefer smaller, focused files over large ones
- Files that change together should live together — split by responsibility, not technical layer
- In existing codebases, follow established patterns; only include restructuring if a file has grown unwieldy
- This structure informs task decomposition — each task should produce self-contained changes

### Step 3: Write the Plan Document

#### Required Header (every plan MUST start with this)

```markdown
# [Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

#### Task Structure Template

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

- [ ] **Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

- [ ] **Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

#### Bite-Sized Task Granularity

Each step is one action (2-5 minutes):
- "Write the failing test" — step
- "Run it to make sure it fails" — step
- "Implement the minimal code to make the test pass" — step
- "Run the tests and make sure they pass" — step
- "Commit" — step

#### No Placeholders Rule

**Plan failures** — never write these:
- "TBD", "TODO", "implement later", "fill in details"
- "Add appropriate error handling" / "add validation" / "handle edge cases"
- "Write tests for the above" (without actual test code)
- "Similar to Task N" (repeat the code — the engineer may be reading tasks out of order)
- Steps that describe what to do without showing how (code blocks required for code steps)
- References to types, functions, or methods not defined in any task

#### Requirements

- Exact file paths always
- Complete code in every step — if a step changes code, show the code
- Exact commands with expected output
- DRY, YAGNI, TDD, frequent commits

### Step 4: Self-Review

After writing the complete plan, check it with fresh eyes. This is a checklist run yourself — not delegated to a subagent.

**1. Spec coverage:** Skim each section/requirement in the spec. Can you point to a task that implements it? List any gaps.

**2. Placeholder scan:** Search the plan for red flags — any patterns from the "No Placeholders" section above. Fix them.

**3. Type consistency:** Do the types, method signatures, and property names used in later tasks match what was defined in earlier tasks? (e.g., `clearLayers()` in Task 3 but `clearFullLayers()` in Task 7 is a bug.)

If you find issues, fix them inline. If you find a spec requirement with no task, add the task.

### Step 5: Optional — Plan Document Review (Subagent)

Optionally delegate a plan document review subagent after the complete plan is written.

**Subagent prompt template:**

```
You are a plan document reviewer. Verify this plan is complete and ready for implementation.

**Plan to review:** [PLAN_FILE_PATH]
**Spec for reference:** [SPEC_FILE_PATH]

## What to Check

| Category | What to Look For |
|----------|------------------|
| Completeness | TODOs, placeholders, incomplete tasks, missing steps |
| Spec Alignment | Plan covers spec requirements, no major scope creep |
| Task Decomposition | Tasks have clear boundaries, steps are actionable |
| Buildability | Could an engineer follow this plan without getting stuck? |

## Calibration

**Only flag issues that would cause real problems during implementation.**
An implementer building the wrong thing or getting stuck is an issue.
Minor wording, stylistic preferences, and "nice to have" suggestions are not.

Approve unless there are serious gaps — missing requirements from the spec,
contradictory steps, placeholder content, or tasks so vague they can't be acted on.

## Output Format

## Plan Review

**Status:** Approved | Issues Found

**Issues (if any):**
- [Task X, Step Y]: [specific issue] - [why it matters for implementation]

**Recommendations (advisory, do not block approval):**
- [suggestions for improvement]
```

**Reviewer returns:** Status, Issues (if any), Recommendations.

### Step 6: Execution Handoff

After saving the plan, offer execution choice:

> **"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**
>
> **1. Subagent-Driven (recommended)** — Dispatch a fresh subagent per task, review between tasks, fast iteration
>
> **2. Inline Execution** — Execute tasks in this session using executing-plans, batch execution with checkpoints
>
> **Which approach?"**

**If Subagent-Driven chosen:**
- REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development`
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**
- REQUIRED SUB-SKILL: Use `superpowers:executing-plans`
- Batch execution with checkpoints for review

## Quality Gates

- [ ] Scope check performed (multiple subsystems → separate plans)
- [ ] File structure mapped before tasks defined
- [ ] Plan header present and complete
- [ ] Every task has exact file paths
- [ ] Every code step has actual code (no placeholders)
- [ ] Every command has expected output
- [ ] TDD cycle explicit in every task (failing test → pass → commit)
- [ ] Spec coverage verified — all requirements have tasks
- [ ] Placeholder scan clean
- [ ] Type consistency verified across tasks
- [ ] Execution handoff offered

## Outputs

- `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md` containing full implementation plan
- Execution path chosen (subagent-driven or inline)

## Feeds Into

- `superpowers:subagent-driven-development` (recommended execution path)
- `superpowers:executing-plans` (inline execution path)

## Harness Notes

Plans are saved as markdown files to the repo. The plan header instructs future agentic workers which execution skill to use — preserve it exactly.
