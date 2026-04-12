---
name: tmux engine
description: Custom _ttm_* functions providing reproducible 3-pane tmux windows under a single session
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# tmux Engine (`_ttm_*`)

A custom tmux helper engine that provides reproducible 3-pane layouts under a single persistent session named `main`.

## Entry points

| Command | Action                                           | Target directory                             |
|---------|--------------------------------------------------|----------------------------------------------|
| `ttmj`  | join (create if absent) a `forzr` window         | `$HOME/Documents/github_local/forzr`         |
| `ttmr`  | reset the `forzr` window                         | same                                         |
| `ttmjc` | join (create if absent) a `chezmoi` window       | `$HOME/.local/share/chezmoi`                 |
| `ttmrc` | reset the `chezmoi` window                       | same                                         |
| `ttmM`  | wipe and recreate both `forzr` and `chezmoi`     | both                                         |

If a target directory does not exist, the engine falls back to `$HOME/Documents/_my_docs` (creating it when missing).

## Window layout

Every window created by `_ttm_create_window` has the same layout:

```
┌─────────────────────────────────┐
│         Pane 1 (oc)             │
│            67%                  │
├──────────────────┬──────────────┤
│  Pane 2 (ls) 67% │ Pane 3 (oc)  │
│                  │    33%       │
└──────────────────┴──────────────┘
```

- Pane 1 (top, 67%) — runs `oc` (opencode)
- Pane 2 (bottom-left, 67% of bottom) — runs `ls`
- Pane 3 (bottom-right, 33% of bottom) — runs `oc`

After pane creation, `_ttm_tmux select-pane -t "$target".1` returns focus to pane 1.

## Smart prompt wait

`_ttm_wait_for_prompt` prevents a race where commands are sent to panes before their shells are ready — which caused `oc` to crash with SIGTRAP on cold start.

How it works:
1. Capture pane contents via `tmux capture-pane -t ... -p`
2. Look for a line starting with `>`, `$`, or `❯` (covers Powerlevel10k and plain prompts)
3. Poll every 0.1s
4. Default timeout 5 seconds — on timeout the engine proceeds anyway to avoid hangs

## Session model

- A single session named `main` holds all project windows
- One window per project (`forzr`, `chezmoi`, ...)
- A temporary `__init__` window is killed once real windows exist
- When starting from outside tmux, `_ttm_clean_env` unsets `TMUX`/`TMUX_PANE` and points `TMUX_TMPDIR` at `$HOME/.local/share/tmux`
- `_ttm_cleanup_stale_socket` removes a dead default socket before re-creating the session
- Detection of "am I inside tmux?" uses `tmux list-clients` filtered by the current tty — stricter than just checking `$TMUX`

## Related aliases

- `spl2f` / `spl3f` — alias wrappers around standalone `spl2` / `spl3` split scripts in `$HOME/.local/bin`
