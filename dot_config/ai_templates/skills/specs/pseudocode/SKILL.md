---
name: pseudocode
description: Expand plan user cases into step-by-step pseudocode describing what the user sees, does, and experiences at each moment. Use when a plan exists but user flows need more detail before implementation, when the user says "pseudocode this", "expand user cases", "walk through the flow", "detail the user journey", or when a plan's user cases section needs to go deeper without writing real code.
---

# Pseudocode — User Journey Detail

Enrich a plan's user cases section with step-by-step pseudocode that describes **what the end user sees, does, and experiences** at each moment.

Write from the user's perspective using `()=>` lines inside code blocks. Every line should be something you could point at on a screen. Interpret intent -- including typos, wrong terminology, and vague phrasing -- and figure out what the user means.

This sits between a plan and implementation. The plan says *what* to build. Pseudocode walks through *what the user actually experiences* -- every screen, every click, every error state, every "what happens next."

## Workflow

1. Read the plan's user cases section (or accept a feature description).
2. For each user case, write a ````js` block with `// start-shorthand` / `// end-shorthand` delimiters.
3. Walk through the flow moment by moment using `()=>` lines.
4. Cover every state from the **User States Checklist** below -- plans usually only cover `'success'`. The rest is where gaps hide.
5. Use indentation (2 spaces) for conditional branches.
6. One user moment per line. Never cram multiple actions into one line.

## Examples

### CLI Script -- YouTube Transcript Pipeline

```js
// start-shorthand
()=> `input` user provides a ["YouTube URL"] as argument
  ()=> if 'error' URL is missing ["Usage -- transcript {youtube-url}"]
  ()=> if 'error' URL is not a valid YouTube link ["Invalid YouTube URL"]

// step 1 -- download audio
()=> while downloading, `feedback` ["Downloading audio from YouTube..."]
  ()=> if 'error' video not found or private ["Video unavailable -- check the URL"]
  ()=> if 'error' download fails ["Download failed -- retrying..."] then retry 3x times
  ()=> if 'success' ["Audio saved -- /tmp/audio-{id}.mp3"]

// step 2 -- transcribe via DeepGram
()=> while transcribing, `feedback` ["Sending audio to DeepGram API..."]
  ()=> if 'error' API key missing ["DEEPGRAM_API_KEY not set"]
  ()=> if 'error' API returns 4xx or 5xx ["DeepGram error {status} -- {message}"]
  ()=> if 'success' ["Transcript ready"]
    ()=> save raw transcript as ["transcript-{id}.txt"]
    ()=> save JSON with timestamps as ["transcript-{id}.json"]

// step 3 -- summarize via OpenCode headless
()=> while processing, `feedback` ["Running OpenCode to generate summary..."]
  ()=> `input` pass transcript + prompt to opencode in headless mode
  ()=> if 'error' opencode not found ["opencode CLI not installed"]
  ()=> if 'error' model fails or times out ["Summary generation failed -- transcript files still available"]
  ()=> if 'success', save markdown as ["summary-{id}.md"]
    ()=> `feedback` ["Done -- files saved"]
    ()=> `feedback` ["transcript-{id}.txt"]
    ()=> `feedback` ["transcript-{id}.json"]
    ()=> `feedback` ["summary-{id}.md"]
// end-shorthand
```

### Signup Form

```js
// start-shorthand
()=> `action` user lands on page ["signup"]
()=> user sees: email field, password field, `click` button ["Create Account"]
()=> `action` user types ["email"]
  ()=> if email format is wrong, show inline 'error' ["Please enter a valid email"]
  ()=> if email is already taken, show `warning` ["Already registered -- log in instead?"] with a link
()=> `action` user types ["password"]
  ()=> if under 8 characters, 'warning' in red ["8 characters minimum"]
  ()=> while typing, strength `indicator` updates from red to yellow to green
()=> user `click` ["Create Account"]
  ()=> while submitting, `feedback` shows spinner with fields disabled
  ()=> if success, `return` to welcome page with ["Check your email to verify"]
  ()=> if server `error`, form stays filled with banner ["Something went wrong. Please try again."]
// end-shorthand
```

### Checkout Flow

```js
// start-shorthand
()=> user reviews cart with item names, quantities, and total
()=> user `click` ["Place Order"]
()=> while processing, `feedback` loading overlay on the cart
  ()=> if 'success' payment goes through
    ()=> `return` to confirmation page with ["order number"]
    ()=> ["estimated delivery date"]
  ()=> if 'error' card declined
    ()=> `return` to checkout with card field in red
    ()=> 'error' ["Payment failed -- please try another card"]
    ()=> other form fields stay filled
  ()=> if 'warning' cart changed since page load
    ()=> `modal` ["Some items changed. Review your updated cart."]
    ()=> if user `click` ["Review"], scroll to changed items in yellow
// end-shorthand
```

## Writing Rules

**One moment per line.** Each line is one thing the user sees or does.

```js
// Good -- one moment per line
// start-shorthand
()=> `action` user fills out all required fields
()=> user `click` ["Save"]
()=> while saving, `feedback` spinner on button
()=> if 'success', `return` to saved item page with ["Saved"] banner
// end-shorthand

// Bad -- too much crammed in one line
// start-shorthand
()=> user fills out form, clicks save, gets redirected, and sees confirmation
// end-shorthand
```

