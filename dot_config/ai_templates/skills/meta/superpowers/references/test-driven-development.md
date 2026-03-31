# Test-Driven Development (TDD)

> Write the test first, watch it fail, then write minimal code to pass — if you didn't watch the test fail, you don't know if it tests the right thing.

## When to Use

**Always:**
- New features
- Bug fixes
- Refactoring
- Behavior changes

**Exceptions (require explicit human partner permission):**
- Throwaway prototypes
- Generated code
- Configuration files

Thinking "skip TDD just this once"? Stop. That's rationalization.

## Inputs

- A defined behavior, requirement, or bug to address
- Access to the test runner for the project

## Methodology

### The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete

Implement fresh from tests. Period.

---

### The Red-Green-Refactor Cycle

```
RED (write failing test)
  └─ Verify fails correctly?
     ├─ NO (wrong failure) → Fix test → back to RED
     └─ YES
        └─ GREEN (write minimal code)
           └─ Verify all tests pass?
              ├─ NO → Fix code (not test) → back to GREEN
              └─ YES
                 └─ REFACTOR (clean up, no new behavior)
                    └─ Stay green?
                       ├─ NO → Fix regression → back to REFACTOR
                       └─ YES → Next feature → back to RED
```

---

### Step 1: RED — Write Failing Test

Write one minimal test showing what should happen.

**Good test:**
```typescript
test('retries failed operations 3 times', async () => {
  let attempts = 0;
  const operation = () => {
    attempts++;
    if (attempts < 3) throw new Error('fail');
    return 'success';
  };

  const result = await retryOperation(operation);

  expect(result).toBe('success');
  expect(attempts).toBe(3);
});
```
Clear name, tests real behavior, one thing.

**Bad test:**
```typescript
test('retry works', async () => {
  const mock = jest.fn()
    .mockRejectedValueOnce(new Error())
    .mockRejectedValueOnce(new Error())
    .mockResolvedValueOnce('success');
  await retryOperation(mock);
  expect(mock).toHaveBeenCalledTimes(3);
});
```
Vague name, tests mock not code.

**Test requirements:**
- One behavior only
- Clear descriptive name
- Real code (no mocks unless absolutely unavoidable)

---

### Step 2: Verify RED — Watch It Fail

**MANDATORY. Never skip.**

Run the test. Confirm:
- Test fails (not errors out)
- Failure message is the expected one
- Fails because the feature is missing (not because of typos)

**Test passes immediately?** You're testing existing behavior. Fix the test.

**Test errors out?** Fix the error; re-run until it fails correctly.

---

### Step 3: GREEN — Write Minimal Code

Write the simplest code that makes the test pass.

**Good:**
```typescript
async function retryOperation<T>(fn: () => Promise<T>): Promise<T> {
  for (let i = 0; i < 3; i++) {
    try {
      return await fn();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
  throw new Error('unreachable');
}
```
Just enough to pass.

**Bad:**
```typescript
async function retryOperation<T>(
  fn: () => Promise<T>,
  options?: {
    maxRetries?: number;
    backoff?: 'linear' | 'exponential';
    onRetry?: (attempt: number) => void;
  }
): Promise<T> { /* YAGNI */ }
```
Over-engineered — adds features the test doesn't require.

Do not: add features, refactor other code, or "improve" beyond what the test demands.

---

### Step 4: Verify GREEN — Watch It Pass

**MANDATORY.**

Run the test. Confirm:
- The new test passes
- All other tests still pass
- Output is pristine (no errors, no warnings)

**Test fails?** Fix code, not the test.

**Other tests fail?** Fix them now, before proceeding.

---

### Step 5: REFACTOR — Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Rules:
- Keep all tests green throughout
- Do not add new behavior
- Do not change test assertions

---

### Step 6: Repeat

Write the next failing test for the next piece of behavior.

---

### Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | Tests one thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes the behavior | `test('test1')` |
| **Shows intent** | Demonstrates the desired API | Obscures what the code should do |

---

### Bug Fix Workflow

Bug found → write failing test reproducing it → follow TDD cycle → test proves fix and prevents regression.

**Never fix bugs without a test first.**

**Example:**

