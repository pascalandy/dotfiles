---
name: Scope
description: `pa-scope` is the scoping entry point — use it to decide what is in play for a requested change
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - pa-sdlc
---

Scope is the second stage of `pa-sdlc`. Load it with the explicit entry point `pa-scope`.

Use Scope when a change has been requested and the question is "what does this touch?". It owns one decision: the touch surface, the blast radius, and whether a specific artifact belongs in scope at all.

Source: `dot_config/ai_templates/skills/pa-sdlc/pa-scope/SKILL.md`.

## When to reach for Scope

| Situation | Why Scope |
|---|---|
| A change has been requested and you need the likely touch surface. | Scope's ChangeSurface mode builds a bounded map of the primary and adjacent surfaces. |
| You already know the starting artifact and need propagation paths. | Scope's ImpactTrace mode walks upstream and downstream dependencies. |
| You must decide whether one file, page, or module belongs in scope. | Scope's ArtifactClarifier mode answers yes/no for exactly one artifact. |

Scope is a factual stage. It produces a surface map — not a plan, not a direction, not an implementation.

## Three internal modes

| Mode | Owns | Use when |
|---|---|---|
| `ChangeSurface` | Bounded scope map | You need the likely primary and adjacent surfaces |
| `ImpactTrace` | Blast-radius tracing | You already know the starting artifact and need propagation paths |
| `ArtifactClarifier` | One scoping decision around one artifact | You must understand one file, page, workflow, or note before including it |

## Default output shape

A Scope brief covers:

1. **Requested change** — the ticket or feature, verbatim.
2. **Primary scope** — the files, modules, or artifacts most likely to change.
3. **Adjacent affected areas** — surfaces that are not primary but may need updates (tests, docs, config).
4. **Relationship paths** — how primary and adjacent connect, the dependency edges.
5. **Validation surfaces** — where a change to the primary scope would show up (tests, logs, UI, observability).
6. **Risks and unknowns** — what you could not verify, what might explode.
7. **Recommended next step** — usually a pointer to Vision, Architect, or Implement depending on how much uncertainty remains.

## Boundaries — when *not* to use Scope

| Real need | Reach for |
|---|---|
| Broad orientation or current-state research | [[scout]] |
| Deciding whether the direction is right | [[vision]] |
| Designing execution or sequencing work | [[architect]] |
| Building the change or fixing the bug | [[implement]] |
| Documenting the result or one concrete artifact | [[doc-update]] |
| Refreshing, deduplicating, or repairing existing docs | [[doc-cleaner]] |

## The "hidden ticket" trick

Scope's ChangeSurface mode often deliberately *hides* the original feature ticket during the factual-gathering phase. The reason: reading the ticket first biases the search toward the narrative the ticket already implies. Gathering facts with the ticket concealed produces a more honest map of what actually exists, which is then compared against the ticket in a second pass.

This is not paranoia — it is a defense against the "plan-reading illusion" where a plausible-sounding plan built on a biased factual base feels trustworthy but is wrong.

## Scope vs. Architect

These are often confused because both produce "plans". They are not the same.

| | Scope | Architect |
|---|---|---|
| Question | "What is in play?" | "How do we get there?" |
| Output | Surface map | Execution sequence |
| Owns opinions? | No — factual only | Yes — slices, risks, checkpoints |
| Timing | Before direction is settled | After direction is settled |

A Scope output says "these files will change". An Architect output says "change them in this order, with these checkpoints, starting with this slice".

## Related

- [[scout]]
- [[vision]]
- [[architect]]
- [[advisor]]
- source: `dot_config/ai_templates/skills/pa-sdlc/pa-scope/SKILL.md`
