# Design Consultation

> Understands your product, researches the landscape, proposes a complete design system (aesthetic, typography, color, layout, spacing, motion), and creates DESIGN.md as the project's design source of truth.

## When to Use

- User says "design system", "brand guidelines", or "create DESIGN.md"
- Starting a new project's UI with no existing design system or DESIGN.md
- Proactively suggest when a new UI project has no design direction established
- For inferring a design system from an existing site, use plan-design-review instead

## Inputs

- Product description (from README, office-hours output, or user description)
- Existing codebase structure (src/, app/, components/, pages/ dirs)
- Existing DESIGN.md if present (will ask to update, start fresh, or cancel)
- User answers to focused product context questions (one question covers everything)

## Methodology

### Phase 0: Pre-checks

Check for existing DESIGN.md. If found, ask the user: update it, start fresh, or cancel?

Gather product context from the codebase: read README (first 50 lines), check package.json, scan directory structure. Look for office-hours output in the project directory — if found, read it, the product context is pre-filled.

If the codebase is empty and purpose is unclear, say: "I don't have a clear picture of what you're building. Want to explore first with office-hours?" Once product direction is known, the design system follows naturally.

Check for available tooling:
- Browse binary (optional — enables visual competitive research via screenshots)
- Design binary (optional — enables AI mockup generation instead of HTML preview)

If design tooling is available, Phase 5 generates AI mockups instead of HTML preview pages. Much more powerful — the user sees what their product could actually look like.

### Phase 1: Product Context

Ask the user ONE question that covers everything. Pre-fill what you can infer from the codebase.

The question must cover:
1. Confirm what the product is, who it's for, what space/industry
2. What project type: web app, dashboard, marketing site, editorial, internal tool
3. "Want me to research what top products in your space are doing for design, or should I work from my design knowledge?"
4. Explicitly say: "At any point you can just drop into chat and talk through anything — this isn't a rigid form, it's a conversation."

If README or office-hours output provides enough context, pre-fill and confirm: "From what I can see, this is [X] for [Y] in the [Z] space. Sound right?"

### Phase 2: Research (only if user said yes)

**Step 1:** Search for 5-10 products in the space. Search for "[product category] website design", "[product category] best websites [year]", "best [industry] web apps".

**Step 2:** If browse tooling is available, visit top 3-5 sites and capture visual evidence (screenshot, DOM snapshot). For each site, analyze: fonts actually used, color palette, layout approach, spacing density, aesthetic direction.

If browse not available, rely on search results and built-in design knowledge — still good.

**Step 3: Three-layer synthesis:**
- **Layer 1 (tried and true):** What design patterns does every product in this category share? These are table stakes — users expect them.
- **Layer 2 (new and popular):** What's trending? What new patterns are emerging?
- **Layer 3 (first principles):** Is there a reason the conventional design approach is wrong for THIS product? Where should we deliberately break from category norms?

**Eureka check:** If Layer 3 reveals a genuine design insight, name it: "EUREKA: Every [category] product does X because they assume [assumption]. But this product's users [evidence] — so we should do Y instead."

Summarize conversationally: "I looked at what's out there. They converge on [patterns]. Most feel [observation]. The opportunity to stand out is [gap]. Here's where I'd play safe and where I'd take a risk..."

### Design Outside Voices (optional)

Ask: "Want outside design voices? One evaluates against design hard rules; one proposes an alternative direction."

If yes, run two voices in parallel:

Voice 1 prompt: "Given this product context, propose a complete design direction: visual thesis (one sentence — mood, material, energy), typography (specific font names — not defaults), color system (CSS variables), layout (composition-first), 2 deliberate departures from category norms, anti-slop constraints. Be opinionated. Be specific. Own it."

Voice 2 prompt: "Given this product context, propose a design direction that would SURPRISE. What would the cool indie studio do that the enterprise UI team wouldn't? Aesthetic direction, typography stack, color palette, 2 departures from category norms, emotional reaction in first 3 seconds. Be bold. Be specific."

