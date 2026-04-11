---
name: Render Stage
description: How `fct_render_ai_templates` uses `chezmoi archive --format tar` to produce an applied-style tree in a scratch directory
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-ai-templates-are-distributed
---

Before the rsync fan-out can run, the script needs a tree where chezmoi prefixes are stripped, templates are rendered, and filenames look like applied targets rather than source-tree sources. That transform is the render stage.

## The mechanic

`fct_render_ai_templates` at `.chezmoiscripts/run_after_backup.sh:114`:

```bash
fct_render_ai_templates() {
	local render_root="$1"

	mkdir -p "$render_root"
	log_info "Rendering chezmoi target state for ~/.config/ai_templates"

	chezmoi archive --format tar \
		"$HOME/.config/ai_templates" |
		tar -xf - -C "$render_root"
}
```

Three things are happening:

1. **`chezmoi archive --format tar`** walks the chezmoi source, resolves every source file against its target path, renders `.tmpl` files through Go `text/template`, and writes the result as a tar stream to stdout. Upstream docs call this "archive the target state."
2. **The target argument `"$HOME/.config/ai_templates"`** scopes the archive to only the subtree that corresponds to `dot_config/ai_templates/` in the source. Chezmoi walks only the slice of its source tree that produces files under that target path, so the archive is exactly the AI templates and nothing else.
3. **`tar -xf - -C "$render_root"`** extracts that stream into the scratch directory. After this runs, `$render_root/.config/ai_templates/` contains the fully-rendered tree.

The render root is created by `mktemp -d` in `fct_main` at `.chezmoiscripts/run_after_backup.sh:146`:

```bash
render_root="$(mktemp -d)"
trap 'fct_cleanup "${render_root:-}"' EXIT
```

The `trap` ensures the scratch directory is removed on every exit path — success, error, or signal. `fct_cleanup` at `.chezmoiscripts/run_after_backup.sh:125` is defensive (`if [[ -n "$render_root_path" && -d "$render_root_path" ]]`) so it is safe to trigger early.

## Why target-path, not source-path

`chezmoi archive` can be called with either a source path or a target path. The script uses the target path `~/.config/ai_templates` because that is chezmoi's "canonical" view — the one that resolves all prefixes, templates, and variants. Calling it with the source path would still work, but it would archive the source tree verbatim (including `dot_` prefixes and `.tmpl` extensions) and the rsync fan-out would end up copying unrendered filenames into every agent home.

The applied path is required because this script runs *during* `chezmoi apply` — it runs after `run_before_sync.sh` has completed and, thanks to being a `run_after_*` script, after the apply has already written the live target tree. Passing the target path means "render the same state that was just applied," which is the state that matches the source of truth for this run.

## What the rendered tree looks like

After `fct_render_ai_templates` returns, the script resolves two subpaths at `.chezmoiscripts/run_after_backup.sh:164-165`:

```bash
commands_src="$render_root/.config/ai_templates/commands"
skills_src="$render_root/.config/ai_templates/skills"
```

Both are applied-style trees. `commands_src` is a flat list of command markdown files. `skills_src` contains the four subtrees `meta/`, `pa-sdlc/`, `specs/`, `utils/` as they exist in the source — still separated, because the flattening happens later, during rsync, and only for the Claude Code target. See [fan-out-targets.md](fan-out-targets.md) and [claude-code-flattening.md](claude-code-flattening.md).

## Failure modes

- **Source of truth missing** — the script guards against this before rendering at `.chezmoiscripts/run_after_backup.sh:153` and exits with `log_error "Source of truth not found: $ai_templates_root"` if `dot_config/ai_templates/` is not in the chezmoi source.
- **Rendered subpaths missing** — after the render, the script checks that both `commands_src` and `skills_src` exist at `.chezmoiscripts/run_after_backup.sh:167-174`. If either is missing, it exits. This catches cases where the subtree structure was renamed in the source without updating the script.
- **`chezmoi archive` returns empty** — if the target path argument is wrong (for example, a typo), the tar stream is empty, the extract succeeds, and the subsequent `commands_src` / `skills_src` guards catch the failure. The error message will point at the missing subpath, not at the real cause, so check the target path first when troubleshooting.

## Related

- [[overview]]
- [[fan-out-targets]]
- [[rsync-semantics]]
- [[troubleshooting]]
- [[how-to-configure-chezmoi]]
