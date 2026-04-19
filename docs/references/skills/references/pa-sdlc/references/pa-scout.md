---
name: Scout
description: `pa-scout` is the discovery entry point — use it to understand what exists before deciding what to change
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - pa-sdlc
---

Scout is the first stage of `pa-sdlc`. Load it with the explicit entry point `pa-scout`.

Use Scout when the question is "what is this?" rather than "what should I change?". Scout is for orientation, onboarding, focused current-state research, and historical archaeology — the phases before you commit to scoping a change.

Source: `dot_config/ai_templates/skills/pa-sdlc/pa-scout/SKILL.md`.

## When to reach for Scout

| Situation | Why Scout |
|---|---|
| You landed in an unfamiliar repo or content system. | Scout gives you the fastest first-pass map. |
| A human needs a guided walkthrough of a surface you already know. | Scout owns the structured-onboarding mode for teachable explanations. |
| You have one focused question and need evidence in the current state. | Scout's targeted-inquiry mode narrows the search to exactly that question. |
| The current state only makes sense if you know how it got there. | Scout's history-archaeology mode traces evolution over time. |

Scout is a research-first stage. It produces maps, walkthroughs, answers, and histories — not plans, not recommendations, not execution.

## Four internal modes

| Mode | Owns | Use when |
|---|---|---|
| `OrientationScan` | Broad first-pass discovery | You need a quick map and the next place to look |
| `StructuredOnboarding` | Human-friendly walkthrough | You need a newcomer guide or teachable explanation |
| `TargetedInquiry` | Narrow current-state research | You have one focused question and need evidence |
| `HistoryArchaeology` | Evolution over time | History matters more than current-state inspection alone |

Pick exactly one. Mixing modes in a single Scout call is usually a symptom that the question was too broad — split it into multiple calls, each with a clearer mode.

## Default output shape

A Scout brief answers five questions:

1. **What is this?** The subject under study, in one line.
2. **Who does it serve?** Users, maintainers, or stakeholders.
3. **How is it organized?** Structural layout — directories, modules, teams, whatever applies.
4. **Where to look next?** The two or three places that reward follow-up reading.
5. **What is still unknown?** Gaps, areas you could not read, questions outside this pass.

The brief is short by default — Scout is a map, not a wiki.

## Boundaries — when *not* to use Scout

| Real need | Reach for |
|---|---|
| Deciding what is in play for a change | [[scope]] |
| Deciding whether a direction is worth pursuing | [[vision]] |
| Designing execution for settled work | [[architect]] |
| Applying a change or fixing a bug | [[implement]] |
| Documenting a concrete change, decision, or artifact | [[doc-update]] |
| Refreshing, deduplicating, or repairing existing docs | [[doc-cleaner]] |

If you notice yourself building a plan mid-Scout, stop. The plan lives in Architect, and scouting further will not make it better.

## Scout vs. Scope

These are the two most commonly confused stages.

| | Scout | Scope |
|---|---|---|
| Question | "What is this?" | "What does *this change* touch?" |
| Starting point | No request in hand, or a research question | A requested change |
| Output | Map + unknowns | Change surface + blast radius |
| Hides the ticket? | Scope hides the ticket during research; Scout does not have a ticket. | Scope often works with the ticket hidden to avoid biased research. |

Scout without a change request is fine. Scope without a change request is incoherent — there is nothing to scope.

## Related

- [[scope]]
- [[vision]]
- [[advisor]]
- source: `dot_config/ai_templates/skills/pa-sdlc/pa-scout/SKILL.md`
