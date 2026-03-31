# Agent Browser

> Browser automation CLI for AI agents using Chrome/Chromium via CDP.

## When to Use

When a task requires interacting with websites: navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, logging into sites, or any programmatic web interaction.

## Inputs

- A URL or sequence of browser actions to perform
- Optional: credentials, session state, or auth profile for authenticated pages

## Methodology

### Installation

```bash
npm i -g agent-browser       # or
brew install agent-browser   # or
cargo install agent-browser

agent-browser install         # download Chrome
agent-browser upgrade         # update to latest
```

### Core Workflow

Every browser automation follows this pattern:

1. **Navigate**: `agent-browser open <url>`
2. **Snapshot**: `agent-browser snapshot -i` (get element refs like `@e1`, `@e2`)
3. **Interact**: Use refs to click, fill, select
4. **Re-snapshot**: After navigation or DOM changes, get fresh refs

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Submit"

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

### Ref Lifecycle (Critical)

Refs (`@e1`, `@e2`, etc.) are **invalidated** when the page changes. Always re-snapshot after:
- Clicking links or buttons that navigate
- Form submissions
- Dynamic content loading (dropdowns, modals)

```bash
agent-browser click @e5              # Navigates to new page
agent-browser snapshot -i            # MUST re-snapshot
agent-browser click @e1              # Use new refs
```

### Command Chaining

Commands chain with `&&`. The browser persists via a background daemon.

```bash
# Chain open + wait + snapshot in one call
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser snapshot -i

# Chain multiple interactions
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "password123" && agent-browser click @e3
```

**When to chain:** Use `&&` when you don't need to read intermediate output before proceeding. Run commands separately when you need to parse output first (e.g., snapshot to discover refs, then interact using those refs).

### Essential Commands

```bash
# Navigation
agent-browser open <url>              # Navigate (aliases: goto, navigate)
agent-browser close                   # Close browser

# Snapshot
agent-browser snapshot -i             # Interactive elements with refs (recommended)
agent-browser snapshot -i -C          # Include cursor-interactive elements (divs with onclick, cursor:pointer)
agent-browser snapshot -s "#selector" # Scope to CSS selector

# Interaction (use @refs from snapshot)
agent-browser click @e1               # Click element
agent-browser click @e1 --new-tab     # Click and open in new tab
agent-browser fill @e2 "text"         # Clear and type text
agent-browser type @e2 "text"         # Type without clearing
agent-browser select @e1 "option"     # Select dropdown option
agent-browser check @e1               # Check checkbox
agent-browser press Enter             # Press key
agent-browser keyboard type "text"    # Type at current focus (no selector)
agent-browser keyboard inserttext "text"  # Insert without key events
agent-browser scroll down 500         # Scroll page
agent-browser scroll down 500 --selector "div.content"  # Scroll within container

# Get information
agent-browser get text @e1            # Get element text
agent-browser get url                 # Get current URL
agent-browser get title               # Get page title
agent-browser get cdp-url             # Get CDP WebSocket URL

# Wait
agent-browser wait @e1                # Wait for element
agent-browser wait --load networkidle # Wait for network idle
agent-browser wait --url "**/page"    # Wait for URL pattern
agent-browser wait 2000               # Wait milliseconds
agent-browser wait --text "Welcome"   # Wait for text to appear (substring match)
agent-browser wait --fn "!document.body.innerText.includes('Loading...')"  # Wait for text to disappear
agent-browser wait "#spinner" --state hidden  # Wait for element to disappear

# Downloads
agent-browser download @e1 ./file.pdf          # Click element to trigger download
agent-browser wait --download ./output.zip     # Wait for any download to complete
agent-browser --download-path ./downloads open <url>  # Set default download directory

# Network
agent-browser network requests                 # Inspect tracked requests
agent-browser network route "**/api/*" --abort  # Block matching requests
agent-browser network har start                # Start HAR recording
agent-browser network har stop ./capture.har   # Stop and save HAR file

# Viewport & Device Emulation
agent-browser set viewport 1920 1080          # Set viewport size (default: 1280x720)
agent-browser set viewport 1920 1080 2        # 2x retina (same CSS size, higher res screenshots)
agent-browser set device "iPhone 14"          # Emulate device (viewport + user agent)

# Capture
agent-browser screenshot              # Screenshot to temp dir
agent-browser screenshot --full       # Full page screenshot
agent-browser screenshot --annotate   # Annotated screenshot with numbered element labels
agent-browser screenshot --screenshot-dir ./shots  # Save to custom directory
agent-browser screenshot --screenshot-format jpeg --screenshot-quality 80
agent-browser pdf output.pdf          # Save as PDF

# Clipboard
agent-browser clipboard read                      # Read text from clipboard
agent-browser clipboard write "Hello, World!"     # Write text to clipboard
agent-browser clipboard copy                      # Copy current selection
agent-browser clipboard paste                     # Paste from clipboard

# Diff (compare page states)
agent-browser diff snapshot                          # Compare current vs last snapshot
agent-browser diff snapshot --baseline before.txt    # Compare current vs saved file
agent-browser diff screenshot --baseline before.png  # Visual pixel diff
agent-browser diff url <url1> <url2>                 # Compare two pages
agent-browser diff url <url1> <url2> --wait-until networkidle  # Custom wait strategy
agent-browser diff url <url1> <url2> --selector "#main"  # Scope to element
```

