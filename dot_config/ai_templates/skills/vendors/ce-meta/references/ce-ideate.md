# ce:ideate

> Generate and critically evaluate grounded improvement ideas for the current project before brainstorming any single idea in depth.

## When to Use

- When asking "what should I improve", "give me ideas", "ideate on this project", "surprise me with improvements", "what would you change"
- Any request for AI-generated project improvement suggestions rather than refining the user's own idea
- Before `ce:brainstorm` — ideation identifies promising directions; brainstorm defines the selected one

**Workflow position:**
- `ce:ideate` answers: "What are the strongest ideas worth exploring?"
- `ce:brainstorm` answers: "What exactly should one chosen idea mean?"
- `ce:plan` answers: "How should it be built?"

This workflow produces a ranked ideation artifact in `docs/ideation/`. It does **not** produce requirements, plans, or code.

## Inputs

- Optional focus hint argument, which may be:
  - A concept such as `DX improvements`
  - A path such as `plugins/compound-engineering/skills/`
  - A constraint such as `low-complexity quick wins`
  - A volume hint such as `top 3`, `100 ideas`, or `raise the bar`
  - If no argument is provided, proceed with open-ended ideation

## Methodology

### Core Principles

1. **Ground before ideating** — Scan the actual codebase first. Do not generate abstract product advice detached from the repository.
2. **Diverge before judging** — Generate the full idea set before evaluating any individual idea.
3. **Use adversarial filtering** — The quality mechanism is explicit rejection with reasons, not optimistic ranking.
4. **Preserve the original prompt mechanism** — Generate many ideas, critique the whole list, then explain only the survivors in detail. Do not let extra process obscure this pattern.
5. **Use agent diversity to improve the candidate pool** — Parallel sub-agents are a support mechanism for richer idea generation and critique, not the core workflow itself.
6. **Preserve the artifact early** — Write the ideation document before presenting results so work survives interruptions.
7. **Route action into brainstorming** — Ideation identifies promising directions; `ce:brainstorm` defines the selected one precisely enough for planning.

### Phase 0: Resume and Scope

#### 0.1 Check for Recent Ideation Work

Look in `docs/ideation/` for ideation documents created within the last 30 days.

Treat a prior ideation doc as relevant when:
- The topic matches the requested focus
- The path or subsystem overlaps the requested focus
- The request is open-ended and there is an obvious recent open ideation doc
- Issue-grounded status matches: do not offer to resume a non-issue ideation when the current argument indicates issue-tracker intent, or vice versa

If a relevant doc exists, ask whether to:
1. Continue from it
2. Start fresh

If continuing:
- Read the document
- Summarize what has already been explored
- Preserve previous idea statuses and session log entries
- Update the existing file instead of creating a duplicate

#### 0.2 Interpret Focus and Volume

Infer three things from the argument:

- **Focus context** — concept, path, constraint, or open-ended
- **Volume override** — any hint that changes candidate or survivor counts
- **Issue-tracker intent** — whether the user wants issue/bug data as an input source

Issue-tracker intent triggers when the argument's primary intent is about analyzing issue patterns: `bugs`, `github issues`, `open issues`, `issue patterns`, `what users are reporting`, `bug reports`, `issue themes`.

Do NOT trigger on arguments that merely mention bugs as a focus: `bug in auth`, `fix the login issue`, `the signup bug` — these are focus hints, not requests to analyze the issue tracker.

When combined (e.g., `top 3 bugs in authentication`): detect issue-tracker intent first, volume override second, remainder is the focus hint.

**Default volume:**
- Each ideation sub-agent generates about 7–8 ideas (yielding 30–40 raw ideas across agents, ~20–30 after dedupe)
- Keep the top 5–7 survivors

**Honor clear overrides such as:**
- `top 3`
- `100 ideas`
- `go deep`
- `raise the bar`

Use reasonable interpretation rather than formal parsing.

### Phase 1: Codebase Scan

Before generating ideas, gather codebase context by running agents in parallel in the **foreground** (results are needed before proceeding):

**1. Quick context scan** — delegate a general-purpose sub-agent with this prompt:
> Read the project's AGENTS.md (or CLAUDE.md only as compatibility fallback, then README.md if neither exists), then discover the top-level directory layout. Return a concise summary (under 30 lines) covering:
> - project shape (language, framework, top-level directory layout)
> - notable patterns or conventions
> - obvious pain points or gaps
> - likely leverage points for improvement
>
> Keep the scan shallow — read only top-level documentation and directory structure. Do not analyze GitHub issues, templates, or contribution guidelines. Do not do deep code search.
>
> Focus hint: {focus_hint}

