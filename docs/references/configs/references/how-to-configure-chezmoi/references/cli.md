---
name: Chezmoi CLI
description: Full command table for the chezmoi CLI with a one-line description for each
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-to-configure-chezmoi
---

The chezmoi CLI has a large command surface. This page covers the commands an agent working in a managed dotfiles repo routinely needs. For anything beyond this list, see [[upstream-links]].

## Setup

| Command | Purpose |
|---|---|
| `chezmoi init` | Initialize a new source directory. |
| `chezmoi init <repo-url>` | Initialize and clone an existing dotfiles repo. |

## Daily workflow

| Command | Purpose |
|---|---|
| `chezmoi managed` | List every file chezmoi currently manages. |
| `chezmoi managed \| grep <pattern>` | Check whether a specific file is managed before editing it. |
| `chezmoi unmanaged` | List files in `~/` that are *not* managed. |
| `chezmoi status` | Show file states (`M` modified, `A` added, `R` will-run for scripts). |
| `chezmoi diff` | Show the diff between source and applied target. |
| `chezmoi edit <target>` | Open the source file for a managed target path. Translates the path automatically. |
| `chezmoi apply` | Apply all pending changes from source to home. |
| `chezmoi apply -v` | Same, with verbose output. |
| `chezmoi apply -n -v` | Dry run: show what would change without writing anything. |
| `chezmoi cd` | Launch a shell inside the source directory (`~/.local/share/chezmoi/`). |

## Adding and removing

| Command | Purpose |
|---|---|
| `chezmoi add <target>` | Start managing an existing file in `~/`. Copies it into the source tree with the right prefix. |
| `chezmoi re-add <target>` | Re-copy a managed file from `~/` back into the source (useful after an upstream tool rewrites its own config). |
| `chezmoi forget <target>` | Stop managing a file but leave the applied copy in `~/` alone. |
| `chezmoi remove <target>` | Stop managing *and* delete the applied copy. |

## Templates and data

| Command | Purpose |
|---|---|
| `chezmoi data` | Print every variable chezmoi exposes to templates (machine info, OS, custom data from `chezmoi.toml`). |
| `chezmoi execute-template '<expr>'` | Evaluate a template expression against the current data. Use this to debug templates without running `apply`. |
| `chezmoi cat <target>` | Print the rendered contents chezmoi would write to a target, without applying. Great for inspecting a `.tmpl` result. |

## Secrets

| Command | Purpose |
|---|---|
| `chezmoi secret keyring set --service=<name> --user=<key>` | Store a secret in the OS keyring. macOS uses Keychain. |
| `chezmoi secret keyring get --service=<name> --user=<key>` | Retrieve a secret for verification. |
| `chezmoi secret keyring delete --service=<name> --user=<key>` | Delete a stored secret. |

See [[secrets]] for template usage.

## Related

- [[overview]]
- [[naming-conventions]]
- [[templates]]
- [[secrets]]
- [[upstream-links]]
