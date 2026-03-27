# last30days wrapper

This chezmoi path intentionally stays small.

The upstream project is large and changes often, so this repo only keeps:

- a thin `SKILL.md` wrapper for OpenCode and Codex
- local setup notes
- a local installer script in `scripts/`

## Local install strategy

Runtime code lives outside the synced skill tree:

- checkout path: `~/.local/share/last30days-skill`
- installer: `~/.config/opencode/skill/utils/last30days/scripts/install_upstream.sh`
- codex installer path: `~/.codex/skills/utils/last30days/scripts/install_upstream.sh`
- config: `~/.config/last30days/.env`

Install or update with:

```bash
bash ~/.config/opencode/skill/utils/last30days/scripts/install_upstream.sh
```

Verify with:

```bash
python3 ~/.local/share/last30days-skill/scripts/last30days.py --diagnose
```

## Why this layout

`dot_config/ai_templates/skills/` is synced into multiple agent homes by chezmoi.
Vendoring the full upstream repo here copies docs, fixtures, tests, and release files into every target.
That makes sync noisy and hard to maintain.

This wrapper keeps the synced skill lean while still using the official upstream code.

## X setup

The upstream project prefers cookie auth for X search:

- `AUTH_TOKEN=<x.com auth_token cookie>`
- `CT0=<x.com ct0 cookie>`

`XAI_API_KEY` is only a fallback backend.
If you only want the skill working quickly, set `AUTH_TOKEN`, `CT0`, and `SCRAPECREATORS_API_KEY` first.
