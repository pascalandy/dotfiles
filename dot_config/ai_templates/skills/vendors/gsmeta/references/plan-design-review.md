# Plan Design Review

> Designer's eye plan review: rates each design dimension 0-10, explains what would make it a 10, then fixes the plan to get there. Works on plans before implementation, not live sites.

## When to Use

- User says "review the design plan" or "design critique"
- Plan has UI/UX components that should be reviewed before implementation starts
- Proactively suggest when a plan with UI scope is about to be implemented without a design review
- For live site visual audits, use design-review instead

## Inputs

- A plan document (required)
- DESIGN.md if it exists (all decisions calibrate against it)
- CLAUDE.md for project conventions
- Existing UI patterns and components in the codebase
- TODOS.md for design-related items this plan touches

## Methodology

### Pre-Review System Audit

Before reviewing the plan:
- Check recent git history (`git log --oneline -15`, `git diff <base> --stat`)
- Read the plan file
- Read CLAUDE.md
- Read DESIGN.md (if it exists — this is the design source of truth)
- Read TODOS.md for design-related items

Map:
- What is the UI scope? (pages, components, interactions)
- Does a DESIGN.md exist? If not, flag as a gap.
- What existing design patterns exist to align with?

**Retrospective check:** If prior commits show previous design review cycles, be more aggressive reviewing those areas.

**UI scope detection:** If the plan involves NONE of: new UI screens, changes to existing UI, user-facing interactions, frontend framework changes, or design system changes — tell the user this plan has no UI scope and exit early.

### Step 0: Design Scope Assessment

**0A. Initial Design Rating**
Rate the plan's overall design completeness 0-10. Be specific: "This plan is a 3/10 because it describes what the backend does but never specifies what the user sees." Explain what a 10 looks like for THIS plan.

**0B. DESIGN.md Status**
- If DESIGN.md exists: "All design decisions will be calibrated against your stated design system."
- If no DESIGN.md: "No design system found. Recommend running design-consultation first. Proceeding with universal design principles."

**0C. Existing Design Leverage**
What existing UI patterns, components, or design decisions should this plan reuse? Don't reinvent what already works.

**0D. Focus Areas**
Ask: "I've rated this plan N/10 on design completeness. The biggest gaps are X, Y, Z. Should I focus on specific areas or all 7 dimensions?"

Wait for user response before proceeding.

### Visual Mockups (default ON when design tooling available)

If the plan involves any UI and a design generation binary is available, generate mockups immediately. Don't ask permission.

The only reasons to skip:
- No design tooling available
- Plan has zero UI scope
- User explicitly says "skip mockups"

Generate 3 style variants for each major UI screen/section in scope. Construct design briefs from the plan description and DESIGN.md constraints. After generation, run a cross-model quality check on each variant.

Present variants inline for immediate preview. Create a comparison board and serve it for feedback. Poll for feedback file (Submit = final choice, Regenerate/Remix = iterate).

Feedback loop:
- If regenerate requested: update brief, generate new variants, reload comparison board
- If submitted: read `preferred`, `ratings`, `comments`, `overall` from feedback
- Confirm understanding: "Here's what I understood from your feedback: PREFERRED: [X], DIRECTION: [overall]. Is this right?"
- Save approved choice

Note the approved direction as the visual reference for all subsequent review passes.

**If no design tooling available:** Proceed with text-based review. Note the user is missing the best part.

### Design Outside Voices (optional)

Offer to run outside design perspectives in parallel: one evaluates against hard design rules and litmus checks, one does an independent completeness review.

**Hard rejection criteria (instant-fail patterns — flag if ANY apply):**
1. Generic SaaS card grid as first impression
2. Beautiful image with weak brand
3. Strong headline with no clear action
4. Busy imagery behind text
5. Sections repeating same mood statement
6. Carousel with no narrative purpose
7. App UI made of stacked cards instead of layout

**Litmus checks (answer YES/NO for each):**
1. Brand/product unmistakable in first screen?
2. One strong visual anchor present?
3. Page understandable by scanning headlines only?
4. Each section has one job?
5. Are cards actually necessary?
6. Does motion improve hierarchy or atmosphere?
7. Would design feel premium with all decorative shadows removed?

After both voices return, produce a litmus scorecard showing Claude and outside voice agreement on each check. Feed hard rejections into Pass 1 as first items tagged [HARD REJECTION]. Feed litmus failures as pre-loaded known issues into relevant passes.

### The 0-10 Rating Method

For each design section:
1. Rate: "Information Architecture: 4/10"
2. Gap: "It's a 4 because X. A 10 would have Y."
3. Fix: Edit the plan to add what's missing
4. Re-rate: "Now 8/10 — still missing Z"
5. Ask if there's a genuine design choice to resolve
6. Fix again → repeat until 10 or user says "good enough"

