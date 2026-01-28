---
name: transcript
description: "Transcrire des vidéos YouTube (Deepgram): audio → txt/json, avec option de résumé Claude au besoin."
---

Here's how to use this script the user wants a transcript of a YouTube video.
Optionally we can generated "summaries" from a CLI like Claude Code.

## Run

```bash
uv run ~/.config/opencode/skill/util-transcript/scripts/transcript.py "<youtube_url>"
```

Use a 10-minute timeout (600 seconds) when running this script.

Discovery (no URL required):

```bash
uv run ~/.config/opencode/skill/util-transcript/scripts/transcript.py --list-prompts
uv run ~/.config/opencode/skill/util-transcript/scripts/transcript.py --list-models
uv run ~/.config/opencode/skill/util-transcript/scripts/transcript.py --help
```

## Choose flags from user intent

**Default behavior**: Script defaults to `follow_along_note` prompt. Just provide the URL.

- **Default** (user gives URL only) → run with just `<url>` (script defaults to follow_along_note)
- **Transcript only** (user explicitly says "transcript only" or "no summary") → add `--no-prompt`
- **Different prompt requested** (user says `short_summary`, `summary_with_quotes`, etc.) → add `--prompt <stem>`
- **Model requested** (user says `haiku`/`sonnet`/`opus`) → add:
  - `haiku` → `--model claude-haiku-4-5`
  - `sonnet` → `--model claude-sonnet-4-5`
  - `opus` → `--model claude-opus-4-5`
- If user asks "what prompts/templates exist?" → run `--list-prompts`, return the list, and ask which one to use.
- If user asks "what models can I use?" → run `--list-models`, return the list, and ask which one to use.

## Shorthand input mapping

Examples:

```bash
# User: transcript https://www.youtube.com/watch?v=2QpXab8z_Gw
# (default: follow_along_note prompt)
uv run ~/.config/opencode/skill/util-transcript/scripts/transcript.py "https://www.youtube.com/watch?v=2QpXab8z_Gw"

# User: transcript, short_summary, haiku, https://www.youtube.com/watch?v=2QpXab8z_Gw
uv run ~/.config/opencode/skill/util-transcript/scripts/transcript.py --prompt short_summary --model claude-haiku-4-5 "https://www.youtube.com/watch?v=2QpXab8z_Gw"

# User: transcript only, https://www.youtube.com/watch?v=2QpXab8z_Gw
uv run ~/.config/opencode/skill/util-transcript/scripts/transcript.py --no-prompt "https://www.youtube.com/watch?v=2QpXab8z_Gw"
```

## Outputs

- The script creates a timestamped output folder (it prints the path and opens it in Finder on macOS).
- Key files: `{prompt}.md`, `raw_transcript.txt`, `raw_sentences.txt`, `raw_transcript.json`, `meta.txt`.

For runtime requirements and validation steps, see `~/.config/opencode/skill/util-transcript/README.md`.

Don't READ the final answer. The user can already see it in the terminal.
