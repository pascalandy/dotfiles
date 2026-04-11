# Orchestration Tools Reference (OpenCode)

```
┌─────────────────────────────────────────────────────────────┐
│  Your toolkit for turning ambitious requests into reality.  │
│  Master these tools, and complex work becomes effortless.   │
└─────────────────────────────────────────────────────────────┘
```

## Table of Contents

1. [Tool Overview](#tool-overview)
2. [Task Tool (Agent Spawning)](#task-tool)
3. [Todo Tools (Task Tracking)](#todo-tools)
4. [Read Tool (Coordination)](#read-tool)
5. [Subagent Prompting Guide](#subagent-prompting-guide)
6. [Agent-Task Workflow](#agent-task-workflow)

---

## Tool Overview

### Orchestrator Tools (YOU use directly)

| Tool        | Purpose                                    |
|-------------|-------------------------------------------|
| `Task`      | Spawn worker agents (@ben, @abby, @oracle) |
| `TodoWrite` | Create and update task lists              |
| `TodoRead`  | Check current task status                 |
| `Read`      | Load references, guides, agent outputs    |
| `Skill`     | Load domain-specific skills               |

### Worker Tools (AGENTS use)

| Tool       | Purpose                    |
|------------|----------------------------|
| `Read`     | Read files for analysis    |
| `Write`    | Create new files           |
| `Edit`     | Modify existing files      |
| `Bash`     | Run shell commands         |
| `Glob`     | Find files by pattern      |
| `Grep`     | Search file contents       |
| `WebFetch` | Fetch web content          |

---

## Task Tool

Spawn an agent to handle work. This is how you delegate.

**Remember:** Subagents do NOT inherit skills. They only know what you tell them in the prompt. You are the conductor — they are the musicians.

### Parameters

| Parameter       | Required | Description                                      |
|-----------------|----------|--------------------------------------------------|
| `subagent_type` | Yes      | Agent type: `@ben`, `@abby`, or `@oracle`        |
| `prompt`        | Yes      | Detailed instructions for the agent              |
| `description`   | Yes      | Short 3-5 word summary                           |

### Parallel Agent Spawning

Launch multiple agents in a single message for parallel execution:

```python
# Multiple Task calls in one message = parallel execution
Task(subagent_type="@ben", description="Find auth patterns", prompt="...")
Task(subagent_type="@ben", description="Search API routes", prompt="...")
Task(subagent_type="@abby", description="Implement feature", prompt="...")
```

### Agent Selection (Cost-Aware)

**ONLY use these three agents. See [SKILL.md](../SKILL.md) for the full registry.**

| Task Complexity        | Agent     | Cost    | Why                          |
|------------------------|-----------|---------|------------------------------|
| Simple search/patterns | `@ben`    | ~$0.02  | Fast and cheap               |
| Standard exploration   | `@ben`    | ~$0.02  | Sufficient for most searches |
| Complex exploration    | `@abby`   | ~$0.50  | Needs reasoning              |
| Simple implementation  | `@ben`    | ~$0.02  | Pattern-based work           |
| Complex implementation | `@abby`   | ~$0.50  | Design decisions needed      |
| Architecture/planning  | `@abby`   | ~$0.50  | Complex trade-offs           |
| Security review        | `@abby`   | ~$0.50  | Careful analysis             |
| After 2 failures       | `@oracle` | ~$10.00 | Last resort only             |

### Parallelism Strategy

| Priority     | Approach                                       |
|--------------|------------------------------------------------|
| **Speed**    | Parallelize with @abby, accept higher cost     |
| **Cost**     | Sequential @ben where possible                 |
| **Balanced** | @ben for exploration, @abby for implementation |

---

## Todo Tools

Use `TodoWrite` and `TodoRead` to track multi-step work.

### TodoWrite

Create or update your task list:

```python
TodoWrite(todos=[
    {"id": "1", "content": "Explore auth patterns", "status": "completed", "priority": "high"},
    {"id": "2", "content": "Implement login route", "status": "in_progress", "priority": "high"},
    {"id": "3", "content": "Add tests", "status": "pending", "priority": "medium"}
])
```

### Task States

| Status        | Meaning                    |
|---------------|----------------------------|
| `pending`     | Not yet started            |
| `in_progress` | Currently working on       |
| `completed`   | Done                       |
| `cancelled`   | No longer needed           |

### TodoRead

Check current task status (no parameters needed).

---

## Read Tool

Use `Read` for coordination work:

```
┌─────────────────────────────────────────────────────────────┐
│  YOU read directly (1-2 files max):                         │
│                                                             │
│  • Skill references (MANDATORY - never delegate these)     │
│  • Domain guides from references/domains/                  │
│  • Quick index lookups (package.json, AGENTS.md, etc.)     │
│  • Agent output to synthesize results                      │
│                                                             │
│  DELEGATE to agents (3+ files):                            │
│                                                             │
│  • Exploring codebases                                      │
│  • Reading multiple source files                           │
│  • Deep documentation analysis                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Rule of thumb:** If you're about to read more than 2 files, spawn an agent instead.

---

## Subagent Prompting Guide

Your agents are only as good as your prompts. Invest in clear instructions.

### The WORKER Preamble (Required)

**Every agent prompt MUST start with this preamble:**

```
CONTEXT: You are a WORKER agent, not an orchestrator.

RULES:
- Complete ONLY the task described below
- Use tools directly (Read, Write, Edit, Bash, etc.)
- Do NOT spawn sub-agents
- Do NOT manage todos (orchestrator handles that)
- Report your results with absolute file paths

TASK:
[Your specific task here]
```

### The Five Elements

After the preamble, include:

```
┌─────────────────────────────────────────────────────────────┐
│  1. PREAMBLE   → WORKER context and rules (required!)       │
│  2. CONTEXT    → What's the bigger picture?                 │
│  3. SCOPE      → What exactly should this agent do?         │
│  4. CONSTRAINTS → What rules or patterns to follow?         │
│  5. OUTPUT     → What should the agent return?              │
└─────────────────────────────────────────────────────────────┘
```

### Example: Implementation Prompt (@abby)

```
CONTEXT: You are a WORKER agent, not an orchestrator.

RULES:
- Complete ONLY the task described below
- Use tools directly (Read, Write, Edit, Bash, etc.)
- Do NOT spawn sub-agents
- Do NOT manage todos (orchestrator handles that)
- Report your results with absolute file paths

TASK:
Create server/src/routes/auth.js with:
- POST /signup - Create user, hash password with bcrypt, return JWT
- POST /login - Verify credentials, return JWT

CONTEXT: Building a Todo app with Express backend and SQLite.
The users table exists in server/src/db/database.js.

CONSTRAINTS:
- Use the existing db from database.js
- JWT secret from process.env.JWT_SECRET
- Follow existing code patterns

RETURN: Confirm files created and summarize implementation.
```

### Example: Exploration Prompt (@ben)

```
CONTEXT: You are a WORKER agent, not an orchestrator.

RULES:
- Complete ONLY the task described below
- Use tools directly (Read, Write, Edit, Bash, etc.)
- Do NOT spawn sub-agents
- Do NOT manage todos (orchestrator handles that)
- Report your results with absolute file paths

TASK:
Find all files related to user authentication.

Look for:
- Route handlers for login/signup/logout
- Middleware that checks authentication
- Session or token management
- User model or schema

RETURN: List of files with brief description of each.
```

### Prompt Anti-Patterns

| Bad                  | Problem           | Good                                                |
|----------------------|-------------------|-----------------------------------------------------|
| "Fix the bug"        | Which bug? Where? | "Fix the 401 error after password reset in auth.js" |
| "Build the frontend" | Too broad         | Split into: components, routing, state, API         |
| "Implement auth"     | No constraints    | Specify: framework, token type, file locations      |
| "Check the code"     | No focus          | "Review for SQL injection, return severity ratings" |

### Scoping Work

| Scope                    | Approach             |
|--------------------------|----------------------|
| 1 file                   | One agent            |
| 2-3 related files        | One agent            |
| Multiple unrelated files | Parallel agents      |
| Full feature (5+ files)  | Decompose into tasks |

---

## Agent-Task Workflow

The complete flow for orchestrated execution:

```
┌─────────────────────────────────────────────────────────────┐
│  1. PLAN                                                    │
│     TodoWrite → create task list with priorities            │
│                                                             │
│  2. SPAWN PARALLEL AGENTS                                   │
│     Task(@ben, ...) Task(@ben, ...) Task(@abby, ...)       │
│     Multiple calls in ONE message = parallel                │
│                                                             │
│  3. UPDATE PROGRESS                                         │
│     TodoWrite → mark tasks in_progress / completed          │
│                                                             │
│  4. SYNTHESIZE                                              │
│     Read agent outputs, weave into response                 │
│                                                             │
│  5. REPEAT                                                  │
│     More work? Spawn more agents. Update todos.             │
└─────────────────────────────────────────────────────────────┘
```

### Example Flow

```python
# 1. Plan
TodoWrite(todos=[
    {"id": "1", "content": "Setup database schema", "status": "in_progress", "priority": "high"},
    {"id": "2", "content": "Implement auth routes", "status": "pending", "priority": "high"},
    {"id": "3", "content": "Build auth middleware", "status": "pending", "priority": "high"}
])

# 2. Spawn agent for first task
Task(subagent_type="@abby",
     description="Setup database",
     prompt="CONTEXT: You are a WORKER agent...
     TASK: Create SQLite database with users table...")

# 3. When agent completes, update todos
TodoWrite(todos=[
    {"id": "1", "content": "Setup database schema", "status": "completed", "priority": "high"},
    {"id": "2", "content": "Implement auth routes", "status": "in_progress", "priority": "high"},
    {"id": "3", "content": "Build auth middleware", "status": "pending", "priority": "high"}
])

# 4. Spawn next agent...
Task(subagent_type="@abby",
     description="Implement auth",
     prompt="...")
```

---

## Best Practices Summary

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  ✓ Launch multiple agents in single message (parallel)      │
│  ✓ Use TodoWrite to track progress visibly                  │
│  ✓ Rich, detailed prompts for agents                        │
│  ✓ Mark tasks completed immediately when done               │
│  ✓ Read skill references yourself (never delegate)          │
│                                                             │
│  ✗ Never use general or explore agents                      │
│  ✗ Never run independent work sequentially                  │
│  ✗ Never give vague prompts to agents                       │
│  ✗ Never read 3+ files yourself (spawn agent)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

```
─── ◈ Tools Reference Complete ──────────────────
```
