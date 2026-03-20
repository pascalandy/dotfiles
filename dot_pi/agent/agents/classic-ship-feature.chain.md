---
name: classic-ship-feature
description: Implement, QA, and ship from a technical feature plan such as docs/features/feat-9234/technical_slug.md
---

## scout
output: context.md
progress: true

The task is a repo-relative technical plan path, for example: `docs/features/feat-9234/technical_example-feature.md`.

Requirements:
- Validate that `{task}` exists and is a technical feature plan file.
- Treat `{task}` as the canonical implementation source.
- Read `{task}` first.
- Read sibling files when present: `request.md`, `context.md`, `meta-prompt.md`, and the matching `plan_<slug>.md` product plan in the same directory.
- Then inspect the current codebase and summarize the exact code paths, tests, and constraints needed to implement the feature.
- Write that implementation context to the chain artifact `context.md`.
- In your response, return only `{task}`.

## implement
reads: context.md
output: false
progress: true

The task is the same technical plan path: `{task}`.

Requirements:
- Implement strictly from `{task}`.
- Use the sibling `plan_<slug>.md` file only as product-intent support when it exists.
- Read the feature docs directly from the plan directory before coding.
- Use `context.md` to target the correct files and tests.
- Keep the diff minimal, repo-grounded, and aligned with the technical plan.
- Add or update tests with the code changes.
- Before finishing, create logical commits so the working tree is clean and ready for `/qa`.
- If the plan is missing, inconsistent, or not implementation-ready, stop and report the blocker clearly.

## qa
reads: context.md
output: false
progress: true

Run the `qa` workflow after implementation.

Requirements:
- Use `{task}` as the feature reference.
- Prefer diff-aware QA unless the technical plan clearly specifies a target URL.
- Treat the technical plan and `context.md` as the scope for what must be verified.
- Fix issues found within the normal QA scope, re-verify them, and leave the branch ready to ship.

## ship
reads: false
output: false
progress: true

Run the `ship` workflow for the current branch after QA is complete.

Requirements:
- Use `{task}` as the feature reference when summarizing what is being shipped.
- If the branch is not ready to ship, fail loudly with the blocker instead of continuing silently.

## document-release
reads: false
output: false
progress: true

Run the `document-release` workflow after shipping completes.

Requirements:
- Cross-check the shipped diff against root docs and the technical plan path `{task}`.
- Also check the sibling `plan_<slug>.md` product plan when it exists.
- If shipped behavior materially differs from the feature docs, update those docs so they reflect the shipped state.
- Preserve the technical plan as the implementation reference and keep the product plan aligned.
- Summarize documentation health clearly.
