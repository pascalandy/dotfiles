# Setup Browser Cookies

> Import logged-in sessions from your real Chromium browser into the headless browse session so QA tests can access authenticated pages.

## When to Use

- Before QA testing pages that require authentication
- User asks to "import cookies", "login to the site", "authenticate the browser"
- Running `/qa` on a site that requires a logged-in session
- Headless browse can navigate to a page but hits a login wall

Do NOT run if browse is already in CDP mode (connected to the user's real browser via `connect-chrome`) — in that case, real browser cookies are already available.

## Inputs

- An installed Chromium-based browser with an active session for the target site
- Optional: specific domain to import directly (skips the picker UI)

## Methodology

### Step 0: CDP mode check

First check if browse is already connected to the user's real browser:

```bash
browse status | grep "Mode: cdp"
```

If CDP mode is active: tell the user no cookie import is needed. Stop.

### Step 1: Find the browse binary

Same setup check as all browse skills — verify the binary exists. Build with `./setup` if missing.

### Step 2: Open the cookie picker

Run `browse cookie-import-browser`.

This command:
1. Auto-detects installed Chromium browsers (Chrome, Comet, Brave, Arc, Edge, etc.)
2. Opens an interactive picker UI in the user's default browser
3. Shows available domains with cookie counts (no cookie values exposed)
4. Lets the user switch between browsers, search domains, click "+" to import, click trash to remove

Tell the user: "Cookie picker opened — select the domains you want to import in your browser, then tell me when you're done."

Wait for user confirmation before proceeding.

### Step 3: Direct import (alternative)

If the user specifies a domain directly, skip the UI:

```bash
browse cookie-import-browser comet --domain github.com
```

Replace `comet` with the appropriate browser name if specified.

### Step 4: Verify

After the user confirms they're done:

```bash
browse cookies
```

Show the user a summary of imported cookies by domain and count.

## Quality Gates

- [ ] CDP mode check passed (not in CDP mode)
- [ ] Cookie picker opened successfully or direct import ran
- [ ] User confirmed import is complete
- [ ] `browse cookies` output shows expected domains
- [ ] Imported cookies verified by navigating to an authenticated page

## Outputs

- Cookies loaded into the Playwright session (persists for the session)
- Summary of imported domains and cookie counts

## Platform Notes

- macOS: first import per browser may trigger a Keychain dialog — click "Allow" or "Always Allow"
- Linux: v11 cookies may require `secret-tool`/libsecret access; v10 cookies use Chromium's standard fallback key
- Cookie picker is served on the same port as the browse server (no extra process)
- Cookie values are never shown in the UI, only domain names and counts
- Imported cookies persist between browse commands for the duration of the session

## Feeds Into

- >browse (authenticated QA testing)
- >qa (full test suite against authenticated pages)

## Harness Notes

Requires the compiled browse binary. The cookie picker UI opens in the user's default browser (not the headless Playwright session). Requires interaction: the agent runs the command and then waits for the user to make selections in their browser.

See harness-compat.md: **Browser Tooling** section.
