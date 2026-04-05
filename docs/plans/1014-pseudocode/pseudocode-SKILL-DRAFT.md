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
()=> user clicks "Place Order"
()=> while processing, show loading overlay on the cart
  ()=> if payment succeeds
    ()=> return to confirmation page with order number
    ()=> show estimated delivery date
  ()=> if card declined
    ()=> return to checkout with card field highlighted in red
    ()=> show message: "Payment failed — please try another card"
    ()=> other form fields stay filled
  ()=> if cart changed since page load
    ()=> show modal: "Some items changed. Review your updated cart."
    ()=> if user clicks "Review", scroll to changed items highlighted in yellow
// end-shorthand
```

### Dashboard with Data Loading

```js
// start-shorthand
()=> user logs in and lands on dashboard
  ()=> if first time ever, show onboarding tour overlay with 3 steps
  ()=> if returning user, return to dashboard directly
()=> while data loads, show skeleton loaders in each widget
  ()=> if all data loads, replace skeletons with charts and numbers
  ()=> if one widget fails, show "Couldn't load — Retry" in that widget with a retry link
  ()=> other widgets still work independently
  ()=> if everything fails, show full-page message: "We're having trouble. Try again in a moment."
()=> user clicks a chart
  ()=> chart expands to detail view with date range picker
// end-shorthand
```

### Search with Empty and Error States

```js
// start-shorthand
()=> user sees search bar with placeholder "Search projects..."
()=> user types a query
  ()=> while typing, wait 300ms pause then show results below the search bar
  ()=> if results found, show list with project name, owner, last updated
  ()=> if no results, show: "No projects match '[query]'. Try a different search."
  ()=> if search fails, show: "Search is temporarily unavailable" with a retry link
()=> if user clears the search bar, return to default view with recent projects
// end-shorthand
```

## Writing Tips

**One moment per line.** Each line is one thing the user sees or does.

```js
// Good -- one moment per line
// start-shorthand
()=> user fills out all required fields
()=> user clicks "Save"
()=> while saving, button shows spinner
()=> if success, return to the saved item page with a "Saved" banner
// end-shorthand

// Bad -- too much crammed in one line
// start-shorthand
()=> user fills out form, clicks save, gets redirected, and sees confirmation
// end-shorthand
```

**Use indentation for branches.** When the user experience forks, indent the paths.

```js
// start-shorthand
()=> user clicks "Delete Account"
()=> show confirmation modal: "This is permanent. Type your email to confirm."
  ()=> if user types email and clicks "Delete"
    ()=> while deleting, show spinner in the modal
    ()=> return to goodbye page: "Your account has been deleted"
  ()=> if user clicks "Cancel"
    ()=> modal closes, nothing changes
  ()=> if user closes the modal by clicking outside
    ()=> same as cancel — nothing changes
// end-shorthand
```

**Name every error the user could see.** The plan won't tell you these — but the user will encounter them.

```js
// start-shorthand
()=> user clicks "Upload File"
  ()=> if file is too large, show: "File must be under 10MB. Yours is [size]."
  ()=> if wrong file type, show: "Only PDF and PNG files are accepted."
  ()=> while uploading, show progress bar
    ()=> if upload fails mid-way, freeze progress bar at [X]% with "Upload failed — Retry"
  ()=> if success, show filename with a green checkmark and "Remove" link
// end-shorthand
```

## User States Checklist

For each user case, walk through what the user experiences in each state. This is where plans have gaps — the happy path is obvious, the rest is not.

| State | Ask yourself... |
|---|---|
| **Loading** | What does the user see while waiting? Spinner? Skeleton? Nothing? |
| **Empty** | What if there's no data yet? First-time user, empty list, no results? |
| **Error** | What does the user see when something fails? Can they retry? |
| **Partial** | What if some parts loaded and others didn't? |
| **Success** | What confirms the action worked? Banner, redirect, animation? |
| **Denied** | What if they don't have permission? What do they see instead? |
| **Repeat** | What if they do the same action twice? Double submit, back button? |
| **Slow** | What if the network is slow? Does the UI feel stuck? |

You don't need every state for every user case. But scanning this list before writing pseudocode will surface the flows your plan didn't cover.

## Format Notes

- Use ` ```js ` for all pseudocode blocks. JS syntax highlighting makes keywords pop in purple.
- `// start-shorthand` and `// end-shorthand` delimit pseudocode sections (rendered as comments).
- `()=>` marks each step. One user moment per line.
- Indentation (2 spaces) marks conditional branches — what happens when the experience forks.

### Keyword conventions

Use these JS keywords deliberately so they highlight and make flows scannable:

| Keyword | Use for | Example |
|---|---|---|
| `if` | conditional branch | `if payment fails, show error in red` |
| `return` | navigate to a page/screen | `return to dashboard with success banner` |
| `while` | loading / waiting / in-progress | `while uploading, show progress bar` |
| `in` | location on screen | `show error in the modal` |
| `with` | accompaniment | `return to page with confirmation banner` |
