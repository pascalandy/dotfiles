---
name: slidev-theme
description: Customize Slidev presentation look — eject the current theme into the project, write scoped per-slide CSS, add icons from any Iconify set. USE WHEN slidev theme, custom theme, eject theme, slidev theme eject, scoped css, per slide style, style scoped, slidev icons, mdi icon, iconify, carbon icon, logos icon.
---

# Slidev Theme

Change how the deck looks — from a quick CSS tweak on one slide up to owning the full theme.

## Core Concept

Three levels of styling control, smallest to largest:

1. **Per-slide scoped CSS** — a `<style>` block inside a slide affects that slide only.
2. **Global styling** — deck-wide overrides via `style.css`, custom CSS in the project root, or CSS vars from the theme.
3. **Ejected theme** — copy the theme source into the project to edit layouts, components, and default styles directly.

Icons are orthogonal to theming: any [Iconify](https://iconify.design/) icon set is usable by writing `<mdi-foo />`, `<carbon-bar />`, `<logos-baz />`.

## Routing Inside This Sub-Skill

| Intent | Open |
|---|---|
| Eject the active theme into the project to modify it | [`references/tool-eject-theme.md`](references/tool-eject-theme.md) |
| Scoped `<style>` blocks inside a slide | [`references/style-scoped.md`](references/style-scoped.md) |
| Iconify icon usage (`<mdi-*>`, `<carbon-*>`, etc.) | [`references/style-icons.md`](references/style-icons.md) |

## Canonical Patterns

**Eject the theme:**

```bash
pnpm exec slidev theme eject
# copies theme into ./theme/, updates slides.md to use it
```

**Scoped style on one slide:**

```md
# My slide

<style>
h1 { color: var(--brand-red); font-family: 'IBM Plex Serif'; }
</style>
```

**Icons:**

```md
<mdi-github class="text-4xl" />
<logos-typescript-icon />
<carbon-ai-status class="text-blue-500" />
```

## Output Contract

A good Theme output delivers:

1. The narrowest tool for the job — never eject a theme if a scoped `<style>` or a CSS var override would do.
2. Correct icon prefix matching the icon set on [icones.js.org](https://icones.js.org).
3. When editing a theme, a note about locking the theme version (ejecting loses future theme updates).

## Selection Guide

| Goal | Level |
|---|---|
| One slide needs a different heading colour | Scoped CSS |
| The whole deck needs a brand font | Global `style.css` or CSS vars |
| Change a built-in layout's markup | Eject the theme |
| Ship the deck as its own theme package | Build a dedicated theme repo (see Slidev theme guide) |
