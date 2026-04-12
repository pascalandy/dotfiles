# Resolution Template

## Bug Track Template

```markdown
---
title: [Title]
date: YYYY-MM-DD
module: [Module]
problem_type: [enum]
component: [enum]
severity: [level]
tags: [tag1, tag2, tag3]
category: [auto-mapped]
---

# [Title]

## Problem

[1-2 sentence description of the issue]

## Symptoms

- [Observable symptom 1: exact error message, behavior]
- [Observable symptom 2]
- [Observable symptom 3]

## What Didn't Work

- [Failed investigation attempt 1 and why it failed]
- [Failed investigation attempt 2]

## Solution

[The actual fix with code examples]

\`\`\`language
// Before (broken)
[problematic code]

// After (fixed)
[corrected code]
\`\`\`

## Why This Works

[Root cause explanation and why the solution addresses it]

## Prevention

- [Strategy 1 to avoid recurrence]
- [Strategy 2: test case, linting rule, code review checklist item]
```

## Knowledge Track Template

```markdown
---
title: [Title]
date: YYYY-MM-DD
module: [Module]
problem_type: best_practice
component: [enum]
severity: [level]
tags: [tag1, tag2, tag3]
category: best-practices
---

# [Title]

## Context

[What situation, gap, or friction prompted this guidance]

## Guidance

[The practice, pattern, or recommendation with code examples when useful]

\`\`\`language
// Example
[illustrative code]
\`\`\`

## Why This Matters

[Rationale and impact of following or not following this guidance]

## When to Apply

[Conditions or situations where this applies]

## Examples

[Concrete before/after or usage examples]
```