### Batch Execution

Execute multiple commands in a single invocation by piping a JSON array of string arrays to `batch`. Avoids per-command process startup overhead.

```bash
echo '[
  ["open", "https://example.com"],
  ["snapshot", "-i"],
  ["click", "@e1"],
  ["screenshot", "result.png"]
]' | agent-browser batch --json

# Stop on first error
agent-browser batch --bail < commands.json
```

Use `batch` when you have a known sequence that doesn't depend on intermediate output. Use separate commands when you need to parse output between steps.

### Handling Authentication

**Option 1: Import auth from the user's browser (fastest for one-off tasks)**

```bash
agent-browser --auto-connect state save ./auth.json
agent-browser --state ./auth.json open https://app.example.com/dashboard
```

State files contain session tokens in plaintext — add to `.gitignore` and delete when done. Set `AGENT_BROWSER_ENCRYPTION_KEY` for encryption at rest.

**Option 2: Persistent profile (simplest for recurring tasks)**

```bash
agent-browser --profile ~/.myapp open https://app.example.com/login
# ... fill credentials, submit ...
agent-browser --profile ~/.myapp open https://app.example.com/dashboard
```

**Option 3: Session name (auto-save/restore cookies + localStorage)**

```bash
agent-browser --session-name myapp open https://app.example.com/login
# ... login flow ...
agent-browser close  # State auto-saved
# Next time: state auto-restored
agent-browser --session-name myapp open https://app.example.com/dashboard
```

**Option 4: Auth vault (credentials stored encrypted, login by name) — Recommended**

```bash
echo "$PASSWORD" | agent-browser auth save myapp --url https://app.example.com/login --username user --password-stdin
agent-browser auth login myapp
# List/show/delete profiles
agent-browser auth list
agent-browser auth show myapp
agent-browser auth delete myapp
```

`auth login` waits for username/password/submit selectors before interacting. More reliable on delayed SPA login screens.

**Option 5: State file (manual save/load)**

```bash
agent-browser state save ./auth.json
agent-browser state load ./auth.json
agent-browser open https://app.example.com/dashboard
```

### Session Management