If a dimension rates below 7/10 and design tooling is available, offer to generate a mockup showing what 10/10 looks like for that dimension.

### The 7 Review Passes

**Priority hierarchy (never skip these):** Step 0 > mockups > Pass 2 (Interaction States) > Pass 4 (AI Slop) > Pass 1 (Info Architecture) > rest

**Pass 1: Information Architecture**
Rate 0-10: Does the plan define what the user sees first, second, third?

Fix to 10: Add information hierarchy to the plan. Include ASCII diagram of screen/page structure and navigation flow. Apply "constraint worship" — if you can only show 3 things, which 3?

Ask once per issue. Do not batch. Give recommendation + why.

**Pass 2: Interaction State Coverage**
Rate 0-10: Does the plan specify loading, empty, error, success, partial states?

Fix to 10: Add interaction state table:
```
FEATURE        | LOADING | EMPTY | ERROR | SUCCESS | PARTIAL
[UI feature]   | [spec]  | [spec]| [spec]| [spec]  | [spec]
```

For each state: describe what the user SEES, not backend behavior. Empty states are features — specify warmth, primary action, and context.

**Pass 3: User Journey and Emotional Arc**
Rate 0-10: Does the plan consider the user's emotional experience?

Fix to 10: Add user journey storyboard:
```
STEP | USER DOES     | USER FEELS      | PLAN SPECIFIES?
1    | Lands on page | [emotion]       | [what supports it?]
```

Apply time-horizon design: 5-second visceral, 5-minute behavioral, 5-year reflective.

**Pass 4: AI Slop Risk**
Rate 0-10: Does the plan describe specific, intentional UI — or generic patterns?

Fix to 10: Rewrite vague descriptions with specific alternatives.

**Design classification:** Determine rule set before evaluating.
- MARKETING/LANDING PAGE: hero-driven, brand-forward, conversion-focused
- APP UI: workspace-driven, data-dense, task-focused (dashboards, admin, settings)
- HYBRID: marketing shell with app-like sections

**Landing page rules:**
- First viewport reads as one composition, not a dashboard
- Brand-first hierarchy: brand > headline > body > CTA
- No default font stacks (Inter, Roboto, Arial, system)
- No flat single-color backgrounds — use gradients, images, subtle patterns
- Full-bleed hero, edge-to-edge, no inset/tiled/rounded variants
- Hero budget: brand, one headline, one supporting sentence, one CTA group, one image
- No cards in hero. Cards only when card IS the interaction
- One job per section: one purpose, one headline, one short supporting sentence
- 2-3 intentional motions minimum
- Copy: product language, not design commentary. "If deleting 30% improves it, keep deleting"
- Beautiful defaults: composition-first, brand as loudest text, two typefaces max, cardless by default

**App UI rules:**
- Calm surface hierarchy, strong typography, few colors
- Dense but readable, minimal chrome
- Organize: primary workspace, navigation, secondary context, one accent
- Avoid: dashboard-card mosaics, thick borders, decorative gradients, ornamental icons
- Cards only when card IS the interaction
- Copy: utility language — orientation, status, action (not mood/brand/aspiration)
- Section headings state what the area is or what the user can do ("Selected KPIs", "Plan status")

**Universal rules:** CSS variables for color system, no default font stacks, one job per section, cards earn their existence.

**AI slop blacklist (10 patterns that scream "AI-generated"):**
1. Purple/violet/indigo gradient backgrounds
2. The 3-column feature grid: icon-in-colored-circle + bold title + 2-line description, 3x symmetric
3. Icons in colored circles as section decoration
4. Centered everything (text-align: center on all headings, descriptions, cards)
5. Uniform bubbly border-radius on every element
6. Decorative blobs, floating circles, wavy SVG dividers
7. Emoji as design elements (rockets in headings, emoji as bullet points)
8. Colored left-border on cards
9. Generic hero copy ("Welcome to X", "Unlock the power of...")
10. Cookie-cutter section rhythm (hero → 3 features → testimonials → pricing → CTA, every section same height)

If visual mockups were generated, evaluate them against this blacklist. If a mockup falls into generic patterns, flag it and offer to regenerate with more specific direction.

**Pass 5: Design System Alignment**
Rate 0-10: Does the plan align with DESIGN.md?

Fix to 10: If DESIGN.md exists, annotate with specific tokens and components. If no DESIGN.md, flag the gap and recommend design-consultation. Flag any new component — does it fit the existing vocabulary?

**Pass 6: Responsive and Accessibility**
Rate 0-10: Does the plan specify mobile/tablet behavior, keyboard navigation, screen reader support?

