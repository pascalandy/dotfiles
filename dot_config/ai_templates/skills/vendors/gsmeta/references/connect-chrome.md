# Connect Chrome

> Launch real headed Chromium controlled by the agent, with the gstack Side Panel extension auto-loaded, so every browser action is visible in real time.

## When to Use

- User asks to "connect chrome", "open chrome", "real browser", "launch chrome"
- User wants to watch the agent work in a visible browser window
- QA or design review where the user wants to observe every click and navigation
- Sidebar chat: user wants to issue browser commands via natural language in the Side Panel
- After debugging with headless browse and needing a visual confirmation

## Inputs

- No required inputs
- Optional: a URL or task to start with after connecting

## Methodology

### Step 0: Pre-flight cleanup

Before connecting, kill any stale browse servers and clean up Chromium profile lock files. This prevents false "already connected" errors and profile lock conflicts from previous crashes.

```bash
# Kill any existing browse server
if [ -f "$(git rev-parse --show-toplevel 2>/dev/null)/.gstack/browse.json" ]; then
  _OLD_PID=$(cat "$(git rev-parse --show-toplevel)/.gstack/browse.json" 2>/dev/null | grep -o '"pid":[0-9]*' | grep -o '[0-9]*')
  [ -n "$_OLD_PID" ] && kill "$_OLD_PID" 2>/dev/null || true
  sleep 1
  [ -n "$_OLD_PID" ] && kill -9 "$_OLD_PID" 2>/dev/null || true
  rm -f "$(git rev-parse --show-toplevel)/.gstack/browse.json"
fi
# Clean Chromium profile locks (can persist after crashes)
_PROFILE_DIR="$HOME/.gstack/chromium-profile"
for _LF in SingletonLock SingletonSocket SingletonCookie; do
  rm -f "$_PROFILE_DIR/$_LF" 2>/dev/null || true
done
echo "Pre-flight cleanup done"
```

### Step 1: Check binary

Same setup check as browse — verify the binary exists at `~/.claude/skills/gstack/browse/dist/browse` or in the repo's `.claude/skills/gstack/browse/dist/browse`. Build with `./setup` if missing.

### Step 2: Connect

Run `browse connect`.

This launches Playwright's bundled Chromium in headed mode (not the user's regular Chrome — that stays untouched) with:
- A golden shimmer line at the top of every page so the user knows which window is agent-controlled
- The gstack Chrome extension auto-loaded
- Port 34567 (the extension auto-connects to this port)

Confirm the output shows `Mode: headed`. If not, run `browse status` and report.

### Step 3: Verify port and extension path

Run `browse status` and confirm `Mode: headed`. Read the port from `.gstack/browse.json` — it should be **34567**.

Find the extension path for manual loading fallback:

```bash
_EXT_PATH=""
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
[ -n "$_ROOT" ] && [ -f "$_ROOT/.claude/skills/gstack/extension/manifest.json" ] && _EXT_PATH="$_ROOT/.claude/skills/gstack/extension"
[ -z "$_EXT_PATH" ] && [ -f "$HOME/.claude/skills/gstack/extension/manifest.json" ] && _EXT_PATH="$HOME/.claude/skills/gstack/extension"
echo "EXTENSION_PATH: ${_EXT_PATH:-NOT FOUND}"
```

### Step 4: Guide user to Side Panel

Ask the user:

> Chrome is launched with gstack control. You should see Playwright's Chromium (not your regular Chrome) with a golden shimmer line at the top of the page.
>
> The Side Panel extension should be auto-loaded. To open it:
> 1. Look for the puzzle piece (Extensions) icon in the toolbar
> 2. Click it, find "gstack browse", click the pin icon
> 3. Click the pinned gstack icon in the toolbar
> 4. The Side Panel should open showing a live activity feed
>
> Port: 34567 (the extension connects automatically)

Options:
- A) I can see the Side Panel — let's go!
- B) I can see Chrome but can't find the extension
- C) Something went wrong

**If B:** Direct the user to `chrome://extensions`. Look for "gstack browse" — it should be listed and enabled. If NOT listed, click "Load unpacked", press Cmd+Shift+G in the file picker, paste the `EXTENSION_PATH` from Step 3, click Select. After loading, pin it and click to open the Side Panel. If the Side Panel badge stays gray (disconnected), click the gstack icon and enter port 34567 manually.

**If C:**
1. Run `browse status` and show the output
2. If server is not healthy, re-run Step 0 cleanup + Step 2 connect
3. If server IS healthy but browser isn't visible, try `browse focus`
4. If that fails, ask the user what they see (error message, blank screen, etc.)

### Step 5: Run a demo

Navigate to a test page and take a snapshot:

```bash
browse goto https://news.ycombinator.com
# wait ~2 seconds, then:
browse snapshot -i
```

Tell the user to check the Side Panel — the `goto` and `snapshot` commands should appear in the activity feed in real time.

### Step 6: Sidebar chat

After the activity feed demo, tell the user:

> The Side Panel also has a chat tab. Type a message like "take a snapshot and describe this page." A sidebar agent (a child agent instance) executes the request in the browser — you'll see the commands appear in the activity feed as they happen.
>
> The sidebar agent can navigate pages, click buttons, fill forms, and read content. Each task gets up to 5 minutes. It runs in an isolated session, so it won't interfere with the main agent window.

### Ongoing session

After connection, all browse skills run in the headed browser automatically — the user sees every page load, click, and assertion live:
- `browse focus` — bring Chrome to foreground
- `browse disconnect` — close headed Chrome, return to headless mode
- `browse handoff [message]` — hand control to the user
- `browse resume` — re-snapshot after user takeover, return control to agent
- `browse state save|load <name>` — save/restore browser state

Skills in headed mode: `/qa` runs its full test suite in the visible browser. `/design-review` takes screenshots in the real browser. All commands appear in the Side Panel activity feed.

## Quality Gates

- [ ] Pre-flight cleanup ran (stale server killed, profile locks cleared)
- [ ] `Mode: headed` confirmed in `browse status` output
- [ ] Port is 34567
- [ ] User has confirmed the Side Panel is visible
- [ ] Activity feed demo ran and the user saw commands appear
- [ ] User briefed on sidebar chat

## Outputs

- A visible headed Chromium window controlled by the agent
- Live activity feed in the gstack Side Panel
- Sidebar chat interface for natural-language browser control

## Feeds Into

- >browse (all browse commands run in the headed window)
- >qa (full QA suite visible in headed browser)
- >design-review (screenshots from real headed browser)

## Harness Notes

Requires the compiled browse binary and the gstack Chrome extension (in `extension/` directory). Uses Playwright's bundled Chromium, not the user's system Chrome. Port 34567 is hardcoded for the extension to auto-connect.

See harness-compat.md: **Browser Tooling** and **Headed Mode** sections.
