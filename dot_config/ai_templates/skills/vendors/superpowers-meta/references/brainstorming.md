# Brainstorming

> Turn ideas into fully formed designs and specs through natural collaborative dialogue before any implementation begins.

## When to Use

Use before ANY creative work — creating features, building components, adding functionality, or modifying behavior. Every project goes through this process regardless of perceived simplicity. A "too simple" project is where unexamined assumptions cause the most wasted work.

## Inputs

- The user's idea or feature request
- Access to current project files, docs, and recent commits
- User availability for interactive dialogue

## Methodology

### HARD GATE

Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action until you have presented a design and the user has approved it. This applies to EVERY project regardless of perceived simplicity.

### Process Flow (Decision Tree)

```
Explore project context
  └─> Visual questions ahead?
        ├─ YES → Offer Visual Companion (own message, no other content)
        │         └─> Ask clarifying questions
        └─ NO  → Ask clarifying questions
                  └─> Propose 2-3 approaches
                        └─> Present design sections
                              └─> User approves design?
                                    ├─ NO (revise) → Present design sections (again)
                                    └─ YES → Write design doc
                                               └─> Spec self-review (fix inline)
                                                     └─> User reviews spec?
                                                           ├─ Changes requested → Write design doc (again)
                                                           └─ Approved → Invoke writing-plans skill
```

**The terminal state is invoking writing-plans.** Do NOT invoke frontend-design, mcp-builder, or any other implementation skill. The ONLY skill invoked after brainstorming is writing-plans.

### Checklist (complete in order)

Track each item and complete in order:

1. **Explore project context** — check files, docs, recent commits
2. **Offer visual companion** (if topic will involve visual questions) — this is its own message, not combined with a clarifying question. See Visual Companion section below.
3. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
4. **Propose 2-3 approaches** — with trade-offs and your recommendation
5. **Present design** — in sections scaled to their complexity, get user approval after each section
6. **Write design doc** — save to `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` and commit
7. **Spec self-review** — quick inline check for placeholders, contradictions, ambiguity, scope (see below)
8. **User reviews written spec** — ask user to review the spec file before proceeding
9. **Transition to implementation** — invoke writing-plans skill to create implementation plan

### Step 1: Explore Project Context

- Check out the current project state (files, docs, recent commits)
- Assess scope before asking detailed questions
- If the request describes multiple independent subsystems (e.g., "build a platform with chat, file storage, billing, and analytics"), flag this immediately — don't spend questions refining details of a project that needs to be decomposed first
- If the project is too large for a single spec, help the user decompose into sub-projects:
  - What are the independent pieces?
  - How do they relate?
  - What order should they be built?
  - Then brainstorm the first sub-project through the normal design flow
  - Each sub-project gets its own spec → plan → implementation cycle

### Step 2: Offer Visual Companion (Conditional)

**Only if** upcoming questions will involve visual content (mockups, layouts, diagrams):

Offer it once in its own message (no other content combined):

> "Some of what we're working on might be easier to explain if I can show it to you in a web browser. I can put together mockups, diagrams, comparisons, and other visuals as we go. This feature is still new and can be token-intensive. Want to try it? (Requires opening a local URL)"

**This offer MUST be its own message.** Do not combine it with clarifying questions, context summaries, or any other content. Wait for the user's response before continuing. If they decline, proceed with text-only brainstorming.

If they accept, consult the Visual Companion Guide (detailed below).

### Step 3: Ask Clarifying Questions

- Ask questions one at a time — never multiple questions in one message
- If a topic needs more exploration, break it into multiple questions
- Prefer multiple choice when possible, but open-ended is fine too
- Focus on: purpose, constraints, success criteria
- Only one question per message

### Step 4: Propose 2-3 Approaches

- Propose 2-3 different approaches with trade-offs
- Present options conversationally with your recommendation and reasoning
- Lead with your recommended option and explain why

### Step 5: Present the Design

- Once you understand what you're building, present the design in sections
- Scale each section to its complexity: a few sentences if straightforward, up to 200-300 words if nuanced
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

