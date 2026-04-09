---
name: IssueTriage
description: Bug investigation and issue management -- triage GitHub issues via label-based state machine, investigate bugs for root cause with TDD fix plans, and run interactive QA sessions. USE WHEN triage issues, review bugs, needs-triage, ready-for-agent, issue workflow, investigate bug, root cause, diagnose problem, TDD fix plan, QA session, report bugs, file issues, conversational QA, agent brief.
---

## Status Update

When beginning a workflow, emit:
`Running the **[WorkflowName]** workflow in the **IssueTriage** skill to [ACTION]...`

# Issue Triage

Three workflows for managing the lifecycle of bugs and issues: systematic triage, root cause investigation, and conversational QA. All produce durable, behavior-focused GitHub issues.

## Core Principles

- **Investigate before filing** -- Explore the codebase to find root cause before creating an issue. No vague bug reports.
- **Durable issues** -- No file paths or line numbers. Use the project's domain language. Describe behaviors, not code.
- **TDD fix plans** -- Every bug gets a concrete plan of RED-GREEN cycles that address the root cause through behavior tests.
- **Agent briefs** -- Issues marked `ready-for-agent` get structured specifications an autonomous agent can work from. See `references/AgentBrief.md`.
- **Institutional memory** -- Track rejected features in an out-of-scope knowledge base to prevent relitigating decisions. See `references/OutOfScope.md`.

## Workflow Routing

| Intent | Workflow |
|--------|----------|
| Triage incoming GitHub issues using labels and state machine | `workflows/GithubTriage.md` |
| Investigate a specific bug and file an issue with a TDD fix plan | `workflows/TriageIssue.md` |
| Run an interactive QA session where the user reports problems | `workflows/QASession.md` |

## Output Format

- **GithubTriage** -- Label transitions, triage notes, agent briefs, or out-of-scope entries depending on the outcome
- **TriageIssue** -- GitHub issue with: Problem (actual vs expected), Root Cause Analysis, TDD Fix Plan (RED-GREEN cycles), Acceptance Criteria
- **QASession** -- One or more GitHub issues per reported problem with: What happened, What I expected, Steps to reproduce, Additional context
