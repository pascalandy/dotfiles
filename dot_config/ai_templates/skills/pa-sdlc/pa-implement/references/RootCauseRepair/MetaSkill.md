---
name: RootCauseRepair
description: Implementation repair mode for reproducing, diagnosing, and fixing broken behavior. USE WHEN something is failing, regressed, inconsistent, or otherwise broken and a trustworthy fix requires reproduction and root-cause reasoning before changes are applied.
---

# RootCauseRepair

## Purpose

Repair broken behavior responsibly.

This mode owns bug-shaped work inside Implement. It should not guess, patch blindly, or treat symptoms as root causes.

## Core Method

Use this sequence:

1. capture the reported symptom clearly
2. form hypotheses
3. reproduce the issue or failure mode
4. identify the root cause
5. apply the smallest trustworthy repair
6. verify the repaired behavior

## Rules

1. Do not fix first and explain later.
2. Reproduction is the default standard when the subject allows it.
3. If exact reproduction is impossible, state what evidence stands in for it.
4. Distinguish symptoms, contributing conditions, and root cause.
5. Keep the repair bounded to the explained problem unless new evidence expands the scope.
6. Verify the repaired path through a real or stakeholder-recognizable flow.

## Proof Styles By Subject

| Subject Type | Preferred Repair Proof |
|--------------|------------------------|
| Code repository | failing test, reproducible runtime path, logs, observable repaired behavior |
| Website or content system | broken path reproduced in preview or live-like environment, then visibly repaired |
| Project-management surface | failed transition or automation reproduced, then rerun successfully |
| Knowledge system | broken route, stale index, or retrieval failure reproduced, then resolved |
| Personal context | failure mode described concretely, then repaired through one validated operating path |

## Output Contract

For any structured artifact, use this exact shape. For a very small request, compress the same six anchors into prose without renaming them:

1. `Requested Change Or Problem`
2. `Execution Boundary`
3. `Work Performed Or Planned`
   Include `Symptoms And Conditions`, `Hypotheses`, `Reproduction Evidence`, `Root Cause`, and `Repair Applied` here. If the repair is still pending, say so explicitly.
4. `Verification Performed`
5. `Risks Or Unresolved Items`
6. `Recommended Next Phase`

## Handoffs

- Hand off to `pa-scout` when the real problem is still broad orientation.
- Hand off to `pa-scope` when the affected surface is still unclear.
- Hand off to `pa-architect` when the repair reveals a larger execution-design problem.
- Hand off to `ChangeApplication` when the bug is understood and the remaining work is ordinary bounded implementation.

## Non-Goals

Do not treat these as primary ownership here:

- feature planning
- architecture redesign without a concrete defect driver
- broad QA sweeps
- review-thread management
- shipping or PR management
