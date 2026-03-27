---
name: last30days
description: |
  Use only when the user explicitly say "last30days". Research topics, news, trends, and recommendations from the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, Bluesky, and the web. 
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
python3 ~/.local/share/last30days-skill/scripts/last30days.py --diagnose
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
- keep the chezmoi skill directory minimal; do not vendor the whole upstream repo here
