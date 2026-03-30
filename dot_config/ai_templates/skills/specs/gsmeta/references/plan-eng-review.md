# Plan Eng Review

> Eng manager-mode plan review: lock in the execution plan — architecture, data flow, diagrams, edge cases, test coverage, performance — before any code is written.

## When to Use

- User says "review the architecture", "engineering review", or "lock in the plan"
- User has a plan or design doc and is about to start coding
- Proactively suggest when implementation is imminent on any non-trivial feature
- Required before shipping — it is the only review marked "required" in the review dashboard

## Inputs

- A plan document or description of what's being built (required)
- Optionally: design doc from office-hours (offer to run it if absent)
- Codebase access (CLAUDE.md for test framework, existing patterns, TODOS.md)
- Access to git history on the branch being reviewed

## Methodology

### Before You Start

**Design doc check:** Look for a design doc from office-hours. If found, read it — it's the source of truth for the problem statement, constraints, and chosen approach. If it has a `Supersedes:` field, check the prior version for context on what changed.

**If no design doc:** Offer to run office-hours first. It gives this review sharper input to work with. If the user skips, proceed with standard review.

### Step 0: Scope Challenge

Before reviewing anything, answer these questions:

1. **Existing code leverage:** What existing code already partially or fully solves each sub-problem? Map every sub-problem to existing code. Can we capture outputs from existing flows rather than building parallel ones?

2. **Minimum viable scope:** What is the minimum set of changes that achieves the stated goal? Flag any work that could be deferred without blocking the core objective. Be ruthless about scope creep.

3. **Complexity check:** If the plan touches more than 8 files or introduces more than 2 new classes/services, treat that as a smell. Challenge whether the same goal can be achieved with fewer moving parts.

4. **Search check:** For each architectural pattern, infrastructure component, or concurrency approach:
   - Does the runtime/framework have a built-in? Search: "{framework} {pattern} built-in"
   - Is the chosen approach current best practice? Search: "{pattern} best practice {year}"
   - Are there known footguns? Search: "{framework} {pattern} pitfalls"
   
   Annotate recommendations with [Layer 1] (tried and true), [Layer 2] (new and popular), [Layer 3] (first principles), or [EUREKA] (conventional approach is wrong for this case). If no web search available, note it.

5. **TODOS cross-reference:** Read TODOS.md. Are any deferred items blocking this plan? Can deferred items be bundled into this PR? Does this plan create new work that should be captured as a TODO?

6. **Completeness check:** Is the plan doing the complete version or a shortcut? With AI-assisted coding, completeness is 10-100x cheaper than human cost. If the plan proposes a shortcut that only saves minutes with AI coding, recommend the complete version.

7. **Distribution check:** If the plan introduces a new artifact (CLI binary, library, container image), does it include the build/publish pipeline? Target platforms? How will users install it? If deferred, flag it explicitly — don't let it silently drop.

If the complexity check triggers (8+ files or 2+ new classes/services), ask the user whether to reduce scope or proceed. After that decision is made, commit to it fully. Don't re-argue in later sections.

## Engineering Preferences

- DRY is important — flag repetition aggressively.
- Well-tested code is non-negotiable; prefer too many tests over too few.
- "Engineered enough" — not under-engineered (fragile, hacky) and not over-engineered (premature abstraction, unnecessary complexity).
- Handle more edge cases, not fewer.
- Bias toward explicit over clever.
- Minimal diff: fewest new abstractions and files touched.

## Question Format Rules

- **One issue = one question.** Never combine multiple issues.
- Describe the problem concretely, with file and line references.
- Present 2-3 options, including "do nothing" where reasonable.
- For each option: effort (human: ~X / AI: ~Y), risk, and maintenance burden.
- Number issues (1, 2, 3...) and letter options (A, B, C...). Label with combo: "3A", "3B".
- **Escape hatch:** If a section has no issues, say so and move on. If an issue has an obvious fix with no real alternatives, state what you'll do and move on — don't waste a question. Only ask when there's a genuine decision with meaningful tradeoffs.
- Map reasoning to engineering preferences: one sentence connecting recommendation to a specific preference.

### Review Sections

Process each section sequentially. For each issue found, present it individually with options, a recommendation, and the reasoning. Wait for user response. Never batch multiple issues into one question.

**1. Architecture Review**

Evaluate:
- Overall system design and component boundaries
- Dependency graph and coupling concerns
- Data flow patterns and potential bottlenecks
- Scaling characteristics and single points of failure
- Security architecture (auth, data access, API boundaries)
- Whether key flows deserve ASCII diagrams in the plan or in code comments
- For each new codepath or integration point: one realistic production failure scenario and whether the plan accounts for it
- Distribution architecture: if a new artifact is introduced, how is it built, published, and updated? Is CI/CD part of the plan?

