---
name: cli-guidelines
description: Design CLI parameters and UX, build CLI tools following best practices, and audit CLIs for agent-friendliness and composability. USE WHEN design CLI, CLI spec, CLI parameters, build CLI, implement CLI, create CLI, CLI best practices, CLI help, CLI errors, CLI output, CLI flags, CLI args, CLI subcommands, audit CLI, agent-friendly CLI, CLI composability, CLI pipeline, CLI idempotent, CLI retry safe, review CLI UX, CLI code review.
keywords: [cli, command-line, cli-spec, cli-design, cli-implementation, cli-audit, agent-friendly, composability, flags, args, subcommands, help-text, exit-codes, config-precedence, idempotent, dry-run, json-output]
---

# CLI Guidelines

> Three CLI disciplines in one unified skill -- from interface design through implementation to agent-operability auditing, routed automatically based on what you need.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Building a CLI that works for humans, scripts, and AI agents requires three distinct disciplines. A CLI spec defines the interface contract (command tree, flags, output modes, exit codes). Implementation translates that contract into working code with proper I/O streams, error handling, and language-specific conventions. Agent-operability auditing ensures the tool doesn't hang on missing input, produces structured output, and behaves safely on retries. These disciplines are usually scattered across different guides, checklists, and tribal knowledge:

- **Designing without building** -- you want a spec but get implementation advice
- **Building without a spec** -- you jump to code but miss interface consistency
- **Missing the agent layer** -- the CLI works for humans but breaks under automation (hangs on prompts, non-idempotent, vague errors cause retry loops)
- **Applying the wrong checklist** -- reviewing implementation quality when the interface design is the problem, or vice versa

The fundamental issue: CLI quality has three stages (spec, build, audit), each with its own methodology, and mixing them produces mediocre results at every stage.

---

## The Solution

The CLI Guidelines skill provides three distinct modes, each with its own methodology and reference materials:

1. **CliSpec** -- Design CLI surface area before implementation. Produces a compact spec: command tree, args/flags table, output rules, exit code map, config precedence, and example invocations. Language-agnostic. Based on the condensed [clig.dev](https://clig.dev/) rubric.

2. **CliImpl** -- Build CLI tools following modern best practices. Covers I/O streams, help text, output formatting, error handling, argument parsing, interactivity, subcommands, robustness, future-proofing, signals, configuration, environment variables, naming, and distribution. Language-specific guidance for Python, TypeScript/Node, and Bash. Includes a 100+ item stress-testing checklist.

3. **CliAudit** -- Audit CLIs for agent-friendliness, composability, and retry safety. Layers agent-operability requirements on top of the human-first foundation: all inputs via flags, structured `--json` output, idempotent commands, actionable errors that resolve in one attempt, `--dry-run` and `--force` for safety.

The collection `SKILL.md` loads `references/ROUTER.md`, which routes requests to the right mode based on keyword matching. Each mode has its own `SKILL.md` and supporting reference documents.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Routing table that dispatches to CLI modes |
| CliSpec skill | `references/CliSpec/SKILL.md` | CLI interface design and spec generation |
| CliSpec references | `references/CliSpec/references/` | Condensed CLI guidelines rubric, source attribution |
| CliImpl skill | `references/CliImpl/SKILL.md` | CLI implementation best practices |
| CliImpl references | `references/CliImpl/references/` | Stress checklist, high-level concepts, full guidelines, index |
| CliAudit skill | `references/CliAudit/SKILL.md` | Agent-friendly CLI requirements and auditing |

**Summary:**
- **CLI modes:** 3 (CliSpec, CliImpl, CliAudit)
- **Supporting documents:** 6 reference files (guidelines, checklist, concepts, full guide, index, source)
- **Dependencies:** None (works standalone)

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "design CLI parameters for my deploy tool" | Routes to CliSpec -- produces command tree, flags table, exit codes, examples |
| "write a CLI spec for a config management tool" | Routes to CliSpec -- asks minimal clarifying questions, outputs spec template |
| "build a CLI tool in Python that manages backups" | Routes to CliImpl -- implements with argparse/click/typer, proper I/O, error handling |
| "implement this CLI spec in Bash" | Routes to CliImpl -- translates spec to Bash with shellcheck-clean code |
| "review the CLI UX of this script" | Routes to CliImpl -- evaluates against best practices checklist |
| "add flags and help text to this script" | Routes to CliImpl -- adds argument parsing, help, examples |
| "audit this CLI for agent-friendliness" | Routes to CliAudit -- checks inputs, output, errors, idempotency, safety |
| "make this script work in CI pipelines" | Routes to CliAudit -- ensures non-interactive, structured output, proper exit codes |
| "check if this tool is safe for automated retries" | Routes to CliAudit -- validates idempotency, error specificity, --dry-run support |

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
6. I/O: stdout for results/status; stderr for progress/errors
7. Exit codes: 0 success, 1 failure, 2 invalid usage
8. Config: DBMIG_DATABASE_URL env, .dbmig.yml project config
9. Examples: dbmig up, dbmig down --steps 2, dbmig status --json
```

### Implementing a CLI

```
User: build a CLI in Python that converts CSV to JSON

AI responds:
Running CliImpl...

[Produces working Python code using argparse]
[stdin/stdout separation, --json output, --quiet flag]
[TTY detection, proper error handling, exit codes]
[Handles Ctrl-C cleanly, no tracebacks for expected errors]
```

### Auditing for Agent-Friendliness

```
User: audit this deploy script for agent use

AI responds:
Running CliAudit...

Input Handling:
  FAIL: --env flag missing, requires interactive prompt
  FIX: Add --env flag; skip prompt when provided

Output:
  PASS: stdout/stderr separated
  FAIL: No --json flag
  FIX: Add --json that emits {"status":"ok","deploy_id":"..."}

Safety:
  FAIL: Not idempotent (errors on re-deploy)
  FIX: Check current state first, return exit 0 with no-op message
```

---

## Configuration

No configuration required.

All three modes work immediately. They reference their own bundled guidelines and checklists -- no external dependencies, API keys, or persistent state.

---

## Credits

- **CLI Guidelines** -- Based on [clig.dev](https://clig.dev/) by Aanand Prasad, Ben Firshman, Carl Tashian, Eva Parish
- **Agent-friendly requirements** -- Adapted from [agent-scripts](https://github.com/steipete/agent-scripts) by Peter Steinberger
