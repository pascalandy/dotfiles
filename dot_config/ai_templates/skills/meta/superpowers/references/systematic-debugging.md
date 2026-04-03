# Systematic Debugging

> Find root cause before attempting any fix — symptom patches are failure.

## When to Use

Use for ANY technical issue:
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues

**Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes
- Previous fix didn't work
- You don't fully understand the issue

**Don't skip when:**
- Issue seems simple (simple bugs have root causes too)
- You're in a hurry (rushing guarantees rework)
- Deadline pressure exists (systematic is faster than thrashing)

## Inputs

- A reproducible (or partially reproducible) bug, failure, or unexpected behavior
- Access to source code, logs, error messages, and test runner

## Methodology

### The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you have not completed Phase 1, you cannot propose fixes.

---

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

#### 1. Read Error Messages Carefully
- Don't skip past errors or warnings — they often contain the exact solution
- Read stack traces completely
- Note line numbers, file paths, error codes

#### 2. Reproduce Consistently
- Can you trigger it reliably?
- What are the exact steps?
- Does it happen every time?
- If not reproducible → gather more data; do not guess

#### 3. Check Recent Changes
- What changed that could cause this?
- Review git diff, recent commits
- Check new dependencies, config changes, environmental differences

#### 4. Gather Evidence in Multi-Component Systems

**When the system has multiple components (CI → build → signing, API → service → database):**

Before proposing fixes, add diagnostic instrumentation at every component boundary:

```
For EACH component boundary:
  - Log what data enters the component
  - Log what data exits the component
  - Verify environment/config propagation
  - Check state at each layer

Run once to gather evidence showing WHERE it breaks
THEN analyze evidence to identify failing component
THEN investigate that specific component
```

**Example (multi-layer system):**
```bash
# Layer 1: Workflow
echo "=== Secrets available in workflow: ==="
echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

# Layer 2: Build script
echo "=== Env vars in build script: ==="
env | grep IDENTITY || echo "IDENTITY not in environment"

# Layer 3: Signing script
echo "=== Keychain state: ==="
security list-keychains
security find-identity -v

# Layer 4: Actual signing
codesign --sign "$IDENTITY" --verbose=4 "$APP"
```

This reveals which layer fails (e.g., secrets → workflow ✓, workflow → build ✗).

#### 5. Trace Data Flow (Root Cause Tracing)

**When error is deep in the call stack:**

**Core principle:** Trace backward through the call chain until you find the original trigger, then fix at the source.

**The tracing process:**

1. **Observe the symptom** — note the error exactly as it appears
2. **Find the immediate cause** — what code directly causes this?
3. **Ask: What called this?** — trace one level up the call chain
4. **Keep tracing up** — what value was passed? where did it come from?
5. **Find the original trigger** — the true source of the bad value

**Example trace:**
```
Symptom: git init failed in /Users/user/project/packages/core
  └─ git init runs with empty cwd → resolves to process.cwd()
     └─ WorktreeManager.createSessionWorktree(projectDir, sessionId)
        └─ Session.initializeWorkspace()
           └─ Session.create()
              └─ test accessed context.tempDir before beforeEach ran
                 └─ setupCoreTest() returns { tempDir: '' } initially
ROOT CAUSE: top-level variable accesses empty value before initialization
```

**When you can't trace manually, add instrumentation:**
```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  console.error('DEBUG git init:', {
    directory,
    cwd: process.cwd(),
    nodeEnv: process.env.NODE_ENV,
    stack,
  });
  await execFileAsync('git', ['init'], { cwd: directory });
}
```
- Use `console.error()` in tests (logger may be suppressed)
- Log BEFORE the dangerous operation, not after it fails
- Include directory, cwd, environment variables, timestamps
- Capture full stack: `new Error().stack`

**Trace decision tree:**
```
Found immediate cause
└─ Can trace one level up?
   ├─ YES → Trace backwards
   │        └─ Is this the source?
   │           ├─ NO → Keep tracing
   │           └─ YES → Fix at source → Add defense-in-depth layers
   └─ NO (dead end) → Fix at symptom point (NEVER preferred)
                      → BETTER: Also add defense-in-depth
```

