---
name: byterover
description: Use when repo-specific memory, prior decisions, postmortems, or hard-to-know project details may change the work. Use `brv query` to retrieve memory and `brv curate` to preserve durable learnings. Skip it for routine work where memory lookup would add noise.
---

# byterover

Use `brv` as a thin project-memory tool.

Core operations:
- `brv query`: retrieve relevant context from `.brv/context-tree/`
- `brv curate`: save durable decisions, patterns, and lessons
- `brv review`: inspect and approve or reject pending curate operations when needed

## Use It When

- Repo memory is likely to change the implementation
- Prior decisions, conventions, or postmortems may matter
- The user asks you to remember, recall, or recover context
- You are resuming work after context loss or across sessions

## Skip It When

- The task is routine and fully specified already
- The needed information is already in the prompt or nearby files
- Running memory lookup would add noise without changing the outcome

## Core Workflow

1. Query only when memory is likely to matter.
2. Do the work using the retrieved context if it changes the implementation.
3. Curate only if the result adds durable project knowledge.
4. If curate creates pending review operations, inspect them before acting.

## Commands

### Query

Use `brv query` to retrieve project memory.

```bash
brv query "How is authentication implemented?"
```

Use query for:
- Prior decisions
- Project conventions
- User preferences worth reusing
- Postmortem lessons and non-obvious gotchas

Do not query by default on every task.

### Curate

Use `brv curate` to preserve durable knowledge after meaningful work.

```bash
brv curate "Auth uses JWT with 24h expiry. Tokens stored in httpOnly cookies via authMiddleware.ts"
```

Include up to 5 relevant project files when they improve the saved memory:

```bash
brv curate "Authentication middleware details" -f src/middleware/auth.ts
```

Curate when the change introduces:
- A decision others will need later
- A reusable implementation pattern
- A lesson from a bug, failure, or postmortem
- A user preference that should persist across sessions

Do not curate transient status, routine edits, or facts already stored unchanged.

### Review

If curate reports pending operations, inspect them with:

```bash
brv review pending
```

Always ask the user before approving or rejecting critical changes.

## Rule Of Thumb

`byterover` is for memory that changes execution, not for day-to-day ceremony.

## Optional Details

Load `references/DETAILS.md` only when you need setup, provider verification, troubleshooting, project locations, or `brv vc` version-control details.
