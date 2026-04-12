---
name: Implement
description: `pa-implement` is the execution entry point — use it to apply a bounded change or repair broken behavior
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - pa-sdlc
---

Implement is the fifth stage of `pa-sdlc`. Load it with the explicit entry point `pa-implement`.

Use Implement when the work is ready to build — the direction is clear, the plan exists, and the outcome is specific enough to name a first slice. Implement also owns bug work: the root-cause-repair mode that starts with reproduction and ends with a fix tied to the explained defect.

Source: `dot_config/ai_templates/skills/pa-sdlc/pa-implement/SKILL.md`.

## When to reach for Implement

| Situation | Mode |
|---|---|
| Something is broken and a trustworthy fix requires reproduction and root-cause reasoning. | `RootCauseRepair` |
| The work is ready to execute and you can name one first slice clearly. | `ChangeApplication` |

Pick RootCauseRepair first when the request is bug-shaped, failure-shaped, or regression-shaped. Pick ChangeApplication for all other bounded execution work.

## Pre-flight check before ChangeApplication

Before starting ChangeApplication, confirm all three of these:

1. The outcome is specific enough to **name one first slice**.
2. The execution surface is known enough to **start**.
3. The remaining uncertainty is **execution detail**, not unresolved discovery, scope, direction, or planning.

If any of the three fails, you are in the wrong stage. Back up:

- Unresolved discovery → [[scout]]
- Unresolved scope → [[scope]]
- Unresolved direction → [[vision]]
- Unresolved planning → [[architect]]

The pre-flight check is the single most important discipline in Implement. Skipping it is how the `pa-sdlc` sequence collapses into "just start coding and figure it out as we go" — which is exactly what the stages exist to prevent.

## Two internal modes

| Mode | Owns | Use when |
|---|---|---|
| `ChangeApplication` | Normal bounded execution | The work is ready and one first slice can be named clearly |
| `RootCauseRepair` | Debugging and repair | Something is broken and a trustworthy fix requires reproduction and root-cause reasoning |

## Default posture

From the SKILL.md:

- **For behavior-bearing software work, default to TDD.** Tests drive the first slice.
- **Across all subjects, default to vertical slices over horizontal layers.** Same principle as Architect.
- **For bug work, reproduce first and keep the repair tied to the explained defect.** Never fix a bug you cannot reproduce. Never trust a fix whose connection to the defect is "it made the test pass".

The TDD default means: for every behavior-bearing change, the first output is a failing test that expresses the slice's outcome. The second output is the code that makes it pass. The third output is any refactor that cleans up what is now working.

The slice default means: the first test and the first code both aim for one end-to-end outcome — not the most-complete backend or the most-polished UI, but the shortest path to "a user can do the thing".

## Root-cause repair workflow

For bug work, RootCauseRepair runs in this order:

1. **Reproduce.** Write a failing test that captures the bug's observed behavior. If you cannot write a reproducing test, you do not understand the bug yet.
2. **Explain.** Use the reproduction to trace the path from input to failure. Name the specific line, function, or interaction that causes the defect.
3. **Repair.** Fix the explained defect at the root. Do not fix it downstream where the symptom showed up.
4. **Verify.** Run the reproducing test. Then run the broader suite to check for regressions.
5. **Document.** Hand off to [[doc-update]] with a rationale-capture brief: the defect, the root cause, the fix, the reason the test suite did not catch it previously.

Steps 2 and 3 are load-bearing. The SKILL.md emphasizes: "keep the repair tied to the explained defect". A fix that is not explained — "I changed this and now it works" — is evidence that you have not actually fixed the bug.

## Default output shape

Implement's output keeps six anchors visible:

1. **Requested change or problem** — what triggered this work.
2. **Execution boundary** — what was in scope and what was deliberately out of scope.
3. **Work performed or planned** — actual diffs, test additions, commits.
4. **Verification performed** — test runs, manual checks, evidence the change is correct.
5. **Risks or unresolved items** — what could still go wrong.
6. **Recommended next phase** — usually Doc-update.

## Boundaries — when *not* to use Implement

| Real need | Reach for |
|---|---|
| Broad orientation | [[scout]] |
| The change surface or blast radius | [[scope]] |
| Direction, value, or end state | [[vision]] |
| Roadmap design, spikes, or structure design | [[architect]] |
| Post-change documentation for one concrete result | [[doc-update]] |
| Refreshing, deduplicating, or repairing existing docs | [[doc-cleaner]] |

## Related

- [[architect]]
- [[doc-update]]
- [[advisor]] — the advisor is particularly useful mid-Implement when a fix is not converging
- source: `dot_config/ai_templates/skills/pa-sdlc/pa-implement/SKILL.md`