**Design for isolation and clarity:**
- Break the system into smaller units that each have one clear purpose, communicate through well-defined interfaces, and can be understood and tested independently
- For each unit, answer: what does it do, how do you use it, and what does it depend on?
- Test: Can someone understand what a unit does without reading its internals? Can you change the internals without breaking consumers? If not, the boundaries need work.
- Smaller, well-bounded units are easier to reason about and edit more reliably.
- When a file grows large, that's often a signal it's doing too much.

**Working in existing codebases:**
- Explore the current structure before proposing changes. Follow existing patterns.
- Where existing code has problems that affect the work (file too large, unclear boundaries, tangled responsibilities), include targeted improvements as part of the design.
- Don't propose unrelated refactoring. Stay focused on what serves the current goal.

### Step 6: Write Design Doc

- Save the validated design (spec) to: `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
  - User preferences for spec location override this default
- Apply clear, concise writing if an elements-of-style skill is available
- Commit the design document to git

### Step 7: Spec Self-Review

After writing the spec document, review it with fresh eyes:

1. **Placeholder scan:** Any "TBD", "TODO", incomplete sections, or vague requirements? Fix them.
2. **Internal consistency:** Do any sections contradict each other? Does the architecture match the feature descriptions?
3. **Scope check:** Is this focused enough for a single implementation plan, or does it need decomposition?
4. **Ambiguity check:** Could any requirement be interpreted two different ways? If so, pick one and make it explicit.

Fix any issues inline. No need to re-review — just fix and move on.

Optionally, delegate spec review to a subagent using the prompt template below.

### Step 8: User Review Gate

After the spec review loop passes, prompt the user:

> "Spec written and committed to `<path>`. Please review it and let me know if you want to make any changes before we start writing out the implementation plan."

Wait for the user's response. If they request changes, make them and re-run the spec review loop. Only proceed once the user approves.

### Step 9: Transition to Implementation

Invoke the writing-plans skill to create a detailed implementation plan. Do NOT invoke any other skill. writing-plans is the next step.

---

## Key Principles

- **One question at a time** — Don't overwhelm with multiple questions
- **Multiple choice preferred** — Easier to answer than open-ended when possible
- **YAGNI ruthlessly** — Remove unnecessary features from all designs
- **Explore alternatives** — Always propose 2-3 approaches before settling
- **Incremental validation** — Present design, get approval before moving on
- **Be flexible** — Go back and clarify when something doesn't make sense

---

## Visual Companion Guide

A browser-based companion for showing mockups, diagrams, and visual options during brainstorming. Available as a tool — not a mode. Accepting the companion means it's available for questions that benefit from visual treatment; it does NOT mean every question goes through the browser.

### Per-Question Decision Rule

Decide per question, not per session. The test: **would the user understand this better by seeing it than reading it?**

**Use the browser** when the content itself is visual:
- UI mockups — wireframes, layouts, navigation structures, component designs
- Architecture diagrams — system components, data flow, relationship maps
- Side-by-side visual comparisons — comparing two layouts, two color schemes, two design directions
- Design polish — questions about look and feel, spacing, visual hierarchy
- Spatial relationships — state machines, flowcharts, entity relationships rendered as diagrams

**Use the terminal** when the content is text or tabular:
- Requirements and scope questions — "what does X mean?", "which features are in scope?"
- Conceptual A/B/C choices — picking between approaches described in words
- Tradeoff lists — pros/cons, comparison tables
- Technical decisions — API design, data modeling, architectural approach selection
- Clarifying questions — anything where the answer is words, not a visual preference

A question *about* a UI topic is not automatically a visual question. "What kind of wizard do you want?" is conceptual — use the terminal. "Which of these wizard layouts feels right?" is visual — use the browser.

### How It Works

The server watches a directory for HTML files and serves the newest one to the browser. HTML content is written to `screen_dir`; the user sees it in their browser and can click to select options. Selections are recorded to `state_dir/events` and read on the next turn.

**Content fragments vs full documents:** If the HTML file starts with `<!DOCTYPE` or `<html`, the server serves it as-is. Otherwise the server automatically wraps the content in the frame template (header, CSS theme, selection indicator, interactive infrastructure). Write content fragments by default. Only write full documents when complete control over the page is needed.

### Starting a Session

```bash
# Start server with persistence (mockups saved to project)
scripts/start-server.sh --project-dir /path/to/project

