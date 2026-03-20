---
name: classic-planning
description: Turn pasted feature text into a durable feature folder with a product plan and a technical plan
---

## context-builder
output: context.md
progress: true

The task is raw feature text pasted by the user.

Requirements:
- Inspect `docs/features/` and determine the next available directory using the repo's numbered pattern: `docs/features/feat-<NNNN>/`.
- Generate the official short kebab-case slug for this feature exactly once in this step.
- Create the feature directory.
- Write the original pasted request to `<FEATURE_DIR>/request.md`.
- Generate `context.md` and `meta-prompt.md` as chain artifacts.
- Mirror those files to the durable feature directory as `context.md` and `meta-prompt.md`.
- Define the canonical output files for all downstream steps:
  - `<FEATURE_DIR>/plan_<FEATURE_SLUG>.md`
  - `<FEATURE_DIR>/technical_<FEATURE_SLUG>.md`
- Keep the feature directory path and official slug stable for all downstream steps.
- In your response, return only the actual values in this shape:
  - `FEATURE_DIR: docs/features/feat-<NNNN>`
  - `FEATURE_SLUG: <slug>`
  - `PLAN_FILE: docs/features/feat-<NNNN>/plan_<slug>.md`
  - `TECHNICAL_FILE: docs/features/feat-<NNNN>/technical_<slug>.md`

## plan-ceo-review
output: plan.md
reads: context.md, meta-prompt.md
progress: true

Use the original pasted request `{task}` and the handoff below:

{previous}

Chain mode rules:
- Do not pause for user input.
- If you would normally ask a question, record it as an unresolved decision with a recommendation and continue.

Requirements:
- Parse `PLAN_FILE` from the handoff. Treat that path as the canonical product-plan output.
- Produce the product-facing plan for this feature.
- Write the plan to the chain artifact `plan.md`.
- Mirror the same content to `PLAN_FILE`.
- Focus on problem framing, scope, non-goals, use cases, functional requirements, acceptance criteria, and unresolved product decisions.
- Keep implementation details light; this file is the product plan, not the technical build plan.
- In your response, return only the actual `PLAN_FILE` path.

## plan-eng-review
output: technical.md
reads: context.md, meta-prompt.md, plan.md
progress: true

Use the original pasted request `{task}` and the handoff below:

{previous}

Chain mode rules:
- Do not pause for user input.
- If you would normally ask a question, record it as an unresolved decision with a recommendation and continue.

Requirements:
- Parse `PLAN_FILE` and `TECHNICAL_FILE` from the handoff.
- Read the chain artifact `plan.md` and treat it as product intent.
- Produce the implementation-ready technical plan.
- Write the technical plan to the chain artifact `technical.md`.
- Mirror the same content to `TECHNICAL_FILE`.
- Focus on architecture, target files, sequencing, test strategy, failure modes, rollout notes, and explicit `NOT in scope` discipline.
- In your response, return only the actual `TECHNICAL_FILE` path.
