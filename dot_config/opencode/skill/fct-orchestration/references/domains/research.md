# Research Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Discovery is where great work begins.                     │
│   Explore broadly, synthesize clearly, answer confidently.  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **AGENT REMINDER**: Only use `@ben`, `@abby`, or `@oracle`.
> See [SKILL.md](../../SKILL.md) for costs and task mapping.
> NEVER use `general`, `explore`, or invented agent names.

> **Load when**: Codebase exploration, technical investigation, dependency analysis, documentation research
> **Common patterns**: Breadth-First Discovery, Feature Tracing, Root Cause Analysis

## Table of Contents

1. [Codebase Exploration](#codebase-exploration)
2. [Technical Investigation](#technical-investigation)
3. [Dependency Analysis](#dependency-analysis)
4. [Documentation Research](#documentation-research)
5. [Competitive Analysis](#competitive-analysis)

---

## Codebase Exploration

### Pattern: Breadth-First Discovery

```
User Request: "Help me understand this codebase"

Phase 1: FAN-OUT (Parallel surface scan)
├─ @ben: Project structure, entry points
├─ @ben: Package.json/requirements/build files
├─ @ben: README, docs folder
└─ @ben: Test structure and patterns

Phase 2: REDUCE
└─ @abby: Synthesize codebase overview

Phase 3: FAN-OUT (Deep dive areas of interest)
├─ @ben: Deep dive area 1
├─ @ben: Deep dive area 2
└─ @ben: Deep dive area 3
```

### Pattern: Feature Tracing

```
User Request: "How does user authentication work?"

Phase 1: EXPLORE
└─ @ben: Find auth-related files (grep patterns)

Phase 2: PIPELINE (Follow the flow)
├─ @ben: Entry point (login route/component)
├─ @ben: Middleware/validation layer
├─ @ben: Session/token handling
└─ @ben: Database/storage layer

Phase 3: REDUCE
└─ @abby: Document complete auth flow
```

### Pattern: Impact Analysis

```
User Request: "What would break if I change UserService?"

Phase 1: EXPLORE
└─ @ben: Find UserService definition and interface

Phase 2: FAN-OUT
├─ @ben: Find all imports of UserService
├─ @ben: Find all usages of each method
└─ @ben: Find tests depending on UserService

Phase 3: REDUCE
└─ @abby: Impact report with risk assessment
```

---

## Technical Investigation

### Pattern: Root Cause Analysis

```
User Request: "Why is the API slow?"

Phase 1: FAN-OUT (Parallel hypothesis generation)
├─ @ben: Check database query patterns
├─ @ben: Check API middleware chain
├─ @ben: Check external service calls
└─ @ben: Check caching implementation

Phase 2: REDUCE
└─ @abby: Ranked hypotheses with evidence

Phase 3: PIPELINE (Validate top hypothesis)
└─ @abby: Instrument/test to confirm
```

### Pattern: Technology Evaluation

```
User Request: "Should we use Redis or Memcached?"

Phase 1: FAN-OUT (Parallel research)
├─ @ben: Redis features, use cases, benchmarks (web search)
├─ @ben: Memcached features, use cases, benchmarks (web search)
└─ @ben: Current caching patterns in codebase

Phase 2: REDUCE
└─ @abby: Comparison matrix, recommendation with rationale
```

### Pattern: Bug Archaeology

```
User Request: "When did this bug get introduced?"

Phase 1: EXPLORE
└─ @ben: Identify relevant files and functions

Phase 2: BACKGROUND
└─ @ben: Git bisect or log analysis

Phase 3: PIPELINE
└─ @abby: Timeline of changes, root cause commit
```

---

## Dependency Analysis

### Pattern: Dependency Graph

```
User Request: "Map all dependencies for the auth module"

Phase 1: EXPLORE
└─ @ben: Find auth module entry points

Phase 2: FAN-OUT (Parallel tracing)
├─ @ben: Trace internal dependencies
├─ @ben: Trace external package dependencies
└─ @ben: Trace database/service dependencies

Phase 3: REDUCE
└─ @abby: Dependency graph visualization
```

### Pattern: Upgrade Impact

```
User Request: "What happens if we upgrade lodash?"

Phase 1: FAN-OUT
├─ @ben: Find all lodash usages
├─ @ben: lodash changelog, breaking changes (web search)
└─ @ben: Find tests covering lodash functionality

Phase 2: REDUCE
└─ @abby: Impact assessment, migration guide
```

### Pattern: Dead Code Detection

```
Phase 1: EXPLORE
└─ @ben: Build export/import graph

Phase 2: FAN-OUT
├─ @ben: Find unreferenced exports
├─ @ben: Find unused internal functions
└─ @ben: Find commented/disabled code

Phase 3: REDUCE
└─ @abby: Dead code report with safe removal list
```

---

## Documentation Research

### Pattern: API Discovery

```
User Request: "Document all API endpoints"

Phase 1: EXPLORE
└─ @ben: Find route definitions (express routes, decorators, etc.)

Phase 2: MAP (Per endpoint group - parallel @ben tasks)
├─ @ben: Document endpoint group 1 (params, responses)
├─ @ben: Document endpoint group 2
└─ @ben: Document endpoint group 3

Phase 3: REDUCE
└─ @abby: Unified API documentation
```
User Request: "Document all API endpoints"

Phase 1: EXPLORE
└─ @ben: Find route definitions (express routes, decorators, etc.)

Phase 2: MAP (Per endpoint)
├─ Agent A: Document endpoint group 1 (params, responses)
├─ Agent B: Document endpoint group 2
└─ Agent C: Document endpoint group 3

Phase 3: REDUCE
└─ @abby: Unified API documentation
```

### Pattern: Cross-Reference

```
User Request: "Find all documentation for the payment system"

Phase 1: FAN-OUT
├─ @ben: Search code comments
├─ @ben: Search markdown files
├─ @ben: Search wiki/confluence (if accessible)
└─ @ben: Search inline JSDoc/docstrings

Phase 2: REDUCE
└─ @abby: Consolidated documentation index
```

---

## Competitive Analysis

### Pattern: Feature Comparison

```
User Request: "Compare our auth to Auth0"

Phase 1: FAN-OUT
├─ @ben: Document our auth capabilities
├─ @ben: Auth0 features and pricing (web search)
└─ @ben: Auth0 limitations and reviews (web search)

Phase 2: REDUCE
└─ @abby: Feature matrix, gap analysis
```

### Pattern: Best Practices Research

```
User Request: "What are best practices for rate limiting?"

Phase 1: FAN-OUT
├─ @ben: Industry rate limiting patterns (web search)
├─ @ben: Framework-specific implementations (web search)
├─ @ben: Current rate limiting in codebase
└─ @ben: Case studies and failure modes (web search)

Phase 2: REDUCE
└─ @abby: Best practices guide with recommendations
```

---

## Research Output Formats

### Investigation Report Template

```markdown
## Question

[Original question/request]

## Summary

[1-2 sentence answer]

## Evidence

1. [Finding 1 with file:line references]
2. [Finding 2 with file:line references]

## Analysis

[Interpretation of evidence]

## Recommendations

1. [Actionable recommendation]

## Open Questions

- [What wasn't answered]
```

### Task Management for Research

For research tasks, structure as exploration followed by synthesis:

```python
# Create research tasks
TaskCreate(subject="Define research scope", description="Clarify questions, identify sources...")
TaskCreate(subject="Explore area 1", description="Search for patterns in auth module...")
TaskCreate(subject="Explore area 2", description="Search for patterns in API layer...")
TaskCreate(subject="Explore area 3", description="Search for patterns in database...")
TaskCreate(subject="Synthesize findings", description="Aggregate discoveries, form conclusions...")

# Exploration can run in parallel, synthesis waits
TaskUpdate(taskId="2", addBlockedBy=["1"])
TaskUpdate(taskId="3", addBlockedBy=["1"])
TaskUpdate(taskId="4", addBlockedBy=["1"])
TaskUpdate(taskId="5", addBlockedBy=["2", "3", "4"])

# Spawn Explore agents in parallel
Task(subagent_type="@ben", prompt="TaskId 2: Find auth patterns...")
Task(subagent_type="@ben", prompt="TaskId 3: Find API patterns...")
Task(subagent_type="@ben", prompt="TaskId 4: Find database patterns...")
```

## Agent Selection for Research

**REMINDER: Only use @ben, @abby, or @oracle. See [SKILL.md](../../SKILL.md) for the full registry.**

| Research Type      | Primary Agent | Secondary Agent | Notes                          |
| ------------------ | ------------- | --------------- | ------------------------------ |
| Codebase questions | `@ben`        | `@abby`         | @ben explores, @abby synthesizes |
| External research  | `@ben`        | `@ben`          | @ben handles web search + local |
| Architecture       | `@abby`       | `@ben`          | @abby plans, @ben discovers    |
| Impact analysis    | `@ben`        | `@abby`         | @ben maps, @abby aggregates    |

---

```
─── ◈ Research ──────────────────────────
```
