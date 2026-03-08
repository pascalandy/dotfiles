---
name: frontend-design-codex
description: Use this skill for redesigning or reviewing frontend UI that should look less AI-generated and more like a real product team shipped it, especially dashboards, admin panels, settings, billing pages, landing pages, and components that feel too glossy, rounded, gradient-heavy, glassy, pill-shaped, or generic SaaS. Reach for it when the user says uncodixify, make it look normal, calmer, more human-designed, more product-specific, or less template-like. It replaces default AI UI moves with grounded layouts, direct hierarchy, existing project tokens first, and restrained fallback palette guidance via color-palette-frappe.
---

# Frontend Design Codex

This skill exists to **uncodixify** frontend work.

The default failure mode for AI-made UI is recognizable: soft gradients, floating cards, pill-shaped everything, eyebrow labels, glossy dark dashboards, fake KPI grids, oversized radii, decorative copy, and layouts that look “premium” instead of useful.

Your job is to notice those easy moves and choose the cleaner option.

The goal is not to make the UI bland. The goal is to make it feel **product-specific, human-directed, and structurally honest**.

## Use this skill for

Use this skill when the task involves:

- building or restyling web UI
- redesigning dashboards, admin panels, settings pages, billing pages, data tables, or app shells
- reviewing an interface that feels AI-generated, too rounded, too glossy, too blue, too gradient-heavy, or too generic
- translating a rough mockup into cleaner production UI
- turning generated frontend code into something that feels more like a real product team shipped it

Do **not** default to this skill for:

- SEO audits
- copywriting
- generic frontend debugging with no visual or UX direction problem
- architecture/spec work without UI implementation or review

## Operating mode

Before changing code, do four things.

### 1. Read the product context

Figure out what kind of surface you are designing:

- **internal product UI**
  - prioritize workflow, hierarchy, density, and predictable navigation
- **marketing or landing page**
  - use proper page sections, but still avoid empty gloss and startup filler
- **settings, billing, CRUD, or data-heavy screens**
  - optimize for clarity first, personality second

If the repo already exists, inspect a few relevant files before designing:

- current colors and CSS variables
- typography choices
- spacing scale
- border radius usage
- layout patterns
- existing components and states

Match the product before inventing anything.

### 2. Reuse existing tokens first

Color priority:

- use the project’s current palette if one exists
- if no palette exists, use restrained inspiration from the **`color-palette-frappe`** skill
- do not invent random color systems just to make the screen look designed

Typography priority:

- keep the existing product fonts if they exist
- if no fonts are defined, choose something restrained and credible for the product
- do not reach for a font just because it is the usual AI default or because it signals fake “premium”

### 3. Choose the correct layout family

Do not invent a novel structure when a standard one fits.

For **internal UI**, prefer familiar patterns:

- fixed sidebar or top nav when information architecture needs it
- plain page title row
- controls row for filters and actions
- main work surface for table, list, editor, or details
- secondary panel only when it has a real job

For **landing pages**, use real sections:

- hero when appropriate
- proof or credibility block
- features or use cases
- CTA section
- footer

For **dashboards**, do not begin with “three metric cards and a fake chart” unless the product truly revolves around monitoring.

### 4. Name the easy AI move, then reject it

Before finalizing a direction, quickly identify the low-effort pattern you are tempted to use:

- floating shell
- glow card
- giant rounded panel
- hero strip inside a dashboard
- decorative micro-copy block
- gradient badge
- fake analytics filler

Then pick the more grounded alternative.

## Core design standard

When in doubt, keep things **normal** in the best sense:

- calm colors
- direct hierarchy
- predictable layout
- small, functional radii
- subtle borders
- restrained shadows
- simple interactions
- copy that labels the UI instead of narrating it

Think more **GitHub, Linear, Raycast, Stripe**.
Think less “generic dark SaaS template generated in one shot.”

## Defaults to prefer

Read `references/normal-defaults.md` when implementing or reviewing UI.

Use those defaults as the baseline for:

- spacing
- radius
- shadows
- transitions
- cards
- forms
- tables
- tabs
- sidebars
- headers
- layout shells

## Anti-patterns to ban

Read `references/anti-patterns.md` when the UI feels even slightly AI-generated, especially for dark dashboards and admin screens.

That file contains:

- the hard no list
- the specifically banned patterns
- the common structural mistakes this skill exists to prevent

## Product-specific guidance

### Internal product UI

Be strict here.

Avoid:

- hero sections inside the product
- eyebrow labels above headings
- decorative status blurbs
- KPI-card grids as the first instinct
- fake charts used to fill a hole in the layout
- right rails that exist only to make the page feel expensive

Prefer:

- dense but readable rows
- real filters
- meaningful table columns
- visible actions
- clear empty states
- useful side navigation only when needed

### Landing pages

Landing pages can be larger and more expressive, but still stay honest.

Allowed:

- proper section-based structure
- a real hero
- stronger contrast or art direction if it fits the brand

Still avoid:

- decorative gradients with no brand reason
- badges and pills everywhere
- filler copy that says nothing
- fake app screenshots full of invented metrics

### Review tasks

If the user asks for a UI review, audit the design in this order:

1. layout honesty
2. hierarchy clarity
3. component consistency
4. color restraint
5. copy usefulness
6. motion restraint
7. accessibility risks

When you critique, do not just say “looks AI-generated.”
Name the exact pattern and give the replacement:

- “Replace the floating sidebar shell with a fixed 248px rail and border-right.”
- “Drop the eyebrow label and use a plain page title with one supporting sentence.”
- “Convert the KPI cards into a table and recent-items list because the workflow is operational, not analytical.”

## Copy rules

UI copy should be functional.

Prefer:

- direct labels
- short helper text
- realistic statuses
- headings that identify the page or task

Avoid:

- ornamental micro-copy
- mini manifestos in cards
- vague “clarity / control / pulse / focus” language
- decorative `<small>` heading patterns that exist only for vibe

One real heading is better than a heading stack made of:

- eyebrow label
- big headline
- soft paragraph explaining the obvious

## Motion rules

Use motion only when it improves comprehension.

Prefer:

- color changes
- opacity changes
- short duration transitions
- focus and hover states that do not move the layout

Avoid:

- bounce
- slide-in theatrics
- translate-on-hover navigation
- motion whose only job is to feel premium

## Color rules

Keep colors calm.

- avoid blue-leaning “AI dark mode” unless the product already uses it
- prefer muted, grounded colors over neon accents
- use one accent family with discipline
- let contrast come from structure, not glow

If you need fallback inspiration, use **`color-palette-frappe`** and choose a restrained subset instead of using the whole palette at once.

## Delivery expectations

When implementing:

- ship working frontend code
- preserve or improve accessibility
- keep the structure simple enough that another human could maintain it
- do not add decorative wrappers with no job

When explaining your choices:

- keep rationale brief
- point to hierarchy, readability, and product fit
- mention what AI-default move you avoided only if useful

## Final preflight

Before finishing, verify:

- the layout matches the product type
- the screen does not rely on gradients, glows, pills, or oversized radii for appeal
- the first thing on the page is not a decorative metric grid unless metrics are truly the product
- headings are plain and useful
- shadows are subtle
- hover states do not slide things around
- the UI feels like a real team’s product, not a showcase template

If a choice feels like the default AI UI move, reject it and pick the cleaner option.