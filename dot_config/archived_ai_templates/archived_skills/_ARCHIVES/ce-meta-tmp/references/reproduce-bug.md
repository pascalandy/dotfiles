# Reproduce Bug

> Systematically reproduce and investigate a bug from a GitHub issue using a hypothesis-driven workflow.

## When to Use

- User provides a GitHub issue number or URL for a bug they want reproduced or investigated
- Before writing a fix, to confirm root cause with evidence
- Works across any language, framework, or project type

## Inputs

- GitHub issue number or URL (ask the user if not provided)
- A running development server (for UI/browser bugs)
- Access to the codebase and its test suite

## Methodology

### Phase 1: Understand the Issue

Fetch and analyze the bug report before touching the codebase.

**Fetch the issue:**
```bash
gh issue view $ISSUE_NUMBER --json title,body,comments,labels,assignees
```

If the argument is a URL rather than a number, extract the issue number or pass the URL directly to `gh`.

If no issue number or URL was provided, prompt the user for one before proceeding.

**Extract key details from the issue and comments:**

- **Reported symptoms** — what the user observed (error message, wrong output, visual glitch, crash)
- **Expected behavior** — what should have happened instead
- **Reproduction steps** — any steps the reporter provided
- **Environment clues** — browser, OS, version, user role, data conditions
- **Frequency** — always reproducible, intermittent, or one-time

If the issue lacks reproduction steps or is ambiguous, note what is missing — this shapes the investigation strategy.

---

### Phase 2: Hypothesize

Before running anything, form theories about the root cause.

**Search for relevant code** by searching file contents for:
- Error messages or strings mentioned in the issue
- Feature names, route paths, or UI labels described in the report
- Related model/service/controller names

**Form 2–3 plausible hypotheses.** Each hypothesis must identify:
- **What** might be wrong (e.g., "race condition in session refresh", "nil check missing on optional field")
- **Where** in the codebase (specific files and line ranges)
- **Why** it would produce the reported symptoms

Rank hypotheses by likelihood. Start investigating the most likely one first.

---

### Phase 3: Reproduce

The reproduction strategy depends on the bug type. Choose the appropriate route.

#### Route A: Test-based reproduction (backend, logic, data bugs)

1. Find existing test files covering the affected code
2. Run existing tests to see if any already fail
3. If no test covers the scenario, write a minimal failing test that demonstrates the reported behavior
4. A failing test that matches the reported symptoms confirms the bug

#### Route B: Browser-based reproduction (UI, visual, interaction bugs)

Use the `agent-browser` CLI for browser automation.

**Verify server is running:**
```bash
agent-browser open http://localhost:${PORT:-3000}
agent-browser snapshot -i
```

If the server is not running, ask the user to start their development server and provide the correct port.

To detect the correct port: check project instruction files (`AGENTS.md`, `CLAUDE.md`) for port references, then `package.json` dev scripts, then `.env` files, falling back to `3000`.

**Follow reproduction steps** — navigate to the affected area and execute the steps from the issue:
```bash
agent-browser open "http://localhost:${PORT}/[affected_route]"
agent-browser snapshot -i
```

Use `agent-browser` commands to interact:
- `agent-browser click @ref` — click elements
- `agent-browser fill @ref "text"` — fill form fields
- `agent-browser snapshot -i` — capture current state
- `agent-browser screenshot bug-evidence.png` — save visual evidence

**When the bug is reproduced:**
1. Take a screenshot of the error state
2. Check for console errors: look at browser output and any visible error messages
3. Record the exact sequence of steps that triggered it

#### Route C: Manual / environment-specific reproduction

For bugs requiring specific data conditions, user roles, external service state, or that cannot be automated:

1. Document what conditions are needed
2. Prompt the user whether they can set up the required conditions
3. Guide them through manual reproduction steps if needed

#### If reproduction fails

If the bug cannot be reproduced after trying the most likely hypotheses:
1. Revisit the remaining hypotheses
2. Check if the bug is environment-specific (version, OS, browser, data-dependent)
3. Search the codebase for recent changes to the affected area:
   ```bash
   git log --oneline -20 -- [affected_files]
   ```
4. Document what was tried and what conditions might be missing

---

### Phase 4: Investigate

Dig deeper into the root cause using available observability.

**Check logs and traces** — what to check depends on the bug and what the project provides:
- **Application logs** — search local log output (dev server stdout, log files) for error patterns, stack traces, or warnings
- **Error tracking** — check for related exceptions in the project's error tracker (Sentry, AppSignal, Bugsnag, Datadog, etc.)
- **Browser console** — for UI bugs, check developer console output for JavaScript errors, failed network requests, or CORS issues
- **Database state** — if the bug involves data, inspect relevant records for unexpected values, missing associations, or constraint violations
- **Request/response cycle** — check server logs for the specific request: status codes, params, timing, middleware behavior

**Trace the code path** starting from the entry point identified in Phase 2:
1. Read the relevant source files
2. Identify where the behavior diverges from expectations
3. Check edge cases: nil/null values, empty collections, boundary conditions, race conditions
4. Look for recent changes that may have introduced the bug:
   ```bash
   git log --oneline -10 -- [file]
   ```

---

### Phase 5: Document Findings

**Compile the report** with these sections:

1. **Root cause** — what is actually wrong and where (with file paths and line numbers, e.g., `app/services/example_service.rb:42`)
2. **Reproduction steps** — verified steps to trigger the bug (mark as confirmed or unconfirmed)
3. **Evidence** — screenshots, test output, log excerpts, console errors
4. **Suggested fix** — if a fix is apparent, describe it with the specific code changes needed
5. **Open questions** — anything still unclear or needing further investigation

**Present to user before any external action.** Do not post comments to GitHub or take any external action without explicit confirmation.

Present the user with options and wait for a reply:

```
Investigation complete. How to proceed?

1. Post findings to the issue as a comment
2. Start working on a fix
3. Just review the findings (no external action)
```

**If the user chooses to post to the issue:**
```bash
gh issue comment $ISSUE_NUMBER --body "$(cat <<'EOF'
## Bug Investigation

**Root Cause:** [summary]

**Reproduction Steps (verified):**
1. [step]
2. [step]

**Relevant Code:** [file:line references]

**Suggested Fix:** [description if applicable]
EOF
)"
```

## Quality Gates

- Issue fetched and all key details extracted before touching the codebase
- At least 2 hypotheses formed before running anything
- Reproduction confirmed via failing test, screenshot, or documented manual steps
- Root cause identified with file path and line number
- User confirmed before any external action (posting to GitHub)

## Outputs

- Investigation report with root cause, reproduction steps, evidence, and suggested fix
- (Optional, user-confirmed) Comment posted to the GitHub issue
- (Optional) Failing test case demonstrating the bug

## Feeds Into

- Fix implementation (manual or via `ce:work`)
- `report-bug-ce` (if the bug is in the compound-engineering plugin itself)
