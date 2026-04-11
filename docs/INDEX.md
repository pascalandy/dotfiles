---
name: Dotfiles Docs
description: Root catalog for the chezmoi dotfiles documentation
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
---

# Dotfiles Docs

> Root catalog for the chezmoi dotfiles repository. Every documentation category is listed here.
> Agents landing in `/docs` should read this file first, then route to the category they need.
> **Categories:** 3 | **Last updated:** 2026-04-11
>
> **Child indexes:** [[configs/INDEX.md]] · [[workflows/INDEX.md]] · [[operations/INDEX.md]]

<scope>
This index orients agents and returning humans inside `~/.local/share/chezmoi/docs/`.

Source of truth: `~/.local/share/chezmoi/docs/`. Nothing in the applied home directory mirrors this tree — documentation is repo-local.

Use this index to pick the right category for a task. Do not treat it as a place to store content; each category has its own `INDEX.md` and `references/`.
</scope>

<workflow>
1. Identify the task type:
   - editing or understanding a specific config file or tool → `configs/`
   - following or refining a workflow or methodology (`pa-*`) → `workflows/` _(planned)_
   - running, testing, or operating the repo itself → `operations/` _(planned)_

2. Open the matching category `INDEX.md`. Do not read every wiki in the category — read the category index first and route from there. Every category index back-links here via its own header, so traversal is bidirectional.

