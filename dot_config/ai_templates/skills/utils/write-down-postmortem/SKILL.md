---
name: write-down-postmortem
description: Use when the user already has a postmortem written and wants it saved in `docs/references/postmortem/references/` with the correct dated folder and matching file name. Focus on placing the postmortem in the right location and preserving the user's content.
---

# Write Down Postmortem

Create a postmortem entry in `docs/references/postmortem/references/`.

## Workflow

1. Use the user's remaining input as the postmortem content.
2. If the content is missing or too thin to title, ask one short question.
3. Create `YYYY-MM-DD-postmortem-short-title/` using today's date and a 2-5 word kebab-case title.
4. Inside it, create `idea-postmortem-short-title.md`.
5. Save the user's content with only minimal cleanup needed to preserve readability.
6. Keep the emphasis on correct placement and naming, not on rewriting the postmortem.
7. Return the folder path, file path, and final slug.

## Rules

- Output under `docs/references/postmortem/references/`.
- Prefer the exact pattern `docs/references/postmortem/references/YYYY-MM-DD-postmortem-short-title/idea-postmortem-short-title.md`.
- Preserve the user's language and structure unless they ask for editing.
- Keep edits small and mechanical.
- If the user provides a strong title, prefer it.
- Do not invent analysis, lessons, or formatting the user did not ask for.
