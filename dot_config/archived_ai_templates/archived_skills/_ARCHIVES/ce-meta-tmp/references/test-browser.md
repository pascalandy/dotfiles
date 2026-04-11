# Test Browser

> Run end-to-end browser tests on pages affected by a PR or branch using the `agent-browser` CLI.

## Quick Usage Examples

```bash
# Test current branch
test-browser current

# Test a specific PR
test-browser 42

# Test a specific branch
test-browser feat/new-login

# Test against a specific port
test-browser current --port 5000
```

## When to Use

- After writing code for a PR or branch, to verify affected pages render and behave correctly.
- As part of the `slfg` parallel phase (spawned as a background subagent).
- Whenever manual browser verification of changed routes is needed.

## Inputs

- PR number, branch name, `"current"`, or `--port PORT` (all optional; defaults to current branch diff).
- A running local development server.
- `agent-browser` CLI installed.

## Methodology

### Step 1 — Verify Installation

Check that `agent-browser` is available:

```bash
command -v agent-browser >/dev/null 2>&1 && echo "Ready" || (echo "Installing..." && npm install -g agent-browser && agent-browser install)
```

If installation fails, inform the user and stop.

**Important:** Use `agent-browser` exclusively for all browser automation in this workflow. Do not substitute any alternative browser automation system, browser MCP integration, or built-in browser-control tool. If the platform offers multiple browser control methods, always choose `agent-browser`.

### Step 2 — Ask Browser Mode

Prompt the user (present numbered options and wait for a reply):

```
Do you want to watch the browser tests run?

1. Headed (watch) - Opens visible browser window so you can see tests run
2. Headless (faster) - Runs in background, faster but invisible
```

Store the choice. Use the `--headed` flag for all `agent-browser` commands when option 1 is selected.

### Step 3 — Determine Test Scope

**If PR number provided:**
```bash
gh pr view [number] --json files -q '.files[].path'
```

**If `current` or empty:**
```bash
git diff --name-only main...HEAD
```

**If branch name provided:**
```bash
git diff --name-only main...[branch]
```

### Step 4 — Map Files to Routes

Map changed files to testable routes using this table:

| File Pattern | Route(s) |
|---|---|
| `app/views/users/*` | `/users`, `/users/:id`, `/users/new` |
| `app/controllers/settings_controller.rb` | `/settings` |
| `app/javascript/controllers/*_controller.js` | Pages using that Stimulus controller |
| `app/components/*_component.rb` | Pages rendering that component |
| `app/views/layouts/*` | All pages (test homepage at minimum) |
| `app/assets/stylesheets/*` | Visual regression on key pages |
| `app/helpers/*_helper.rb` | Pages using that helper |
| `src/app/*` (Next.js) | Corresponding routes |
| `src/components/*` | Pages using those components |

Build a list of URLs to test based on the mapping.

### Step 5 — Detect Dev Server Port

Determine the dev server port using this priority order:

1. **Explicit argument** — if the user passed `--port 5000`, use that directly.
2. **Project instructions** — check `AGENTS.md`, `CLAUDE.md`, or other instruction files for port references.
3. **package.json** — check dev/start scripts for `--port` flags.
4. **Environment files** — check `.env`, `.env.local`, `.env.development` for `PORT=`.
5. **Default** — fall back to `3000`.

```bash
PORT="${EXPLICIT_PORT:-}"
if [ -z "$PORT" ]; then
  PORT=$(grep -Eio '(port\s*[:=]\s*|localhost:)([0-9]{4,5})' AGENTS.md 2>/dev/null | grep -Eo '[0-9]{4,5}' | head -1)
  if [ -z "$PORT" ]; then
    PORT=$(grep -Eio '(port\s*[:=]\s*|localhost:)([0-9]{4,5})' CLAUDE.md 2>/dev/null | grep -Eo '[0-9]{4,5}' | head -1)
  fi
fi
if [ -z "$PORT" ]; then
  PORT=$(grep -Eo '\-\-port[= ]+[0-9]{4,5}' package.json 2>/dev/null | grep -Eo '[0-9]{4,5}' | head -1)
fi
if [ -z "$PORT" ]; then
  PORT=$(grep -h '^PORT=' .env .env.local .env.development 2>/dev/null | tail -1 | cut -d= -f2)
fi
PORT="${PORT:-3000}"
echo "Using dev server port: $PORT"
```

### Step 6 — Verify Server is Running

```bash
agent-browser open http://localhost:${PORT}
agent-browser snapshot -i
```

If the server is not running, inform the user:

```
Server not running on port ${PORT}

Please start your development server:
- Rails: `bin/dev` or `rails server`
- Node/Next.js: `npm run dev`
- Custom port: run this skill again with `--port <your-port>`

Then re-run this skill.
```

### Step 7 — Test Each Affected Page

