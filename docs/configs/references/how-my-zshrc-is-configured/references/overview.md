---
name: zshrc overview
description: Big-picture snapshot of the zshrc sections, tools, and structure
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Overview

> Snapshot of `$HOME/.local/share/chezmoi/dot_zshrc`. This is an analyst report — read the live source when accuracy is required.

## At a glance

- **Shell framework**: Oh My Zsh with Powerlevel10k theme
- **Terminal**: Ghostty (macOS)
- **Package manager**: Homebrew (`shellenv` eval'd at top)
- **Language runtimes**: Node (nvm, lazy-loaded), Go, Rust, Bun, PNPM
- **Editors**: `nano` as `EDITOR`, `zed --wait` as `VISUAL`
- **Locale**: `en_CA.UTF-8`
- **History**: 10,000 lines, shared across sessions, deduped

## File sections (top to bottom)

1. OpenSpec completion init (managed block between `# OPENSPEC:START` / `# OPENSPEC:END`)
2. Powerlevel10k instant prompt bootstrap
3. Homebrew `shellenv` + `command-not-found` handler
4. Environment variables (`ZSH`, `EDITOR`, `VISUAL`, `LC_ALL`, `NVM_DIR`)
5. History configuration
6. Oh My Zsh config (theme, case sensitivity, plugins, sourcing)
7. Node.js lazy load (default-bin preload + wrapper functions)
8. Tooling initializations: VS Code integration, Claude wrapper, Zoxide, FZF, keychain, sqlite-utils
9. Custom functions (`vs`, `fdf`, `fdd`, `ggco`, git-clone wrappers, `mkcd`, `ggc`)
10. `_ttm_*` tmux engine and helper entry points (`ttmj`, `ttmr`, `ttmjc`, `ttmrc`, `ttmM`)
11. Alias catalog organized by `=== CATEGORY ===` sections
12. Directory bookmarks (`cd*` aliases + `PROJ_*` env vars)
13. `direnv hook zsh`
14. `POWERLEVEL9K_INSTANT_PROMPT=quiet`
15. Go environment variables
16. Zsh completions (fpath + cached `compinit`)
17. PATH management (consolidated, dedup'd via `typeset -U path PATH`)
18. Google Cloud SDK path + completion init
19. Worktrunk (`wt`) shell init

## Third-party tools assumed installed

brew, nvm, fzf, fd, eza, bat, ripgrep, trash, zoxide, direnv, keychain, sqlite-utils, tmux, btop, cmatrix, asciiquarium, ttok, Obsidian, Visual Studio Code, Zed, opencode, claude, gemini, wt, just.

## Personal shell scripts (in `$HOME/.local/bin`)

Referenced by aliases and function wrappers: `yt-transcript`, `git-clone-branch-out`, `git-clone-delete`, `git-clone-clean`, `spl2`, `spl3`, `run-script`, `devtree-pascalandy-blog-paper`, `vps1..4`.
