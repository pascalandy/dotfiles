---
name: alias catalog
description: All aliases grouped by the === CATEGORY === markers used in the zshrc
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Alias Catalog

Aliases are grouped in the source file by `=== CATEGORY ===` markers. Respect those groups when adding new aliases.

## Miscellaneous

| Alias  | Expansion         |
|--------|-------------------|
| `yt`   | `yt-transcript`   |

## `=== SYSTEM & NAVIGATION ===`

| Alias | Expansion |
|-------|-----------|
| `c`   | `clear`   |
| `o`   | `open .`  |
| `..`  | `cd ..`   |

## `=== FILE OPERATIONS ===`

| Alias   | Expansion    | Note                                       |
|---------|--------------|--------------------------------------------|
| `cp`    | `cp -iv`     | interactive + verbose                      |
| `mv`    | `mv -iv`     | interactive + verbose                      |
| `rmi`   | `rm -i`      |                                            |
| `rm`    | `trash`      | safe delete — works for files and dirs     |
| `rr`    | `/bin/rm`    | escape hatch when you really mean POSIX rm |
| `ln`    | `ln -i`      |                                            |
| `mkdir` | `mkdir -pv`  |                                            |
| `size`  | `du -sh`     |                                            |
| `disk`  | `df -h`      |                                            |

A comment in the file reminds: "Prefer 'rg' (ripgrep) over grep for better performance."

## `=== DIRECTORY LISTING (EZA) ===`

All clear the screen first.

| Alias     | Flavor                                     |
|-----------|--------------------------------------------|
| `ls`      | files + dirs, non-recursive, time-sorted   |
| `lsd`     | directories only                           |
| `lsf`     | files only                                 |
| `tree`    | recursive depth 5                          |
| `tree4`   | recursive depth 4                          |
| `tree3`   | recursive depth 3                          |
| `tree2`   | recursive depth 2                          |
| `treeall` | recursive without depth cap                |

## `=== DEVELOPMENT TOOLS ===`

| Alias  | Expansion                               |
|--------|-----------------------------------------|
| `f`    | `fzf`                                   |
| `fman` | `compgen -c \| fzf \| xargs man`        |

## `=== CONFIGURATION ===`

| Alias    | Expansion                                                    |
|----------|--------------------------------------------------------------|
| `reload` | `source $HOME/.zshrc && echo 'ZSH config reloaded!'`         |

## `=== APPLICATIONS ===`

| Alias    | Expansion           |
|----------|---------------------|
| `obs`    | `open -a Obsidian`  |
| `neovim` | `nvim`              |
| `trix`   | `cmatrix -u 9`      |
| `htop`   | `btop`              |
| `aqua`   | `asciiquarium`      |

## `=== NETWORK & SYSTEM INFO ===`

| Alias      | Expansion                       |
|------------|---------------------------------|
| `ports`    | `lsof -PiTCP -sTCP:LISTEN`      |
| `myip`     | `curl -s ifconfig.me`           |
| `localip`  | `ipconfig getifaddr en0`        |
| `flushdns` | `sudo dscacheutil -flushcache`  |

## `=== TEXT PROCESSING ===`

| Alias   | Expansion |
|---------|-----------|
| `count` | `wc -l`   |
| `json`  | `jq .`    |

## `=== GIT ALIASES - CORE ===`

| Alias       | Expansion                                   |
|-------------|---------------------------------------------|
| `gsync`     | `git push origin HEAD && git fetch origin`  |
| `treep`     | `devtree-pascalandy-blog-paper`             |
| `gs`        | `git status -s`                             |
| `gp`        | `git push`                                  |
| `gl`        | `git pull`                                  |
| `gdiff`     | `git diff`                                  |
| `gclone`    | `git-clone-branch-out` (wrapped by a function for cd support) |
| `gclonedel` | `git-clone-delete` (wrapped for cd support) |

## `=== GIT ALIASES - BRANCHES ===`

| Alias   | Expansion                                    |
|---------|----------------------------------------------|
| `gb`    | `git branch`                                 |
| `gbd`   | `git branch -d`                              |
| `gbD`   | `git branch -D`                              |
| `gbn`   | `git branch --no-merged`                     |
| `gauto` | `git add . && gcauto && git push`            |

## Git log

| Alias   | Expansion                                                   |
|---------|-------------------------------------------------------------|
| `gglog` | `git --no-pager log --oneline --graph -10 --decorate=short` |
| `ggcl`  | `git-clone-clean`                                           |

## `=== WORKTRUNK ===`

| Alias   | Expansion                    |
|---------|------------------------------|
| `wc`    | `wt switch -c`               |
| `wm`    | `wt merge`                   |
| `wl`    | `wt list --no-progressive`   |
| `wls`   | `wt list --no-progressive`   |
| `ws`    | `wt switch`                  |
| `wmain` | `wt switch ^`                |

## `=== AI AGENT CLI ===`

| Alias  | Expansion                              |
|--------|----------------------------------------|
| `oc`   | `opencode`                             |
| `cld`  | `claude`                               |
| `cldd` | `claude --dangerously-skip-permissions`|

## `=== gemini ===`

| Alias    | Expansion                                       |
|----------|-------------------------------------------------|
| `ggem`   | `gemini -m gemini-3-flash-preview --yolo`       |
| `ggemy`  | `gemini -m gemini-3-flash-preview --yolo`       |
| `gemini` | `gemini -m gemini-3-flash-preview`              |

## `=== configs ===`

| Alias  | Expansion                                      |
|--------|------------------------------------------------|
| `ccma` | `chezmoi apply`                                |

## `=== script manage via chezmoi ===`

| Alias  | Expansion                                                |
|--------|----------------------------------------------------------|
| `uca`  | `cd $HOME/.local/share/chezmoi && just uca`              |
| `ttok` | `ttok "${@}" 2>/dev/null`                                |
| `run`  | `run-script`                                             |

## Not in the zshrc but referenced by comments

- `vps1..4` — SSH with coloured terminals, standalone scripts in `$HOME/.local/bin`
- `spl2`, `spl3`, `spl3c`, `spl3v`, `spl4` — tmux split layouts (standalone scripts)
- `antinote` — query the Antinote SQLite database (standalone script)
