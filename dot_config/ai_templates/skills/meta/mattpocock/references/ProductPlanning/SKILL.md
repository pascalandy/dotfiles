---
name: ProductPlanning
description: Product planning pipeline -- write PRDs through relentless interviews, convert to phased plans with tracer-bullet vertical slices, break into independently-grabbable GitHub issues, and stress-test designs. USE WHEN write PRD, product requirements, plan feature, create issues, vertical slices, tracer bullets, grill me, stress-test plan, interview about design, user stories, phased plan, HITL, AFK, decision tree.
---

## Status Update

When beginning a workflow, emit:
`Running the **[WorkflowName]** workflow in the **ProductPlanning** skill to [ACTION]...`

# Product Planning

The full pipeline from problem to work items. Four workflows covering each stage of product planning, all grounded in vertical-slice thinking and relentless interviewing.

## Core Principles

- **Vertical slices (tracer bullets)** -- Every plan and issue is a thin end-to-end slice through ALL integration layers, not a horizontal cut at one layer. Each slice is demoable and verifiable on its own.
- **Relentless interviewing** -- Walk every branch of the decision tree one question at a time. If a question can be answered by exploring the codebase, explore instead of asking.
- **Durable descriptions** -- No file paths or line numbers. Describe interfaces, types, and behavioral contracts that survive refactors.
- **Deep module awareness** -- During PRD writing, sketch major modules and look for deep module opportunities (small interface, significant hidden complexity).

## Workflow Routing

| Intent | Workflow |
|--------|----------|
| Write a PRD, define requirements, plan a new feature | `workflows/WritePRD.md` |
| Convert a PRD to a phased implementation plan | `workflows/PRDToPlan.md` |
| Break a PRD into GitHub issues | `workflows/PRDToIssues.md` |
| Stress-test a plan or design through exhaustive questioning | `workflows/GrillMe.md` |

## Output Format

All workflows produce structured artifacts:

- **WritePRD** -- GitHub issue with: Problem Statement, Solution, User Stories, Implementation Decisions, Testing Decisions, Out of Scope
- **PRDToPlan** -- Markdown file in `./plans/` with: Architectural Decisions, Phased Vertical Slices with Acceptance Criteria
- **PRDToIssues** -- GitHub issues with: Parent PRD reference, End-to-end behavior, Acceptance Criteria, Dependencies, User Stories addressed
- **GrillMe** -- Shared understanding through exhaustive Q&A; no written artifact, the value is the refined thinking
