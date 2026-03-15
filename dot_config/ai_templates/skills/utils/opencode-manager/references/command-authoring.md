# OpenCode Command Authoring

Use this file when creating or editing slash commands.

## Locations

- Project: `.opencode/command/<name>.md`
- Global: `~/.config/opencode/command/<name>.md`

## Frontmatter

```yaml
---
description: Review changed files
agent: plan
subtask: true
---
```

## Placeholder rules

- Prefer `$ARGUMENTS` unless positional arguments are clearly better.
- Insert each placeholder once.
- Keep user input in a dedicated block.

## Template pattern

```markdown
<summary>
You MUST review the requested scope.
You SHOULD use any provided context.
You MUST return actionable findings.
</summary>

<user_guidelines>
$ARGUMENTS
</user_guidelines>

<objective>
Review the target and report concrete issues.
</objective>
```

## Design rules

- Commands are for users, not agents.
- Use `agent: plan` for analysis-only commands.
- Keep the description short enough to scan in help output.