```
Bug: Empty email accepted

RED:
  test('rejects empty email', async () => {
    const result = await submitForm({ email: '' });
    expect(result.error).toBe('Email required');
  });

Verify RED:
  FAIL: expected 'Email required', got undefined  ✓

GREEN:
  function submitForm(data: FormData) {
    if (!data.email?.trim()) {
      return { error: 'Email required' };
    }
  }

Verify GREEN:
  PASS  ✓

REFACTOR:
  Extract validation for multiple fields if needed.
```

---

### Testing Anti-Patterns (avoid all of these)

#### Anti-Pattern 1: Testing Mock Behavior

**The violation:**
```typescript
// ❌ BAD: Testing that the mock exists
test('renders sidebar', () => {
  render(<Page />);
  expect(screen.getByTestId('sidebar-mock')).toBeInTheDocument();
});
```
Verifies mock exists, not that component works.

**Fix:**
```typescript
// ✅ GOOD: Test real component or don't mock it
test('renders sidebar', () => {
  render(<Page />);  // Don't mock sidebar
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});
```

**Gate function:**
```
BEFORE asserting on any mock element:
  Ask: "Am I testing real component behavior or just mock existence?"
  IF testing mock existence:
    STOP - Delete the assertion or unmock the component
  Test real behavior instead
```

#### Anti-Pattern 2: Test-Only Methods in Production Classes

**The violation:**
```typescript
// ❌ BAD: destroy() only used in tests
class Session {
  async destroy() { /* cleanup */ }
}
afterEach(() => session.destroy());
```
Production class polluted with test-only code; dangerous if called in production.

**Fix:**
```typescript
// ✅ GOOD: Put cleanup in test utilities
// In test-utils/
export async function cleanupSession(session: Session) {
  const workspace = session.getWorkspaceInfo();
  if (workspace) {
    await workspaceManager.destroyWorkspace(workspace.id);
  }
}
afterEach(() => cleanupSession(session));
```

**Gate function:**
```
BEFORE adding any method to a production class:
  Ask: "Is this only used by tests?"
  IF yes:
    STOP - Don't add it. Put it in test utilities instead.
  Ask: "Does this class own this resource's lifecycle?"
  IF no:
    STOP - Wrong class for this method.
```

#### Anti-Pattern 3: Mocking Without Understanding

**The violation:**
```typescript
// ❌ BAD: Mock breaks test logic by removing needed side effect
test('detects duplicate server', () => {
  vi.mock('ToolCatalog', () => ({
    discoverAndCacheTools: vi.fn().mockResolvedValue(undefined)
  }));
  // Mock prevented config write that duplicate detection depends on!
  await addServer(config);
  await addServer(config);  // Should throw — but won't
});
```

**Fix:**
```typescript
// ✅ GOOD: Mock at correct level, preserve behavior test needs
test('detects duplicate server', () => {
  vi.mock('MCPServerManager'); // Just mock slow server startup
  await addServer(config);    // Config written ✓
  await addServer(config);    // Duplicate detected ✓
});
```

**Gate function:**
```
BEFORE mocking any method:
  STOP - Don't mock yet.
  1. Ask: "What side effects does the real method have?"
  2. Ask: "Does this test depend on any of those side effects?"
  3. Ask: "Do I fully understand what this test needs?"

  IF depends on side effects:
    Mock at lower level (the actual slow/external operation)
    OR use test doubles that preserve necessary behavior
    NOT the high-level method the test depends on

  IF unsure what test depends on:
    Run test with real implementation FIRST
    Observe what actually needs to happen
    THEN add minimal mocking at the right level

  Red flags:
    - "I'll mock this to be safe"
    - "This might be slow, better mock it"
    - Mocking without understanding the dependency chain
```

#### Anti-Pattern 4: Incomplete Mocks

**The violation:**
```typescript
// ❌ BAD: Partial mock — only fields you think you need
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' }
  // Missing: metadata that downstream code uses
};
// Breaks when code accesses response.metadata.requestId
```

**Fix:**
```typescript
// ✅ GOOD: Mirror real API completeness
const mockResponse = {
  status: 'success',
  data: { userId: '123', name: 'Alice' },
  metadata: { requestId: 'req-789', timestamp: 1234567890 }
  // All fields the real API returns
};
```

