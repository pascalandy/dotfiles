---
name: commit
description: "Faire des commits atomiques (split + staging ciblé); à charger avant toute opération git commit."
---

# Skill: Commit

Create **truly atomic commits** — one logical change per commit, no exceptions.

## Core Principle: Atomicity First

> **An atomic commit contains exactly ONE logical change that can be described in a single sentence without using "and".**

If you need the word "and" to describe what a commit does, it should be split into multiple commits.

## Rules

- **Do not push by default** — Let the user review their commits first
- Only push when the user explicitly asks
- **NEVER combine unrelated changes** in a single commit
- **ALWAYS analyze and split** before committing
- **ALWAYS use the commit body** for non-trivial commits — the body explains the "why", the impact, and provides context for future readers. Only trivial changes (typo fixes, formatting) may use a minimal body.

---

## Mandatory Process

### Step 1: Analyze All Changes

Run `git status` and `git diff --stat` to identify all modified files.

### Step 2: Group by Logical Change

Categorize each change into logical groups. A logical group is:

- Changes that serve **one single purpose**
- Changes that would be **reverted together**
- Changes that have **one commit type**

### Step 3: Identify Split Points

**MUST SPLIT when changes involve:**

| Situation                                       | Action                    |
| ----------------------------------------------- | ------------------------- |
| Different purposes (delete old + add new)       | Separate commits          |
| Different file types (code + docs)              | Separate commits          |
| Different features                              | Separate commits          |
| Different commit types (feat vs docs vs remove) | Separate commits          |
| Unrelated directories                           | Consider separate commits |

### Step 4: Commit Sequentially

For each logical group:

1. Stage ONLY files for that group: `git add <specific-files>`
2. Commit with appropriate message (including body if necessary)
3. Repeat for next group

---

## Atomicity Decision Tree

```
Is this change describable in ONE sentence without "and"?
├── YES → Single commit OK
└── NO → MUST SPLIT
    │
    Ask: "What are the distinct actions?"
    │
    For each distinct action:
    └── Create separate commit
```

## Split Examples

### ❌ BAD: Combined Commit

```
📚 docs: Remove old docs directory and update README with new section
```

### ✅ GOOD: Atomic Commits (in order)

```
🧹 remove: Delete deprecated /docs directory
📚 docs: Add installation section to README
```

### ✅ GOOD: Atomic Commit with Body

```
✨ feat: dufuddle (cli): enhance CLI with Bun best practices

- File(s) changed:
  - WORKDIR/dufuddle/dufuddle.ts
- Nature of changes: Enhancement
- Purpose: Modernize the CLI using Bun idioms and improve robustness
- Impact: Better terminal UX, prevents blocking by servers, and adds timeout control
```

### ❌ BAD: Mixed Changes

```
✨ feat: Add user dashboard and fix login bug and update config
```

### ✅ GOOD: Atomic Commits (in order)

```
🚑 fix: Resolve null pointer in login validation
🧑‍💻 chore: Update database config for production
✨ feat: Add user dashboard with activity summary
```

---

## Staging Strategy for Splits

When you have multiple logical changes in the working directory:

```bash
# First commit: Remove deprecated docs
git add docs/old-directory/
git commit -m "🧹 remove: Delete deprecated /docs/old-directory"

# Second commit: Update README
git add README.md
git commit -m "📚 docs: Add installation section to README"
```

**Never use `git add .` or `git add -A` when splitting commits.**

---

## Commit Types

| Emoji | Type       | Description                                       |
| ----- | ---------- | ------------------------------------------------- |
| ✨    | `feat`     | New features, changes in existing functionality   |
| 🧑‍💻    | `chore`    | Tooling, configuration, maintenance               |
| 📚    | `docs`     | Documentation changes                             |
| 🎨    | `style`    | Code formatting, missing semicolons, etc.         |
| 🧪    | `test`     | Adding or correcting tests                        |
| ♻️    | `refactor` | Code restructuring without changing functionality |
| 🧹    | `remove`   | Removing code, features, or files                 |
| 🚑    | `fix`      | Bug fixes                                         |
| ⚡️    | `perf`     | Performance improvements                          |
| 🚧    | `wip`      | Work in progress                                  |
| 🔒    | `security` | Security improvements                             |

## Message Format

