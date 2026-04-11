# ce:plan

> Transform feature descriptions or requirements into structured, codebase-grounded implementation plans.

## When to Use

- When the user says "plan this", "create a plan", "write a tech plan", "plan the implementation", "how should we build", "what's the approach for", "break this down"
- When a brainstorm/requirements document is ready for technical planning
- For plan deepening when the user says "deepen the plan", "deepen my plan", "deepening pass", or uses "deepen" in reference to a plan
- Best when requirements are at least roughly defined; for exploratory or ambiguous requests, prefer `ce:brainstorm` first

**Workflow position:**
- `ce:brainstorm` defines **WHAT** to build
- `ce:plan` defines **HOW** to build it
- `ce:work` executes the plan

This workflow produces a durable implementation plan. It does **not** implement code, run tests, or learn from execution-time results.

## Inputs

- Feature description, requirements doc path, plan path to deepen, or improvement idea (as argument)
- If the argument is empty, ask: "What would you like to plan? Please describe the feature, bug fix, or improvement you have in mind." Do not proceed until you have a clear planning input.
- Optional: existing requirements document in `docs/brainstorms/` (auto-discovered)
- Optional: existing plan in `docs/plans/` (for resume or deepen flows)

## Methodology

### Core Principles

1. **Use requirements as the source of truth** — If `ce:brainstorm` produced a requirements document, planning should build from it rather than re-inventing behavior.
2. **Decisions, not code** — Capture approach, boundaries, files, dependencies, risks, and test scenarios. Do not pre-write implementation code or shell command choreography. Pseudo-code sketches or DSL grammars that communicate high-level technical design are welcome when explicitly framed as directional guidance, not implementation specification.
3. **Research before structuring** — Explore the codebase, institutional learnings, and external guidance when warranted before finalizing the plan.
4. **Right-size the artifact** — Small work gets a compact plan. Large work gets more structure. The philosophy stays the same at every depth.
5. **Separate planning from execution discovery** — Resolve planning-time questions here. Explicitly defer execution-time unknowns to implementation.
6. **Keep the plan portable** — The plan should work as a living document, review artifact, or issue body without embedding tool-specific executor instructions.
7. **Carry execution posture lightly when it matters** — If the request, origin document, or repo context clearly implies test-first, characterization-first, or another non-default execution posture, reflect that in the plan as a lightweight signal.

### Plan Quality Bar

Every plan should contain:
- A clear problem frame and scope boundary
- Concrete requirements traceability back to the request or origin document
- Exact file paths for the work being proposed
- Explicit test file paths for feature-bearing implementation units
- Decisions with rationale, not just tasks
- Existing patterns or code references to follow
- Enumerated test scenarios for each feature-bearing unit, specific enough that an implementer knows exactly what to test without inventing coverage themselves
- Clear dependencies and sequencing

A plan is ready when an implementer can start confidently without needing the plan to write the code for them.

---

### Phase 0: Resume, Source, and Scope

#### 0.1 Resume Existing Plan Work When Appropriate

If the user references an existing plan file or there is an obvious recent matching plan in `docs/plans/`:
- Read it
- Confirm whether to update it in place or create a new plan
- If updating, preserve completed checkboxes and revise only the still-relevant sections

**Deepen intent:** The word "deepen" (or "deepening") in reference to a plan is the primary trigger for the deepening fast path. Target document is a **plan** in `docs/plans/`, not a requirements document. If the match is not obvious, confirm with the user before proceeding.

Words like "strengthen", "confidence", "gaps", and "rigor" are NOT sufficient on their own to trigger deepening unless the request clearly targets the plan as a whole and does not name a specific section or content area.

Once the plan is identified and appears complete (all major sections present, implementation units defined, `status: active`), short-circuit to Phase 5.3 (Confidence Check and Deepening) in **interactive mode**.

Normal editing requests (e.g., "update the test scenarios", "add a new implementation unit") should NOT trigger the fast path.

If the plan already has a `deepened: YYYY-MM-DD` frontmatter field and there is no explicit user request to re-deepen, the fast path still applies the same confidence-gap evaluation.

#### 0.2 Find Upstream Requirements Document

Before asking planning questions, search `docs/brainstorms/` for files matching `*-requirements.md`.

**Relevance criteria:** A requirements document is relevant if:
- The topic semantically matches the feature description
- It was created within the last 30 days
- It appears to cover the same user problem or scope

If multiple source documents match, ask which one to use.

#### 0.3 Use the Source Document as Primary Input

If a relevant requirements document exists:
1. Read it thoroughly
2. Announce that it will serve as the origin document for planning
3. Carry forward all of: Problem frame, Requirements and success criteria, Scope boundaries, Key decisions and rationale, Dependencies or assumptions, Outstanding questions
4. Use the source document as the primary input to planning and research
5. Reference important carried-forward decisions in the plan with `(see origin: <source-path>)`
6. Do not silently omit source content — if the origin document discussed it, the plan must address it. Before finalizing, scan each section of the origin document to verify nothing was dropped.