**2. Code Quality Review**

Evaluate:
- Code organization and module structure
- DRY violations (be aggressive)
- Error handling patterns and missing edge cases (call these out explicitly)
- Technical debt hotspots
- Areas that are over-engineered or under-engineered
- Existing ASCII diagrams in touched files: are they still accurate after this change?

**3. Test Review (most important section — never skip)**

100% coverage is the goal. Walk every codepath in the plan and ensure tests exist for each one.

**Test framework detection:**
First, read CLAUDE.md for a "## Testing" section. If found, use it as authoritative. Otherwise, detect from project files (Gemfile → Ruby, package.json → Node, pyproject.toml → Python, go.mod → Go, etc.) and check for existing test infrastructure.

**Step 1: Trace every codepath**

For each new feature, service, endpoint, or component, trace data flow from each entry point:
- Where does input come from? (request params, props, database, API call)
- What transforms it? (validation, mapping, computation)
- Where does it go? (database write, API response, rendered output)
- What can go wrong at each step? (null/undefined, invalid input, network failure, empty collection)

**Step 2: Map user flows and interaction edge cases**

Beyond code coverage, map how real users interact with the changed code:
- User flows: full journey through the feature (e.g., "user clicks Pay → form validates → API call → success/failure screen")
- Interaction edge cases: double-click/rapid resubmit, navigate away mid-operation, submit with stale data, slow connection, concurrent actions
- Error states the user can see: clear message or silent failure? Can user recover?
- Empty/zero/boundary states: zero results, 10,000 results, minimum-length input, maximum-length input

**Step 3: Check each branch against existing tests**

For each branch in the diagram, search for a test that exercises it. Apply quality scoring:
- 3 stars: tests behavior with edge cases AND error paths
- 2 stars: tests correct behavior, happy path only
- 1 star: smoke test or trivial assertion

**E2E test decision matrix:**

Recommend E2E when:
- Common user flow spanning 3+ components/services
- Integration point where mocking hides real failures
- Auth/payment/data-destruction flows

Recommend eval when:
- Critical LLM call that needs a quality eval
- Prompt template or system instruction changes

Stick with unit tests for:
- Pure functions with clear inputs/outputs
- Internal helpers with no side effects
- Edge cases of single functions

**Regression rule (iron rule, no exceptions):** When the audit identifies code that previously worked but the diff broke, add a regression test as a critical requirement. Regressions are the highest-priority test.

**Step 4: ASCII coverage diagram**

```
CODE PATH COVERAGE
===========================
[+] src/services/billing.ts
    |
    +-- processPayment()
    |   +-- [3* TESTED] Happy path + card declined + timeout
    |   +-- [GAP]       Network timeout — NO TEST
    |   +-- [GAP]       Invalid currency — NO TEST
    ...

USER FLOW COVERAGE
===========================
[+] Payment checkout flow
    |
    +-- [3* TESTED] Complete purchase
    +-- [GAP][->E2E] Double-click submit
    +-- [GAP]        Navigate away during payment
    ...

COVERAGE: 5/13 paths tested (38%)
  Code paths: 3/5 (60%)
  User flows: 2/8 (25%)
GAPS: 8 paths need tests (2 need E2E)
```

**Step 5: Add missing tests to the plan**

For each gap, add a test requirement: what file to create, what to assert, whether it's unit/E2E/eval. Tests belong in the plan and should be written alongside feature code — not deferred.

**Test plan artifact:** Write a test plan to the project directory that `qa` and `qa-only` can consume. Include: affected pages/routes, key interactions to verify, edge cases, critical paths.

**4. Performance Review**

Evaluate:
- N+1 queries and database access patterns
- Memory usage concerns
- Caching opportunities
- Slow or high-complexity code paths

### Confidence Calibration

Every finding must include a confidence score (1-10):

| Score | Meaning | Display rule |
|-------|---------|-------------|
| 9-10 | Verified by reading specific code | Show normally |
| 7-8 | High confidence pattern match | Show normally |
| 5-6 | Moderate, could be false positive | Show with caveat: "Medium confidence, verify this is actually an issue" |
| 3-4 | Low confidence, pattern suspicious but may be fine | Suppress to appendix only |
| 1-2 | Speculation | Only report if severity is P0 |

Finding format: `[SEVERITY] (confidence: N/10) file:line — description`

If a low-confidence finding turns out to be real, log it as a calibration event and update pattern recognition.

### Worktree Parallelization Strategy

Analyze the plan's implementation steps for parallel execution opportunities.

**Skip if:** all steps touch the same primary module, or fewer than 2 independent workstreams exist. Write: "Sequential implementation, no parallelization opportunity."

**Otherwise, produce:**