**Use indentation for branches.** When the user experience forks, indent the paths.

```js
// start-shorthand
()=> user `click` ["Delete Account"]
()=> `modal` ["This is permanent. Type your email to confirm."]
  ()=> if user `input` email and `click` ["Delete"]
    ()=> while deleting, `feedback` spinner in the modal
    ()=> `return` to goodbye page with ["Your account has been deleted"]
  ()=> if user `click` ["Cancel"]
    ()=> `dismiss` modal, nothing changes
  ()=> if user `click` outside the modal
    ()=> `dismiss` modal, nothing changes
// end-shorthand
```

**Name every error the user could see.** The plan won't tell you these -- but the user will encounter them.

```js
// start-shorthand
()=> user `click` ["Upload File"]
  ()=> if 'error' file too large ["File must be under 10MB. Yours is {size}."]
  ()=> if 'error' wrong file type ["Only PDF and PNG files are accepted."]
  ()=> while uploading, `indicator` progress bar
    ()=> if 'error' upload fails mid-way, `indicator` frozen at ["X"]% with ["Upload failed -- Retry"]
  ()=> if 'success', filename with green checkmark and ["Remove"] link
// end-shorthand
```

## Syntax Reference

Use ` ```js ` for all pseudocode blocks. JS syntax highlighting gives three visual layers that make flows scannable at a glance.

### Structure

- `// start-shorthand` and `// end-shorthand` -- delimit pseudocode sections (gray, italic)
- `()=>` -- marks each step. One user moment per line.
- Indentation (2 spaces) -- conditional branches, what happens when the experience forks.
- **Avoid breaking JS highlighting** -- no `<>` angle brackets (use `{}` for variables), no nested `[""]`.

### Layer 1 -- Backtick tags (green) -- what's happening

Categorize the interaction type. Place before the thing it describes.

| Tag | Use for | Example |
|---|---|---|
| `` `action` `` | User does something | `` `action` user lands on page ["settings"] `` |
| `` `click` `` | User clicks/taps | `` user `click` ["Save"] `` |
| `` `input` `` | User types/enters data | `` `input` user types ["email"] `` |
| `` `return` `` | Navigate to a page | `` `return` to dashboard with ["Saved"] banner `` |
| `` `feedback` `` | System visual response | `` `feedback` spinner on button `` |
| `` `indicator` `` | State display element | `` `indicator` progress bar `` |
| `` `modal` `` | Popup/overlay appears | `` `modal` ["Are you sure?"] `` |
| `` `display` `` | Content renders | `` `display` detail view with date range picker `` |
| `` `dismiss` `` | User closes/removes | `` `dismiss` modal, nothing changes `` |
| `` `toggle` `` | User switches on/off | `` user `toggle` ["Dark mode"] `` |

### Layer 2 -- Single-quote tags (yellow) -- what state it's in

Mark the condition or severity. Place before the description.

| Tag | Use for | Example |
|---|---|---|
| `'error'` | Something failed | `` 'error' ["Payment failed -- try another card"] `` |
| `'warning'` | Caution / attention | `` 'warning' in red ["8 characters minimum"] `` |
| `'success'` | Action completed | `` if 'success', `return` to confirmation page `` |
| `'empty'` | No data / first time | `` if 'empty' no results ["No matches found"] `` |
| `'info'` | Informational message | `` 'info' ["Your trial ends in 3 days"] `` |
| `'disabled'` | Element not interactive | `` 'disabled' submit button until form is valid `` |
| `'denied'` | No permission | `` if 'denied' ["You don't have access"] `` |

### Layer 3 -- JS keywords (purple) -- flow control

These highlight automatically. Use them to control the flow.

| Keyword | Use for | Example |
|---|---|---|
| `if` | Conditional branch | `if email is taken, show 'warning'` |
| `while` | Loading / waiting | `` while submitting, `feedback` spinner `` |
| `in` | Location on screen | `show 'error' in the modal` |
| `with` | Accompaniment | `return to page with ["Saved"] banner` |

### Layer 4 -- Square brackets -- UI content

Wrap any text the user literally sees on screen: button labels, page names, error messages, field names.

| Usage | Example |
|---|---|
| Button label | `` user `click` ["Create Account"] `` |
| Page name | `` `action` user lands on page ["signup"] `` |
| Error message | `` 'error' ["File must be under 10MB"] `` |
| Field name | `` `input` user types ["email"] `` |
| Banner text | `` `return` to page with ["Changes saved"] `` |

## User States Checklist

Before writing pseudocode for a user case, scan these tags and ask: did I cover this state?

| Tag to use | Ask yourself... |
|---|---|
| `while` + `` `feedback` `` | What does the user see while waiting? Spinner? Skeleton? Nothing? What if it's slow? |
| `'empty'` | What if there's no data yet? First-time user, empty list, no results? |
| `'error'` | What does the user see when something fails? Can they retry? What if only part of the page fails? |
| `'success'` | What confirms the action worked? Banner, redirect, animation? |
| `'warning'` | Is there something the user should know before proceeding? What if they repeat the same action twice? |
| `'denied'` | What if they don't have permission? What do they see instead? |
| `'info'` | Is there context the user needs that isn't an error or warning? |