#### 0.4 No-Requirements-Doc Fallback

If no relevant requirements document exists:
- Assess whether the request is clear enough for direct technical planning
- If the ambiguity is mainly product framing, user behavior, or scope definition, recommend `ce:brainstorm` first
- If the user wants to continue here anyway, run a short planning bootstrap to establish: Problem frame, Intended behavior, Scope boundaries and obvious non-goals, Success criteria, Blocking questions or assumptions

If the bootstrap uncovers major unresolved product questions:
- Recommend `ce:brainstorm` again
- If the user still wants to continue, require explicit assumptions before proceeding

#### 0.5 Classify Outstanding Questions Before Planning

If the origin document contains blocking questions (`Resolve Before Planning` or similar):
- Review each one before proceeding
- Reclassify as planning-owned work **only if** it is actually a technical, architectural, or research question
- Keep it as a blocker if it would change product behavior, scope, or success criteria

If true product blockers remain, ask the user whether to:
1. Resume `ce:brainstorm` to resolve them
2. Convert them into explicit assumptions or decisions and continue

Do not continue planning while true blockers remain unresolved.

#### 0.6 Assess Plan Depth

Classify the work into one of these plan depths:

- **Lightweight** — small, well-bounded, low ambiguity
- **Standard** — normal feature or bounded refactor with some technical decisions to document
- **Deep** — cross-cutting, strategic, high-risk, or highly ambiguous implementation work

If depth is unclear, ask one targeted question and then continue.

---

### Phase 1: Gather Context

#### 1.1 Local Research (Always Runs)

Prepare a concise planning context summary (a paragraph or two) to pass as input to the research agents. Then run these agents in parallel:

- `compound-engineering:research:repo-research-analyst` (Scope: technology, architecture, patterns)
- `compound-engineering:research:learnings-researcher`

Collect:
- Technology stack and versions
- Architectural patterns and conventions to follow
- Implementation patterns, relevant files, modules, and tests
- AGENTS.md guidance that materially affects the plan
- Institutional learnings from `docs/solutions/`

#### 1.1b Detect Execution Posture Signals

Look for signals:
- The user explicitly asks for TDD, test-first, or characterization-first work
- The origin document calls for test-first implementation
- Local research shows the target area is legacy, weakly tested, or historically fragile
- The user asks for external delegation or mentions "use codex" / "delegate mode" — add `Execution target: external-delegate` to implementation units that are pure code writing

When the signal is clear, carry it forward silently in the relevant implementation units. Ask the user only if the posture would materially change sequencing or risk.

#### 1.2 Decide on External Research

Based on the origin document, user signals, and local findings, decide whether external research adds value.

**Leverage repo-research-analyst's technology context:**
- If specific frameworks and versions were detected, pass exact identifiers to framework-docs-researcher for version-specific documentation
- If the feature touches a technology layer well-established in the repo, lean toward skipping external research
- If the feature touches a technology layer absent or thin in the repo, lean toward external research

**Always lean toward external research when:**
- The topic is high-risk: security, payments, privacy, external APIs, migrations, compliance
- The codebase lacks relevant local patterns — fewer than 3 direct examples of the pattern this plan needs
- Local patterns exist for an adjacent domain but not the exact one — frame the external research query around the domain gap specifically
- The user is exploring unfamiliar territory

**Skip external research when:**
- The codebase already shows a strong local pattern — multiple direct examples, recently touched, following current conventions
- The user already knows the intended shape
- The technology scan found the relevant layer well-established

Announce the decision briefly before continuing.

#### 1.3 External Research (Conditional)

If Step 1.2 indicates external research is useful, run these agents in parallel:
- `compound-engineering:research:best-practices-researcher`
- `compound-engineering:research:framework-docs-researcher`

#### 1.4 Consolidate Research

Summarize: relevant codebase patterns and file paths, relevant institutional learnings, external references and best practices if gathered, related issues/PRs/prior art, any constraints that should materially shape the plan.

#### 1.4b Reclassify Depth When Research Reveals External Contract Surfaces

If the current classification is **Lightweight** and Phase 1 research found that the work touches any of these external contract surfaces, reclassify to **Standard**:
- Environment variables consumed by external systems, CI, or other repositories
- Exported public APIs, CLI flags, or command-line interface contracts
- CI/CD configuration files
- Shared types or interfaces imported by downstream consumers
- Documentation referenced by external URLs

Announce the reclassification briefly.

#### 1.5 Flow and Edge-Case Analysis (Conditional)

For **Standard** or **Deep** plans, or when user flow completeness is still unclear, run:
- `compound-engineering:workflow:spec-flow-analyzer`