**NEVER fix just where the error appears.** Always trace back to the original trigger.

**Stack trace tips:**
- In tests: use `console.error()` not logger
- Log before the dangerous operation, not after it fails
- Include: directory, cwd, environment variables, timestamps
- Capture stack: `new Error().stack`

**Finding test pollution (when tests pass alone but fail together):**

Use `find-polluter.sh` (from the upstream [Superpowers project](https://github.com/obra/superpowers) `skills/systematic-debugging/`) — a bisection script that runs each test file in isolation and checks whether a specific file/dir is created after each run:

```bash
# Find which test creates an unwanted .git directory
./find-polluter.sh '.git' 'src/**/*.test.ts'

# Find which test creates a temp directory
./find-polluter.sh '/tmp/stale-dir' 'tests/**/*.test.ts'
```

The script:
1. Collects all test files matching the pattern
2. For each file: checks for pollution, runs the test, checks again
3. Reports the first file that creates the pollution artifact
4. Prints investigation commands (`npm test <file>`, `cat <file>`) for follow-up

After finding the polluter: add `afterEach`/`afterAll` cleanup in that test file or fix the missing teardown. This bisection approach cuts hours of manual isolation down to a single command.

---

### Phase 2: Pattern Analysis

**Find the pattern before fixing:**

1. **Find Working Examples** — locate similar working code in the same codebase; what's working that's similar to what's broken?
2. **Compare Against References** — if implementing a pattern, read the reference implementation COMPLETELY (don't skim — read every line; understand before applying)
3. **Identify Differences** — list every difference between working and broken, however small; do not assume "that can't matter"
4. **Understand Dependencies** — what other components does this need? What settings, config, environment? What assumptions does it make?

---

### Phase 3: Hypothesis and Testing

**Scientific method:**

1. **Form Single Hypothesis** — state clearly: "I think X is the root cause because Y"; write it down; be specific, not vague
2. **Test Minimally** — make the SMALLEST possible change to test the hypothesis; one variable at a time; do not fix multiple things at once
3. **Verify Before Continuing:**
   - Did it work? YES → Phase 4
   - Didn't work? Form NEW hypothesis; do NOT add more fixes on top
4. **When You Don't Know** — say "I don't understand X"; do not pretend to know; ask for help; research more

---

### Phase 4: Implementation

**Fix the root cause, not the symptom:**

#### Step 1: Create Failing Test Case
- Simplest possible reproduction
- Automated test if possible
- One-off test script if no framework
- MUST have a failing test before fixing
- Follow test-driven-development for writing proper failing tests

#### Step 2: Implement Single Fix
- Address the root cause identified in Phase 1
- ONE change at a time
- No "while I'm here" improvements
- No bundled refactoring

#### Step 3: Verify Fix
- Test passes now?
- No other tests broken?
- Issue actually resolved?

#### Step 4: If Fix Doesn't Work
- STOP
- Count how many fixes you have tried
- If < 3: Return to Phase 1, re-analyze with new information
- **If ≥ 3: STOP and question the architecture (Step 5)**
- Do NOT attempt Fix #4 without architectural discussion

#### Step 5: If 3+ Fixes Failed — Question Architecture

**Pattern indicating architectural problem:**
- Each fix reveals new shared state / coupling / problem in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Are we "sticking with it through sheer inertia"?
- Should we refactor architecture vs. continue fixing symptoms?

**Discuss with your human partner before attempting more fixes.**

This is NOT a failed hypothesis — this is a wrong architecture.

---

### Defense-in-Depth (after finding root cause)

When you fix a bug caused by invalid data, add validation at EVERY layer data passes through to make the bug structurally impossible.

**The four layers:**

**Layer 1: Entry Point Validation** — reject obviously invalid input at the API boundary
```typescript
function createProject(name: string, workingDirectory: string) {
  if (!workingDirectory || workingDirectory.trim() === '') {
    throw new Error('workingDirectory cannot be empty');
  }
  if (!existsSync(workingDirectory)) {
    throw new Error(`workingDirectory does not exist: ${workingDirectory}`);
  }
  if (!statSync(workingDirectory).isDirectory()) {
    throw new Error(`workingDirectory is not a directory: ${workingDirectory}`);
  }
}
```

**Layer 2: Business Logic Validation** — ensure data makes sense for this operation
```typescript
function initializeWorkspace(projectDir: string, sessionId: string) {
  if (!projectDir) {
    throw new Error('projectDir required for workspace initialization');
  }
}
```

**Layer 3: Environment Guards** — prevent dangerous operations in specific contexts
```typescript
async function gitInit(directory: string) {
  if (process.env.NODE_ENV === 'test') {
    const normalized = normalize(resolve(directory));
    const tmpDir = normalize(resolve(tmpdir()));
    if (!normalized.startsWith(tmpDir)) {
      throw new Error(`Refusing git init outside temp dir during tests: ${directory}`);
    }
  }
}
```

**Layer 4: Debug Instrumentation** — capture context for forensics
```typescript
async function gitInit(directory: string) {
  const stack = new Error().stack;
  logger.debug('About to git init', { directory, cwd: process.cwd(), stack });
}
```

**Applying the pattern:**
1. Trace the data flow — where does the bad value originate? Where is it used?
2. Map all checkpoints — list every point data passes through
3. Add validation at each layer — entry, business, environment, debug
4. Test each layer — try to bypass layer 1, verify layer 2 catches it

All four layers are necessary. Different code paths, mocks, and platform edge cases bypass different layers.

---

### Condition-Based Waiting (for flaky/timing-related bugs)

**Core principle:** Wait for the actual condition you care about, not a guess about how long it takes.

**When to use:**
- Tests have arbitrary delays (`setTimeout`, `sleep`, `time.sleep()`)
- Tests are flaky (pass sometimes, fail under load)
- Tests timeout when run in parallel
- Waiting for async operations to complete

**Don't use when:**
- Testing actual timing behavior (debounce, throttle intervals) — document WHY timeout is needed

**Pattern:**
```typescript
// ❌ BEFORE: Guessing at timing
await new Promise(r => setTimeout(r, 50));
const result = getResult();
expect(result).toBeDefined();

// ✅ AFTER: Waiting for condition
await waitFor(() => getResult() !== undefined);
const result = getResult();
expect(result).toBeDefined();
```

**Common scenarios:**

| Scenario | Pattern |
|----------|---------|
| Wait for event | `waitFor(() => events.find(e => e.type === 'DONE'))` |
| Wait for state | `waitFor(() => machine.state === 'ready')` |
| Wait for count | `waitFor(() => items.length >= 5)` |
| Wait for file | `waitFor(() => fs.existsSync(path))` |
| Complex condition | `waitFor(() => obj.ready && obj.value > 10)` |

**Generic polling implementation:**
```typescript
async function waitFor<T>(
  condition: () => T | undefined | null | false,
  description: string,
  timeoutMs = 5000
): Promise<T> {
  const startTime = Date.now();
  while (true) {
    const result = condition();
    if (result) return result;
    if (Date.now() - startTime > timeoutMs) {
      throw new Error(`Timeout waiting for ${description} after ${timeoutMs}ms`);
    }
    await new Promise(r => setTimeout(r, 10)); // Poll every 10ms
  }
}
```

**Domain-specific helper signatures** (adapt to your domain):

```typescript
// Wait for a single event type
waitForEvent(threadManager, threadId, 'TOOL_RESULT', timeoutMs?)
  → Promise<LaceEvent>

// Wait for N events of a type
waitForEventCount(threadManager, threadId, 'AGENT_MESSAGE', count, timeoutMs?)
  → Promise<LaceEvent[]>

// Wait for event matching a predicate (when type alone isn't enough)
waitForEventMatch(threadManager, threadId, (e) => e.type === 'TOOL_RESULT' && e.data.id === 'call_123', 'description', timeoutMs?)
  → Promise<LaceEvent>
```

**Before / After example:**

```typescript
// ❌ BEFORE (flaky): guessing at timing
const messagePromise = agent.sendMessage('Execute tools');
await new Promise(r => setTimeout(r, 300)); // Hope tools start in 300ms
agent.abort();
await messagePromise;
await new Promise(r => setTimeout(r, 50));  // Hope results arrive in 50ms
expect(toolResults.length).toBe(2);         // Fails randomly

// ✅ AFTER (reliable): wait for actual conditions
const messagePromise = agent.sendMessage('Execute tools');
await waitForEventCount(threadManager, threadId, 'TOOL_CALL', 2);   // Tools started
agent.abort();
await messagePromise;
await waitForEventCount(threadManager, threadId, 'TOOL_RESULT', 2); // Results ready
expect(toolResults.length).toBe(2); // Always succeeds
// Result: 60% pass rate → 100%, 40% faster execution
```

**Common mistakes:**
- Polling too fast (`setTimeout(check, 1)`) — wastes CPU; use 10ms intervals
- No timeout — always include timeout with clear error message
- Stale data — call the getter inside the loop, not before it

**When arbitrary timeout IS correct:**
```typescript
await waitForEvent(manager, 'TOOL_STARTED'); // First: wait for condition
await new Promise(r => setTimeout(r, 200));  // Then: wait for timed behavior
// 200ms = 2 ticks at 100ms intervals — documented and justified
```
Requirements: (1) first wait for triggering condition, (2) based on known timing not guessing, (3) comment explaining WHY.

---

## Quality Gates

### Phase completion criteria

| Phase | Key Activities | Success Criteria |
|-------|----------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

### Red flags — STOP and return to Phase 1

If you catch yourself thinking any of the following:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- "Pattern says X but I'll adapt it differently"
- "Here are the main problems: [lists fixes without investigation]"
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)
- Each fix reveals a new problem in a different place

**ALL of these mean: STOP. Return to Phase 1.**
**If 3+ fixes failed:** Question the architecture (Phase 4, Step 5).

### Common rationalizations table

| Excuse | Reality |
|--------|---------|
| "Issue is simple, don't need process" | Simple issues have root causes too. Process is fast for simple bugs. |
| "Emergency, no time for process" | Systematic debugging is FASTER than guess-and-check thrashing. |
| "Just try this first, then investigate" | First fix sets the pattern. Do it right from the start. |
| "I'll write test after confirming fix works" | Untested fixes don't stick. Test first proves it. |
| "Multiple fixes at once saves time" | Can't isolate what worked. Causes new bugs. |
| "Reference too long, I'll adapt the pattern" | Partial understanding guarantees bugs. Read it completely. |
| "I see the problem, let me fix it" | Seeing symptoms ≠ understanding root cause. |
| "One more fix attempt" (after 2+ failures) | 3+ failures = architectural problem. Question pattern, don't fix again. |

### Human partner signals you're off-track

| Signal | Meaning |
|--------|---------|
| "Is that not happening?" | You assumed without verifying |
| "Will it show us...?" | You should have added evidence gathering |
| "Stop guessing" | You're proposing fixes without understanding |
| "Ultrathink this" | Question fundamentals, not just symptoms |
| "We're stuck?" (frustrated) | Your approach isn't working |

When you see these: STOP. Return to Phase 1.

### When "no root cause" is found

If systematic investigation reveals the issue is truly environmental, timing-dependent, or external:
1. Document what you investigated
2. Implement appropriate handling (retry, timeout, error message)
3. Add monitoring/logging for future investigation

Note: 95% of "no root cause" cases are incomplete investigation.

## Outputs

- Identified root cause (stated explicitly before any fix)
- Failing test that reproduces the bug
- Single targeted fix at the root cause
- Passing test suite (original + new test)
- Defense-in-depth validation layers added where applicable

## Feeds Into

- **test-driven-development** — for creating the failing test case in Phase 4
- **verification-before-completion** — verify fix worked before claiming success

## Harness Notes

Real-world impact data:
- Systematic approach: 15–30 minutes to fix
- Random fixes approach: 2–3 hours of thrashing
- First-time fix rate: 95% (systematic) vs 40% (ad hoc)
- New bugs introduced: near zero (systematic) vs common (ad hoc)
