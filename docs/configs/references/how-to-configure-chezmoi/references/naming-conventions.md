---
name: Chezmoi Naming Conventions
description: Source filename prefixes and the `.tmpl` suffix that control how chezmoi translates source names into applied targets
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-to-configure-chezmoi
---

Chezmoi uses filename prefixes and suffixes to encode metadata about each source file. The prefix tells chezmoi what kind of target to produce; the suffix controls how the file is processed. Getting the name right is how you control the permissions, hidden-ness, and templating of the applied copy.

## Prefix table

| Prefix | What it does | Example source → target |
|---|---|---|
| `dot_` | Applied name starts with `.` | `dot_zshrc` → `~/.zshrc` |
| `private_` | Applied with `600` for files or `700` for directories | `private_dot_ssh/config` → `~/.ssh/config` (mode 600) |
| `executable_` | Applied with `+x` permission | `executable_passgen` → `~/passgen` (mode +x) |
| `readonly_` | Applied read-only | `readonly_secrets.yaml` → `~/secrets.yaml` (mode 0444) |
| `symlink_` | Creates a symlink instead of a copy | `symlink_AppSupport` → `~/AppSupport` (symlink) |
| `exact_` | Directory is managed exactly: files in `~/` that are *not* in source get deleted | `exact_dot_config/foo/` removes any untracked files under `~/.config/foo/` on apply |
| `empty_` | File is allowed to be empty | `empty_dot_hushlogin` → `~/.hushlogin` (empty file allowed) |

Prefixes can be stacked. Common combinations:

- `private_dot_ssh` → `~/.ssh` with mode 700
- `executable_dot_local/bin/hello` → `~/.local/bin/.hello` with +x (rarely needed — the `dot_` applies to the file, not the whole path)
- `private_executable_my-secret-script` → `~/my-secret-script` with mode 700 (private trumps the exact executable mask)

## Suffixes

| Suffix | What it does |
|---|---|
| `.tmpl` | The file is a Go `text/template`. Chezmoi renders it on apply before writing. Any file using `{{ }}` must have this suffix or the braces will reach the applied copy literally. |

Examples:

- `dot_zshrc` → plain copy, no templating.
- `dot_zshenv.tmpl` → renders through templates, applied to `~/.zshenv`.
- `private_dot_ssh/config.tmpl` → renders, applied to `~/.ssh/config` with mode 600.
- `executable_voxtral.tmpl` → renders, applied to `~/voxtral` with +x.

## Run script prefixes

Files under `.chezmoiscripts/` (or anywhere in the source tree, though a dedicated directory is preferred) can use run prefixes to fire shell scripts around an apply:

| Prefix | When it runs |
|---|---|
| `run_before_<name>.sh` | Before chezmoi walks the source tree on every apply. |
| `run_after_<name>.sh` | After chezmoi finishes applying files, on every apply. |
| `run_once_<name>.sh` | Only the first time chezmoi sees this script (content hash tracked). |
| `run_onchange_<name>.sh` | Only when the script contents change. |

Run scripts appear in `chezmoi status` with an `R` flag. Seeing `R` on every apply is normal for `run_after_*.sh` and does *not* mean the repo is drifting.

## Common mistakes

- **Forgetting `.tmpl`.** You add a variable like `{{ keyring "foo" "bar" }}` to a plain file. The braces end up literally in the applied copy. Always check: if the source body contains `{{`, the filename must end in `.tmpl`.
- **Editing the applied target.** You open `~/.zshrc` and save. The next `chezmoi apply` wipes your change. Always edit the source, or use `chezmoi edit ~/.zshrc` which opens the source for you.
- **Wrong prefix order.** `private_` and `executable_` go *before* `dot_`: `private_executable_dot_foo`, not `dot_private_executable_foo`. When unsure, run `chezmoi add <target>` first and let chezmoi pick the name.

## Related

- [[overview]]
- [[cli]]
- [[templates]]
- [[how-my-chezmoi-is-configured]]
