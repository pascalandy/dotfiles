---
name: pa-architect
description: Execution-design entry point for turning settled direction into a plan. Use `pa-architect` when you need a roadmap, a bounded spike, a target structure, or a hard review of an existing plan, then export the final architect artifact.
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

## Export Contract

Create an idea entry in `docs/references/ideas/references/`.

Resolve the export target before running the writing workflow. This contract is separate so the same export pattern can be reused elsewhere by swapping only the destination and naming rules.

- `export_root`: `docs/references/ideas/references/`
- `entry_slug`: a 2-4 word kebab-case title, preferably from a strong user-provided title
- `export_dir`: `YYYY-MM-DD-entry_slug/`
- `export_file`: `architect-entry_slug.md`
- Final path: `export_root/export_dir/export_file`

## Workflow

1. Use the user's remaining input as the raw idea text.
2. If the idea is missing or too thin to title, ask one short question.
3. Resolve `entry_slug`, `export_dir`, and `export_file` before editing any text.
4. Start from the raw text.
5. Route to the right Architect mode and produce the final architect artifact.
6. Write the final text to the resolved export path.
7. Return the folder path, file path, and final slug.

## Rules

- Keep export naming mechanical and separate from the writing pass.
- Prefer a strong user-provided title when resolving `entry_slug`.
- Keep the final artifact aligned with the selected Architect mode rather than forcing a single document shape.
- For reuse, change the export contract first and keep the workflow steps unchanged unless the content workflow itself differs.

## Non-Goals

Architect does not own discovery, scoping, product direction, implementation, or documentation maintenance.
