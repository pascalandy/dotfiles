---
title: Create nia-docs skill for centralized documentation browsing
type: feat
status: draft
date: 2026-04-07
---

# Create nia-docs skill for centralized documentation browsing

## Overview

Create a new skill called `nia-docs` that provides centralized documentation for using the `npx nia-docs` CLI tool. This skill will package the Quick Reference content currently duplicated across three headless-* UPDATE.md files.

## Problem Statement

The same 5 `npx nia-docs` command examples are duplicated verbatim in:
- `headless-claude/references/UPDATE.md` (lines 17-34)
- `headless-codex/references/UPDATE.md` (lines 17-34)
- `headless-opencode/references/UPDATE.md` (lines 17-34)

## Proposed Solution

Create a standalone `nia-docs` skill containing the Quick Reference documentation.

## Scope

**In Scope:**
- Create `dot_config/ai_templates/skills/utils/nia-docs/SKILL.md`

**Out of Scope (for later):**
- Updating headless-* UPDATE.md files
- Creating references/ directory or additional files

## Technical Approach

### Skill Structure

```
dot_config/ai_templates/skills/utils/nia-docs/SKILL.md
```

### SKILL.md Content

**Frontmatter:**
- `name`: nia-docs
- `description`: Use when the user needs to browse documentation sites using npx nia-docs. Provides command patterns for searching, reading, and exploring documentation.

**Sections:**
1. **Quick Start** - Basic usage patterns
2. **Command Patterns** - All 5 command examples from current UPDATE.md files
3. **Configuration** - Setting DOC_URL
4. **Usage Notes** - Shell behavior, available tools
5. **Gotchas** - Non-obvious behaviors

## Acceptance Criteria

- [ ] nia-docs skill created at `dot_config/ai_templates/skills/utils/nia-docs/SKILL.md`
- [ ] Skill includes all 5 command patterns currently duplicated
- [ ] Skill includes Configuration section with DOC_URL setup
- [ ] Skill includes Usage Notes and Gotchas sections
- [ ] chezmoi apply syncs the new skill successfully

## Success Metrics

- Single skill file containing nia-docs documentation
- Ready for future integration into headless-* UPDATE.md files

## Dependencies & Risks

**Dependencies:** None

**Risks:** Low - additive change only

## Sources & References

### Current Duplication

All three files contain identical Quick Reference sections:
- `/dot_config/ai_templates/skills/utils/headless-claude/references/UPDATE.md` (lines 17-34)
- `/dot_config/ai_templates/skills/utils/headless-codex/references/UPDATE.md` (lines 17-34)
- `/dot_config/ai_templates/skills/utils/headless-opencode/references/UPDATE.md` (lines 17-34)

### nia-docs Tool

- Tool: `npx nia-docs`
- Purpose: Browse documentation sites via bash commands