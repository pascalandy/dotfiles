# Project Management Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Complex projects, clearly decomposed.                     │
│   Dependencies tracked. Progress visible. Team aligned.     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **AGENT REMINDER**: Only use `@ben`, `@abby`, or `@oracle`.
> See [SKILL.md](../../SKILL.md) for costs and task mapping.
> In examples below, "Agent A/B/C" = parallel `@abby` tasks for planning or `@ben` for gathering info.

> **Load when**: Epic breakdown, sprint planning, progress tracking, dependency management, team coordination
> **Common patterns**: Hierarchical Decomposition, Capacity-Based Planning, Multi-Dimension Status

## Table of Contents

1. [Epic Breakdown](#epic-breakdown)
2. [Sprint Planning](#sprint-planning)
3. [Progress Tracking](#progress-tracking)
4. [Dependency Management](#dependency-management)
5. [Team Coordination](#team-coordination)

---

## Epic Breakdown

### Pattern: Hierarchical Decomposition

```
User Request: "Break down the authentication epic"

Phase 1: EXPLORE
└─ @ben: Understand requirements, existing system

Phase 2: PLAN
└─ @abby: Design high-level feature breakdown

Phase 3: FAN-OUT (Parallel story creation - @ben tasks)
├─ @ben: User stories for login/logout
├─ @ben: User stories for registration
├─ @ben: User stories for password management
├─ @ben: User stories for session management
└─ @ben: User stories for OAuth integration

Phase 4: REDUCE
└─ @abby: Organize into coherent backlog
```

**Task Management Implementation:**

```
# Create epic
TaskCreate(subject="Epic: User Authentication", description="Complete auth system")

# Create stories
TaskCreate(subject="Story: Login flow", description="...")
TaskCreate(subject="Story: Registration", description="...")
TaskCreate(subject="Story: Password reset", description="...")

# Set dependencies
TaskUpdate(taskId="3", addBlockedBy=["2"])  # Reset after registration
```

### Pattern: Vertical Slice Breakdown

```
Phase 1: EXPLORE
└─ @ben: Map feature touchpoints (UI, API, DB)

Phase 2: FAN-OUT (Slice by user value - @ben tasks)
├─ @ben: Define slice 1 (minimal viable feature)
├─ @ben: Define slice 2 (enhanced feature)
└─ @ben: Define slice 3 (complete feature)

Phase 3: PIPELINE
└─ @abby: Estimate, prioritize, sequence
```

### Pattern: Spike-First Breakdown

```
Phase 1: EXPLORE
└─ @ben: Identify unknowns and risks

Phase 2: FAN-OUT (Parallel spikes - @ben tasks)
├─ @ben: Technical spike - feasibility
├─ @ben: Technical spike - performance
└─ @ben: UX spike - user research

Phase 3: REDUCE
└─ @abby: Use spike findings to refine breakdown
```

---

## Sprint Planning

### Pattern: Capacity-Based Planning

```
User Request: "Plan the next sprint"

Phase 1: FAN-OUT (Gather context)
├─ @ben: Review backlog priority
├─ @ben: Check team capacity
├─ @ben: Review blockers and dependencies
└─ @ben: Check carryover from last sprint

Phase 2: REDUCE
└─ @abby: Propose sprint scope

Phase 3: FAN-OUT (Task breakdown - @ben tasks)
├─ @ben: Break down story 1 into tasks
├─ @ben: Break down story 2 into tasks
└─ @ben: Break down story 3 into tasks

Phase 4: PIPELINE
└─ @abby: Finalize sprint backlog
```

**Task Structure:**

```
# Sprint-level task
TaskCreate(subject="Sprint 14: Auth Implementation", description="...")

# Stories within sprint
TaskCreate(subject="Login API endpoint", description="...")
TaskCreate(subject="Login UI component", description="...")
TaskUpdate(taskId="2", addBlockedBy=["1"])  # UI needs API first

# Sub-tasks
TaskCreate(subject="Write login validation", description="...")
TaskCreate(subject="Add rate limiting", description="...")
```

### Pattern: Risk-Adjusted Planning

```
Phase 1: FAN-OUT (parallel @ben tasks)
├─ @ben: Identify technical risks
├─ @ben: Identify dependency risks
└─ @ben: Identify scope risks

Phase 2: REDUCE
└─ @abby: Adjust estimates with risk buffer

Phase 3: PIPELINE
└─ @abby: Create contingency tasks
```

---

## Progress Tracking

### Pattern: Multi-Dimension Status

```
User Request: "What's the project status?"

Phase 1: FAN-OUT (Parallel status gathering - @ben tasks)
├─ @ben: Task completion status (from TaskList)
├─ @ben: Blocker analysis
├─ @ben: Timeline vs plan
├─ @ben: Quality metrics
└─ @ben: Risk status

Phase 2: REDUCE
└─ @abby: Executive status summary
```

**Using TaskList:**

```
# Get current state
TaskList()  # Returns all tasks with status

# Update progress
TaskUpdate(taskId="5", addComment={
  author: "agent-id",
  content: "50% complete, blocked on API review"
})

# Mark complete
TaskUpdate(taskId="5", status="resolved")
```

### Pattern: Burndown Tracking

```
Phase 1: EXPLORE
└─ @ben: Calculate completed vs remaining work

Phase 2: PIPELINE
├─ @abby: Project completion trajectory
├─ @abby: Identify velocity trends
└─ @abby: Flag at-risk items

Phase 3: REDUCE
└─ @abby: Burndown report
```

### Pattern: Blocker Resolution

```
Phase 1: EXPLORE
└─ @ben: Identify all blocked tasks

Phase 2: FAN-OUT (Parallel resolution paths - @ben tasks)
├─ @ben: Investigate blocker 1
├─ @ben: Investigate blocker 2
└─ @ben: Investigate blocker 3

Phase 3: REDUCE
└─ @abby: Resolution plan, escalation needs
```

---

## Dependency Management

### Pattern: Dependency Graph Construction

```
User Request: "Map project dependencies"

Phase 1: EXPLORE
└─ @ben: List all tasks and their relationships

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Map technical dependencies
├─ @ben: Map team/resource dependencies
└─ @ben: Map external dependencies

Phase 3: REDUCE
└─ @abby: Dependency graph, critical path
```

**Implementation:**

```
# Create dependency chain
TaskCreate(subject="Database schema", description="...")
TaskCreate(subject="API models", description="...")
TaskCreate(subject="API endpoints", description="...")
TaskCreate(subject="Frontend integration", description="...")

TaskUpdate(taskId="2", addBlockedBy=["1"])
TaskUpdate(taskId="3", addBlockedBy=["2"])
TaskUpdate(taskId="4", addBlockedBy=["3"])

# Cross-team dependency
TaskCreate(subject="External API access", description="Waiting on partner")
TaskUpdate(taskId="3", addBlockedBy=["5"])  # Blocked by external
```

### Pattern: Critical Path Analysis

```
Phase 1: EXPLORE
└─ @ben: Map all task dependencies

Phase 2: PIPELINE
├─ @abby: Calculate path lengths
├─ @abby: Identify critical path
└─ @abby: Find parallel opportunities

Phase 3: REDUCE
└─ @abby: Optimization recommendations
```

### Pattern: Dependency Resolution

```
Phase 1: FAN-OUT (parallel @ben tasks)
├─ @ben: Identify circular dependencies
├─ @ben: Identify unnecessary dependencies
└─ @ben: Identify dependency bottlenecks

Phase 2: PIPELINE
└─ @abby: Restructure to unblock work
```

---

## Team Coordination

### Pattern: Work Distribution

```
User Request: "Assign work for this sprint"

Phase 1: FAN-OUT
├─ @ben: Analyze task requirements
├─ @ben: Review team skills/capacity
└─ @ben: Check current assignments

Phase 2: REDUCE
└─ @abby: Optimal assignment recommendations

Phase 3: FAN-OUT (Parallel task assignment - @ben tasks)
├─ @ben: Create task assignments for dev 1
├─ @ben: Create task assignments for dev 2
└─ @ben: Create task assignments for dev 3
```

### Pattern: Handoff Coordination

```
Phase 1: EXPLORE
└─ @ben: Identify tasks requiring handoffs

Phase 2: PIPELINE
├─ @abby: Document handoff requirements
├─ @abby: Create handoff checklist
└─ @abby: Schedule coordination points
```

### Pattern: Multi-Team Sync

```
Phase 1: FAN-OUT (parallel @ben tasks)
├─ @ben: Gather Team A status
├─ @ben: Gather Team B status
└─ @ben: Identify cross-team dependencies

Phase 2: REDUCE
└─ @abby: Cross-team status, blockers, needs
```

---

## Task Management in Practice

All project management work should use TaskCreate for proper tracking:

```python
# Sprint planning example
TaskCreate(subject="Sprint 14 Planning", description="Plan next sprint scope...")
TaskCreate(subject="Review backlog", description="Prioritize stories...")
TaskCreate(subject="Break down Story A", description="Create implementation tasks...")
TaskCreate(subject="Break down Story B", description="Create implementation tasks...")
TaskCreate(subject="Set dependencies", description="Wire task dependencies...")
TaskCreate(subject="Assign work", description="Distribute to team...")

# Planning sequence
TaskUpdate(taskId="2", addBlockedBy=["1"])
TaskUpdate(taskId="3", addBlockedBy=["2"])
TaskUpdate(taskId="4", addBlockedBy=["2"])
TaskUpdate(taskId="5", addBlockedBy=["3", "4"])
TaskUpdate(taskId="6", addBlockedBy=["5"])

# Parallel breakdown
Task(subagent_type="@abby", prompt="TaskId 3: Break down Story A...")
Task(subagent_type="@abby", prompt="TaskId 4: Break down Story B...")
```

## Best Practices

1. **Break down early** - Large tasks are hard to track
2. **Set dependencies explicitly** - Prevents blocked work
3. **Update status frequently** - Real-time visibility
4. **Comment on blockers** - Context for resolution
5. **Close completed tasks immediately** - Accurate progress

---

```
─── ◈ Project Management ────────────────
```
