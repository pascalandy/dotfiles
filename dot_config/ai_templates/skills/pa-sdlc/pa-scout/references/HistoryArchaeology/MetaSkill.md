---
name: HistoryArchaeology
description: Historical and evolutionary analysis for understanding why a repository, workspace, content system, project surface, knowledge base, or personal context looks the way it does today. USE WHEN revision history, chronology, or change archaeology matters more than current-state scanning alone.
---

# HistoryArchaeology

## When To Use

Use this mode when static inspection is not enough and the user needs historical context.

Typical triggers:

- Why is it structured this way?
- How did this evolve?
- Who changed this?
- What are the major turning points?

## Core Method

1. Identify the relevant history source.
2. Trace major changes over time.
3. Map contributors, owners, or stewards when possible.
4. Connect historical events to the current structure.
5. Separate evidence from interpretation.

## Subject Adaptation Rules

- For code repositories, use revision history, blame, change clustering, and related files.
- For content systems, use revision logs, page history, migrations, and template changes.
- For PM systems, use workflow changes, archived artifacts, audit logs, and process updates.
- For knowledge systems, use note history, renames, reorganizations, and index evolution.

If no usable history exists, say so directly and fall back to current-state evidence only.

## Workflow

1. Define the historical question.
2. Gather timeline evidence from the available history surface.
3. Identify turning points, major refactors, reorganizations, or process changes.
4. Explain how those changes produced the present state.
5. Call out uncertainty where motives cannot be proven.

## Output Format

Produce these sections:

1. `Historical Question`
2. `Timeline Of Major Changes`
3. `Key Contributors Or Stewards`
4. `Patterns Of Change`
5. `How History Explains The Current State`
6. `Evidence`
7. `Unknowns`
8. `Recommended Next Scout Step`

## Examples

- "Why did this repo end up organized this way?"
- "Trace the major changes in this subsystem over time."

## Boundaries

- Do not romanticize or narrativize beyond the evidence.
- Do not assume version history exists.
- Do not use history as a substitute for current-state inspection when the current state is easy to observe directly.
