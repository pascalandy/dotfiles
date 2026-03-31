# Todo Create

> Create and manage durable, cross-session work items in the file-based todo tracking system.

## When to Use

- A fix or task requires more than ~15 minutes of work.
- Work has dependencies on other items.
- The item requires planning or prioritization before action.
- A code review, browser test, or Xcode test surfaces a failure that should not be fixed immediately.
- Tracking technical debt, feature requests, or multi-session findings.

**Act immediately instead** when the fix is trivial, obvious, and self-contained.

## Inputs

- Description of the problem or work item.
- Priority (`p1` critical, `p2` important, `p3` nice-to-have).
- Any known dependencies (issue IDs of blocking todos).

## Methodology

### Directory Paths

| Purpose | Path |
|---|---|
| **Canonical (write here)** | `.context/compound-engineering/todos/` |
| **Legacy (read-only)** | `todos/` |

Always check **both** paths when reading or searching for todos. Write new todos only to the canonical path. This directory has a multi-session lifecycle — do not clean it up as scratch.

### File Naming Convention

```
{issue_id}-{status}-{priority}-{description}.md
```

- **issue_id**: Sequential number (001, 002, …) — never reused.
- **status**: `pending` | `ready` | `complete`
- **priority**: `p1` (critical) | `p2` (important) | `p3` (nice-to-have)
- **description**: kebab-case, brief

**Example:** `002-ready-p1-fix-n-plus-1.md`

### YAML Frontmatter

```yaml
---
status: ready
priority: p1
issue_id: "002"
tags: [rails, performance]
dependencies: ["001"]     # Issue IDs this is blocked by
---
```

### Required Sections in Every Todo File

- Problem Statement
- Findings
- Proposed Solutions
- Recommended Action *(filled during triage)*
- Acceptance Criteria
- Work Log

### Optional Sections

- Technical Details
- Resources
- Notes

---

### Workflow: Creating a New Todo

1. Run in terminal: `mkdir -p .context/compound-engineering/todos/`
2. Find files matching pattern `[0-9]*-*.md` in both directory paths. Find the highest numeric prefix, increment by 1, zero-pad to 3 digits → `NEXT_ID`.
3. Create the file at `.context/compound-engineering/todos/{NEXT_ID}-pending-{priority}-{description}.md` using the todo template below.
4. Fill in: Problem Statement, Findings, Proposed Solutions, Acceptance Criteria, and an initial Work Log entry.
5. Set status to `pending` (needs triage) or `ready` (pre-approved).

### Workflow: Triaging Pending Items

1. Find files matching `*-pending-*.md` in both directory paths.
2. Review each todo's Problem Statement, Findings, and Proposed Solutions.
3. **Approve:** rename `pending` → `ready` in both the filename and the frontmatter `status` field; fill in the Recommended Action section.
4. **Defer:** leave as `pending`.

For an interactive approval workflow, load the `todo-triage` skill.

### Workflow: Managing Dependencies

```yaml
dependencies: ["002", "005"]  # Blocked by these issues
dependencies: []               # No blockers
```

To check blockers: search file contents for `{dep_id}-complete-*.md` in both paths. Missing matches = incomplete blockers.

### Workflow: Completing a Todo

1. Verify all acceptance criteria are met.
2. Update the Work Log with a final session entry.
3. Rename `ready` → `complete` in both the filename and frontmatter `status` field.
4. Check for newly unblocked work: search file contents for `dependencies:.*"{issue_id}"`.

### Integration with Workflows

| Trigger | Flow |
|---|---|
| Code review | `ce:review` → Findings → `todo-triage` → Todos |
| Autonomous review | `ce:review mode:autofix` → Residual todos → `todo-resolve` |
| Code TODOs | `todo-resolve` → Fixes + Complex todos |
| Planning | Brainstorm → Create todo → Work → Complete |

### Tool Preference

Use native file-search/glob and content-search tools instead of shell commands for finding and reading todo files. Use shell only for operations with no native equivalent (`mv`, `mkdir -p`).

---

## Todo Template

