---
name: PATH management
description: How PATH entries are ordered, deduped, and consolidated
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# PATH Management

## Philosophy

Most `PATH` additions are consolidated near the bottom of the zshrc. Ordering matters — earlier entries win ties — and duplicates are kept out automatically:

```zsh
typeset -U path PATH
```

This is a zsh feature that keeps the linked `path` array unique while preserving first-match order.

## Order of additions (consolidated block)

1. **PNPM** — `$HOME/Library/pnpm`. Guarded by a case-matching check so it is not added twice across reloads.
2. **User scripts** — `$HOME/.local/bin` (XDG-compliant location for chezmoi-managed scripts)
3. **browser-use** — `$HOME/.browser-use-env/bin`
4. **Go** — `$GOPATH/bin:$GOROOT/bin` (`GOROOT=/opt/homebrew/opt/go/libexec`, `GOPATH=$HOME/go`)
5. **Rust** — `$HOME/.cargo/bin`
6. **Bun** — `$HOME/.bun/bin`
7. **Amp CLI** — `$HOME/.amp/bin`
8. **LM Studio** — `$HOME/.cache/lm-studio/bin`
9. **yourock2** — `$HOME/Documents/github_firepress/yourock2/flows/main`
10. **ByteRover CLI** — `$HOME/.brv-cli/bin`
11. **Homebrew formulas** — `/opt/homebrew/opt/{ruby,trash,postgresql@18}/bin`
12. **Docker** — `/Applications/Docker.app/Contents/Resources/bin`

## Eagerly prepended earlier in the file

The default nvm-managed node's `bin/` is prepended during the node lazy-load setup (see `node-nvm-lazy-load.md`) so global CLIs like `claude` resolve immediately without sourcing nvm:
```zsh
export PATH="$NVM_DIR/versions/node/$_NODE_DEFAULT/bin:$PATH"
```

## Google Cloud SDK init

Sourced via the auto-generated two-line block at the very bottom of the file:

```zsh
if [ -f "/Users/andy16/Documents/github_local/OS_PASCAL/google-cloud-sdk/path.zsh.inc" ]; then . "/Users/andy16/Documents/github_local/OS_PASCAL/google-cloud-sdk/path.zsh.inc"; fi
if [ -f "/Users/andy16/Documents/github_local/OS_PASCAL/google-cloud-sdk/completion.zsh.inc" ]; then . "/Users/andy16/Documents/github_local/OS_PASCAL/google-cloud-sdk/completion.zsh.inc"; fi
```

These are the two occurrences of hardcoded `/Users/andy16/...` paths in the file — observational only. See `preferences.md` for the "always use `$HOME`" rule.

## Worktrunk (`wt`) shell init

```zsh
if command -v wt >/dev/null 2>&1; then eval "$(command wt config shell init zsh)"; fi
```

Runs at the very end of the file when the `wt` binary is present.
