---
name: coding-standards
description: Language and framework coding standards -- CLI design/implementation/auditing, Bash scripting conventions, Python development with uv, and Starlette/ASGI web framework patterns. USE WHEN design CLI, CLI spec, CLI parameters, build CLI, implement CLI, create CLI, CLI best practices, CLI help, CLI errors, CLI output, CLI flags, CLI args, CLI subcommands, audit CLI, agent-friendly CLI, CLI composability, CLI idempotent, CLI retry safe, review CLI UX, CLI code review, bash script, shell script, shellcheck, shfmt, strict mode, create shell script, refactor shell script, lint shell script, python, uv, PEP 723, pyright, ruff, pytest, python script, python project, type hints, starlette, ASGI, FastAPI internals, routing, middleware, WebSocket, templates, static files, authentication, uvicorn.
keywords: [cli, cli-spec, cli-design, cli-implementation, cli-audit, agent-friendly, bash, shell, shellcheck, shfmt, python, uv, pep-723, pyright, ruff, pytest, starlette, asgi, fastapi, middleware, websocket, uvicorn]
---

# Coding Standards

> Six coding disciplines in one unified skill -- from CLI design through Bash scripting, Python development, and Starlette web framework patterns, routed automatically based on what you need.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Coding standards for different languages and frameworks are scattered across separate skills, tribal knowledge, and ad-hoc conventions. Without a single entry point:

- **Wrong guide selected** -- agent applies generic Python advice when Starlette-specific patterns exist, or shell scripting advice when CLI design is the actual need
- **Conventions missed** -- each language has tooling preferences (uv not pip, shellcheck not eyeballing, ruff not black) that get lost when standards live in separate places
- **Domain confusion** -- CLI interface design, CLI implementation, and CLI agent-operability are three distinct disciplines, but they get conflated into one
- **Inconsistent quality** -- Bash scripts skip strict mode, Python scripts skip type hints, Starlette apps skip middleware best practices -- because the right checklist wasn't loaded

The fundamental issue: coding quality is language-specific and framework-specific, but the entry point should be universal.

---

## The Solution

The Coding Standards skill provides six distinct modes, each with its own methodology and reference materials:

### CLI Standards

