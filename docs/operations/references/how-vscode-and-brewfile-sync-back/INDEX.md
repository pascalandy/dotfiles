---
name: How VS Code and Brewfile Sync Back
description: The pre-apply script that pulls VS Code settings, keybindings, extensions and the Brewfile from the live system back into the chezmoi source
aliases:
  - pre-apply-sync
  - run-before-sync
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# How VS Code and Brewfile Sync Back

<scope>
Load this wiki when the task touches `.chezmoiscripts/run_before_sync.sh`, the VS Code settings/keybindings/extensions in the chezmoi source, or the `dot_Brewfile`.

This script is the *reverse* direction from the rest of chezmoi: instead of copying from chezmoi source into the home directory, it copies from the live home directory back into the chezmoi source so that subsequent `chezmoi apply`, git commit, and git push operations capture local changes made outside of chezmoi itself.

It runs before every `chezmoi apply` as a `run_before_*` script. Sibling wiki for the post-apply fan-out is [[how-ai-templates-are-distributed]].
</scope>

<workflow>
1. Decide what the task actually needs:
   - VS Code settings, keybindings, or extensions changed in VS Code and need to land in git → [vscode-sync.md](references/vscode-sync.md)
   - a new Homebrew package was installed and the `dot_Brewfile` should pick it up → [brewfile-dump.md](references/brewfile-dump.md)
   - understanding the overall pre-apply flow → read both pages in order

2. Never edit the chezmoi source copies of `settings.json`, `keybindings.json`, or `dot_Brewfile` directly. Edit in VS Code or `brew install` as usual, then let the next `chezmoi apply` trigger this script to capture the changes.

3. If a change must land *right now*, run `chezmoi apply -v`. The pre-apply script runs first and syncs back before the rest of the apply executes.
</workflow>

<checklist>
Before finishing any change that touches VS Code configuration or the Brewfile:
- VS Code changes were made in VS Code itself, not in the chezmoi source
- the next `chezmoi apply` completed successfully and `git status` shows the expected updates under `private_Library/.../User/` or `dot_Brewfile`
- if a Brewfile dump was expected, the 72h rate limit did not silently skip it (check `.last_brewfile_sync`)
- the commit message references the source of the change (e.g. "VS Code settings update" or "Brewfile dump")
</checklist>

<references>
Load only what the task needs:
- [vscode-sync.md](references/vscode-sync.md) — the three diff-gated copies for settings, keybindings, and the extensions list
- [brewfile-dump.md](references/brewfile-dump.md) — the master switch, the 72h rate limit, the force-sync recipe
</references>

---

> Content catalog. Every wiki page is listed here with a one-line summary.
> **Total pages:** 3 | **Last updated:** 2026-04-11

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/doc

| File | Description |
|------|-------------|
| `references/vscode-sync.md` | VS Code settings.json, keybindings.json, extensions list — diff-gated copy from live user dir into chezmoi source |
| `references/brewfile-dump.md` | `brew bundle dump` into `dot_Brewfile`, gated by `SYNC_BREWFILE` and a 72-hour timestamp file |

## Related

- [[how-ai-templates-are-distributed]] — the sibling post-apply fan-out
- [[how-to-configure-chezmoi]] — generic chezmoi mechanics, including `run_before_*` scripts
- [[how-my-chezmoi-is-configured]] — which files in this repo are templated today