Use the output to: identify missing edge cases, state transitions, or handoff gaps; tighten requirements trace or verification strategy; add only the flow details that materially improve the plan.

---

### Phase 2: Resolve Planning Questions

Build a planning question list from: deferred questions in the origin document, gaps discovered in research, and technical decisions required to produce a useful plan.

For each question, decide whether it should be:
- **Resolved during planning** — the answer is knowable from repo context, documentation, or user choice
- **Deferred to implementation** — the answer depends on code changes, runtime behavior, or execution-time discovery

Ask the user only when the answer materially affects architecture, scope, sequencing, or risk and cannot be responsibly inferred.

**Do not** run tests, build the app, or probe runtime behavior in this phase.

---

### Phase 3: Structure the Plan

#### 3.1 Title and File Naming

- Draft a clear, searchable title using conventional format such as `feat: Add user authentication` or `fix: Prevent checkout double-submit`
- Determine the plan type: `feat`, `fix`, or `refactor`
- Build the filename: `docs/plans/YYYY-MM-DD-NNN-<type>-<descriptive-name>-plan.md`
  - Create `docs/plans/` if it does not exist
  - Check existing files for today's date to determine the next sequence number (zero-padded to 3 digits, starting at 001)
  - Keep the descriptive name concise (3–5 words) and kebab-cased
  - Examples: `2026-01-15-001-feat-user-authentication-flow-plan.md`, `2026-02-03-002-fix-checkout-race-condition-plan.md`
  - Avoid: missing sequence numbers, vague names like "new-feature", invalid characters (colons, spaces)

#### 3.2 Stakeholder and Impact Awareness

For **Standard** or **Deep** plans, briefly consider who is affected by this change — end users, developers, operations, other teams — and how that should shape the plan.

#### 3.3 Break Work into Implementation Units

Break the work into logical implementation units. Each unit should represent one meaningful change that an implementer could typically land as an atomic commit.

**Good units are:**
- Focused on one component, behavior, or integration seam
- Usually touching a small cluster of related files
- Ordered by dependency
- Concrete enough for execution without pre-writing code
- Marked with checkbox syntax for progress tracking

**Avoid:**
- 2–5 minute micro-steps
- Units that span multiple unrelated concerns
- Units that are so vague an implementer still has to invent the plan

#### 3.4 High-Level Technical Design (Optional)

Before detailing implementation units, decide whether an overview would help a reviewer validate the intended approach.

**When to include it:**

| Work involves... | Best overview form |
|---|---|
| DSL or API surface design | Pseudo-code grammar or contract sketch |
| Multi-component integration | Mermaid sequence or component diagram |
| Data pipeline or transformation | Data flow sketch |
| State-heavy lifecycle | State diagram |
| Complex branching logic | Flowchart |
| Mode/flag combinations or multi-input behavior | Decision matrix (inputs → outcomes) |
| Single-component with non-obvious shape | Pseudo-code sketch |

**When to skip it:**
- Well-patterned work where prose and file paths tell the whole story
- Straightforward CRUD or convention-following changes
- Lightweight plans where the approach is obvious

Frame every sketch with: *"This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce."*

#### 3.5 Define Each Implementation Unit

For each unit, include:
- **Goal** — what this unit accomplishes
- **Requirements** — which requirements or success criteria it advances
- **Dependencies** — what must exist first
- **Files** — exact file paths to create, modify, or test
- **Approach** — key decisions, data flow, component boundaries, or integration notes
- **Execution note** — optional, only when the unit benefits from a non-default execution posture such as test-first, characterization-first, or external delegation
- **Technical design** — optional pseudo-code or diagram when the unit's approach is non-obvious. Frame explicitly as directional guidance, not implementation specification.
- **Patterns to follow** — existing code or conventions to mirror
- **Test scenarios** — enumerate specific test cases the implementer should write, right-sized to the unit's complexity and risk. Consider each category below and include scenarios from every category that applies:
  - **Happy path behaviors** — core functionality with expected inputs and outputs
  - **Edge cases** (when the unit has meaningful boundaries) — boundary values, empty inputs, nil/null states, concurrent access
  - **Error and failure paths** (when the unit has failure modes) — invalid input, downstream service failures, timeout behavior, permission denials
  - **Integration scenarios** (when the unit crosses layers) — behaviors that mocks alone will not prove, e.g., "creating X triggers callback Y which persists Z"
  - For units with no behavioral change (pure config, scaffolding, styling), use `Test expectation: none -- [reason]` instead of leaving the field blank
- **Verification** — how an implementer should know the unit is complete, expressed as outcomes rather than shell command scripts

Every feature-bearing unit should include the test file path in **Files**.