**Gate function:**
```
BEFORE creating mock responses:
  Check: "What fields does the real API response contain?"
  Actions:
    1. Examine actual API response from docs/examples
    2. Include ALL fields the system might consume downstream
    3. Verify mock matches real response schema completely
  Critical:
    If you're creating a mock, you must understand the ENTIRE structure.
    Partial mocks fail silently when code depends on omitted fields.
  If uncertain: Include all documented fields.
```

#### Anti-Pattern 5: Integration Tests as Afterthought

**The violation:**
```
✅ Implementation complete
❌ No tests written
"Ready for testing"
```
Testing is part of implementation, not optional follow-up.

**Fix:** Follow TDD cycle. Claim complete only after tests pass.

#### Anti-Pattern 6: Over-Complex Mocks

**Warning signs:**
- Mock setup is longer than test logic
- Mocking everything to make test pass
- Mocks missing methods real components have
- Test breaks when mock changes

**Ask yourself:** "Do we need to be using a mock here?"

**Recommendation:** Integration tests with real components are often simpler and more reliable than complex mocks. When mock complexity grows, prefer switching to integration tests that exercise real behavior.

---

### TDD Prevents These Anti-Patterns

**Why TDD helps:**

1. **Write test first** — Forces you to think about what you're actually testing before adding any mocks
2. **Watch it fail** — Confirms the test tests real behavior, not mock behavior
3. **Minimal implementation** — No test-only methods creep into production classes
4. **Real dependencies** — You see what the test actually needs before deciding what (if anything) to mock

**If you're testing mock behavior, you violated TDD** — you added mocks without watching the test fail against real code first.

---

## Quality Gates

### Verification checklist (before marking work complete)

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for the expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output is pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and error paths covered

Can't check all boxes? You skipped TDD. Start over.

### Red flags — stop and start over

- Code written before test
- Test written after implementation
- Test passes immediately
- Can't explain why test failed
- Tests planned for "later"
- Rationalizing "just this once"
- "I already manually tested it"
- "Tests after achieve the same purpose"
- "It's about spirit not ritual"
- "Keep as reference" or "adapt existing code"
- "Already spent X hours, deleting is wasteful"
- "TDD is dogmatic, I'm being pragmatic"
- "This is different because..."

**All of these mean: Delete code. Start over with TDD.**

### Common rationalizations table

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD will slow me down" | TDD is faster than debugging. Pragmatic = test-first. |
| "Manual test faster" | Manual doesn't prove edge cases. You'll re-test every change. |
| "Existing code has no tests" | You're improving it. Add tests for existing code. |

### When stuck

| Problem | Solution |
|---------|----------|
| Don't know how to test | Write the wished-for API. Write the assertion first. Ask your human partner. |
| Test too complicated | Design too complicated. Simplify the interface. |
| Must mock everything | Code too coupled. Use dependency injection. |
| Test setup is huge | Extract helpers. Still complex? Simplify the design. |

---

### Three iron laws of testing anti-patterns

```
1. NEVER test mock behavior
2. NEVER add test-only methods to production classes
3. NEVER mock without understanding dependencies
```

### Anti-pattern quick reference

| Anti-Pattern | Fix |
|--------------|-----|
| Assert on mock elements | Test real component or unmock it |
| Test-only methods in production | Move to test utilities |
| Mock without understanding | Understand dependencies first, mock minimally |
| Incomplete mocks | Mirror real API completely |
| Tests as afterthought | TDD — tests first |
| Over-complex mocks | Consider integration tests |

### Anti-pattern red flags

- Assertion checks for `*-mock` test IDs
- Methods only called in test files
- Mock setup is >50% of test
- Test fails when you remove mock
- Can't explain why mock is needed
- Mocking "just to be safe"

---

## Outputs

- Failing test (committed before implementation)
- Minimal passing implementation
- Clean test suite (all green, no warnings)
- Verified behavior through test failure then passage

## Feeds Into

- **systematic-debugging** — write failing test reproducing bug in Phase 4
- **subagent-driven-development** — subagents follow TDD for each task
- **requesting-code-review** — reviewer checks test quality as part of code review

## Final Rule

```
Production code → test exists and failed first
Otherwise → not TDD
```

No exceptions without explicit human partner permission.
