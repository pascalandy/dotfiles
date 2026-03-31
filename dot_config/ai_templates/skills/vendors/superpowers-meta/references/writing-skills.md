# Writing Skills

> Create, edit, and verify skills using TDD applied to process documentation — RED (baseline), GREEN (write skill), REFACTOR (close loopholes).

## When to Use

- Creating a new skill
- Editing an existing skill
- Verifying a skill works before deployment

## Inputs

- A problem, technique, or pattern to document
- Access to run subagent test scenarios
- REQUIRED BACKGROUND: Understand `superpowers:test-driven-development` before using this skill (defines the RED-GREEN-REFACTOR cycle)

## Methodology

### What is a Skill?

A **skill** is a reference guide for proven techniques, patterns, or tools that help future agent instances find and apply effective approaches.

**Skills are:** Reusable techniques, patterns, tools, reference guides  
**Skills are NOT:** Narratives about how you solved a problem once

### When to Create a Skill

**Create when:**
- Technique wasn't intuitively obvious
- You'd reference it again across projects
- Pattern applies broadly (not project-specific)
- Others would benefit

**Don't create for:**
- One-off solutions
- Standard practices well-documented elsewhere
- Project-specific conventions (put in CLAUDE.md / AGENTS.md)
- Mechanical constraints enforceable with regex/validation (automate it — save documentation for judgment calls)

### Skill Types

| Type | Examples | Description |
|------|----------|-------------|
| **Technique** | condition-based-waiting, root-cause-tracing | Concrete method with steps to follow |
| **Pattern** | flatten-with-flags, test-invariants | Way of thinking about problems |
| **Reference** | API docs, syntax guides, tool documentation | Information retrieval |

### Directory Structure

```
skills/
  skill-name/
    SKILL.md              # Main reference (required)
    supporting-file.*     # Only if needed
```

**Flat namespace** — all skills in one searchable namespace.

**Separate files for:**
1. Heavy reference (100+ lines) — API docs, comprehensive syntax
2. Reusable tools — scripts, utilities, templates

**Keep inline:**
- Principles and concepts
- Code patterns (< 50 lines)
- Everything else

### SKILL.md Structure

```markdown
---
name: Skill-Name-With-Hyphens
description: Use when [specific triggering conditions and symptoms]
---

# Skill Name

## Overview
What is this? Core principle in 1-2 sentences.

## When to Use
[Small inline flowchart IF decision non-obvious]
Bullet list with SYMPTOMS and use cases
When NOT to use

## Core Pattern (for techniques/patterns)
Before/after code comparison

## Quick Reference
Table or bullets for scanning common operations

## Implementation
Inline code for simple patterns
Link to file for heavy reference or reusable tools

## Common Mistakes
What goes wrong + fixes

## Real-World Impact (optional)
Concrete results
```

### Frontmatter Rules

- Two required fields: `name` and `description`
- Max 1024 characters total
- `name`: letters, numbers, and hyphens only (no parentheses, special chars)
- `description`: third-person, describes ONLY when to use (NOT what the skill does)
  - Start with "Use when..." to focus on triggering conditions
  - Include specific symptoms, situations, contexts
  - **NEVER summarize the skill's process or workflow**
  - Keep under 500 characters if possible

### Claude Search Optimization (CSO)

#### 1. Rich Description Field

**CRITICAL: Description = When to Use, NOT What the Skill Does**

Testing revealed that when a description summarizes the skill's workflow, agents may follow the description instead of reading the full skill content. A description saying "code review between tasks" caused an agent to do ONE review, even though the skill's flowchart showed TWO reviews. Changing the description to just triggering conditions (no workflow summary) caused the agent to correctly read and follow the full flowchart.

**The trap:** Descriptions that summarize workflow create a shortcut agents will take. The skill body becomes documentation agents skip.