3. For vocabulary questions (`pa-*`, agent homes, source vs applied, fan-out, chezmoi prefixes) read the [Glossary](#glossary) section below.

4. If you are about to write a new doc, decide up front whether it is a **generic guide** or a **personal-preferences** doc. See [Two Kinds of "How" Pages](#two-kinds-of-how-pages). Do not mix the two in the same file.
</workflow>

<checklist>
Before writing or editing any doc under `/docs`:
- it belongs in one of the three categories below, not loose at the root
- it matches the wiki-map house style (frontmatter + `INDEX.md` + `references/` + `LOG.md`)
- kebab-case filenames and Obsidian-style `[[wikilinks]]`
- `area/ea`, `kind/*`, `status/open`, `date_created`, `date_updated` in frontmatter
- generic-vs-personal distinction is respected (see below)
- the corresponding category `INDEX.md` and its `LOG.md` are updated in the same change
</checklist>

## How This Doc Tree Is Organized

Three top-level categories plus a personal brainstorm area.

| Category | Purpose | Status |
|---|---|---|
| `configs/` | How individual files, tools, and configs are set up | active |
| `workflows/` | How processes and methodologies work (e.g. `pa-sdlc`) | active |
| `operations/` | How the repo itself runs (chezmoi apply, fan-out, pre-apply sync) | active |
| `ideas/` | Personal brainstorms. Not indexed. Agents should not read unless explicitly asked. | excluded |

Each active category has its own `INDEX.md` at its root, a `references/` subdirectory for wiki pages, and an append-only `references/LOG.md`.

## Two Kinds of "How" Pages

This repo deliberately separates two kinds of documentation that look similar but serve different purposes. Do not mix them in the same file.

| Kind | File name pattern | Answers | Reusable by others? |
|---|---|---|---|
| **Generic guide** | `how-to-configure-X/` | How does X work in general? What are the options, schema, and commands? | Yes — anyone using the same tool. |
| **Personal preferences** | `how-my-X-is-configured/` | How is X set up on this operator's machine? Which providers, which opinions, which trade-offs? | No — this is one person's choices. |

Today the split is visible in `configs/references/`:

- Generic: [`how-to-configure-opencode/`](configs/references/how-to-configure-opencode/INDEX.md)
- Personal: `how-my-opencode-is-configured.md` and [`how-my-zshrc-is-configured/`](configs/references/how-my-zshrc-is-configured/INDEX.md)

When writing a new doc, ask: *could this page be reused by a stranger with the same tool, or is it only true for this machine?* That answer picks the kind.

## Archives

The repo parks retired skills, commands, and templates in archive directories so they stay in git history without being loaded by the runtime. Archives are **excluded from the `ai_templates/` fan-out** (see `.chezmoiscripts/run_after_backup.sh`), so nothing in them reaches any agent home.

Known archive locations:

- `dot_config/archived_ai_templates/`
- `dot_config/ai_templates/archived_commands/`
- `bienvenue_chez_moi/`

Agents should ignore archives unless the task explicitly asks to revisit one.

## Glossary

One-line definitions for recurring vocabulary in this repo. Promote to `glossary.md` once this section exceeds ~30 terms.

### Repository shape

- **chezmoi source** — the tree under `~/.local/share/chezmoi/`. The only place files should be edited.
- **applied target** — the tree under `~/`. Files here are copies overwritten on every `chezmoi apply`.
- **source vs applied** — shorthand for the distinction above. Most mistakes in this repo come from editing applied files instead of source files.
- **`dot_` / `private_` / `executable_` / `symlink_` / `readonly_` / `exact_` / `.tmpl` / `run_before_` / `run_after_` / `run_once_` / `run_onchange_`** — chezmoi filename prefixes and suffixes. Full table in [[how-to-configure-chezmoi]] → `naming-conventions.md`. For which prefixes this repo actually uses, see [[how-my-chezmoi-is-configured]].
- **`keyring`** — chezmoi template function that reads a secret from the OS keyring (macOS Keychain on this machine). Called inside `.tmpl` files as `{{ keyring "service" "user" }}`. See [[how-to-configure-chezmoi]] → `secrets.md`.
- **`chezmoi.toml`** — chezmoi's config file, at `~/.config/chezmoi/chezmoi.toml`. Its `[data]` table exposes custom variables to templates as `.my_var`.
- **fan-out** — the process in `.chezmoiscripts/run_after_backup.sh` that renders `dot_config/ai_templates/` with `chezmoi archive` and rsyncs `commands/` and `skills/` into every agent home.
- **agent home** — a per-agent runtime config directory. Current targets of the fan-out: `~/.claude/`, `~/.config/opencode/`, `~/.pi/agent/`, `~/.codex/`, `~/.gemini/`, `~/.config/amp/`, `~/.config/agents/`, `~/.factory/`.
- **Claude Code flattening** — `~/.claude/skills/` receives `meta/`, `pa-sdlc/`, `specs/`, and `utils/` merged into one directory, while other agent homes keep the four-way split. A gotcha when naming skills.

### Workflow family (`pa-sdlc`)

- **pa-sdlc** — "Pascal Andy Software Development Lifecycle". A workflow of skills under `dot_config/ai_templates/skills/pa-sdlc/`.
- **pa-scout** — discovery / onboarding. "What is this and where should I look?"
- **pa-scope** — factual record of the current codebase for a given task, no opinions.
- **pa-vision** — where the work is going (design intent, end state, trade-offs).
- **pa-architect** — how the work gets there (signatures, phases, vertical slices).
- **pa-implement** — applying the change.
- **pa-doc-update** — documenting a concrete change, decision, or artifact.
- **pa-doc-cleaner** — refreshing, deduplicating, repairing existing docs.
- **pa-advisor** — advisory / second-opinion skill.

### Tools and agents

- **opencode** — AI coding agent. Config: `dot_config/opencode/`.
- **pi** — Pi Mono agent ([pi-mono](https://github.com/badlogic/pi-mono)). Config: `dot_pi/`.
- **claude** — Claude Code. Config: `dot_claude/` plus the fan-out target `~/.claude/`.
- **codex** — OpenAI Codex CLI. Fan-out target: `~/.codex/`.
- **gemini** — Google Gemini CLI. Fan-out target: `~/.gemini/`.
- **amp** — Amp agent. Fan-out target: `~/.config/amp/`.
- **factory** — Factory agent. Fan-out target: `~/.factory/`.
- **qmd** — tool referenced in `just uca` maintenance recipes.
- **brv / byterover** — knowledge/context tool storing state under `.brv/`.

### Document kinds

- **wiki-map** — the skill and schema defining the `INDEX.md` + `references/` + `LOG.md` pattern used throughout `/docs`. Source: `dot_config/ai_templates/skills/pa-sdlc/wiki-map/`.
- **generic guide** — `how-to-configure-X` page documenting a tool in general terms.
- **personal preferences** — `how-my-X-is-configured` page documenting this operator's specific choices.

---

> Content catalog. Every top-level documentation entry is listed here with a one-line summary.
> **Total entries:** 3 | **Last updated:** 2026-04-11

## Wiki Map

### kind/wiki

| File | Description |
|------|-------------|
| [`configs/INDEX.md`](configs/INDEX.md) | How individual files, tools, and configs are set up |
| [`workflows/INDEX.md`](workflows/INDEX.md) | How processes and methodologies work (`pa-sdlc`) |
| [`operations/INDEX.md`](operations/INDEX.md) | How the repo itself runs — post-apply fan-out, pre-apply sync-back |
