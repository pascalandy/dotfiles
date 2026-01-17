## Skills

Discovered at startup from ~/.opencode/skill. Entries: name, description, file path. Content not inlined; context stays lean.

Example format:

- skill-name: description (file: ~/.opencode/skill/skill-name/skill.md)

### Discovery

- Source of truth: project docs + runtime "## Skills" section
- Skill bodies on disk at listed paths

### Triggers

- Explicit: `$SkillName` or plain text mention → use that skill
- Implicit: task matches skill description → use it
- Multiple mentions → use all
- No carry-over across turns unless re-mentioned
- YAML `description` in SKILL.md = primary trigger signal; clarify if unsure

### Usage (progressive disclosure)

1. Open SKILL.md; read minimum needed
2. `references/` → load only files needed, no bulk
3. `scripts/` → run/patch; avoid retyping
4. `assets/`/templates → reuse, don't recreate
5. Ignore directories starting with a dot. example: `.solution_design`

### Multi-skill

- Minimal set covering request; state order
- Announce skill(s) + reason (one line)
- Skipping obvious skill → state why

### Context hygiene

- Summarize long sections; load extras only when needed
- One-hop refs preferred; avoid deep nesting
- Variants (frameworks/providers/domains) → pick relevant file(s), note choice

### Fallback

- Missing/blocked skill → say so briefly, continue with best alternative
- Unclean apply (missing files, unclear) → state issue, next-best approach, proceed
