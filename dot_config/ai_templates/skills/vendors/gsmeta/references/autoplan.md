# Autoplan

> Auto-review pipeline -- reads the full CEO, design, and eng review skill files and runs them sequentially with auto-decisions using 6 principles. Surfaces taste decisions and user challenges at a final approval gate. One command, fully reviewed plan out.

## When to Use

- User says "auto review", "autoplan", "run all reviews", "review this plan automatically", or "make the decisions for me"
- User has a plan file and wants the full review gauntlet without answering 15-30 intermediate questions
- Proactively suggest when a plan file exists and the user wants to proceed quickly

## Inputs

- A plan file (markdown) for the current branch
- The current codebase (read access to verify plan claims against actual code)
- `CLAUDE.md` and `TODOS.md` for context
- Git log and diff against base branch (for context and blast radius assessment)
- Full CEO, Design, and Eng review skill files (read from disk at runtime -- this is what "auto" means)

## Methodology

### The 6 Decision Principles

These rules auto-answer every intermediate question during the review phases:

1. **Choose completeness** -- ship the whole thing, pick the approach covering more edge cases
2. **Boil lakes** -- fix everything in the blast radius (files modified by this plan + direct importers) if in blast radius AND less than 1 day of effort (< 5 files, no new infra). Auto-approve. Flag oceans (multi-quarter migrations).
3. **Pragmatic** -- if two options fix the same thing, pick the cleaner one
4. **DRY** -- rejects anything that duplicates existing functionality
5. **Explicit over clever** -- 10-line obvious fix beats a 200-line abstraction; pick what a new contributor reads in 30 seconds
6. **Bias toward action** -- merge over review cycles over stale deliberation; flag concerns but don't block

**Conflict resolution by phase:**
- CEO phase: P1 (completeness) + P2 (boil lakes) dominate
- Eng phase: P5 (explicit) + P3 (pragmatic) dominate
- Design phase: P5 (explicit) + P1 (completeness) dominate

### Decision Classification

**Mechanical** -- one clearly right answer (run codex: always yes; reduce scope on a complete plan: always no). Auto-decide silently.

**Taste** -- reasonable people could disagree. Auto-decide with recommendation, but surface at the final gate. Three natural sources:
1. Close approaches -- top two are both viable with different tradeoffs
2. Borderline scope -- in blast radius but 3-5 files, or ambiguous radius
3. Disagreements between the two review voices

