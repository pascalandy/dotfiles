---
links:
  - "[rel path/[PRD Title]]"
  - "[Link / path / note]"
owner: "Pascal Andy"
status: "[Draft / In Progress / Ready / Shipped / Parked]"
date_updated: "[YYYY-MM-DD] / v0.1"
---

<!--
Before drafting this document, read the @pm expectations comment at the end of this file.
-->

# PRD Template

## 1. Abstract

`[Write 1-2 short paragraphs.]`

## 2. Motivation

`[Write 1-3 short paragraphs.]`

## 3. Scope Overview

### In Scope
- `[Major capability]`
- ..

### Out of Scope for This Version
- `[Deferred item]`
- ..

### Assumptions
- `[Assumption about users, distribution, implementation speed, budget, or AI support]`
- ..

## 4. Experience Overview

### Core User Journey
1. `[Start]`
2. `[User or AI takes action]`
3. `[System responds]`
4. `[Outcome is delivered]`

### Happy Path
`[Describe the default end-to-end flow.]`

### UX / Interaction Notes
`[Anything important about defaults, clarity, speed, visibility, trust, or control.]`

## 5. Functional Spec

# COMPONENT 1: `[Major Capability Area]`

### COMPONENT Goal
`[What this area is meant to accomplish.]`

### Why This COMPONENT Exists
`[What value this COMPONENT creates for the product or business.]`

### Optional Workflow Diagram

```mermaid
flowchart TD
    A[[Start]] --> B[First step]
    B --> C[Second step]
    C --> D[[Outcome]]
```

## FEAT 1.1: `[Feature Name]`

### What It Does
`[One concise paragraph describing the capability.]`

`[Why this FEAT exists and what it unlocks.]`

### How It Works
- `[Key behavior or mechanism]`
- `[What the user sees, does, receives, or controls.]`

- ..
### Inputs
- `[Input source]`
- ..

### Outputs
- `[Output / artifact / visible result]`
- ..

### Product Rules / Constraints
- `[Rule, limit, or product constraint]`
- ..

### Edge Cases / Failure Handling
- `[Failure mode and expected behavior]`
- ..

### Acceptance Criteria
- `[Observable condition that proves this works]`
- ..

## 6. Cross-Cutting Concerns, Risks, and Open Questions

### Security
- `[Access, data, permission, or trust requirement]`
- `[Sensitive operation rule]`

### Reliability
- `[Failure, interruption, recovery, or fallback rule]`
- `[What should happen under partial failure]`

### Performance
- `[Latency, responsiveness, or throughput expectation]`
- `[Known tradeoff worth documenting]`

### Observability
- `[What needs to be visible during operation or after failure]`
- `[What signals indicate health or progress]`

### Known Risks
- `[Risk]`
- ..

### Unknowns
- `[Unknown that needs research, validation, or prototyping]`
- ..

### Open Questions
- `[Question]`
- ..

## 7. Delivery Plan

### Execution Tree

**COMPONENT 1 (p1) @pm**
├── FEAT 1.1 @engineer_II
├── FEAT 1.2 @engineer_II
└── ..

**COMPONENT 2 (p2) @pm ← COMPONENT 1**
├── FEAT 2.1 @engineer_II
└── FEAT 2.2 @engineer_II

**COMPONENT 3 (p3) @pm ← COMPONENT 1, COMPONENT 2**
├── FEAT 3.1 @engineer_II
└── ..

### External Dependencies
- `[Dependency]`
- ..

## 8. Evolution

- `[Deferred capability]` — `[Why it matters]`
- ..

## 9. Annexes (Optional)

## 10. Acceptance Plan (E2E QA)

### Test Strategy
- `[Explain the overall E2E testing approach in 3-6 bullets.]`
- `[State what must be covered before ship.]`
- `[State what can be deferred.]`
- `[State what environments or data setup are required.]`

### Affected Pages/Routes
- `[URL path] — [what to test and why]`

### Key Interactions to Verify
- `[interaction description] on [page / route]`

### Edge Cases
- `[edge case] on [page / route / flow]`

### Critical Paths
- `[end-to-end flow that must work]`

### E2E Ticket List

#### 10.1 `[Atomic E2E ticket]`
- Type: `[Core flow]`
- Covers flow: `[Single user flow or validation target]`
- Covers FEATs:
  - `[FEAT 1.1]`
  - `[FEAT 1.2]`
  - `[FEAT 2.1]`
- Does not cover: `[Adjacent behavior left to another ticket]`
- Preconditions: `[Only if needed]`
- Steps:
  1. `[Step]`
  2. `[Step]`
  3. `[Step]`
- Expected result:
  - `[Result]`
  - `[Result]`

### Ship Readiness Checklist (final E2E test)
- `[All critical E2E tickets pass]`
- `[All blocker bugs from E2E are fixed or explicitly accepted]`
- `[Core user journey has atomic ticket coverage]`
- `[Important edge cases have atomic ticket coverage]`
- `[Known risks reviewed against actual E2E results]`

