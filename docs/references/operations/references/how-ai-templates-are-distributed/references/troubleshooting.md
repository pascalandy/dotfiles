---
name: Fan-out Troubleshooting
description: How to debug missing, stale, or surprising skills and commands in an agent home after a chezmoi apply
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-18
sources:
  - how-ai-templates-are-distributed
---

Start here when something did not land where you expected it to. Each section describes one symptom and the checks that isolate the cause.

## A new skill is missing from one agent home

Most likely causes, ordered by frequency:

1. **You edited under `~/`, not under `dot_config/ai_templates/`.** Run `chezmoi managed | grep <filename>` — if chezmoi does not know about the file, the edit was never applied. Move the file to the chezmoi source and run `chezmoi apply -v`.
2. **You haven't run `chezmoi apply` since the edit.** The fan-out runs only as part of apply. Editing the source has no effect until the next apply. Run `chezmoi apply -n -v` first to preview.
3. **The target agent home may not receive skills at all.** Verify against [fan-out-targets.md](fan-out-targets.md).
4. **A skill name already exists in another bucket subtree.** Because `fct_compile_assets` flattens `pa-sdlc/`, `devtools/`, `think/`, `knowledge/`, `web/`, `distill/`, `diagram/`, and `media/` into one directory per agent, a new skill named `foo/` in `devtools/` collides with an existing `foo/` in `knowledge/`. The later bucket wins, silently. See [claude-code-flattening.md](claude-code-flattening.md) for the ordering rule and how to check before naming a new skill.

## A skill was renamed but the old name persists in some agent home

If the old name is still present after an apply:

1. Was the rename made in the chezmoi source (`dot_config/ai_templates/skills/...`), or in the applied copy under `~/.config/ai_templates/skills/...`? The rendered tree is archived from the applied path, so a rename that did not propagate to the applied copy will not appear in the fan-out.
2. Did chezmoi actually propagate the rename on this apply? `chezmoi managed | grep <old-name>` should return nothing; `chezmoi status` should show the change as applied.
3. Was the apply interrupted mid-run? The compile step and the sixteen `fct_copy_dir` calls each take non-zero time. An interrupt can leave torn state, especially if it happens after compilation but before all eight agent homes have been synced.
4. If the rename crossed a bucket-subtree boundary (e.g. `devtools/foo/` → `knowledge/foo/`), the source under `~/.config/ai_templates/skills/` may keep both locations until the next apply, because chezmoi does not prune the applied copy of the source without the `exact_` prefix. See [rsync-semantics.md](rsync-semantics.md). The compile stage reads from the applied source, so stale entries there will be re-flattened into every agent home.

## A skill was deleted but still appears somewhere

If the deletion was made in `dot_config/ai_templates/`, ran through `chezmoi apply`, and the file is still visible in an agent home:

1. Check `~/.config/ai_templates/skills/<path>` directly. If it still exists in the applied copy of the source, chezmoi did not prune it — the `exact_` prefix is absent on the source (see [rsync-semantics.md](rsync-semantics.md)). A second `chezmoi apply` does not fix this; only a manual delete of the applied path plus another apply will.
2. If the applied `~/.config/ai_templates/skills/<path>` is already gone but the agent home still has it, the render stage must have succeeded but the rsync call for that target must have failed. Re-run `chezmoi apply -v` and watch the `fct_copy_dir` log lines for that specific target.
3. The agent home may contain manual edits that collide with the deletion. Rsync `--force` allows replacing non-empty directories with files, but a file written directly into the agent home after the last apply would be swept up on the next apply. If it persists across two applies, the fan-out is not reaching that target at all — check for errors in the apply log.

## The apply failed with "Rendered commands directory not found"

This guard at `.chezmoiscripts/run_after_backup.sh:207-210` fires when the render stage produced an empty or misshapen tree. Checklist:

1. Does `dot_config/ai_templates/commands/` still exist in the source? The render stage archives `~/.config/ai_templates`, which chezmoi derives from `dot_config/ai_templates` — if the source subtree was renamed or moved, the render's expected output path no longer exists.
2. Does `~/.config/ai_templates/commands/` exist in the applied copy? The archive reads target state, so a missing applied copy will produce a missing rendered copy.
3. Run the render step manually to inspect the scratch tree:
   ```bash
   t=$(mktemp -d)
   chezmoi archive --format tar "$HOME/.config/ai_templates" | tar -xf - -C "$t"
   /bin/ls "$t/.config/ai_templates/"
   ```
   If `commands/` is missing from the output, the problem is in the render, not the fan-out.

## Everything applies cleanly but an agent CLI does not see a new skill

Not every agent loads skills the same way, even when the file is in the right place. Checks:

1. Is `SKILL.md` present and readable? Claude Code, OpenCode, and most other CLIs load skills by finding a `SKILL.md` in each skill directory. An incomplete directory is skipped silently.
2. Does the agent require a restart to pick up a new skill? Claude Code and OpenCode usually reload on each session, but an already-running session may cache the skill list.
3. Is the skill's frontmatter `name` field unique across the agent's loaded skills? Two skills with the same `name` will collide regardless of directory layout.
4. Does the skill name collide with another bucket subtree? Because `fct_compile_assets` flattens all eight source buckets into one directory per agent, two skills with the same name in `pa-sdlc/`, `devtools/`, `think/`, `knowledge/`, `web/`, `distill/`, `diagram/`, or `media/` will silently overwrite each other in the compile directory. See [claude-code-flattening.md](claude-code-flattening.md).

## Preview without applying

Three one-off commands are useful when debugging the fan-out without running a full `chezmoi apply`:

```bash
# List the rendered commands tree without extracting anything
chezmoi archive --format tar "$HOME/.config/ai_templates" \
  | tar -tf - | grep '^\.config/ai_templates/commands/'

# Same for skills, filtered to a subtree
chezmoi archive --format tar "$HOME/.config/ai_templates" \
  | tar -tf - | grep '^\.config/ai_templates/skills/devtools/'

# Dry-run a single fan-out leg without touching disk
t=$(mktemp -d)
chezmoi archive --format tar "$HOME/.config/ai_templates" | tar -xf - -C "$t"
rsync -avn --delete "$t/.config/ai_templates/skills/" ~/.claude/skills/
```

The third form uses `-n` to tell rsync what it *would* do without doing it. Useful for checking whether a specific file is about to be deleted from an agent home.

## Related

- [[overview]]
- [[render-stage]]
- [[fan-out-targets]]
- [[claude-code-flattening]]
- [[rsync-semantics]]
