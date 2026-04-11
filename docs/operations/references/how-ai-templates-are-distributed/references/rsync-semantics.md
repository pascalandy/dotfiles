---
name: Rsync Semantics
description: The rsync flag set used by `fct_copy_dir`, what `--delete` really prunes, and the interaction with the missing `exact_` prefix on the source
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-ai-templates-are-distributed
---

Every fan-out target runs through `fct_copy_dir` at `.chezmoiscripts/run_after_backup.sh:21`. This page explains what that function's rsync flags mean in practice and how they interact with the rest of the apply pipeline.

## The function

```bash
fct_copy_dir() {
	local src_dir="$1"
	local dst_dir="$2"
	local sync_mode="${3:-delete}"
	local -a extra_args=("${@:4}")
	local -a rsync_args

	rsync_args=(-a --exclude '.DS_Store')

	if [[ "$sync_mode" == "delete" ]]; then
		rsync_args+=(--delete --delete-excluded --force)
	fi
	# ... guards omitted ...
	rsync "${rsync_args[@]}" "$src_dir/" "$dst_dir/"
}
```

Every call from `fct_sync_agent_assets` passes only two arguments, so `sync_mode` defaults to `delete` and the full flag set is always applied.

## What each flag does

| Flag | Meaning | Why it is in the set |
|---|---|---|
| `-a` | Archive mode: recursive, preserve permissions, timestamps, symlinks, ownership where possible. | Matches chezmoi's semantics — the destination should look like the source, metadata included. |
| `--exclude '.DS_Store'` | Do not copy macOS Finder metadata files. | macOS development machine, and `.DS_Store` would constantly churn the rsync. |
| `--delete` | Remove destination files that are not in the source. | Source of truth semantics: a file removed from `dot_config/ai_templates/` should disappear from every agent home on the next apply. |
| `--delete-excluded` | Also remove destination files that match an `--exclude` pattern. | Stale `.DS_Store` files in destination trees get cleaned up instead of accumulating. |
| `--force` | Allow deletion of non-empty destination directories when they need to be replaced by a file (or removed). | Prevents the rsync from aborting on awkward destination state. |

Trailing slashes on `"$src_dir/" "$dst_dir/"` are significant: with the slash, rsync copies the *contents* of the source directory into the destination, not the source directory itself. Dropping the trailing slash on either side would produce a different and almost-always-wrong layout.

## Why `--delete` is load-bearing

A deletion in `dot_config/ai_templates/` needs to propagate to every agent home. Without `--delete`, the rsync would copy new and changed files but leave old files behind. Over time each agent home would accumulate orphaned skills and commands, and the four agent homes would drift away from the source of truth.

With `--delete`, every apply reconstructs each destination to match its source. The cost is that rsync is authoritative — any file an operator writes directly into an agent home is removed on the next apply. This is the reason "never edit files under an agent home" is a rule in this repo.

## The missing `exact_` prefix on the source

Chezmoi has its own mechanism for "the destination should be exactly the source": the `exact_` prefix on a directory. When a source directory is `exact_foo`, chezmoi removes any entries in the applied target under `foo/` that do not appear in the source. Without the prefix, chezmoi leaves unrelated files in place.

`dot_config/ai_templates/skills/` **does not have the `exact_` prefix**. The directory is simply `dot_config/ai_templates/skills/`. That means:

1. When `chezmoi apply` runs, chezmoi itself will not prune files from `~/.config/ai_templates/skills/` that were removed from the source. If you delete `dot_config/ai_templates/skills/utils/foo/`, the applied path `~/.config/ai_templates/skills/utils/foo/` stays behind until some other mechanism removes it.
2. The render stage uses `chezmoi archive --format tar "$HOME/.config/ai_templates"`. This archives the **applied state**, which includes the stale directory. So the scratch render tree would still contain `utils/foo/`.
3. The rsync fan-out is what actually removes the stale entry from each agent home, because each `fct_copy_dir` call runs with `--delete`.

**Reality is messier than that clean story.** Because `exact_` is absent, `~/.config/ai_templates/` accumulates orphaned files over time, and `chezmoi archive` faithfully includes them. It is the fan-out rsync that keeps agent homes clean, not chezmoi. But:

- The orphans persist in `~/.config/ai_templates/` itself, which is the applied (not source) copy. Nothing ever removes them.
- If a new agent home was added that copied from `dot_config/ai_templates/` without `--delete`, it would inherit the accumulated orphans.
- A render from source path (`chezmoi archive "$HOME/.local/share/chezmoi/dot_config/ai_templates"`) would give a different answer than the current target-path render, and the difference is exactly the orphan set.

The simplest fix for the underlying drift would be to rename `dot_config/ai_templates/skills/` to `exact_dot_config/ai_templates/exact_skills/` (and same for `commands/`), so chezmoi prunes the applied copy on every apply. That would also let `chezmoi archive` produce a source-equivalent tree without relying on the rsync to paper over the difference.

This fix is **not applied** by this wiki. Documenting the drift is sufficient for now. Decide and execute in a separate task.

## Interaction with Claude Code flattening

The Claude Code subtree is fanned out by four separate calls that all target `~/.claude/skills/`. Because each call runs with `--delete`, each call wipes the previous call's output. Only the final call (`utils/`) survives. See [claude-code-flattening.md](claude-code-flattening.md) for the full analysis and verification. The same `--delete` flag that enforces source-of-truth mirroring in single-destination calls is the reason the shared-destination Claude Code flow does not produce a real merge.

## The `merge` mode that exists but is never used

`fct_copy_dir` supports `sync_mode=merge`. Passing anything other than `"delete"` as the third argument skips the `--delete --delete-excluded --force` append. No call in the current script uses it. The mode exists as an opt-in for future work — e.g., a target that needs additive-only updates, where removing an entry from the source should not remove it from the destination.

If the Claude Code flattening is ever fixed by switching to `merge` (option 1 in [claude-code-flattening.md](claude-code-flattening.md)), that would be the first caller of the merge mode in this script.

## Related

- [[overview]]
- [[render-stage]]
- [[fan-out-targets]]
- [[claude-code-flattening]]
- [[troubleshooting]]
- [[how-to-configure-chezmoi]]
