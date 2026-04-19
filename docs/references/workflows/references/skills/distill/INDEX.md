---
name: distill
description: Apply a named prompt to a local text file via claude, codex, or opencode, writing output to a timestamped run folder
aliases:
  - distill
  - distill-script
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-18
---

# distill

<scope>
Load this wiki when the task involves running, extending, or debugging the `distill` skill under `dot_config/ai_templates/skills/distill/distill/`, or when deciding whether distill is the right tool for a content-processing job.

`distill` is a self-contained Python CLI that takes a local text file, looks up a named prompt in the sibling `distill-prompt` library, runs the prompt against one of three LLM providers (`claude`, `codex`, `opencode`), and writes the distilled output to a timestamped run folder alongside the original input. It exists so that distilling a document is one command, not a workflow. For day-to-day invocation — flag tables, examples, and defaults — read the skill's own `help.md` via `distill.py --help`; this wiki captures the mental model, the design decisions, and the failure modes that do not belong in `--help`.

Source of truth: `dot_config/ai_templates/skills/distill/distill/scripts/distill.py`. The wiki is a narrative layer that points back at that file with specific line numbers. Every claim in the reference pages is grounded in the source so the wiki stays useful as the script evolves.
</scope>

<workflow>
1. Decide what the task actually needs:
   - understanding what distill does and why it exists → [overview.md](references/overview.md)
   - picking a provider, model, or effort level → [providers-and-effort.md](references/providers-and-effort.md)
   - understanding the files written to disk (or why a renamed artifact is missing) → [output-layout.md](references/output-layout.md)
   - adding or resolving a distill prompt → [prompts-library.md](references/prompts-library.md)
   - an invocation is failing and the error is not self-explanatory → [troubleshooting.md](references/troubleshooting.md)

2. Never edit `~/.claude/skills/distill/` or any other agent home copy. The authoritative path is `dot_config/ai_templates/skills/distill/distill/` and everything else is a fan-out target rewritten on every `chezmoi apply`. See [[how-ai-templates-are-distributed]].

3. `distill.py` is a pure CLI — no config file, no hidden state. Everything is either a flag, an input file, or a constant at the top of the source. When behavior surprises you, the answer is almost always in the first 130 lines of the script.
</workflow>

<checklist>
Before finishing any change that touches distill:
- the edit was made under `dot_config/ai_templates/skills/distill/distill/`, not under an agent home
- if a constant changed (defaults, models, effort ETL), `help.md` and this wiki were updated in the same commit
- the test suite under `scripts/tests/test_distill.py` still passes: `uv run --with pytest pytest scripts/tests/test_distill.py -x -q`
- a `--dry-run` invocation still prints the expected plan and artifact names
- if the artifact naming scheme changed, the three downstream docs agree: `help.md`, `SKILL.md`, and `references/from-file/MetaSkill.md`
</checklist>

<references>
Load only what the task needs:
- [overview.md](references/overview.md) — what distill is, why it exists, the three-stage pipeline inside `execute_plan`
- [providers-and-effort.md](references/providers-and-effort.md) — claude, codex, opencode; canonical effort vocabulary; the ETL table; Sonnet special-case; context limits
- [output-layout.md](references/output-layout.md) — run folder name; the three `{slug}_*` artifacts; `meta.yml` schema
- [prompts-library.md](references/prompts-library.md) — how `distill-prompt` feeds distill; stem normalization; how to add a new prompt
- [troubleshooting.md](references/troubleshooting.md) — exit codes, common failures, dry-run as a diagnostic
</references>

---

> Content catalog. Every wiki page is listed here with a one-line summary.
> **Total pages:** 6 | **Last updated:** 2026-04-11

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/doc

| File | Description |
|------|-------------|
| `references/overview.md` | What distill is, why it exists, the three-stage pipeline inside `execute_plan` |
| `references/providers-and-effort.md` | Provider/model matrix, canonical effort vocabulary, ETL table, Sonnet default special-case, per-provider context limits |
| `references/output-layout.md` | Run folder naming, the three slug-prefixed artifacts, full `meta.yml` field schema |
| `references/prompts-library.md` | How `distill-prompt` feeds distill, stem normalization, how to add a prompt |
| `references/troubleshooting.md` | Exit codes, common failures, `--dry-run` as a diagnostic |

## Related

- [[how-ai-templates-are-distributed]] — how the edited source in `dot_config/ai_templates/` lands in `~/.claude/skills/distill/` and every other agent home
- [[how-my-chezmoi-is-configured]] — chezmoi prefix and template conventions this skill lives inside
- [[pa-sdlc]] — the sibling wiki for the `pa-*` lifecycle stages that share distill's parent source directory
