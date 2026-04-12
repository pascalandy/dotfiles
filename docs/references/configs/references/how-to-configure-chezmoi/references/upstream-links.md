---
name: Chezmoi Upstream Links
description: Canonical pointers to chezmoi.io documentation for topics this wiki does not cover
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-to-configure-chezmoi
---

This wiki intentionally covers only what an agent working in this repo routinely needs. For anything beyond that, upstream documentation at `chezmoi.io` is authoritative.

## Entry points

- **User guide** — https://www.chezmoi.io/user-guide/command-overview/
- **Reference manual** — https://www.chezmoi.io/reference/
- **Quick start** — https://www.chezmoi.io/quick-start/
- **Source code** — https://github.com/twpayne/chezmoi

## Topics not covered in this wiki

When the task involves any of these, read upstream first:

| Topic | Upstream page |
|---|---|
| Full command reference with every flag | `/reference/commands/` |
| Full template function list | `/reference/templates/functions/` |
| Config file schema (`chezmoi.toml`) | `/reference/configuration-file/` |
| Archive format options | `/reference/commands/archive/` |
| Platform-specific quirks (Windows, WSL) | `/user-guide/machines/` |
| Advanced scripting patterns | `/user-guide/use-scripts-to-perform-actions/` |
| Importing from another dotfiles tool | `/user-guide/setup/` |
| Encryption (age, GPG) | `/user-guide/encryption/` |

## When to reach for upstream vs this wiki

- Use **this wiki** for the 80% of daily work: what is a prefix, how do I name a template, how does a secret get into a config file, what command do I type to check status.
- Use **upstream** for the 20% of edge cases: a flag you have never seen, a template function missing from this wiki, an error message you do not recognize, or anything platform-specific.

If you find yourself reaching for upstream repeatedly on the same topic, that is a signal the topic should be absorbed into this wiki. Flag it and the omission can be fixed.

## Related

- [[overview]]
- [[cli]]
- [[templates]]
- [[secrets]]
