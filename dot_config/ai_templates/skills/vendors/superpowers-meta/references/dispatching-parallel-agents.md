# Dispatching Parallel Agents

> Solve multiple independent problems simultaneously by delegating each to a focused subagent with isolated context.

## When to Use

**Decision tree:**

```
Multiple failures / tasks?
  ├─ NO  → Not applicable
  └─ YES → Are they independent?
              ├─ NO (related: fixing one may fix others) → Single agent investigates all
              └─ YES → Can they work in parallel?
                          ├─ NO (shared state, would interfere) → Sequential agents
                          └─ YES → Parallel dispatch (this skill)
```

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state first
- Agents would interfere with each other (editing same files, using same resources)
- Still in exploratory debugging (don't know what's broken yet)

## Inputs

- A set of 2+ independent failures, tasks, or problems
- Enough context to describe each domain clearly to an isolated agent
- Confidence that the domains are truly independent

## Methodology

### Step 1: Identify Independent Domains

Group failures by what's broken. Each domain must be independently understandable and fixable.

Example grouping:
- File A tests: Tool approval flow
- File B tests: Batch completion behavior
- File C tests: Abort functionality

Each domain is independent — fixing tool approval doesn't affect abort tests.

### Step 2: Create Focused Agent Tasks

Each agent gets:
- **Specific scope:** One test file or subsystem (not "all the tests")
- **Clear goal:** Make these tests pass / fix this specific thing
- **Constraints:** Don't change other code / fix tests only
- **Expected output:** Summary of what you found and fixed

### Step 3: Dispatch in Parallel

Delegate all agents in a single parallel dispatch. They run concurrently.

**Generic dispatch pattern:**
```
[Single message, multiple concurrent subagent invocations]

Subagent A: [Focused prompt for domain A — self-contained, specific scope, explicit output]
Subagent B: [Focused prompt for domain B — self-contained, specific scope, explicit output]
Subagent C: [Focused prompt for domain C — self-contained, specific scope, explicit output]

// All run concurrently; controller waits for all before integrating
```

**Example dispatch (3 agents):**
```
Agent 1 → Fix agent-tool-abort.test.ts
Agent 2 → Fix batch-completion-behavior.test.ts
Agent 3 → Fix tool-approval-race-conditions.test.ts
```

### Step 4: Review and Integrate

When agents return:
1. Read each summary — understand what changed
2. Check for conflicts — did agents edit the same code?
3. Run full test suite — verify all fixes work together
4. Spot check — agents can make systematic errors

---

## Agent Prompt Structure

Good agent prompts are:
1. **Focused** — One clear problem domain
2. **Self-contained** — All context needed to understand the problem
3. **Specific about output** — What should the agent return?

**Prompt template:**

```
Fix the [N] failing tests in [FILE_PATH]:

1. "[test name 1]" - [what it expects]
2. "[test name 2]" - [what it expects]
3. "[test name 3]" - [what it expects]

These are [characterization of issue, e.g., timing/race condition issues]. Your task:

1. Read the test file and understand what each test verifies
2. Identify root cause - [type of issue] or actual bugs?
3. Fix by:
   - [specific approach 1]
   - [specific approach 2]
   - [specific approach 3]

Do NOT [anti-pattern, e.g., just increase timeouts] - find the real issue.

Return: Summary of what you found and what you fixed.
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Too broad scope | "Fix all the tests" — agent gets lost | Specify one file or subsystem |
| No context | "Fix the race condition" — agent doesn't know where | Paste the error messages and test names |
| No constraints | Agent might refactor everything | "Do NOT change production code" or "Fix tests only" |
| Vague output | "Fix it" — you don't know what changed | "Return summary of root cause and changes" |

---

## Verification (After Agents Return)

1. **Review each summary** — Understand what changed and why
2. **Check for conflicts** — Did agents edit the same code? Would changes interfere?
3. **Run full suite** — Verify all fixes work together; no regressions
4. **Spot check** — Agents can make systematic errors; verify the logic looks correct

## Quality Gates

- [ ] Each dispatched domain is truly independent (no shared state)
- [ ] Each agent prompt is self-contained (no implicit context inherited)
- [ ] Each agent has a specific, focused scope
- [ ] Each agent has explicit output requirements
- [ ] After return: all summaries reviewed
- [ ] After return: no conflicting changes
- [ ] After return: full test suite passes

## Outputs

- Parallel investigations completed concurrently
- Each agent returns a summary of root cause and changes made
- Integrated result: all fixes applied, full suite green

## Key Benefits

1. **Parallelization** — Multiple investigations happen simultaneously
2. **Focus** — Each agent has narrow scope, less context to manage
3. **Independence** — Agents don't interfere with each other
4. **Speed** — N problems solved in the time of 1

## Real-World Example

**Session (2025-10-03):** 6 test failures across 3 files after major refactoring.

**Failures:**
- `agent-tool-abort.test.ts`: 3 failures (timing issues)
- `batch-completion-behavior.test.ts`: 2 failures (tools not executing)
- `tool-approval-race-conditions.test.ts`: 1 failure (execution count = 0)

**Decision:** Independent domains — abort logic separate from batch completion separate from race conditions.

**Dispatch:** 3 agents in parallel, one per file.

**Results:**
- Agent 1: Replaced timeouts with event-based waiting
- Agent 2: Fixed event structure bug (threadId in wrong place)
- Agent 3: Added wait for async tool execution to complete

**Integration:** All fixes independent, no conflicts, full suite green. Zero conflicts between agent changes.

## Feeds Into

- Post-integration verification and commit
- If additional failures remain: repeat dispatch cycle or investigate as single agent

## Harness Notes

Parallel dispatch requires the harness to support concurrent subagent execution (e.g., Claude Code, Codex). On harnesses without subagent support, approximate by sequencing agents one after another with the same isolated-context prompt discipline. The quality of parallel work is significantly higher when true parallel execution is available.
