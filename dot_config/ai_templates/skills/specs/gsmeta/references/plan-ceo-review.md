# Plan CEO Review

> CEO/founder-mode plan review: rethink the problem, find the 10-star product, challenge premises, and expand/hold/reduce scope based on what the plan actually needs.

## When to Use

- User says "think bigger", "expand scope", "strategy review", "rethink this", or "is this ambitious enough"
- Plan feels like it could be more ambitious, or conversely, overbuilt
- Before starting implementation on any non-trivial feature
- After office-hours when a design doc exists and you want strategic validation
- Proactively suggest when the user is questioning scope or ambition

## Inputs

- A plan document (required)
- Optionally: a design doc from office-hours (strongly recommended — offer to run office-hours if absent)
- Codebase access (CLAUDE.md, TODOS.md, git log, recent diffs)

## Methodology

### Pre-Review System Audit

Before anything else, gather context:

```
git log --oneline -30
git diff <base> --stat
git stash list
grep -r "TODO|FIXME|HACK|XXX" files touched by the plan
git log --since=30.days --name-only | sort | uniq -c | sort -rn | head -20
```

Read CLAUDE.md, TODOS.md, and any existing architecture docs.

Check for a design doc from office-hours. If found, read it — it's the source of truth for the problem statement, constraints, and chosen approach.

Check for a handoff note from a prior CEO review session. If found, read it to avoid re-asking questions already answered.

**If no design doc found:** Offer to run office-hours inline before the review. Office-hours produces a structured problem statement, premise challenge, and explored alternatives — it gives this review sharper input. If user skips, proceed with standard review.

**Retrospective check:** If prior commits show a previous review cycle (review-driven refactors, reverted changes), be more aggressive reviewing those areas. Recurring problem areas are architectural smells.

**Frontend/UI scope detection:** Note if the plan involves any new UI screens, components, user-facing flows, or design system changes. Flag DESIGN_SCOPE for review.

**Taste calibration (for expansion modes):** Identify 2-3 files in the codebase that are particularly well-designed (style references) and 1-2 anti-patterns to avoid repeating.

**Landscape check:** Search for:
- "[product category] landscape [year]"
- "[key feature] alternatives"
- "why [incumbent] succeeds/fails"

Three-layer synthesis:
- **Layer 1:** Tried-and-true approach in this space
- **Layer 2:** What current search results say
- **Layer 3:** First-principles — where might conventional wisdom be wrong?

Feed into premise challenge and dream state mapping. Log any eureka moments.

### Step 0: Nuclear Scope Challenge + Mode Selection

**0A. Premise Challenge**
1. Is this the right problem? Could a different framing yield a simpler or more impactful solution?
2. What is the actual user/business outcome? Is the plan the most direct path, or is it solving a proxy problem?
3. What would happen if we did nothing? Real pain or hypothetical?

**0B. Existing Code Leverage**
1. What existing code already partially or fully solves each sub-problem?
2. Is this plan rebuilding anything that already exists? If yes, why is rebuilding better than refactoring?

**0C. Dream State Mapping**
Describe the ideal end state 12 months from now. Does this plan move toward it or away?
```
CURRENT STATE ---> THIS PLAN (delta) ---> 12-MONTH IDEAL
```

**0C-bis. Implementation Alternatives (MANDATORY)**
Before mode selection, produce 2-3 distinct approaches:
```
APPROACH A: [Name]
  Summary: [1-2 sentences]
  Effort:  [S/M/L/XL]
  Risk:    [Low/Med/High]
  Pros:    [2-3 bullets]
  Cons:    [2-3 bullets]
  Reuses:  [existing code/patterns]
```
At least 2 required. One must be minimal viable; one must be ideal architecture. Do not proceed to mode selection without user approval.

**0D. Mode-Specific Analysis**

**SCOPE EXPANSION mode:**
1. 10x check: What's the version that's 10x more ambitious for 2x the effort?
2. Platonic ideal: If the best engineer with unlimited time and perfect taste built this, what would it look and feel like? Start from user experience, not architecture.
3. Delight opportunities: At least 5 adjacent 30-minute improvements that would make users think "oh nice, they thought of that."
4. Expansion opt-in ceremony: Present each concrete proposal individually. Ask the user to accept, defer to TODOS.md, or skip. Do NOT batch. Accepted items become plan scope for all remaining sections.

**SELECTIVE EXPANSION mode:**
1. Run HOLD SCOPE analysis first to make the plan bulletproof
2. Then run expansion scan: 10x check, delight opportunities, platform potential
3. Cherry-pick ceremony: Present each expansion individually. Neutral recommendation posture — state effort and risk, let the user decide. If more than 8 candidates, surface top 5-6.

