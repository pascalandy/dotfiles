# RequestRefactor

Create a detailed refactor plan with tiny commits via user interview, then file it as a GitHub issue.

You may skip steps if you don't consider them necessary.

## Process

### 1. Capture the Problem

Ask for a long, detailed description of:
- What is wrong with the current code
- What the user thinks the solution might be
- Why this refactor matters now

### 2. Explore the Repository

Verify the user's assertions about the current state. Understand:
- The modules involved and their interfaces
- How callers interact with the code being refactored
- Existing test coverage of the area

### 3. Present Alternatives

Ask what other options were considered. Present alternatives the user may not have thought of. Challenge the proposed approach if a simpler option exists.

### 4. Interview in Extreme Detail

Interview the user about the implementation. Be extremely detailed and thorough. Walk through the implementation plan one decision at a time:
- What changes and what stays the same?
- What are the interface contracts before and after?
- How do callers migrate?
- What are the failure modes during migration?

### 5. Hammer Out Exact Scope

Define precisely:
- What changes
- What does NOT change
- Where the boundary is between this refactor and future work

### 6. Check Test Coverage

Examine existing test coverage of the affected area. If coverage is insufficient:
- Ask about the user's testing plan
- Recommend what tests to add before refactoring

### 7. Break into Tiny Commits

Plan the implementation as a sequence of tiny commits. Remember Martin Fowler's advice: "make each refactoring step as small as possible, so that you can always see the program working."

Rules:
- Each commit leaves the codebase in a fully working state
- Each commit does one logical thing
- Commits are ordered so each builds on the previous
- No commit should be large enough to create merge conflicts

### 8. Create GitHub Issue

Use `gh issue create`:

```markdown
## Problem Statement
[What is wrong, why it matters]

## Solution
[What the refactored code will look like -- interfaces and contracts, not file paths]

## Commits
[LONG, detailed plan of tiny commits]
1. [First commit -- what it does, leaves codebase working]
2. [Second commit -- builds on first]
3. ...

## Decision Document
[Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.]
- Modules and their responsibilities
- Key interfaces and function signatures
- Technical clarifications and constraints
- Architectural decisions and trade-offs
- Schema changes (if any)
- API contracts (if any)
- Specific interactions between modules

## Testing Decisions
- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules need tests and what kind
- Prior art in the codebase (existing test patterns to follow)

## Out of Scope
[What this refactor explicitly does NOT touch]

## Further Notes
[Optional additional context]
```
