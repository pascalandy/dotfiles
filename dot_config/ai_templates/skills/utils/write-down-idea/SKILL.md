---
name: write-down-idea
description: Use when the user wants to capture a rough idea in `docs/references/ideas/references/`. Create a dated folder and matching idea file, keep the author's voice and language, run a `simple-editor` pass, then a `writer-sk` pass.
---

# Write Down Idea

Create an idea entry in `docs/references/ideas/references/`.

## Workflow

1. Use the user's remaining input as the raw idea text.
2. If the idea is missing or too thin to title, ask one short question.
3. Create `YYYY-MM-DD-short-title/` using today's date and a 2-4 word kebab-case title.
4. Inside it, create `idea-short-title.md`.
5. Start from the raw text.
6. Do a `simple-editor` (skill) pass: keep the voice and language, remove obvious duplication, fix clear typos, and organize into readable paragraphs.
7. Do a `writer-sk` (skill) pass: make it clearer and tighter without changing meaning or personality.
8. Save the result and return the folder path, file path, and final slug.

## Rules

- Keep the original language, including mixed French and English.
- Keep the edit small.
- Do not add sections, advice, or analysis the user did not ask for.
- If the user gives a strong title, prefer it.
