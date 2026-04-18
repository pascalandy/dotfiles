---
name: coding-language
description: Language and framework conventions -- Bash scripting (strict mode, shellcheck, shfmt, fct_ naming), Python development with uv (PEP 723, pyright, ruff, pytest, type hints), and Starlette/ASGI web framework patterns (routing, middleware, WebSocket, templates, auth, uvicorn). USE WHEN bash script, shell script, shellcheck, shfmt, strict mode, fct_ naming, create shell script, refactor shell script, lint shell script, debug shell error, python, uv, PEP 723, pyright, ruff, pytest, python script, python project, type hints, python environment, starlette, ASGI, FastAPI internals, routing, middleware, WebSocket, templates, static files, authentication, background tasks, ASGI server, uvicorn.
keywords: [bash, shell, shellcheck, shfmt, python, uv, pep-723, pyright, ruff, pytest, starlette, asgi, fastapi, middleware, websocket, uvicorn]
---

# Coding Language

Language and framework-specific conventions: idiomatic syntax, tooling, and patterns for each supported stack.

## Scope

**In scope:**
- Bash scripting conventions, strict mode, shellcheck/shfmt, script templates
- Python development with `uv`, PEP 723 inline metadata, pyright, ruff, pytest
- Starlette/ASGI applications (including FastAPI internals): routing, requests/responses, middleware, WebSockets, templates, static files, authentication, sessions, background tasks, lifespan, testing

**Out of scope:**
- CLI design principles, implementation patterns, or agent-friendliness auditing
- General architectural design decisions

## Routing

Load `references/ROUTER.md` to dispatch the request to the correct sub-skill.

## Sub-skills

| Sub-skill | Purpose |
|-----------|---------|
| `Bash` | Create and refactor Bash scripts: `set -Eeuo pipefail`, `fct_` naming, proper quoting, `readonly` constants, `local` variables. Shellcheck wrapper and script template included. |
| `Python` | Modern Python development with `uv` as the exclusive package manager. PEP 723 single-file scripts, type hints with pyright, formatting with ruff, testing with pytest. Covers TDD workflow, exit code standards, security. |
| `Starlette` | Build, debug, and extend Starlette applications and Starlette-powered internals (including FastAPI). Covers routing, requests/responses, middleware, WebSockets, templates, static files, authentication, sessions, background tasks, configuration, lifespan, testing. |

## Credits

- Starlette reference -- audited against [starlette.io](https://www.starlette.io/) official documentation
