---
name: Lightweight Plan Template
description: Lighter alternative plan template -- core sections only (Abstract through Open Questions), no add-on sections
tags:
  - area/ea
  - kind/template
  - status/stable
date_updated: 2026-04-04
---

# {{ FEATURE_OR_SPEC_TITLE }}

## Abstract

<!-- The assistant AI must summarize what is proposed, for whom, and the expected outcome. Keep this short and concrete. -->

## Motivation

<!-- The assistant AI must explain the problem, current pain, why now, and why the current state is not sufficient. Add product, technical, or business context only when it directly helps. -->

## Non-Goals

- **NG_01:** {{ out of scope 1 }}
- **NG_02:** {{ out of scope 2 }}

<!-- The assistant AI must define what this spec does not attempt to solve. -->

## Use Cases

### UC_01 — {{ short name }}

**Actor:** {{ user, system, admin, API consumer }}

**Scenario:** {{ starting situation }}

**Expected Outcome:** {{ expected result }}

### UC_02 — {{ short name }}

<!-- The assistant AI must keep use cases concrete and tied to real usage. Add edge or negative flows here only when they are best described as scenarios. -->

## Functional Requirements

- **REQ_01:** {{ The system must... }}
- **REQ_02:** {{ The service must reject... }}
- **REQ_03:** {{ The interface must display... }}

<!-- The assistant AI must write clear, testable, and unambiguous requirements, including core business rules, permissions, or calculations. Prefer formulations such as "The system must...", "The service must reject...", or "The interface must display...". Add lightweight references when helpful, for example "(covers: UC_01)". -->

## Acceptance Criteria

- **ACC_01:** {{ Observable behavior... Validates: REQ_01 or Covers: REQ_01 }}
- **ACC_02:** {{ Observable behavior... Validates: REQ_01 or Covers:REQ_01 }}
- **ACC_03:** {{ Observable behavior... Validates: REQ_02, REQ_03 or Covers: REQ_02, REQ_03 }}

<!-- The assistant AI must write behavioral acceptance criteria, not implementation tasks or test steps. Acceptance Criteria define what must be true in production or in user-observable/system-observable behavior. Every Acceptance Criterion must validate at least one requirement, for example "(validates: REQ_02)". -->

## Open Question and Decisions

<!-- Reviewers do not write in the plan. They create standalone `review-*.md` files in the same feature directory. The Product Manager (PM) reads all pending review files, updates the plan to reflect accepted decisions, rejected suggestions that matter for future review, and unresolved questions, records durable outcomes in `Open Question and Decisions`, and deletes the consumed review files after consolidation. The commit agent is the only role that creates commits. Git history serves as the audit trail. If there are no open questions, write "None". example:

```md
**QST_{XX}:** {{ concise question, concern, or decision topic }}
- **DECISION:** {{ selected answer. }}. RATIONALE: {{ short reason this choice stands }} ({timestamp})
```
-->

<!--
Why is this section so important?
The key is to stop having to re-ask the same question (or suggestions) over and over when we are reviewing the plan. 
Imagine we do 90 reviews of course, many ideas will come over and again and again. 
-->

## Assumptions / Dependencies *(add-on)*

<!-- The assistant AI must capture only relevant assumptions or dependencies, such as an external service, a prior migration, another feature, or a product/technical assumption. Delete this section if it adds no value. -->

<!-- Use these sections only when they materially reduce ambiguity. Delete the rest. -->

<!-- ============ END of this template ============ -->

<!--
RULES:

The assistant AI must:

- write clearly and concisely without filler
- complete all Core sections
- add Add-on sections only when they materially reduce ambiguity; otherwise delete them
- if a fact is unknown, write "Unknown" or move it to Open Question and Decisions
- for trivial or highly visual features, Functional Requirements can be omitted if the Acceptance Criteria alone perfectly describe the system rules without ambiguity.
- write testable requirements and observable acceptance criteria
- keep use cases grounded in real usage
- reviewer passes must not edit the plan directly; they create standalone `review_*.md` artifacts in the same feature directory as the plan
- the PM is the only role that resolves reviewer items by updating the plan and turning durable outcomes into in-place decisions in Open Question and Decisions
- the commit agent is the only role that creates commits in this workflow
- resolved decision-log entries should record the chosen direction with concise inline rationale so future reviewers do not repeat the same feedback churn
- use stable IDs:
  - QST_01
  - UC_01
  - NG_01
  - REQ_01
  - ACC_01
- When the PM (or assistant AI acting as PM) resolves an Open Question, the PM must update the relevant Use Cases, requirements, or Acceptance Criteria to reflect the finalized decision, rather than leaving the spec and the decision out of sync.
- use lightweight inline traceability:
  - REQ_02 (covers: UC_01) when helpful
  - every Acceptance Criterion must validate at least one requirement, for example: ACC_03 (validates: REQ_02)
- do not renumber existing IDs after review
- retire IDs instead of reusing them by replacing the text with "[RETIRED]" (e.g., `- **REQ_02:** [RETIRED]`).
- keep the document concise and avoid speculative detail
- avoid roadmap filler
- do not invent stakeholders, business value, metrics, or technical constraints
- avoid generic business value claims unless they are measurable or directly tied to the problem
- do not use vague claims such as "improves UX", "ensures scalability", or "increases flexibility" unless tied to a specific problem or measurable effect
- avoid repeating the same information across sections
- NOT simply restate Use Cases as Functional Requirements; requirements must define system rules, limits, state changes, or calculations.
- prefer concrete facts over inferred rationale
-->

## Related

- [[plan-template-prd]]
- [[bdd-principles-for-plans]]
- [[1004-feature-plan-template]]