```bash
# Parallel sessions (each agent gets its own isolated session)
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com
agent-browser session list

# Always close sessions to avoid leaked processes
agent-browser close                    # Close default session
agent-browser --session agent1 close   # Close specific session

# Auto-shutdown after inactivity (useful for CI)
AGENT_BROWSER_IDLE_TIMEOUT_MS=60000 agent-browser open example.com

# State management
agent-browser state list
agent-browser state show myapp-default.json
agent-browser state clear myapp
agent-browser state clean --older-than 7
```

### Working with Iframes

Iframe content is automatically inlined in snapshots. Refs inside iframes carry frame context — interact directly.

```bash
agent-browser open https://example.com/checkout
agent-browser snapshot -i
# @e2 [Iframe] "payment-frame"
#   @e3 [input] "Card number"
#   @e4 [input] "Expiry"
#   @e5 [button] "Pay"

agent-browser fill @e3 "4111111111111111"
agent-browser fill @e4 "12/28"
agent-browser click @e5

# To scope a snapshot to one iframe:
agent-browser frame @e2
agent-browser snapshot -i         # Only iframe content
agent-browser frame main          # Return to main frame
```

### Annotated Screenshots (Vision Mode)

Use `--annotate` to take a screenshot with numbered labels overlaid on interactive elements. Each label `[N]` maps to ref `@eN`. Also caches refs, so you can interact immediately without a separate snapshot.

```bash
agent-browser screenshot --annotate
# Output includes the image path and a legend:
#   [1] @e1 button "Submit"
#   [2] @e2 link "Home"
#   [3] @e3 textbox "Email"
agent-browser click @e2              # Click using ref from annotated screenshot
```

Use annotated screenshots when:
- The page has unlabeled icon buttons or visual-only elements
- You need to verify visual layout or styling
- Canvas or chart elements are present (invisible to text snapshots)
- You need spatial reasoning about element positions

### Semantic Locators (Alternative to Refs)

When refs are unavailable or unreliable:

```bash
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find role button click --name "Submit"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click
```

### JavaScript Evaluation

```bash
# Simple expressions
agent-browser eval 'document.title'
agent-browser eval 'document.querySelectorAll("img").length'

# Complex JS: use --stdin with heredoc (RECOMMENDED for nested quotes)
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify(
  Array.from(document.querySelectorAll("img"))
    .filter(i => !i.alt)
    .map(i => ({ src: i.src.split("/").pop(), width: i.width }))
)
EVALEOF

# Base64 encoding (avoids all shell escaping issues)
agent-browser eval -b "$(echo -n 'Array.from(document.querySelectorAll("a")).map(a => a.href)' | base64)"
```

**Rules of thumb:**
- Single-line, no nested quotes → regular `eval 'expression'` with single quotes is fine
- Nested quotes, arrow functions, template literals, or multiline → use `eval --stdin <<'EVALEOF'`
- Programmatic/generated scripts → use `eval -b` with base64

### Timeouts and Slow Pages

Default timeout is 25 seconds. Override with `AGENT_BROWSER_DEFAULT_TIMEOUT` (milliseconds).

```bash
agent-browser wait --load networkidle         # Wait for network activity to settle
agent-browser wait "#content"                 # Wait for specific element
agent-browser wait --url "**/dashboard"       # Wait for URL pattern
agent-browser wait --fn "document.readyState === 'complete'"  # JS condition
agent-browser wait 5000                       # Fixed duration (last resort)
```

### Diffing (Verifying Changes)

```bash
# Typical workflow: snapshot → action → diff
agent-browser snapshot -i          # Take baseline snapshot
agent-browser click @e2            # Perform action
agent-browser diff snapshot        # See what changed (auto-compares to last snapshot)

# Visual regression testing
agent-browser screenshot baseline.png
agent-browser diff screenshot --baseline baseline.png

# Compare two pages
agent-browser diff url https://staging.example.com https://prod.example.com --screenshot
```

`diff snapshot` output uses `+` for additions and `-` for removals. `diff screenshot` produces a diff image with changed pixels highlighted in red, plus a mismatch percentage.

### Connect to Existing Chrome

