---
name: How to Configure Chezmoi
description: Generic guide for using chezmoi to manage dotfiles — commands, naming conventions, templates, and secrets
aliases:
  - chezmoi-guide
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-18
---

# How to Configure Chezmoi

<scope>
Load this wiki when the task involves using the `chezmoi` CLI to manage dotfiles: installing, adding files, editing source, applying changes, templating, or handling secrets.

This is the **generic guide**. It covers chezmoi as a tool and could be reused by anyone with the same CLI. For this specific repo's conventions, which prefixes are actually in use, which files are templated today, and the `just cm-*` recipe surface, see [[how-my-chezmoi-is-configured]].

Upstream documentation at `https://www.chezmoi.io/` is authoritative for anything not covered here. This wiki only documents what an agent working in this repo routinely needs.
</scope>

<workflow>
1. Decide what kind of task this is:
   - reading or explaining chezmoi behavior → [overview.md](references/overview.md)
   - looking up a command → [cli.md](references/cli.md)
   - naming a new source file → [naming-conventions.md](references/naming-conventions.md)
   - writing or debugging a `.tmpl` file → [templates.md](references/templates.md)
   - handling an API key or credential → [secrets.md](references/secrets.md)
   - anything not covered above → [upstream-links.md](references/upstream-links.md)

2. If the task is about *this* repo's actual setup, jump to [[how-my-chezmoi-is-configured]] instead. This wiki is generic.

3. Never edit files under `~/`. The source of truth is `~/.local/share/chezmoi/`. See `overview.md` for why.
</workflow>

<checklist>
Before finishing any chezmoi-related change:
- edits were made in the chezmoi source tree, not in `~/`
- new source filenames use the right prefix (`dot_`, `private_`, `executable_`, etc.)
- any file using `{{ }}` has the `.tmpl` suffix
- secrets are retrieved via `keyring` or another supported backend, never committed in plaintext
- `chezmoi apply -n -v` (dry run) was used before the real `chezmoi apply -v`
- the target file under `~/` was spot-checked after apply
</checklist>

<references>
Load only what the task needs:
- [overview.md](references/overview.md) — mental model: source vs applied, copies not symlinks, apply semantics
- [cli.md](references/cli.md) — full command table with a one-line description for each
- [naming-conventions.md](references/naming-conventions.md) — prefixes and the `.tmpl` suffix with examples
- [templates.md](references/templates.md) — Go `text/template` basics, `chezmoi data`, `chezmoi execute-template`
- [secrets.md](references/secrets.md) — keyring backend, alternatives, best practices, `.env` migration
- [upstream-links.md](references/upstream-links.md) — canonical pointers to `chezmoi.io` for anything this wiki does not cover
</references>

---

> Content catalog. Every wiki page is listed here with a one-line summary.
> Read this first to find relevant pages for any query.
> **Total pages:** 7 | **Last updated:** 2026-04-11

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/doc

| File | Description |
|------|-------------|
| `references/cli.md` | Full command table: init, add, edit, apply, diff, status, managed, cd, forget, remove |
| `references/naming-conventions.md` | Source filename prefixes (`dot_`, `private_`, `executable_`, `symlink_`, `exact_`, `readonly_`) and the `.tmpl` suffix |
| `references/overview.md` | Source vs applied, copies not symlinks, what happens on `chezmoi apply` |
| `references/secrets.md` | Keyring integration, alternative backends, best practices, `.env` migration recipe |
| `references/templates.md` | Go `text/template` basics, `chezmoi data`, `chezmoi execute-template` |
| `references/upstream-links.md` | Canonical upstream documentation pointers |

## Related

- [[how-my-chezmoi-is-configured]]
- [[how-to-configure-opencode]]
- [[how-my-zshrc-is-configured]]
