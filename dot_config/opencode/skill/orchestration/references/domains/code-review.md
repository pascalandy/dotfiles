# Code Review Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Reviews should be thorough, fast, and actionable.         │
│   Parallel analysis. Unified feedback. Clear priorities.    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **AGENT REMINDER**: Only use `@ben`, `@abby`, or `@oracle`.
> See [SKILL.md](../../SKILL.md) for costs and task mapping.
> NEVER use `general`, `explore`, or invented agent names.

> **Load when**: PR review, security audit, performance review, architecture review, pre-merge validation
> **Common patterns**: Multi-Dimensional Analysis, OWASP-Parallel, Layer-by-Layer

## Table of Contents

1. [Pull Request Review](#pull-request-review)
2. [Security Audit](#security-audit)
3. [Performance Review](#performance-review)
4. [Architecture Review](#architecture-review)
5. [Pre-merge Validation](#pre-merge-validation)

---

## Pull Request Review

### Pattern: Multi-Dimensional Analysis

```
User Request: "Review PR #123"

Phase 1: FAN-OUT (Parallel analysis - @ben for context, @abby for review)
├─ @ben: Understand PR context, related issues
├─ @abby: Code quality analysis (style, patterns, DRY)
├─ @abby: Logic correctness (edge cases, error handling)
├─ @abby: Security implications
└─ @abby: Performance implications

Phase 2: REDUCE (Synthesize)
└─ @abby: Aggregate findings, prioritize, format review
```

**Implementation:**

```
# All in single message for parallelism
Task(subagent_type="@ben", prompt="Fetch PR #123 details, understand context and related issues")
Task(subagent_type="@abby", prompt="Review code quality: patterns, readability, maintainability")
Task(subagent_type="@abby", prompt="Review logic: correctness, edge cases, error handling")
Task(subagent_type="@abby", prompt="Review security: injection, auth, data exposure")
Task(subagent_type="@abby", prompt="Review performance: complexity, queries, memory")
```

### Pattern: Contextual Deep-Dive

```
Phase 1: PIPELINE (Understand)
├─ @ben: Get PR diff, commit messages
└─ @ben: Find related code, understand impact

Phase 2: FAN-OUT (File-by-file)
├─ @abby per changed file (for large PRs)

Phase 3: PIPELINE (Consolidate)
└─ @abby: Create cohesive review
```

---

## Security Audit

### Pattern: OWASP-Parallel

```
User Request: "Security audit the authentication module"

Phase 1: FAN-OUT (OWASP categories - parallel @abby tasks)
├─ @abby: Injection vulnerabilities (SQL, command, XSS)
├─ @abby: Authentication/session issues
├─ @abby: Access control problems
├─ @abby: Cryptographic weaknesses
├─ @abby: Data exposure risks
└─ @abby: Security misconfiguration

Phase 2: REDUCE
└─ @abby: Risk-ranked findings with remediation
```

### Pattern: Attack Surface Mapping

```
Phase 1: EXPLORE
└─ @ben: Map all entry points (APIs, forms, file uploads)

Phase 2: FAN-OUT (Per entry point)
├─ @abby per entry point: Analyze input validation, sanitization

Phase 3: PIPELINE
└─ @abby: Threat model, prioritized vulnerabilities
```

### Pattern: Dependency Audit

```
Phase 1: FAN-OUT (parallel @ben tasks)
├─ @ben: Scan npm/pip dependencies for CVEs
├─ @ben: Check for outdated packages
└─ @ben: Analyze transitive dependencies

Phase 2: REDUCE
└─ @abby: Prioritized upgrade plan
```

---

## Performance Review

### Pattern: Layer-by-Layer

```
User Request: "Find performance bottlenecks"

Phase 1: FAN-OUT (Analyze each layer - parallel @abby tasks)
├─ @abby: Database queries (N+1, missing indexes, slow queries)
├─ @abby: API layer (response times, payload sizes)
├─ @abby: Frontend (bundle size, render performance)
└─ @abby: Infrastructure (caching, connection pooling)

Phase 2: REDUCE
└─ @abby: Prioritized optimization roadmap
```

### Pattern: Hot Path Analysis

```
Phase 1: EXPLORE
└─ @ben: Identify critical user flows

Phase 2: PIPELINE (Per flow)
└─ @abby: Trace request lifecycle, find bottlenecks

Phase 3: FAN-OUT (Optimization)
├─ @abby per bottleneck: Implement optimization
```

### Pattern: Complexity Audit

```
Phase 1: MAP
└─ @ben: Find all functions, measure complexity

Phase 2: FAN-OUT (High complexity functions - parallel @abby tasks)
├─ @abby: Analyze function X, suggest optimizations
├─ @abby: Analyze function Y, suggest optimizations
└─ @abby: Analyze function Z, suggest optimizations
```

---

## Architecture Review

### Pattern: Multi-Stakeholder

```
User Request: "Review system architecture"

Phase 1: FAN-OUT (Perspectives - parallel @abby tasks)
├─ @abby: Scalability assessment
├─ @abby: Maintainability assessment
├─ @abby: Security architecture
├─ @abby: Cost efficiency
└─ @abby: Developer experience

Phase 2: REDUCE
└─ @abby: Synthesize into architecture decision record
```

### Pattern: Dependency Analysis

```
Phase 1: EXPLORE
└─ @ben: Map all module dependencies

Phase 2: FAN-OUT (parallel @ben tasks for analysis)
├─ @ben: Identify circular dependencies
├─ @ben: Find coupling hotspots
└─ @ben: Assess abstraction boundaries

Phase 3: PIPELINE
└─ @abby: Recommend architectural improvements
```

### Pattern: Standards Compliance

```
Phase 1: FAN-OUT (parallel @abby tasks)
├─ @abby: Check against SOLID principles
├─ @abby: Check against team style guide
├─ @abby: Check against industry patterns
└─ @abby: Check against regulatory requirements

Phase 2: REDUCE
└─ @abby: Compliance report with gaps
```

---

## Pre-merge Validation

### Pattern: Comprehensive Gate

```
User Request: "Validate PR ready for merge"

Phase 1: FAN-OUT (All checks in parallel - @ben tasks)
├─ @ben: Run full test suite
├─ @ben: Verify all review comments addressed
├─ @ben: Check for merge conflicts
├─ @ben: Validate documentation updated
└─ @ben: Confirm CI checks passing

Phase 2: REDUCE
└─ @abby: Go/no-go recommendation with blockers
```

### Pattern: Regression Check

```
Phase 1: EXPLORE
└─ @ben: Identify areas affected by changes

Phase 2: FAN-OUT (parallel @abby tasks)
├─ @abby: Test affected area 1
├─ @abby: Test affected area 2
└─ @abby: Integration test critical paths

Phase 3: PIPELINE
└─ @abby: Regression report
```

---

## Review Output Formats

### Structured Review Template

```markdown
## Summary

[1-2 sentence overview]

## Risk Assessment

- **Security**: Low/Medium/High
- **Performance**: Low/Medium/High
- **Breaking Changes**: Yes/No

## Must Fix (Blocking)

1. [Critical issue with line reference]

## Should Fix (Non-blocking)

1. [Important improvement]

## Consider (Optional)

1. [Nice-to-have suggestion]

## Positive Notes

- [What was done well]
```

### Task Management for Reviews

For comprehensive reviews, create parallel analysis tasks:

```python
# Create review tasks (can run in parallel)
TaskCreate(subject="Analyze PR context", description="Understand changes, related issues...")
TaskCreate(subject="Review code quality", description="Patterns, readability, maintainability...")
TaskCreate(subject="Check security", description="Injection, auth, data exposure...")
TaskCreate(subject="Assess performance", description="Complexity, queries, memory...")
TaskCreate(subject="Synthesize review", description="Aggregate findings into review...")

# Synthesis blocked by analysis tasks
TaskUpdate(taskId="5", addBlockedBy=["1", "2", "3", "4"])

# Spawn parallel agents for analysis
Task(subagent_type="@abby", prompt="TaskId 1: Analyze PR context...")
Task(subagent_type="@abby", prompt="TaskId 2: Review code quality...")
Task(subagent_type="@abby", prompt="TaskId 3: Check security...")
Task(subagent_type="@abby", prompt="TaskId 4: Assess performance...")
```

---

```
─── ◈ Code Review ───────────────────────
```
