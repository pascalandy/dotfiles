# Anti-Patterns to Ban

This is the kill list for default AI UI behavior.

Use it when building or reviewing interfaces that risk looking generic, glossy, or over-generated.

## Hard no

Avoid these unless the user explicitly asks for them and the product truly supports them:

- oversized rounded corners everywhere
- pill overload
- glassmorphism as the default visual language
- soft corporate gradients used to fake taste
- generic dark SaaS composition
- decorative sidebar blobs
- control-room styling with no product reason
- fake premium typography combos used as a shortcut
- lazy font choices added just because they are common AI defaults
- sticky left rails when the information architecture does not need them
- metric-card grids as the first instinct
- fake charts that only fill space
- glows, haze, frosted panels, or decorative blur
- hero sections inside internal product UI without a real reason
- alignment that creates dead space to feel expensive
- overpadded layouts
- mobile collapse that becomes one long stack of oversized cards
- invented product voice like “live pulse” or “operator checklist” when the brand never asked for it
- generic startup copy
- style decisions made because they are easy to generate

## Heading and copy mistakes

Avoid heading stacks that look like this pattern:

- eyebrow label
- large headline
- soft paragraph explaining what the section already shows

Avoid small decorative labels such as:

- Focus
- Snapshot
- Team Command
- Live Pulse
- Night Shift

Avoid rounded status spans and ornamental note cards whose only job is tone.

## Specifically banned patterns

These are common failure modes worth naming explicitly:

- 20px to 32px border radii repeated across most components
- the same rounded rectangle language on sidebar, cards, buttons, and panels
- a roughly 280px sidebar with a brand block on top and nav links below, when a simpler rail would do
- floating detached sidebars with outer shell rounding
- donut charts with vague percentages
- canvas or dashboard charts in glass cards with no product-specific reason
- glow-based hierarchy
- mixed alignment logic where some blocks hug the edge and others drift toward the center
- muted gray-blue text that weakens contrast
- blue-black gradient dark mode with cyan accents masquerading as sophistication
- eyebrow labels in uppercase with letter spacing
- hero strips inside dashboards
- decorative headers like “operational clarity without the clutter”
- mini explanation cards that narrate what the UI already does
- transform animations on nav hover
- dramatic box shadows
- pseudo-element status dots used as decoration rather than signal
- gradient progress bars when a simple bar would do
- three-up KPI grids as the default dashboard answer
- decorative “team focus” or “recent activity” panels
- tag badges on every table row whether needed or not
- sidebar workspace blocks with CTA buttons that exist for polish, not function
- gradient brand marks with no brand system behind them
- live-count nav badges when they do not support a real workflow
- quota panels and progress bars added as filler
- footer meta text that describes the demo rather than the product
- trend indicators in color-coded text with no analytical purpose
- right rails full of “today” cards that exist only for composition
- too many nested panel types just to create visual variety

## Better replacements

If you notice one of the banned patterns, replace it with something more honest:

- floating sidebar shell -> fixed rail with border-right
- hero strip in dashboard -> plain title row plus action bar
- KPI cards -> table, list, backlog, queue, or timeline
- fake chart -> remove it or replace with real data view
- glow hierarchy -> spacing, border contrast, and typography hierarchy
- decorative copy card -> direct helper text near the control it explains
- right rail filler -> a simpler two-column or single-column main layout

## Color warning

When dark mode drifts toward glossy blue, pull it back.

Prefer:

- charcoal
- slate
- muted green, peach, red, or warm neutral accents
- one restrained accent family

Avoid building the whole UI around saturated blue highlights unless the product already owns that color.

## Final question

Ask yourself:

- if a human designer had one more hour to simplify this, what would they remove?

Remove that first.