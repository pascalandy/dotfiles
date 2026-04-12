---
name: VS Code Pre-Apply Sync
description: Three diff-gated copies that pull VS Code settings, keybindings, and extensions from the live user directory back into the chezmoi source before every apply
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-vscode-and-brewfile-sync-back
---

`.chezmoiscripts/run_before_sync.sh` runs before every `chezmoi apply`. Its first job is to capture any VS Code configuration changes that were made outside of chezmoi and land them back in the chezmoi source so the next commit can pick them up.

## Why the reverse direction exists

VS Code writes its settings whenever you change a preference in the Settings UI. Keybindings are edited through the Keybindings editor. Extensions are installed and removed through the Extensions sidebar. None of these operations touch the chezmoi source — they write to `~/Library/Application Support/Code/User/` directly.

If the chezmoi source stayed unchanged, every `chezmoi apply` would overwrite the live config with the stale source, clobbering all UI-made changes. The pre-apply script inverts that: it copies the live config *into* the chezmoi source first, so the subsequent apply has no new information to write back and effectively becomes a no-op for these files.

## The three sources and destinations

Declared at `.chezmoiscripts/run_before_sync.sh:43-46`:

```bash
VSCODE_USER="$HOME/Library/Application Support/Code/User"
VSCODE_DST="$HOME/.local/share/chezmoi/private_Library/private_Application Support/private_Code/User"
VSCODE_EXT_DST="$HOME/.local/share/chezmoi/dot_config/vscode/extensions.txt"
```

Three files are tracked:

| Live path | Chezmoi source path | Mechanism |
|---|---|---|
| `~/Library/Application Support/Code/User/settings.json` | `private_Library/private_Application Support/private_Code/User/settings.json` | Diff-gated `cp` |
| `~/Library/Application Support/Code/User/keybindings.json` | `private_Library/private_Application Support/private_Code/User/keybindings.json` | Diff-gated `cp` |
| `code --list-extensions` | `dot_config/vscode/extensions.txt` | Diff-gated `cp` via tempfile |

The source paths use nested `private_` prefixes — three of them — because macOS's `Library/Application Support/Code/User/` is under the user library directory and every intermediate level needs the `600`/`700` permission bits. See [[how-to-configure-chezmoi]] → `naming-conventions.md` for the `private_` semantics.

## The diff gate

Every copy is gated on `diff -q`:

```bash
if [[ -f "$VSCODE_USER/settings.json" ]]; then
	if ! diff -q "$VSCODE_USER/settings.json" "$VSCODE_DST/settings.json" >/dev/null 2>&1; then
		log "Syncing VS Code: settings.json to chezmoi source"
		cp "$VSCODE_USER/settings.json" "$VSCODE_DST/settings.json"
		log "VS Code: settings.json synced"
	else
		log "VS Code: settings.json unchanged, skipping"
	fi
fi
```

`diff -q` returns non-zero when the files differ (or when the destination does not exist, which `2>/dev/null` swallows). A non-zero return triggers the `cp`, and the log line records whether the sync happened. A zero return means the files are identical, the copy is skipped, and the log line says "unchanged, skipping".

Same pattern at `.chezmoiscripts/run_before_sync.sh:58` for keybindings and at `.chezmoiscripts/run_before_sync.sh:69` for extensions. The extensions case uses a `mktemp` tempfile because the source is `code --list-extensions` output, not a file on disk.

## Why the extensions list uses a tempfile

`code --list-extensions` prints to stdout. To diff it against the committed list at `dot_config/vscode/extensions.txt`, the script writes the output to a tempfile first and then diffs:

```bash
TEMP_EXT=$(mktemp)
code --list-extensions >"$TEMP_EXT"
if ! diff -q "$TEMP_EXT" "$VSCODE_EXT_DST" >/dev/null 2>&1; then
	cp "$TEMP_EXT" "$VSCODE_EXT_DST"
fi
rm -f "$TEMP_EXT"
```

The `rm -f "$TEMP_EXT"` is unconditional and always runs. If you are reading this in a repo that prefers `trash` over `rm`: yes, this is one of the few exceptions — it is a tempfile and it is safe to `rm`. The `trash` preference from the repo-level preferences applies to user-visible file deletion, not to tempfiles inside a pre-apply script.

## What happens when VS Code is not installed

If `code` is not on the PATH, the extensions block at `.chezmoiscripts/run_before_sync.sh:69` is wrapped in `if command -v code >/dev/null 2>&1; then`. When it fails, the extensions-list copy is silently skipped and the apply proceeds. The `settings.json` and `keybindings.json` copies use `[[ -f ... ]]` guards instead; if VS Code has never been installed on this machine, those files will not exist and the copies are silently skipped as well.

This means a fresh install of the repo on a machine without VS Code will run `chezmoi apply` cleanly, materialize the committed VS Code source files, and never try to read from the live user directory.

## Integration with the rest of the apply

The diff gate is load-bearing here. Without it, the script would `cp` on every apply and dirty the git working tree every time, even when nothing had actually changed. The chezmoi commit habit in this repo depends on `git status` being clean after every apply unless there is a real change.

If you see unexpected entries in `git status` after a `chezmoi apply`, either the live VS Code state diverged from the committed source (legitimate sync), or the diff is spuriously firing because of line-ending differences, whitespace, or other noise. Spot-check with `diff` directly before committing.

## Related

- [[brewfile-dump]]
- [[how-ai-templates-are-distributed]]
- [[how-to-configure-chezmoi]]
