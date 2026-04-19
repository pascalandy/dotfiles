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
bash ~/.config/opencode/skills/last30days/scripts/install_upstream.sh
# or in Codex:
bash ~/.codex/skills/last30days/scripts/install_upstream.sh
```

## Diagnose runtime

```bash
uv run python ~/.local/share/last30days-skill/scripts/last30days.py --diagnose
```

## Why this layout

Putting the whole upstream repo inside the chezmoi skill tree causes unnecessary sync noise across OpenCode, Codex, Claude, Amp, and other agent homes.
This wrapper keeps the synced surface small and leaves the heavy runtime in one local checkout.

## Path reference

The skill source lives at `dot_config/ai_templates/skills/web/last30days/`. After `chezmoi apply`, the post-apply fan-out flattens the 8 workflow-arc buckets into a single flat `skills/` directory per agent home. See [[how-ai-templates-are-distributed]]. Applied paths:

- source: `dot_config/ai_templates/skills/web/last30days/`
- shared applied copy: `~/.config/ai_templates/skills/web/last30days/`
- OpenCode copy: `~/.config/opencode/skills/last30days/`
- Codex copy: `~/.codex/skills/last30days/`
- Claude Code copy: `~/.claude/skills/last30days/`

Expected wrapper contents under any agent home:

- `SKILL.md`
- `references/`
- `scripts/`

Every downstream copy is reconstructed on every `chezmoi apply` via `rsync --delete`, so manually editing under an agent home never survives — always edit the chezmoi source.