1. **CliSpec** -- Design CLI surface area before implementation. Produces a compact spec: command tree, args/flags table, output rules, exit code map, config precedence, and example invocations. Language-agnostic. Based on the condensed [clig.dev](https://clig.dev/) rubric.

2. **CliImpl** -- Build CLI tools following modern best practices. Covers I/O streams, help text, output formatting, error handling, argument parsing, interactivity, subcommands, robustness, future-proofing, signals, configuration, environment variables, naming, and distribution. Language-specific guidance for Python, TypeScript/Node, and Bash. Includes a 100+ item stress-testing checklist.

3. **CliAudit** -- Audit CLIs for agent-friendliness, composability, and retry safety. Layers agent-operability requirements on top of the human-first foundation: all inputs via flags, structured `--json` output, idempotent commands, actionable errors that resolve in one attempt, `--dry-run` and `--force` for safety.

### Language & Framework Standards

4. **Bash** -- Create and refactor Bash scripts following strict conventions: `set -Eeuo pipefail`, `fct_` naming, proper quoting, `readonly` constants, `local` variables. Includes a shellcheck linting wrapper and a script template. Two reference docs cover the full convention set and requirements.

5. **Python** -- Modern Python development with `uv` as the exclusive package manager. PEP 723 inline metadata for single-file scripts, type hints with pyright, formatting with ruff, testing with pytest. Covers TDD workflow, exit code standards, security practices, and common pitfalls. Three reference docs for pyright, pytest, and ruff.

6. **Starlette** -- Build, debug, and extend Starlette applications and Starlette-powered internals (including FastAPI). Covers routing, requests/responses, middleware, WebSockets, templates, static files, authentication, sessions, background tasks, configuration, lifespan, and testing. Six reference docs organized by feature area.

The `SKILL.md` loads `references/ROUTER.md`, which routes requests to the right mode based on keyword matching. Each mode has its own `SKILL.md` and supporting reference documents.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Routing table that dispatches to all 6 modes |
| CliSpec skill | `references/CliSpec/SKILL.md` | CLI interface design and spec generation |
| CliSpec references | `references/CliSpec/references/` | Condensed CLI guidelines rubric, source attribution |
| CliImpl skill | `references/CliImpl/SKILL.md` | CLI implementation best practices |
| CliImpl references | `references/CliImpl/references/` | Stress checklist, high-level concepts, full guidelines, index |
| CliAudit skill | `references/CliAudit/SKILL.md` | Agent-friendly CLI requirements and auditing |
| Bash skill | `references/Bash/SKILL.md` | Bash scripting conventions and workflow |
| Bash references | `references/Bash/references/` | Full convention doc (`pref_bash.md`), requirements |
| Bash scripts | `references/Bash/scripts/` | Shellcheck wrapper, script template |
| Python skill | `references/Python/SKILL.md` | Python development with uv, PEP 723, tooling |
| Python references | `references/Python/references/` | pyright, pytest, ruff guides |
| Starlette skill | `references/Starlette/SKILL.md` | Starlette/ASGI framework patterns |
| Starlette references | `references/Starlette/references/` | HTTP, middleware, features, testing, internals, ecosystem |

**Summary:**
- **Coding modes:** 6 (CliSpec, CliImpl, CliAudit, Bash, Python, Starlette)
- **Supporting documents:** 14+ reference files
- **Scripts:** 2 (shellcheck wrapper, bash template)
- **Dependencies:** None (works standalone)

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "design CLI parameters for my deploy tool" | Routes to CliSpec -- produces command tree, flags table, exit codes, examples |
| "write a CLI spec for a config management tool" | Routes to CliSpec -- asks minimal clarifying questions, outputs spec template |
| "build a CLI tool in Python that manages backups" | Routes to CliImpl -- implements with argparse/click/typer, proper I/O, error handling |
| "implement this CLI spec in Bash" | Routes to CliImpl -- translates spec to Bash with shellcheck-clean code |
| "audit this CLI for agent-friendliness" | Routes to CliAudit -- checks inputs, output, errors, idempotency, safety |
| "create a bash script to sync files" | Routes to Bash -- uses template, strict mode, fct_ naming, shellcheck lint |
| "refactor this shell script" | Routes to Bash -- applies conventions from pref_bash.md, runs shellcheck |
| "lint my shell scripts" | Routes to Bash -- runs shellcheck wrapper on target files |
| "create a python script with uv" | Routes to Python -- PEP 723 inline metadata, uv run, type hints |
| "set up pyright for this project" | Routes to Python -- type checking configuration from pyright.md reference |
| "run ruff on this code" | Routes to Python -- linting and formatting via ruff reference |
| "build a starlette API" | Routes to Starlette -- application scaffold, routing, JSON responses |
| "add middleware to my FastAPI app" | Routes to Starlette -- middleware patterns from middleware.md reference |
| "set up WebSocket endpoints" | Routes to Starlette -- WebSocket patterns from features.md reference |
| "write tests for my starlette app" | Routes to Starlette -- TestClient patterns from testing.md reference |

---

## Example Usage

### Designing a CLI Spec

```
User: design CLI parameters for a database migration tool

AI responds:
Running CliSpec...

1. Name: dbmig
2. One-liner: Run and manage database migrations
3. USAGE: dbmig [global flags] <subcommand> [args]
4. Subcommands: up, down, status, create
5. Global flags: -h, --help, --version, --json, -q/--quiet, -v/--verbose
6. Exit codes: 0 success, 1 failure, 2 invalid usage
```

### Creating a Bash Script

```
User: create a bash script to rotate log files

AI responds:
Running Bash...

[Copies script template with set -Eeuo pipefail]
[Implements fct_rotate_logs with proper quoting]
[Adds --dry-run flag, usage header, trap cleanup]
[Runs shellcheck -- 0 warnings]
```

### Python Development

```
User: create a python script that fetches API data

AI responds:
Running Python...

[Creates PEP 723 script with #!/usr/bin/env uv run python3]
[Inline dependencies: httpx, typer, rich]
[Type hints throughout, docstrings with Args/Returns/Raises]
[Exit codes: 0 success, 1 runtime error, 2 validation error]
```

### Starlette Application

```
User: build a starlette API with authentication

AI responds:
Running Starlette...

[Application scaffold with lifespan, typed state]
[Routes with path convertors, class-based endpoints]
[AuthenticationMiddleware with custom backend]
[TestClient tests for authenticated and unauthenticated paths]
```

---

## Configuration

No configuration required.

All six modes work immediately. They reference their own bundled guidelines, checklists, and templates -- no external dependencies, API keys, or persistent state.

---

## Credits

- **CLI Guidelines** -- Based on [clig.dev](https://clig.dev/) by Aanand Prasad, Ben Firshman, Carl Tashian, Eva Parish
- **Agent-friendly requirements** -- Adapted from [agent-scripts](https://github.com/steipete/agent-scripts) by Peter Steinberger
- **Starlette reference** -- Audited against [starlette.io](https://www.starlette.io/) official documentation