<!--

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 0. Introduction
EXPECTATIONS about this document.

This template is optimized for a solo founder working with AI assistants.

Before drafting, the AI assistant must also read `bdd_principles.md` in the same directory as this template.
That document defines the writing principles (concrete examples, domain language, declarative style, etc.) that apply across every section of the plan.

When the AI assistant has a question for the user, always leave a comment starting with the flag: 0o0o
- These four characters make it easy for the user to find items that need attention.

Use this document for:
- product focus; leave out architecture and implementation design
- scope
- workflow shape
- FEAT breakdown
- launch planning

This PRD may include build-order and acceptance-test planning when those details help define scope and ship readiness.

- definitions:
  - COMPONENT = major product area
  - FEAT = feature inside a COMPONENT

- template_version: v2.1

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 1. Abstract
The AI assistant must summarize what is proposed, for whom, and the expected outcome. Keep this short and concrete.

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 2. Motivation
The AI assistant must explain the problem, current pain, why now, and why the current state is not sufficient.
Add product, technical, or business context only when it directly helps.

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 3. Scope Overview
Be explicit.
For solo work, this section is one of the main defenses against accidental bloat.

`Out of Scope for This Version` is a hard boundary — items explicitly excluded from the current version.
Keep it lean and firm. No rationale needed here; just the line in the sand.

Do not use `Out of Scope` to park future ideas. Deferred ideas with future value belong in Section 8 (Evolution).
The distinction matters:
- Out of Scope = "We are not doing this now. Stop asking."
- Evolution = "We want this later. Here is rough thinking on why and when."

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 5. Functional Spec
Terminology rules:
- COMPONENT = a major product area or workstream.
- FEAT = a concrete capability inside a COMPONENT.

Authoring rules:
- Organize the PRD by COMPONENTS and FEATs.
- Use optional workflow diagrams only when they clarify the experience.
- Keep implementation planning separate from product structure.
- Copy the COMPONENT block as many times as needed.
- Prefer multiple small FEATs over giant vague sections.

Workflow diagram:
- Use this only if flow or sequencing matters.
- If a COMPONENT does not need a workflow diagram, delete that subsection.
- Mermaid is preferred over tables here.
- Replace the example with a real flow only when it adds clarity.
- Do not force a diagram into every COMPONENT.

FEAT guidance:
- Keep this section product-facing.
- If the AI assistant feels tempted to specify schema fields or endpoint payloads, move that to the Technical Spec.
- Duplicate more FEAT blocks as needed by copying FEAT 1.1 and trimming or expanding it based on the actual FEAT.

FEAT subsection structure (v1.1):
- `What It Does`: Covers both the capability and why it matters. Do not create a separate "Why It Matters" subsection — if the reason is not obvious from context, add it as a bullet here.
- `How It Works`: Covers mechanism and user-facing behavior together. In a product-facing document, describing how a feature works already describes what the user sees. Do not create a separate "User-Facing Behavior" subsection.
- `Inputs` / `Outputs`: What goes in, what comes out.
- `Product Rules / Constraints`: Limits, rules, guardrails. For every rule, the AI assistant must generate 2-3 concrete examples that disambiguate it (principles from BDD). A rule without examples is ambiguous by definition. Format: state the rule, then show what happens with specific inputs.
  - Bad: "Loyal customers get a discount."
  - Good: "Customers with 12+ months of tenure receive 15% off. Example: Marie, 14 months, 100$ cart → pays 85$. Example: Paul, 3 months, 100$ cart → pays 100$. Example: Luc, exactly 12 months → pays 85$."
  - If the AI assistant cannot generate concrete examples for a rule, the rule is not understood well enough. Flag it as an open question in Section 6.
- `Edge Cases / Failure Handling`: What breaks and what happens when it does.
- `Acceptance Criteria`: Observable conditions that prove the FEAT works. Each criterion must include a concrete scenario with specific data, not an abstract assertion (principles from BDD). The AI assistant must write criteria that a reviewer can mentally execute and say "yes, that is correct" or "no, that is wrong."
  - Bad: "User can cancel within 24h."
  - Good: "Marie places an order at 14:00 Monday. She cancels at 13:59 Tuesday → cancellation succeeds. She cancels at 14:01 Tuesday → cancellation is refused with message 'Cancellation window has passed.'"
- No `Dependencies` subsection at the FEAT level. Dependencies are managed in the Delivery Plan (Section 7) using `←` notation. Duplicating them per FEAT creates drift.

Additional COMPONENTS:
- Add as many COMPONENTS as needed.
- Recommended pattern:
  - COMPONENTS describe the product shape.
  - FEATs describe the capabilities.
- Do not rewrite the template for each COMPONENT unless the COMPONENT genuinely needs a different shape.

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 6. Cross-Cutting Concerns, Risks, and Open Questions
Do not hide uncertainty.
Do not let the cross-cutting checklist bury:
- the real risks
- unknowns
- unresolved questions