After both return, synthesize: areas of agreement across all three voices, genuine divergences as creative alternatives, "Voice 1 and I agree on X. Voice 1 suggested Y where I'm proposing Z — here's why..."

### Phase 3: The Complete Proposal

This is the soul of the skill. Propose EVERYTHING as one coherent package with a SAFE/RISK breakdown.

```
Based on [product context] and [research findings / design knowledge]:

AESTHETIC: [direction] — [one-line rationale]
DECORATION: [level] — [why this pairs with the aesthetic]
LAYOUT: [approach] — [why this fits the product type]
COLOR: [approach] + proposed palette (hex values) — [rationale]
TYPOGRAPHY: [3 font recommendations with roles] — [why these fonts]
SPACING: [base unit + density] — [rationale]
MOTION: [approach] — [rationale]

This system is coherent because [explain how choices reinforce each other].

SAFE CHOICES (category baseline — users expect these):
  - [2-3 decisions matching category conventions, with rationale for playing safe]

RISKS (where your product gets its own face):
  - [2-3 deliberate departures from convention]
  - For each risk: what it is, why it works, what you gain, what it costs
```

The SAFE/RISK breakdown is the critical part. Design coherence is table stakes — every product in a category can be coherent and look identical. The real question is: where do you take creative risks? Always propose at least 2 risks with clear rationale and explicit tradeoffs.

**Design knowledge (use to inform proposals — never display as a menu):**

Aesthetic directions:
- Brutally Minimal — Type and whitespace only, no decoration, modernist
- Maximalist Chaos — Dense, layered, pattern-heavy, Y2K meets contemporary
- Retro-Futuristic — Vintage tech nostalgia, CRT glow, pixel grids, warm monospace
- Luxury/Refined — Serifs, high contrast, generous whitespace, precious metals
- Playful/Toy-like — Rounded, bouncy, bold primaries, approachable
- Editorial/Magazine — Strong typographic hierarchy, asymmetric grids, pull quotes
- Brutalist/Raw — Exposed structure, system fonts, visible grid, no polish
- Art Deco — Geometric precision, metallic accents, symmetry, decorative borders
- Organic/Natural — Earth tones, rounded forms, hand-drawn texture, grain
- Industrial/Utilitarian — Function-first, data-dense, monospace accents, muted palette

Font recommendations by purpose:
- Display/Hero: Satoshi, General Sans, Instrument Serif, Fraunces, Clash Grotesk, Cabinet Grotesk
- Body: Instrument Sans, DM Sans, Source Sans 3, Geist, Plus Jakarta Sans, Outfit
- Data/Tables: Geist (tabular-nums), JetBrains Mono, IBM Plex Mono
- Code: JetBrains Mono, Fira Code, Berkeley Mono, Geist Mono

Font blacklist (never recommend): Papyrus, Comic Sans, Lobster, Impact, Jokerman, Bleeding Cowboys, Permanent Marker, Bradley Hand, Brush Script, Hobo, Trajan, Raleway, Clash Display, Courier New (for body).

Overused fonts (never recommend as primary): Inter, Roboto, Arial, Helvetica, Open Sans, Lato, Montserrat, Poppins.

AI slop anti-patterns (never include):
- Purple/violet gradients as default accent
- 3-column feature grid with icons in colored circles
- Centered everything with uniform spacing
- Uniform bubbly border-radius on all elements
- Gradient buttons as primary CTA pattern
- Generic stock-photo-style hero sections
- "Built for X" / "Designed for Y" marketing copy

**Coherence validation:** When the user overrides one section, check if the rest still coheres. Flag mismatches with a gentle nudge, never block. Always accept the user's final choice.

Examples:
- Brutalist aesthetic + expressive motion: "Brutalist aesthetics usually pair with minimal motion. Your combo is unusual — intentional?"
- Creative-editorial layout + data-heavy product: "Editorial layouts can fight data density. Want me to show a hybrid approach?"