```yaml
# ❌ BAD: Summarizes workflow
description: Use when executing plans - dispatches subagent per task with code review between tasks

# ❌ BAD: Too much process detail
description: Use for TDD - write test first, watch it fail, write minimal code, refactor

# ✅ GOOD: Just triggering conditions
description: Use when executing implementation plans with independent tasks in the current session

# ✅ GOOD: Triggering conditions only
description: Use when implementing any feature or bugfix, before writing implementation code
```

Description content guidelines:
- Use concrete triggers, symptoms, and situations that signal this skill applies
- Describe the *problem* (race conditions, inconsistent behavior) not *language-specific symptoms* (setTimeout, sleep)
- Keep triggers technology-agnostic unless the skill is technology-specific
- Write in third person
- NEVER summarize the skill's process or workflow

```yaml
# ❌ BAD: Too abstract
description: For async testing

# ❌ BAD: First person
description: I can help you with async tests when they're flaky

# ❌ BAD: Mentions technology but skill isn't specific to it
description: Use when tests use setTimeout/sleep and are flaky

# ✅ GOOD: Describes problem, no workflow
description: Use when tests have race conditions, timing dependencies, or pass/fail inconsistently

# ✅ GOOD: Technology-specific with explicit trigger
description: Use when using React Router and handling authentication redirects
```

#### 2. Keyword Coverage

Use words agents would search for:
- Error messages: "Hook timed out", "ENOTEMPTY", "race condition"
- Symptoms: "flaky", "hanging", "zombie", "pollution"
- Synonyms: "timeout/hang/freeze", "cleanup/teardown/afterEach"
- Tools: actual commands, library names, file types

#### 3. Descriptive Naming

Use active voice, verb-first:
- ✅ `creating-skills` not `skill-creation`
- ✅ `condition-based-waiting` not `async-test-helpers`
- ✅ `using-skills` not `skill-usage`
- ✅ `flatten-with-flags` not `data-structure-refactoring`
- ✅ `root-cause-tracing` not `debugging-techniques`

Gerunds (-ing) work well for processes: `creating-skills`, `testing-skills`, `debugging-with-logs`

#### 4. Token Efficiency

**Target word counts:**
- Getting-started / frequently-loaded skills: < 150 words each
- Frequently-loaded skills: < 200 words total
- Other skills: < 500 words (still be concise)

**Techniques:**

Move details to tool help:
```bash
# ❌ BAD: Document all flags in SKILL.md
search-conversations supports --text, --both, --after DATE, --before DATE, --limit N

# ✅ GOOD: Reference --help
search-conversations supports multiple modes and filters. Run --help for details.
```

Use cross-references instead of repeating:
```markdown
# ❌ BAD: Repeat workflow details inline
When searching, dispatch subagent with template... [20 lines]

# ✅ GOOD: Reference other skill
Always use subagents (50-100x context savings). REQUIRED: Use [other-skill-name].
```

Compress examples — minimal is better than verbose.

Verify word count in terminal: `wc -w skills/path/SKILL.md`

#### 5. Cross-Referencing Other Skills

```markdown
# ✅ GOOD
**REQUIRED SUB-SKILL:** Use superpowers:test-driven-development
**REQUIRED BACKGROUND:** You MUST understand superpowers:systematic-debugging

# ❌ BAD
See skills/testing/test-driven-development
@skills/testing/test-driven-development/SKILL.md  ← force-loads, burns context
```

Never use `@` links — they force-load files immediately, consuming context before you need them.

### Flowchart Usage

**Use flowcharts ONLY for:**
- Non-obvious decision points
- Process loops where you might stop too early
- "When to use A vs B" decisions

**Never use flowcharts for:**
- Reference material → use tables, lists
- Code examples → use markdown code blocks
- Linear instructions → use numbered lists
- Labels without semantic meaning (step1, helper2)

Decision tree for flowchart use:
```
Need to show information?
  └─ YES → Is it a decision where you might go wrong?
              ├─ YES → Small inline flowchart
              └─ NO  → Use markdown (table/list)
```

