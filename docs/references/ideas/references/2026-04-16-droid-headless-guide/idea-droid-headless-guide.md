# Droid Headless Mode Guide

Run Droid non-interactively for automation and CI/CD pipelines.

## docs

https://docs.factory.ai/cli/getting-started/overview

## Basic Command

```bash
droid exec [options] "prompt"
```

## Usage Patterns

| Task | Command |
|------|---------|
| Read-only analysis | `droid exec "analyze codebase"` |
| Safe file edits | `droid exec --auto low "add comments"` |
| Development tasks | `droid exec --auto medium "run tests"` |
| CI/CD deployment | `droid exec --auto high "test, commit, push"` |
| Plan then execute | `droid exec --use-spec --auto medium "implement feature"` |
| Load from file | `droid exec -f prompt.md --auto medium` |
| JSON output | `droid exec -o json "summarize"` |
| Custom model | `droid exec -m "custom:glm5.1-0" "task"` |

## Autonomy Levels

| Level | Allows | Use For |
|-------|--------|---------|
| *(none)* | Read-only operations | Analysis, planning |
| `low` | File edits, formatters | Documentation, comments |
| `medium` | + Package installs, local git, build/test | Development |
| `high` | + Git push, deploy, production | CI/CD |

## Key Flags

| Flag | Purpose |
|------|---------|
| `-m, --model` | Select model (e.g., `glm-5.1`, `custom:glm5.1-0`) |
| `--use-spec` | Plan before executing |
| `--spec-model` | Different model for planning phase |
| `-f, --file` | Load prompt from file |
| `-o, --output-format` | `text` (default), `json`, `stream-json` |
| `--cwd` | Set working directory |
| `-r, --reasoning-effort` | `off`, `low`, `medium`, `high` |

## CI/CD Example

```yaml
- name: Droid Analysis
  env:
    FACTORY_API_KEY: ${{ secrets.FACTORY_API_KEY }}
  run: |
    droid exec -m "custom:glm5.1-0" \
      --use-spec \
      --auto medium \
      -o json \
      "review code and output findings"
```

## Limitations

Headless mode does not support:
- **Missions** — Use `--use-spec` for multi-step work
- **Real-time intervention** — Fire-and-forget only
- **TUI features** — No slash commands or bash mode

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | General error |
| `2` | Invalid arguments |

## Tips

- Start without `--auto` for read-only reconnaissance
- Use `--use-spec` for complex tasks
- Use `--auto low` for safe, minimal changes
- Use `--auto high` only in isolated CI/CD environments
- Never use `--skip-permissions-unsafe` outside disposable containers
- Custom models use `custom:<id>-<index>` format (e.g., `custom:glm5.1-0`)
