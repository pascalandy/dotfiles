# PRDToPlan

Convert a PRD into a phased implementation plan using tracer-bullet vertical slices. Output is a Markdown file in `./plans/`.

## Process

### 1. Confirm the PRD Is in Context

The PRD should already be in the conversation. If it is not, ask the user to paste it or point you to the file. If the PRD is a GitHub issue, fetch it with `gh issue view <number>` (with comments).

### 2. Explore the Codebase

Understand the current architecture, existing patterns, and integration points relevant to the PRD.

### 3. Identify Durable Architectural Decisions

Before slicing, identify decisions that span multiple phases:
- **Routes:** URL patterns and route structure
- **Schema:** Database schema shapes (tables, key columns)
- **Key models:** Data models and their relationships
- **Auth:** Authentication/authorization approach
- **Boundaries:** Third-party service boundaries

These go in the plan header and inform every phase.

### 4. Draft Vertical Slices

Break the PRD into phases. Each phase is a thin vertical slice through ALL integration layers end-to-end (schema, API, UI, tests).

Rules:
- Each slice delivers a narrow but COMPLETE path through every layer
- Each completed slice is demoable and verifiable on its own
- Prefer many thin slices over few thick ones
- Do NOT include specific file names or implementation details likely to change
- DO include durable decisions: route paths, schema shapes, data model names, interface contracts

### 5. Quiz the User

Present the breakdown. For each phase show: title and which user stories it covers.

Ask:
- Does the granularity feel right?
- Should any phases be merged or split further?

Iterate until the user approves.

### 6. Write the Plan File

Create `./plans/<feature-name>.md`:

```markdown
# Plan: <Feature Name>

> Source PRD: <brief identifier or link>

---

## Architectural Decisions
- **Routes:** ...
- **Schema:** ...
- **Key models:** ...
- **Auth:** ...
- **Boundaries:** ...

---

## Phase 1: <Title>
**User stories:** [which ones from the PRD]
**What to build:** [end-to-end behavior, not file-level tasks]
**Acceptance criteria:**
- [ ] [Concrete, testable criterion]
- [ ] ...

---

## Phase 2: <Title>
**User stories:** ...
**What to build:** ...
**Acceptance criteria:**
- [ ] ...

---

<!-- Repeat for each phase -->
```
