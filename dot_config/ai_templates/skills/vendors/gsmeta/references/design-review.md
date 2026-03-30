# Design Review

> Designer's eye QA: finds visual inconsistency, spacing issues, hierarchy problems, AI slop patterns, and slow interactions — then fixes them in source code with atomic commits and before/after verification.

## When to Use

- User says "audit the design", "visual QA", "check if it looks good", or "design polish"
- User mentions visual inconsistencies or wants to polish a live site
- After shipping a feature branch with UI changes — diff-aware mode scopes to changed pages
- Pre-launch visual audit to catch AI slop patterns before users see them
- For plan-mode design review (before implementation), use the plan-design-review variant instead

## Inputs

- Running web application (local dev server or URL)
- Optional: `DESIGN.md` or `design-system.md` in the repo root — all design decisions are calibrated against it. If not found, the skill infers the system from the rendered site and offers to create one.
- Optional: auth credentials or cookie file
- Optional: `--quick` (homepage + 2 pages), `--deep` (10-15 pages), `--regression`
- Clean git working tree (required — each design fix gets its own atomic commit)

## Methodology

### Setup

Read `DESIGN.md` if it exists. Check for clean working tree — if dirty, ask to commit, stash, or abort.

Check if the design binary is available for generating target mockups (progressive enhancement). If not available, skip visual mockup generation — the fix loop works without it.

If available, the design binary commands are:
- `$D generate --brief "..." --output /path.png` — generate a single mockup
- `$D variants --brief "..." --count 3 --output-dir /path/` — generate N style variants
- `$D compare --images "a.png,b.png,c.png" --output /path/board.html --serve` — comparison board
- `$D serve --html /path/board.html` — serve comparison board and collect feedback
- `$D check --image /path.png --brief "..."` — vision quality gate
- `$D iterate --session /path/session.json --feedback "..." --output /path.png` — iterate

All design artifacts MUST be saved to `~/.gstack/projects/$SLUG/designs/` — never to `.context/`, `docs/designs/`, `/tmp/`, or project-local directories. Design artifacts are user data, not project files.

Create output directories under `~/.gstack/projects/$SLUG/designs/design-audit-{YYYYMMDD}/`.

Detect browser CDP mode — if connected to the user's real browser, skip cookie import and headless workarounds.

### Phase 1: First Impression

Before analyzing anything, form a gut reaction. Navigate to the target URL. Take a full-page desktop screenshot.

Write the **First Impression** using exactly this structure:
- "The site communicates **[what]**." (what it says at a glance — competence? playfulness? confusion?)
- "I notice **[observation]**." (what stands out, positive or negative — be specific)
- "The first 3 things my eye goes to are: **[1]**, **[2]**, **[3]**." (hierarchy check — are these intentional?)
- "If I had to describe this in one word: **[word]**." (gut verdict)

Be opinionated. A designer doesn't hedge.

### Phase 2: Design System Extraction

