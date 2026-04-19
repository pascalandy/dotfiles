---
name: How My Chezmoi is Configured
description: Personal preferences and opinions about how chezmoi is used in this specific dotfiles repository
aliases:
  - my-chezmoi-config
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - how-to-configure-chezmoi
---

This repo's specific opinions about chezmoi: which prefixes are actually in use, which files are templated today, how the `just` task runner wraps chezmoi commands, which secret backend is chosen, and which guardrails run on every change. For the generic "how does chezmoi work" question, see [[how-to-configure-chezmoi]] instead.

## The #1 rule

**Never edit files under `~/`.** The chezmoi source at `~/.local/share/chezmoi/` is the only place files should be edited. Files under `~/` are applied copies and get overwritten on every `chezmoi apply`.

Before editing any file, check whether it is managed:

```bash
chezmoi managed | grep <filename>
```

If it is managed, either edit under `~/.local/share/chezmoi/` directly, or use:

```bash
chezmoi edit ~/.zshrc
```

which opens the source file and translates the path automatically.

This rule is enforced nowhere but the cost of breaking it is high: your work silently disappears on the next apply. Agents in this repo should treat it as a non-negotiable.

## Prefixes actually in use

Chezmoi supports many prefixes. This repo uses a subset. If a prefix is not in this table, it is not currently used here.

