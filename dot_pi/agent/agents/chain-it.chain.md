---
name: chain-it
description: Summarize the opencode configuration doc and save English and French outputs to a feature folder
---

## general
reads: false
output: false
progress: true

The feature id is `{task}`.

Read `docs/features/opencode/opencode-configurations.md` and write a 2 to 3 sentence summary to `/Users/andy16/.local/share/chezmoi/docs/features/{task}/opencode-configurations-summary.en.md`.

Requirements:
- Create parent directories if needed.
- Write plain Markdown with no code fences.
- In your response, return only the summary text that you wrote to the file.

## general
reads: false
output: false
progress: true

The feature id is `{task}`.

Translate the following text into French and write it to `/Users/andy16/.local/share/chezmoi/docs/features/{task}/opencode-configurations-summary.fr.md`.

Text to translate:
{previous}

Requirements:
- Create parent directories if needed.
- Write plain Markdown with no code fences.
- In your response, return only the translated text that you wrote to the file.
