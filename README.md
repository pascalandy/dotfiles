# Pascal Andy's Dotfiles

My personal dotfiles managed with [chezmoi](https://www.chezmoi.io/).

## Quick Start

1. Install chezmoi and apply:
```bash
chezmoi init https://github.com/pascalandy/dotfiles.git
chezmoi apply
```

2. Create `~/.config/chezmoi/chezmoi.toml` with your secrets (see below).

3. Re-apply to inject secrets:
```bash
chezmoi apply
```

## Required Template Variables

Create `~/.config/chezmoi/chezmoi.toml` with these variables:

```toml
[data]
# API Keys (required for opencode.json)
exa_api_key = "your-exa-api-key"
openrouter_api_key = "sk-or-v1-your-key"
context7_api_key = "your-context7-key"

# SSH Config (required for ~/.ssh/config)
ssh_host_1 = "your-server-1.example.com"
ssh_host_2 = "your-server-2.example.com"
ssh_user_2 = "your-username"
```

Get your API keys:
- Exa: https://exa.ai/
- OpenRouter: https://openrouter.ai/keys
- Context7: https://context7.com/

## What's Included

- Shell config (`.zshrc`, `.p10k.zsh`)
- Git config (`.gitconfig`)
- SSH config (templated)
- VS Code settings
- CLI tool configs (opencode, amp, zed)
- Custom scripts in `~/.local/bin/`
- AI agent skills and prompts

## Chezmoi Basics

### Add Files

```bash
chezmoi add ~/.file
chezmoi apply
chezmoi cd && git add . && git commit -m "msg" && git push
```

### Templates for Secrets

Files containing `{{ .variable }}` must have the `.tmpl` extension:

```bash
# Wrong - variables won't be processed
opencode.json

# Correct - chezmoi processes templates
opencode.json.tmpl
```

### Run Scripts

- `run_once_*` - Runs only on first apply
- `run_before_*` - Runs before every apply
- `run_after_*` - Runs after every apply

## Crash Recovery

See [crash_procedure.md](crash_procedure.md) for emergency recovery procedures.

## Official Docs

https://www.chezmoi.io/user-guide/command-overview/
