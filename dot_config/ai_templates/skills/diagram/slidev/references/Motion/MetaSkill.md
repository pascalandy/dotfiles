---
name: slidev-motion
description: Add motion and interactivity to Slidev -- click-revealed content (v-click, v-clicks, v-after, v-switch, v-motion), slide transitions, rough-style markers, drawing mode, direction-based styles, note click markers, and slide lifecycle hooks. USE WHEN v-click, v-clicks, v-after, v-switch, v-motion, click reveal, click counter, click animation, slide transition, page transition, rough marker, v-mark, underline marker, circle marker, drawing mode, drawings persist, direction style, forward delay, reverse delay, note click marker, onSlideEnter, onSlideLeave, slide hooks.
---

# Slidev Motion

Control how a slide *unfolds* during presentation: clicks, transitions, markers, drawings, and lifecycle.

## Core Concept

Motion in Slidev splits cleanly along *when* it fires:

- **On click** — `v-click`, `<v-clicks>`, click-phased highlights, rough markers, note `[click]` triggers.
- **On slide change** — page transitions configured via headmatter, frontmatter, or direction-specific styles.
- **On lifecycle** — `onSlideEnter()` / `onSlideLeave()` hooks run arbitrary logic.
- **Presenter-controlled freeform** — drawing mode (`C` key) lets the speaker sketch on top of the slide.

## Routing Inside This Sub-Skill

| Intent | Open |
|---|---|
| Reveal bullets on click, click counter, fade-in groups | [`references/core-animations.md`](references/core-animations.md) |
| Hand-drawn underline, circle, box markers | [`references/animation-rough-marker.md`](references/animation-rough-marker.md) |
| Presenter drawing mode and persistence | [`references/animation-drawing.md`](references/animation-drawing.md) |
| Highlight presenter notes line-by-line with `[click]` | [`references/animation-click-marker.md`](references/animation-click-marker.md) |
| Apply styles only when navigating forward / backward | [`references/style-direction.md`](references/style-direction.md) |
| `onSlideEnter`, `onSlideLeave`, slide lifecycle API | [`references/api-slide-hooks.md`](references/api-slide-hooks.md) |

## Canonical Patterns

**Reveal each bullet on click:**

```md
<v-clicks>

- First point
- Second point
- Third point

</v-clicks>
```

**Single element on the 2nd click:**

```md
<div v-click="2">Appears on click 2</div>
```

**Rough underline marker on click:**

```md
<span v-mark.underline>critical constraint</span>
<span v-mark="{ at: 3, type: 'circle', color: '#e11d48' }">timed + styled</span>
```

**Slide transition:**

```yaml
---
transition: slide-left
---
```

Deck-wide in headmatter, per-slide in frontmatter.

**Slide hook** (must live in a `<script setup>` block inside the slide, not top-level Markdown):

```vue
<script setup>
import { onSlideEnter, onSlideLeave } from '@slidev/client'

onSlideEnter(() => {
  // e.g. start a media clip or begin an animation
})
onSlideLeave(() => {
  // e.g. pause the clip, clean up timers
})
</script>
```

Do *not* use `onMounted` / `onUnmounted` -- the component instance persists while the slide is inactive, so those hooks won't fire at the right time.

## Output Contract

A good Motion output delivers:

1. The exact markup (`<v-clicks>`, `v-click="n"`, `v-mark.*`) ready to paste.
2. The transition name, *placed in the correct scope* (deck vs slide).
3. For hooks, the correct import path and the observation that hooks only fire inside the slide's own `<script setup>`.

## Click Counter Model

Slidev counts clicks per slide. Understanding the counter prevents animation bugs:

- `v-click` auto-assigns the next click index; `v-click="+1"` is relative, `v-click="3"` is absolute, `v-click="[2,5]"` is a visible range.
- `<v-clicks>` wraps and auto-assigns one click per direct child; `depth="2"` cascades into nested lists.
- `v-after` shows with the previous click (no increment).
- `<v-switch>` renders one `<template #n>` per click.
- `v-motion` drives `:initial → :enter`, and click-scoped keys like `:click-1`, `:click-2` advance with the same counter.
- Click-phased code highlighting (`{1|2-3|all}`) shares the same counter.
- Override total count with `clicks: N` in frontmatter; start at an offset with `clicksStart: N`.

See [`references/core-animations.md`](references/core-animations.md) for the full semantics.
