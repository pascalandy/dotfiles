---
name: write-down-idea
description: Use when the user wants to capture a rough idea into `docs/ideas/references/`, including feature ideas, post-mortems, repos to explore, or personal notes they want stored in a structured place. Create a dated idea folder, write the idea file, preserve the original voice and language mix, then tighten the prose with a second clarity pass.
---

# Write Down Idea

Capture loose thinking into the ideas wiki without flattening the author's voice.

## Use This Skill When

- The user wants to write down an idea for later.
- The input is rough, mixed-language, or personal, but should still be stored cleanly.
- The note belongs in `docs/ideas/references/`.
- The user mentions a feature idea, post-mortem, repo to explore, or a personal line of thought to keep.

## Workflow

1. Identify the idea text from the user's message.
2. If the idea text is missing or too thin to title, ask one short question.
3. Derive a directory name as `YYYY-MM-DD-short-title/` using today's date and a 2-4 word kebab-case title.
4. Create `docs/ideas/references/YYYY-MM-DD-short-title/idea-short-title.md`.
5. Start from the user's raw text.
6. Do a first editing pass with the `simple-editor` standard:
   preserve the voice, emotion, and original language mix; remove obvious duplication; fix clear typos; break the text into readable paragraphs.
7. Do a second pass with the `writer-sk` standard:
   make the text clearer and tighter without changing facts, meaning, or personality.
8. Save the final text to the idea file.
9. Return the created path.

## Naming Rules

- Use today's date.
- Keep the short title to 2-4 words when possible.
- Use lowercase kebab-case.
- Match the file name to the folder slug: `idea-short-title.md`.
- If the user gives a strong title, prefer that over inventing one.

## Editing Rules

- Keep the note in the author's language.
- If the source mixes French and English, keep the mix.
- Do not turn a raw note into polished marketing copy.
- Do not add analysis, advice, or sections the user did not imply.
- Keep the edit small. Readability first.

## Output

Return:

- the folder path
- the file path
- the final title slug

## Example

If today is `2026-04-10` and the idea is about implementing a dark mode toggle, create:

- `docs/ideas/references/2026-04-10-dark-mode-toggle/`
- `docs/ideas/references/2026-04-10-dark-mode-toggle/idea-dark-mode-toggle.md`

## Gotcha

The source of truth is the repository copy under chezmoi. If you are asked to edit an applied file under `~/`, check whether it is managed first and write to the chezmoi source path instead.
