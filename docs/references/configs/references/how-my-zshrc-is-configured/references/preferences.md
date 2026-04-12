---
name: zshrc personal preferences
description: Cross-cutting rules and conventions an agent should respect when touching the zshrc
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Personal Preferences

> These are the rules an agent should keep in mind when reading or modifying the zshrc. They are the "why" behind many seemingly small choices.

## Path privacy: always use `$HOME`

**Always use `$HOME`, never a hardcoded `/Users/<name>` path.**

The reason is privacy — the real username should not be visible in the tracked dotfiles or in any documentation about them. When adding paths, always write `$HOME/...` (or `$PROJ_HOME`, `$MY_DOCS`, etc.).

Current state: the Google Cloud SDK auto-generated block at the bottom of the file contains two hardcoded `/Users/andy16/...` paths. It is the one known deviation.

## Tool substitutions (coreutils replacements)

| Instead of | Use       | Where it is wired up                                   |
|------------|-----------|--------------------------------------------------------|
| `rm`       | `trash`   | `alias rm="trash"` — `rr` is the escape hatch for real `rm` |
| `ls`       | `eza`     | `ls`, `lsd`, `lsf`, `tree`, `tree2..4`, `treeall` aliases |
| `find`     | `fd`      | FZF defaults, `fdf`, `fdd`                             |
| `grep`     | `rg`      | Not aliased. In-file comment: "Prefer 'rg' (ripgrep) over grep" |
| `cat`      | `bat`     | FZF previews                                           |
| `htop`     | `btop`    | `alias htop="btop"`                                    |

## Shell behavior preferences

- **Case-sensitive completion** (`CASE_SENSITIVE="true"`)
- **Autocorrect is off** (`unsetopt correct` / `unsetopt correct_all`) — no "did you mean…" prompts
- **Magic functions disabled** (`DISABLE_MAGIC_FUNCTIONS=true`) — avoids zsh auto-escaping URLs in ways that break pasted commands
- **Shared history with dedupe** — `SHARE_HISTORY`, `HIST_IGNORE_ALL_DUPS`, `HIST_SAVE_NO_DUPS`, `HIST_FIND_NO_DUPS`, `HIST_IGNORE_SPACE`, `HIST_VERIFY`

## Locale and terminal

- `LC_ALL=en_CA.UTF-8` — Canadian English
- Terminal: Ghostty on macOS
- `EDITOR=nano`, `VISUAL=zed --wait`

## Startup performance rules

- **`zsh-syntax-highlighting` must always be the last plugin** in the `plugins=(...)` list
- **P10k instant prompt bootstrap must stay at the very top** of the file (above any output)
- **`compinit` is called once** near the end of the file, with a 24-hour cache (`compinit -C`) unless the dump file is stale
- **nvm is lazy-loaded** — see `node-nvm-lazy-load.md`. Do not add `source $NVM_DIR/nvm.sh` at the top.

## Organisational conventions

- Aliases are grouped by `=== CATEGORY ===` markers. Keep new aliases under the right category.
- Helpers that need logic use **functions**, not aliases (`vs`, `fdf`, `fdd`, `ggco`, `mkcd`, `ggc`, `git-clone-*`, `_ttm_*`).
- Interactive fzf functions always guard with `[ -t 0 ]` so they do not trigger inside scripts.

## Ergonomics

- From `$HOME`, the shell auto-cds into `$PROJ_DEFAULT` (`forzr`) and runs `ls`. Shells started elsewhere are left alone.
- `_ttm_*` tmux engine gives reproducible 3-pane windows (`oc` / `ls` / `oc`) under a single `main` session, one window per project.
- All `cd*` bookmark aliases clear the screen and run `ls` on arrival.

## Git workflow preferences

- Short aliases for everyday commands: `gs`, `gp`, `gl`, `gb`, `gdiff`, `gglog`, `gauto`.
- `gsync` combines push + fetch (`git push origin HEAD && git fetch origin`).
- Worktrunk (`wt`) wrappers: `wc`, `wm`, `wl`, `ws`, `wmain`.
- Custom clone helpers wrapped as shell functions so they can `cd` the parent shell: `git-clone-branch-out`, `git-clone-delete`, `git-clone-clean` (aliased `gclone`, `gclonedel`, `ggcl`).