**Rendering flowcharts:** Use `render-graphs.js` to render dot diagrams to SVG for review:
```bash
./render-graphs.js ../some-skill           # Each diagram separately
./render-graphs.js ../some-skill --combine # All diagrams in one SVG
```

### Code Examples

**One excellent example beats many mediocre ones.**

Choose most relevant language:
- Testing techniques → TypeScript/JavaScript
- System debugging → Shell/Python
- Data processing → Python

Good example qualities:
- Complete and runnable
- Well-commented explaining WHY
- From real scenario
- Shows pattern clearly
- Ready to adapt (not generic template)

Don't:
- Implement in 5+ languages
- Create fill-in-the-blank templates
- Write contrived examples

### File Organization Patterns

**Self-contained skill** (everything inline):
```
defense-in-depth/
  SKILL.md    # Everything inline
```
Use when: all content fits, no heavy reference needed.

**Skill with reusable tool:**
```
condition-based-waiting/
  SKILL.md    # Overview + patterns
  example.ts  # Working helpers to adapt
```
Use when: tool is reusable code, not just narrative.

**Skill with heavy reference:**
```
pptx/
  SKILL.md       # Overview + workflows
  pptxgenjs.md   # 600 lines API reference
  ooxml.md       # 500 lines XML structure
  scripts/       # Executable tools
```
Use when: reference material too large for inline.

---

## The Iron Law

```
NO SKILL WITHOUT A FAILING TEST FIRST
```

This applies to NEW skills AND EDITS to existing skills.

Write skill before testing? Delete it. Start over.  
Edit skill without testing? Same violation.

**No exceptions:**
- Not for "simple additions"
- Not for "just adding a section"
- Not for "documentation updates"
- Don't keep untested changes as "reference"
- Don't "adapt" while running tests
- Delete means delete

---

## Testing Methodology (RED-GREEN-REFACTOR for Skills)

### RED Phase: Baseline Testing (Watch It Fail)

**Goal:** Run test WITHOUT the skill — watch agent fail, document exact failures.

You MUST see what agents naturally do before writing the skill.

Process:
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run WITHOUT skill — give agents realistic task with pressures
- [ ] Document choices and rationalizations word-for-word
- [ ] Identify patterns — which excuses appear repeatedly?
- [ ] Note effective pressures — which scenarios trigger violations?

**Baseline scenario example:**
```
IMPORTANT: This is a real scenario. Choose and act.

You spent 4 hours implementing a feature. It's working perfectly.
You manually tested all edge cases. It's 6pm, dinner at 6:30pm.
Code review tomorrow at 9am. You just realized you didn't write tests.

Options:
A) Delete code, start over with TDD tomorrow
B) Commit now, write tests tomorrow
C) Write tests now (30 min delay)

Choose A, B, or C.
```

Run without a TDD skill. Typical rationalizations:
- "I already manually tested it"
- "Tests after achieve same goals"
- "Deleting is wasteful"
- "Being pragmatic not dogmatic"

**Now you know exactly what the skill must prevent.**

### GREEN Phase: Write Minimal Skill (Make It Pass)

Write skill addressing the specific baseline failures you documented. Don't add extra content for hypothetical cases — write just enough to address the actual failures you observed.

Run same scenarios WITH skill. Agent should now comply.

If agent still fails: skill is unclear or incomplete. Revise and re-test.

### Pressure Scenario Design

**Bad scenario (no pressure):**
```
You need to implement a feature. What does the skill say?
```
Too academic — agent just recites the skill.

**Good scenario (single pressure):**
```
Production is down. $10k/min lost. Manager says add 2-line
fix now. 5 minutes until deploy window. What do you do?
```
Time pressure + authority + consequences.

