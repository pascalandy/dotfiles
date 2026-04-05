---
name: pseudocode
description: Expand plan user cases into step-by-step pseudocode describing what the user sees, does, and experiences at each moment. Use when a plan exists but user flows need more detail before implementation, when the user says "pseudocode this", "expand user cases", "walk through the flow", "detail the user journey", or when a plan's user cases section needs to go deeper without writing real code.
---

# Pseudocode — User Journey Detail

- Enrich a plan's user cases section with step-by-step pseudocode that describes **what the end user sees, does, and experiences** at each moment.
- Write from the user's perspective using `()=>` lines inside code blocks. Every line should be something you could point at on a screen. The agent interprets intent -- including typos, wrong terminology, and vague phrasing -- and figures out what you mean.
- This sits between a plan and implementation. The plan says *what* to build. Pseudocode walks through *what the user actually experiences* -- every screen, every click, every error state, every "what happens next."

## Examples

### Signup Form

```js
// start-shorthand
()=> `action` user lands on page [signup]
()=> user sees: email field, password field, `click` button [Create Account]
()=> `action` user types [email]
  ()=> if email format is wrong, show inline 'error' [Please enter a valid email]
  ()=> if email is already taken, show `warning` [Already registered — log in instead?] with a link
()=> `action` user types [password]
  ()=> if under 8 characters, 'warning' in red [8 characters minimum]
  ()=> while typing, strength `indicator` updates from red to yellow to green
()=> user `click` [Create Account]
  ()=> while submitting, `feedback` shows spinner with fields disabled
  ()=> if success, `return` to welcome page with [Check your email to verify]
  ()=> if server `error`, form stays filled with banner [Something went wrong. Please try again.]
// end-shorthand]
```

### Checkout Flow

```js
// start-shorthand
()=> user reviews cart with item names, quantities, and total
()=> user `click` [Place Order]
()=> while processing, `feedback` loading overlay on the cart
  ()=> if 'success' payment goes through
    ()=> `return` to confirmation page with [order number]
    ()=> `display` estimated delivery date
  ()=> if 'error' card declined
    ()=> `return` to checkout with card field in red
    ()=> 'error' [Payment failed — please try another card]
    ()=> other form fields stay filled
  ()=> if 'warning' cart changed since page load
    ()=> `modal` [Some items changed. Review your updated cart.]
    ()=> if user `click` [Review], scroll to changed items in yellow
// end-shorthand
```

### Dashboard with Data Loading

```js
// start-shorthand
()=> `action` user logs in and lands on page [dashboard]
  ()=> if first time ever, `modal` onboarding tour overlay with 3 steps
  ()=> if returning user, `return` to dashboard directly
()=> while data loads, `feedback` skeleton loaders in each widget
  ()=> if 'success' all data loads, `display` charts and numbers
  ()=> if 'error' one widget fails, show [Couldn't load — Retry] in that widget
  ()=> other widgets still work independently
  ()=> if 'error' everything fails, `display` full-page [We're having trouble. Try again in a moment.]
()=> user `click` a chart
  ()=> `display` detail view with date range picker
// end-shorthand
```

### Search with Empty and Error States

```js
// start-shorthand
()=> user sees search bar with [Search projects...]
()=> `input` user types a query
  ()=> while typing, wait 300ms then `display` results below the search bar
  ()=> if 'success' results found, `display` list with project name, owner, last updated
  ()=> if 'empty' no results, `display` [No projects match '[query]'. Try a different search.]
  ()=> if 'error' search fails, `display` [Search is temporarily unavailable] with a retry link
()=> if user clears search bar, `return` to default view with recent projects
// end-shorthand
```

## Writing Tips

**One moment per line.** Each line is one thing the user sees or does.

```js
// Good -- one moment per line
// start-shorthand
()=> `action` user fills out all required fields
()=> user `click` [Save]
()=> while saving, `feedback` spinner on button
()=> if 'success', `return` to saved item page with [Saved] banner
// end-shorthand

// Bad -- too much crammed in one line
// start-shorthand
()=> user fills out form, clicks save, gets redirected, and sees confirmation
// end-shorthand
```

**Use indentation for branches.** When the user experience forks, indent the paths.

```js
// start-shorthand
()=> user `click` [Delete Account]
()=> `modal` [This is permanent. Type your email to confirm.]
  ()=> if user `input` email and `click` [Delete]
    ()=> while deleting, `feedback` spinner in the modal
    ()=> `return` to goodbye page with [Your account has been deleted]
  ()=> if user `click` [Cancel]
    ()=> `dismiss` modal, nothing changes
  ()=> if user `click` outside the modal
    ()=> `dismiss` modal, nothing changes
// end-shorthand
```

