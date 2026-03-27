# last30days local layout

## Goal

Keep the chezmoi-managed skill directory small while using the official upstream runtime.

## Managed here

- `SKILL.md`
- `README.md`
- `scripts/install_upstream.sh`
- `references/install.md`

## Stored outside the synced skill tree

- upstream checkout: `~/.local/share/last30days-skill`
- secrets: `~/.config/last30days/.env`

## Install or update upstream

```bash
bash ~/.config/opencode/skill/utils/last30days/scripts/install_upstream.sh
# or in Codex:
bash ~/.codex/skills/utils/last30days/scripts/install_upstream.sh
```

## Diagnose runtime

```bash
uv run python ~/.local/share/last30days-skill/scripts/last30days.py --diagnose
```

## Why this layout

Putting the whole upstream repo inside the chezmoi skill tree causes unnecessary sync noise across OpenCode, Codex, Claude, Amp, and other agent homes.
This wrapper keeps the synced surface small and leaves the heavy runtime in one local checkout.