Extract the actual design system the site uses (not what DESIGN.md says, but what's rendered):

```js
// Fonts in use (capped at 500 elements to avoid timeout)
JSON.stringify([...new Set([...document.querySelectorAll('*')].slice(0,500).map(e => getComputedStyle(e).fontFamily))])

// Color palette in use
JSON.stringify([...new Set([...document.querySelectorAll('*')].slice(0,500).flatMap(e => [getComputedStyle(e).color, getComputedStyle(e).backgroundColor]).filter(c => c !== 'rgba(0, 0, 0, 0)'))])

// Heading hierarchy
JSON.stringify([...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].map(h => ({tag:h.tagName, text:h.textContent.trim().slice(0,50), size:getComputedStyle(h).fontSize, weight:getComputedStyle(h).fontWeight})))

// Touch target audit (find undersized interactive elements)
JSON.stringify([...document.querySelectorAll('a,button,input,[role=button]')].filter(e => {const r=e.getBoundingClientRect(); return r.width>0 && (r.width<44||r.height<44)}).map(e => ({tag:e.tagName, text:(e.textContent||'').trim().slice(0,30), w:Math.round(e.getBoundingClientRect().width), h:Math.round(e.getBoundingClientRect().height)})).slice(0,20))
```

Run these JS queries in the page context after navigation. Also run the `perf` command for a performance baseline.

Structure findings as an **Inferred Design System:**
- **Fonts:** list with usage counts. Flag if >3 distinct font families.
- **Colors:** palette extracted. Flag if >12 unique non-gray colors. Note warm/cool/mixed.
- **Heading Scale:** h1-h6 sizes. Flag skipped levels, non-systematic size jumps.
- **Spacing Patterns:** sample padding/margin values. Flag non-scale values.

Offer to save findings as `DESIGN.md`.

### Phase 3: Page-by-Page Visual Audit

For each page in scope, take an annotated screenshot, responsive screenshots (mobile/tablet/desktop), check console for errors, and run perf.

**Auth detection:** After each navigation, check if the URL changed to a login path. If so, ask user to import cookies or authenticate.

Apply the **Design Audit Checklist** (10 categories, ~80 items):

**1. Visual Hierarchy & Composition** (8 items)
- Clear focal point? One primary CTA per view?
- Eye flows naturally top-left to bottom-right?
- Visual noise — competing elements?
- Information density appropriate?
- Z-index clarity — unexpected overlaps?
- Above-the-fold communicates purpose in 3 seconds?
- Squint test: hierarchy visible when blurred?
- White space intentional, not leftover?

**2. Typography** (15 items)
- Font count <=3
- Scale follows ratio (1.25 major third or 1.333 perfect fourth)
- Line-height: 1.5x body, 1.15-1.25x headings
- Measure: 45-75 characters per line (66 ideal)
- No skipped heading levels
- Weight contrast: >=2 weights for hierarchy
- No blacklisted fonts (Papyrus, Comic Sans, Lobster, Impact, Jokerman)
- Primary font is Inter/Roboto/Open Sans/Poppins → flag as potentially generic
- `text-wrap: balance` or `text-pretty` on headings
- Curly quotes used (not straight quotes)
- Ellipsis character `…` not three dots `...`
- `font-variant-numeric: tabular-nums` on number columns
- Body text >= 16px, captions >= 12px
- No letterspacing on lowercase text

**3. Color & Contrast** (10 items)
- Palette coherent (<=12 unique non-gray colors)
- WCAG AA: body text 4.5:1, large text (18px+) 3:1, UI components 3:1
- Semantic colors consistent (success=green, error=red, warning=amber)
- No color-only encoding
- Dark mode surfaces use elevation, not just lightness inversion
- Dark mode text off-white (~#E0E0E0), not pure white
- Primary accent desaturated 10-20% in dark mode
- `color-scheme: dark` on html element (if dark mode present)
- No red/green only combinations
- Neutral palette warm or cool consistently, not mixed

**4. Spacing & Layout** (12 items)
- Grid consistent at all breakpoints
- Spacing uses a scale (4px or 8px base), not arbitrary values
- Consistent alignment, nothing floats outside the grid
- Proximity: related items closer, distinct sections further
- Border-radius hierarchy (not uniform bubbly radius everywhere)
- Inner radius = outer radius - gap (nested elements)
- No horizontal scroll on mobile
- Max content width set (no full-bleed body text)
- `env(safe-area-inset-*)` for notch devices
- URL reflects state (filters, tabs, pagination in query params)
- Flex/grid for layout (not JS measurement)
- Breakpoints: mobile (375), tablet (768), desktop (1024), wide (1440)

**5. Interaction States** (10 items)
- Hover state on all interactive elements
- `focus-visible` ring present (never `outline: none` without replacement)
- Active/pressed state with depth effect or color shift
- Disabled: reduced opacity + `cursor: not-allowed`
- Loading: skeleton shapes match real content layout
- Empty states: warm message + primary action + visual (not just "No items.")
- Error messages: specific + include fix/next step
- Success: confirmation animation or color, auto-dismiss
- Touch targets >= 44px
- `cursor: pointer` on all clickable elements

**6. Responsive Design** (8 items)
- Mobile layout makes design sense (not just stacked desktop columns)
- Touch targets sufficient on mobile
- No horizontal scroll at any viewport
- Images handle responsive (srcset, sizes, or CSS containment)
- Text readable without zooming on mobile (>= 16px body)
- Navigation collapses appropriately
- Forms usable on mobile (correct input types, no autoFocus)
- No `user-scalable=no` or `maximum-scale=1` in viewport meta

**7. Motion & Animation** (6 items)
- Easing: ease-out for entering, ease-in for exiting, ease-in-out for moving
- Duration: 50-700ms (nothing slower unless page transition)
- Every animation communicates something (state change, attention, spatial relationship)
- `prefers-reduced-motion` respected
- No `transition: all` — properties listed explicitly
- Only `transform` and `opacity` animated (not layout properties)

**8. Content & Microcopy** (8 items)
- Empty states designed with warmth (message + action + illustration/icon)
- Error messages specific: what happened + why + what to do next
- Button labels specific ("Save API Key" not "Continue" or "Submit")
- No placeholder/lorem ipsum text in production
- Truncation handled (`text-overflow: ellipsis`, `line-clamp`, or `break-words`)
- Active voice ("Install the CLI" not "The CLI will be installed")
- Loading states end with `…` ("Saving…" not "Saving...")
- Destructive actions have confirmation or undo window

**9. AI Slop Detection** (10 anti-patterns)

The test: would a human designer at a respected studio ever ship this?

1. Purple/violet/indigo gradient backgrounds or blue-to-purple color schemes
2. **The 3-column feature grid:** icon-in-colored-circle + bold title + 2-line description, repeated 3x symmetrically. THE most recognizable AI layout.
3. Icons in colored circles as section decoration
4. Centered everything (`text-align: center` on all headings, descriptions, cards)
5. Uniform bubbly border-radius on every element
6. Decorative blobs, floating circles, wavy SVG dividers (if a section feels empty, it needs better content, not decoration)
7. Emoji as design elements (rockets in headings, emoji as bullet points)
8. Colored left-border on cards (`border-left: 3px solid <accent>`)
9. Generic hero copy ("Welcome to [X]", "Unlock the power of...", "Your all-in-one solution for...")
10. Cookie-cutter section rhythm (hero → 3 features → testimonials → pricing → CTA, every section same height)

**10. Performance as Design** (6 items)
- LCP < 2.0s (web apps), < 1.5s (informational sites)
- CLS < 0.1 (no visible layout shifts)
- Skeleton quality: shapes match real content, shimmer animation
- Images: `loading="lazy"`, width/height set, WebP/AVIF format
- Fonts: `font-display: swap`, preconnect to CDN origins
- No FOUT (critical fonts preloaded)

### Phase 4: Interaction Flow Review

Walk 2-3 key user flows and evaluate the feel, not just function:
- **Response feel:** Is clicking responsive? Any delays or missing loading states?
- **Transition quality:** Intentional or absent/generic?
- **Feedback clarity:** Does the action clearly succeed or fail? Is feedback immediate?
- **Form polish:** Focus states visible? Validation timing correct? Errors near the source?

### Phase 5: Cross-Page Consistency

Compare screenshots across pages:
- Navigation bar consistent?
- Footer consistent?
- Component reuse vs one-off designs (same button styled differently on different pages?)
- Tone consistency (playful on one page, corporate on another?)
- Spacing rhythm carries across pages?

### Phase 6: Compile Report

**Scoring System:**

Two headline scores:
- **Design Score: A-F** — weighted average of all 10 categories
- **AI Slop Score: A-F** — standalone grade with pithy verdict

**Grade computation:** Each category starts at A. Each High-impact finding drops one letter grade. Each Medium-impact drops half a letter grade. Polish findings noted but don't affect grade.

| Category | Weight |
|----------|--------|
| Visual Hierarchy | 15% |
| Typography | 15% |
| Spacing & Layout | 15% |
| Color & Contrast | 10% |
| Interaction States | 10% |
| Responsive | 10% |
| Content Quality | 10% |
| AI Slop | 5% |
| Motion | 5% |
| Performance Feel | 5% |

**Grade meanings:**
- **A:** Intentional, polished, delightful. Shows design thinking.
- **B:** Solid fundamentals, minor inconsistencies. Looks professional.
- **C:** Functional but generic. No design point of view.
- **D:** Noticeable problems. Feels unfinished or careless.
- **F:** Actively hurting user experience.

**Design Critique Format** (structured, not opinion):
- "I notice..." — observation
- "I wonder..." — question
- "What if..." — suggestion
- "I think... because..." — reasoned opinion

Tie everything to user goals. Always suggest specific improvements alongside problems.

**Classifier:** Determine page type before applying rules:
- **MARKETING/LANDING PAGE** (hero-driven, brand-forward, conversion-focused)
- **APP UI** (workspace-driven, data-dense, task-focused)
- **HYBRID** → apply Landing Page rules to marketing sections, App UI rules to functional sections

**Landing page rules:**
- First viewport reads as one composition, not a dashboard
- Brand-first hierarchy: brand > headline > body > CTA
- Typography: expressive, purposeful — no default stacks (Inter, Roboto, Arial, system)
- No flat single-color backgrounds — use gradients, images, subtle patterns
- Hero: full-bleed, edge-to-edge, no inset/tiled/rounded variants
- Hero budget: brand, one headline, one supporting sentence, one CTA group, one image
- No cards in hero. Cards only when card IS the interaction
- One job per section: one purpose, one headline, one short supporting sentence
- Motion: 2-3 intentional motions minimum (entrance, scroll-linked, hover/reveal)
- Color: define CSS variables, avoid purple-on-white defaults, one accent color default
- Copy: product language not design commentary. "If deleting 30% improves it, keep deleting"
- Beautiful defaults: composition-first, brand as loudest text, two typefaces max, cardless by default, first viewport as poster not document

**App UI rules:**
- Calm surface hierarchy, strong typography, few colors
- Dense but readable, minimal chrome
- Organize: primary workspace, navigation, secondary context, one accent
- Avoid: dashboard-card mosaics, thick borders, decorative gradients, ornamental icons
- Copy: utility language — orientation, status, action. Not mood/brand/aspiration
- Cards only when card IS the interaction
- Section headings state what area is or what user can do (e.g., "Selected KPIs", "Plan status")

**Universal rules (apply to ALL page types):**
- Define CSS variables for the color system
- No default font stacks (Inter, Roboto, Arial, system)
- One job per section
- "If deleting 30% of the copy improves it, keep deleting"
- Cards earn their existence — no decorative card grids

**Hard rejection criteria (instant-fail patterns):**
1. Generic SaaS card grid as first impression
2. Beautiful image with weak brand
3. Strong headline with no clear action
4. Busy imagery behind text
5. Sections repeating same mood statement
6. Carousel with no narrative purpose
7. App UI made of stacked cards instead of layout

**Litmus checks (answer YES/NO):**
1. Brand/product unmistakable in first screen?
2. One strong visual anchor present?
3. Page understandable by scanning headlines only?
4. Each section has one job?
5. Are cards actually necessary?
6. Does motion improve hierarchy or atmosphere?
7. Would design feel premium with all decorative shadows removed?

### Design Outside Voices (parallel, if Codex is available)

Check if Codex CLI is available. If yes, launch two voices simultaneously:

1. **Codex source audit:** Review frontend source code for spacing systematicity (design tokens vs. magic numbers), typography (expressive purposeful fonts vs. default stacks), color system (CSS variables vs. scattered hex), responsive breakpoints, accessibility, motion, and card usage. Apply litmus checks and hard rejection criteria. Reference file:line for every finding.

2. **Claude subagent consistency audit:** Independently review frontend source code focusing on CONSISTENCY PATTERNS across files — are spacing values systematic? Is there one color system or scattered approaches? Are responsive breakpoints consistent? Is accessibility consistent or spotty?

Merge findings from both voices with `[codex]` / `[subagent]` / `[cross-model]` tags.

### Phase 7: Triage

Sort findings by impact: High (affects first impression, hurts user trust), Medium (reduces polish), Polish (separates good from great). Mark findings that require copy from the team or third-party changes as "deferred."

### Phase 8: Fix Loop

**8a. Locate source:** Search for CSS classes, component names, style files. Prefer CSS/styling changes over structural component changes.

**8a.5. Target Mockup (if design binary available):** For layout, hierarchy, or spacing findings (not trivial CSS value fixes), generate a target mockup. Show the user current state vs. intended state before fixing.

**8b. Fix:** Minimal fix — smallest change that resolves the design issue. CSS-only changes preferred.

**8c. Commit:** `git commit -m "style(design): FINDING-NNN — short description"`. One commit per fix.

**8d. Re-test:** Navigate to affected page. Take before/after screenshot pair. Check console.

**8e. Classify:** verified, best-effort, or reverted. Run `git revert HEAD` if regression detected.

**8e.5. Regression Test:** Only for fixes involving JavaScript behavior changes (broken dropdowns, animation failures, conditional rendering). CSS-only fixes: skip entirely.

**8f. Self-Regulation (every 5 fixes):**
```
DESIGN-FIX RISK:
  Start at 0%
  Each revert:                        +15%
  Each CSS-only file change:          +0%
  Each JSX/TSX/component file change: +5%
  After fix 10:                       +1% per additional fix
  Touching unrelated files:           +20%
```

If risk > 20%: STOP. Show the user what's been done. Ask whether to continue.

Hard cap: 30 fixes.

### Phase 9: Final Design Audit

Re-run the design audit on all affected pages. If target mockups were generated during the fix loop AND the design binary is available, run `$D verify --mockup <target.png> --screenshot <after.png>` to compare the fix result against the target — include pass/fail in the report. Compute final design score and AI slop score. If scores are WORSE than baseline, warn prominently.

### Phase 10: Report

Write to `$REPORT_DIR/design-audit-{domain}.md`. Include per-finding fix status, commit SHA, files changed, before/after screenshots.

Summary section: total findings, fixes applied (verified/best-effort/reverted), deferred, design score delta, AI slop score delta.

PR summary: "Design review found N issues, fixed M. Design score X → Y, AI slop score X → Y."

### Phase 11: TODOS.md Update

If the repo has a `TODOS.md`:
1. Add new deferred design findings as TODOs with impact level, category, and description
2. Annotate fixed findings that were already in TODOS.md: "Fixed by /design-review on {branch}, {date}"

## Quality Gates

1. Screenshots are evidence. Every finding needs at least one screenshot.
2. Be specific and actionable. "Change X to Y because Z" — not "the spacing feels off."
3. Never read source code for evaluation (exception: offer to write DESIGN.md from extracted observations).
4. AI Slop detection is the superpower. Most developers can't tell if their site looks AI-generated. Be direct.
5. Always include "Quick Wins" — 3-5 highest-impact fixes that take less than 30 minutes each.
6. Use `snapshot -C` for tricky UIs. Finds clickable divs that the accessibility tree misses.
7. Responsive is design, not just "not broken." A stacked desktop layout on mobile is lazy.
8. Document incrementally. Write each finding to the report as you find it.
9. Depth over breadth. 5-10 well-documented findings > 20 vague observations.
10. Never delete output files. Screenshots and design reports accumulate — that's intentional.
11. Display screenshots inline for the user. After every screenshot command, read the output file so the user can see it. For responsive screenshots (3 files), read all three. Without this, screenshots are invisible.
12. CSS-first. Prefer CSS/styling changes over structural component changes. CSS-only changes are safer.
13. Only modify tests when generating regression tests in Phase 8e.5. Never modify CI configuration. Never modify existing tests — only create new test files.
14. Clean working tree required before starting. Each fix gets its own atomic commit.
15. Revert on regression immediately.
16. DESIGN.md export: may write a DESIGN.md file if user accepts the offer from Phase 2.

**AI Slop blacklist source:** OpenAI "Designing Delightful Frontends with GPT-5.4" (Mar 2026) + gstack design methodology.

## Outputs

```
~/.gstack/projects/$SLUG/designs/design-audit-{YYYYMMDD}/
├── design-audit-{domain}.md              # Structured report
├── screenshots/
│   ├── first-impression.png              # Phase 1
│   ├── {page}-annotated.png              # Per-page annotated
│   ├── {page}-mobile.png                 # Responsive
│   ├── {page}-tablet.png
│   ├── {page}-desktop.png
│   ├── finding-001-before.png            # Before fix
│   ├── finding-001-target.png            # Target mockup (if generated)
│   ├── finding-001-after.png             # After fix
│   └── ...
└── design-baseline.json                  # For regression mode
```

Also writes a one-line summary to `~/.gstack/projects/{slug}/{user}-{branch}-design-audit-{datetime}.md`.

## Feeds Into

- `>qa` — design fixes done, run functional QA to verify nothing broke
- `>ship` — design review is a natural pre-ship gate
- `>cso` — security audit after visual/functional reviews

## Harness Notes

**Browser automation is a hard dependency.** This skill requires the `browse` daemon (`$B`) for navigation, screenshots, JS execution, and responsive testing.

**Design binary is optional.** The `design` binary enables target mockup generation, but the skill runs fully without it. All mockup generation steps degrade gracefully.

**Parallel outside voices** require Codex CLI and subagent capability. If Codex fails, continue with subagent output only tagged `[single-model]`. If both fail, continue with primary review only.

Design artifacts (mockups, comparison boards) are saved to `~/.gstack/projects/$SLUG/designs/` — user data, not project files. Never save to `.context/`, `docs/designs/`, `/tmp/`, or project-local directories.

See `harness-compat.md: "Browse daemon setup"`, `"Subagent patterns"`, `"CDP vs headless mode"`.
