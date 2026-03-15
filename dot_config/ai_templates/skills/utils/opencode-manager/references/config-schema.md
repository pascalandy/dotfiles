# OpenCode Config Reference

Use this file when editing `opencode.json`.

## Scope and precedence

- Project config: `./opencode.json`
- Global config: `~/.config/opencode/opencode.json`
- Project config overrides global config
- `AGENTS.md` follows the same project/global split

## Common top-level fields

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "model": "provider/model-id",
  "small_model": "provider/model-id",
  "provider": {},
  "disabled_providers": [],
  "theme": "opencode",
  "autoupdate": true,
  "share": "manual",
  "tools": {},
  "permission": {},
  "agent": {},
  "command": {},
  "instructions": [],
  "mcp": {},
  "formatter": {}
}
```

## Model and provider rules

- Use `provider/model-id` format.
- Prefer checking available models with `opencode models` before hardcoding identifiers.
- Put provider credentials behind environment variables where possible.

## Permissions

Simple form:

```jsonc
{
  "permission": {
    "edit": "ask",
    "webfetch": "allow"
  }
}
```

Pattern-based shell permissions:

```jsonc
{
  "permission": {
    "bash": {
      "*": "ask",
      "git *": "allow",
      "rm *": "ask",
      "sudo *": "deny"
    }
  }
}
```

Skill permissions:

```jsonc
{
  "permission": {
    "skill": {
      "*": "deny",
      "opencode-manager": "allow"
    }
  }
}
```

## Instructions and rules

- Put durable project guidance in `AGENTS.md`.
- Use `instructions` for additional files the model should load automatically.
- Keep `AGENTS.md` concise and specific to the repo's actual workflows.

## Validation

- Re-read the edited file for JSONC mistakes such as missing commas or trailing commas.
- If the `opencode` CLI is installed, run a small smoke check after major config changes.
