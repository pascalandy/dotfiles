# Changelog Format Reference

## Convention 1: Date-based with Sections

For personal projects, internal tools, no formal releases.

### Basic Structure

```markdown
## YYYY-MM-DD — Descriptive Title

section-name:
- description of change (abc1234)
- another change (def5678)

another-section:
- more changes here (ghi9012)
```

### Elements

- **ISO date** (`2025-12-22`) as version identifier
- **Em dash** (`—`) as separator
- **Short title** summarizing the change intent
- **Section labels** — lowercase with colon: `skills:`, `projects:`, `commands:`, `scripts:`, etc.
- **Bullets** describing concrete changes
- **Short SHA** commit links in parentheses at end of line: `(abc1234)`

### Text Style

- **Lowercase verbs**: `add`, `move`, `fix`, `remove`, `rename` (not Title Case)
- **Backticks** on technical names: skill names, script names, CLI flags, file paths
- **Bold** for emphasis on key terms when needed

### Full Example

```markdown
## 2025-12-31 — Skills Refactoring & Tool Organization

skills:
- add `cli-creator` skill for CLI design framework (abc1234)
- add `shellck` skill for shell script linting (def5678)
- move `pg-memory` to skills directory (ghi9012)
- rename `coding-in-bash` to `bash` for clarity (jkl3456)
- rename `task-search` to `agt-search` for **librarian** delegation (mno7890)
- remove deprecated `cas-utilisation` skill (pqr1234)

projects:
- move multiple projects from WORKDIR to IDEATION: antinote, debug_zen_quote, nuxt_blog (stu5678)
- move docling research from IDEATION to WORKDIR (vwx9012)
- remove sevalla-cli and fs_explorer projects (yza3456)

commands:
- simplify `project_status` orchestrator command (bcd7890)
- fix REPO_ROOT path in `scan_projects.py` (efg1234)

scripts:
- add sync-skills for AI agent skill management (hij5678)
- add sync-commands for slash commands distribution (klm9012)
- add logging to post-commit hook for better tracking (nop3456)

docs:
- update AGENTS skill to ignore dot directories (qrs7890)
- add concise communication guideline (tuv1234)
```

### Simple Example (Few Changes)

When there are only a few changes, sections are optional:

```markdown
## 2025-12-22 — Remove Custom rm Shim
- drop `bin/rm` and `scripts/trash.ts`; rely on system `trash` command (a1b2c3d)
```

## Convention 2: Unreleased + Tags

For published packages, OSS, semantic versioning.

```markdown
## Unreleased
- Added feature X. #123
- Fixed bug Y. #456

## v1.2.3 — 2025-12-20
- Added feature Z. #100
```

**Elements:**

- **Unreleased section** at top for pending changes
- **Version tag** (`v1.2.3`) when releasing
- **PR/issue references** (`#123`) when available

## Principles

- Changelogs are for humans, not machines
- Newest entries at top
- Use sections to group related changes (infer from nature of changes)
- Use lowercase verbs and backticks on technical names
- Clearly mark breaking changes
- Focus on **business value**, not just user-facing changes
- Include refactors (they enable future work), docs updates, and test additions
- Always exclude today's commits (generate up to yesterday only)
- Curate aggressively — drop minor/temporary items

## Anti-patterns

- **Commit log dumps** — Commits document code evolution; changelog documents notable business-value changes
- **Title Case verbs** — Use lowercase: `add`, not `Add`
- **Missing backticks** — Technical names should be in backticks: `skill-name`
- **Flat lists** — Group related items into sections when there are many changes
- **Inconsistent entries** — A partial changelog can be worse than none
- **Ignoring deprecations** — Always mention what will break
- **Including today's commits** — Work may still be in progress
- **Meta entries** — Skip "update changelog" type entries