**2. Learnings search** — delegate `compound-engineering:research:learnings-researcher` with a brief summary of the ideation focus.

**3. Issue intelligence** (conditional) — if issue-tracker intent was detected in Phase 0.2, delegate `compound-engineering:research:issue-intelligence-analyst` with the focus hint. Run in parallel with agents 1 and 2.

If the agent returns an error (tool not installed, no remote, auth failure), log a warning ("Issue analysis unavailable: {reason}. Proceeding with standard ideation.") and continue.

If the agent reports fewer than 5 total issues, note "Insufficient issue signal for theme analysis" and proceed with default ideation frames in Phase 2.

**Consolidate all results into a grounding summary with sections:**
- **Codebase context** — project shape, notable patterns, obvious pain points, likely leverage points
- **Past learnings** — relevant institutional knowledge from `docs/solutions/`
- **Issue intelligence** (when present) — theme summaries preserving theme titles, descriptions, issue counts, and trend directions

Do **not** do external research in v1.

### Phase 2: Divergent Ideation

Follow this mechanism exactly:

1. Generate the full candidate list before critiquing any idea.
2. Each sub-agent targets about 7–8 ideas by default. With 4–6 agents this yields 30–40 raw ideas, which merge and dedupe to roughly 20–30 unique candidates. Adjust the per-agent target when volume overrides apply.
3. Push past the safe obvious layer. Each agent's first few ideas tend to be obvious — push past them.
4. Ground every idea in the Phase 1 scan.
5. Use this prompting pattern as the backbone: first generate many ideas → then challenge them systematically → then explain only the survivors in detail.
6. Give each ideation sub-agent the same: grounding summary, focus hint, per-agent volume target (~7–8 ideas by default), and instruction to generate raw candidates only, not critique.
7. When using sub-agents, assign each one a different ideation frame as a **starting bias, not a constraint**. Prompt each agent to begin from its assigned perspective but follow any promising thread wherever it leads — cross-cutting ideas that span multiple frames are valuable.

**Frame selection depends on whether issue intelligence is active:**

**When issue-tracker intent is active and themes were returned:**
- Each theme with `confidence: high` or `confidence: medium` becomes an ideation frame. The frame prompt uses the theme title and description as the starting bias.
- If fewer than 4 cluster-derived frames, pad with default frames in this order: "leverage and compounding effects", "assumption-breaking or reframing", "inversion, removal, or automation of a painful step"
- Cap at 6 total frames. If more than 6 themes qualify, use the top 6 by issue count; note remaining themes in the grounding summary as "minor themes" so sub-agents are still aware of them.

**When issue-tracker intent is NOT active (default):**
- user or operator pain and friction
- unmet need or missing capability
- inversion, removal, or automation of a painful step
- assumption-breaking or reframing
- leverage and compounding effects
- extreme cases, edge cases, or power-user pressure

8. Ask each ideation sub-agent to return a standardized structure for each idea so the orchestrator can merge and reason over outputs consistently. Prefer a compact JSON-like structure with:
   - title
   - summary
   - why_it_matters
   - evidence or grounding hooks
   - optional local signals such as boldness or focus_fit

9. Merge and dedupe the sub-agent outputs into one master candidate list.

10. **Synthesize cross-cutting combinations.** After deduping, scan the merged list for ideas from different frames that together suggest something stronger than either alone. If two or more ideas naturally combine into a higher-leverage proposal, add the combined idea to the list (expect 3–5 additions at most). This synthesis step belongs to the orchestrator because it requires seeing all ideas simultaneously.

11. Spread ideas across multiple dimensions when justified:
    - workflow/DX
    - reliability
    - extensibility
    - missing capabilities
    - docs/knowledge compounding
    - quality and maintenance
    - leverage on future work

12. If a focus was provided, pass it to every ideation sub-agent and weight the merged list toward it without excluding stronger adjacent ideas.

**The mechanism to preserve:**
- generate many ideas first
- critique the full combined list second
- explain only the survivors in detail

**The sub-agent pattern to preserve:**
- independent ideation with frames as starting biases first
- orchestrator merge, dedupe, and cross-cutting synthesis second
- critique only after the combined and synthesized list exists

### Phase 3: Adversarial Filtering

Review every generated idea critically.

**Prefer a two-layer critique:**
1. Have one or more skeptical sub-agents attack the merged list from distinct angles.
2. Have the orchestrator synthesize those critiques, apply the rubric consistently, score the survivors, and decide the final ranking.

