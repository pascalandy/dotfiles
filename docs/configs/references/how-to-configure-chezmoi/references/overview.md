---
name: Chezmoi Overview
description: Mental model for chezmoi — source vs applied, copies not symlinks, and what happens on apply
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-to-configure-chezmoi
---

Chezmoi is a dotfiles manager. It keeps your configuration files in one directory (the **source**), then copies them into your home directory (the **target**) when you run `chezmoi apply`. The key idea: your home directory does not contain the originals. It contains copies.

## Source vs Applied

| Concept | Where | Role |
|---|---|---|
| **Source** | `~/.local/share/chezmoi/` | The tree you edit, commit, and version-control. Single source of truth. |
| **Applied target** | `~/` | The tree chezmoi *produces*. Everything here is a copy overwritten on every `chezmoi apply`. |

Rule: **never edit the applied target directly**. Any change you make in `~/.config/foo` or `~/.zshrc` gets wiped the next time someone runs `chezmoi apply`. Edit the source instead.

To check whether a file is managed:

```bash
chezmoi managed | grep .zshrc
```

To open the source file for a managed target:

```bash
chezmoi edit ~/.zshrc
```

`chezmoi edit` translates the target path into the corresponding source path automatically (e.g. `~/.zshrc` → `~/.local/share/chezmoi/dot_zshrc`), so you do not have to remember the prefix rules by hand.

## Copies, not symlinks

Unlike `stow` or a hand-rolled `ln -s`, chezmoi copies files from source to target. This means:

- Your home directory keeps working even if the source directory is unmounted.
- You must run `chezmoi apply` to propagate changes — editing the source is not enough.
- `chezmoi diff` shows what an apply would change before it changes anything.

The only exception is the `symlink_` prefix, which creates an actual symlink. Everything else is a literal copy.

## What happens on `chezmoi apply`

A plain `chezmoi apply` does the following, in order:

1. Runs any `.chezmoiscripts/run_before_*.sh` scripts.
2. Walks the source tree and, for each file:
   - resolves the target name by stripping prefixes and adding the leading `.` from `dot_`
   - renders `.tmpl` files through Go `text/template`
   - applies permissions (`private_` → 600/700, `executable_` → +x)
   - writes the result to the target path, replacing what was there
3. Runs any `.chezmoiscripts/run_after_*.sh` scripts.

The run scripts are important: a repo that has them is not doing a plain copy. `chezmoi apply` in such a repo has side effects that go beyond its own source tree. Always read the `.chezmoiscripts/` contents when joining a new chezmoi repo.

## Dry runs are cheap

Any time you are unsure, preview first:

```bash
chezmoi apply -n -v
```

`-n` is dry-run, `-v` is verbose. It tells you exactly which files would change and how, without touching anything. Use it before every real apply.

## Related

- [[cli]]
- [[naming-conventions]]
- [[templates]]
- [[how-my-chezmoi-is-configured]]
