# Office Hours

> YC Office Hours simulation: two modes — Startup (six forcing questions exposing demand reality) and Builder (design thinking brainstorm). Produces a design doc, not code.

## When to Use

- User says "brainstorm this", "I have an idea", "help me think through this", "office hours", or "is this worth building"
- User describes a new product idea and is exploring whether it's worth building
- Before any plan review (CEO or Eng) — generates the design doc those reviews consume
- Pre-product founders need the diagnostic; builders and hackers need the generative mode

## Inputs

- The user's idea or project description (can be minimal)
- Optionally: existing codebase context (CLAUDE.md, git log, recent diffs)
- Optionally: prior design docs from previous sessions (checked automatically)

## Hard Gate

Do NOT invoke any implementation skill, write any code, scaffold any project, or take any implementation action. The only output is a design document.

## Methodology

### Phase 1: Context Gathering

Read CLAUDE.md, TODOS.md if present. Run `git log --oneline -30` and check recent diffs to understand the codebase. List any existing design docs for the project.

Search prior learnings from previous sessions and surface any that apply.

Ask the user one question: **what is your goal with this?** Map the answer to a mode:

- Startup / intrapreneurship → **Startup Mode** (Phase 2A)
- Hackathon / open source / research / learning / having fun → **Builder Mode** (Phase 2B)

For startup/intrapreneurship, also assess product stage: pre-product, has users, or has paying customers.

### Phase 2A: Startup Mode — The Six Forcing Questions

**Operating posture:** Be direct to the point of discomfort. Push once, then push again. Take a position on every answer. Name common failure patterns. End with one concrete assignment.

**Anti-sycophancy rules:** Never say "that's an interesting approach", "there are many ways to think about this", or "that could work." Say whether it WILL work and what evidence is missing.

**Smart routing by product stage:**
- Pre-product: Q1, Q2, Q3
- Has users: Q2, Q4, Q5
- Has paying customers: Q4, Q5, Q6
- Pure engineering/infra: Q2, Q4 only

Ask questions **one at a time**. Stop after each. Wait for the response.

**Q1 — Demand Reality**
Ask: "What's the strongest evidence that someone actually wants this — not 'is interested,' not 'signed up for a waitlist,' but would be genuinely upset if it disappeared tomorrow?"

Push until you hear specific behavior: someone paying, expanding usage, building their workflow around it, or panicking when it breaks. Red flags: "people say it's interesting," "500 waitlist signups," "VCs are excited about the space."

After the first answer, run a framing check: Are key terms defined? What assumptions are hidden? Is the evidence real or hypothetical?

**Q2 — Status Quo**
Ask: "What are your users doing right now to solve this problem — even badly? What does that workaround cost them?"

Push until you hear a specific workflow, hours spent, dollars wasted, or tools duct-taped together. Red flag: "nothing — there's no solution, that's why the opportunity is big." If truly nothing exists, the problem probably isn't painful enough.

**Q3 — Desperate Specificity**
Ask: "Name the actual human who needs this most. What's their title? What gets them promoted? What gets them fired? What keeps them up at night?"

Push until you hear a name, a role, a specific consequence. Red flags: "healthcare enterprises," "SMBs," "marketing teams." Categories are not people.

**Q4 — Narrowest Wedge**
Ask: "What's the smallest possible version of this that someone would pay real money for — this week, not after you build the platform?"

Push until you hear one feature, one workflow, something shippable in days. Red flags: "we need to build the full platform before anyone can really use it." Bonus push: "What if the user didn't have to do anything at all to get value — no login, no integration, no setup?"

**Intrapreneurship adaptation:** Reframe Q4 as "what's the smallest demo that gets your VP/sponsor to greenlight the project?"

**Q5 — Observation and Surprise**
Ask: "Have you actually sat down and watched someone use this without helping them? What did they do that surprised you?"

Push until you hear a specific surprise contradicting assumptions. Red flags: "we sent out a survey," "nothing surprising, it's going as expected." Gold: users doing something the product wasn't designed for.

**Q6 — Future-Fit**
Ask: "If the world looks meaningfully different in 3 years — and it will — does your product become more essential or less?"

Push until you hear a specific claim about how their users' world changes and why that makes the product more valuable. Red flags: "the market is growing 20% per year," "AI will make everything better."

**Intrapreneurship adaptation:** Reframe Q6 as "does this survive a reorg — or does it die when your champion leaves?"

