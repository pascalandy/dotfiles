# Design Shotgun

> Generate multiple AI design variants, open a side-by-side comparison board, collect structured feedback, and iterate until a direction is approved.

## When to Use

- User says "explore designs", "show me options", "design variants", "visual brainstorm", or "I don't like how this looks"
- User describes a UI feature but hasn't seen what it could look like (proactively suggest)
- Post-investigation, when implementation direction is clear but visual direction isn't
- Called by other skills (plan-design-review, design-consultation) to generate and compare mockups

## Inputs

- A description of the screen or component to design (gathered interactively if not provided)
- Existing codebase for auto-context (component structure, existing pages, routing)
- `DESIGN.md` in repo root if it exists (design system constraints)
- Prior approved designs from previous sessions (auto-loaded for taste memory)
- Optionally: a running local dev server to screenshot ("I don't like THIS" path)

## Methodology

### Step 0: Session Detection

Check for prior design explorations for this project (look for `approved.json` files in the project's design store).

If prior sessions found: offer to revisit them (reopen comparison board) or start fresh. If first time: introduce the tool briefly and proceed.

### Step 1: Context Gathering (5 dimensions)

Auto-gather first. Read `DESIGN.md`, list `src/` / `app/` / `components/`, check office-hours output if available.

If a local server is running AND the user referenced how something currently looks, screenshot the current page. This enables the "evolve from screenshot" path instead of generating from scratch.

Then ask the user for what's still missing, pre-filling what you already inferred. Cover:

1. **Who** is this for? (persona, expertise, audience)
2. **Job to be done** on this screen/page
3. **What already exists** in the codebase (components, patterns)
4. **User flow** -- how do users arrive and where do they go next?
5. **Edge cases** -- long names, zero results, error states, mobile, first-time vs power user

Two rounds max. After two rounds proceed with assumptions noted. Do not over-interrogate.

If `DESIGN.md` exists: follow it by default. Tell the user. If they want to go off-reservation, they can say so.

### Step 2: Taste Memory

Read prior approved designs (up to last 10 sessions). Extract patterns from approved variants. Include a taste bias in the brief: "User previously approved designs with these characteristics: [high contrast, generous whitespace, modern sans-serif]. Bias toward this aesthetic unless explicitly directed otherwise."

### Step 3: Generate Variants

**Step 3a: Concept generation.** Before any generation, write N text concepts describing each variant's creative direction. Each concept is a distinct direction, not a minor variation. Present as:

```
I'll explore 3 directions:
A) "Name" — one-line visual description
B) "Name" — one-line visual description
C) "Name" — one-line visual description
```

Draw on DESIGN.md, taste memory, and the user's brief to make them genuinely different.

**Step 3b: Confirm before generating.** Ask the user to confirm or adjust the concepts before spending any generation time. Note that parallel generation means total time is ~60s regardless of count.

Options: approve all, change some, add more, drop some. Max 2 rounds of concept adjustment.

**Step 3c: Parallel generation.** Launch N generation subagents simultaneously, one per variant. Each subagent handles its own generation, quality check, and retry (up to 3 retries on rate limit). Each reports back: `VARIANT_{letter}_DONE`, `VARIANT_{letter}_FAILED`, or `VARIANT_{letter}_RATE_LIMITED`.

For the "evolve from screenshot" path: each subagent uses the evolution command with the screenshot as input instead of generating from scratch.

If zero variants succeed via parallel generation: fall back to sequential generation one at a time, informing the user.

**Step 3d: Show variants inline immediately.** After all agents complete, display all generated images directly in the terminal/interface before opening any comparison board. Then report counts (N succeeded, M failed).

### Step 4: Comparison Board + Feedback Loop

Build the image list from whatever variant files actually exist (don't assume A/B/C all succeeded).

Open a comparison board serving all variants side-by-side in the browser.

**Feedback collection loop:**

Poll for two feedback file types:
- `feedback-pending.json` -- user clicked Regenerate/Remix/More Like This
- `feedback.json` -- user clicked Submit (final choice)

Poll every 5 seconds, up to 10 minutes.

**If regenerate feedback arrives:**
1. Read the regenerate action: "different" (new directions), "match" (match the winner), "more_like_X" (variants closer to X), "remix" (mix components: layout from A, colors from B), or custom text
2. Generate new variants using the updated brief
3. Reload the comparison board in the same browser tab
4. Poll again for the next feedback

**If submit feedback arrives (or polling times out):** Read `preferred`, `ratings` (per-variant 1-5), `comments` (per-variant text), and `overall` text.

**If the server fails to start or no feedback arrives in 10 minutes:** Fall back to asking the user directly: "Which variant do you prefer? Any feedback?"

**Feedback confirmation.** After receiving feedback via any path, output a clear summary:

```
PREFERRED: Variant X
RATINGS: A: 4/5, B: 3/5, C: 2/5
YOUR NOTES: [full text of comments]
DIRECTION: [overall or regenerate action]
```

Ask the user to confirm this is what they meant before saving.

### Step 5: Save and Next Steps

Save the approved choice as `approved.json` with the variant letter, feedback text, date, screen name, and current branch.

**Storage rule: all design artifacts (PNG mockups, comparison boards, approved.json) go to a persistent user-level design store, never to project directories, temp, or source control.**

If called from another skill: return the structured feedback for that skill to consume (it reads `approved.json` and the approved variant PNG).

If standalone, offer next steps: iterate more on the approved variant, start implementing, save as an approved mockup reference in the current plan, or done.

## Quality Gates

- [ ] Concepts confirmed before generation (no silent generation of unwanted directions)
- [ ] All variant results reported -- failures acknowledged, not silently skipped
- [ ] All variants shown inline before comparison board opens
- [ ] Feedback confirmed with explicit summary before saving
- [ ] `approved.json` written to persistent design store
- [ ] Prior taste memory consulted and reflected in generation brief
- [ ] DESIGN.md constraints followed (or user explicitly opted out)

## Outputs

- N variant PNG mockups saved to persistent project design store
- `approved.json` recording preferred variant, ratings, comments, date, branch
- Comparison board HTML
- Structured feedback summary (for calling skills)

## Feeds Into

- `>plan` -- approved mockup becomes design reference in plan file
- `>implement` -- build from the approved design direction

## Important Rules

1. **Never save to `.context/`, `docs/designs/`, `/tmp/`, or any project directory.** All design artifacts (PNGs, comparison boards, `approved.json`) go to `~/.gstack/projects/$SLUG/designs/`. This is enforced. Design artifacts are user data, not project files -- they persist across branches, conversations, and workspaces.
2. **Show variants inline before opening the board.** The user should see designs immediately in their terminal/interface. The browser board is for detailed feedback.
3. **Confirm feedback before saving.** Always summarize what you understood (PREFERRED, RATINGS, NOTES, DIRECTION) and ask the user to verify before writing `approved.json`.
4. **Taste memory is automatic.** Prior approved designs inform new generations by default.
5. **Two rounds max on context gathering.** Do not over-interrogate. Proceed with noted assumptions after two rounds.
6. **DESIGN.md is the default constraint.** Unless the user explicitly opts out, follow it.

## Harness Notes

Requires a design generation binary (`design generate`, `design variants`, `design evolve`, `design compare`). If the binary is unavailable, fall back to writing HTML wireframes directly.

Requires a headless browse capability for screenshotting current state (the "I don't like THIS" path). If unavailable, skip the screenshot and generate from description only.

Parallel variant generation requires subagent delegation (N independent agents running simultaneously). In a single-agent harness, fall back to sequential generation -- inform the user that generation will take N x 60s instead of ~60s.

The HTTP feedback polling loop requires running a local server. If the server cannot start, fall back to asking the user directly for feedback.

See `harness-compat.md`: Subagents, Browser/Screenshot, External Binaries.