### Phase 4: Drill-downs (only if user requests adjustments)

When user wants to change a specific section, go deep on that section only:
- Fonts: 3-5 specific candidates with rationale, what each evokes
- Colors: 2-3 palette options with hex values and color theory reasoning
- Aesthetic: which directions fit their product and why
- Layout/Spacing/Motion: approaches with concrete tradeoffs for their product type

Each drill-down is one focused question. After the user decides, re-check coherence with the rest of the system.

### Phase 5: Design System Preview

Two paths depending on available tooling.

**Path A: AI Mockups (if design tooling available)**

Generate 3 AI-rendered mockups showing the proposed design system applied to realistic screens for this product. Construct a design brief from the Phase 3 proposal (aesthetic, colors, typography, spacing, layout) and product context.

Run a quality check on each variant. Show variants inline for immediate preview.

Create a comparison board and serve it for user feedback. Poll for feedback file:
- `feedback.json` (Submit): read preferred, ratings, comments, overall — proceed with approved variant
- `feedback-pending.json` (Regenerate/Remix): update brief, generate new variants, reload board, poll again

Confirm understanding before proceeding: "Here's what I understood from your feedback..."

After approval, extract design tokens from the approved mockup to ground DESIGN.md in what was actually approved visually, not just text descriptions.

If in plan mode: add approved mockup path and extracted tokens to the plan under "## Approved Design Direction." DESIGN.md is written at implementation time.

If NOT in plan mode: proceed directly to Phase 6 and write DESIGN.md.

**Path B: HTML Preview Page (if no design tooling)**

Generate a polished, self-contained HTML file that:
1. Loads proposed fonts (no CDN dependencies for rendering, use Google Fonts via link tags)
2. Uses the proposed color palette throughout — dogfood the design system
3. Shows the product name (not "Lorem Ipsum") as the hero heading
4. Font specimen: each font in its proposed role, side-by-side comparison for candidates, real content matching the product
5. Color palette: swatches with hex values, sample UI components (buttons, cards, inputs, alerts) in the palette, background/text combinations with contrast
6. Realistic product mockups based on project type:
   - Dashboard/app: data table, sidebar nav, header with user avatar, stat cards
   - Marketing site: hero section, feature highlights, testimonial, CTA
   - Settings/admin: labeled inputs, toggles, dropdowns, save button
   - Auth/onboarding: login form with social buttons, validation states
7. Light/dark mode toggle using CSS custom properties
8. Clean, professional layout — the preview page IS a taste signal for the skill
9. Responsive — looks good on any screen width

Open the file in the browser. If headless environment, tell the user the file path.

### Phase 6: Write DESIGN.md and Confirm

If design tokens were extracted from an approved mockup (Path A), use them as primary source for exact values. The Phase 3 proposal provides rationale and context; extraction provides exact hex codes, font stacks, spacing values.

Write DESIGN.md with this structure:

