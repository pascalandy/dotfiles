# Testing Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Confidence through verification.                          │
│   Generate, execute, analyze — all in parallel.             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **AGENT REMINDER**: Only use `@ben`, `@abby`, or `@oracle`.
> See [SKILL.md](../../SKILL.md) for costs and task mapping.
> In examples below, "Agent A/B/C" = parallel `@abby` tasks for implementation or `@ben` for exploration.

> **Load when**: Test generation, test execution, coverage analysis, test maintenance, E2E testing
> **Common patterns**: Coverage-Driven Generation, Parallel Test Suites, Broken Test Triage

## Table of Contents

1. [Test Generation](#test-generation)
2. [Test Execution](#test-execution)
3. [Coverage Analysis](#coverage-analysis)
4. [Test Maintenance](#test-maintenance)
5. [E2E Testing](#e2e-testing)

---

## Test Generation

### Pattern: Coverage-Driven Generation

```
User Request: "Add tests for the UserService"

Phase 1: EXPLORE
└─ @ben: Understand UserService methods, dependencies

Phase 2: FAN-OUT (Parallel test writing - @ben tasks)
├─ @ben: Unit tests for method group 1
├─ @ben: Unit tests for method group 2
├─ @ben: Integration tests for external dependencies
└─ @ben: Edge cases and error scenarios

Phase 3: PIPELINE
└─ @abby: Verify tests pass, check coverage
```

### Pattern: Behavior-First

```
User Request: "Test the checkout flow"

Phase 1: EXPLORE
└─ @ben: Map checkout flow steps and branches

Phase 2: PIPELINE (Generate by behavior)
├─ @abby: Happy path tests
├─ @abby: Error path tests
└─ @abby: Edge case tests

Phase 3: BACKGROUND
└─ @ben: Run tests, report results
```

### Pattern: Contract Testing

```
User Request: "Add API contract tests"

Phase 1: EXPLORE
└─ @ben: Document API endpoints and schemas

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Request validation tests
├─ @ben: Response schema tests
└─ @ben: Error response tests

Phase 3: PIPELINE
└─ @abby: Integrate with CI, add OpenAPI validation
```

---

## Test Execution

### Pattern: Parallel Test Suites

```
User Request: "Run all tests"

Phase 1: FAN-OUT (Parallel suites)
├─ @ben: Unit tests
├─ @ben: Integration tests
├─ @ben: E2E tests
└─ @ben: Performance tests

Phase 2: REDUCE
└─ @abby: Aggregate results, identify failures
```

### Pattern: Targeted Execution

```
User Request: "Test the changes I made"

Phase 1: EXPLORE
└─ @ben: Identify changed files and affected tests

Phase 2: FAN-OUT
├─ @ben: Run directly affected tests
└─ @ben: Run dependent module tests

Phase 3: PIPELINE
└─ @abby: Report results, suggest additional tests
```

### Pattern: Flaky Test Detection

```
Phase 1: BACKGROUND (Multiple runs)
├─ @ben: Run test suite (run 1)
├─ @ben: Run test suite (run 2)
└─ @ben: Run test suite (run 3)

Phase 2: REDUCE
└─ @abby: Compare results, identify inconsistencies
```

---

## Coverage Analysis

### Pattern: Gap Identification

```
User Request: "Improve test coverage"

Phase 1: BACKGROUND
└─ @ben: Run coverage report

Phase 2: EXPLORE
└─ @ben: Identify critical uncovered paths

Phase 3: FAN-OUT (Prioritized gap filling - @ben tasks)
├─ @ben: Tests for critical uncovered module 1
├─ @ben: Tests for critical uncovered module 2
└─ @ben: Tests for error handlers

Phase 4: PIPELINE
└─ @abby: Re-run coverage, verify improvement
```

### Pattern: Risk-Based Coverage

```
Phase 1: EXPLORE
└─ @ben: Identify high-risk code (complexity, change frequency)

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Analyze coverage of high-risk area 1
├─ @ben: Analyze coverage of high-risk area 2
└─ @ben: Analyze coverage of high-risk area 3

Phase 3: REDUCE
└─ @abby: Prioritized test improvement plan
```

---

## Test Maintenance

### Pattern: Broken Test Triage

```
User Request: "Fix failing tests"

Phase 1: BACKGROUND
└─ @ben: Run tests, capture failures

Phase 2: FAN-OUT (Parallel diagnosis - @ben tasks)
├─ @ben: Diagnose failure group 1
├─ @ben: Diagnose failure group 2
└─ @ben: Diagnose failure group 3

Phase 3: FAN-OUT (Parallel fixes - @ben tasks)
├─ @ben: Fix test group 1
├─ @ben: Fix test group 2
└─ @ben: Fix test group 3

Phase 4: PIPELINE
└─ @ben: Verify all tests pass
```

### Pattern: Test Refactoring

```
User Request: "Clean up test duplication"

Phase 1: EXPLORE
└─ @ben: Find duplicate test patterns

Phase 2: PLAN
└─ @abby: Design shared fixtures, helpers, patterns

Phase 3: FAN-OUT (parallel @ben tasks)
├─ @ben: Extract shared fixtures
├─ @ben: Refactor test file group 1
└─ @ben: Refactor test file group 2

Phase 4: PIPELINE
└─ @ben: Verify tests still pass
```

### Pattern: Mock Maintenance

```
Phase 1: EXPLORE
└─ @ben: Find outdated mocks (API changes, schema changes)

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Update mock group 1
├─ @ben: Update mock group 2
└─ @ben: Update fixtures and factories

Phase 3: PIPELINE
└─ @ben: Run affected tests
```

---

## E2E Testing

### Pattern: User Journey Testing

```
User Request: "Add E2E tests for user registration"

Phase 1: EXPLORE
└─ @ben: Map registration flow, identify test scenarios

Phase 2: PIPELINE (Sequential scenarios)
├─ @abby: Happy path registration
├─ @abby: Validation error scenarios
├─ @abby: Duplicate email handling
└─ @abby: Email verification flow

Phase 3: BACKGROUND
└─ @ben: Run E2E suite, capture screenshots
```

### Pattern: Cross-Browser Testing

```
Phase 1: FAN-OUT (Parallel browsers)
├─ @ben: Run E2E in Chrome
├─ @ben: Run E2E in Firefox
├─ @ben: Run E2E in Safari
└─ @ben: Run E2E in Edge

Phase 2: REDUCE
└─ @abby: Browser compatibility report
```

### Pattern: Visual Regression

```
Phase 1: BACKGROUND
└─ @ben: Run visual regression tests

Phase 2: EXPLORE (If failures)
└─ @ben: Compare screenshots, identify changes

Phase 3: PIPELINE
└─ @abby: Categorize as bugs vs intentional changes
```

---

## Task Management for Testing

Structure testing work as tasks with clear dependencies:

```python
# Create testing tasks
TaskCreate(subject="Identify testing scope", description="Analyze what needs testing...")
TaskCreate(subject="Generate unit tests", description="Tests for module A...")
TaskCreate(subject="Generate integration tests", description="Tests for API endpoints...")
TaskCreate(subject="Run test suite", description="Execute all tests, capture results...")
TaskCreate(subject="Fix failures", description="Address any failing tests...")
TaskCreate(subject="Verify all pass", description="Final test run to confirm...")

# Dependencies
TaskUpdate(taskId="2", addBlockedBy=["1"])
TaskUpdate(taskId="3", addBlockedBy=["1"])
TaskUpdate(taskId="4", addBlockedBy=["2", "3"])
TaskUpdate(taskId="5", addBlockedBy=["4"])
TaskUpdate(taskId="6", addBlockedBy=["5"])

# Parallel test generation
Task(subagent_type="@abby", prompt="TaskId 2: Generate unit tests...")
Task(subagent_type="@abby", prompt="TaskId 3: Generate integration tests...")
```

## Test Execution Best Practices

1. **Always run in background** for long test suites
2. **Parallelize independent suites** (unit, integration, e2e)
3. **Fail fast** - stop on first failure for quick feedback
4. **Capture artifacts** - screenshots, logs, coverage reports
5. **Report actionable results** - file:line for failures

---

```
─── ◈ Testing ───────────────────────────
```
