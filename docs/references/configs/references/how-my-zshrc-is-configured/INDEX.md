---
name: How My zshrc is Configured
description: Analyst report of the current zshrc setup, tools, aliases, functions, and personal conventions
aliases:
  - zshrc-analyst-report
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-18
---

# How My zshrc is Configured

<scope>
Load this wiki when the task involves reading, understanding, or modifying `$HOME/.zshrc`.

Source of truth: `$HOME/.local/share/chezmoi/dot_zshrc`. The copy at `$HOME/.zshrc` is an applied target and must never be edited directly.

Use this wiki as a reference for tools, aliases, functions, and personal conventions. It is a snapshot in time — read the live source when accuracy matters.

Do NOT load it for generic shell troubleshooting unrelated to this machine.
</scope>

<workflow>
1. Confirm the task concerns this user's zshrc. Generic zsh advice does not need this wiki.

2. Route to the correct reference:
   - personal rules and tool substitutions → `preferences.md`
   - Oh My Zsh, P10k, env vars, history, locale → `shell-environment.md`
   - fzf / fd / eza / bat / ripgrep / zoxide → `toolchain.md`
   - Node.js via nvm → `node-nvm-lazy-load.md`
   - tmux windows and panes → `tmux-engine.md`
   - helper functions (vs, fdf, fdd, ggco, ggc, mkcd, git-clone wrappers) → `functions.md`
   - alias catalog → `aliases.md`
   - cd bookmarks and `PROJ_*` vars → `directory-bookmarks.md`
   - PATH additions → `path-management.md`

3. Edit the chezmoi source at `$HOME/.local/share/chezmoi/dot_zshrc`, never the copy at `$HOME/.zshrc`.

4. Apply changes with `chezmoi apply -v` (or the `ccma` alias), then `source $HOME/.zshrc` (or `reload`) to validate.
</workflow>

<checklist>
Before finishing any zshrc change:
- edits happened in the chezmoi source, not `$HOME/.zshrc`
- every new path uses `$HOME` (never a hardcoded `/Users/...` value)
- preferred tools are respected (`trash`, `eza`, `fd`, `rg`, `bat`, `btop`)
- new aliases placed under the matching `=== CATEGORY ===` block
- `zsh-syntax-highlighting` is still the last plugin in `plugins=(...)`
- P10k instant prompt block is still at the very top of the file
- lazy-loaded `nvm` wrappers are still intact
- `chezmoi apply -v` ran and the shell was reloaded
</checklist>

<references>
Load only what the task needs:
- [overview.md](references/overview.md) — big-picture snapshot
- [preferences.md](references/preferences.md) — personal conventions and rules
- [shell-environment.md](references/shell-environment.md) — OMZ, P10k, env vars, history
- [toolchain.md](references/toolchain.md) — fzf, fd, eza, bat, ripgrep, zoxide
- [node-nvm-lazy-load.md](references/node-nvm-lazy-load.md) — nvm lazy loading
- [tmux-engine.md](references/tmux-engine.md) — `_ttm_*` helper engine
- [functions.md](references/functions.md) — custom shell functions
- [aliases.md](references/aliases.md) — alias catalog by category
- [directory-bookmarks.md](references/directory-bookmarks.md) — cd shortcuts and `PROJ_*` vars
- [path-management.md](references/path-management.md) — PATH additions and ordering
</references>

---

> Content catalog. Every wiki page is listed here with a one-line summary.
> Read this first to find relevant pages for any query.
> **Total pages:** 11 | **Last updated:** 2026-04-11

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/doc

| File | Description |
|------|-------------|
| `references/aliases.md` | Alias catalog organized by category |
| `references/directory-bookmarks.md` | cd shortcuts and `PROJ_*` env vars |
| `references/functions.md` | Custom shell functions |
| `references/node-nvm-lazy-load.md` | nvm lazy loading pattern |
| `references/overview.md` | High-level snapshot of the zshrc |
| `references/path-management.md` | PATH additions and ordering |
| `references/preferences.md` | Personal conventions and rules |
| `references/shell-environment.md` | OMZ, P10k, env vars, history |
| `references/toolchain.md` | fzf, fd, eza, bat, ripgrep, zoxide |
| `references/tmux-engine.md` | Custom tmux helper engine |
