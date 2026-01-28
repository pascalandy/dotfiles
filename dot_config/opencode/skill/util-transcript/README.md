# Transcript skill

This skill runs `.opencode/skill/transcript/scripts/transcript.py` to download YouTube audio, transcribe it, and save outputs to a timestamped folder (base directory is configured by `OUTPUT_DIR` in the script).

## Requirements (runtime)

- Python 3.10+ and `uv`
- `yt-dlp` installed and on PATH
- Deepgram API key in macOS keyring:
  ```bash
  chezmoi secret keyring set --service=deepgram --user=api_key
  ```
  (Falls back to `DEEPGRAM_API_KEY` env var if keyring unavailable)
- Optional (only for prompt-based summaries): `claude` CLI installed and working
- Optional (nicer terminal preview): `glow` installed (`brew install glow`)

## Defaults

- **Default model**: `claude-opus-4-5` (most capable)
- **Default prompt**: `follow_along_note` (comprehensive follow-along notes with the transcript)
- **Available prompts**: `follow_along_note`, `short_summary`, `summary_with_quotes`
- **Transcript only**: use `--no-prompt` flag

## Output files

Each run creates a timestamped folder containing:

- `{prompt}.md` - AI-generated summary (default: `follow_along_note.md`)
- `raw_transcript.txt` - plain text transcript
- `raw_sentences.txt` - timestamped sentences in the form `[0s - 5s] text...`
- `raw_transcript.json` - structured JSON data
- `meta.txt` - video metadata

## Quick sanity checks

1. **Syntax check (no network / no API calls)**

   ```bash
   uv run python -m py_compile .opencode/skill/transcript/scripts/transcript.py
   ```

2. **List bundled prompts**

   ```bash
   uv run .opencode/skill/transcript/scripts/transcript.py --list-prompts
   ```

   Expected: one prompt name per line (filename stems from `scripts/prompts/`).

3. **List available Claude models**

   ```bash
   uv run .opencode/skill/transcript/scripts/transcript.py --list-models
   ```

   Expected: the three valid model names, one per line.

## End‑to‑end smoke test

```bash
uv run .opencode/skill/transcript/scripts/transcript.py --prompt short_summary --model claude-haiku-4-5 "<youtube_url>"
```

Verify:

- A new folder appears under the base output directory configured in `.opencode/skill/transcript/scripts/transcript.py` (`OUTPUT_DIR`).
- `raw_transcript.txt`, `raw_sentences.txt`, `raw_transcript.json`, and `meta.txt` exist.
- If `--prompt` was used, the corresponding `*.md` summary file exists.
- The summary renders in the terminal after Finder opens (uses `glow` if installed).