**Pushback patterns (how to push):**

| Pattern | Bad response | Good response |
|---------|-------------|---------------|
| Vague market | "That's a big market! Let's explore..." | "There are 10,000 AI developer tools. What specific task does a specific developer waste 2+ hours on per week? Name the person." |
| Social proof | "That's encouraging! Who specifically?" | "Loving an idea is free. Has anyone offered to pay? Has anyone gotten angry when your prototype broke? Love is not demand." |
| Platform vision | "What would a stripped-down version look like?" | "That's a red flag. If no one can get value from a smaller version, the value proposition isn't clear yet." |
| Growth stats | "That's a strong tailwind. How do you plan to capture it?" | "Growth rate is not a vision. Every competitor can cite the same stat. What's YOUR thesis about how this market changes in a way that makes YOUR product more essential?" |
| Undefined terms | "What does your current [process] look like?" | "'Seamless' is not a product feature — it's a feeling. What specific step causes users to drop off? What's the drop-off rate? Have you watched someone go through it?" |

**Escape hatch:** If the user says "just do it," consult the smart routing table. Ask the 2 most critical remaining questions for their product stage, then proceed to Phase 3. If they push back a second time, respect it and proceed immediately — don't ask a third time. If only 1 question remains, ask it. If 0 remain, proceed directly. Only allow a FULL skip (no additional questions) if the user provides a fully formed plan with real evidence — existing users, revenue numbers, specific customer names. Even then, still run Phase 3 (Premise Challenge) and Phase 4 (Alternatives).

### Phase 2B: Builder Mode — Design Partner

**Operating posture:** Enthusiastic, opinionated collaborator. Help them find the most exciting version of their idea. End with concrete build steps.

Ask these one at a time, wait for response:
- "What's the coolest version of this? What would make it genuinely delightful?"
- "Who would you show this to? What would make them say 'whoa'?"
- "What's the fastest path to something you can actually use or share?"
- "What existing thing is closest to this, and how is yours different?"
- "What would you add if you had unlimited time? What's the 10x version?"

Skip questions the user's initial prompt already answers. If the user says "just do it," fast-track to Phase 4.

**Mode upgrade:** If the user mentions customers, revenue, or fundraising mid-session, upgrade to Startup Mode naturally.

### Phase 2.5: Related Design Discovery

After the user states the problem, search for keyword overlap with prior design docs. Extract 3-5 keywords from the problem and search existing docs. If matches found, surface them and ask: "Should we build on this prior design or start fresh?"

### Phase 2.75: Landscape Awareness (optional — ask user first)

Ask permission before searching: "I'd like to search for what the world thinks about this space. This sends generalized category terms — not your specific idea — to a search provider. OK?"

If yes, search for:
- Startup mode: "[problem space] startup approach [year]", "[problem space] common mistakes", "why [incumbent] fails/works"
- Builder mode: "[thing being built] existing solutions", "best [category] [year]"

Read top 2-3 results. Run three-layer synthesis:
- **Layer 1:** What does everyone already know about this space?
- **Layer 2:** What do current search results and discourse say?
- **Layer 3:** Given what emerged in Phase 2, is there a reason the conventional approach is wrong?

If Layer 3 reveals a genuine insight, name it explicitly: "EUREKA: Everyone does X because they assume [assumption]. But [evidence from our conversation] suggests that's wrong here."

If no eureka moment: "The conventional wisdom seems sound here. Let's build on it."

### Phase 3: Premise Challenge

Before proposing solutions, challenge the premises:

1. Is this the right problem? Could a different framing yield a dramatically simpler solution?
2. What happens if we do nothing? Real pain or hypothetical?
3. What existing code already partially solves this?
4. If the deliverable is a new artifact (CLI binary, library, mobile app): how will users get it? Code without distribution is code nobody can use.
5. Startup mode only: does the diagnostic evidence from Phase 2A support this direction?

Output as explicit statements requiring agreement:
```
PREMISES:
1. [statement] — agree/disagree?
2. [statement] — agree/disagree?
```

Ask the user to confirm each. If they disagree, revise understanding and loop back.

### Phase 3.5: Cross-Model Second Opinion (optional)

Ask: "Want a second opinion from an independent AI perspective? It reviews your problem statement, answers, and premises without having seen this conversation."