# Returns JSON with: port, url, screen_dir, state_dir
```

Save `screen_dir` and `state_dir` from the response. Tell user to open the URL.

**Finding connection info:** The server writes its startup JSON to `$STATE_DIR/server-info`. If the server was launched in the background without capturing stdout, read that file to get the URL and port.

**Note:** Pass the project root as `--project-dir` so mockups persist in `.superpowers/brainstorm/` and survive server restarts. Without it, files go to `/tmp` and get cleaned up. Remind the user to add `.superpowers/` to `.gitignore` if not already there.

**Platform launch notes:**
- **macOS/Linux:** Default mode works — the script backgrounds the server itself
- **Windows:** Windows auto-detects and uses foreground mode, which blocks. Run with `run_in_background: true` so the server survives across conversation turns. Then read `$STATE_DIR/server-info` on the next turn.
- **Codex:** Codex reaps background processes. The script auto-detects `CODEX_CI` and switches to foreground mode. Run it normally — no extra flags needed.
- **Gemini CLI:** Use `--foreground` and set `is_background: true` on the shell tool call so the process survives across turns.
- **Other environments:** The server must keep running in the background across conversation turns. If your environment reaps detached processes, use `--foreground` and launch with your platform's background execution mechanism.

If the URL is unreachable from the browser (common in remote/containerized setups):
```bash
scripts/start-server.sh --project-dir /path/to/project --host 0.0.0.0 --url-host localhost
```
Use `--url-host` to control the hostname printed in the returned URL JSON.

### The Loop

1. **Check server is alive**, then **write HTML** to a new file in `screen_dir`:
   - Before each write, check that `$STATE_DIR/server-info` exists. If it doesn't (or `$STATE_DIR/server-stopped` exists), the server has shut down — restart it before continuing. The server auto-exits after 30 minutes of inactivity.
   - Use semantic filenames: `platform.html`, `visual-style.html`, `layout.html`
   - **Never reuse filenames** — each screen gets a fresh file
   - Write the file directly — never use cat/heredoc (dumps noise into terminal)
   - Server automatically serves the newest file

2. **Tell user what to expect and end your turn:**
   - Remind them of the URL (every step, not just first)
   - Give a brief text summary of what's on screen (e.g., "Showing 3 layout options for the homepage")
   - Ask them to respond in the terminal: "Take a look and let me know what you think. Click to select an option if you'd like."

3. **On your next turn** — after the user responds in the terminal:
   - Read `$STATE_DIR/events` if it exists — contains user's browser interactions (clicks, selections) as JSON lines
   - Merge with the user's terminal text to get the full picture
   - The terminal message is the primary feedback; `state_dir/events` provides structured interaction data

4. **Iterate or advance** — if feedback changes current screen, write a new file (e.g., `layout-v2.html`). Only move to the next question when the current step is validated.

5. **Unload when returning to terminal** — when the next step doesn't need the browser, push a waiting screen:

   ```html
   <!-- filename: waiting.html (or waiting-2.html, etc.) -->
   <div style="display:flex;align-items:center;justify-content:center;min-height:60vh">
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

   This prevents the user from staring at a resolved choice while the conversation has moved on.

6. Repeat until done.

### Writing Content Fragments

Write just the content that goes inside the page. The server wraps it in the frame template automatically.

**Minimal example:**

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

No `<html>`, no CSS, no `<script>` tags needed. The server provides all of that.

### CSS Classes Available

**Options (A/B/C choices):**
```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**Multi-select:** Add `data-multiselect` to the container to let users select multiple options. Each click toggles the item. The indicator bar shows the count.
```html
<div class="options" data-multiselect>
  <!-- same option markup — users can select/deselect multiple -->
</div>
```

**Cards (visual designs):**
```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup content --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

**Mockup container:**
```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard Layout</div>
  <div class="mockup-body"><!-- your mockup HTML --></div>
</div>
```

**Split view (side-by-side):**
```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

**Pros/Cons:**
```html
<div class="pros-cons">
  <div class="pros"><h4>Pros</h4><ul><li>Benefit</li></ul></div>
  <div class="cons"><h4>Cons</h4><ul><li>Drawback</li></ul></div>
