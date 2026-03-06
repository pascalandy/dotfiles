# Documentation Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Good documentation is parallel-friendly.                  │
│   Multiple sections, generated simultaneously.              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **AGENT REMINDER**: Only use `@ben`, `@abby`, or `@oracle`.
> See [SKILL.md](../../SKILL.md) for costs and task mapping.
> In examples below, "Agent A/B/C" = parallel `@abby` tasks for writing or `@ben` for exploration.

> **Load when**: API documentation, code documentation, README generation, architecture docs, user guides
> **Common patterns**: Endpoint Discovery, Batch JSDoc Generation, Comprehensive README

## Table of Contents

1. [API Documentation](#api-documentation)
2. [Code Documentation](#code-documentation)
3. [README Generation](#readme-generation)
4. [Architecture Documentation](#architecture-documentation)
5. [User Guides](#user-guides)

---

## API Documentation

### Pattern: Endpoint Discovery and Documentation

```
User Request: "Document all REST API endpoints"

Phase 1: EXPLORE
└─ @ben: Find all route definitions

Phase 2: FAN-OUT (Parallel documentation - @ben tasks)
├─ @ben: Document auth endpoints
├─ @ben: Document user endpoints
├─ @ben: Document product endpoints
└─ @ben: Document order endpoints

Phase 3: REDUCE
└─ @abby: Compile into unified OpenAPI/Swagger spec
```

### Pattern: Request/Response Documentation

```
Phase 1: EXPLORE
└─ @ben: Find endpoint handlers and schemas

Phase 2: FAN-OUT (Per endpoint group - @ben tasks)
├─ @ben: Document request schemas, validation
├─ @ben: Document response schemas, status codes
└─ @ben: Document error responses

Phase 3: PIPELINE
└─ @abby: Generate examples, test payloads
```

### Pattern: Interactive Documentation

```
Phase 1: PIPELINE (Foundation)
├─ @ben: Extract all endpoints with types
└─ @abby: Generate OpenAPI spec

Phase 2: FAN-OUT (Enhancement - @ben tasks)
├─ @ben: Add example requests
├─ @ben: Add example responses
└─ @ben: Add authentication examples

Phase 3: PIPELINE
└─ @abby: Setup Swagger UI / Redoc
```

---

## Code Documentation

### Pattern: Batch JSDoc/Docstring Generation

```
User Request: "Add documentation to the utils module"

Phase 1: EXPLORE
└─ @ben: Find all undocumented functions

Phase 2: MAP (Parallel documentation - @ben tasks)
├─ @ben: Document file1.ts functions
├─ @ben: Document file2.ts functions
└─ @ben: Document file3.ts functions

Phase 3: PIPELINE
└─ @abby: Verify consistency, generate type docs
```

### Pattern: Complexity-Driven Documentation

```
Phase 1: EXPLORE
└─ @ben: Find complex functions (high cyclomatic complexity)

Phase 2: FAN-OUT (Prioritized - @ben tasks)
├─ @ben: Document most complex function
├─ @ben: Document second most complex
└─ @ben: Document third most complex

Each agent:
- Explain algorithm/logic
- Document edge cases
- Add usage examples
```

### Pattern: Module Overview Generation

```
Phase 1: EXPLORE
└─ @ben: Map module structure, exports, dependencies

Phase 2: PIPELINE
├─ @abby: Write module overview
├─ @abby: Document public API
└─ @abby: Add usage examples

Phase 3: FAN-OUT (Internal docs - @ben tasks)
├─ @ben: Document internal utilities
└─ @ben: Document configuration options
```

---

## README Generation

### Pattern: Comprehensive README

```
User Request: "Create a README for this project"

Phase 1: FAN-OUT (Parallel information gathering)
├─ @ben: Project structure and technologies
├─ @ben: Build and run scripts (package.json, Makefile)
├─ @ben: Environment variables and config
├─ @ben: Test setup and commands
└─ @ben: Existing docs and comments

Phase 2: REDUCE
└─ @abby: Synthesize into structured README

Sections:
- Overview and purpose
- Quick start
- Installation
- Configuration
- Usage examples
- Development setup
- Testing
- Contributing
```

### Pattern: README Update

```
Phase 1: FAN-OUT
├─ @ben: Current README content
├─ @ben: Recent changes to codebase
└─ @ben: New dependencies or features

Phase 2: PIPELINE
└─ @abby: Update README sections, maintain style
```

---

## Architecture Documentation

### Pattern: C4 Model Documentation

```
User Request: "Document the system architecture"

Phase 1: FAN-OUT (Parallel level documentation - @ben tasks)
├─ @ben: Context diagram (system + external actors)
├─ @ben: Container diagram (applications, data stores)
├─ @ben: Component diagram (internal components)
└─ @ben: Code diagram (critical classes/modules)

Phase 2: REDUCE
└─ @abby: Compile into architecture doc with diagrams
```

### Pattern: Decision Record Generation

```
Phase 1: EXPLORE
└─ @ben: Find architectural patterns in code

Phase 2: FAN-OUT (parallel @ben tasks)
├─ @ben: Document decision 1 (why this database?)
├─ @ben: Document decision 2 (why this framework?)
└─ @ben: Document decision 3 (why this structure?)

Each ADR includes:
- Context
- Decision
- Consequences
- Alternatives considered
```

### Pattern: Data Flow Documentation

```
Phase 1: EXPLORE
└─ @ben: Trace data through system

Phase 2: PIPELINE
├─ @abby: Document ingress points
├─ @abby: Document transformations
├─ @abby: Document storage
└─ @abby: Document egress points

Phase 3: REDUCE
└─ @abby: Create data flow diagram
```

---

## User Guides

### Pattern: Feature-Based Guides

```
User Request: "Write user documentation for the dashboard"

Phase 1: EXPLORE
└─ @ben: Map dashboard features and capabilities

Phase 2: FAN-OUT (Parallel feature guides - @ben tasks)
├─ @ben: Guide for feature 1 (with screenshots)
├─ @ben: Guide for feature 2
├─ @ben: Guide for feature 3
└─ @ben: Troubleshooting guide

Phase 3: REDUCE
└─ @abby: Compile into user manual with TOC
```

### Pattern: Tutorial Generation

```
Phase 1: EXPLORE
└─ @ben: Identify key user workflows

Phase 2: PIPELINE (Sequential tutorials)
├─ @abby: Getting started tutorial
├─ @abby: Basic usage tutorial
├─ @abby: Advanced usage tutorial
└─ @abby: Best practices guide
```

### Pattern: FAQ Generation

```
Phase 1: FAN-OUT
├─ @ben: Common patterns in issues/tickets
├─ @ben: Error messages and their causes
└─ @ben: Configuration gotchas

Phase 2: REDUCE
└─ @abby: Compile FAQ with clear answers
```

---

## Documentation Quality Patterns

### Pattern: Consistency Audit

```
Phase 1: FAN-OUT (parallel @ben tasks)
├─ @ben: Check terminology consistency
├─ @ben: Check formatting consistency
├─ @ben: Check example code validity
└─ @ben: Check link validity

Phase 2: REDUCE
└─ @abby: Inconsistency report with fixes
```

### Pattern: Freshness Check

```
Phase 1: FAN-OUT
├─ @ben: Find outdated code examples
├─ @ben: Find references to removed features
└─ @ben: Find mismatched version numbers

Phase 2: PIPELINE
└─ @abby: Update stale documentation
```

---

## Task Management for Documentation

Structure documentation work with parallel generation:

```python
# Create documentation tasks
TaskCreate(subject="Audit existing docs", description="Review current documentation state...")
TaskCreate(subject="Document API endpoints", description="REST API documentation...")
TaskCreate(subject="Document components", description="React component docs...")
TaskCreate(subject="Document utilities", description="Helper function docs...")
TaskCreate(subject="Review consistency", description="Ensure consistent style...")
TaskCreate(subject="Verify examples", description="Test all code examples...")

# Parallel doc generation after audit
TaskUpdate(taskId="2", addBlockedBy=["1"])
TaskUpdate(taskId="3", addBlockedBy=["1"])
TaskUpdate(taskId="4", addBlockedBy=["1"])
TaskUpdate(taskId="5", addBlockedBy=["2", "3", "4"])
TaskUpdate(taskId="6", addBlockedBy=["5"])

# Spawn parallel documentation agents
Task(subagent_type="@abby", prompt="TaskId 2: Document API endpoints...")
Task(subagent_type="@abby", prompt="TaskId 3: Document components...")
Task(subagent_type="@abby", prompt="TaskId 4: Document utilities...")
```

## Output Formats

| Doc Type     | Format              | Tool                   |
| ------------ | ------------------- | ---------------------- |
| API docs     | OpenAPI/Swagger     | YAML/JSON              |
| Code docs    | JSDoc/docstrings    | Inline                 |
| READMEs      | Markdown            | .md files              |
| Architecture | Markdown + diagrams | Mermaid/PlantUML       |
| User guides  | Markdown/HTML       | Static site generators |

---

```
─── ◈ Documentation ─────────────────────
```