**Use `Execution note` sparingly. Good uses include:**
- `Execution note: Start with a failing integration test for the request/response contract.`
- `Execution note: Add characterization coverage before modifying this legacy parser.`
- `Execution note: Implement new domain behavior test-first.`
- `Execution note: Execution target: external-delegate`

Do not expand units into literal `RED/GREEN/REFACTOR` substeps.

#### 3.6 Keep Planning-Time and Implementation-Time Unknowns Separate

If something is important but not knowable yet, record it explicitly under deferred implementation notes rather than pretending to resolve it in the plan.

Examples:
- Exact method or helper names
- Final SQL or query details after touching real code
- Runtime behavior that depends on seeing actual test failures
- Refactors that may become unnecessary once implementation starts

---

### Phase 4: Write the Plan

#### 4.1 Plan Depth Guidance

**Lightweight:**
- Keep the plan compact
- Usually 2–4 implementation units
- Omit optional sections that add little value

**Standard:**
- Use the full core template, omitting optional sections that add no value for this particular work
- Usually 3–6 implementation units
- Include risks, deferred questions, and system-wide impact when relevant

**Deep:**
- Use the full core template plus optional analysis sections where warranted
- Usually 4–8 implementation units
- Group units into phases when that improves clarity
- Include alternatives considered, documentation impacts, and deeper risk treatment when warranted

#### 4.1b Optional Deep Plan Extensions

For sufficiently large, risky, or cross-cutting work, add the sections that genuinely help:
- **Alternative Approaches Considered**
- **Success Metrics**
- **Dependencies / Prerequisites** — external systems, services, or preconditions required before work begins
- **Risk Analysis & Mitigation**
- **Phased Delivery**
- **Documentation Plan**
- **Operational / Rollout Notes**
- **Future Considerations** — only when they materially affect current design decisions or constrain the implementation shape

Do not add these as boilerplate. Include them only when they improve execution quality or stakeholder alignment.

#### 4.2 Core Plan Template

```markdown
---
title: [Plan Title]
type: [feat|fix|refactor]
status: active
date: YYYY-MM-DD
origin: docs/brainstorms/YYYY-MM-DD-<topic>-requirements.md  # include when planning from a requirements doc
deepened: YYYY-MM-DD  # optional, set when the confidence check substantively strengthens the plan
---

# [Plan Title]

## Overview

[What is changing and why]

## Problem Frame

[Summarize the user/business problem and context. Reference the origin doc when present.]

## Requirements Trace

- R1. [Requirement or success criterion this plan must satisfy]
- R2. [Requirement or success criterion this plan must satisfy]

## Scope Boundaries

- [Explicit non-goal or exclusion]

## Context & Research

### Relevant Code and Patterns

- [Existing file, class, component, or pattern to follow]

### Institutional Learnings

- [Relevant `docs/solutions/` insight]

### External References

- [Relevant external docs or best-practice source, if used]

## Key Technical Decisions

- [Decision]: [Rationale]

## Open Questions

### Resolved During Planning

- [Question]: [Resolution]

### Deferred to Implementation

- [Question or unknown]: [Why it is intentionally deferred]

<!-- Optional: Include this section only when the work involves DSL design, multi-component
     integration, complex data flow, state-heavy lifecycle, or other cases where prose alone
     would leave the approach shape ambiguous. Omit it entirely for well-patterned or
     straightforward work. -->
## High-Level Technical Design

> *This illustrates the intended approach and is directional guidance for review, not implementation specification. The implementing agent should treat it as context, not code to reproduce.*

[Pseudo-code grammar, mermaid diagram, data flow sketch, or state diagram]

## Implementation Units

- [ ] **Unit 1: [Name]**

**Goal:** [What this unit accomplishes]

**Requirements:** [R1, R2]

**Dependencies:** [None / Unit 1 / external prerequisite]

**Files:**
- Create: `path/to/new_file`
- Modify: `path/to/existing_file`
- Test: `path/to/test_file`

**Approach:**
- [Key design or sequencing decision]

**Execution note:** [Optional test-first, characterization-first, external-delegate, or other execution posture signal]

**Technical design:** *(optional -- pseudo-code or diagram when the unit's approach is non-obvious. Directional guidance, not implementation specification.)*

**Patterns to follow:**
- [Existing file, class, or pattern]

**Test scenarios:**
- [Scenario: specific input/action -> expected outcome. Prefix with category — Happy path, Edge case, Error path, or Integration — to signal intent]

**Verification:**
- [Outcome that should hold when this unit is complete]

## System-Wide Impact

- **Interaction graph:** [What callbacks, middleware, observers, or entry points may be affected]
- **Error propagation:** [How failures should travel across layers]
- **State lifecycle risks:** [Partial-write, cache, duplicate, or cleanup concerns]
- **API surface parity:** [Other interfaces that may require the same change]
- **Integration coverage:** [Cross-layer scenarios unit tests alone will not prove]
- **Unchanged invariants:** [Existing APIs, interfaces, or behaviors that this plan explicitly does not change]

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| [Meaningful risk] | [How it is addressed or accepted] |

## Documentation / Operational Notes

- [Docs, rollout, monitoring, or support impacts when relevant]

## Sources & References

- **Origin document:** [docs/brainstorms/YYYY-MM-DD-<topic>-requirements.md](path)
- Related code: [path or symbol]
- Related PRs/issues: #[number]
- External docs: [url]
```

