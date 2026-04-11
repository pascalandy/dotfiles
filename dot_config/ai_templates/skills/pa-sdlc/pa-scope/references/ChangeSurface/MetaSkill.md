---
name: ChangeSurface
description: Build a bounded scope map for a requested change across code, content, workflow, or knowledge systems. USE WHEN the user wants to know what is likely in play, which artifacts may need updates, which validation surfaces matter, and where the main risks live.
---

# ChangeSurface

## When To Use

Use this mode for the default Scope job when the user asks what they need to touch.

Typical triggers:

- What do I need to touch?
- Scope this change
- Which files or artifacts are likely involved?
- What should I validate if this changes?

This mode should produce a bounded scoping brief, not a full dependency graph and not a plan.

## Core Method

1. Restate the requested change in neutral terms.
2. Identify the primary artifacts most likely to bear the change.
3. Identify adjacent artifacts that may need updates, checks, or coordination.
4. Find validation surfaces such as tests, QA paths, review checkpoints, or operational checks.
5. Surface the main risks and unknowns.
6. End with the next recommended step: `ImpactTrace` or `ArtifactClarifier` if scoping is still incomplete, otherwise `pa-vision`, `pa-architect`, or `pa-implement` depending on how defined the change already is.

## Subject Adaptation Rules

- For code, prioritize feature-bearing files, dependencies, tests, configs, migrations, and reference patterns.
- For websites or content systems, prioritize pages, templates, models, publishing rules, assets, and QA paths.
- For PM systems, prioritize boards, statuses, automations, templates, reporting artifacts, and ownership boundaries.
- For knowledge systems, prioritize indexes, canonical notes, backlinks, naming conventions, and routing documents.
- For personal workflows, prioritize trackers, plans, routines, calendars, and supporting documents.

## Workflow

1. Clarify the requested change.
2. Search for the most direct implementation or ownership surfaces.
3. Expand one level outward to likely adjacent impact.
4. Find existing patterns or precedent worth following.
5. Find the validation surfaces that would confirm the scope.
6. Produce the bounded scope map.

## Output Format

Produce these sections:

1. `Requested Change`
2. `Primary Scope`
3. `Adjacent Or Potentially Affected Areas`
4. `Relationship Paths`
5. `Patterns To Follow`
6. `Validation Surfaces`
7. `Risks And Unknowns`
8. `Recommended Next Step`

When useful, represent `Primary Scope`, `Adjacent Or Potentially Affected Areas`, `Patterns To Follow`, and `Validation Surfaces` as tables. Omit sections that would add no signal for a tightly bounded request.

## Examples

- "Scope the work needed for this feature request."
- "What pages, templates, and checks are in play for this website update?"
- "Which boards and automations would this process change touch?"

## Boundaries

- Stay bounded. Do not broaden into a full repo or workspace tour.
- Prefer likely impact plus evidence over speculative completeness.
- Do not turn this into a deep relationship trace unless the user asks for blast radius explicitly.
- Do not turn this into a technical plan or implementation sequence.
