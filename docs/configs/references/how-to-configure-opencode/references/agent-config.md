---
name: Agent Config
description: Agent configuration reference for creating and editing custom agents
tags:
  - area/ea
  - kind/doc
  - status/stable
date_created: 2025-04-11
date_updated: 2025-04-11
---

# OpenCode Agent Reference

Use this file when creating or editing custom agents.

## Locations

- Project: `.opencode/agent/<name>.md`
- Global: `~/.config/opencode/agent/<name>.md`

## Frontmatter pattern

```yaml
---
description: |-
  Code review specialist. Use when the user asks for PR review, bug finding, or risk analysis.

  Examples:
  - user: "review this diff" -> inspect changes and report issues
  - user: "find bugs in this PR" -> perform a code review
mode: subagent
model: provider/model-id
permission:
  edit: ask
  bash:
    "*": ask
    "git diff *": allow
  skill:
    "*": deny
    "opencode-manager": allow
---
System prompt body in markdown.
```

## Mode guidance

- Leave `mode` unset for a normal selectable agent.
- Use `subagent` for task-tool specialists.
- Use `primary` only when you intentionally want a main user-facing agent.

## Permission guidance

- Default to standard permissions unless the user requests otherwise.
- Use explicit permission blocks for non-standard access.
- When allowing skills, deny all by default and whitelist only the needed skills.

## Prompt guidance

- State purpose, boundaries, and output shape clearly.
- Give workflow heuristics, not brittle if-else logic.
- Prefer second-person instructions in the body.
