# PRDToIssues

Break a PRD into independently-grabbable GitHub issues using tracer-bullet vertical slices.

## Process

### 1. Locate the PRD

Ask for the PRD issue number or URL. If the PRD is not already in your context window, fetch it with `gh issue view <number>` (with comments).

### 2. Explore the Codebase (Optional)

If the PRD references existing modules or patterns, explore to understand the current state of the code.

### 3. Draft Vertical Slices

Break into **tracer bullet** issues. Each is a thin vertical slice through ALL integration layers end-to-end, NOT a horizontal layer.

Each slice is classified as:
- **HITL** -- Human-in-the-loop. Requires human interaction, such as an architectural decision or a design review.
- **AFK** -- Autonomous. Can be implemented and merged without human interaction.

Prefer AFK when the slice is well-specified with clear acceptance criteria.

Rules:
- Each slice delivers a narrow but COMPLETE path through every layer
- Each completed slice is demoable and verifiable on its own
- Prefer many thin slices over few thick ones

### 4. Quiz the User

Present the breakdown with:
- Title
- Type (HITL or AFK)
- Blocked by (dependencies)
- User stories covered

Ask about:
- Granularity -- should any slice be split or merged?
- Dependencies -- are the ordering constraints correct?
- HITL vs AFK -- should any classification change?

Iterate until approved.

### 5. Create the GitHub Issues

Create issues in dependency order (blockers first) so you can reference real issue numbers in the "Blocked by" field. Use `gh issue create` for each.

```markdown
**Parent PRD:** #<issue-number>
**Type:** AFK / HITL

## What to Build
[End-to-end behavior this slice delivers]

## Acceptance Criteria
- [ ] [Concrete, testable criterion]
- [ ] ...

## Blocked By
- #<issue-number>
- Or "None -- can start immediately"

## User Stories Addressed
- [From the PRD]
```

Rules:
- Do NOT close or modify the parent PRD issue
- Do NOT include specific file paths or code snippets
- Each issue must be independently understandable
- Prefer many thin issues over few thick ones
- Mark blocking relationships honestly
- Maximize parallelism -- the goal is that multiple people (or agents) can grab different issues simultaneously