**Optional extensions for Deep plans:**

```markdown
## Alternative Approaches Considered

- [Approach]: [Why rejected or not chosen]

## Success Metrics

- [How we will know this solved the intended problem]

## Risk Analysis & Mitigation

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk] | [Low/Med/High] | [Low/Med/High] | [How addressed] |

## Phased Delivery

### Phase 1
- [What lands first and why]

## Documentation Plan

- [Docs or runbooks to update]

## Operational / Rollout Notes

- [Monitoring, migration, feature flag, or rollout considerations]
```

#### 4.3 Planning Rules

- Prefer path plus class/component/pattern references over brittle line numbers
- Keep implementation units checkable with `- [ ]` syntax for progress tracking
- Do not include implementation code — no imports, exact method signatures, or framework-specific syntax
- Pseudo-code sketches and DSL grammars are allowed in High-Level Technical Design and per-unit technical design fields. Frame them explicitly as directional guidance.
- Mermaid diagrams are encouraged when they clarify relationships or flows that prose alone would make hard to follow
- Do not include git commands, commit messages, or exact test command recipes
- Do not expand implementation units into micro-step `RED/GREEN/REFACTOR` instructions
- Do not pretend an execution-time question is settled just to make the plan look complete

#### 4.4 Visual Communication in Plan Documents

Visual aids for plan navigation (dependency graphs, interaction diagrams, comparison tables) are conditional on content patterns, not on plan depth classification.

**When to include:**

| Plan describes... | Visual aid | Placement |
|---|---|---|
| 4+ implementation units with non-linear dependencies | Mermaid dependency graph | Before or after the Implementation Units heading |
| System-Wide Impact naming 3+ interacting surfaces | Mermaid interaction or component diagram | Within the System-Wide Impact section |
| 3+ behavioral modes, states, or variants | Markdown comparison table | Within Overview or Problem Frame |
| 3+ interacting decisions or 3+ alternatives | Markdown comparison table | Within the relevant section |

**When to skip:**
- The plan has 3 or fewer units in a straight dependency chain
- Prose already communicates the relationships clearly
- The visual would duplicate what the High-Level Technical Design section already shows
- The visual describes code-level detail (specific method names, SQL columns, API field lists)

**Format selection:**
- **Mermaid** (default) for dependency graphs and interaction diagrams — 5–15 nodes, no in-box annotations, use `TB` (top-to-bottom) direction
- **ASCII/box-drawing diagrams** for annotated flows that need rich in-box content — follow 80-column max for code blocks
- **Markdown tables** for mode/variant comparisons and decision/approach comparisons

Prose is authoritative: when a visual aid and its surrounding prose disagree, the prose governs.

---

### Phase 5: Final Review, Write File, and Handoff

#### 5.1 Review Before Writing

Before finalizing, check:
- The plan does not invent product behavior that should have been defined in `ce:brainstorm`
- Every major decision is grounded in the origin document or research
- Each implementation unit is concrete, dependency-ordered, and implementation-ready
- If test-first or characterization-first posture was explicit or strongly implied, the relevant units carry it forward with a lightweight `Execution note`
- Each feature-bearing unit has test scenarios from every applicable category — right-sized to the unit's complexity, not padded or skimped
- Test scenarios name specific inputs, actions, and expected outcomes without becoming test code
- Feature-bearing units with blank or missing test scenarios are flagged as incomplete. The `Test expectation: none -- [reason]` annotation is only valid for non-feature-bearing units.
- Deferred items are explicit and not hidden as fake certainty
- Would a visual aid (dependency graph, interaction diagram, comparison table) help a reader grasp the plan structure faster than scanning prose alone?

If the plan originated from a requirements document, re-read that document and verify:
- The chosen approach still matches the product intent
- Scope boundaries and success criteria are preserved
- Blocking questions were either resolved, explicitly assumed, or sent back to `ce:brainstorm`
- Every section of the origin document is addressed in the plan

#### 5.2 Write Plan File

**REQUIRED: Write the plan file to disk before presenting any options.**

Save the complete plan to: `docs/plans/YYYY-MM-DD-NNN-<type>-<descriptive-name>-plan.md`

Confirm: `Plan written to docs/plans/[filename]`

**Pipeline mode:** If invoked from an automated workflow (LFG, SLFG, or any `disable-model-invocation` context), skip interactive questions. Make the needed choices automatically and proceed to writing the plan.

