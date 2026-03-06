# Software Development Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Building software is what we do best.                     │
│   Features, fixes, refactors — all orchestrated elegantly.  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **AGENT REMINDER**: Only use `@ben`, `@abby`, or `@oracle`.
> See [SKILL.md](../../SKILL.md) for costs and task mapping.
> NEVER use `general`, `explore`, or invented agent names.

> **Load when**: Feature implementation, bug fixes, refactoring, migrations, greenfield development
> **Common patterns**: Plan-Parallel-Integrate, Diagnose-Hypothesize-Fix, Map-Analyze-Transform

## Table of Contents

1. [Feature Implementation](#feature-implementation)
2. [Bug Fixing](#bug-fixing)
3. [Refactoring](#refactoring)
4. [Migration](#migration)
5. [Greenfield Development](#greenfield-development)

---

## Feature Implementation

### Pattern: Plan-Parallel-Integrate

```
User Request: "Add user authentication"

Phase 1: PIPELINE (Research → Plan)
├─ @ben: Find existing auth patterns, user models, middleware
└─ @abby: Design auth architecture using findings

Phase 2: FAN-OUT (Parallel @abby tasks)
├─ @abby: Implement user model + database schema
├─ @abby: Implement JWT/session middleware
├─ @abby: Implement login/logout routes
└─ @abby: Implement frontend auth components

Phase 3: PIPELINE (Integration)
└─ @abby: Wire components, add tests, verify flow
```

**Task breakdown:**

```
TaskCreate("Design authentication architecture")
TaskCreate("Implement user model and schema")
TaskCreate("Build auth middleware")
TaskCreate("Create auth API routes")
TaskCreate("Build frontend auth UI")
TaskCreate("Integration testing")

# Dependencies
Task 2-5 blocked by Task 1
Task 6 blocked by Tasks 2-5
```

### Pattern: Vertical Slice

For full-stack features, implement one complete slice first:

```
Phase 1: Single complete flow
└─ @abby: DB → API → UI for one use case

Phase 2: FAN-OUT expansion (parallel @abby tasks)
├─ @abby: Additional DB operations
├─ @abby: Additional API endpoints
└─ @abby: Additional UI components
```

---

## Bug Fixing

### Pattern: Diagnose-Hypothesize-Fix

```
User Request: "Users can't log in after password reset"

Phase 1: FAN-OUT (Parallel Diagnosis)
├─ @ben: Search error logs, recent changes to auth
├─ @ben: Find password reset flow implementation
└─ @ben: Check session/token handling

Phase 2: PIPELINE (Analysis)
└─ @abby: Synthesize findings, form hypotheses

Phase 3: SPECULATIVE (If cause unclear - parallel @abby tasks)
├─ @abby: Test hypothesis 1 (token expiry issue)
├─ @abby: Test hypothesis 2 (session invalidation)
└─ @abby: Test hypothesis 3 (password hash mismatch)

Phase 4: PIPELINE
└─ @abby: Implement fix, add regression test
```

### Pattern: Reproduction-First

```
Phase 1: Reproduce
└─ @abby: Create minimal reproduction case

Phase 2: Bisect (if needed)
└─ @ben: Git bisect to find breaking commit

Phase 3: Fix
└─ @abby: Implement and verify fix
```

---

## Refactoring

### Pattern: Map-Analyze-Transform

```
User Request: "Refactor callback-based code to async/await"

Phase 1: MAP (Find all instances)
└─ @ben: Find all callback patterns in codebase

Phase 2: FAN-OUT (Analyze impact - parallel @ben tasks)
├─ @ben: Analyze module A dependencies
├─ @ben: Analyze module B dependencies
└─ @ben: Analyze module C dependencies

Phase 3: PIPELINE (Safe transformation)
├─ @abby: Design migration order (leaf nodes first)
└─ @abby: Transform files in dependency order
```

### Pattern: Strangler Fig

For large refactors, wrap old with new:

```
Phase 1: Create parallel implementation (@abby tasks)
├─ @abby: Build new abstraction layer
└─ @abby: Implement new pattern alongside old

Phase 2: Gradual migration
└─ @abby: Migrate consumers one by one

Phase 3: Cleanup
└─ @abby: Remove old implementation
```

---

## Migration

### Pattern: Schema-Data-Code

```
User Request: "Migrate from MongoDB to PostgreSQL"

Phase 1: FAN-OUT (Analysis)
├─ @ben: Document all MongoDB schemas
├─ @ben: Find all database queries
└─ @ben: Identify data transformation needs

Phase 2: PIPELINE (Schema)
└─ @abby: Create PostgreSQL schemas, migrations

Phase 3: FAN-OUT (Code updates - parallel @abby tasks)
├─ @abby: Update user-related queries
├─ @abby: Update product-related queries
└─ @abby: Update order-related queries

Phase 4: PIPELINE (Data migration)
└─ @abby: Write and run data migration scripts
```

### Pattern: Version Upgrade

```
User Request: "Upgrade React from v17 to v18"

Phase 1: EXPLORE
└─ @ben: Find breaking changes, deprecated APIs used

Phase 2: MAP-REDUCE (parallel @abby tasks)
├─ @abby: Update component files batch 1
├─ @abby: Update component files batch 2
└─ @abby: Update component files batch 3
→ Aggregate: Collect all breaking changes found

Phase 3: PIPELINE
├─ @abby: Fix breaking changes
└─ @ben: Run full test suite
```

---

## Greenfield Development

### Pattern: Scaffold-Parallel-Integrate

```
User Request: "Build a REST API for task management"

Phase 1: PIPELINE (Foundation)
├─ @abby: Design API architecture, endpoints, data models
└─ @abby: Scaffold project, setup tooling

Phase 2: FAN-OUT (Core features - parallel @abby tasks)
├─ @abby: User management (model, routes, auth)
├─ @abby: Task CRUD operations
├─ @abby: Project/workspace management
└─ @abby: Shared middleware, utilities

Phase 3: FAN-OUT (Cross-cutting - mix of @abby and @ben)
├─ @abby: Error handling, validation
├─ @abby: Logging, monitoring setup
└─ @ben: API documentation

Phase 4: PIPELINE (Polish)
└─ @abby: Integration tests, final wiring
```

### Pattern: MVP-First

```
Phase 1: Minimal viable implementation
└─ @abby: End-to-end flow, minimal features

Phase 2: BACKGROUND (Feedback loop)
├─ User testing while...
└─ @ben prepares next features (background)

Phase 3: FAN-OUT (Feature expansion)
├─ Multiple @abby agents expand different features in parallel
```

---

## Task Management Integration

For any software development task, create explicit tasks:

```python
# Decompose the work
TaskCreate(subject="Analyze requirements", description="Understand codebase patterns, existing code...")
TaskCreate(subject="Design approach", description="Plan implementation strategy...")
TaskCreate(subject="Implement core functionality", description="Build the main feature...")
TaskCreate(subject="Add error handling", description="Handle edge cases, validation...")
TaskCreate(subject="Write tests", description="Unit and integration tests...")

# Set dependencies
TaskUpdate(taskId="2", addBlockedBy=["1"])  # Design after analysis
TaskUpdate(taskId="3", addBlockedBy=["2"])  # Implement after design
TaskUpdate(taskId="4", addBlockedBy=["3"])  # Error handling after core
TaskUpdate(taskId="5", addBlockedBy=["3"])  # Tests can parallel with error handling

# Spawn agents for unblocked tasks
Task(subagent_type="@abby", prompt="TaskId 1: Analyze requirements...")
```

Agents mark tasks resolved immediately upon completion.

---

```
─── ◈ Software Development ─────────────
```
