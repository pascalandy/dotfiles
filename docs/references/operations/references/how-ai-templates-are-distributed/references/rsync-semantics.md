---
name: Rsync Semantics
description: The rsync flag set used by `fct_copy_dir`, what `--delete` prunes, and the interaction with the missing `exact_` prefix on the source
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-ai-templates-are-distributed
---

Every fan-out target runs through `fct_copy_dir` at `.chezmoiscripts/run_after_backup.sh:21-51`. This page explains what that function's rsync flags mean in practice and how they interact with the rest of the apply pipeline.

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

Every call from `fct_sync_agent_assets` passes `"delete"` as the third argument explicitly, so `sync_mode` is always `delete` and the full flag set is always applied. Under the current design, no call opts out of `--delete`.

## What each flag does

| Flag | Meaning | Why it is in the set |
|---|---|---|
| `-a` | Archive mode: recursive, preserve permissions, timestamps, symlinks, ownership where possible. | Matches chezmoi's semantics — the destination should look like the source, metadata included. |
| `--exclude '.DS_Store'` | Do not copy macOS Finder metadata files. | macOS development machine, and `.DS_Store` would constantly churn the rsync. |
| `--delete` | Remove destination files that are not in the source. | Source-of-truth semantics: a file removed from `dot_config/ai_templates/` should disappear from every agent home on the next apply. |
| `--delete-excluded` | Also remove destination files that match an `--exclude` pattern. | Stale `.DS_Store` files in destination trees get cleaned up instead of accumulating. |
| `--force` | Allow deletion of non-empty destination directories when they need to be replaced. | Prevents the rsync from aborting on awkward destination state. |

Trailing slashes on `"$src_dir/" "$dst_dir/"` are significant: with the slash, rsync copies the *contents* of the source directory into the destination, not the source directory itself. Dropping the trailing slash on either side would produce a different and almost-always-wrong layout.

## Why `--delete` is load-bearing

A deletion in `dot_config/ai_templates/` needs to propagate to every agent home. Without `--delete`, the rsync would copy new and changed files but leave old files behind. Over time each agent home would accumulate orphaned skills and commands, and the eight agent homes would drift away from the source of truth.

With `--delete`, every apply reconstructs each destination to match its compiled source. The cost is that rsync is authoritative — any file an operator writes directly into an agent home is removed on the next apply. This is the reason "never edit files under an agent home" is a rule in this repo.

## Why shared destinations are no longer a problem

Earlier versions of `fct_sync_agent_assets` called `fct_copy_dir` four times into `~/.claude/skills/`, each time with a different category subtree as the source and each time with `--delete`. Because `--delete` removes destination files that are not in the current source, each of the four calls wiped the previous call's contribution, and only the last call (`utils/`) survived. The four-call-into-shared-destination pattern was incompatible with `--delete`.

The current design sidesteps the problem entirely: `fct_compile_assets` (see [claude-code-flattening.md](claude-code-flattening.md)) merges the four category subtrees into one compiled scratch directory additively, with `cp -r` and no `--delete`, before the fan-out starts. Then `fct_sync_agent_assets` calls `fct_copy_dir` exactly once per destination — one call per agent home per asset type. No destination receives more than one rsync per apply, so `--delete` is safe at every call site.

## The missing `exact_` prefix on the source

Chezmoi has its own mechanism for "the destination should be exactly the source": the `exact_` prefix on a directory. When a source directory is `exact_foo`, chezmoi removes any entries in the applied target under `foo/` that do not appear in the source. Without the prefix, chezmoi leaves unrelated files in place.

`dot_config/ai_templates/skills/` **does not have the `exact_` prefix**. The directory is simply `dot_config/ai_templates/skills/`. That means:

1. When `chezmoi apply` runs, chezmoi itself will not prune files from `~/.config/ai_templates/skills/` that were removed from the source. If you delete `dot_config/ai_templates/skills/utils/foo/`, the applied path `~/.config/ai_templates/skills/utils/foo/` stays behind until some other mechanism removes it.
2. The render stage uses `chezmoi archive --format tar "$HOME/.config/ai_templates"`. This archives the **applied state**, which includes the stale directory. So the scratch render tree would still contain `utils/foo/`.
3. `fct_compile_assets` reads from the scratch render tree, so it faithfully includes the stale entry in the compile directory.
4. Every agent home's `fct_copy_dir` call copies the compile directory to its destination. Because the call runs with `--delete`, it would prune a file that is in the destination but not in the compile directory — which helps with *new* deletions if they propagated through the render stage, but does not help here, because the deletion did not propagate.

**Reality is messier than that clean story.** Because `exact_` is absent, `~/.config/ai_templates/` accumulates orphaned files over time, and `chezmoi archive` faithfully includes them. The fan-out happily copies the orphans into every agent home. Nothing in the current pipeline removes them.

The simplest fix for the underlying drift would be to rename `dot_config/ai_templates/skills/` to `exact_dot_config/ai_templates/exact_skills/` (and same for `commands/`), so chezmoi prunes the applied copy on every apply. That would also let `chezmoi archive` produce a source-equivalent tree, and the fan-out's orphans would disappear.

This fix is **not applied** by this wiki. Documenting the drift is sufficient for now. Decide and execute in a separate task.

## The `merge` mode that exists but is never used

`fct_copy_dir` supports a non-`delete` sync mode. Passing anything other than `"delete"` as the third argument skips the `--delete --delete-excluded --force` append, which turns the rsync into an additive copy. No call in the current script uses it — every `fct_copy_dir` call from `fct_sync_agent_assets` passes `"delete"` explicitly.

The `merge` mode exists as an opt-in for future work. If a new agent home ever needs additive-only updates (e.g., a target that intentionally accumulates content rather than mirroring the source), the third argument is where to request it. Until that happens, `--delete` is always on for every fan-out call.

## Related

- [[overview]]
- [[render-stage]]
- [[fan-out-targets]]
- [[claude-code-flattening]]
- [[troubleshooting]]
- [[how-to-configure-chezmoi]]