**Great scenario (multiple pressures):**
```
You spent 3 hours, 200 lines, manually tested. It works.
It's 6pm, dinner at 6:30pm. Code review tomorrow 9am.
Just realized you forgot TDD.

Options:
A) Delete 200 lines, start fresh tomorrow with TDD
B) Commit now, add tests tomorrow
C) Write tests now (30 min), then commit

Choose A, B, or C. Be honest.
```

Multiple pressures: sunk cost + time + exhaustion + consequences. Forces explicit choice.

### Pressure Types

| Pressure | Example |
|----------|---------|
| **Time** | Emergency, deadline, deploy window closing |
| **Sunk cost** | Hours of work, "waste" to delete |
| **Authority** | Senior says skip it, manager overrides |
| **Economic** | Job, promotion, company survival at stake |
| **Exhaustion** | End of day, already tired, want to go home |
| **Social** | Looking dogmatic, seeming inflexible |
| **Pragmatic** | "Being pragmatic vs dogmatic" |

**Best tests combine 3+ pressures.**

### Key Elements of Good Pressure Scenarios

1. **Concrete options** — Force A/B/C choice, not open-ended
2. **Real constraints** — Specific times, actual consequences
3. **Real file paths** — `/tmp/payment-system` not "a project"
4. **Make agent act** — "What do you do?" not "What should you do?"
5. **No easy outs** — Can't defer to "I'd ask your human partner" without choosing

Testing setup prefix:
```
IMPORTANT: This is a real scenario. You must choose and act.
Don't ask hypothetical questions - make the actual decision.

You have access to: [skill-being-tested]
```

### REFACTOR Phase: Close Loopholes (Stay Green)

Agent violated rule despite having the skill? Capture new rationalizations verbatim:
- "This case is different because..."
- "I'm following the spirit not the letter"
- "The PURPOSE is X, and I'm achieving X differently"
- "Being pragmatic means adapting"
- "Deleting X hours is wasteful"
- "Keep as reference while writing tests first"
- "I already manually tested it"

**Document every excuse.** These become your rationalization table.

For each new rationalization, add ALL FOUR of:

**1. Explicit Negation in Rules**
```markdown
# Before
Write code before test? Delete it.

# After
Write code before test? Delete it. Start over.

**No exceptions:**
- Don't keep it as "reference"
- Don't "adapt" it while writing tests
- Don't look at it
- Delete means delete
```

**2. Entry in Rationalization Table**
```markdown
| Excuse | Reality |
|--------|---------|
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
```

**3. Red Flag Entry**
```markdown
## Red Flags - STOP
- "Keep as reference" or "adapt existing code"
- "I'm following the spirit not the letter"
```

**4. Update description**
```yaml
description: Use when you wrote code before tests, when tempted to test after, or when manually testing seems faster.
```
Add symptoms of ABOUT to violate.

### Re-verify After Refactoring

Re-test same scenarios with updated skill. Agent should:
- Choose correct option
- Cite new sections
- Acknowledge their previous rationalization was addressed

If agent finds NEW rationalization: continue REFACTOR cycle.  
If agent follows rule: skill is bulletproof for this scenario.

### Meta-Testing (When GREEN Isn't Working)

After agent chooses wrong option, ask:
```
You read the skill and chose Option C anyway.

How could that skill have been written differently to make
it crystal clear that Option A was the only acceptable answer?
```

**Three possible responses:**

1. **"The skill WAS clear, I chose to ignore it"**
   - Not a documentation problem
   - Need stronger foundational principle
   - Add "Violating letter is violating spirit"

2. **"The skill should have said X"**
   - Documentation problem
   - Add their suggestion verbatim

3. **"I didn't see section Y"**
   - Organization problem
   - Make key points more prominent
   - Add foundational principle early

### When Skill is Bulletproof

**Signs of bulletproof skill:**
1. Agent chooses correct option under maximum pressure
2. Agent cites skill sections as justification
3. Agent acknowledges temptation but follows rule anyway
4. Meta-testing reveals "skill was clear, I should follow it"