#### 5.3 Confidence Check and Deepening

After writing the plan file, automatically evaluate whether the plan needs strengthening.

**Two deepening modes:**
- **Auto mode** (default during plan generation): Runs without asking the user for approval. Sub-agent findings are synthesized directly into the plan.
- **Interactive mode** (activated by the re-deepen fast path in Phase 0.1): Sub-agent findings are presented individually for review before integration. The user can accept, reject, or discuss each agent's findings. Only accepted findings are synthesized into the plan.

**Pipeline mode:** This phase always runs in auto mode in pipeline/disable-model-invocation contexts.

##### 5.3.1 Classify Plan Depth and Topic Risk

Determine the plan depth from the document (Lightweight, Standard, Deep).

**High-risk signals:**
- Authentication, authorization, or security-sensitive behavior
- Payments, billing, or financial flows
- Data migrations, backfills, or persistent data changes
- External APIs or third-party integrations
- Privacy, compliance, or user data handling
- Cross-interface parity or multi-surface behavior
- Significant rollout, monitoring, or operational concerns

##### 5.3.2 Gate: Decide Whether to Deepen

- **Lightweight** plans usually do not need deepening unless they are high-risk
- **Standard** plans often benefit when one or more important sections still look thin
- **Deep** or high-risk plans often benefit from a targeted second pass
- **Thin local grounding override:** If Phase 1.2 triggered external research because local patterns were thin (fewer than 3 direct examples or adjacent-domain match), always proceed to scoring regardless of how grounded the plan appears.

If the plan already appears sufficiently grounded and the thin-grounding override does not apply, report "Confidence check passed — no sections need strengthening" and proceed to Phase 5.4.

##### 5.3.3 Score Confidence Gaps

Use a checklist-first, risk-weighted scoring pass.

For each section, compute:
- **Trigger count** — number of checklist problems that apply
- **Risk bonus** — add 1 if the topic is high-risk and this section is materially relevant to that risk
- **Critical-section bonus** — add 1 for `Key Technical Decisions`, `Implementation Units`, `System-Wide Impact`, `Risks & Dependencies`, or `Open Questions` in Standard or Deep plans

Treat a section as a candidate if:
- it hits **2+ total points**, or
- it hits **1+ point** in a high-risk domain and the section is materially important

Choose only the top **2–5** sections by score. If deepening a lightweight plan (high-risk exception), cap at **1–2** sections.

If the plan already has a `deepened:` date, prefer sections not yet substantially strengthened if their scores are comparable.

**Section Checklists:**

**Requirements Trace:**
- Requirements are vague or disconnected from implementation units
- Success criteria are missing or not reflected downstream
- Units do not clearly advance the traced requirements
- Origin requirements are not clearly carried forward

**Context & Research / Sources & References:**
- Relevant repo patterns are named but never used in decisions or implementation units
- Cited learnings or references do not materially shape the plan
- High-risk work lacks appropriate external or internal grounding
- Research is generic instead of tied to this repo or this plan

**Key Technical Decisions:**
- A decision is stated without rationale
- Rationale does not explain tradeoffs or rejected alternatives
- The decision does not connect back to scope, requirements, or origin context
- An obvious design fork exists but the plan never addresses why one path won

**Open Questions:**
- Product blockers are hidden as assumptions
- Planning-owned questions are incorrectly deferred to implementation
- Resolved questions have no clear basis in repo context, research, or origin decisions
- Deferred items are too vague to be useful later

**High-Level Technical Design (when present):**
- The sketch uses the wrong medium for the work
- The sketch contains implementation code rather than pseudo-code
- The non-prescriptive framing is missing or weak
- The sketch does not connect to the key technical decisions or implementation units

**High-Level Technical Design (when absent) — Standard or Deep plans only:**
- The work involves DSL design, API surface design, multi-component integration, complex data flow, or state-heavy lifecycle
- Key technical decisions would be easier to validate with a visual or pseudo-code representation
- The approach section of implementation units is thin and a higher-level technical design would provide context

**Implementation Units:**
- Dependency order is unclear or likely wrong
- File paths or test file paths are missing where they should be explicit
- Units are too large, too vague, or broken into micro-steps
- Approach notes are thin or do not name the pattern to follow
- Test scenarios are vague, skip applicable categories, or are disproportionate to the unit's complexity
- Feature-bearing units have blank or missing test scenarios
- Verification outcomes are vague or not expressed as observable results

**System-Wide Impact:**
- Affected interfaces, callbacks, middleware, entry points, or parity surfaces are missing
- Failure propagation is underexplored
- State lifecycle, caching, or data integrity risks are absent where relevant
- Integration coverage is weak for cross-layer work

