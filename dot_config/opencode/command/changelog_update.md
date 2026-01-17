---
description: update changelog
---

Update `CHANGELOG.md` using the changelog skill.

## Instructions

1. Load the changelog skill first
2. Curate changes from git history since the last entry in CHANGELOG.md
3. **Always exclude today's commits** — generate up to end of yesterday only

## Grouping

- Group entries by **date** (not by release/tag)
- Only include dates where work was done
- Example: if work happened on Dec 26, 27, and 30 (but not 28-29), show sections for 26, 27, and 30

## What to Include

Focus on **business value**, not just user-facing changes:

- New features and capabilities
- Bug fixes
- Refactors (they enable future work)
- Documentation updates ("updated docs for X")
- Test additions ("added N tests for X")
- Skip dependency bumps (unless significant)
- Skip meta entries like "update changelog"

## Format

### Structure

- Use **sections** to group related changes within a date entry
- Section labels are lowercase with colon: `skills:`, `projects:`, `commands:`, `scripts:`, etc.
- Infer section names from the nature of changes (flexible, not fixed categories)

### Text Style

- Use **lowercase verbs**: `add`, `move`, `fix`, `remove`, `rename` (not Title Case)
- Use **backticks** on technical names: skill names, script names, CLI flags, file paths
- Use **bold** for emphasis on key terms when needed
- Include short SHA commit links at end of line, e.g., `(abc1234)`

### Example

```markdown
## 2025-12-31 — Skills Refactoring & Tool Organization

skills:
- add `cli-creator` skill for CLI design framework (abc1234)
- rename `coding-in-bash` to `bash` for clarity (def5678)

scripts:
- add sync-skills for AI agent skill management (ghi9012)

commands:
- simplify project_status orchestrator command (jkl3456)
```

### Curation

- Curate aggressively — drop minor/temporary items
- Combine related items when possible
- Remove redundant or meta entries