```markdown
---
status: pending
priority: p2
issue_id: "XXX"
tags: []
dependencies: []
---

# Brief Task Title

Replace with a concise title describing what needs to be done.

## Problem Statement

What is broken, missing, or needs improvement? Provide clear context about why this matters.

**Example:**
- Template system lacks comprehensive test coverage for edge cases discovered during PR review
- Email service is missing proper error handling for rate-limit scenarios
- Documentation doesn't cover the new authentication flow

## Findings

Investigation results, root cause analysis, and key discoveries.

- Finding 1 (with specifics: file, line number if applicable)
- Finding 2
- Key discovery with impact assessment
- Related issues or patterns discovered

**Example format:**
- Identified 12 missing test scenarios in `app/models/user_test.rb`
- Current coverage: 60% of code paths
- Missing: empty inputs, special characters, large payloads
- Similar issues exist in `app/models/post_test.rb` (~8 scenarios)

## Proposed Solutions

Present multiple options with pros, cons, effort estimates, and risk assessment.

### Option 1: [Solution Name]

**Approach:** Describe the solution clearly.

**Pros:**
- Benefit 1
- Benefit 2

**Cons:**
- Drawback 1
- Drawback 2

**Effort:** 2-3 hours

**Risk:** Low / Medium / High

---

### Option 2: [Solution Name]

**Approach:** Describe the solution clearly.

**Pros:**
- Benefit 1
- Benefit 2

**Cons:**
- Drawback 1
- Drawback 2

**Effort:** 4-6 hours

**Risk:** Low / Medium / High

---

### Option 3: [Solution Name]

(Include if you have alternatives)

## Recommended Action

**To be filled during triage.** Clear, actionable plan for resolving this todo.

**Example:**
"Implement both unit tests (covering each scenario) and integration tests (full pipeline) before merging. Estimated 4 hours total effort. Target coverage > 85% for this module."

## Technical Details

Affected files, related components, database changes, or architectural considerations.

**Affected files:**
- `app/models/user.rb:45` - full_name method
- `app/services/user_service.rb:12` - validation logic
- `test/models/user_test.rb` - existing tests

**Related components:**
- UserMailer (depends on user validation)
- AccountPolicy (authorization checks)

**Database changes (if any):**
- Migration needed? Yes / No
- New columns/tables? Describe here

## Resources

Links to errors, tests, PRs, documentation, similar issues.

- **PR:** #1287
- **Related issue:** #456
- **Error log:** [link to AppSignal incident]
- **Documentation:** [relevant docs]
- **Similar patterns:** Issue #200 (completed, ref for approach)

## Acceptance Criteria

Testable checklist items for verifying completion.

- [ ] All acceptance criteria checked
- [ ] Tests pass (unit + integration if applicable)
- [ ] Code reviewed and approved
- [ ] (Example) Test coverage > 85%
- [ ] (Example) Performance metrics acceptable
- [ ] (Example) Documentation updated

## Work Log

Chronological record of work sessions, actions taken, and learnings.

### YYYY-MM-DD - Initial Discovery

**By:** [agent or person]

**Actions:**
- Identified the issue
- Analyzed existing patterns (file:line references)
- Drafted solution approaches

**Learnings:**
- Similar issues exist in related modules
- Current setup supports both unit and integration tests

---

(Add more entries as work progresses)

## Notes

Additional context, decisions, or reminders.

- Decision: Include both unit and integration tests for comprehensive coverage
- Blocker: Depends on completion of issue #001
- Timeline: Priority for sprint due to blocking other work
```

## Quality Gates

- Never reuse an issue ID.
- Always write to the canonical path, never to the legacy `todos/` path.
- New todos start as `pending` unless pre-approved (set `ready` only if explicitly authorized).
- Every todo must have Problem Statement, Findings, Proposed Solutions, Acceptance Criteria, and at least one Work Log entry before being considered complete.

## Outputs

- A markdown todo file at `.context/compound-engineering/todos/{id}-{status}-{priority}-{description}.md`.

## Feeds Into

- `todo-triage` — to approve pending todos and set Recommended Action.
- `todo-resolve` — to implement approved (ready) todos in batch.
