# TriageIssue

Investigate a reported problem, find its root cause by exploring the codebase, and create a GitHub issue with a TDD fix plan. This is a mostly hands-off workflow -- minimize questions to the user.

## Process

### 1. Capture the Problem

Get a brief description from the user. If they haven't provided one, ask ONE question: "What's the problem you're seeing?" Do NOT ask follow-up questions yet. Start investigating immediately.

### 2. Explore and Diagnose

Explore the codebase to find:
- Where the bug manifests
- What code path leads to the failure
- Why it fails (the root cause, not just the symptom)
- Related code that might be affected

Look at: source files, existing tests, recent changes to affected areas (`git log`), error handling in the code path, similar patterns elsewhere in the codebase that work correctly.

### 3. Identify the Fix Approach

Determine:
- The minimal change needed
- Which modules and interfaces are affected
- Which behaviors need to be verified
- Whether this is a regression, a missing feature, or a design flaw

### 4. Design TDD Fix Plan

Create an ordered list of RED-GREEN cycles (vertical slices):

For each cycle:
- **RED:** Describe the test that captures the broken or missing behavior
- **GREEN:** Describe the minimal code change to make it pass

Rules:
- Test through public interfaces, not implementation details
- One cycle at a time
- Tests must survive future refactors
- Include a final REFACTOR step if needed
- Only suggest fixes that would survive radical codebase changes
- Describe behaviors and contracts, not internal structure
- Tests assert on observable outcomes (API responses, UI state, user-visible effects), not internal state
- A good suggestion reads like a spec; a bad one reads like a diff

### 5. Create the GitHub Issue

Do NOT ask the user to review before creating -- just create it and share the URL. Use `gh issue create`:

```markdown
## Problem
**Actual behavior:** [what happens now]
**Expected behavior:** [what should happen]
**How to reproduce:** [steps]

## Root Cause Analysis
[What code path leads to the failure]
[Why it fails -- describe by module responsibility, not file path]
[Do NOT include specific file paths, line numbers, or implementation details that couple to current code layout. Describe modules, behaviors, and contracts instead. The issue should remain useful even after major refactors.]

## TDD Fix Plan
1. **RED:** Write test for [broken behavior] -- should fail
   **GREEN:** [Minimal change to pass]

2. **RED:** Write test for [edge case] -- should fail
   **GREEN:** [Minimal change to pass]

3. **REFACTOR:** [If needed -- what to clean up]

## Acceptance Criteria
- [ ] [Concrete, testable criterion]
- [ ] All new tests pass
- [ ] Existing tests still pass
- [ ] No regression in related behavior
```

Print the issue URL and a one-line root cause summary.