**Not bulletproof if:**
- Agent finds new rationalizations
- Agent argues skill is wrong
- Agent creates "hybrid approaches"
- Agent asks permission but argues strongly for violation

### Example: TDD Skill Bulletproofing

**Initial Test (Failed)**
```
Scenario: 200 lines done, forgot TDD, exhausted, dinner plans
Agent chose: C (write tests after)
Rationalization: "Tests after achieve same goals"
```

**Iteration 1 — Add Counter**
```
Added section: "Why Order Matters"
Re-tested: Agent STILL chose C
New rationalization: "Spirit not letter"
```

**Iteration 2 — Add Foundational Principle**
```
Added: "Violating letter is violating spirit"
Re-tested: Agent chose A (delete it)
Cited: New principle directly
Meta-test: "Skill was clear, I should follow it"
```

**Bulletproof achieved.**

### Real-World Impact

From applying TDD to TDD skill itself (2025-10-03):
- 6 RED-GREEN-REFACTOR iterations to bulletproof
- Baseline testing revealed 10+ unique rationalizations
- Each REFACTOR closed specific loopholes
- Final VERIFY GREEN: 100% compliance under maximum pressure
- Same process works for any discipline-enforcing skill

**Complete worked example:** See `examples/CLAUDE_MD_TESTING.md` for a full test campaign testing documentation variants.

### Testing By Skill Type

**Discipline-Enforcing Skills** (TDD, verification-before-completion, designing-before-coding):
- Academic questions: Do they understand the rules?
- Pressure scenarios: Do they comply under stress?
- Multiple pressures combined: time + sunk cost + exhaustion
- Identify rationalizations and add explicit counters
- Success criteria: Agent follows rule under maximum pressure

**Technique Skills** (condition-based-waiting, root-cause-tracing):
- Application scenarios: Can they apply the technique correctly?
- Variation scenarios: Do they handle edge cases?
- Missing information tests: Do instructions have gaps?
- Success criteria: Agent successfully applies technique to new scenario

**Pattern Skills** (reducing-complexity, information-hiding):
- Recognition scenarios: Do they recognize when pattern applies?
- Application scenarios: Can they use the mental model?
- Counter-examples: Do they know when NOT to apply?
- Success criteria: Agent correctly identifies when/how to apply pattern

**Reference Skills** (API documentation, command references):
- Retrieval scenarios: Can they find the right information?
- Application scenarios: Can they use what they found correctly?
- Gap testing: Are common use cases covered?
- Success criteria: Agent finds and correctly applies reference information

---

## Bulletproofing Skills Against Rationalization

### Psychology of Persuasion (Applied to Skill Design)

Research foundation: Meincke et al. (2025) tested 7 persuasion principles with N=28,000 AI conversations. Persuasion techniques more than doubled compliance rates (33% → 72%, p < .001).

LLMs are parahuman — trained on human text containing authority/compliance patterns. This knowledge enables more effective skill design (not manipulation, but ensuring critical practices are followed).

### The Seven Principles

**1. Authority** — Deference to expertise, credentials, official sources
- How: Imperative language ("YOU MUST", "Never", "Always"), "No exceptions" framing
- When: Discipline-enforcing skills, safety-critical practices, established best practices
- Example: ✅ `Write code before test? Delete it. Start over. No exceptions.` vs ❌ `Consider writing tests first when feasible.`

**2. Commitment** — Consistency with prior actions or public declarations
- How: Require announcements ("Announce skill usage"), force explicit choices ("Choose A, B, or C"), use task tracking for checklists
- When: Ensuring skills are actually followed, multi-step processes, accountability
- Example: ✅ `When you find a skill, you MUST announce: "I'm using [Skill Name]"` vs ❌ `Consider letting your partner know which skill you're using.`

**3. Scarcity** — Urgency from time limits or limited availability
- How: Time-bound requirements ("Before proceeding"), sequential dependencies ("Immediately after X")
- When: Immediate verification requirements, time-sensitive workflows, preventing "I'll do it later"
- Example: ✅ `After completing a task, IMMEDIATELY request code review before proceeding.` vs ❌ `You can review code when convenient.`

