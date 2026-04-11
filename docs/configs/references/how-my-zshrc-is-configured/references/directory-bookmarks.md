---
name: directory bookmarks
description: cd shortcuts and PROJ_* environment variables for quick navigation
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Directory Bookmarks

## Exported path variables

| Var            | Value                                   |
|----------------|-----------------------------------------|
| `PROJ_HOME`    | `$HOME/Documents/github_local`          |
| `MY_DOCS`      | `$HOME/Documents/_my_docs`              |
| `PROJ_DEFAULT` | `$HOME/Documents/github_local/forzr`    |

## Auto-cd at startup

```zsh
[[ "$PWD" == "$HOME" ]] && { cd "$PROJ_DEFAULT" && ls; }
```

A new shell started in `$HOME` jumps straight to `forzr` and lists its contents. Shells opened anywhere else are left where they are.

## `cd*` aliases

All clear the screen, `cd`, then `ls`.

| Alias | Target                                                       | Mnemonic          |
|-------|--------------------------------------------------------------|-------------------|
| `cdc` | `$HOME/.local/share/chezmoi`                                 | **c**hezmoi       |
| `cdd` | `$HOME/Documents/devtree`                                    | **d**evtree       |
| `cde` | `$HOME/Documents/github_local/executive-assistant`           | **e**xec assistant|
| `cdf` | `$PROJ_HOME/forzr`                                           | **f**orzr         |
| `cdh` | `$HOME`                                                      | **h**ome          |
| `cdl` | `$PROJ_HOME`                                                 | **l**ocal projects|
| `cdo` | `$PROJ_HOME/os_pascal`                                       | **o**s_pascal     |
| `cdm` | `$MY_DOCS`                                                   | **m**y_docs       |
| `cdp` | `$PROJ_HOME/pascalandy-blog-paper`                           | **p**ascalandy    |
| `cdv` | `$MY_DOCS/10_obsidian/vault_obsidian`                        | **v**ault         |

## Convention

- Every `cd*` alias runs `ls` on arrival so directory contents are always visible
- The first letter of the alias is a hint for the destination
- New bookmarks should follow the same `clear && cd <path> && ls` pattern
