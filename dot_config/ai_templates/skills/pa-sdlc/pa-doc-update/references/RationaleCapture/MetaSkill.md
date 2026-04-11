---
name: RationaleCapture
description: Capture why something was decided or why something happened across code, content, workflow, or knowledge systems. USE WHEN the user wants an ADR, a decision record, a postmortem, lessons learned, tradeoff documentation, or another artifact centered on rationale and consequences.
---

# RationaleCapture

## When To Use

Use this mode when the main value is preserving the why.

Typical triggers:

- ADR this
- Record this decision
- Why did we choose this?
- Write a postmortem
- Capture lessons learned

This mode should produce rationale-rich documentation, not a release summary and not a generic current-state reference.

Entry condition: the decision, incident, or lesson already exists. `RationaleCapture` documents it after the fact. If the user is still deciding what to do, route to the earlier SDLC phase that owns product definition, planning, or problem-solving.

## Core Method

1. Identify the decision, incident, or lesson that needs to be preserved.
2. Gather the motivating context and constraints.
3. Capture the alternatives, contributing factors, or failed paths when they matter.
4. State the actual conclusion, root cause, or lesson plainly.
5. Record the consequences, risks, and follow-up implications.
6. End with the next recommended step: `ChangeCapture` if shipped-change docs are also needed, `ArtifactDocumenter` if the artifact itself now needs a current-state reference, otherwise finish the rationale capture.

## Subject Adaptation Rules

- For code, prioritize architectural decisions, technical tradeoffs, root causes, and follow-up constraints.
- For websites or content systems, prioritize content strategy decisions, publishing incidents, UX rationale, and operational lessons.
- For PM systems, prioritize process changes, automation decisions, workflow failures, and retrospective learnings.
- For knowledge systems, prioritize taxonomy decisions, routing changes, note-structure rationale, and failures in discoverability that are already decided or concluded; do not perform index or routing maintenance as part of this mode.
- For personal workflows, prioritize habit decisions, planning tradeoffs, missed expectations, and reflective lessons.

## Workflow

1. Clarify whether this is a decision record, incident review, or lessons-learned capture.
2. Gather the strongest evidence for context and outcome.
3. Separate facts from interpretation.
4. Make alternatives, causes, and consequences explicit.
5. Produce the rationale artifact in a durable, reviewable form.

## Output Format

Produce these sections:

1. `Documentation Objective`
2. `Primary Target`
3. `Evidence Used`
4. `Key Content To Capture`
5. `Canonical Placement Or Output Shape`
6. `Cross-References And Dependencies`
7. `Risks And Unknowns`
8. `Recommended Next Step`

Within `Key Content To Capture`, emphasize context, alternatives, rationale, consequences, timeline, or lessons depending on the request.

## Examples

- "Record why we chose this approach over the other one."
- "Write a postmortem for this incident."
- "Capture the main lessons from this failed workflow experiment."

## Boundaries

- Keep the focus on why, not on documenting every changed surface.
- Do not collapse into a changelog or release-note style summary.
- Do not produce generic artifact reference docs unless the user is actually asking for current-state documentation.
- Do not drift into long-term governance or documentation-system maintenance.
- Do not use this mode to make the decision, redesign the process, or run the planning work itself.
