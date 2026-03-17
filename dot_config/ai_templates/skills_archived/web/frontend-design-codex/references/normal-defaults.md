# Normal UI Defaults

Use these defaults when the project does not already define a stronger system.

These are not meant to be flashy. They are meant to keep the interface usable, steady, and hard to date.

## Layout

- containers: max width around 1200px to 1400px
- app shells: predictable grid or flex layout
- sidebars: fixed width around 240px to 260px when truly needed
- headers: plain title row with actions, not a decorative hero strip
- sections: standard spacing, usually 20px to 32px
- grids: consistent columns and gaps
- wrappers: functional only

## Spacing

Use a simple spacing rhythm:

- 4px
- 8px
- 12px
- 16px
- 24px
- 32px

Avoid random spacing jumps and excessive padding.

## Typography

- body text should usually sit around 14px to 16px
- keep hierarchy obvious with plain h1, h2, h3 usage
- use one clear heading system
- prefer readable, neutral copy over decorative tone
- avoid stacked heading formulas that rely on eyebrow labels

## Borders and radius

- borders: 1px solid with subtle contrast
- buttons: 8px to 10px radius
- cards and panels: 8px to 12px radius
- badges: 6px to 8px radius

Do not repeat large rounding on every single component.

## Shadows

Keep shadows quiet.

Good default range:

- `0 2px 8px rgba(0, 0, 0, 0.10)`

Use borders before shadows whenever possible.

## Motion

- duration: 100ms to 200ms
- easing: simple ease or ease-out
- prefer color, opacity, and focus-ring changes
- keep transitions local and subtle

Avoid transform-heavy hover behavior unless it communicates state.

## Components

### Sidebars

- solid background
- border-right for separation
- no floating outer shell
- no detached glass panel look

### Buttons

- solid fill or simple outline
- no pill shapes by default
- no gradient backgrounds unless brand-driven

### Cards and panels

- use only when grouping real information
- prefer subtle surface separation over floating effect
- keep nesting shallow

### Forms

- labels above inputs
- simple borders and focus rings
- no floating labels
- no animated underline gimmicks

### Tables

- left-aligned text by default
- clean rows and subtle hover states
- use badges only when status needs a compact signal
- prefer tables and lists over decorative KPI tiles for operational screens

### Tabs

- simple underline or border indicator
- no pill-tab styling unless the product already uses it

### Modals and dropdowns

- centered modal with straightforward overlay
- simple dropdown list with visible selected state
- no theatrical enter animations

## Copy and hierarchy

- headings should identify the page, not sell it
- helper text should clarify action or state
- labels should be short and concrete
- status text should reflect real workflow language

If the copy sounds like a design presentation, simplify it.