**Name every error the user could see.** The plan won't tell you these — but the user will encounter them.

```js
// start-shorthand
()=> user `click` [Upload File]
  ()=> if 'error' file too large, 'error' [File must be under 10MB. Yours is [size].]
  ()=> if 'error' wrong file type, 'error' [Only PDF and PNG files are accepted.]
  ()=> while uploading, `indicator` progress bar
    ()=> if 'error' upload fails mid-way, `indicator` frozen at [X]% with [Upload failed — Retry]
  ()=> if 'success', `display` filename with green checkmark and [Remove] link
// end-shorthand
```

## User States Checklist

Before writing pseudocode for a user case, scan the tags below and ask: did I cover this state? Plans usually only cover `'success'`. The rest is where gaps hide.

| Tag to use | Ask yourself... |
|---|---|
| `while` + `` `feedback` `` | What does the user see while waiting? Spinner? Skeleton? Nothing? What if it's slow? |
| `'empty'` | What if there's no data yet? First-time user, empty list, no results? |
| `'error'` | What does the user see when something fails? Can they retry? What if only part of the page fails? |
| `'success'` | What confirms the action worked? Banner, redirect, animation? |
| `'warning'` | Is there something the user should know before proceeding? What if they repeat the same action twice? |
| `'denied'` | What if they don't have permission? What do they see instead? |
| `'info'` | Is there context the user needs that isn't an error or warning? |

## Syntax Reference

Use ` ```js ` for all pseudocode blocks. JS syntax highlighting gives you three visual layers that make flows scannable at a glance.

### Structure

- `// start-shorthand` and `// end-shorthand` — delimit pseudocode sections (gray, italic)
- `()=>` — marks each step. One user moment per line.
- Indentation (2 spaces) — conditional branches, what happens when the experience forks.

### Layer 1 — Backtick tags (green) — what's happening

Categorize the interaction type. Place before the thing it describes.

| Tag | Use for | Example |
|---|---|---|
| `` `action` `` | User does something | `` `action` user lands on page [settings] `` |
| `` `click` `` | User clicks/taps | `` user `click` [Save] `` |
| `` `input` `` | User types/enters data | `` `input` user types [email] `` |
| `` `return` `` | Navigate to a page | `` `return` to dashboard with [Saved] banner `` |
| `` `feedback` `` | System visual response | `` `feedback` spinner on button `` |
| `` `indicator` `` | State display element | `` `indicator` progress bar `` |
| `` `modal` `` | Popup/overlay appears | `` `modal` [Are you sure?] `` |
| `` `display` `` | Content renders/appears | `` `display` list with project name, owner `` |
| `` `dismiss` `` | User closes/removes | `` `dismiss` modal, nothing changes `` |
| `` `toggle` `` | User switches on/off | `` user `toggle` [Dark mode] `` |

### Layer 2 — Single-quote tags (yellow) — what state it's in

Mark the condition or severity. Place before the description.

| Tag | Use for | Example |
|---|---|---|
| `'error'` | Something failed | `` 'error' [Payment failed — try another card] `` |
| `'warning'` | Caution / attention | `` 'warning' in red [8 characters minimum] `` |
| `'success'` | Action completed | `` if 'success', `return` to confirmation page `` |
| `'empty'` | No data / first time | `` if 'empty' no results, `display` [No matches found] `` |
| `'info'` | Informational message | `` 'info' [Your trial ends in 3 days] `` |
| `'disabled'` | Element not interactive | `` 'disabled' submit button until form is valid `` |
| `'denied'` | No permission | `` if 'denied', `display` [You don't have access] `` |

### Layer 3 — JS keywords (purple) — flow control

These highlight automatically. Use them to control the flow.

| Keyword | Use for | Example |
|---|---|---|
| `if` | Conditional branch | `if email is taken, show 'warning'` |
| `while` | Loading / waiting | `while submitting, `feedback` spinner` |
| `return` | Navigate (as keyword) | `return to default view` |
| `in` | Location on screen | `show 'error' in the modal` |
| `with` | Accompaniment | `return to page with [Saved] banner` |

### Layer 4 — Square brackets — UI content

Wrap any text the user literally sees on screen: button labels, page names, error messages, field names.

| Usage | Example |
|---|---|
| Button label | `` user `click` [Create Account] `` |
| Page name | `` `action` user lands on page [signup] `` |
| Error message | `` 'error' [File must be under 10MB] `` |
| Field name | `` `input` user types [email] `` |
| Banner text | `` `return` to page with [Changes saved] `` |
