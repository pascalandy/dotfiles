# Getting Started

Use this file when the task is about configuring or using OpenCode.

## Core setup flow

1. Install OpenCode.
2. Configure a provider.
3. Open a project.
4. Run `/init` to create `AGENTS.md`.
5. Start with read-only planning before making changes.

## Primary files

- Project config: `./opencode.json`
- Global config: `~/.config/opencode/opencode.json`
- Project instructions: `./AGENTS.md`
- Global instructions: `~/.config/opencode/AGENTS.md`

## Chezmoi-managed dotfiles

If these OpenCode files are managed by chezmoi:

- edit the chezmoi source, not the rendered file in `$HOME`
- never edit the home-directory target directly
- apply the change with `just cma`

In this repo, the chezmoi source is the source of truth.

## Configuration topics

- model and provider selection
- permissions
- instruction files
- agents and commands declared in config
- environment-backed secrets

For field-level details, load [config-schema.md](config-schema.md).

## Everyday usage

- Use `@` to reference files.
- Use plan mode first when the task is ambiguous or risky.
- Use `/init` when a project has no OpenCode instructions yet.
- Prefer the least invasive command that proves a config or workflow works.
- If the config lives in chezmoi, update the source and then run `just cma`.