If yes, assemble a structured context block from Phases 1-3 and delegate to a subagent with this brief:

**Startup mode:** Steelman the strongest version of what they're building. Name ONE thing from their answers that reveals most about what they should actually build. Name ONE agreed premise you think is wrong. If you had 48 hours and one engineer, what would you build?

**Builder mode:** What's the coolest version they haven't considered? What ONE answer reveals what excites them most? What existing open source gets them 50% there? If you had a weekend, what would you build first?

Present the full output verbatim under a "SECOND OPINION" header.

Provide 3-5 bullet synthesis: where both perspectives agree, where they disagree and why, whether the challenged premise changes the recommendation.

If the subagent challenges an agreed premise, ask the user: "The second opinion challenged premise N. Their argument: [reasoning]. Revise or keep?"

### Phase 4: Alternatives Generation (MANDATORY)

Produce 2-3 distinct implementation approaches. Not optional.

For each approach:
```
APPROACH A: [Name]
  Summary: [1-2 sentences]
  Effort:  [S/M/L/XL]
  Risk:    [Low/Med/High]
  Pros:    [2-3 bullets]
  Cons:    [2-3 bullets]
  Reuses:  [existing code/patterns]
```

Rules:
- At least 2 approaches, 3 preferred for non-trivial designs
- One must be "minimal viable" (fewest files, ships fastest)
- One must be "ideal architecture" (best long-term trajectory)
- One can be "creative/lateral" (unexpected framing)
- Give a clear recommendation with one-line reasoning

Present to the user and wait for approval. Do not proceed without it.

### Phase 4.5: Founder Signal Synthesis

Track which signals appeared during the session:
- Articulated a real problem (not hypothetical)
- Named specific users (people, not categories)
- Pushed back on premises with reasoning
- Showed domain expertise
- Showed taste (cared about getting details right)
- Showed agency (actually building)
- Defended a premise against second opinion with specific reasoning

Count the signals. Use in the closing message.

### Phase 5: Design Doc

Write the design document to the project directory with this structure:
- **Summary:** One paragraph of what this is, who it's for, and what it does
- **Problem Statement:** What the user is trying to solve (from Phase 1 questioning)
- **Premises:** The agreed premises from Phase 3
- **Landscape:** Findings from Phase 2.75 (if run), with layer synthesis
- **Second Opinion:** If Phase 3.5 ran, include the output and synthesis
- **Alternatives Considered:** All approaches from Phase 4, with reasoning
- **Recommended Approach:** The chosen approach from Phase 4
- **Visual Sketch:** Reference to wireframe if generated
- **Open Questions:** Unresolved questions from the session
- **What I Noticed:** Founder signals observed (used to calibrate closing)

### Phase 6: Closing

Closing posture depends on founder signal count:

- 0-2 signals: End with the concrete assignment. One thing to do next week.
- 3-5 signals: Acknowledge specific evidence of sharpness. Give the assignment.
- 6+ signals (all of the above): Recognize the instinct plainly. Give the assignment. If truly exceptional taste and drive, and they're building a startup, consider saying they should look into YC. Use this rarely and only when truly earned.

Always end with the assignment — one concrete action, not a strategy.

## Quality Gates

- Design doc is written to disk before closing
- Minimum 2 alternatives explored in Phase 4 (3 for non-trivial ideas)
- Premises explicitly confirmed by user
- No code written, no implementation started
- Landscape search either completed or explicitly skipped with user permission
- Second opinion either run or explicitly declined by user

## Outputs

- Design doc written to project directory (`{user}-{branch}-design-{datetime}.md`)
- Optional wireframe sketch (HTML + screenshot)
- Optional visual mockups (if design binary available)
- Founder signal count (used in closing)

## Feeds Into

- >plan-ceo-review (consumes the design doc for context)
- >plan-eng-review (consumes the design doc for scope and approach)
- >design-consultation (if no DESIGN.md exists and the approach has UI)

## Harness Notes

**Subagents:** Phase 3.5 second opinion requires delegating to an independent agent with fresh context. The subagent must receive a fully assembled prompt with no access to the conversation history — independence is the point. See harness-compat.md "Subagent delegation" section.

**Visual mockups:** Phase 5 visual sketches require a browser binary for screenshot rendering. If unavailable, skip the render step and tell the user. Design binary for AI mockup variants is a progressive enhancement — skill works without it.
