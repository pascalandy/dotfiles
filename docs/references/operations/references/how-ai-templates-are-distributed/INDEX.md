---
name: How AI Templates Are Distributed
description: The post-apply fan-out pipeline that renders `dot_config/ai_templates/` through chezmoi and rsyncs commands and skills into every agent home
aliases:
  - ai-templates-fanout
  - fan-out
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# How AI Templates Are Distributed

<scope>
Load this wiki when the task involves anything downstream of `dot_config/ai_templates/`: creating a new skill, renaming a command, debugging why a skill did or did not show up in one agent home, or understanding why editing files directly under `~/.claude/skills/` does not stick.

The pipeline lives in `.chezmoiscripts/run_after_backup.sh` and runs on every `chezmoi apply`. It is a two-stage fan-out:

1. **Render stage** — `chezmoi archive --format tar` resolves templates and chezmoi prefixes, producing an applied-style tree in a `mktemp -d` scratch directory.
2. **Rsync stage** — `fct_copy_dir` mirrors the rendered `commands/` and `skills/` into eight agent homes with `rsync -a --delete`.

Source of truth for every agent's prompts and skills is `dot_config/ai_templates/`. Every other location you see — `~/.claude/skills/`, `~/.config/opencode/skills/`, `~/.pi/agent/skills/`, etc. — is a copy re-derived on every apply.
</scope>

<workflow>
1. Decide what the task actually needs:
   - understanding the pipeline end-to-end → [overview.md](references/overview.md)
   - the render step (template resolution, archive/tar mechanic) → [render-stage.md](references/render-stage.md)
   - which agent home gets what → [fan-out-targets.md](references/fan-out-targets.md)
   - naming a new skill safely → [claude-code-flattening.md](references/claude-code-flattening.md)
   - debugging why a deletion did or did not propagate → [rsync-semantics.md](references/rsync-semantics.md)
   - something is missing from one agent home → [troubleshooting.md](references/troubleshooting.md)

2. Never edit files under an agent home directly. They are overwritten on the next apply. Edit under `dot_config/ai_templates/` and run `chezmoi apply -v`.

3. If a file only exists under one agent home and not in `dot_config/ai_templates/`, it is orphaned — the next apply may or may not remove it depending on the rsync `--delete` semantics. See [rsync-semantics.md](references/rsync-semantics.md).
</workflow>

<checklist>
Before finishing any change that touches `dot_config/ai_templates/`:
- the edit was made under `dot_config/ai_templates/`, not under an agent home
- the new or renamed file does not collide with another skill after compile-stage flattening (`meta/`, `pa-sdlc/`, `specs/`, `utils/` all land as siblings in every agent home's `skills/` directory)
- `chezmoi apply -n -v` was run first and the render step completed successfully
- the expected target under at least one agent home was spot-checked after apply
- if a skill was deleted or moved, every agent home was checked for the old name
</checklist>

<references>
Load only what the task needs:
- [overview.md](references/overview.md) — mental model: source of truth, two-stage pipeline, why it exists
- [render-stage.md](references/render-stage.md) — `fct_render_ai_templates` and the `chezmoi archive --format tar | tar -xf -` mechanic
- [fan-out-targets.md](references/fan-out-targets.md) — the eight agent homes and what each one receives
- [claude-code-flattening.md](references/claude-code-flattening.md) — the compile-stage flattening: how `fct_compile_assets` merges the four category subtrees into one flat directory for every agent, and the residual cross-category name collision risk
- [rsync-semantics.md](references/rsync-semantics.md) — `fct_copy_dir` flags, `--delete` behavior, the interaction with the missing `exact_` prefix
- [troubleshooting.md](references/troubleshooting.md) — what to check when a skill or command does not land where expected
</references>

---

> Content catalog. Every wiki page is listed here with a one-line summary.
> **Total pages:** 7 | **Last updated:** 2026-04-11

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/doc

| File | Description |
|------|-------------|
| `references/overview.md` | Two-stage render + rsync fan-out, source of truth, why this exists |
| `references/render-stage.md` | `chezmoi archive --format tar` into a `mktemp -d` scratch, trap cleanup |
| `references/fan-out-targets.md` | The eight agent homes and their commands/ and skills/ destinations |
| `references/claude-code-flattening.md` | How `fct_compile_assets` flattens the four category subtrees into one directory for every agent home, with the cross-category name collision gotcha |
| `references/rsync-semantics.md` | `fct_copy_dir` rsync flags, `--delete`, the absent `exact_` on the source |
| `references/troubleshooting.md` | How to debug missing or stale skills and commands in an agent home |

## Related

- [[how-to-configure-chezmoi]] — generic chezmoi mechanics, including `chezmoi archive` and the `exact_` prefix
- [[how-my-chezmoi-is-configured]] — the prefixes and templates this repo actually uses
- [[how-vscode-and-brewfile-sync-back]] — the sibling pre-apply sync in the same `.chezmoiscripts/` directory