**HOLD SCOPE mode:**
1. Complexity check: If plan touches more than 8 files or introduces more than 2 new classes/services, challenge whether the same goal can be achieved with fewer moving parts.
2. Identify the minimum set of changes that achieves the stated goal. Flag deferrable work.

**SCOPE REDUCTION mode:**
1. Ruthless cut: What is the absolute minimum that ships value to a user? Defer everything else.
2. Separate "must ship together" from "nice to ship together."

**0D-POST: Persist CEO Plan (expansion modes only)**
After the ceremony, write the vision and scope decisions to disk in the project directory. Run an adversarial spec review (subagent with fresh context, no conversation history) on 5 dimensions: completeness, consistency, clarity, scope, feasibility. Fix issues iteratively (max 3 rounds). Report quality score to user.

**0E. Temporal Interrogation**
Think ahead to implementation. Resolve NOW the decisions the implementer will hit:
```
HOUR 1 (foundations):    What does the implementer need to know?
HOUR 2-3 (core logic):   What ambiguities will they hit?
HOUR 4-5 (integration):  What will surprise them?
HOUR 6+ (polish/tests):  What will they wish they'd planned for?
```
(These represent human hours; with AI-assisted coding, 6 human hours compresses to ~30-60 minutes. Decisions are identical.)

**0F. Mode Selection**
Present four options to the user, with context-dependent defaults:

| Situation | Default mode |
|-----------|-------------|
| Greenfield feature | EXPANSION |
| Feature enhancement or iteration | SELECTIVE EXPANSION |
| Bug fix or hotfix | HOLD SCOPE |
| Refactor | HOLD SCOPE |
| Plan touching >15 files | suggest REDUCTION |
| User says "go big" | EXPANSION |
| User says "show me options" | SELECTIVE EXPANSION |

Once selected, commit fully. Never silently drift to a different mode.

## Prime Directives

1. Zero silent failures. Every failure mode must be visible — to the system, to the team, to the user. If a failure can happen silently, that is a critical defect.
2. Every error has a name. Don't say "handle errors." Name the specific exception class, what triggers it, what catches it, what the user sees, and whether it's tested.
3. Data flows have shadow paths. Every new data flow has a happy path and three shadow paths: nil input, empty/zero-length input, upstream error. Trace all four.
4. Interactions have edge cases. Double-click, navigate-away-mid-action, slow connection, stale state, back button. Map them.
5. Observability is scope, not afterthought. New dashboards, alerts, and runbooks are first-class deliverables.
6. Diagrams are mandatory. ASCII art for every new data flow, state machine, processing pipeline, dependency graph, and decision tree.
7. Everything deferred must be written down. TODOS.md or it doesn't exist.
8. Optimize for the 6-month future, not just today. If this plan solves today's problem but creates next quarter's nightmare, say so.
9. Permission to say "scrap it and do this instead." If there's a fundamentally better approach, table it now.

## Engineering Preferences

- DRY is important — flag repetition aggressively.
- Well-tested code is non-negotiable; prefer too many tests over too few.
- Code that is "engineered enough" — not under-engineered (fragile, hacky) and not over-engineered (premature abstraction, unnecessary complexity).
- Handle more edge cases, not fewer; thoughtfulness over speed.
- Bias toward explicit over clever.
- Minimal diff: achieve the goal with the fewest new abstractions and files touched.
- Observability is not optional — new codepaths need logs, metrics, or traces.
- Security is not optional — new codepaths need threat modeling.
- Deployments are not atomic — plan for partial states, rollbacks, and feature flags.

### Review Sections (10 sections)

Process each section one at a time. For each issue found, present it individually with options and a recommendation. Wait for the user's response before proceeding. Never batch multiple issues.

**Section 1: Architecture Review**
- Overall system design and component boundaries (draw the dependency graph)
- Data flow — all four paths for every new flow: happy path, nil path, empty path, error path
- State machines: ASCII diagram for every new stateful object, including impossible transitions
- Coupling concerns: which components are now coupled that weren't before? Is that justified?
- Scaling characteristics: what breaks first under 10x? Under 100x?
- Single points of failure
- Security architecture: auth boundaries, data access, API surfaces
- Production failure scenarios: for each new integration, describe one realistic production failure
- Rollback posture: if this ships and immediately breaks, what's the procedure?

Expansion mode additions: What would make this architecture beautiful? What infrastructure would make this feature a platform other features can build on?

