---
name: ArtifactClarifier
description: Explain one artifact in context so it can be included or excluded from scope. USE WHEN the user needs to understand a specific file, module, page, workflow, board, note, or document before deciding whether it matters to the requested change.
---

# ArtifactClarifier

## When To Use

Use this mode when one candidate artifact is ambiguous and the scoping decision depends on understanding its role.

If the user only wants a descriptive explanation of current state with no scoping decision attached, hand off to Scout's `TargetedInquiry` mode instead.

Typical triggers:

- Explain this file before I change anything
- Does this page belong in scope?
- What does this workflow actually control?
- Help me understand this artifact so I can decide whether it matters

This mode should resolve ambiguity around one area, not scope the whole system.

## Core Method

1. Identify the artifact and the scoping decision around it.
2. Explain its role, inputs, outputs, and neighboring connections.
3. Clarify how it relates to the requested change.
4. State whether it looks in scope, adjacent, or irrelevant based on current evidence.
5. Call out any unknowns that block a confident scoping judgment.

## Subject Adaptation Rules

- For code, explain the module's role, interfaces, dependencies, data flow, and test relevance.
- For websites or content systems, explain the page, template, model, rule, or workflow and how it influences user-facing output.
- For PM systems, explain the board, field, automation, report, or status rule and how it participates in the process.
- For knowledge systems, explain the note, hub, index, or taxonomy artifact and its routing role.
- For personal workflows, explain the tracker, document, routine, or plan and its role in the broader system.

## Workflow

1. Restate the artifact and the user's uncertainty.
2. Read the smallest set of evidence needed to explain it.
3. Describe its purpose and connections.
4. Judge its relevance to the requested change.
5. Recommend whether to continue with `ChangeSurface`, `ImpactTrace`, or another SDLC phase.

## Output Format

Produce these sections:

1. `Requested Change`
2. `Artifact Role`
3. `Why It Matters For Scope`
4. `Immediate Connections`
5. `Unknowns`
6. `Recommended Next Step`

This mode is intentionally lighter than the other Scope modes.

- `Artifact Role` should explain what the artifact does in context.
- `Why It Matters For Scope` should judge whether it looks in scope, adjacent, or irrelevant.
- `Immediate Connections` should show only the nearest important links.
- `Recommended Next Step` should usually hand off to `ChangeSurface` or `ImpactTrace` when the ambiguity is resolved.

## Examples

- "Explain what this service actually owns."
- "Does this template matter for the requested homepage update?"
- "What does this recurring-review note control in the workflow?"

## Boundaries

- Stay centered on one artifact or tightly bounded area.
- Do not broaden into full onboarding or architecture research.
- Do not use this for generic current-state explanation without a scoping decision; that belongs to Scout's `TargetedInquiry` mode.
- Do not drift into plan-writing or implementation advice.
- If the artifact cannot be understood with confidence, say that directly and state what evidence is missing.
