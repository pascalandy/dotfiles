---
name: opencode-manager
description: |-
  Configure and maintain OpenCode itself: `opencode.json`, `AGENTS.md`, custom agents, slash commands, skills, permissions, and repository audits. Use for OpenCode administration, workflow setup, or troubleshooting. Do NOT use for ordinary coding tasks that merely happen inside OpenCode.

  Examples:
  - user: "Set up OpenCode for this repo" -> create or refine `opencode.json` and `AGENTS.md`
  - user: "Make an agent for code review" -> design the agent file, prompt, mode, and permissions
  - user: "Turn this prompt into a slash command" -> author a command with arguments, routing, and safe defaults
  - user: "Merge these OpenCode skills" -> refactor skill structure, frontmatter, and references
  - user: "Audit my OpenCode setup" -> run maintenance checks, review findings, and apply targeted fixes
---

# OpenCode Manager

<scope>
Use this skill when the task is about OpenCode itself: setup, config, usage patterns, agents, commands, skills, subagents, permissions, audits, or CLI troubleshooting.

Do NOT load it just because the user happens to be coding inside OpenCode. Ordinary coding, debugging, and refactoring should use the normal project workflow.

When OpenCode config is managed through chezmoi, treat the chezmoi source as the only editable location. MUST NOT edit the copy in the home directory directly.
</scope>

<workflow>
1. Classify the task:
   - configure OpenCode
   - use OpenCode effectively
   - create or refine agents, commands, or skills
   - work with subagents and workflows
   - audit or troubleshoot an OpenCode setup

2. Clarify only what matters:
   - project vs global
   - create vs update
   - permission boundary
   - expected trigger phrases or workflow

3. If the files are managed by chezmoi:
   - edit the chezmoi source, not the home-directory target
   - apply changes with `just cma`

4. Keep the main file light:
   - put details, schemas, and examples in `references/`
   - load only the reference file that matches the task
</workflow>

<checklist>
Before finishing, verify:
- the change is in the right scope
- chezmoi-managed files were edited in source, not in `$HOME`
- `just cma` was used when the change should be applied
- triggers are specific enough
- permissions are no broader than needed
- validation or smoke testing was run when practical
- the result will not over-trigger for generic coding work
</checklist>

<references>
Load only what the task needs:
- [official-links.md](references/official-links.md) for website, docs, and GitHub links
- [getting-started.md](references/getting-started.md) for configuring and using OpenCode
- [workflows.md](references/workflows.md) for planning, subagents, and repeatable workflows
- [best-practices.md](references/best-practices.md) for guardrails and operating habits
- [config-schema.md](references/config-schema.md) for `opencode.json`
- [agent-config.md](references/agent-config.md) and [agent-patterns.md](references/agent-patterns.md) for agents
- [command-authoring.md](references/command-authoring.md) for slash commands
- [skill-authoring.md](references/skill-authoring.md) for skills
- [cli.md](references/cli.md) for CLI commands and smoke checks
- [validation-rules.md](references/validation-rules.md) and [maintenance-standards.md](references/maintenance-standards.md) for audits
</references>
