---
name: custom shell functions
description: Non-tmux helper functions defined directly in the zshrc
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Custom Shell Functions

Functions that exist because aliases are not expressive enough. These are the non-tmux helpers — the `_ttm_*` engine has its own reference.

## File and directory navigation

### `vs [path]`
```zsh
vs() {
    open "${1:-.}" -a "Visual Studio Code"
}
```
Opens the argument (or current directory if absent) in Visual Studio Code via macOS `open`.

### `fdf`
Interactive file picker.
- Source: `fd --type f --hidden --exclude .git`
- Picker: `fzf` with an `eza` preview
- Action: opens the selection in VS Code via `vs`
- Guard: wrapped in `[ -t 0 ]`; prints "fdf: not available in non-interactive mode" otherwise

### `fdd`
Interactive directory picker.
- Source: `fd --type d --hidden --exclude .git`
- Picker: `fzf` with an `eza` preview
- Action: `cd` into the selection and then run `vs` to open it in VS Code
- Guard: same `[ -t 0 ]` check

### `mkcd <dir>`
```zsh
mkcd() {
    mkdir -p "$1" && cd "$1"
}
```
Create a directory and enter it.

## Git helpers

### `ggco`
Interactive git branch checkout.
- Source: `git branch --all | grep -v HEAD | sed "s/remotes\/origin\///" | sort -u`
- Picker: `fzf`
- Action: `git checkout "$branch"`
- Guard: `[ -t 0 ]`

### `ggc [message]`
```zsh
ggc() {
    git add . && git commit -m "${1:-minor}"
}
```
Stage everything and commit with the given message; defaults to `minor` when no argument is supplied.

### `git-clone-branch-out(...)` and `git-clone-delete(...)`
```zsh
git-clone-branch-out() {
  local clone_path
  clone_path="$(command git-clone-branch-out "$@")" || return $?
  [[ -n "$clone_path" && -d "$clone_path" ]] && cd "$clone_path"
}

git-clone-delete() {
  local result
  result="$(command git-clone-delete "$@")" || return $?
  [[ "$result" == "deleted" ]] && cd ..
}
```
Wrapper functions around the standalone scripts in `$HOME/.local/bin`. The wrappers exist because scripts cannot `cd` their parent shell — the wrappers capture the script's final output (a path or the literal `deleted`) and perform the cd themselves.

Aliased as `gclone` and `gclonedel`.

## Convention for new interactive fzf functions

```zsh
myfn() {
    if [ -t 0 ]; then
        # interactive work with fzf
    else
        echo "myfn: not available in non-interactive mode"
    fi
}
```

The `[ -t 0 ]` guard is mandatory: it prevents fzf from opening unexpectedly inside scripts or hooks.
