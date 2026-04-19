---
name: slidev-present
description: Run a Slidev deck live — presenter mode, camera recording, timer, remote control, presenter notes (with ruby text), and the navigation/global-context API. USE WHEN presenter mode, record presentation, camera overlay, slidev timer, countdown, duration, slidev remote, remote control, speaker notes, presenter notes, ruby text notes, notesAutoRuby, $nav, $slidev, navigation api, useNav, global context.
---

# Slidev Present

Everything the presenter needs during the live show.

## Core Concept

When `slidev` is running, two surfaces coexist:

- **Audience view** (default) — the slides themselves.
- **Presenter view** (`/presenter`) — next slide preview, notes, timer, drawing tools, camera overlay, click counter.

Both views share the same navigation state through `$nav` / `$slidev`, and both respect the same keyboard shortcuts. The presenter can also hand the clicker off to a phone via `--remote`.

## Routing Inside This Sub-Skill

| Intent | Open |
|---|---|
| Overlay a camera feed and record the talk (WebRTC + RecordRTC) | [`references/presenter-recording.md`](references/presenter-recording.md) |
| Show a timer or countdown (`duration`, `timer`) | [`references/presenter-timer.md`](references/presenter-timer.md) |
| Control the deck from a phone over LAN | [`references/presenter-remote.md`](references/presenter-remote.md) |
| Auto-render Japanese ruby text in notes | [`references/presenter-notes-ruby.md`](references/presenter-notes-ruby.md) |
| `$nav`, `$slidev`, `useNav()`, slide/click state API | [`references/core-global-context.md`](references/core-global-context.md) |

## Canonical Patterns

**Start presenter mode:**

```bash
pnpm run dev
# open http://localhost:3030/presenter in a second tab/window
```

**Start with remote control enabled:**

```bash
slidev --remote                 # open access
slidev --remote mypassword      # password-gated
# opens /remote on LAN; visit from a phone on the same network
```

**Speaker notes (HTML comment on a slide):**

```md
# My slide

Some content

<!--
Emphasise point 1 here.
Click [click] to reveal the next bullet.
-->
```

**Timer and duration** (duration takes a time string with a unit):

```yaml
---
duration: 30min       # default unit is minutes; '1h' or '45min' also valid
timer: countdown      # 'stopwatch' (default) or 'countdown'
---
```

**Read current nav state inside a slide (template variables — no import needed):**

```md
On slide {{ $nav.currentPage }} of {{ $nav.total }}
```

**Or via composable in `<script setup>`:**

```vue
<script setup>
import { useNav } from '@slidev/client'
const nav = useNav()
</script>

<div>Layout: {{ nav.currentLayout }}</div>
```

## Output Contract

A good Present output delivers:

1. The keyboard shortcut or CLI flag that performs the task (no guessed shortcuts).
2. Correct scope for `duration` / `timer` (headmatter for deck-wide, frontmatter for a single slide).
3. A verified API reference when proposing `$nav` / `$slidev` access (see [`references/core-global-context.md`](references/core-global-context.md)).
4. Awareness that remote mode requires clients on the same LAN.

## Controls

| Action | How |
|---|---|
| Start drawing mode | Press `C` or click the pen icon in the nav bar |
| Show camera overlay | Click the camera icon in the nav bar |
| Start recording | Click the video (record) icon in the nav bar |
| Navigate | Arrow keys, space, or click the nav arrows |

Only the controls above are guaranteed by the Slidev references shipped with this skill. For the complete keybinding map (fullscreen, dark mode, goto, etc.), check the live dev-server UI or Slidev's official docs.
