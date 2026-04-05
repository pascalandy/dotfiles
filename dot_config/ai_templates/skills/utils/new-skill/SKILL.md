---
name: new-skill
description: Create new agent skills following the Agent Skills specification. Use when the user says "new-skill", "create a skill", "write a skill", or wants to scaffold a new SKILL.md with proper frontmatter, structure, and progressive disclosure.
metadata:
  ref: https://code.claude.com/docs/en/cli-reference
---

# Create a New Skill

## Workflow

1. Ask the user: skill name, what it does, and when it should trigger
2. Create the skill directory and `SKILL.md`
3. Add scripts/references/assets only if needed

## SKILL.md Template

```markdown
---
name: skill-name
description: What the skill does and when to use it. Be specific about trigger conditions.
---

# Skill Title

Core instructions go here. Keep under 500 lines / 5000 tokens.

Move detailed reference material to `references/` and tell the agent when to load it.
```

## Directory Structure

```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs loaded on demand
└── assets/           # Optional: templates, schemas, resources
```

## Frontmatter Rules

| Field | Required | Notes |
|-------|----------|-------|
| `name` | Yes | Lowercase, hyphens only. Must match directory name. Max 64 chars. |
| `description` | Yes | Max 1024 chars. Describe what it does AND when to use it. |
| `compatibility` | No | Environment requirements (e.g., "Requires Python 3.14+ and uv") |
| `metadata` | No | Arbitrary key-value pairs (author, version) |

## Description Best Practices

- Use imperative phrasing: "Use when..." not "This skill does..."
- Focus on user intent, not implementation details
- List explicit trigger conditions including indirect ones
- Keep concise -- a few sentences to a short paragraph

## Instructions Best Practices

- Add what the agent lacks, omit what it knows
- Provide defaults, not menus of equal options
- Favor procedures over declarations
- Include a gotchas section for non-obvious facts
- Use validation loops: do work, validate, fix, repeat

## Full Specification and Guides

Read these references for depth:

- [Agent Skills Specification](https://agentskills.io/specification)
- [Best Practices](https://agentskills.io/skill-creation/best-practices)
- [Optimizing Descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Using Scripts](https://agentskills.io/skill-creation/using-scripts)
