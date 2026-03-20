# Pascal Andy's Dotfiles

Personal dotfiles and AI tooling managed with [chezmoi](https://www.chezmoi.io/).

This repository manages classic shell and editor config, local CLI helpers, and a
shared set of AI agent commands, skills, and runtime config. The source of truth
lives in `~/.local/share/chezmoi/` and is applied to `~/` with `chezmoi apply`.

## Why Follow This Repo?

- OpenCode setup
  The OpenCode configuration is one of the main reasons to look around here. It
  is heavily used, well tested, and has had a lot of iteration put into the
  runtime config, prompts, skills, and guardrails.
- Pi experiments
  The Pi setup under `dot_pi/agent/` is another reason to watch the repo. It is
  promising and getting more capable, and the upstream project is
  [Pi Mono](https://github.com/badlogic/pi-mono), but it is not fully solid yet.
- Just-powered workflow
  The [`justfile`](justfile) is a core part of how this repo is operated. If you
  like pragmatic command surfaces, the chezmoi workflow recipes here, especially
  `just cma`, are worth stealing.

## Quick Start

1. Install chezmoi and initialize the repo:

```bash
chezmoi init https://github.com/pascalandy/dotfiles.git
```

2. Create `~/.config/chezmoi/chezmoi.toml` if you want to provide data through
   chezmoi, or make sure the required keyring entries exist if you use the
   default template lookups.

3. Preview the apply, then apply:

```bash
chezmoi apply -n -v
chezmoi apply
```

## Repo Map

### Active surfaces

- `dot_zshrc`, `dot_gitconfig`, `dot_Brewfile`, `dot_local/bin/`
  Core shell, git, package, and local CLI configuration.
- `dot_config/opencode/`
  Live OpenCode runtime config, plugins, and helper tools.
- `dot_config/ai_templates/`
  Shared commands and skills distributed to multiple agent environments.
- `dot_pi/agent/`
  Pi agent configuration, prompts, and keybindings.
- `docs/`
  Planning templates, workflow notes, and durable configuration rationale.

### Archived or reference material

- `dot_config/ai_templates/commands_archives/`
- `dot_config/ai_templates/skills_archived/`
- `bienvenue_chez_moi/`

These areas are useful reference, but they are not the main active runtime
surface.

## Operator Workflow

[`just`](justfile) is the main operator entrypoint for this repo.

Common commands:

```bash
just ci              # gitleaks + shellcheck + shfmt + chezmoi dry-run
just cm-status       # chezmoi drift, excluding run scripts
just cm-diff         # chezmoi diff, excluding run scripts
just cm-apply-dry    # preview an apply
just cm-apply-verbose
```

You can also use raw chezmoi commands directly:

```bash
chezmoi managed
chezmoi edit ~/.zshrc
chezmoi apply -n -v
chezmoi apply -v
```

## Secrets and Template Variables

This repo uses the `keyring` template function by default in templated files
such as `dot_config/opencode/opencode.json.tmpl` and
`private_dot_ssh/config.tmpl`.

If you prefer using `chezmoi.toml` data instead of keyring, replace the
template lookups with `.data` and use this example:

```toml
[data]
# API keys
exa_api_key = "your-exa-api-key"
openrouter_api_key = "sk-or-v1-your-key"
context7_api_key = "your-context7-key"

# SSH config
ssh_host_1 = "your-server-1.example.com"
ssh_host_2 = "your-server-2.example.com"
ssh_user_2 = "your-username"
```

Files containing `{{ .variable }}` must keep the `.tmpl` extension:

```bash
# Wrong
opencode.json

# Correct
opencode.json.tmpl
```

## Apply-Time Side Effects

This repo uses two chezmoi run scripts under `.chezmoiscripts/`:

- `run_before_sync.sh`
  Syncs VS Code settings and keybindings back into the repo and refreshes the
  VS Code extensions list. Brewfile dumping is currently disabled by default.
- `run_after_backup.sh`
  Renders `dot_config/ai_templates/` into target-safe names and syncs shared
  commands and skills out to multiple agent homes such as Claude Code, Codex,
  Amp, Pi, and OpenCode.

`chezmoi apply` is therefore not just a plain file copy in this repo.

## Quality Checks

Local checks are centered around [`just ci`](justfile):

- `gitleaks`
- `shellcheck`
- `shfmt`
- `chezmoi apply -n -v`

Pre-commit hooks are managed by [`lefthook`](lefthook.yml) and run staged
`gitleaks`, `shellcheck`, and `shfmt`. GitHub Actions currently runs those same
three checks in CI.

Install hooks once per machine:

```bash
lefthook install
```

## Managed Config

The repo currently includes:

- shell config such as `.zshrc` and `.p10k.zsh`
- git and SSH config
- VS Code, Ghostty, tmux, bat, fish, amp, zed, and related CLI config
- custom scripts in `~/.local/bin/`
- OpenCode runtime config and plugins
- shared AI agent commands and skills

## Crash Recovery

See [crash_procedure.md](crash_procedure.md) for recovery steps and apply-time
behavior notes.

## Official Docs

https://www.chezmoi.io/user-guide/command-overview/
