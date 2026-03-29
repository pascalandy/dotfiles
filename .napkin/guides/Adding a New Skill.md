---
date: "2026-03-29"
tags:
  - guide
---
# Adding a New Skill

## Prerequisites
- Skill follows the standard structure (SKILL.md + optional scripts/ and references/)
- You know which agents need this skill (OpenCode-only vs shared)

## Steps

### For OpenCode-only skills
1. Create skill under `dot_config/opencode/skill/`
2. Follow naming convention: `skill-name/SKILL.md`
3. No sync needed — OpenCode reads directly from its own skill directory

### For shared skills (distributed to all agents)
1. Create skill under `dot_config/ai_templates/skills/`
   ```
   dot_config/ai_templates/skills/your-skill/
   ├── SKILL.md
   ├── scripts/ (optional)
   └── references/ (optional)
   ```

2. Write SKILL.md following the template:
   - Frontmatter with name, description, version
   - Clear usage instructions
   - Any required parameters or environment variables

3. Apply changes
   ```bash
   just cm-apply-verbose
   ```
   The `run_after_backup.sh` script will sync to all agent homes automatically.

4. Verify distribution
   - Check Claude: `~/.claude/skills/`
   - Check Codex: `~/.codex/skills/`
   - Check Gemini: `~/.gemini/skills/`
   - Check Pi: `~/.pi/skills/`

## Common problems
- **Skill not appearing** — Run `chezmoi apply` to trigger the sync
- **Merge conflicts** — OpenCode-specific skills take precedence over shared ones
- **Wrong location** — Shared skills go in `ai_templates/`, OpenCode-only in `opencode/skill/`

## Related
- [[AI Tooling Surface]]
- [[Chezmoi Apply Automation]]
