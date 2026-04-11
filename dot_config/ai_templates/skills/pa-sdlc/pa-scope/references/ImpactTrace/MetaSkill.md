---
name: ImpactTrace
description: Trace upstream and downstream relationships to measure blast radius across code, content, workflow, or knowledge systems. USE WHEN the user asks what depends on something, what will be affected by a change, or how impact propagates through connected artifacts.
---

# ImpactTrace

## When To Use

Use this mode when the user already knows the starting artifact and wants to understand propagation.

Typical triggers:

- What else breaks if I change this?
- What depends on this?
- Trace the blast radius
- Follow the upstream and downstream relationships

This mode should feel like a propagation map, not a broad scoping inventory.

## Core Method

1. Identify the starting artifact or relationship anchor.
2. Trace direct upstream and downstream connections.
3. Separate direct dependencies from second-order effects.
4. Highlight choke points, shared surfaces, and public interfaces.
5. Surface the best validation points for confirming the trace.
6. End with the next recommended step: `ChangeSurface` if the user still needs the broader touch surface, otherwise `pa-vision`, `pa-architect`, or `pa-implement` depending on how defined the change already is.

## Subject Adaptation Rules

- For code, trace callers, callees, imports, exports, shared types, configs, APIs, and tests.
- For websites or content systems, trace shared templates, content models, navigation surfaces, publishing dependencies, and downstream pages.
- For PM systems, trace automations, field dependencies, handoff rules, status transitions, and reports.
- For knowledge systems, trace canonical sources, backlinks, embeds, indexes, and taxonomy routes.
- For personal workflows, trace dependencies between routines, trackers, deadlines, and supporting artifacts.

## Workflow

1. Restate the starting point.
2. Trace direct outward relationships first.
3. Expand only where the chain materially changes the blast radius.
4. Classify findings into direct, adjacent, and uncertain propagation.
5. Produce a relationship-focused impact brief.

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

Within `Relationship Paths`, show the strongest dependency chains or propagation routes in the clearest compact format available.

## Examples

- "If we change this module, what else moves?"
- "Trace downstream impact from this content type."
- "What workflows depend on this board automation?"

## Boundaries

- Do not widen into a full change map unless the user needs the complete scope handoff.
- Do not treat every adjacency as equal; separate direct from plausible impact.
- Do not invent hidden dependencies when the evidence is weak.
- Do not plan the implementation or prescribe changes.