| Prefix | Used here? | Examples in this repo |
|---|---|---|
| `dot_` | yes | `dot_zshrc`, `dot_Brewfile`, `dot_gitconfig`, `dot_p10k.zsh`, `dot_config/`, `dot_local/`, `dot_claude/`, `dot_pi/` |
| `private_` | yes | `private_dot_ssh/`, `private_dot_gnupg/`, `private_Library/` |
| `executable_` | yes | `dot_local/bin/executable_*` (all user scripts), `dot_claude/executable_statusline-command.sh` |
| `symlink_` | yes, one file | `dot_config/iterm2/symlink_AppSupport.tmpl` |
| `.tmpl` | yes | see [Templated files](#templated-files) below |
| `run_before_` | yes | `.chezmoiscripts/run_before_sync.sh` |
| `run_after_` | yes | `.chezmoiscripts/run_after_backup.sh` |
| `readonly_` | not used | — |
| `exact_` | not used | — |
| `run_once_` | not used | — |
| `run_onchange_` | not used | — |

Takeaway: when writing a new source file, almost everything is `dot_*` or `private_dot_*`. User scripts go under `dot_local/bin/executable_*` without the `.sh` extension. Private keys and SSH config live under `private_dot_ssh/`. Run scripts live under `.chezmoiscripts/`.

## Templated files

Every `.tmpl` file active in this repo today:

| Source path | Applied target | Why templated |
|---|---|---|
| `dot_zshenv.tmpl` | `~/.zshenv` | Injects machine-specific env values |
| `dot_config/opencode/opencode.json.tmpl` | `~/.config/opencode/opencode.json` | API keys via `keyring` |
| `private_dot_ssh/config.tmpl` | `~/.ssh/config` | Host aliases + credentials |
| `dot_config/last30days/private_dot_env.tmpl` | `~/.config/last30days/.env` | API keys for the last30days tool |
| `dot_config/util-qobuz-dl/config.ini.tmpl` | `~/.config/util-qobuz-dl/config.ini` | Qobuz credentials |
| `dot_config/iterm2/symlink_AppSupport.tmpl` | `~/iTerm2 Application Support` symlink | Host-dependent path resolution |
| `dot_local/bin/executable_voxtral.tmpl` | `~/.local/bin/voxtral` | Mistral TTS API key injected into the script |
| `dot_pi/agent/extensions/pi-fireworks-provider/index.ts.tmpl` | `~/.pi/agent/extensions/pi-fireworks-provider/index.ts` | Fireworks API key |

When adding a new secret, use one of these templated files as a reference. The pattern is always: `.tmpl` suffix, `private_` prefix if appropriate, `keyring` function call for the value.

## Secrets backend: keyring (macOS Keychain)

This repo uses `keyring` as the primary secret backend. The `chezmoi.toml` `.data` fallback pattern is documented in [[how-to-configure-chezmoi]] → `secrets.md` but is not the default here.

To add a new secret:

```bash
chezmoi secret keyring set --service=<name> --user=<key>
# paste value at prompt
```

Then reference it in a `.tmpl` file:

```bash
"<key>": "{{ keyring "<name>" "<key>" }}"
```

Apply and spot-check the rendered copy:

```bash
chezmoi apply -v
chezmoi cat ~/.config/example/config.json
```

## `just` is the task runner

This repo uses [`just`](https://github.com/casey/just) as its main operator entry point. All chezmoi commands are wrapped in `just cm-*` recipes so routine operations have a short, typo-proof alias. The full `justfile` lives at the repo root.

### chezmoi recipes

| Recipe | Underlying command | When to use |
|---|---|---|
| `just cm-status` | `chezmoi status -x scripts` | Show real drift between source and target. Excludes run scripts on purpose (they always show `R`). |
| `just cm-diff` | `chezmoi diff -x scripts` | Diff source vs target, excluding run-script noise. |
| `just cma` | `chezmoi apply` | Apply. The most common recipe. |
| `just cm-apply-verbose` | `chezmoi apply -v` | Apply with output. Use when you want to see every file touched. |
| `just cm-apply-dry` | `chezmoi apply -n -v` | Dry run. Use before every real apply if you are not sure. |
| `just cm-managed` | `chezmoi managed` | List every managed file. |
| `just cm-quick-check` | `git status -sb` + `chezmoi status -x scripts` | Pre-commit sanity check. |
| `just cm-audit` | `git status` + `chezmoi status` + `chezmoi diff` | Full inspection, no changes. |
| `just cm-add <path>` | `chezmoi add <path>` | Start managing an existing file in `~/`. |
| `just cm-edit <path>` | `chezmoi edit <path>` | Edit a managed file's source. |

### Quality recipe

| Recipe | Runs |
|---|---|
| `just ci` | `gitleaks` + `shellcheck` + `shfmt` + `test-all` (four pytest suites) + `chezmoi apply -n -v` |

`just ci` is the "before I commit" check. It is the same surface as the GitHub Actions pipeline plus a dry-run apply.

For the full `justfile` surface beyond chezmoi recipes, see the dedicated justfile wiki (planned under `operations/`).

## Apply has side effects in this repo

`chezmoi apply` is not a plain file copy here. Two run scripts fire around the copy phase:

1. `.chezmoiscripts/run_before_sync.sh` — pulls VS Code settings and extensions back into the source tree before the copy. Brewfile dumping is currently disabled by default.
2. `.chezmoiscripts/run_after_backup.sh` — renders `dot_config/ai_templates/` via `chezmoi archive` and rsyncs `commands/` and `skills/` out to every agent home (`~/.claude/`, `~/.config/opencode/`, `~/.pi/agent/`, `~/.codex/`, `~/.gemini/`, `~/.config/amp/`, `~/.config/agents/`, `~/.factory/`).

**Implication:** an apply in this repo is expected to be chatty and slightly slow. Seeing `R` status on the scripts is not drift. Editing a skill under `dot_config/ai_templates/skills/` affects eight agent homes at once on the next apply.

A dedicated wiki covering the fan-out mechanism end-to-end is planned under `operations/references/how-ai-templates-are-distributed/`. Until that exists, read `.chezmoiscripts/run_after_backup.sh` directly if the details matter.

## Quality guardrails

Three tools run on every change, in three places:

| Tool | Pre-commit (`lefthook`) | Local `just ci` | GitHub Actions |
|---|---|---|---|
| `gitleaks` | staged files | full repo | full repo |
| `shellcheck` | staged `.sh` files | all tracked `.sh` | all tracked `.sh` |
| `shfmt` | staged `.sh` files | all tracked `.sh` | all tracked `.sh` |
| pytest suites (transcript, banana, map-fs, tavily) | — | all four | — |
| `chezmoi apply -n -v` | — | yes | — |

Install the pre-commit hooks once per machine:

```bash
lefthook install
```

Then every `git commit` runs staged-file checks automatically. Skipping hooks with `--no-verify` is off-limits in this repo.

## Common mistakes in this repo specifically

- **Editing `~/.config/opencode/opencode.json`.** It is a rendered copy of `dot_config/opencode/opencode.json.tmpl`. The next apply wipes your change. Edit the `.tmpl` instead.
- **Editing a shared AI skill in `~/.config/opencode/skills/`.** Same problem — that tree is fan-out output from `dot_config/ai_templates/skills/`. Edit the source under `ai_templates/`.
- **Creating a script with a `.sh` extension in `dot_local/bin/`.** The convention here is no `.sh` extension for cleaner CLI usage (`passgen`, not `passgen.sh`).
- **Adding `{{ }}` to a file without the `.tmpl` suffix.** The braces land literally in the applied copy. Always rename to `.tmpl` when introducing a placeholder.
- **Running `chezmoi apply` without a dry-run first.** The fan-out side effects make this costly to undo. Always `just cm-apply-dry` first if you are not certain.

## Related

- [[how-to-configure-chezmoi]]
- [[how-to-configure-opencode]]
- [[how-my-zshrc-is-configured]]