**Risks & Dependencies / Documentation / Operational Notes:**
- Risks are listed without mitigation
- Rollout, monitoring, migration, or support implications are missing when warranted
- External dependency assumptions are weak or unstated
- Security, privacy, performance, or data risks are absent where they obviously apply

##### 5.3.4 Report and Dispatch Targeted Research

Before dispatching agents, report what sections are being strengthened and why:
```text
Strengthening [section names] — [brief reason for each]
```

For each selected section, choose the smallest useful agent set. At most **1–3 agents per section** and usually no more than **8 agents total**.

**Deterministic Section-to-Agent Mapping:**

- **Requirements Trace / Open Questions classification:**
  - `compound-engineering:workflow:spec-flow-analyzer` for missing user flows, edge cases, and handoff gaps
  - `compound-engineering:research:repo-research-analyst` (Scope: `architecture, patterns`) for repo-grounded patterns and implementation reality checks

- **Context & Research / Sources & References gaps:**
  - `compound-engineering:research:learnings-researcher`
  - `compound-engineering:research:framework-docs-researcher`
  - `compound-engineering:research:best-practices-researcher`
  - Add `compound-engineering:research:git-history-analyzer` only when historical rationale is materially missing

- **Key Technical Decisions:**
  - `compound-engineering:review:architecture-strategist`
  - Add `compound-engineering:research:framework-docs-researcher` or `compound-engineering:research:best-practices-researcher` when the decision needs external grounding

- **High-Level Technical Design:**
  - `compound-engineering:review:architecture-strategist`
  - `compound-engineering:research:repo-research-analyst` (Scope: `architecture, patterns`)
  - Add `compound-engineering:research:best-practices-researcher` when the technical design involves a DSL, API surface, or pattern that benefits from external validation

- **Implementation Units / Verification:**
  - `compound-engineering:research:repo-research-analyst` (Scope: `patterns`)
  - `compound-engineering:review:pattern-recognition-specialist`
  - Add `compound-engineering:workflow:spec-flow-analyzer` when sequencing depends on user flow or handoff completeness

- **System-Wide Impact:**
  - `compound-engineering:review:architecture-strategist`
  - Add the specific specialist that matches the risk:
    - `compound-engineering:review:performance-oracle` for scalability, latency, throughput, and resource-risk analysis
    - `compound-engineering:review:security-sentinel` for auth, validation, exploit surfaces, and security boundary review
    - `compound-engineering:review:data-integrity-guardian` for migrations, persistent state safety, consistency, and data lifecycle risks

- **Risks & Dependencies / Operational Notes:**
  - `compound-engineering:review:security-sentinel` for security, auth, privacy, and exploit risk
  - `compound-engineering:review:data-integrity-guardian` for persistent data safety, constraints, and transaction boundaries
  - `compound-engineering:review:data-migration-expert` for migration realism, backfills, and production data transformation risk
  - `compound-engineering:review:deployment-verification-agent` for rollout checklists, rollback planning, and launch verification
  - `compound-engineering:review:performance-oracle` for capacity, latency, and scaling concerns

**For each selected agent, pass:**
- Scope prefix from the mapping above when the agent supports scoped invocation
- A short plan summary
- The exact section text
- Why the section was selected (which checklist triggers fired)
- The plan depth and risk profile
- A specific question to answer
- Instruction to return findings that change planning quality — stronger rationale, sequencing, verification, risk treatment, or references — no implementation code, no shell commands

##### 5.3.5 Choose Research Execution Mode

- **Direct mode** (default) — use when the selected section set is small and parent can safely read agent outputs inline
- **Artifact-backed mode** — use only when selected research scope is large (more than 5 agents likely to return meaningful findings, selected section excerpts are long, topic is high-risk and likely to attract bulky source-backed analysis)

Artifact-backed mode uses a per-run scratch directory under `.context/compound-engineering/ce-plan/deepen/`.

##### 5.3.6 Run Targeted Research

Launch the selected agents in parallel (if the platform supports it; otherwise run sequentially).

Prefer local repo and institutional evidence first. Use external research only when the gap cannot be closed responsibly from repo context or already-cited sources.

If a selected section can be improved by reading the origin document more carefully, do that before dispatching external agents.

**Direct mode:** Have each selected agent return its findings directly to the parent. Keep the return payload focused: strongest findings only, the evidence or sources that matter, the concrete planning improvement implied by the finding.

**Artifact-backed mode:** For each selected agent, instruct it to write one compact artifact file in the scratch directory and return only a short completion summary. Each artifact should contain: target section, why selected, 3–7 findings, source-backed rationale, the specific plan change implied by each finding. No implementation code, no shell commands.

If an artifact is missing or clearly malformed, re-run that agent or fall back to direct-mode reasoning for that section.

If agent outputs conflict: prefer repo-grounded and origin-grounded evidence over generic advice; prefer official framework documentation over secondary best-practice summaries when the conflict is about library behavior; if a real tradeoff remains, record it explicitly in the plan.

