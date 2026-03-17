# OpenCode Skill Authoring

Use this file when creating, merging, or refining skills.

## Locations

- Project: `.opencode/skill/<name>/SKILL.md`
- Global: `~/.config/opencode/skill/<name>/SKILL.md`

## Structure

```text
skill-name/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

## Frontmatter pattern

```yaml
---
name: skill-name
description: |-
  Perform a specific OpenCode workflow. Use for concrete cases. Use proactively when the user asks for that workflow.

  Examples:
  - user: "..." -> action
  - user: "..." -> action
---
```

## Writing rules

- Skills are workflows, not personas.
- Put the trigger boundary in `description`.
- Keep the main file compact; move bulky material into `references/`.
- If two skills trigger on the same class of request, merge or narrow them.

## Trigger discipline

- Do not trigger only because the product name appears.
- Require a real match between the user request and the workflow the skill provides.
