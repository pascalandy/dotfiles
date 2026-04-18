---
name: coding-standard
description: Language-agnostic coding disciplines -- CLI design (spec), CLI implementation patterns, and CLI agent-friendly auditing. USE WHEN design CLI, CLI spec, CLI parameters, CLI surface area, command tree, args table, flags table, exit code map, config precedence, build CLI, implement CLI, create CLI, CLI best practices, CLI help text, CLI errors, CLI output, CLI flags, CLI args, CLI subcommands, review CLI UX, CLI code review, audit CLI, agent-friendly CLI, CLI composability, CLI idempotent, CLI retry safe, CLI operability, CLI non-interactive, CLI safety check.
keywords: [cli, cli-spec, cli-design, cli-implementation, cli-audit, agent-friendly, composability, idempotent, retry-safe]
---

# Coding Standard

Language-agnostic coding disciplines: what good design looks like, regardless of implementation language.

## Scope

**In scope:**
- CLI surface-area design (command tree, flags, exit codes, config precedence)
- CLI implementation best practices (I/O, help text, error handling, argument parsing, subcommands, signals, distribution)
- CLI agent-friendly auditing (structured output, idempotency, non-interactive operation, retry safety)

**Out of scope:**
- Language syntax, idioms, tooling, or package managers
- Framework-specific patterns

## Routing

Load `references/ROUTER.md` to dispatch the request to the correct sub-skill.

## Sub-skills

| Sub-skill | Purpose |
|-----------|---------|
| `CliSpec` | Design the CLI surface before implementation. Compact spec: command tree, args/flags table, output rules, exit code map, config precedence, examples. Based on the condensed [clig.dev](https://clig.dev/) rubric. |
| `CliImpl` | Build CLI tools following modern best practices. I/O streams, help text, output formatting, error handling, argument parsing, interactivity, subcommands, robustness, signals, configuration, env vars, naming, distribution. Includes a 100+ item stress-testing checklist. |
| `CliAudit` | Audit CLIs for agent-friendliness, composability, retry safety. All inputs via flags, structured `--json` output, idempotent commands, actionable errors resolvable in one attempt, `--dry-run` and `--force` for safety. |

## Credits

- CLI Guidelines -- [clig.dev](https://clig.dev/) by Aanand Prasad, Ben Firshman, Carl Tashian, Eva Parish
- Agent-friendly requirements -- adapted from [agent-scripts](https://github.com/steipete/agent-scripts) by Peter Steinberger