**User Challenge** -- both independent models agree the user's stated direction should change (merge features, split workflows, add/remove scope). This is qualitatively different from taste. Never auto-decided. Always surfaced at the final gate with:
- What the user said (their original direction)
- What both models recommend
- Why
- What context might be missing (explicit acknowledgment of blind spots)
- Cost if the models are wrong (downside of overriding the user's original direction)

The user's original direction is the default. Models must make the case for change, not the other way around. Security/feasibility blockers get an explicit warning: "Both models flag this as a security/feasibility risk, not just a preference."

### What "Auto-Decide" Means

Auto-decide replaces the user's judgment with the 6 principles. It does NOT replace the analysis.

**Every section from the loaded skill files must still be executed at full depth:**
- Read the actual code, diffs, and files each section references
- Produce every output the section requires (diagrams, tables, registries, artifacts)
- Identify every issue the section is designed to catch
- Decide each issue using the 6 principles (instead of asking the user)
- Log each decision in the audit trail
- Write all required artifacts to disk

"No issues found" is valid -- but only after doing the analysis and stating what was examined and why nothing was flagged (1-2 sentences minimum). A one-sentence summary of a review section is a skip, not full depth. If you catch yourself writing fewer than 3 sentences for any review section, you are compressing.

**Two gates -- never auto-decided:**
1. Premises (Phase 1) -- require human judgment about what problem to solve
2. User Challenges -- when both models agree the user's stated direction should change

### Phase 0: Intake and Restore Point

**Capture a restore point.** Before doing anything, save the plan file's current state to an external file. The restore path uses: project slug + branch + timestamp. Write the verbatim plan contents there with re-run instructions. Prepend a one-line HTML comment to the plan file pointing at the restore path.

**Read context.** Read `CLAUDE.md`, `TODOS.md`, recent git log (last 30 commits), and the diff stat against base branch.

**Discover design docs.** Look for office-hours design docs scoped to the current branch.

**Detect UI scope.** Search the plan for view/rendering terms (component, screen, form, button, modal, layout, dashboard, sidebar, nav, dialog). Require 2+ matches. Exclude false positives ("page" alone, "UI" in acronyms). If UI scope detected, Phase 2 runs. If not, Phase 2 is skipped.

**Load skill files.** Read each review skill file from disk:
- CEO review skill file
- Design review skill file (only if UI scope detected)
- Eng review skill file

**Section skip list.** When following a loaded skill file, skip these sections (already handled by autoplan): Preamble, AskUserQuestion Format, Completeness Principle, Search Before Building, Contributor Mode, Completion Status Protocol, Telemetry, Step 0: Detect base branch, Review Readiness Dashboard, Plan File Review Report, Prerequisite Skill Offer, Outside Voice / Design Outside Voices (parallel).

Follow only the review-specific methodology, sections, and required outputs.

**Output a plan summary:** what the plan is for, whether UI scope was detected, and that the review pipeline is starting with auto-decisions.

### Phase 1: CEO Review (Strategy and Scope)

Follow the CEO review skill at full depth. Override: every intermediate question auto-decided using the 6 principles. EXCEPT: premises require user confirmation (the one gate that is not auto-decided).

**Override rules:**
- Mode selection: SELECTIVE EXPANSION
- Premises: accept reasonable ones (P6), challenge only clearly wrong ones. **GATE: present premises to user for confirmation.**
- Alternatives: pick highest completeness (P1). If tied, pick simplest (P5). If top 2 are close, mark TASTE DECISION.
- Scope expansion: in blast radius + less than 1 day CC effort (< 5 files, no new infra) -- approve (P2). Outside blast radius -- defer to TODOS.md (P3). Duplicates -- reject (P4). Borderline (3-5 files) -- mark TASTE DECISION.
- Run all 10 review sections at full depth.

**Dual voices.** Run two independent voices sequentially (not in parallel):
1. A Claude subagent with no prior review context (fresh, independent perspective)
2. The OpenAI Codex CLI with adversarial CEO prompt (if available)

Each is given an adversarial framing: challenge strategic foundations, identify premises that are assumed not stated, find the 6-month regret scenario, surface alternatives dismissed too quickly, assess competitive risk.

Present Claude subagent output under `CLAUDE SUBAGENT (CEO -- strategic independence):` header. Present Codex output under `CODEX SAYS (CEO -- strategy challenge):` header. If only one voice is available, tag the result accordingly.

Build a CEO consensus table:
```
CEO DUAL VOICES -- CONSENSUS TABLE:
═══════════════════════════════════════════════════════════════
  Dimension                           Claude  Codex  Consensus
  ────────────────────────────────── ─────── ─────── ─────────
  1. Premises valid?
  2. Right problem to solve?
  3. Scope calibration correct?
  4. Alternatives sufficiently explored?
  5. Competitive/market risks covered?
  6. 6-month trajectory sound?
═══════════════════════════════════════════════════════════════
CONFIRMED = both agree. DISAGREE = models differ (taste decision or user challenge).
```

**Mandatory Phase 1 outputs (must exist in plan file before Phase 2 begins):**
- Premise challenge with specific premises named and evaluated
- Existing code leverage map (sub-problems mapped to existing code)
- Dream state delta (CURRENT → THIS PLAN → 12-MONTH IDEAL)
- Implementation alternatives table (2-3 approaches with effort/risk/tradeoffs)
- "NOT in scope" section with deferred items and rationale
- Error and Rescue Registry table
- Failure Modes Registry table
- CEO completion summary
- CEO consensus table
- Decision audit trail rows for all CEO auto-decisions

**Phase transition:** Emit a summary -- Codex N concerns, Claude subagent N issues, consensus X/6 confirmed. Do NOT begin Phase 2 until all Phase 1 outputs are written.

### Phase 2: Design Review (conditional -- skip if no UI scope)

Follow the design review skill at full depth. Override: every intermediate question auto-decided using the 6 principles.

**Override rules:**
- Structural issues (missing states, broken hierarchy): auto-fix (P5)
- Aesthetic/taste issues: mark TASTE DECISION
- Design system alignment: auto-fix if DESIGN.md exists and fix is obvious

**Dual voices.** Same pattern as Phase 1: Claude subagent first (fresh, independent), then Codex (with CEO phase findings included in its context -- the subagent stays truly independent, Codex gets prior context).

Produce a design litmus scorecard (consensus table) across all 7 design dimensions.

**Mandatory Phase 2 outputs (if Phase 2 ran):**
- All 7 design dimensions evaluated with scores
- Design litmus scorecard (consensus table)
- Issues identified and auto-decided
- Design completion summary

**Phase transition:** Emit summary, verify outputs written. Do NOT begin Phase 3 until complete.

### Phase 3: Eng Review

Follow the eng review skill at full depth. Override: every intermediate question auto-decided using the 6 principles.

**Override rules:**
- Scope challenge: never reduce (P2)
- Architecture choices: explicit over clever (P5)
- Evals: always include all relevant suites (P1)

**Dual voices.** Same pattern: Claude subagent first (fresh), then Codex (with CEO and Design findings in context -- only the Codex prompt, not the subagent).

Produce an eng consensus table across 6 dimensions: architecture sound, test coverage sufficient, performance risks addressed, security threats covered, error paths handled, deployment risk manageable.

**Section 3 (Test Review) -- NEVER SKIP OR COMPRESS.** This requires reading actual code, not summarizing from memory.
- Read the diff and affected files
- Build the test diagram: list every new UX flow, data flow, codepath, and branch
- For each item: what type of test covers it? Does one exist? Gaps?
- Auto-deciding test gaps means: identify the gap, decide whether to add a test or defer (with rationale and principle), log the decision. Not skipping the analysis.

**Mandatory Phase 3 outputs:**
- Architecture ASCII diagram showing new components and relationships to existing ones
- Test diagram mapping codepaths to test coverage
- Test plan artifact written to disk at project store
- "NOT in scope" section
- "What already exists" section
- Failure modes registry with critical gap assessment
- Eng completion summary
- Eng consensus table
- TODOS.md updates (collected from all phases)
- Decision audit trail rows for all Eng auto-decisions

### Decision Audit Trail

After each auto-decision, append a row to the plan file (incrementally, not accumulated in memory):

```markdown
## Decision Audit Trail

| # | Phase | Decision | Classification | Principle | Rationale | Rejected |
|---|-------|----------|----------------|-----------|-----------|---------|
```

Write one row per decision. Log every choice -- no silent auto-decisions.

### Pre-Gate Verification

Before presenting the final gate, verify that all required outputs were actually produced. Check the plan file for each mandatory item from all three phases. If any are missing: attempt to produce them (max 2 attempts). Proceed to gate with a warning noting any items that remain incomplete. Do not loop indefinitely.

### Phase 4: Final Approval Gate

Present the full review state in one message with AskUserQuestion:

```
## /autoplan Review Complete

### Plan Summary
[1-3 sentences]

### Decisions Made: N total (M auto-decided, K taste choices, J user challenges)

### User Challenges (both models disagree with your stated direction)
[For each:]
Challenge N: [title] (from [phase])
You said: [user's original direction]
Both models recommend: [the change]
Why: [reasoning]
What we might be missing: [blind spots]
If we're wrong, the cost is: [downside of changing]
[If security/feasibility: "Both models flag this as a security/feasibility risk, not just a preference."]
Your call -- your original direction stands unless you explicitly change it.

### Your Choices (taste decisions)
[For each:]
Choice N: [title] (from [phase])
I recommend [X] -- [principle]. But [Y] is also viable:
  [1-sentence downstream impact if you pick Y]

### Auto-Decided: M decisions [see Decision Audit Trail in plan file]

### Review Scores
- CEO: [summary]
- CEO Voices: Codex [summary], Claude subagent [summary], Consensus X/6 confirmed
- Design: [summary or "skipped, no UI scope"]
- Design Voices: Codex [summary], Claude subagent [summary], Consensus X/7 confirmed (or "skipped")
- Eng: [summary]
- Eng Voices: Codex [summary], Claude subagent [summary], Consensus X/6 confirmed

### Cross-Phase Themes
[For any concern that appeared in 2+ phases' dual voices independently:]
Theme: [topic] -- flagged in [Phase 1, Phase 3]. High-confidence signal.
[If none: "No cross-phase themes -- each phase's concerns were distinct."]

### Deferred to TODOS.md
[Items auto-deferred with reasons]
```

**Cognitive load management:**
- 0 user challenges: skip User Challenges section
- 0 taste decisions: skip Your Choices section
- 1-7 taste decisions: flat list
- 8+ taste decisions: group by phase, add warning: "This plan had unusually high ambiguity ([N] taste decisions). Review carefully."

**Gate options:**
- A) Approve as-is (accept all recommendations)
- B) Approve with overrides (user specifies which taste decisions to change)
- B2) Approve with user challenge responses (accept or reject each challenge)
- C) Interrogate (ask about any specific decision)
- D) Revise (plan needs changes -- re-run affected phases, max 3 cycles)
- E) Reject (start over)