Fix to 10: Add responsive specs per viewport — not "stacked on mobile" but intentional layout changes for each breakpoint. Add accessibility specifications:
- Keyboard navigation patterns
- ARIA landmarks
- Touch target sizes (44px minimum)
- Color contrast requirements (WCAG AA minimum)

**Pass 7: Unresolved Design Decisions**
Surface ambiguities that will haunt the implementer:
```
DECISION NEEDED              | IF DEFERRED, WHAT HAPPENS
What does empty state look like? | Engineer ships "No items found."
Mobile nav pattern?          | Desktop nav hides behind hamburger
```

If mockups were generated, reference them when surfacing decisions. A mockup makes decisions concrete.

Each decision = one question with recommendation + why + alternatives. Edit the plan with each decision as it's made.

### Post-Pass: Update Mockups

If review passes changed significant design decisions (information architecture restructure, new states, layout changes), offer to regenerate mockups to reflect the updated plan.

### Design Cognitive Patterns (internalize, don't enumerate)

These run automatically during review:

- **Seeing the system, not the screen:** Never evaluate in isolation — what comes before, after, when things break.
- **Empathy as simulation:** Run mental simulations: bad signal, one hand free, boss watching, first-timer vs power user.
- **Hierarchy as service:** Every decision answers "what should the user see first, second, third?" Respecting their time, not prettifying pixels.
- **Edge case paranoia:** What if the name is 47 chars? Zero results? Network fails? Colorblind? RTL language?
- **The "Would I notice?" test:** Invisible = perfect. The highest compliment is not noticing the design.
- **Principled taste:** "This feels wrong" is always traceable to a broken principle. Taste is debuggable.
- **Subtraction default:** "As little design as possible" (Rams). If an element doesn't earn its pixels, cut it.
- **Design for trust:** Every design decision either builds or erodes trust. Pixel-level intentionality.
- **Storyboard the journey:** Before touching pixels, trace the full emotional arc. Every moment is a scene with a mood.

## Question Format Rules

- **One issue = one question.** Never combine multiple issues.
- Describe the design gap concretely — what's missing and what the user will experience if it's not specified.
- Present 2-3 options. For each: effort to specify now, risk if deferred.
- Map recommendation to a specific Design Principle (one sentence).
- Number issues (1, 2, 3...) and letter options (A, B, C...). Label with combo: "3A", "3B".
- **Escape hatch:** If a section has no issues, say so and move on. If a gap has an obvious fix, state what you'll add and move on — only ask when there's a genuine design choice with meaningful tradeoffs.

## Quality Gates

- UI scope confirmed (exit early if no UI scope)
- Initial design rating given with specific reasoning
- Mockups generated (if tooling available and UI scope exists)
- All 7 passes completed or explicitly deferred with reasoning
- Interaction state table added to plan
- User journey storyboard added to plan
- AI slop patterns checked and called out
- DESIGN.md alignment checked
- Responsive specs added per viewport
- Accessibility specs added
- All unresolved decisions surfaced individually
- "NOT in scope" section written
- "What already exists" section written
- TODOS.md updates presented individually
- Completion summary produced showing before/after scores per pass
- Review log written

## Outputs

- Annotated/improved plan document with design decisions added
- Interaction state table
- User journey storyboard
- ASCII screen/page structure diagrams
- Approved mockups section in the plan (paths, directions, constraints)
- Completion summary:
  ```
  Pass 1 (Info Arch):  N/10 → N/10 after fixes
  Pass 2 (States):     N/10 → N/10 after fixes
  Pass 3 (Journey):    N/10 → N/10 after fixes
  Pass 4 (AI Slop):    N/10 → N/10 after fixes
  Pass 5 (Design Sys): N/10 → N/10 after fixes
  Pass 6 (Responsive): N/10 → N/10 after fixes
  Pass 7 (Decisions):  N resolved, N deferred
  Overall:             N/10 → N/10
  ```
- Review readiness dashboard entry

## Feeds Into

- >design-consultation (if no DESIGN.md exists and plan has significant UI)
- >ce:work or implementation (approved mockups are the visual spec)
- >qa or >qa-only (review passes define what to test visually)

## Harness Notes

**Visual mockups:** This skill depends heavily on a design generation binary for the mockup workflow (generate, variants, compare, iterate). If unavailable, fall back to text-based review for all passes. The comparison board feedback loop uses file polling — the server writes feedback.json when user submits. See harness-compat.md "Design binary" section.

**Outside voices:** Two parallel agents (one for hard-rules evaluation, one for completeness). These can be launched simultaneously if parallel execution is available. See harness-compat.md "Parallel subagents" section.
