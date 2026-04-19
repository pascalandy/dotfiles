---
name: last30days
description: |
  Use only when the user explicitly says "last30days". Research topics, news, trends, and recommendations from the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, Truth Social, Xiaohongshu, Tavily, and the web (Parallel AI, Brave, OpenRouter, or assistant fallback).
---

# last30days

This is a thin wrapper skill for OpenCode and Codex.

The real upstream runtime lives in a local sparse checkout at `~/.local/share/last30days-skill`.
Keep setup helpers inside this skill folder, not in `~/.local/bin`.

## Setup and runtime

1. If `~/.local/share/last30days-skill/scripts/last30days.py` is missing, run:

```bash
bash ~/.config/opencode/skill/utils/last30days/scripts/install_upstream.sh
# or in Codex:
bash ~/.codex/skills/utils/last30days/scripts/install_upstream.sh
```

2. Before first real use, verify the environment:

```bash
uv run python ~/.local/share/last30days-skill/scripts/last30days.py --diagnose
```

3. Read and follow the upstream instruction file:

```text
~/.local/share/last30days-skill/SKILL.md
```

If the user asks for watchlists, briefings, or history mode, also read:

```text
~/.local/share/last30days-skill/variants/open/SKILL.md
```

4. For local maintenance details, read:

```text
~/.config/opencode/skill/utils/last30days/references/install.md
~/.codex/skills/utils/last30days/references/install.md
```

## OpenCode/Codex execution rule

- In this setup, always run the real runtime from `~/.local/share/last30days-skill`.
- Always use `uv run python ~/.local/share/last30days-skill/scripts/last30days.py ...`.
- Do not run `scripts/last30days.py` from the synced skill directory.
- For X, do not invoke the vendored Bird module directly; rely on `AUTH_TOKEN` and `CT0` injected through `~/.config/last30days/.env`.

## Config locations

The upstream skill loads config in this order:

1. environment variables
2. `.claude/last30days.env` in the current project tree
3. `~/.config/last30days/.env`

## X auth

Use one of these:

- recommended: `AUTH_TOKEN` and `CT0` from x.com cookies
- fallback: `XAI_API_KEY`

## Notes

- `OPENAI_API_KEY` is optional when Codex is already logged in
- `SCRAPECREATORS_API_KEY` unlocks Reddit, TikTok, and Instagram
- Tavily API key is stored in macOS keyring (`chezmoi secret keyring get --service=tavily --user=api_key`)
- keep the chezmoi skill directory minimal; do not vendor the whole upstream repo here

## Tavily sub-agent

Run a Tavily web search **in parallel** with the main `last30days.py` execution.
Spawn a sub-agent using the Task tool at the same time you launch the script.

The sub-agent must use skill `tavily-sk` for all Tavily API calls.

### When to use basic vs deep search

- **Basic search** (`POST /search`): default for most queries -- news, trends,
  recommendations, general topics.
- **Deep research** (`POST /research`): use when the query is complex, requires
  multi-step analysis, or when the user explicitly asks for deep research.

### How to spawn

When launching the `last30days.py` script, send a **parallel** Task tool call
with instructions like:

```
Use skill: "tavily-sk" to search: "<the user's query>"

Search parameters:
- time_range: "month"
- max_results: 10
- include_answer: true
- topic: "<general|news|finance>" (pick based on query)

If the query is complex or the user asked for deep research, use
POST /research instead of POST /search.

Return: a list of results with title, url, content summary, and score.
If the search fails, return the exact error (status code, message).
```

Adapt the query terms as needed -- expand abbreviations, add context, use
the same query variations the main script would use.

### Merging results

After both the main script and the Tavily sub-agent return:

1. Deduplicate by URL -- if Tavily returns a URL already in the main results,
   keep whichever has richer content.
2. Tavily results appear under a **Tavily** section in the synthesis, same
   format as other sources.
3. If Tavily returned an AI-generated answer, include it as supplementary
   context but do not present it as a primary source.

## Failure reporting

- If any source fails because of billing, auth, missing modules, rate limits, or runtime errors, report that failure explicitly.
- Treat a failed source as unavailable coverage, not partial success.
- Call out the exact source and error before any synthesis.
- Do not present a synthesis as if Reddit, X, Tavily, or web contributed when those sources failed.
- If the Tavily sub-agent fails or times out, report it as `Tavily: error -- {message}` alongside other source statuses.
