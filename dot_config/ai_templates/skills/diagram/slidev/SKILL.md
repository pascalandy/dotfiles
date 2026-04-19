---
name: slidev
description: Build web-based developer slidedecks with Slidev — scaffold projects, author Markdown slides, embed live code (Monaco, magic-move, twoslash), add click animations and transitions, render Mermaid/PlantUML/LaTeX diagrams, run presenter mode with recording, customize themes, and export to PDF/PPTX/PNG or deploy as a SPA. USE WHEN slidev, sli.dev, pnpm create slidev, developer slides, technical presentation, conference talk, code walkthrough deck, live code slides, monaco slides, magic move, v-click, slidev layout, slidev theme, mermaid slides, plantuml slides, latex in slides, presenter mode, record presentation, export slidev pdf, slidev pptx, slidev spa, slidev deploy, slidev og image, slidev seo.
keywords: [slidev, sli.dev, slides, presentation, deck, monaco, magic-move, twoslash, v-click, mermaid, plantuml, latex, presenter, recording, pdf-export, pptx-export, spa, theme, vue, vite, markdown]
---

# Slidev

> Web-based slidedecks for developers, built on Vite + Vue + Markdown. Eight focused sub-skills routed automatically from intent.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Slidev is a large surface. A single deck touches scaffolding, Markdown syntax, Vue components, layouts, code highlighting, Monaco, magic-move, click animations, transitions, Mermaid/PlantUML/LaTeX, presenter mode, recording, themes, scoped CSS, icons, PDF/PPTX export, SPA hosting, SEO, OG images, and slide hooks. Asking an AI to "help me with Slidev" collapses that surface into a generic reply: vague code, mixed concerns, and usually the wrong mental model for what the user is actually doing -- are they *starting* a deck, *writing* a slide, *animating* something, or *shipping* the output?

The fix is to split Slidev along the natural workflow axes so the right specialist activates on the right intent, and only the slice of documentation relevant to that slice of work is loaded.

---

## The Solution

`slidev` is a meta-skill with eight specialists, each owning a distinct chunk of Slidev:

1. **Bootstrap** — scaffold a project, learn the CLI, configure deck-wide headmatter.
2. **Authoring** — Markdown syntax, slide separators, frontmatter, built-in layouts, Vue components, slots, draggable elements, canvas sizing.
3. **Code** — code blocks with line highlighting, magic-move transitions, Monaco editor (read/run/write), twoslash types, external snippet imports, code tabs, editor tooling.
4. **Motion** — `v-click` / `v-clicks`, click animations, slide transitions, rough markers, drawings, direction styles, slide lifecycle hooks.
5. **Diagrams** — Mermaid flowcharts, PlantUML diagrams, inline and block LaTeX math.
6. **Present** — presenter mode, camera recording, timers, remote control, notes with ruby text, global navigation context.
7. **Theme** — theme ejection, scoped CSS, icon usage, styling patterns.
8. **Ship** — PDF/PPTX/PNG export, SPA build, hosting, remote asset caching, OG images, SEO metadata.

The root `SKILL.md` (this file) loads `references/ROUTER.md`, which dispatches to exactly one sub-skill. Each sub-skill lives under `references/<Name>/MetaSkill.md` with its own `references/` directory holding only the topic files relevant to its domain.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Router | `references/ROUTER.md` | Intent → sub-skill dispatch table |
| Bootstrap skill | `references/Bootstrap/MetaSkill.md` | Scaffold a Slidev project, CLI, headmatter |
| Bootstrap references | `references/Bootstrap/references/` | core-cli, core-headmatter |
| Authoring skill | `references/Authoring/MetaSkill.md` | Markdown syntax, layouts, components, slots |
| Authoring references | `references/Authoring/references/` | core-syntax, core-frontmatter, core-layouts, core-components, layout-*, syntax-* |
| Code skill | `references/Code/MetaSkill.md` | Code blocks, Monaco, magic-move, twoslash |
| Code references | `references/Code/references/` | code-*, editor-* |
| Motion skill | `references/Motion/MetaSkill.md` | Click animations, transitions, markers, hooks |
| Motion references | `references/Motion/references/` | core-animations, animation-*, style-direction, api-slide-hooks |
| Diagrams skill | `references/Diagrams/MetaSkill.md` | Mermaid, PlantUML, LaTeX |
| Diagrams references | `references/Diagrams/references/` | diagram-mermaid, diagram-plantuml, diagram-latex |
| Present skill | `references/Present/MetaSkill.md` | Presenter mode, recording, timer, remote |
| Present references | `references/Present/references/` | presenter-*, core-global-context |
| Theme skill | `references/Theme/MetaSkill.md` | Eject theme, scoped CSS, icons |
| Theme references | `references/Theme/references/` | tool-eject-theme, style-scoped, style-icons |
| Ship skill | `references/Ship/MetaSkill.md` | Export, build, deploy, SEO, OG |
| Ship references | `references/Ship/references/` | core-exporting, core-hosting, build-* |

---

## When Each Specialist Activates

| Trigger phrase | Routes to |
|---|---|
| "create a slidev project", "pnpm create slidev", "new deck", "project structure" | Bootstrap |
| "add a slide", "two-cols layout", "frontmatter", "cover slide", "import another deck", "draggable", "canvas size" | Authoring |
| "code block", "line highlighting", "magic move", "monaco editor", "twoslash", "import snippet", "code tabs" | Code |
| "v-click", "click animation", "slide transition", "rough marker", "drawing mode", "onSlideEnter" | Motion |
| "mermaid", "plantuml", "latex", "equation" | Diagrams |
| "presenter mode", "record presentation", "timer", "remote control", "speaker notes" | Present |
| "custom theme", "eject theme", "scoped css", "icons" | Theme |
| "export pdf", "export pptx", "build spa", "deploy slidev", "og image", "seo meta" | Ship |

---

## Quick Start (abbreviated — see Bootstrap for full workflow)

```bash
pnpm create slidev
pnpm run dev          # opens http://localhost:3030
pnpm run build        # static SPA
pnpm run export       # PDF (needs playwright-chromium)
```

---

## Usage Examples

**Example 1 -- scaffolding a new deck**

> "I want to start a new slidev deck for a conference talk."

Routes to Bootstrap; output includes scaffolding commands, a sample `slides.md`, and deck-wide headmatter.

**Example 2 -- animating reveal-by-click**

> "How do I make each bullet appear on click?"

Routes to Motion; output is a `<v-clicks>` block with ready-to-paste markup and a note on the click counter.

**Example 3 -- exporting to PDF with a download link**

> "Export my deck to PDF and add a download button on the hosted site."

Routes to Ship; output installs `playwright-chromium`, runs `slidev export`, and sets `download: true` in headmatter.

---

## Harness Notes

This skill folder is portable. Every internal path is relative (`references/...`). No harness-specific tools are assumed — the skill only asks the assistant to read files and execute shell commands that Slidev itself documents.