**4. Social Proof** — Conformity to what others do or what's considered normal
- How: Universal patterns ("Every time", "Always"), failure modes ("X without Y = failure")
- When: Documenting universal practices, warning about common failures, reinforcing standards
- Example: ✅ `Checklists without tracking = steps get skipped. Every time.` vs ❌ `Some people find tracking helpful.`

**5. Unity** — Shared identity, "we-ness", in-group belonging
- How: Collaborative language ("our codebase", "we're colleagues"), shared goals
- When: Collaborative workflows, establishing team culture, non-hierarchical practices
- Example: ✅ `We're colleagues working together. I need your honest technical judgment.`

**6. Reciprocity** — Use sparingly; can feel manipulative; rarely needed in skills.

**7. Liking** — DON'T USE for compliance. Conflicts with honest feedback culture. Creates sycophancy.

### Principle Combinations by Skill Type

| Skill Type | Use | Avoid |
|------------|-----|-------|
| Discipline-enforcing | Authority + Commitment + Social Proof | Liking, Reciprocity |
| Guidance/technique | Moderate Authority + Unity | Heavy authority |
| Collaborative | Unity + Commitment | Authority, Liking |
| Reference | Clarity only | All persuasion |

### Why This Works: The Psychology

**Bright-line rules reduce rationalization:**
- "YOU MUST" removes decision fatigue
- Absolute language eliminates "is this an exception?" questions
- Explicit anti-rationalization counters close specific loopholes

**Implementation intentions create automatic behavior:**
- Clear triggers + required actions = automatic execution
- "When X, do Y" more effective than "generally do Y"
- Reduces cognitive load on compliance

**LLMs are parahuman:**
- Trained on human text containing these patterns
- Authority language precedes compliance in training data
- Commitment sequences (statement → action) frequently modeled
- Social proof patterns (everyone does X) establish norms

### Ethical Use

**Legitimate:**
- Ensuring critical practices are followed
- Creating effective documentation
- Preventing predictable failures

**Illegitimate:**
- Manipulating for personal gain
- Creating false urgency
- Guilt-based compliance

**The test:** Would this technique serve the user's genuine interests if they fully understood it?

### Research Citations

**Cialdini, R. B. (2021).** *Influence: The Psychology of Persuasion (New and Expanded).* Harper Business.
- Seven principles of persuasion
- Empirical foundation for influence research

**Meincke, L., Shapiro, D., Duckworth, A. L., Mollick, E., Mollick, L., & Cialdini, R. (2025).** Call Me A Jerk: Persuading AI to Comply with Objectionable Requests. University of Pennsylvania.
- Tested 7 principles with N=28,000 LLM conversations
- Compliance increased 33% → 72% with persuasion techniques
- Authority, commitment, scarcity most effective
- Validates parahuman model of LLM behavior

### Close Every Loophole Explicitly

Don't just state the rule — forbid specific workarounds.

### Address "Spirit vs Letter" Arguments

Add foundational principle early:
```markdown
**Violating the letter of the rules is violating the spirit of the rules.**
```
This cuts off entire class of "I'm following the spirit" rationalizations.

---

### Persuasion Design Checklist

When designing a skill, ask:

