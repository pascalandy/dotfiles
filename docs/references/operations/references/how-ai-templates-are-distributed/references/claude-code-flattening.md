---
name: Skill Flattening
description: How `fct_compile_assets` merges the eight source subtrees into one flat skills directory that every agent home receives
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-18
sources:
  - how-ai-templates-are-distributed
---

The source tree under `dot_config/ai_templates/skills/` is organized into eight workflow-arc subtrees: `pa-sdlc/`, `devtools/`, `think/`, `knowledge/`, `web/`, `distill/`, `diagram/`, and `media/`. Every skill lives in exactly one of those eight buckets. The fan-out script flattens them into a single peer-level directory before handing the result to rsync, so every agent home receives a flat `skills/` tree with all eight buckets merged into one level. The bucket structure exists only in the source; it is source-side metadata, not runtime structure.

This page was originally written for a Claude-Code-only flattening gotcha. The script now flattens uniformly for every agent, so the old gotcha is gone. The page name is kept for back-compat with existing links.

## The compile step

`fct_compile_assets` at `.chezmoiscripts/run_after_backup.sh:75-104`:

```bash
fct_compile_assets() {
	local src_dir="$1"
	local compile_dir="$2"
	local -a categories=(pa-sdlc devtools think knowledge web distill diagram media)

	mkdir -p "$compile_dir"

	# If src has subdirectories (categories), compile them
	# If src is flat, copy everything directly
	local has_categories=false
	local category
	for category in "${categories[@]}"; do
		if [[ -d "$src_dir/$category" ]]; then
			has_categories=true
			break
		fi
	done

	if [[ "$has_categories" == true ]]; then
		for category in "${categories[@]}"; do
			if [[ -d "$src_dir/$category" ]]; then
				cp -r "$src_dir/$category/"* "$compile_dir/" 2>/dev/null || true
			fi
		done
	else
		cp -r "$src_dir/"* "$compile_dir/" 2>/dev/null || true
	fi
}
```

The function takes a rendered source directory and a fresh compile directory (both `mktemp -d` scratch paths) and produces a flat tree:

1. **Detection.** It checks for any of the eight known bucket subdirectories. If at least one exists, it treats the input as categorized.
2. **Categorized path.** It loops over the eight buckets in a fixed order (`pa-sdlc` → `devtools` → `think` → `knowledge` → `web` → `distill` → `diagram` → `media`) and does `cp -r` for each one that exists, copying the *contents* of the bucket directory into the compile root. `cp` is additive — no `--delete` — so each call adds to the compile directory rather than overwriting it.
3. **Flat path.** If none of the eight bucket directories exist, it treats the input as already flat and just copies everything across. This is how the `commands/` input is handled: commands do not use bucket subtrees, so the flat branch applies.
4. **Silent collisions.** The `2>/dev/null || true` suffix swallows errors. A cross-subtree filename collision (two buckets containing the same skill directory name) is resolved silently by "later write wins", since `cp -r` on macOS will overwrite without complaint when it can and silently fail when it cannot.

The compile function is called twice per apply — once for commands, once for skills — in `fct_sync_agent_assets` at `.chezmoiscripts/run_after_backup.sh:113-116`:

```bash
compiled_commands_dir="$(mktemp -d)"
compiled_skills_dir="$(mktemp -d)"
fct_compile_assets "$commands_src" "$compiled_commands_dir"
fct_compile_assets "$skills_src" "$compiled_skills_dir"
```

After these two calls, `$compiled_skills_dir` contains every skill from every bucket as a direct child, and `$compiled_commands_dir` contains every command as a direct child.

## The single rsync per agent

With the compile step done, each agent home receives exactly two rsync calls (one for commands, one for skills), both sourcing from the compiled scratch directories. From `.chezmoiscripts/run_after_backup.sh:118-148`:

```bash
fct_copy_dir "$compiled_commands_dir" "$HOME/.config/opencode/commands" "delete"
fct_copy_dir "$compiled_skills_dir"   "$HOME/.config/opencode/skills"   "delete"
# ... same pattern for Pi, Claude Code, Codex, Gemini, Amp, Agents, Factory ...
```

This is a fundamental shift from the pre-`b6d0042` design. The key consequences:

1. **The shared-destination `--delete` bug is gone.** Earlier, Claude Code got four separate `fct_copy_dir` calls all targeting `~/.claude/skills/`, and each call's `--delete` wiped the previous call's output. The new design calls `fct_copy_dir` exactly once per destination per asset type. No call overwrites another's work.
2. **The flattening applies uniformly.** Every agent home now receives the same compiled skills directory, so OpenCode, Pi, Claude Code, Codex, Gemini, Amp, Agents, and Factory all see the same flat layout. The source-tree category split is visible only in `dot_config/ai_templates/skills/` itself; it is invisible to every downstream agent.
3. **Gemini now receives skills.** The old design's `fct_sync_agent_assets` had no `skills_src` call for Gemini (it was commands-only). The new design gives Gemini the same compiled skills directory every other agent gets. If a new agent CLI starts ignoring the directory later, that will be a per-agent decision about whether to load skills, not a fan-out decision.
4. **Cleanup is explicit.** `fct_sync_agent_assets` ends with `rm -rf "$compiled_commands_dir" "$compiled_skills_dir"` at `.chezmoiscripts/run_after_backup.sh:151`, removing both scratch directories after the fan-out completes. The render-stage scratch directory is still cleaned up by the `trap` in `fct_main`.

## Cross-subtree name collisions

The compile step has one remaining trap: if two bucket subtrees contain a skill with the same directory name, the later bucket (in `pa-sdlc` → `devtools` → `think` → `knowledge` → `web` → `distill` → `diagram` → `media` order) wins, silently. `cp -r` on macOS does not warn on overwrite, and the `|| true` suffix suppresses errors.

Examples that would collide:

| `dot_config/ai_templates/skills/devtools/foo/` | `dot_config/ai_templates/skills/knowledge/foo/` | Result in compile dir |
|---|---|---|
| exists | exists | `foo/` = `knowledge/foo/` contents (later bucket wins) |
| exists | does not exist | `foo/` = `devtools/foo/` contents |
| does not exist | exists | `foo/` = `knowledge/foo/` contents |

The collision is source-side, not per-agent: every agent home receives the same collided result, because every agent home is fed from the same compiled directory. This is a different collision shape from the pre-`b6d0042` design, where only Claude Code suffered from the collision and every other agent kept the two skills in separate subtrees.

**What to check before naming a new skill:**

```bash
ls ~/.local/share/chezmoi/dot_config/ai_templates/skills/pa-sdlc/ \
   ~/.local/share/chezmoi/dot_config/ai_templates/skills/devtools/ \
   ~/.local/share/chezmoi/dot_config/ai_templates/skills/think/ \
   ~/.local/share/chezmoi/dot_config/ai_templates/skills/knowledge/ \
   ~/.local/share/chezmoi/dot_config/ai_templates/skills/web/ \
   ~/.local/share/chezmoi/dot_config/ai_templates/skills/distill/ \
   ~/.local/share/chezmoi/dot_config/ai_templates/skills/diagram/ \
   ~/.local/share/chezmoi/dot_config/ai_templates/skills/media/
```

If the name already exists under any of the eight buckets, pick a different one. The old advice "every other agent keeps the category split, so you are safe except for Claude Code" no longer applies.

## Historical note — the pre-`b6d0042` bug

Before the refactor in commit `b6d0042` (2026-04-11), `fct_sync_agent_assets` contained four separate `fct_copy_dir` calls targeting `~/.claude/skills/`, one per category, each with `sync_mode=delete`. Because `rsync --delete` removes destination files that are not in the current source, and all four calls shared the same destination, each call wiped the previous one's output. Only the last call (`utils/`) survived a full apply.

The symptom was that every `meta/`, `pa-sdlc/`, and `specs/` skill was invisible to Claude Code after a `chezmoi apply`, while every other agent home (which handled the four subtrees separately, without flattening) showed all the skills correctly. Verified on 2026-04-11 by `diff <(ls ~/.claude/skills/) <(ls .../skills/utils/)` — the diff was empty, confirming `~/.claude/skills/` held nothing but `utils/` contents.

The `b6d0042` refactor replaced the four-call pattern with the compile-then-single-rsync design documented above. The bug is gone; the flattening is now uniform; the collision trap is the only residual hazard.

## Related

- [[overview]]
- [[fan-out-targets]]
- [[rsync-semantics]]
- [[troubleshooting]]
