# ImproveArchitecture

Explore a codebase to find opportunities for architectural improvement, focusing on deepening shallow modules and improving testability.

## Process

### 1. Explore the Codebase

Navigate the codebase naturally. Do NOT follow rigid heuristics -- explore organically and note where you experience friction. The friction you encounter IS the signal.

Note:

- Where does understanding one concept require bouncing between many small files?
- Where are modules so shallow that the interface is nearly as complex as the implementation?
- Where have pure functions been extracted solely for testability?
- Where do tightly-coupled modules create integration risk?
- Which parts are untested or hard to test?

### 2. Present Candidates

Do NOT propose interfaces yet. Provide a numbered list of deepening opportunities. For each candidate:

- **Cluster** -- which modules/concepts would be consolidated
- **Why coupled** -- evidence: shared types, call patterns, co-ownership of a concept
- **Dependency category** -- In-process / Local-substitutable / Remote-but-owned / True-external (see `references/DeepModules.md`)
- **Test impact** -- what existing tests would be replaced by boundary tests on the consolidated module

Ask the user: "Which of these would you like to explore?"

### 3. User Picks a Candidate

### 4. Frame the Problem Space

Write a user-facing explanation of the selected candidate:
- Constraints (what cannot change)
- Dependencies (what this module depends on, what depends on it)
- Rough illustrative code sketch showing the current interface shape

This is not a proposal, just a way to ground the constraints. Show to the user, then immediately proceed to Step 5. The user reads and thinks about the problem while the sub-agents work in parallel.

### 5. Design Multiple Interfaces

Spawn 3+ sub-agents in parallel. Prompt each sub-agent with a separate technical brief (coupling details, dependency category, what is being hidden). This brief is independent of the user-facing explanation in Step 4.

Design constraints:
- Agent 1: Minimize interface (1-3 entry points)
- Agent 2: Maximize flexibility
- Agent 3: Optimize for the most common caller
- Agent 4 (optional): Ports & adapters pattern

Each agent outputs:
1. Interface signature
2. Usage example
3. What it hides internally
4. Trade-offs

After comparing, give your own recommendation: which design you think is strongest and why. If elements from different designs would combine well, propose a hybrid. Be opinionated -- the user wants a strong read, not just a menu.

### 6. User Picks an Interface

### 7. Create GitHub Issue

Do NOT ask the user to review before creating -- just create it and share the URL. Use `gh issue create`:

```markdown
## Problem
- Which modules are shallow and tightly coupled
- Integration risk in the seams between them
- Why this makes the codebase harder to navigate and maintain

## Proposed Interface
- Interface signature
- Usage example
- What complexity it hides
- Durable architectural guidance that is NOT coupled to current file paths

## Dependency Strategy
- In-process / Local-substitutable / Ports & adapters / Mock
- Recommendation for this specific case

## Testing Strategy
- Replace, don't layer: new boundary tests replace old shallow-module unit tests
- Write tests at the module boundary, assert on observable outcomes
- Tests should survive internal refactors
- New boundary tests to write
- Old tests to delete
- Test environment needs

## Implementation Recommendations
- What the module should own, hide, and expose
- How callers should migrate
```
