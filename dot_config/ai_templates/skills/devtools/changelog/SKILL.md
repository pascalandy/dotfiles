---
name: changelog
description: Update CHANGELOG.md following project conventions. Use when adding, fixing, or removing features that need changelog entries.
---

# Changelog Skill

Curate business-value changes from git history into `CHANGELOG.md`.

**Don't let your friends dump git logs into changelogs.**

## Workflow

### 1. Detect Format Convention

Read the existing `CHANGELOG.md` and identify which convention is used:

| Convention            | Pattern                       | Continue with                  |
| --------------------- | ----------------------------- | ------------------------------ |
| **Date-based**        | `## 2025-12-22 — Title`       | New date section at top        |
| **Unreleased + tags** | `## Unreleased` / `## v1.2.3` | Add to `## Unreleased` section |

If no changelog exists, ask the user which convention to use.

### 2. Pick Baseline

Determine the starting point for collecting commits:

- Use the **last entry date** in `CHANGELOG.md`
- If no entries exist, use the first commit date

**Important:** Always exclude today's commits — generate up to end of yesterday only.

### 3. Collect Commits

```bash
git log <baseline>..HEAD --oneline --reverse
```

Skim diffs as needed to understand business impact.

### 4. Curate Entries

#### Include

- New features and capabilities
- Bug fixes
- Breaking changes
- Refactors (they enable future work)
- Documentation updates ("updated docs for X")
- Test additions ("added N tests for X")
- Notable UX/behavior tweaks

#### Exclude

- Typo-only edits
- Dependency bumps (unless security/breaking)
- Features added then removed in same window
- Meta entries like "update changelog"

#### Curation Guidelines

- Curate aggressively — drop minor/temporary items
- Combine related items when possible
- Remove redundant entries

### 5. Edit CHANGELOG.md

#### Structure: Sectioned Grouping

Group related changes under labeled sections within each date entry:

```markdown
## YYYY-MM-DD — Descriptive Title

skills:
- add `skill-name` for description (abc1234)
- rename `old-name` to `new-name` for clarity (def5678)

projects:
- move X from WORKDIR to IDEATION (ghi9012)

commands:
- simplify `command-name` workflow (jkl3456)

scripts:
- add sync-tool for description (mno7890)
```

#### Section Labels

- Use lowercase with colon: `skills:`, `projects:`, `commands:`, `scripts:`, `docs:`, etc.
- Infer section names from the nature of changes (flexible, not fixed categories)
- Only create sections when there are multiple related items

#### Text Style

- Use **lowercase verbs**: `add`, `move`, `fix`, `remove`, `rename` (not Title Case)
- Use **backticks** on technical names: skill names, script names, CLI flags, file paths
- Use **bold** for emphasis on key terms when needed, e.g., `**librarian**`
- Include short SHA commit links at end of line: `(abc1234)`
- Add PR/issue numbers when available: `#123`

### 6. Sanity Checks

- [ ] Markdown renders correctly
- [ ] No duplicate entries
- [ ] Wording is concise (lowercase verbs, backticks on tech names)
- [ ] Breaking changes are clearly marked
- [ ] Today's commits are excluded
- [ ] Sections are logically grouped

## Format Reference

See `references/format.md` for detailed format examples and anti-patterns.