Required: full ASCII system architecture diagram showing new components and relationships.

**Section 2: Error and Rescue Map**
For every new method or codepath that can fail, fill in two tables:

Table 1: What can go wrong, and what exception class covers it.

Table 2: For each exception class — rescued or not, rescue action, what the user sees.

Rules:
- Catch-all error handling is always a smell. Name specific exceptions.
- Catching with only a generic log message is insufficient. Log full context.
- Every rescued error must retry, degrade gracefully, or re-raise with context. Never swallow silently.
- For LLM/AI calls: malformed response, empty response, hallucinated JSON, refusal — each is a distinct failure mode.

**Section 3: Security and Threat Model**
- Attack surface: new endpoints, new params, new file paths, new background jobs
- Input validation: nil, empty string, wrong type, too long, unicode, HTML injection
- Authorization: every new data access scoped correctly? Direct object reference vulnerabilities?
- Secrets and credentials: in env vars, not hardcoded, rotatable?
- New dependencies: security track record?
- Data classification: PII, payment data, credentials?
- Injection vectors: SQL, command, template, LLM prompt injection
- Audit logging for sensitive operations

For each finding: threat, likelihood (High/Med/Low), impact (High/Med/Low), whether the plan mitigates it.

**Section 4: Data Flow and Interaction Edge Cases**

Data flow tracing: ASCII diagram showing INPUT → VALIDATION → TRANSFORM → PERSIST → OUTPUT, with shadow paths at each node (nil, empty, exception, conflict, stale).

Interaction edge cases table:
```
INTERACTION    | EDGE CASE              | HANDLED? | HOW?
Form submit    | Double-click           | ?        |
               | Submit with stale data | ?        |
Async op       | User navigates away    | ?        |
               | Operation times out    | ?        |
List view      | Zero results           | ?        |
               | 10,000 results         | ?        |
Background job | Fails mid-batch        | ?        |
               | Runs twice (dup)       | ?        |
```

**Section 5: Code Quality Review**
- Code organization and module structure. Does new code fit existing patterns?
- DRY violations (be aggressive, reference file and line)
- Naming quality (named for what it does, not how)
- Error handling patterns (cross-reference Section 2)
- Over-engineering check: any abstraction solving a non-existent problem?
- Under-engineering check: anything fragile, assuming happy path only?
- Cyclomatic complexity: flag any new method branching more than 5 times, propose refactor

**Section 6: Test Review**
Diagram every new thing introduced:
- New UX flows
- New data flows
- New codepaths
- New background jobs / async work
- New integrations / external calls
- New error/rescue paths

For each item: test type (unit/integration/system/E2E), whether a test exists in the plan, happy path test, failure path test, edge case test.

Test ambition checks:
- What's the test that makes you confident shipping at 2am on a Friday?
- What's the test a hostile QA engineer would write to break this?
- What's the chaos test?

Also: test pyramid shape, flakiness risks, load/stress test requirements for high-frequency paths.

**Section 7: Performance Review**
- N+1 queries: every new association traversal, does it have includes/preload?
- Memory usage: maximum size in production for each new data structure
- Database indexes: every new query needs an index check
- Caching opportunities for expensive computations or external calls
- Background job sizing: worst-case payload, runtime, retry behavior
- Top 3 slowest new codepaths with estimated p99 latency
- Connection pool pressure (DB, Redis, HTTP)

**Section 8: Observability and Debuggability Review**
New systems break. Ensure you can see why.
- Logs: every new codepath logs enough context to diagnose problems in production
- Metrics: new endpoints/jobs have latency, error rate, and throughput metrics
- Alerts: new failure modes have alerts
- Dashboards: new systems have runbooks
- Distributed tracing: new service calls instrumented
- Debug tools: is there a way to inspect state in production without deploying code?

**Section 9: Deployment and Rollout Review**
- Deployment is not atomic: plan for partial states
- Feature flags: can this be shipped dark and enabled incrementally?
- Migration safety: every schema change is backwards-compatible until old code is gone
- Rollback plan: concrete procedure for every failure mode
- Canary or gradual rollout: is this risky enough to warrant it?
- Zero-downtime: any operations that require downtime?
- Dependencies: does this require coordinating with other services or teams?

**Section 10: Opinionated Recommendations**
Now that all sections are complete, synthesize the 3-5 most impactful changes — the ones that would most improve quality, reduce risk, or unlock future value. For each: why it matters, the concrete change, and the cost.

If UI scope was detected (DESIGN_SCOPE), note that a design review should follow.

