---
name: pa-vision
description: Direction-setting entry point for defining where work is going before execution planning begins. Use `pa-vision` when you need to pressure-test the direction, align on the end state, or package settled direction into a durable brief, then export the final vision artifact.
keywords: [pa-vision, vision, direction, alignment, brief, prd, direction-check]
---

# Vision

Explicit entry point: `pa-vision`.

Use Vision to answer one question before planning: where are we going?

## Route

Load `references/ROUTER.md`.

## Use This When

- You need to test whether a direction is worth pursuing.
- You need to make the target state explicit before planning.
- You need a durable brief for settled direction.

## Internal Modes

| Mode | Owns | Use when |
|---|---|---|
| `DirectionCheck` | Direction pressure test | You need a go, revise, defer, or stop recommendation |
| `AlignmentDraft` | Default pre-planning artifact | You need the current state, end state, and pattern choices made explicit |
| `BriefAuthoring` | Durable brief or PRD | The direction is settled and the main job is packaging it cleanly |

## Boundaries

| If the real need is... | Use instead |
|---|---|
| understanding what exists today | `pa-scout` |
| identifying what is in play for a change | `pa-scope` |
| designing execution, structure, or sequencing | `pa-architect` |
| building the change or fixing a bug | `pa-implement` |
| documenting an already-made change, decision, or artifact | `pa-doc-update` |
| refreshing, deduplicating, or repairing existing docs | `pa-doc-cleaner` |

## Default Output

Default to a direction-oriented artifact that makes these easy to find:

1. request or decision
2. current state
3. desired end state
4. key decisions or pattern choices
5. success signals
6. risks and review points
7. recommended next phase

## Export Contract

Create an idea entry in `docs/references/ideas/references/`.

Resolve the export target before running the writing workflow. This contract is separate so the same export pattern can be reused elsewhere by swapping only the destination and naming rules.

- `export_root`: `docs/references/ideas/references/`
- `entry_slug`: a 2-4 word kebab-case title, preferably from a strong user-provided title
- `export_dir`: `YYYY-MM-DD-entry_slug/`
- `export_file`: `vision-entry_slug.md`
- Final path: `export_root/export_dir/export_file`

## Workflow

1. Use the user's remaining input as the raw idea text.
2. If the idea is missing or too thin to title, ask one short question.
3. Resolve `entry_slug`, `export_dir`, and `export_file` before editing any text.
4. Start from the raw text.
5. Route to the right Vision mode and produce the final vision artifact.
6. Write the final text to the resolved export path.
7. Only after export, return the folder path, file path, and final slug.

## Rules

- Keep export naming mechanical and separate from the writing pass.
- Prefer a strong user-provided title when resolving `entry_slug`.
- Keep the final artifact aligned with the selected Vision mode rather than forcing a single document shape.
- Export is mandatory when `pa-vision` produces a direction check, alignment draft, brief, PRD, charter, or other vision artifact.
- Do not hand off to `pa-architect` or any later phase before the vision artifact has been written to the resolved export path.
- For reuse, change the export contract first and keep the workflow steps unchanged unless the content workflow itself differs.

## Non-Goals

Vision does not own scoping, execution planning, implementation, release documentation, or documentation maintenance.