##### 5.3.6b Interactive Finding Review (Interactive Mode Only)

Skip this step in auto mode.

In interactive mode, for each agent that returned findings:
1. Summarize the agent and its target section
2. Present the findings concisely — bullet the key points, enough context for the user to evaluate
3. Ask the user: **Accept** / **Reject** / **Discuss** (discuss lets the user talk through findings, then re-ask with only accept/reject on the second ask)

Present findings from multiple agents targeting the same section one agent at a time.

After all agents have been reviewed, carry only the accepted findings forward to 5.3.7.

If the user accepted no findings, report "No findings accepted — plan unchanged." Clean up the scratch directory if artifact-backed mode was used. Proceed directly to Phase 5.4 (skip 5.3.7 and 5.3.8). This interactive-mode-only skip does not apply in auto mode; auto mode always proceeds through 5.3.7 and 5.3.8.

If findings were accepted and the plan was modified, proceed through 5.3.7 and 5.3.8 as normal — document-review acts as a quality gate on the changes.

##### 5.3.7 Synthesize and Update the Plan

Strengthen only the selected sections. Keep the plan coherent and preserve its overall structure.

In interactive mode: only integrate findings the user accepted.

**Allowed changes:**
- Clarify or strengthen decision rationale
- Tighten requirements trace or origin fidelity
- Reorder or split implementation units when sequencing is weak
- Add missing pattern references, file/test paths, or verification outcomes
- Expand system-wide impact, risks, or rollout treatment where justified
- Reclassify open questions between `Resolved During Planning` and `Deferred to Implementation` when evidence supports the change
- Strengthen, replace, or add a High-Level Technical Design section when warranted
- Strengthen or add per-unit technical design fields where the unit's approach is non-obvious
- Add or update `deepened: YYYY-MM-DD` in frontmatter when the plan was substantively improved

**Do NOT:**
- Add implementation code — no imports, exact method signatures, or framework-specific syntax (pseudo-code sketches are allowed)
- Add git commands, commit choreography, or exact test command recipes
- Add generic `Research Insights` subsections everywhere
- Rewrite the entire plan from scratch
- Invent new product requirements, scope changes, or success criteria without surfacing them explicitly

If research reveals a product-level ambiguity: record it under `Open Questions` and recommend `ce:brainstorm` if the gap is truly product-defining.

##### 5.3.8 Document Review

After the confidence check (and any deepening), run the `document-review` skill on the plan file. Pass the plan path as the argument. This step is mandatory — do not skip it because the confidence check already ran. The two tools catch different classes of issues.

If document-review returns findings that were auto-applied, note them briefly when presenting handoff options. If residual P0/P1 findings were surfaced, mention them so the user can decide whether to address them before proceeding.

**Pipeline mode:** Run `document-review` with `mode:headless` and the plan path.

##### 5.3.9 Final Checks and Cleanup

Before proceeding to post-generation options:
- Confirm the plan is stronger in specific ways, not merely longer
- Confirm the planning boundary is intact
- Confirm origin decisions were preserved when an origin document exists

If artifact-backed mode was used, clean up the temporary scratch directory.

#### 5.4 Post-Generation Options

**Pipeline mode:** Skip the interactive menu and return control to the caller immediately.

After document-review completes, present options and wait for the user's reply:

**Question:** "Plan ready at `docs/plans/YYYY-MM-DD-NNN-<type>-<name>-plan.md`. What would you like to do next?"

**Options:**
1. **Start `ce:work`** — Begin implementing this plan (recommended)
2. **Open plan in editor** — Open the plan file for review
3. **Run additional document review** — Another pass for further refinement
4. **Share to Proof** — Upload the plan for collaborative review and sharing (uses `proof` CLI tool if available)
5. **Start `ce:work` in another session** — Begin implementing in a separate agent session when the current platform supports it
6. **Create Issue** — Create an issue in the configured tracker

**Issue creation:** When the user selects "Create Issue", detect the project tracker from `AGENTS.md` (check for `project_tracker: github` or `project_tracker: linear`). Create the issue using the appropriate tool. Display the issue URL. Ask whether to proceed to `ce:work`.

## Quality Gates

- Plan file written to disk before presenting options
- All feature-bearing units have actual test scenarios (not blank fields)
- All decisions have rationale
- Exact file paths included for every implementation unit
- Deferred items are explicit, not hidden as fake certainty
- No implementation code in the plan
- If an origin document exists, every section of it is addressed in the plan
- `document-review` has run on the final plan

## Outputs

- Plan file at `docs/plans/YYYY-MM-DD-NNN-<type>-<descriptive-name>-plan.md`
- Optional: related GitHub/Linear issue

## Feeds Into

- `ce:work` — executes the plan
- `document-review` — for additional review passes