**Section 11: Design and UX Review (skip if no UI scope detected)**
Not a pixel-level audit — that's plan-design-review's job. This ensures design intentionality exists.

Evaluate:
- Information architecture: what does the user see first, second, third?
- Interaction state coverage: `FEATURE | LOADING | EMPTY | ERROR | SUCCESS | PARTIAL`
- User journey coherence: storyboard the emotional arc
- AI slop risk: does the plan describe generic UI patterns?
- DESIGN.md alignment: does the plan match the stated design system?
- Responsive intention: is mobile mentioned or an afterthought?
- Accessibility basics: keyboard nav, screen readers, contrast, touch targets

Expansion mode additions:
- What would make this UI feel *inevitable*?
- What 30-minute UI touches would make users think "oh nice, they thought of that"?

Required ASCII diagram: user flow showing screens/states and transitions.

If the plan has significant UI scope, recommend: "Consider running plan-design-review for a deep design review before implementation."

### Cognitive Patterns (internalize, don't enumerate)

These shape how you evaluate the plan throughout:

- **Classification instinct:** Reversibility x magnitude. Most things are two-way doors — move fast.
- **Inversion reflex:** For every "how do we win?" also ask "what would make us fail?"
- **Focus as subtraction:** Primary value is what NOT to do. Fewer things, better.
- **Speed calibration:** 70% information is enough to decide. Slow down only for irreversible + high-magnitude.
- **Proxy skepticism:** Are metrics still serving users or have they become self-referential?
- **Temporal depth:** Think in 5-10 year arcs. Apply regret minimization for major bets.
- **Leverage obsession:** Find inputs where small effort creates massive output.
- **Subtraction default:** If a UI element doesn't earn its pixels, cut it. Feature bloat kills products faster than missing features.
- **Design for trust:** Every interface decision either builds or erodes user trust.
- **Edge case paranoia:** What if the name is 47 chars? Zero results? Network fails mid-action?

## Required Outputs

**"NOT in scope" section:** Every plan review must produce this — work considered and explicitly deferred, with one-line rationale each.

**"What already exists" section:** Existing code/flows that already partially solve sub-problems, and whether the plan reuses or unnecessarily rebuilds them.

**TODOS.md updates:** After all review sections, present each potential TODO as its own individual question. Never batch — one per question. For each TODO:
- **What:** one-line description
- **Why:** concrete problem it solves or value it unlocks
- **Pros/Cons:** what you gain vs. cost and complexity
- **Context:** enough detail for someone picking it up in 3 months
- **Depends on / blocked by:** prerequisites
Options: A) Add to TODOS.md, B) Skip — not valuable enough, C) Build now in this PR.

**Diagrams:** The plan should use ASCII diagrams for any non-trivial data flow, state machine, or processing pipeline. Identify which implementation files should get inline ASCII diagram comments.

**Failure modes:** For each new codepath, list one realistic production failure (timeout, nil, race condition, stale data) and whether: a test covers it, error handling exists, the user would see a clear error or silent failure. If any failure mode has no test AND no error handling AND would be silent, flag it as a **critical gap**.

## Quality Gates

**Priority hierarchy (never skip these):**
Step 0 > System audit > Error/rescue map > Test diagram > Failure modes > Opinionated recommendations > everything else

- Step 0 (scope challenge) completed
- Implementation alternatives presented and one approved
- Mode selected and committed to (no silent drift)
- All 10 review sections walked through
- Spec review subagent run on any written documents
- "NOT in scope" section written
- "What already exists" section written
- TODOS.md updates presented individually
- Failure modes: critical gaps flagged (failure with no test AND no error handling AND silent is critical)
- Diagrams present for all non-trivial flows
- Review log written

## Outputs

- Annotated/improved plan document
- CEO plan document (for expansion modes): vision, scope decisions, deferred items
- "NOT in scope" section in the plan
- "What already exists" section
- TODOS.md updates (presented one at a time, user decides each)
- Review readiness dashboard entry

## Feeds Into

- >plan-eng-review (architectural findings inform engineering review)
- >plan-design-review (if DESIGN_SCOPE detected)
- >ce:work or implementation (once plan is approved)

## Harness Notes

**Subagents:** Two uses requiring delegation to fresh-context agents:
1. Spec review loop (Step 0D-POST): adversarial review of the written CEO plan document
2. Outside voice (optional): independent challenge of the plan after all sections complete

For the outside voice, the subagent must receive the full plan content (truncate at 30KB) with no access to the review conversation. Independence is the point. See harness-compat.md "Subagent delegation" section.
