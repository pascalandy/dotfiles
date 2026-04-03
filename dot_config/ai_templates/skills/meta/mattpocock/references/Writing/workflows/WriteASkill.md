# WriteASkill

Create new agent skills with proper structure, progressive disclosure, and bundled resources.

## Process

### 1. Gather Requirements

Ask about:
- What task or domain does this skill cover?
- What are the primary use cases?
- Does it need executable scripts or just instructions?
- Any reference materials to bundle?

### 2. Draft the Skill

Create the skill directory with:

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Detailed docs (if content exceeds ~500 lines total)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
```

### 3. Write SKILL.md

Use this template:

```markdown
---
name: skill-name
description: What it does. Use when [specific triggers].
---

# Skill Name

## Quick Start
[What it does, how to invoke it]

## Workflows
[Step-by-step processes]

## Advanced Features
[Link to REFERENCE.md or other files if needed]
```

### 4. Write the Description

The description is **the only thing the AI sees** when deciding which skill to load. It must be precise.

Rules:
- Maximum 1024 characters
- Write in third person
- First sentence: what it does
- Second sentence: "Use when [specific triggers]"
- Include when/why to trigger it (specific keywords, contexts, file types)

Good: "Extract text and tables from PDF files using OCR and structural analysis. Use when the user has a PDF to parse, mentions 'extract from PDF', or needs tabular data from a document."

Bad: "Helps with documents." (No triggers, no specifics, agent has no idea when to load this.)

### 5. Review with User

Present the draft. Ask about:
- Coverage -- does it handle all use cases?
- Missing items -- anything not covered?
- Detail level -- too much or too little?

## When to Add Scripts

Add scripts when:
- An operation is deterministic and repeatable
- The same code would be generated every time
- Errors need explicit handling with specific exit codes

## When to Split Files

Split into separate reference files when:
- SKILL.md would exceed ~100 lines
- There are distinct domains within the skill
- Advanced features are rarely needed

## Review Checklist

- [ ] Description includes trigger phrases
- [ ] SKILL.md is under ~100 lines (split if needed)
- [ ] No time-sensitive information (versions, dates that go stale)
- [ ] Consistent terminology throughout
- [ ] Concrete examples, not abstract descriptions
- [ ] References are one level deep (no reference-to-reference chains)
- [ ] Harness-agnostic (no assistant-specific paths or tool names)
