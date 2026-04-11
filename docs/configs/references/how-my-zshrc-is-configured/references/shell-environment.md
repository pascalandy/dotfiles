---
name: shell environment
description: Oh My Zsh, Powerlevel10k, environment variables, history, and completion setup
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Shell Environment

## Framework

- Theme: `ZSH_THEME="powerlevel10k/powerlevel10k"`
- P10k instant prompt block placed before any output, sourced from `${XDG_CACHE_HOME:-$HOME/.cache}/p10k-instant-prompt-${(%):-%n}.zsh`
- `POWERLEVEL9K_INSTANT_PROMPT=quiet` — suppresses instant-prompt console warnings
- Config loaded from `$HOME/.p10k.zsh` when present

## Oh My Zsh plugins

```zsh
plugins=(
    docker
    colored-man-pages
    command-not-found
    macos
    zsh-history-substring-search
    zsh-autosuggestions
    zsh-syntax-highlighting   # always keep this last
)
```

OMZ is sourced from `$ZSH/oh-my-zsh.sh` after plugin declaration. The order of plugins matters — `zsh-syntax-highlighting` must remain last, otherwise it overrides the other plugins' colorisation.

## Environment variables

| Var            | Value                                   | Purpose                     |
|----------------|-----------------------------------------|-----------------------------|
| `ZSH`          | `$HOME/.oh-my-zsh`                      | OMZ install path            |
| `EDITOR`       | `nano`                                  | Terminal-first editor       |
| `VISUAL`       | `zed --wait`                            | GUI editor (git commit etc.) |
| `LC_ALL`       | `en_CA.UTF-8`                           | Canadian English locale     |
| `NVM_DIR`      | `$HOME/.nvm`                            | nvm install path            |
| `GOROOT`       | `/opt/homebrew/opt/go/libexec`          | Go runtime                  |
| `GOPATH`       | `$HOME/go`                              | Go workspace                |
| `PNPM_HOME`    | `$HOME/Library/pnpm`                    | PNPM bin dir                |
| `PROJ_HOME`    | `$HOME/Documents/github_local`          | Project parent              |
| `MY_DOCS`      | `$HOME/Documents/_my_docs`              | Personal docs               |
| `PROJ_DEFAULT` | `$HOME/Documents/github_local/forzr`    | Default project             |

## History

```zsh
HISTSIZE=10000
SAVEHIST=10000
HISTFILE=$HOME/.zsh_history

setopt HIST_VERIFY
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_SAVE_NO_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_FIND_NO_DUPS
setopt SHARE_HISTORY
```

- `HIST_VERIFY` expands `!n` before executing it
- `HIST_IGNORE_ALL_DUPS` drops older duplicates as new ones arrive
- `HIST_SAVE_NO_DUPS` does not write consecutive duplicates to disk
- `HIST_IGNORE_SPACE` skips recording commands that start with a space
- `HIST_FIND_NO_DUPS` hides duplicates during history search
- `SHARE_HISTORY` makes history immediately visible across panes and sessions

## Case sensitivity and corrections

- `CASE_SENSITIVE="true"` — completion matches exact case
- `DISABLE_MAGIC_FUNCTIONS=true` — prevents zsh from auto-escaping pasted URLs
- `unsetopt correct` / `unsetopt correct_all` — no auto-correct prompts

## Other integrations initialised in the middle of the file

- VS Code integration: `[[ "$TERM_PROGRAM" == "vscode" ]] && . "$(code --locate-shell-integration-path zsh)"`
- Claude wrapper with dynamic terminal title: sourced from `$HOME/.config/zsh/claude-wrapper.zsh`
- Zoxide: `eval "$(zoxide init zsh)"`
- FZF: `eval "$(fzf --zsh)"` (see `toolchain.md` for defaults)
- SSH agent via `keychain --eval --quiet`
- `sqlite-utils` zsh completion via its `_SQLITE_UTILS_COMPLETE` hook
- direnv: `eval "$(direnv hook zsh)"`

## Completion init

`fpath` has two additions:
- `$HOME/.oh-my-zsh/custom/completions` (OpenSpec block at the top)
- `$HOME/.zsh/completions` (near the bottom)

Then:
```zsh
autoload -Uz compinit
if [[ -n $HOME/.zcompdump(#qN.mh+24) ]]; then
  compinit
else
  compinit -C
fi
```

Translation: if `.zcompdump` is older than 24 hours, regenerate it; otherwise run `compinit` in cache mode for a fast start.