For each affected route:

**Navigate and capture snapshot:**
```bash
agent-browser open "http://localhost:${PORT}/[route]"
agent-browser snapshot -i
```

**For headed mode:**
```bash
agent-browser --headed open "http://localhost:${PORT}/[route]"
agent-browser --headed snapshot -i
```

**Verify key elements:**
- Use `agent-browser snapshot -i` to get interactive elements with refs.
- Page title/heading present.
- Primary content rendered.
- No error messages visible.
- Forms have expected fields.

**Test critical interactions:**
```bash
agent-browser click @e1
agent-browser snapshot -i
```

**Take screenshots:**
```bash
agent-browser screenshot page-name.png
agent-browser screenshot --full page-name-full.png
```

### Step 8 — Human Verification (When Required)

Pause for human input when testing touches flows that require external interaction:

| Flow Type | What to Ask |
|---|---|
| OAuth | "Please sign in with [provider] and confirm it works" |
| Email | "Check your inbox for the test email and confirm receipt" |
| Payments | "Complete a test purchase in sandbox mode" |
| SMS | "Verify you received the SMS code" |
| External APIs | "Confirm the [service] integration is working" |

Present to the user and wait for reply:

```
Human Verification Needed

This test touches [flow type]. Please:
1. [Action to take]
2. [What to verify]

Did it work correctly?
1. Yes - continue testing
2. No - describe the issue
```

### Step 9 — Handle Failures

When a test fails:

1. **Document the failure:**
   - Screenshot the error state: `agent-browser screenshot error.png`
   - Note the exact reproduction steps.

2. **Present options to the user and wait for reply:**

   ```
   Test Failed: [route]

   Issue: [description]
   Console errors: [if any]

   How to proceed?
   1. Fix now - I'll help debug and fix
   2. Create todo - Add a todo for later (using the todo-create skill)
   3. Skip - Continue testing other pages
   ```

3. **If "Fix now":** investigate, propose a fix, apply, re-run the failing test.
4. **If "Create todo":** run the `todo-create` skill, create a todo with priority `p1` and description `browser-test-{description}`, then continue.
5. **If "Skip":** log as skipped, continue.

### Step 10 — Test Summary

After all tests complete, present:

```markdown
## Browser Test Results

**Test Scope:** PR #[number] / [branch name]
**Server:** http://localhost:${PORT}

### Pages Tested: [count]

| Route | Status | Notes |
|-------|--------|-------|
| `/users` | Pass | |
| `/settings` | Pass | |
| `/dashboard` | Fail | Console error: [msg] |
| `/checkout` | Skip | Requires payment credentials |

### Console Errors: [count]
- [List any errors found]

### Human Verifications: [count]
- OAuth flow: Confirmed
- Email delivery: Confirmed

### Failures: [count]
- `/dashboard` - [issue description]

### Created Todos: [count]
- `005-pending-p1-browser-test-dashboard-error.md`

### Result: [PASS / FAIL / PARTIAL]
```

## agent-browser CLI Reference

```bash
# Navigation
agent-browser open <url>            # Navigate to URL
agent-browser back                  # Go back
agent-browser close                 # Close browser

# Snapshots (get element refs)
agent-browser snapshot -i           # Interactive elements with refs (@e1, @e2, etc.)
agent-browser snapshot -i --json    # JSON output

# Interactions (use refs from snapshot)
agent-browser click @e1             # Click element
agent-browser fill @e1 "text"       # Fill input
agent-browser type @e1 "text"       # Type without clearing
agent-browser press Enter           # Press key

# Screenshots
agent-browser screenshot out.png        # Viewport screenshot
agent-browser screenshot --full out.png # Full page screenshot

# Headed mode (visible browser)
agent-browser --headed open <url>       # Open with visible browser
agent-browser --headed click @e1        # Click in visible browser

# Wait
agent-browser wait @e1              # Wait for element
agent-browser wait 2000             # Wait milliseconds
```

## Quality Gates

- Do not proceed past Step 6 if the dev server is not running.
- Do not proceed past Step 1 if `agent-browser` cannot be installed.
- Every failed page must result in one of: fix applied, todo created, or explicitly skipped.

## Outputs

- Browser test results summary (pass/fail/partial per route).
- Screenshots of tested pages and any error states.
- Todo files created for failures deferred for later fix.

## Feeds Into

- `todo-create` — for failures deferred to todos.
- `todo-resolve` — to work through browser-test todos.

## Harness Notes

- The `agent-browser` CLI must be used exclusively. Do not use Chrome MCP tools (`mcp__claude-in-chrome__*`) or any other browser automation method.
- Human verification prompts require the ability to pause and wait for user input; implement via the platform's question/input tool.
- In Codex, do not substitute unrelated browsing tools. Use `agent-browser` exclusively as specified in Step 1.
