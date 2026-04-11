---
name: Brewfile Pre-Apply Dump
description: The rate-limited `brew bundle dump` that captures installed Homebrew packages back into `dot_Brewfile` before every apply
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-vscode-and-brewfile-sync-back
---

The second half of `.chezmoiscripts/run_before_sync.sh` runs `brew bundle dump` to capture the current set of installed Homebrew packages into `dot_Brewfile` so the next commit records them. The important detail is the rate limit: the dump runs at most once every 72 hours even if every apply triggers the script.

## Why the rate limit exists

`brew bundle dump` is fast but not free. Running it on every `chezmoi apply` has three problems:

1. **Git noise.** Even when no packages changed, the dump order can shift or formula descriptions can change upstream, making the Brewfile appear modified on every apply.
2. **Apply slowdown.** Every apply pays the cost of `brew bundle dump` — modest on its own, but multiplied across many applies per day it becomes noticeable.
3. **Analytics.** Repeated `brew` invocations show up in Homebrew's anonymous analytics and can trigger rate-limiting behavior upstream.

The rate limit solves all three by using a timestamp file to decide whether enough time has passed since the last successful dump.

## The master switch

From `.chezmoiscripts/run_before_sync.sh:35`:

```bash
SYNC_BREWFILE=true
```

This is a hard-coded flag, not an environment variable. Setting it to `false` in the source file and re-applying will skip the Brewfile logic entirely. The repo's AGENTS.md describes the Brewfile dump as "currently disabled by default via `SYNC_BREWFILE=false`", but the actual source value is `true` — the description in AGENTS.md is stale. In practice the 72h rate limit makes the dump infrequent enough that it feels "mostly disabled", which is likely the source of the outdated description.

If you want to truly disable the dump, change the flag to `false` and commit. If you want to force an immediate dump, see the "Forcing an immediate sync" section below.

## The 72-hour gate

From `.chezmoiscripts/run_before_sync.sh:37-41`:

```bash
BREWFILE_TIMESTAMP="$HOME/.local/share/chezmoi/.last_brewfile_sync"
BREWFILE_DST="$HOME/.local/share/chezmoi/dot_Brewfile"
# 72 hours in seconds
SYNC_INTERVAL=$((72 * 60 * 60))
```

A timestamp file at `.last_brewfile_sync` holds the Unix epoch seconds of the last successful dump. On each apply, the script compares the current time against the stored time and decides whether `SYNC_INTERVAL` has elapsed.

The decision logic at `.chezmoiscripts/run_before_sync.sh:86-105`:

```bash
if [[ "$SYNC_BREWFILE" == true ]]; then
	if [[ -f "$BREWFILE_TIMESTAMP" ]]; then
		last_sync=$(cat "$BREWFILE_TIMESTAMP")
		current_time=$(date +%s)
		time_diff=$((current_time - last_sync))
		if [[ $time_diff -ge $SYNC_INTERVAL ]]; then
			should_sync_brewfile=true
		fi
	else
		should_sync_brewfile=true  # no timestamp → first run, sync
	fi
fi
```

Two paths set `should_sync_brewfile=true`:

- The timestamp exists and `$time_diff >= $SYNC_INTERVAL`. The log line reports the elapsed hours.
- The timestamp does not exist. First-run bootstrap path.

Two paths set `should_sync_brewfile=false` (the default):

- The timestamp exists but not enough time has elapsed. The log line reports the elapsed hours and the threshold.
- `SYNC_BREWFILE=false`. The log line says "skipping Brewfile update".

## The dump itself

From `.chezmoiscripts/run_before_sync.sh:107-116`:

```bash
if [[ "$should_sync_brewfile" == true ]]; then
	if command -v brew >/dev/null 2>&1; then
		log "Updating Brewfile to chezmoi source"
		brew bundle dump --file "$BREWFILE_DST" --force
		date +%s >"$BREWFILE_TIMESTAMP"
		log "Brewfile updated successfully"
	else
		log "Warning: brew command not found, skipping Brewfile update"
	fi
fi
```

`brew bundle dump --force` overwrites the existing `dot_Brewfile`. The `--force` flag is what lets the dump replace a non-empty source file. The timestamp file is updated only *after* a successful dump — a failed dump leaves the old timestamp in place, so the next apply will retry.

If `brew` is not installed (a machine without Homebrew, or a stripped environment), the script logs a warning and proceeds. The apply does not fail.

## Forcing an immediate sync

Delete the timestamp file and run `chezmoi apply`:

```bash
trash ~/.local/share/chezmoi/.last_brewfile_sync
chezmoi apply -v
```

The missing timestamp triggers the first-run bootstrap path, which sets `should_sync_brewfile=true`. The subsequent dump recreates the timestamp, and the 72-hour clock restarts from the new sync.

There is no `--force-brewfile-sync` environment variable or CLI flag. The timestamp file is the only mechanism.

## Interaction with git and commits

A successful dump modifies `dot_Brewfile`. If `git diff` shows changes after an apply, a commit is expected before the next push. The repo's commit habits place this update on its own commit (or alongside a related package installation) rather than mixing it with other changes. The timestamp file `.last_brewfile_sync` is **not** tracked by git — check `.gitignore` if this ever changes, because committing the timestamp would defeat the rate limit on other machines.

## Why the AGENTS.md description is stale

AGENTS.md currently says the Brewfile sync is "currently disabled by default via `SYNC_BREWFILE=false`". The source file disagrees — `SYNC_BREWFILE=true` at `.chezmoiscripts/run_before_sync.sh:35`. The practical effect is the same: the 72-hour gate makes the dump invisible on any given apply, so an operator who runs `chezmoi apply` twice an hour will see it sync maybe once every few days. The description reflects the lived experience rather than the code. When documenting the repo today, the source is the authority — the flag is `true`, the 72-hour rate limit is the reason it feels disabled.

A docs-only correction to AGENTS.md would bring the description into line with the code. Not applied in this documentation pass; flagged for a future cleanup.

## Related

- [[vscode-sync]]
- [[how-to-configure-chezmoi]]
- [[how-my-chezmoi-is-configured]]
