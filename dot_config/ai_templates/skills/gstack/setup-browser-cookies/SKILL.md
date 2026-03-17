---
name: setup-browser-cookies
version: 1.0.0
description: |
  Import cookies from your real browser (Comet, Chrome, Arc, Brave, Edge) into the
  headless browse session. Opens an interactive picker UI where you select which
  cookie domains to import. Use before QA testing authenticated pages.
---

## Preamble (run first)

```bash
_BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
echo "BRANCH: $_BRANCH"
```

## Assistant Compatibility

- Treat references like `/ship` or `/review` as workflow names, not as a requirement for slash-command support.
- When these instructions say `AskUserQuestion`, ask the user directly using the current assistant's native interaction flow.
- When these instructions mention `CLAUDE.md`, interpret that as the project's assistant guidance file, such as `AGENTS.md`, `CLAUDE.md`, or an equivalent instructions document.
- If a helper path assumes a specific assistant install layout, prefer the local skill directory first and then fall back to the current assistant's standard skill location.

## User Questions

When you have any questions, use skill `ask-questions`.


# Setup Browser Cookies

Import logged-in sessions from your real Chromium browser into the headless browse session.

## How it works

1. Find the browse binary
2. Run `cookie-import-browser` to detect installed browsers and open the picker UI
3. User selects which cookie domains to import in their browser
4. Cookies are decrypted and loaded into the Playwright session

## Steps

### 1. Find the browse binary

## SETUP (run this check BEFORE any browse command)

```bash
_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
B=""
for _candidate in \
  "${GSTACK_BROWSE_BIN:-}" \
  "$_ROOT/.opencode/skill/gstack/browse/dist/browse" \
  "$_ROOT/.opencode/skills/gstack/browse/dist/browse" \
  "$_ROOT/.claude/skills/gstack/browse/dist/browse" \
  "$HOME/.config/opencode/skill/gstack/browse/dist/browse" \
  "$HOME/.config/opencode/skills/gstack/browse/dist/browse" \
  "$HOME/.opencode/skill/gstack/browse/dist/browse" \
  "$HOME/.opencode/skills/gstack/browse/dist/browse" \
  "$HOME/.claude/skills/gstack/browse/dist/browse"
do
  [ -n "$_candidate" ] && [ -x "$_candidate" ] && B="$_candidate" && break
done
[ -z "$B" ] && [ -n "${GSTACK_ROOT:-}" ] && [ -x "${GSTACK_ROOT}/browse/dist/browse" ] && B="${GSTACK_ROOT}/browse/dist/browse"
if [ -n "$B" ]; then
  echo "READY: $B"
else
  echo "NEEDS_SETUP"
fi
```

If `NEEDS_SETUP`:
1. Tell the user: "gstack browse is not available in any supported install path yet."
2. If they have a full gstack checkout, run its one-time setup: `cd <gstack-root> && ./setup`
3. If they only have this vendored prompt bundle, set `GSTACK_BROWSE_BIN` to a compiled `browse` binary path, or install a full gstack checkout first.
4. If `bun` is not installed and a build is needed: `curl -fsSL https://bun.sh/install | bash`

### 2. Open the cookie picker

```bash
$B cookie-import-browser
```

This auto-detects installed Chromium browsers (Comet, Chrome, Arc, Brave, Edge) and opens
an interactive picker UI in your default browser where you can:
- Switch between installed browsers
- Search domains
- Click "+" to import a domain's cookies
- Click trash to remove imported cookies

Tell the user: **"Cookie picker opened — select the domains you want to import in your browser, then tell me when you're done."**

### 3. Direct import (alternative)

If the user specifies a domain directly (e.g., `/setup-browser-cookies github.com`), skip the UI:

```bash
$B cookie-import-browser comet --domain github.com
```

Replace `comet` with the appropriate browser if specified.

### 4. Verify

After the user confirms they're done:

```bash
$B cookies
```

Show the user a summary of imported cookies (domain counts).

## Notes

- First import per browser may trigger a macOS Keychain dialog — click "Allow" / "Always Allow"
- Cookie picker is served on the same port as the browse server (no extra process)
- Only domain names and cookie counts are shown in the UI — no cookie values are exposed
- The browse session persists cookies between commands, so imported cookies work immediately