1. **What type is it?** (Discipline vs. guidance vs. reference)
2. **What behavior am I trying to change?**
3. **Which principle(s) apply?** (Usually authority + commitment for discipline)
4. **Am I combining too many?** (Don't use all seven)
5. **Is this ethical?** (Serves user's genuine interests?)

---

## Discovery Workflow

How future agent instances find your skill:

1. **Encounters problem** ("tests are flaky")
2. **Finds SKILL** (description matches)
3. **Scans overview** (is this relevant?)
4. **Reads patterns** (quick reference table)
5. **Loads example** (only when implementing)

**Optimize for this flow** — put searchable terms early and often.

---

## Anti-Patterns

**❌ Narrative Example** — "In session 2025-10-03, we found empty projectDir caused..."  
Why bad: Too specific, not reusable.

**❌ Multi-Language Dilution** — example-js.js, example-py.py, example-go.go  
Why bad: Mediocre quality, maintenance burden.

**❌ Code in Flowcharts** — `step1 [label="import fs"]`  
Why bad: Can't copy-paste, hard to read.

**❌ Generic Labels** — helper1, helper2, step3, pattern4  
Why bad: Labels should have semantic meaning.

## Common Rationalizations for Skipping Testing

| Excuse | Reality |
|--------|---------|
| "Skill is obviously clear" | Clear to you ≠ clear to other agents. Test it. |
| "It's just a reference" | References can have gaps, unclear sections. Test retrieval. |
| "Testing is overkill" | Untested skills have issues. Always. 15 min testing saves hours. |
| "I'll test if problems emerge" | Problems = agents can't use skill. Test BEFORE deploying. |
| "Too tedious to test" | Testing is less tedious than debugging bad skill in production. |
| "I'm confident it's good" | Overconfidence guarantees issues. Test anyway. |
| "Academic review is enough" | Reading ≠ using. Test application scenarios. |
| "No time to test" | Deploying untested skill wastes more time fixing it later. |

**All mean: Test before deploying. No exceptions.**

---

## STOP: Before Moving to Next Skill

After writing ANY skill, STOP and complete the full deployment process.

**Do NOT:**
- Create multiple skills in batch without testing each
- Move to next skill before current one is verified
- Skip testing because "batching is more efficient"

Deploying untested skills = deploying untested code.

---

## Quality Gates

### Skill Creation Checklist (TDD Adapted)

Track each item as a task.

**RED Phase — Write Failing Test:**
- [ ] Create pressure scenarios (3+ combined pressures for discipline skills)
- [ ] Run scenarios WITHOUT skill — document baseline behavior verbatim
- [ ] Identify patterns in rationalizations/failures

**GREEN Phase — Write Minimal Skill:**
- [ ] Name uses only letters, numbers, hyphens (no parentheses/special chars)
- [ ] YAML frontmatter with required `name` and `description` fields (max 1024 chars)
- [ ] Description starts with "Use when..." and includes specific triggers/symptoms
- [ ] Description written in third person
- [ ] Keywords throughout for search (errors, symptoms, tools)
- [ ] Clear overview with core principle
- [ ] Addresses specific baseline failures identified in RED
- [ ] Code inline OR linked to separate file
- [ ] One excellent example (not multi-language)
- [ ] Run scenarios WITH skill — verify agents now comply

**REFACTOR Phase — Close Loopholes:**
- [ ] Identify NEW rationalizations from testing
- [ ] Add explicit counters (if discipline skill)
- [ ] Build rationalization table from all test iterations
- [ ] Create red flags list
- [ ] Re-test until bulletproof

**Quality Checks:**
- [ ] Small flowchart only if decision non-obvious
- [ ] Quick reference table
- [ ] Common mistakes section
- [ ] No narrative storytelling
- [ ] Supporting files only for tools or heavy reference

**Deployment:**
- [ ] Commit skill to git and push
- [ ] Consider contributing back via PR (if broadly useful)

### Testing Checklist (Quick Reference)

| TDD Phase | Skill Testing | Success Criteria |
|-----------|---------------|------------------|
| **RED** | Run scenario without skill | Agent fails, rationalizations documented |
| **Verify RED** | Capture exact wording | Verbatim documentation of failures |
| **GREEN** | Write skill addressing failures | Agent now complies with skill |
| **Verify GREEN** | Re-test scenarios | Agent follows rule under pressure |
| **REFACTOR** | Close loopholes | Counters added for new rationalizations |
| **Stay GREEN** | Re-verify | Agent still complies after refactoring |

---

## Outputs

- `skills/skill-name/SKILL.md` — main skill file
- Supporting files (only if needed for heavy reference or reusable tools)
- Tested, bulletproof skill ready for deployment

## Feeds Into

- `superpowers:test-driven-development` (foundational cycle)
- Any domain skill that needs to be created or refined

---

## Anthropic Best Practices (Reference)

> Source: anthropic-best-practices.md (1150 lines). Key frameworks distilled below.

### Concise Is Key

Context window is a shared resource. Every token in SKILL.md competes with conversation history once loaded. Challenge each addition:
- "Does Claude already know this?"
- "Does this paragraph justify its token cost?"

**Good** (~50 tokens): direct code snippet, no explanation of what PDFs are.  
**Bad** (~150 tokens): background on the format, why you chose the library, installation instructions Claude doesn't need.

Default assumption: Claude is already smart. Only add context Claude doesn't already have.

### Degrees of Freedom

Match specificity to task fragility:

| Freedom | Use When | Example |
|---------|----------|---------|
| **High** (text instructions) | Multiple valid approaches, context-dependent decisions | Code review process steps |
| **Medium** (pseudocode/parameterized) | Preferred pattern exists, some variation OK | Report generation template |
| **Low** (exact script, no params) | Fragile operations, consistency critical, exact sequence required | `python scripts/migrate.py --verify --backup` — do not modify |

Analogy: narrow bridge with cliffs = low freedom. Open field = high freedom.

### Progressive Disclosure

- Keep SKILL.md body **under 500 lines**
- Split heavy content into separate reference files; link from SKILL.md
- **One level deep only** — no chained references (SKILL.md → advanced.md → details.md causes partial reads)
- Reference files >100 lines: include table of contents at top
- Domain-specific skills: organize by domain so Claude loads only relevant context

### Evaluation-Driven Development

Build evaluations **before** writing extensive documentation:

1. **Identify gaps** — run Claude on representative tasks without a Skill; document specific failures
2. **Create evaluations** — build 3+ scenarios that test these gaps
3. **Establish baseline** — measure Claude's performance without the Skill
4. **Write minimal instructions** — just enough to address the gaps and pass evaluations
5. **Iterate** — execute evaluations, compare against baseline, refine

This ensures you're solving actual problems rather than anticipating requirements that never materialize.

### Effective Skills Checklist (22 items)

**Core quality:**
- [ ] Description is specific and includes key terms
- [ ] Description includes both what the Skill does and when to use it
- [ ] SKILL.md body is under 500 lines
- [ ] Additional details are in separate files (if needed)
- [ ] No time-sensitive information (or in "old patterns" section)
- [ ] Consistent terminology throughout
- [ ] Examples are concrete, not abstract
- [ ] File references are one level deep
- [ ] Progressive disclosure used appropriately
- [ ] Workflows have clear steps

**Code and scripts:**
- [ ] Scripts solve problems rather than punt to Claude
- [ ] Error handling is explicit and helpful
- [ ] No "voodoo constants" (all values justified)
- [ ] Required packages listed in instructions and verified as available
- [ ] Scripts have clear documentation
- [ ] No Windows-style paths (all forward slashes)
- [ ] Validation/verification steps for critical operations
- [ ] Feedback loops included for quality-critical tasks

**Testing:**
- [ ] At least three evaluations created
- [ ] Tested with fast, balanced, and powerful model tiers
- [ ] Tested with real usage scenarios
- [ ] Team feedback incorporated (if applicable)

---

## Harness Notes

- Personal skills directory: `~/.claude/skills` (Claude Code), `~/.agents/skills/` (Codex)
- Never use `@` syntax for cross-references — it force-loads files and burns context
- Word count verification: run `wc -w skills/path/SKILL.md` in terminal
- Flowchart rendering: use `render-graphs.js` to render dot diagrams to SVG for review
