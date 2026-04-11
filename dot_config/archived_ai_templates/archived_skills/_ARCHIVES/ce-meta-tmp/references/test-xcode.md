# Test Xcode

> Build and test iOS apps on the simulator using XcodeBuildMCP, capturing screenshots, logs, and verifying app behavior.

## Quick Usage Examples

```bash
# Test with default/auto-discovered scheme
test-xcode

# Test a specific scheme
test-xcode MyApp

# Test current scheme explicitly
test-xcode current
```

## When to Use

- After writing or modifying iOS code, to verify the app builds and key screens render correctly on the simulator.
- When reviewing PRs that touch iOS code (can be spawned as a background subagent from `ce:review`).
- Whenever build verification or simulator-based smoke testing is needed.

## Inputs

- Scheme name, or `"current"` to use the default/last-used scheme (optional; auto-discovered if omitted).
- Xcode installed with command-line tools.
- XcodeBuildMCP MCP server connected.
- Valid Xcode project or workspace.
- At least one iOS Simulator available.

## Methodology

### Step 0 — Verify XcodeBuildMCP is Available

Call the XcodeBuildMCP server's `list_simulators` tool to confirm it is connected.

If the tool is not found or errors, inform the user:

```
XcodeBuildMCP not installed

Install via Homebrew:
  brew tap getsentry/xcodebuildmcp && brew install xcodebuildmcp

Or via npx (no global install needed):
  npx -y xcodebuildmcp@latest mcp

Then add "XcodeBuildMCP" as an MCP server in your agent configuration
and restart your agent.
```

**Do NOT proceed until XcodeBuildMCP is confirmed working.**

### Step 1 — Discover Project and Scheme

Call XcodeBuildMCP's `discover_projs` tool to find available projects, then call `list_schemes` with the project path to get available schemes.

- If a scheme argument was provided, use that scheme name.
- If `"current"` was provided, use the default/last-used scheme.

### Step 2 — Boot Simulator

Call `list_simulators` to find available simulators. Boot the preferred simulator (**iPhone 15 Pro recommended**) by calling `boot_simulator` with the simulator's UUID.

Wait for the simulator to be ready before proceeding.

### Step 3 — Build the App

Call `build_ios_sim_app` with the project path and scheme name.

**On failure:**
- Capture build errors.
- Create a P1 todo (via `todo-create`) for each build error.
- Report to user with specific error details.
- Stop.

**On success:**
- Note the built app path for installation.
- Proceed to step 4.

### Step 4 — Install and Launch

1. Call `install_app_on_simulator` with the built app path and simulator UUID.
2. Call `launch_app_on_simulator` with the bundle ID and simulator UUID.
3. Call `capture_sim_logs` with the simulator UUID and bundle ID to start log capture.

### Step 5 — Test Key Screens

For each key screen in the app:

**Take screenshot:**
Call `take_screenshot` with the simulator UUID and a descriptive filename (e.g., `screen-home.png`).

**Review screenshot for:**
- UI elements rendered correctly.
- No error messages visible.
- Expected content displayed.
- Layout looks correct.

**Check logs for errors:**
Call `get_sim_logs` with the simulator UUID. Look for:
- Crashes.
- Exceptions.
- Error-level log messages.
- Failed network requests.

**Known automation limitation — SwiftUI Text links:**
Simulated taps (via XcodeBuildMCP or any simulator automation tool) do not trigger gesture recognizers on SwiftUI `Text` views with inline `AttributedString` links. Taps report success but have no effect. This is a platform limitation — inline links are not exposed as separate elements in the accessibility tree. When a tap on a Text link has no visible effect, prompt the user to tap manually in the simulator. If the target URL is known, `xcrun simctl openurl <device> <URL>` can open it directly as a fallback.

### Step 6 — Human Verification (When Required)

Pause for human input when testing touches flows that require device interaction:

| Flow Type | What to Ask |
|---|---|
| Sign in with Apple | "Please complete Sign in with Apple on the simulator" |
| Push notifications | "Send a test push and confirm it appears" |
| In-app purchases | "Complete a sandbox purchase" |
| Camera/Photos | "Grant permissions and verify camera works" |
| Location | "Allow location access and verify map updates" |
| SwiftUI Text links | "Please tap on [element description] manually — automated taps cannot trigger inline text links" |

Present to the user and wait for reply:

```
Human Verification Needed

This test requires [flow type]. Please:
1. [Action to take on simulator]
2. [What to verify]

Did it work correctly?
1. Yes - continue testing
2. No - describe the issue
```

### Step 7 — Handle Failures

When a test fails:

1. **Document the failure:**
   - Take a screenshot of the error state.
   - Capture console logs.
   - Note reproduction steps.

2. **Present options to the user and wait for reply:**

   ```
   Test Failed: [screen/feature]

   Issue: [description]
   Logs: [relevant error messages]

   How to proceed?
   1. Fix now - I'll help debug and fix
   2. Create todo - Add a todo for later (using the todo-create skill)
   3. Skip - Continue testing other screens
   ```

3. **If "Fix now":** investigate, propose a fix, rebuild and retest.
4. **If "Create todo":** run the `todo-create` skill, create a todo with priority `p1` and description `xcode-{description}`, then continue.
5. **If "Skip":** log as skipped, continue.

### Step 8 — Test Summary

After all tests complete, present:

```markdown
## Xcode Test Results

**Project:** [project name]
**Scheme:** [scheme name]
**Simulator:** [simulator name]

### Build: Success / Failed

### Screens Tested: [count]

| Screen | Status | Notes |
|--------|--------|-------|
| Launch | Pass | |
| Home | Pass | |
| Settings | Fail | Crash on tap |
| Profile | Skip | Requires login |

### Console Errors: [count]
- [List any errors found]

### Human Verifications: [count]
- Sign in with Apple: Confirmed
- Push notifications: Confirmed

### Failures: [count]
- Settings screen - crash on navigation

### Created Todos: [count]
- `006-pending-p1-xcode-settings-crash.md`

### Result: [PASS / FAIL / PARTIAL]
```

### Step 9 — Cleanup

After testing:

1. Call `stop_log_capture` with the simulator UUID.
2. Optionally call `shutdown_simulator` with the simulator UUID.

## Quality Gates

- Do not proceed past Step 0 if XcodeBuildMCP is not confirmed working.
- Do not proceed past Step 3 if the build fails (create todos and stop).
- Every failed screen must result in one of: fix applied + retest, todo created, or explicitly skipped.

## Outputs

- Xcode test results summary (pass/fail/partial per screen).
- Screenshots of tested screens and any error states.
- Console log excerpts for any errors found.
- Todo files created for failures deferred for later fix.

## Feeds Into

- `todo-create` — for build errors and test failures deferred to todos.
- `ce:review` — this skill can be spawned as a subagent from the review workflow for iOS PRs.

## Harness Notes

- Requires the XcodeBuildMCP MCP server to be connected. MCP tool call naming varies by platform (e.g., `mcp__xcodebuildmcp__list_simulators` in Claude Code; use the equivalent method call for other platforms).
- Human verification prompts require the ability to pause and wait for user input.
- When reviewing PRs that touch iOS code, the `ce:review` workflow can spawn an agent to run this skill, build on the simulator, test key screens, and check for crashes.
