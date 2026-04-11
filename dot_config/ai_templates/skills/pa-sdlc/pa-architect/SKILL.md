---
name: pa-architect
description: Execution-design entry point for turning settled direction into a plan. Use `pa-architect` when you need a roadmap, a bounded spike, a target structure, or a hard review of an existing plan.
keywords: [pa-architect, architect, roadmap, spike, structural-design, stress-test, execution-plan]
---

# Architect

Explicit entry point: `pa-architect`.

Use Architect after direction is settled and before implementation starts.

## Route

Load `references/ROUTER.md`.

Choose one primary mode in this order:

1. `PlanStressTest` when a meaningful plan already exists.
2. `DecisionSpike` when one blocking unknown must be answered first.
3. `StructuralDesign` when the main blocker is the target shape or boundary design.
4. `RoadmapDesign` for the default planning job.

## Use This When

- The direction is clear enough to plan execution.
- The work needs phases, milestones, or workstreams.
- One blocker needs a bounded spike before a real plan is credible.
- An existing plan needs a readiness review before implementation.

## Planning Principle

Architect defaults to vertical slices over horizontal layers.

- Prefer slices that produce one user-recognizable outcome through every relevant layer.
- Sequence slices by risk and unknowns, not by layer dependency or implementation comfort.
- Treat plans framed as "build all the backend first" or "finish the UI later" as a warning sign unless the user explicitly needs a layer-isolated task.
- Make each planned slice independently demonstrable, reviewable, and safe to stop after.
- Use mocks only to preserve an end-to-end path inside the current slice, and name the later slice that replaces each mock.

## Internal Modes

| Mode | Owns | Use when |
|---|---|---|
| `RoadmapDesign` | Default execution roadmap | You need sequencing, decisions, risks, and validation checkpoints |
| `DecisionSpike` | One bounded unknown | Planning would be fake without answering one specific question first |
| `StructuralDesign` | Target shape or boundaries | The problem is system structure, workflow shape, or interface design |
| `PlanStressTest` | Hardening an existing plan | A real plan exists and needs challenge before implementation |

## Boundaries

| If the real need is... | Use instead |
|---|---|
| broad orientation or current-state research | `pa-scout` |
| identifying the change surface or blast radius | `pa-scope` |
| deciding whether the direction is right | `pa-vision` |
| building the work or debugging a failure | `pa-implement` |
| documenting a concrete outcome, decision, or artifact | `pa-doc-update` |
| refreshing, deduplicating, or repairing existing docs | `pa-doc-cleaner` |

## Default Output

Route to one primary mode, then use that mode's output contract. In all modes, make these easy to find:

1. framing goal
2. current constraint or blocker
3. recommended structure, path, or conclusion
4. what needs human review
5. recommended next phase

When a mode produces execution sequencing, prefer slices described as demonstrable outcomes rather than layer buckets.

## Non-Goals

Architect does not own discovery, scoping, product direction, implementation, or documentation maintenance.