```bash
# Auto-discover running Chrome with remote debugging enabled
agent-browser --auto-connect open https://example.com
agent-browser --auto-connect snapshot

# Or with explicit CDP port
agent-browser --cdp 9222 snapshot
```

### Color Scheme (Dark Mode)

```bash
agent-browser --color-scheme dark open https://example.com
AGENT_BROWSER_COLOR_SCHEME=dark agent-browser open https://example.com
agent-browser set media dark
```

### Local Files

```bash
agent-browser --allow-file-access open file:///path/to/document.pdf
agent-browser --allow-file-access open file:///path/to/page.html
agent-browser screenshot output.png
```

### iOS Simulator (Mobile Safari)

```bash
agent-browser device list
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1          # Tap (alias for click)
agent-browser -p ios fill @e2 "text"
agent-browser -p ios swipe up         # Mobile-specific gesture
agent-browser -p ios screenshot mobile.png
agent-browser -p ios close
```

Requirements: macOS with Xcode, Appium (`npm install -g appium && appium driver install xcuitest`). Real devices: use `--device "<UDID>"`.

### Visual Browser (Debugging)

```bash
agent-browser --headed open https://example.com
agent-browser highlight @e1          # Highlight element
agent-browser inspect                # Open Chrome DevTools for the active page
agent-browser record start demo.webm # Record session
agent-browser profiler start         # Start Chrome DevTools profiling
agent-browser profiler stop trace.json # Stop and save profile
```

Set `AGENT_BROWSER_HEADED=1` to enable headed mode via environment variable.

### Browser Engine Selection

```bash
agent-browser --engine lightpanda open example.com
export AGENT_BROWSER_ENGINE=lightpanda
agent-browser --engine lightpanda --executable-path /path/to/lightpanda open example.com
```

Supported engines:
- `chrome` (default) — Chrome/Chromium via CDP
- `lightpanda` — Lightpanda headless browser via CDP (10x faster, 10x less memory). Does NOT support `--extension`, `--profile`, `--state`, or `--allow-file-access`.

### Security

All security features are opt-in. By default, agent-browser imposes no restrictions.

**Content Boundaries (recommended for AI agents):**

```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1
agent-browser snapshot
# Output wrapped in: --- AGENT_BROWSER_PAGE_CONTENT nonce=<hex> origin=https://example.com ---
```

**Domain Allowlist:**

```bash
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"
# Wildcards like *.example.com also match the bare domain.
# Sub-resource requests, WebSocket, and EventSource to non-allowed domains are blocked.
```

**Action Policy:**

```bash
export AGENT_BROWSER_ACTION_POLICY=./policy.json
```

```json
{ "default": "deny", "allow": ["navigate", "snapshot", "click", "scroll", "wait", "get"] }
```

Auth vault operations bypass action policy, but domain allowlist still applies.

**Output Limits:**

```bash
export AGENT_BROWSER_MAX_OUTPUT=50000
```

### Configuration File

Create `agent-browser.json` in the project root for persistent settings:

```json
{
  "headed": true,
  "proxy": "http://localhost:8080",
  "profile": "./browser-data"
}
```

Priority (lowest to highest): `~/.agent-browser/config.json` < `./agent-browser.json` < env vars < CLI flags.

## Quality Gates

- Always close browser sessions when done to avoid leaked processes
- Always re-snapshot after page navigation or DOM changes
- For authenticated pages, verify session is valid before proceeding
- Use `wait --load networkidle` for slow pages before taking snapshots

## Outputs

- Accessibility tree snapshots with element refs
- Screenshots (PNG, JPEG) and PDFs
- Extracted text and JSON data
- Diff reports (snapshot diffs and visual pixel diffs)
- HAR files for network analysis

## Feeds Into

- QA testing and bug reporting
- Form automation workflows
- Authenticated data extraction
- Visual regression testing
- Web scraping pipelines