This section should help the AI assistant decide whether to ship, prototype, or narrow scope.

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 7. Delivery Plan
Keep this simple.
- Use only the planning concepts defined in this template.
- Do not invent additional frameworks, labels, or sections here.
- If planning gets detailed, move it to a separate execution or project plan.
- This section is for build order only.
- Stay anchored to COMPONENTS and FEATs.

Keys:
  ```yaml
  priority:
    p1: high
    p2: medium
    p3: low
    # p0 and p4 are reserved

  assignee:
    @pm: Product Manager
    @engineer_I: Entry SWE I
    @engineer_II: Mid SWE II (default)
    @engineer_III: Senior SWE III / Senior SWE
    @qa: Quality Assurance
    @qa-e2e: E2E Quality Assurance

  dependency:
    ←: depends on
  ```

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 8. Evolution
This section captures ideas that are explicitly out of scope for the current version but worth preserving for future iterations.

Why this section exists:
- `Out of Scope` in Section 3 is a hard boundary. Its job is to say "no" and protect the current version from creep.
- `Evolution` is forward-looking. Its job is to say "not yet" and preserve ideas that have future value.
- Without this section, deferred ideas end up in `Out of Scope` where they are framed as rejections and forgotten.
- With this section, the PM and reviewers can explicitly distinguish between "rejected" and "deferred with intent."

Rules:
- Do not turn this section into a backlog. Keep it to the 3-7 most important items.
- Each item needs a one-line rationale. Bare bullet lists without context lose their value across sessions.
- Do not describe implementation. This is product-level thinking: what and why, not how.
- If an item in `Out of Scope` (Section 3) has future value, it should appear here too. The duplication is intentional — different framing for different purposes.

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 9. Annexes (Optional)
Use this section as annex material if needed.
Only for useful supporting material that helps execution or review, but does not belong in the core PRD structure.

Examples:
- links to related issues, tasks, or project notes, reference maps
- official docs, market references, or policy pages
- diagrams, mockups, or external artifacts

Keep it lightweight.
Do not move core product requirements here.

Annex examples:
- Related Issues / Tasks
- Official Docs / References
- Diagrams / Artifacts
- Other Notes

=—=—=—=—=—=—=—=—=—=—=—=—=—=—=
## 10. Acceptance Plan (E2E QA)
This section is extremely important.

The AI assistant should strongly recommend this section by default.
It may be skipped only for very small FEATs or COMPONENTS with no meaningful end-to-end flow and no separate acceptance risk.

Rules:
- plan the E2E work as separate tickets
- make each ticket atomic and easy to validate
- prefer many small tests over a few large tests
- make it obvious what each ticket covers and what it does not cover
- each E2E ticket should verify one flow, one edge case, or one failure mode
- do not write vague test buckets such as "test onboarding" or "test payments"

Good:
- "User signs up with valid email"
- "User sees validation error for invalid email"
- "User retries payment after card decline"

Bad:
- "Test auth"
- "Test checkout"
- "Test everything around uploads"

Before writing the `10.x` tickets, the AI assistant should identify:
- critical paths that must work before ship
- important edge cases
- affected pages/routes if this is a UI product
- key interactions to verify if this is a UI product
- how tests are run (for example via `just`) when that context helps define the acceptance plan
- which behaviors need unit, integration, or E2E coverage at a high level

Delete any subsection that does not apply.
Do not add API contracts, CLI contracts, service contracts, or technical design material here.

Ticketing rules:
- Every E2E test must become its own ticket under section `10.x`.
- Every ticket must be independently executable.
- Every ticket must have a single clear pass/fail outcome.
- Every ticket must name the exact flow, edge case, or failure mode being tested.
- Every ticket must explicitly list the FEAT IDs it covers.
- A single atomic E2E ticket may cover multiple FEATs.
- Use explicit references such as `FEAT 1.1`, `FEAT 1.2`, `FEAT 2.3`.
- Use `Preconditions` only when the test needs specific state, data, or environment setup.
- Add as many `10.x` atomic E2E tickets as needed.

About beads:
- When creating beads (`bd`) tasks, assignee="qa-e2e"
- In beads, they live under an EPIC. That Beads EPIC is a task-management concept.
- Recommended approach:
  - for each COMPONENT, create the implementation EPIC first
  - then create a separate code-review EPIC using skill `review-diff`
  - then create a separate Acceptance Plan (E2E QA) EPIC
  - the Acceptance Plan (E2E QA) EPIC must depend on the previous implementation EPICs it needs
  - create one child beads task per `10.x` E2E ticket under the Acceptance Plan (E2E QA) EPIC
  - create logical dependencies between these EPICs
- These tests should not be run by the developer who implemented the related FEATs.
- They should be run by someone else acting as the tester.
- That is why this work lives in a separate Beads EPIC.

The AI assistant should generate enough atomic tickets so that:
- the main flows are covered
- the important failures are covered
- each ticket stays small and easy to execute

-->
