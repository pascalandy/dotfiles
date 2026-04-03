# WritePRD

Create a comprehensive PRD through user interview, codebase exploration, and module design, then submit as a GitHub issue.

You may skip steps if you don't consider them necessary.

## Process

### 1. Capture the Problem

Ask the user for a long, detailed description of the problem they want to solve and any potential ideas for solutions. Let the user talk. Do not interrupt with premature structuring.

### 2. Explore the Codebase

Explore the repository to verify the user's assertions and understand the current state. Check existing patterns, data models, and related modules.

### 3. Interview Relentlessly

Interview the user about every aspect of the plan until reaching shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one.

Rules:
- Ask questions one at a time
- If a question can be answered by exploring the codebase, explore instead of asking
- For each question, provide your recommended answer

### 4. Sketch Major Modules

Identify the major modules to build or modify. Look for deep module opportunities. A deep module (as opposed to a shallow module) is one which encapsulates a lot of functionality in a simple, testable interface which rarely changes.

Check module sketches with the user. Ask which modules need tests.

### 5. Write and Submit the PRD

Create a GitHub issue using `gh issue create` with this structure:

```markdown
## Problem Statement
[From the user's perspective -- what's wrong, what's missing, why it matters]

## Solution
[From the user's perspective -- what the system will do differently]

## User Stories
[This list should be extremely extensive and cover all aspects of the feature]
1. As an <actor>, I want a <feature>, so that <benefit>
2. As a mobile bank customer, I want to see my balance update in real time, so that I can trust the displayed amount
3. ...

## Implementation Decisions
[Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.]
- Modules to build or modify and their responsibilities
- Key interfaces and function signatures
- Technical clarifications and constraints
- Architectural decisions and trade-offs
- Schema changes (new tables, columns, indexes)
- API contracts (endpoints, request/response shapes)
- Specific interactions between modules

## Testing Decisions
- A description of what makes a good test (only test external behavior, not implementation details)
- Which modules need tests and what kind
- Prior art in the codebase (existing test patterns to follow)

## Out of Scope
[What this PRD explicitly does NOT cover]

## Further Notes
[Optional additional context]
```
