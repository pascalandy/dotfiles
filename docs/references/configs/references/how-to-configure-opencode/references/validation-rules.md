---
name: Validation Rules
description: Metadata validation rules for auditing OpenCode configurations
tags:
  - area/ea
  - kind/doc
  - status/stable
date_created: 2025-04-11
date_updated: 2025-04-11
---

# OpenCode Validation Rules

Use this file when auditing or fixing OpenCode metadata.

## Frontmatter requirements

- Agent, command, and skill markdown files MUST have YAML frontmatter.
- Multi-line descriptions SHOULD use `|-`.
- Skill `name:` MUST match the skill directory name.

## Description rules

### Skills

- Start with the capability, not a persona.
- Include a concrete `Use for` or `Use when` clause.
- Include at least two examples in `user: "..." -> action` form.

### Agents

- Describe what triggers the agent.
- Include examples when the agent is not an obvious manual-only primary agent.

### Commands

- Keep descriptions short enough to scan in command lists.

## Audit workflow

1. Run the audit.
2. Read the full output.
3. Open the files mentioned by the audit.
4. Apply targeted fixes.
5. Re-run the audit.

If the fixes are broad or risky, ask the user before changing behavior.
