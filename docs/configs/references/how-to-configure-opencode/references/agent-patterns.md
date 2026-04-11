---
name: Agent Patterns
description: Agent prompt patterns for structuring agent markdown bodies
tags:
  - area/ea
  - kind/doc
  - status/stable
date_created: 2025-04-11
date_updated: 2025-04-11
---

# Agent Prompt Patterns

Use this file to shape an agent's markdown body.

## Recommended structure

```markdown
# Role and Objective
[What the agent does and what it should avoid]

# Instructions
- Core rules
- Safety and permission expectations

# Workflow
1. Gather context
2. Analyze or act
3. Verify

# Output Format
[How the result should be presented]
```

## Description guidance

- The `description` is the trigger surface.
- Keep it concrete: action, triggers, and examples.
- Avoid vague descriptions such as `Helpful OpenCode agent`.

## Good trigger pattern

```yaml
description: |-
  Repository audit specialist. Use when the user asks to validate OpenCode agents, commands, or skills.

  Examples:
  - user: "check my OpenCode setup" -> audit repository metadata
  - user: "validate these agents" -> inspect agent files and report issues
```