1. **Dependency table** (module-level, not file-level — plans describe intent not specific files):

| Step | Modules touched | Depends on |
|------|----------------|------------|

2. **Parallel lanes:** group steps into lanes. Steps with no shared modules and no dependency go in separate lanes. Steps sharing a module go in the same lane. Example: `Lane A: step1 → step2 (sequential, shared models/)` / `Lane B: step3 (independent)`

3. **Execution order:** which lanes launch in parallel, which wait. Example: "Launch A + B in parallel. Merge both. Then C."

4. **Conflict flags:** if two parallel lanes touch the same module directory, flag it: "Lanes X and Y both touch module/ — potential merge conflict."

### Failure Modes

For each new codepath in the test review diagram, list one realistic production failure (timeout, nil reference, race condition, stale data) and whether:
1. A test covers that failure
2. Error handling exists for it
3. The user would see a clear error or a silent failure

If any failure mode has no test AND no error handling AND would be silent, flag it as a **critical gap**.

### Outside Voice (optional, recommended)

After all review sections complete, offer an independent second opinion from a different AI system.

Ask: "Want an outside voice? A different AI gives a brutally honest challenge of this plan — logical gaps, feasibility risks, blind spots. Takes ~2 minutes."

If yes, delegate to a subagent with fresh context (no conversation history). Give it the full plan content (truncate at 30KB). The prompt: "Find what the review missed. Look for: logical gaps and unstated assumptions that survived review scrutiny, overcomplexity, feasibility risks the review took for granted, missing dependencies, strategic miscalibration. Be direct. Be terse. No compliments."

Present findings verbatim under an "OUTSIDE VOICE" header.

After presenting, note any points where the outside voice disagrees with review findings:
```
CROSS-MODEL TENSION:
  [Topic]: Review said X. Outside voice says Y. [Context that might change the answer.]
```

For each tension point, ask the user: accept the outside voice's recommendation, keep the current approach, investigate further, or add to TODOS.md. Do NOT auto-incorporate. Cross-model agreement is a strong signal — present it as such — but the user decides.

### Engineering Cognitive Patterns (internalize, don't enumerate)

These shape how you evaluate the plan:

- **Boring by default:** "Every company gets about three innovation tokens." Everything else should be proven technology.
- **Incremental over revolutionary:** Strangler fig, not big bang. Canary, not global rollout.
- **Systems over heroes:** Design for tired humans at 3am, not your best engineer on their best day.
- **Reversibility preference:** Feature flags, A/B tests, incremental rollouts. Make the cost of being wrong low.
- **Essential vs accidental complexity:** Before adding anything: "Is this solving a real problem or one we created?"
- **Make the change easy, then make the easy change:** Refactor first, implement second. Never structural + behavioral changes simultaneously.
- **Own your code in production:** No wall between dev and ops.
- **Two-week smell test:** If a competent engineer can't ship a small feature in two weeks, it's an onboarding problem disguised as architecture.

## Quality Gates

**Priority hierarchy (never skip these):**
Step 0 > Test diagram > Opinionated recommendations > everything else

- Step 0 scope challenge completed
- Architecture review done (all four data flow paths traced)
- Test coverage diagram produced (every codepath mapped, every gap identified)
- Test plan artifact written to project directory
- Performance review done
- "NOT in scope" section written
- "What already exists" section written
- TODOS.md updates presented individually (never batched)
- Failure modes identified (no test + no error handling + silent = critical gap)
- Parallelization strategy produced (if 2+ independent workstreams)
- Review log written

## Outputs

- Annotated/improved plan document with test requirements added
- ASCII coverage diagram
- Test plan artifact for QA consumption
- Parallelization strategy (lanes, dependencies, conflict flags)
- Completion summary:
  - Step 0: scope result
  - Architecture: N issues
  - Code quality: N issues
  - Test review: diagram produced, N gaps
  - Performance: N issues
  - NOT in scope: written
  - What already exists: written
  - TODOS.md: N items proposed
  - Failure modes: N critical gaps
  - Outside voice: ran / skipped
  - Parallelization: N lanes
  - Lake score: X/Y chose complete option
- Review readiness dashboard entry (required, feeds the ship workflow)

## Feeds Into

- >ce:work or implementation (once plan is approved)
- >qa or >qa-only (test plan artifact is primary input)
- >ship (review readiness dashboard entry gates shipping)

## Harness Notes

**Subagent:** Outside voice requires delegating to a fresh-context agent with no conversation history. The plan content (up to 30KB) is passed in the prompt. The subagent must not see prior review conversation — independence is the point. See harness-compat.md "Subagent delegation" section.

**Test framework detection:** Reads project files to auto-detect. If CLAUDE.md has a `## Testing` section, use that as authoritative and skip auto-detection.