```markdown
# Design System — [Project Name]

## Product Context
- What this is: [1-2 sentences]
- Who it's for: [target users]
- Space/industry: [category, peers]
- Project type: [web app / dashboard / marketing site / etc.]

## Aesthetic Direction
- Direction: [name]
- Decoration level: [minimal / intentional / expressive]
- Mood: [1-2 sentences]
- Reference sites: [URLs if research was done]

## Typography
- Display/Hero: [font name] — [rationale]
- Body: [font name] — [rationale]
- UI/Labels: [font name or "same as body"]
- Data/Tables: [font name] — [rationale, must support tabular-nums]
- Code: [font name]
- Loading: [CDN URL or self-hosted strategy]
- Scale: [modular scale with specific px/rem values for each level]

## Color
- Approach: [restrained / balanced / expressive]
- Primary: [hex] — [usage]
- Secondary: [hex] — [usage]
- Neutrals: [warm/cool grays, hex range]
- Semantic: success [hex], warning [hex], error [hex], info [hex]
- Dark mode: [strategy]

## Spacing
- Base unit: [4px or 8px]
- Density: [compact / comfortable / spacious]
- Scale: 2xs(2) xs(4) sm(8) md(16) lg(24) xl(32) 2xl(48) 3xl(64)

## Layout
- Approach: [grid-disciplined / creative-editorial / hybrid]
- Grid: [columns per breakpoint]
- Max content width: [value]
- Border radius: [hierarchical scale — sm:4px, md:8px, lg:12px, full:9999px]

## Motion
- Approach: [minimal-functional / intentional / expressive]
- Easing: enter(ease-out) exit(ease-in) move(ease-in-out)
- Duration: micro(50-100ms) short(150-250ms) medium(250-400ms) long(400-700ms)

## Decisions Log
| Date | Decision | Rationale |
|------|----------|-----------|
| [today] | Initial design system created | [reasoning] |
```

Also update CLAUDE.md (or create it) — append: "Always read DESIGN.md before making any visual or UI decisions. All font choices, colors, spacing, and aesthetic direction are defined there. Do not deviate without explicit user approval. In QA mode, flag any code that doesn't match DESIGN.md."

Show a summary of all decisions to the user. Flag any that used defaults without explicit confirmation. Ask: "Ship it? Change something? Start over?"

### Important Rules

1. **Propose, don't present menus.** Make opinionated recommendations based on product context, then let the user adjust.
2. **Every recommendation needs a rationale.** Never say "I recommend X" without "because Y."
3. **Coherence over individual choices.** A system where every piece reinforces every other beats one with individually "optimal" but mismatched choices.
4. **Never recommend blacklisted or overused fonts as primary.** If the user specifically requests one, comply but explain the tradeoff.
5. **SAFE/RISK is always required.** Never present only "the right answer." Always surface where to play safe and where to take creative risks.
6. **The preview page must be beautiful.** It's the first visual output and sets the tone for the whole skill.
7. **Conversational tone.** This isn't a rigid workflow. If the user wants to talk through a decision, engage as a thoughtful design partner.
8. **Accept the user's final choice.** Nudge on coherence issues, but never block or refuse to write DESIGN.md because you disagree with a choice.
9. **No AI slop in your own output.** Your recommendations, preview page, and DESIGN.md should demonstrate the taste you're asking the user to adopt.

## Quality Gates

- Product context understood (from code, README, or user answer)
- If research requested, three-layer synthesis produced with eureka check
- Outside voices offered and either run or explicitly declined
- Complete proposal with SAFE/RISK breakdown presented
- Coherence check run when any section overridden
- Design preview generated (mockups or HTML page)
- User confirmed final direction before DESIGN.md is written
- DESIGN.md written to repo root with all required sections
- CLAUDE.md updated with design system reference
- Decisions log includes today's entry

## Outputs

- DESIGN.md written to repo root
- CLAUDE.md updated
- Optional: AI mockups (approved.json + variant PNGs)
- Optional: HTML preview page (if no design tooling)
- Optional: competitive research findings (if user requested)

## Feeds Into

- >plan-design-review (DESIGN.md is the calibration baseline for all design reviews)
- >office-hours (if user wants to explore product direction before committing to a design system)

## Harness Notes

**Browse tooling:** Phase 2 visual research uses a headless browser to screenshot competitor sites. Optional enhancement — skill works without it using search results and built-in knowledge.

**Design binary:** Phase 5 AI mockup generation requires a design generation binary. If unavailable, fall back to HTML preview page. Both paths are fully functional. See harness-compat.md "Design binary" section.

**Parallel voices:** Phase 2.5 outside voices can be run simultaneously if parallel execution is available. Both voices receive the same product context but produce independent proposals. See harness-compat.md "Parallel subagents" section.
