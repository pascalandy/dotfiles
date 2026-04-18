---
name: write-down-idea
description: Use when the user wants to capture a rough idea in `docs/references/ideas/references/`. Resolve the export path and file name first, then run the editing workflow while keeping the author's voice and language.
---

# Write Down Idea

## Export Contract

Create an idea entry in `docs/references/ideas/references/`.

Resolve the export target before running the writing workflow. This contract is separate so the same export pattern can be reused elsewhere by swapping only the destination and naming rules.

- `export_root`: `docs/references/ideas/references/`
- `entry_slug`: a 2-4 word kebab-case title, preferably from a strong user-provided title
- `export_dir`: `YYYY-MM-DD-entry_slug/`
- `export_file`: `idea-entry_slug.md`
- Final path: `export_root/export_dir/export_file`

## Workflow

1. Use the user's remaining input as the raw idea text.
2. If the idea is missing or too thin to title, ask one short question.
3. Resolve `entry_slug`, `export_dir`, and `export_file` before editing any text.
4. Start from the raw text.
5. Do a `simple-editor` (skill) pass.
6. Do a `writer-sk` (skill) pass.
7. Write the final text to the resolved export path.
8. Return the folder path, file path, and final slug.

## Rules

- Keep the original language, including mixed French and English.
- Keep the edit small.
- Do not add sections, advice, or analysis the user did not ask for.
- If the user gives a strong title, prefer it.
- Keep export naming mechanical and separate from the writing pass.
- For reuse, change the export contract first and keep the workflow steps unchanged unless the content workflow itself differs.
