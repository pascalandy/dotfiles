# Requesting Code Review

> Dispatch a code-reviewer subagent to catch issues before they cascade, giving it precisely crafted context — never your session history.

## When to Use

**Mandatory:**
- After each task in subagent-driven development
- After completing a major feature
- Before merging to main

**Optional but valuable:**
- When stuck (fresh perspective)
- Before refactoring (baseline check)
- After fixing a complex bug

## Inputs

- `{WHAT_WAS_IMPLEMENTED}` — What you just built
- `{PLAN_OR_REQUIREMENTS}` — What it should do (plan file or requirements text)
- `{BASE_SHA}` — Starting commit SHA
- `{HEAD_SHA}` — Ending commit SHA
- `{DESCRIPTION}` — Brief summary of what was implemented

## Methodology

### Step 1: Get Git SHAs

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
```

For subagent-driven development, capture the SHA before each task begins so you can pass an accurate range.

### Step 2: Dispatch Code-Reviewer Subagent

Delegate to a code-reviewer subagent using the full prompt template below. Fill all placeholders before dispatching.

**Complete subagent prompt template:**

```
You are reviewing code changes for production readiness.

Your task:
1. Review {WHAT_WAS_IMPLEMENTED}
2. Compare against {PLAN_OR_REQUIREMENTS}
3. Check code quality, architecture, testing
4. Categorize issues by severity
5. Assess production readiness

## What Was Implemented

{DESCRIPTION}

## Requirements/Plan

{PLAN_REFERENCE}

## Git Range to Review

Base: {BASE_SHA}
Head: {HEAD_SHA}

  git diff --stat {BASE_SHA}..{HEAD_SHA}
  git diff {BASE_SHA}..{HEAD_SHA}

## Review Checklist

**Code Quality:**
- Clean separation of concerns?
- Proper error handling?
- Type safety (if applicable)?
- DRY principle followed?
- Edge cases handled?

**Architecture:**
- Sound design decisions?
- Scalability considerations?
- Performance implications?
- Security concerns?

**Testing:**
- Tests actually test logic (not mocks)?
- Edge cases covered?
- Integration tests where needed?
- All tests passing?

**Requirements:**
- All plan requirements met?
- Implementation matches spec?
- No scope creep?
- Breaking changes documented?

**Production Readiness:**
- Migration strategy (if schema changes)?
- Backward compatibility considered?
- Documentation complete?
- No obvious bugs?

## Output Format

### Strengths
[What's well done? Be specific.]

### Issues

#### Critical (Must Fix)
[Bugs, security issues, data loss risks, broken functionality]

#### Important (Should Fix)
[Architecture problems, missing features, poor error handling, test gaps]

#### Minor (Nice to Have)
[Code style, optimization opportunities, documentation improvements]

For each issue:
- File:line reference
- What's wrong
- Why it matters
- How to fix (if not obvious)

### Recommendations
[Improvements for code quality, architecture, or process]

### Assessment

**Ready to merge?** [Yes/No/With fixes]

**Reasoning:** [Technical assessment in 1-2 sentences]

## Critical Rules

DO:
- Categorize by actual severity (not everything is Critical)
- Be specific (file:line, not vague)
- Explain WHY issues matter
- Acknowledge strengths
- Give clear verdict

DON'T:
- Say "looks good" without checking
- Mark nitpicks as Critical
- Give feedback on code you didn't review
- Be vague ("improve error handling")
- Avoid giving a clear verdict
```

### Example Workflow

```
[Just completed Task 2: Add verification function]

Capture SHAs:
  BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | awk '{print $1}')
  # e.g., a7981ec
  HEAD_SHA=$(git rev-parse HEAD)
  # e.g., 3df7661

[Dispatch code-reviewer subagent with filled template]
  WHAT_WAS_IMPLEMENTED: Verification and repair functions for conversation index
  PLAN_OR_REQUIREMENTS: Task 2 from docs/plans/deployment-plan.md
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661
  DESCRIPTION: Added verifyIndex() and repairIndex() with 4 issue types

[Reviewer returns]:
  Strengths:
    - Clean separation of concerns
    - Real tests, not mock tests
  Issues:
    Important: Missing progress indicators for long-running repair
    Minor: Magic number (100) for reporting interval
  Assessment: Ready to proceed with fixes

[Fix Important issue: add progress indicators]
[Note Minor for later]
[Continue to Task 3]
```

### Step 3: Act on Feedback

| Severity | Action |
|----------|--------|
| Critical | Fix immediately before doing anything else |
| Important | Fix before proceeding to next task |
| Minor | Note for later |
| Reviewer is wrong | Push back with technical reasoning; show code/tests that prove it works |

## Quality Gates

**Never:**
- Skip review because "it's simple"
- Ignore Critical issues
- Proceed with unfixed Important issues
- Argue with valid technical feedback without evidence

**If reviewer is wrong:**
- Provide technical reasoning
- Show code/tests that prove correct behavior
- Request clarification

## Outputs

A structured review report containing:
- **Strengths** — specific, file-referenced positive findings
- **Issues** — categorized Critical / Important / Minor with file:line, explanation, and fix guidance
- **Recommendations** — process or quality improvements
- **Assessment** — merge readiness verdict with one-sentence reasoning

## Feeds Into

- **subagent-driven-development** — reviews gate every task completion
- **finishing-a-development-branch** — final review before branch close

## Harness Notes

The reviewer subagent must receive explicitly constructed context (placeholders filled). Never forward your session history to it. The reviewer runs `git diff {BASE_SHA}..{HEAD_SHA}` independently to read the actual code.