**Option handling:**
- A: mark APPROVED, write review logs (see Completion below), suggest `/ship`
- B: ask which overrides, apply them, re-present the gate
- B2: accept or reject each challenge, apply accepted changes, re-present gate
- C: answer freeform, re-present gate
- D: make changes, re-run affected phases (scope → Phase 1B, design → Phase 2, test plan/arch → Phase 3). Max 3 revision cycles.
- E: start over

### Completion

On approval, write 3 separate review log entries so ship's readiness dashboard recognizes them:

```
gstack-review-log '{"skill":"plan-ceo-review","timestamp":"TIMESTAMP","status":"STATUS","unresolved":N,"critical_gaps":N,"mode":"SELECTIVE_EXPANSION","via":"autoplan","commit":"COMMIT"}'

gstack-review-log '{"skill":"plan-eng-review","timestamp":"TIMESTAMP","status":"STATUS","unresolved":N,"critical_gaps":N,"issues_found":N,"mode":"FULL_REVIEW","via":"autoplan","commit":"COMMIT"}'
```

If Phase 2 ran (UI scope detected):
```
gstack-review-log '{"skill":"plan-design-review","timestamp":"TIMESTAMP","status":"STATUS","unresolved":N,"via":"autoplan","commit":"COMMIT"}'
```