Do not let critique agents generate replacement ideas in this phase unless explicitly refining.
Critique agents may provide local judgments, but final scoring authority belongs to the orchestrator so the ranking stays consistent.

**For each rejected idea, write a one-line reason.**

**Rejection criteria such as:**
- too vague
- not actionable
- duplicates a stronger idea
- not grounded in the current codebase
- too expensive relative to likely value
- already covered by existing workflows or docs
- interesting but better handled as a brainstorm variant, not a product improvement

**Survivor rubric — weigh:**
- groundedness in the current repo
- expected value
- novelty
- pragmatism
- leverage on future work
- implementation burden
- overlap with stronger ideas

**Target output:**
- Keep 5–7 survivors by default
- If too many survive, run a second stricter pass
- If fewer than 5 survive, report that honestly rather than lowering the bar

### Phase 4: Present the Survivors

Present the surviving ideas to the user before writing the durable artifact. This first presentation is a review checkpoint, not the final archived result.

**For each survivor, present:**
- title
- description
- rationale
- downsides
- confidence score
- estimated complexity

Then include a brief rejection summary so the user can see what was considered and cut.

Keep the presentation concise. The durable artifact holds the full record.

Allow brief follow-up questions and lightweight clarification before writing the artifact.

**Do not write the ideation doc yet unless:**
- The user indicates the candidate set is good enough to preserve
- The user asks to refine and continue in a way that should be recorded
- The workflow is about to hand off to `ce:brainstorm`, sharing, or session end

### Phase 5: Write the Ideation Artifact

Write the ideation artifact after the candidate set has been reviewed enough to preserve.

Always write or update the artifact before:
- Handing off to `ce:brainstorm`
- Ending the session

**Steps:**
1. Ensure `docs/ideation/` exists
2. Choose the file path:
   - `docs/ideation/YYYY-MM-DD-<topic>-ideation.md`
   - `docs/ideation/YYYY-MM-DD-open-ideation.md` when no focus exists
3. Write or update the ideation document

**Ideation document structure:**
```markdown
---
date: YYYY-MM-DD
topic: <kebab-case-topic>
focus: <optional focus hint>
---

# Ideation: <Title>

## Codebase Context
[Grounding summary from Phase 1]

## Ranked Ideas

### 1. <Idea Title>
**Description:** [Concrete explanation]
**Rationale:** [Why this improves the project]
**Downsides:** [Tradeoffs or costs]
**Confidence:** [0-100%]
**Complexity:** [Low / Medium / High]
**Status:** [Unexplored / Explored]

## Rejection Summary

| # | Idea | Reason Rejected |
|---|------|-----------------|
| 1 | <Idea> | <Reason rejected> |

## Session Log
- YYYY-MM-DD: Initial ideation — <candidate count> generated, <survivor count> survived
```

If resuming: update the existing file in place, append to the session log, and preserve explored markers.

### Phase 6: Refine or Hand Off

After presenting the results, ask what should happen next:
1. Brainstorm a selected idea
2. Refine the ideation
3. End the session

#### 6.1 Brainstorm a Selected Idea

If the user selects an idea:
- Write or update the ideation doc first
- Mark that idea as `Explored`
- Note the brainstorm date in the session log
- Invoke `ce:brainstorm` with the selected idea as the seed

Do **not** skip brainstorming and go straight to planning from ideation output.

#### 6.2 Refine the Ideation

Route refinement by intent:
- `add more ideas` or `explore new angles` → return to Phase 2
- `re-evaluate` or `raise the bar` → return to Phase 3
- `dig deeper on idea #N` → expand only that idea's analysis

After each refinement:
- Update the ideation document before any handoff, sharing, or session end
- Append a session log entry

#### 6.3 End the Session

When ending:
- Offer to commit only the ideation doc
- Do not create a branch
- Do not push
- If the user declines, leave the file uncommitted

## Quality Gates

Before finishing, check:
- The idea set is grounded in the actual repo
- The candidate list was generated before filtering
- The original many-ideas → critique → survivors mechanism was preserved
- If sub-agents were used, they improved diversity without replacing the core workflow
- Every rejected idea has a reason
- Survivors are materially better than a naive "give me ideas" list
- The artifact was written before any handoff, sharing, or session end
- Acting on an idea routes to `ce:brainstorm`, not directly to implementation

## Outputs

- Ranked ideation artifact at `docs/ideation/YYYY-MM-DD-<topic>-ideation.md`
- Rejection summary (in the artifact)
- Session log entry (in the artifact)

## Feeds Into

- `ce:brainstorm` — to define and refine the chosen idea into requirements
