---
name: toolchain
description: fzf, fd, eza, bat, ripgrep, and zoxide configuration
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Toolchain

## Zoxide

Initialised with:
```zsh
eval "$(zoxide init zsh)"
```
Provides the `z` frecency-based directory jumper alongside standard `cd`.

## FZF

Initialised with `eval "$(fzf --zsh)"`. Defaults:

```zsh
export FZF_DEFAULT_COMMAND="fd --hidden --strip-cwd-prefix --exclude .git "
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"
export FZF_ALT_C_COMMAND="fd --type=d --hidden --strip-cwd-prefix --exclude .git"
export FZF_DEFAULT_OPTS="--height 50% --layout=default --border --color=hl:#2dd4bf"
export FZF_CTRL_T_OPTS="--preview 'bat --color=always -n --line-range :500 {}'"
export FZF_ALT_C_OPTS="--preview 'eza -ls=time -r --git --tree --level=2 --git-ignore --no-user --no-permissions --group-directories-first --git-repos --icons=always --total-size {} | head -20'"
```

Observations:
- `fd` is the fuzzy source for both file (`CTRL+T`) and directory (`ALT+C`) pickers
- `.git` is always excluded
- Preview commands use `bat` for files and `eza --tree` for directories
- Teal highlight colour (`#2dd4bf`)
- A comment in the source warns that fzf can open unexpectedly in non-interactive scripts — functions using fzf (`fdf`, `fdd`, `ggco`) guard with `[ -t 0 ]`

## eza (ls replacement)

Used by multiple aliases, all with screen clear:

| Alias      | What it shows                                     |
|------------|---------------------------------------------------|
| `ls`       | Files + dirs, non-recursive, time-sorted reverse  |
| `lsd`      | Directories only                                  |
| `lsf`      | Files only                                        |
| `tree`     | Recursive, depth 5, git-ignore aware              |
| `tree4`    | Recursive, depth 4                                |
| `tree3`    | Recursive, depth 3                                |
| `tree2`    | Recursive, depth 2                                |
| `treeall`  | Recursive, no depth cap                           |

Common flags across the aliases:
```
-l --sort=time --reverse --no-user --no-permissions --group-directories-first --icons=always --git --git-ignore --git-repos --total-size
```

## bat

Not aliased directly — used as the preview command inside FZF (`--color=always -n --line-range :500`). Assumed available on `PATH`.

## fd

Used as:
- FZF default source
- Backbone of `fdf` (file picker) and `fdd` (directory picker)

Flags in interactive use: `--type f|d --hidden --exclude .git`.

## ripgrep

Not initialised in the zshrc, but an in-file comment reads:
```
# Note: Prefer 'rg' (ripgrep) over grep for better performance
```
and the global `$HOME/.claude/CLAUDE.md` lists `rg` as the preferred search tool.