```
<emoji> <type>: <scope> (<context>): <imperative description>

- File(s) changed:
  - path/to/file1.ts
  - path/to/file2.ts
- Nature of changes: <what kind of work was done>
- Purpose: <why this change was made>
- Impact: <what effect this has on users/system/codebase>
```

- **Subject line**: imperative mood ("Add feature" not "Added feature"), under 72 characters
- **Scope**: the affected module, component, or area (e.g., `auth`, `dashboard`, `api`)
- **Context** (optional): additional categorization like `skill`, `ui`, `backend`
- **Body**: adapt to context — simple changes may only need 1-2 fields, complex changes should include all relevant fields
- **No periods** at the end of body lines

---

## Commit Body Guidelines

The subject line answers **"what changed?"** — the body answers **"why does it matter?"**

### When to include each field

| Field                 | When to use                                                                           |
| --------------------- | ------------------------------------------------------------------------------------- |
| **File(s) changed**   | Multi-file commits, or when the path isn't obvious from context                       |
| **Nature of changes** | Always helpful — categorizes the work (bug fix, refactor, new feature, cleanup, etc.) |
| **Purpose**           | Always — the human-readable "why" behind the change                                   |
| **Impact**            | When the change affects UX, performance, behavior, or other developers                |

### Flexibility

Adapt the body to the commit's complexity:

- **Trivial** (typo, formatting): Body optional or minimal
- **Simple** (single-file fix): 1-2 fields
- **Complex** (multi-file feature, refactor): All fields recommended

### Think about future readers

Someone reading `git log` in 6 months should understand:

1. What was changed
2. Why it was changed
3. What impact it has

If your commit message doesn't answer these questions, add more context.

---

## Examples

### Feature

```
✨ feat: dashboard (ui): add real-time activity feed widget

- File(s) changed:
  - src/components/Dashboard/ActivityFeed.tsx
  - src/hooks/useActivityStream.ts
- Nature of changes: New feature implementation
- Purpose: Give users visibility into recent actions on their account
- Impact: Improved engagement and transparency for end users
```

### Bug Fix

```
🚑 fix: auth: resolve session timeout on idle users

- File(s) changed:
  - src/services/auth.ts
- Nature of changes: Bug fix
- Purpose: Prevent users from being logged out unexpectedly after 5 minutes of inactivity
- Impact: Better UX for users who leave tabs open
```

### Refactoring

```
♻️ refactor: api: extract payment logic into dedicated service

- File(s) changed:
  - src/services/payment.ts
  - src/controllers/checkout.ts
  - src/utils/stripe.ts
- Nature of changes: Code restructuring
- Purpose: Improve maintainability by isolating payment concerns
- Impact: Easier testing and future payment provider changes
```

### Removal

```
🧹 remove: legacy: delete deprecated v1 API endpoints

- File(s) changed:
  - src/routes/v1/
  - src/controllers/legacy/
- Nature of changes: Cleanup
- Purpose: Remove unused code after v2 migration completed
- Impact: Reduced codebase size and maintenance burden
```

### Documentation

```
📚 docs: readme: add installation instructions for Windows

- File(s) changed:
  - README.md
- Nature of changes: Documentation update
- Purpose: Help Windows users get started without friction
- Impact: Broader accessibility for contributors
```

### Maintenance

```
🧑‍💻 chore: deps: update dependencies to latest versions

- File(s) changed:
  - package.json
  - bun.lock
- Nature of changes: Maintenance
- Purpose: Keep dependencies current and address security advisories
- Impact: Improved security posture and access to latest features
```

### Test

```
🧪 test: auth: add unit tests for session management

- File(s) changed:
  - src/services/__tests__/auth.test.ts
- Nature of changes: Test coverage
- Purpose: Ensure session timeout logic is properly validated
- Impact: Higher confidence in auth reliability during refactoring
```

### Performance

```
⚡️ perf: api: optimize database queries for user listing

- File(s) changed:
  - src/repositories/user.ts
- Nature of changes: Performance optimization
- Purpose: Reduce response time for paginated user queries
- Impact: 3x faster load times on the admin user list page
```

### Trivial (minimal body)

```
🎨 style: readme: fix typo in header

- File(s) changed: README.md
- Nature of changes: Typo correction
```