</div>
```

**Mock elements (wireframe building blocks):**
```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display: flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field">
<div class="placeholder">Placeholder area</div>
```

**Typography and sections:**
- `h2` — page title
- `h3` — section heading
- `.subtitle` — secondary text below title
- `.section` — content block with bottom margin
- `.label` — small uppercase label text

### Browser Events Format

When the user clicks options in the browser, interactions are recorded to `$STATE_DIR/events` (one JSON object per line). The file is cleared automatically when a new screen is pushed.

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"c","text":"Option C - Complex Grid","timestamp":1706000108}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

The full event stream shows the user's exploration path — they may click multiple options before settling. The last `choice` event is typically the final selection, but the pattern of clicks can reveal hesitation or preferences worth asking about.

If `$STATE_DIR/events` doesn't exist, the user didn't interact with the browser — use only their terminal text.

### Design Tips

- **Scale fidelity to the question** — wireframes for layout, polish for polish questions
- **Explain the question on each page** — "Which layout feels more professional?" not just "Pick one"
- **Iterate before advancing** — if feedback changes current screen, write a new version
- **2-4 options max** per screen
- **Use real content when it matters** — for a photography portfolio, use actual images (e.g., Unsplash). Placeholder content obscures design issues.
- **Keep mockups simple** — focus on layout and structure, not pixel-perfect design

### File Naming

- Use semantic names: `platform.html`, `visual-style.html`, `layout.html`
- Never reuse filenames — each screen must be a new file
- For iterations: append version suffix like `layout-v2.html`, `layout-v3.html`
- Server serves newest file by modification time

### Cleaning Up

```bash
scripts/stop-server.sh $SESSION_DIR
```

If the session used `--project-dir`, mockup files persist in `.superpowers/brainstorm/` for later reference. Only `/tmp` sessions get deleted on stop.

---

## Spec Document Reviewer Subagent Prompt

Use this when delegating spec review to a subagent after writing the spec document.

**Purpose:** Verify the spec is complete, consistent, and ready for implementation planning.

**Dispatch after:** Spec document is written to `docs/superpowers/specs/`

```
You are a spec document reviewer. Verify this spec is complete and ready for planning.

**Spec to review:** [SPEC_FILE_PATH]

## What to Check

| Category     | What to Look For |
|--------------|------------------|
| Completeness | TODOs, placeholders, "TBD", incomplete sections |
| Consistency  | Internal contradictions, conflicting requirements |
| Clarity      | Requirements ambiguous enough to cause someone to build the wrong thing |
| Scope        | Focused enough for a single plan — not covering multiple independent subsystems |
| YAGNI        | Unrequested features, over-engineering |

## Calibration

Only flag issues that would cause real problems during implementation planning.
A missing section, a contradiction, or a requirement so ambiguous it could be
interpreted two different ways — those are issues. Minor wording improvements,
stylistic preferences, and "sections less detailed than others" are not.

Approve unless there are serious gaps that would lead to a flawed plan.

## Output Format

## Spec Review

**Status:** Approved | Issues Found

**Issues (if any):**
- [Section X]: [specific issue] - [why it matters for planning]

**Recommendations (advisory, do not block approval):**
- [suggestions for improvement]
```

**Reviewer returns:** Status, Issues (if any), Recommendations

---

## Quality Gates

- [ ] Project context explored before asking questions
- [ ] Visual companion offered separately (if applicable) before asking clarifying questions
- [ ] No more than one question per message
- [ ] 2-3 approaches proposed with trade-offs
- [ ] Design sections presented and approved before writing doc
- [ ] Design doc written and committed to correct path
- [ ] Spec self-review completed (placeholder scan, consistency, scope, ambiguity)
- [ ] User approved the written spec
- [ ] Only writing-plans invoked next (no other implementation skill)

## Outputs

- Written spec document at `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md`
- Git commit containing the spec
- Handoff to writing-plans skill

## Feeds Into

- **writing-plans** — creates the implementation plan from the approved spec

## Harness Notes

The Visual Companion feature requires a local server (`scripts/start-server.sh`) that watches a directory and serves HTML files. The server auto-exits after 30 minutes of inactivity. Platform-specific launch instructions are in the Visual Companion Guide above. If the harness does not support background processes, use `--foreground` mode with the platform's background execution mechanism.
