# RedGreenRefactor

Build features or fix bugs using vertical-slice red-green-refactor loops. One test, one implementation, repeat.

## Anti-Pattern: Horizontal Slices

DO NOT write all tests first, then all implementation. This produces bad tests because:

- Tests written in bulk test _imagined_ behavior, not real behavior driven by actual implementation feedback
- You end up testing the _shape_ of things rather than meaningful behavior
- Bulk tests are insensitive to real changes -- they pass when they should fail and fail when they should pass
- You outrun your headlights -- decisions made now will be wrong by the time you implement

```
WRONG (horizontal):
  Write test 1, test 2, test 3, test 4
  Write code 1, code 2, code 3, code 4

RIGHT (vertical):
  Write test 1 → Write code 1
  Write test 2 → Write code 2
  Write test 3 → Write code 3
  Write test 4 → Write code 4
```

## Process

### 1. Planning

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Confirm with user which behaviors to test
- [ ] List the behaviors to test (not implementation steps)
- [ ] Identify deep module opportunities -- can we consolidate or simplify?
- [ ] Design interfaces for testability (see `references/InterfaceDesign.md`)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors are most important to test?"

You can't test everything. Confirm with the user exactly which behaviors matter most. Focus testing effort on critical paths and complex logic, not every possible edge case.

### 2. Tracer Bullet (First Slice)

The first slice proves the end-to-end path works.

**RED:** Write a test for the first behavior. The test must:
- Describe behavior, not implementation
- Use the public interface only
- Survive an internal refactor

Run the test. Confirm it fails.

**GREEN:** Write the minimal code to make the test pass. No more, no less. No speculative features.

Run the test. Confirm it passes.

### 3. Incremental Loop (Remaining Slices)

For each remaining behavior:

**RED:** Write the next test. It must fail.
**GREEN:** Write minimal code to pass. Run all tests.

Rules:
- One test at a time -- never batch
- Each test adds one behavior
- All previous tests must still pass
- If a previous test breaks, fix it before continuing

### 4. Refactor

Only after ALL tests pass. Never refactor while RED -- get to GREEN first.

Look for (see `references/Refactoring.md`):
- Duplication -- extract function or class
- Long methods -- break into private helpers (keep tests on public interface)
- Shallow modules -- combine or deepen
- Feature envy -- move logic to where data lives
- Primitive obsession -- introduce value objects
- Apply SOLID principles where natural
- Existing code the new code reveals as problematic

After each refactoring step:
- Run all tests
- If any test fails, undo the refactoring step and try a smaller step
- Commit after each successful step
