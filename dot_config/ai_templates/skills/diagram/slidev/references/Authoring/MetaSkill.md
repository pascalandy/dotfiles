---
name: slidev-authoring
description: Author Slidev slides — Markdown syntax, per-slide frontmatter, built-in layouts, Vue components, slots, draggable elements, canvas and zoom controls, and multi-file deck composition. USE WHEN add slide, slide separator, slide frontmatter, cover slide, two-cols, image layout, iframe layout, quote, section, fact, statement, intro, end layout, slot syntax, ::right::, ::default::, v-drag, draggable element, canvas size, aspect ratio, zoom slide, transform scale, global-top, global-bottom, import slides, comark, mdc, block frontmatter, frontmatter merging.
---

# Slidev Authoring

Write the content of the deck: slides, layouts, components, and cross-file composition.

## Core Concept

A Slidev deck is a chain of Markdown slides separated by `---`. Each slide may have its own frontmatter block, a layout, slots for multi-column content, and embedded Vue components. The *entire deck* can be split across multiple `.md` files and reassembled with `src:` imports.

## Routing Inside This Sub-Skill

| Intent | Open |
|---|---|
| Markdown separators, headmatter vs frontmatter, notes, code blocks | [`references/core-syntax.md`](references/core-syntax.md) |
| Per-slide frontmatter keys (`layout`, `background`, `class`, `transition`, `clicks`, etc.) | [`references/core-frontmatter.md`](references/core-frontmatter.md) |
| All built-in layouts with their slot names | [`references/core-layouts.md`](references/core-layouts.md) |
| Built-in Vue components (`<Tweet>`, `<Youtube>`, `<Toc>`, `<Arrow>`, etc.) | [`references/core-components.md`](references/core-components.md) |
| Canvas width + aspect ratio | [`references/layout-canvas-size.md`](references/layout-canvas-size.md) |
| Zoom a single slide | [`references/layout-zoom.md`](references/layout-zoom.md) |
| Scale arbitrary elements with `<Transform :scale>` | [`references/layout-transform.md`](references/layout-transform.md) |
| Layout slots (`::default::`, `::right::`) | [`references/layout-slots.md`](references/layout-slots.md) |
| Global layers (`global-top.vue`, `global-bottom.vue`) | [`references/layout-global-layers.md`](references/layout-global-layers.md) |
| Draggable elements (`v-drag`, `<v-drag>`) | [`references/layout-draggable.md`](references/layout-draggable.md) |
| Comark inline styles, attributes, and components (`comark: true`) | [`references/syntax-mdc.md`](references/syntax-mdc.md) |
| Block frontmatter declared in a fenced `yaml` block | [`references/syntax-block-frontmatter.md`](references/syntax-block-frontmatter.md) |
| Import slides from another file (`src:`) | [`references/syntax-importing-slides.md`](references/syntax-importing-slides.md) |
| How frontmatter merges between imported and importing slides | [`references/syntax-frontmatter-merging.md`](references/syntax-frontmatter-merging.md) |

## Canonical Slide Shape

```md
---
layout: two-cols
class: text-sm
transition: fade
---

# Left column content

::right::

# Right column content

<!-- Presenter notes here -->
```

- `---` on its own line separates slides
- First block = *headmatter* (deck config); all others = *frontmatter* (slide config)
- `::slot::` lines split layout slots
- HTML comments become presenter notes

## Output Contract

A good Authoring output delivers:

1. A correctly formatted Markdown snippet that drops into `slides.md` and renders as intended.
2. The right layout for the content (never forcing `default` when `two-cols`, `image-left`, or `cover` fits).
3. Slot syntax when layouts require it.
4. No leakage into deck-wide headmatter — per-slide changes stay in per-slide frontmatter.

## Common Layouts Quick Map

| Goal | Layout |
|---|---|
| Title/cover | `cover` |
| Centered content | `center` |
| Two columns of content | `two-cols` (use `::right::`) |
| Header row over two columns | `two-cols-header` |
| Full-bleed image | `image` / `image-left` / `image-right` |
| Embed external page | `iframe` / `iframe-left` / `iframe-right` |
| Pull quote | `quote` |
| Section divider | `section` |
| Data/statement emphasis | `fact` / `statement` |
| First/last slide | `intro` / `end` |

Full list and slot names → [`references/core-layouts.md`](references/core-layouts.md).

## Examples

**Two-column comparison:**

```md
---
layout: two-cols
---

## Before

REST with 12 endpoints

::right::

## After

GraphQL with 1 endpoint
```

**Importable sub-deck:**

```md
---
src: ./chapters/intro.md
---
```

**Draggable element with persisted position** (position keyed by frontmatter):

```md
---
dragPos:
  logo: 120,80,200,_
---

<v-drag pos="logo">
  Drag me anywhere
</v-drag>
```

`_` (or `NaN`) in the Height slot means "auto-size". The five slots are `Left,Top,Width,Height,Rotate`.
