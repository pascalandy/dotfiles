---
description: review-code
---

FIRST STEP:
Read @AGENTS.md to understand project conventions before reviewing.

Please do a code review of: {$ARGUMENTS}

FOCUS: [correctness, readability, performance, idiomatic Python etc.]

THEN:
Once your code review is completed, reverse engineer it into an **implementation-ready prompt** for a coder

REQUIREMENTS:

1. **Extract all actionable suggestions** — code changes, refactors, fixes, improvements
2. **Preserve context** — include file paths, function names, dependencies, constraints
3. **Be explicit** — assume the coder has no prior context
4. **Output only** — don't ask me to implement, just provide the spec

OUTPUT FORMAT:

```md
## Context
[Brief summary of what the code does and its current state]

## Files Involved
[List of files/paths]

## Changes Required
1. 🔴/🟡/🟢 [Specific change with details]
2. ...

## Constraints / Notes
[Gotchas, edge cases, style preferences]

## Decisions Needed
[Ambiguities or trade-offs requiring your input]
```