Dual-voice consensus logs (one per phase that ran):
```
gstack-review-log '{"skill":"autoplan-voices","timestamp":"TIMESTAMP","status":"STATUS","source":"SOURCE","phase":"ceo","via":"autoplan","consensus_confirmed":N,"consensus_disagree":N,"commit":"COMMIT"}'
gstack-review-log '{"skill":"autoplan-voices","timestamp":"TIMESTAMP","status":"STATUS","source":"SOURCE","phase":"eng","via":"autoplan","consensus_confirmed":N,"consensus_disagree":N,"commit":"COMMIT"}'
```

SOURCE = "codex+subagent", "codex-only", "subagent-only", or "unavailable". STATUS = "clean" if no unresolved issues, "issues_open" otherwise. Replace N with actual counts from consensus tables.

Suggest next step: `/ship` when ready to create the PR.

## Quality Gates

- [ ] Restore point captured before any edits
- [ ] Premise gate passed (user confirmed)
- [ ] All Phase 1 mandatory outputs in plan file before Phase 2 begins
- [ ] All Phase 2 mandatory outputs (if ran) before Phase 3 begins
- [ ] Architecture ASCII diagram produced (Phase 3)
- [ ] Test diagram produced (Phase 3)
- [ ] Test plan artifact written to disk (Phase 3)
- [ ] Decision audit trail has at least one row per auto-decision
- [ ] Pre-gate verification checklist run
- [ ] All taste decisions and user challenges surfaced at final gate

## Outputs

- Updated plan file with all review findings, diagrams, registries, and artifacts
- Decision Audit Trail (in plan file)
- Test plan artifact (on disk)
- TODOS.md updates
- Review log entries (for ship's readiness dashboard)

## Feeds Into

- `>ship` -- review logs written by autoplan are recognized by ship's readiness gate

## Important Rules

- **Never abort.** The user chose autoplan. Respect that choice. Surface all taste decisions at the gate -- never redirect to interactive review mid-run.
- **Two gates only.** The only non-auto-decided questions are: (1) premise confirmation in Phase 1, and (2) User Challenges when both models agree the user's stated direction should change. Everything else uses the 6 principles.
- **Log every decision.** No silent auto-decisions. Every choice gets a row in the audit trail.
- **Full depth means full depth.** Do not compress or skip sections from the loaded skill files (except the skip list in Phase 0). Read the code each section asks for, produce every required output, identify every issue, decide each one. If you catch yourself writing fewer than 3 sentences for any review section, you are compressing. "No issues found" is valid only after doing the analysis.
- **Artifacts are deliverables.** Test plan artifact, failure modes registry, error/rescue table, ASCII diagrams -- these must exist on disk or in the plan file when the review completes. If they don't exist, the review is incomplete.
- **Sequential order.** CEO → Design → Eng. Each phase builds on the last. Never run phases in parallel.

## Harness Notes

Dual voices (subagent + Codex) run sequentially, not in parallel. The Claude subagent is dispatched as an independent delegate with a fresh context window. In single-agent harnesses, simulate the subagent with a second analytical pass -- state explicitly that you are adopting an independent reviewer perspective and have not seen the prior analysis.

Codex CLI calls require the `codex exec` binary. If unavailable, all three phases run with Claude subagent only, tagged `[single-model]`. Never skip the analysis -- just run it single-model.

The filesystem boundary instruction must be prepended to every prompt sent to Codex to prevent it from reading and following skill definition files in the repo.

See `harness-compat.md`: Subagents, External CLIs (Codex), Plan File Editing.
