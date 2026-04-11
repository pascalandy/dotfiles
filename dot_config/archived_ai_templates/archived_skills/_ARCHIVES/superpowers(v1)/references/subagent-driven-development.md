# Subagent-Driven Development

> Execute an implementation plan by dispatching a fresh subagent per task with two-stage review (spec compliance, then code quality) after each task — all within a single session.

## When to Use

Decision tree:

```
Have implementation plan?
├── NO  → Manual execution or brainstorm first
└── YES → Tasks mostly independent?
          ├── NO (tightly coupled) → Manual execution or brainstorm first
          └── YES → Stay in this session?
                    ├── NO (parallel session) → executing-plans skill
                    └── YES → subagent-driven-development  ✓
```

**vs. executing-plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task: spec compliance first, then code quality
- Faster iteration (no human-in-loop between tasks)

## Inputs

- A written implementation plan with discrete, mostly-independent tasks
- An isolated git worktree (using-git-worktrees REQUIRED before starting)
- The full text of the plan extracted upfront (subagents never read the plan file)

## Methodology

### Phase 0: Setup

1. Set up an isolated workspace using the using-git-worktrees skill before any implementation begins. Never start on main/master without explicit user consent.
2. Read the plan file once.
3. Extract ALL tasks with their full text and context.
4. Track all tasks (e.g., in a todo list) so progress is visible.

### Phase 1: Per-Task Loop

Repeat for each task:

#### 1a. Dispatch Implementer Subagent

**Model selection:**
| Task type | Model |
|-----------|-------|
| Mechanical (isolated functions, clear spec, 1–2 files) | Fast/cheap model |
| Integration (multi-file, pattern matching, debugging) | Standard model |
| Architecture, design, review | Most capable model |

**Signals for complexity:**
- Touches 1–2 files with complete spec → cheap model
- Touches multiple files with integration concerns → standard model
- Requires design judgment or broad codebase understanding → most capable model

**Full implementer subagent prompt template:**

```
You are implementing Task N: [task name]

## Task Description

[FULL TEXT of task from plan - paste it here, don't make subagent read file]

## Context

[Scene-setting: where this fits, dependencies, architectural context]

## Before You Begin

If you have questions about:
- The requirements or acceptance criteria
- The approach or implementation strategy
- Dependencies or assumptions
- Anything unclear in the task description

**Ask them now.** Raise any concerns before starting work.

## Your Job

Once you're clear on requirements:
1. Implement exactly what the task specifies
2. Write tests (following TDD if task says to)
3. Verify implementation works
4. Commit your work
5. Self-review (see below)
6. Report back

Work from: [directory]

**While you work:** If you encounter something unexpected or unclear, **ask questions**.
It's always OK to pause and clarify. Don't guess or make assumptions.

## Code Organization

You reason best about code you can hold in context at once, and your edits are more
reliable when files are focused. Keep this in mind:
- Follow the file structure defined in the plan
- Each file should have one clear responsibility with a well-defined interface
- If a file you're creating is growing beyond the plan's intent, stop and report
  it as DONE_WITH_CONCERNS — don't split files on your own without plan guidance
- If an existing file you're modifying is already large or tangled, work carefully
  and note it as a concern in your report
- In existing codebases, follow established patterns. Improve code you're touching
  the way a good developer would, but don't restructure things outside your task.

## When You're in Over Your Head

It is always OK to stop and say "this is too hard for me." Bad work is worse than
no work. You will not be penalized for escalating.

**STOP and escalate when:**
- The task requires architectural decisions with multiple valid approaches
- You need to understand code beyond what was provided and can't find clarity
- You feel uncertain about whether your approach is correct
- The task involves restructuring existing code in ways the plan didn't anticipate
- You've been reading file after file trying to understand the system without progress

**How to escalate:** Report back with status BLOCKED or NEEDS_CONTEXT. Describe
specifically what you're stuck on, what you've tried, and what kind of help you need.
The controller can provide more context, re-dispatch with a more capable model,
or break the task into smaller pieces.

## Before Reporting Back: Self-Review

Review your work with fresh eyes. Ask yourself:

**Completeness:**
- Did I fully implement everything in the spec?
- Did I miss any requirements?
- Are there edge cases I didn't handle?

**Quality:**
- Is this my best work?
- Are names clear and accurate (match what things do, not how they work)?
- Is the code clean and maintainable?

**Discipline:**
- Did I avoid overbuilding (YAGNI)?
- Did I only build what was requested?
- Did I follow existing patterns in the codebase?

**Testing:**
- Do tests actually verify behavior (not just mock behavior)?
- Did I follow TDD if required?
- Are tests comprehensive?

If you find issues during self-review, fix them now before reporting.

## Report Format

When done, report:
- **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
- What you implemented (or what you attempted, if blocked)
- What you tested and test results
- Files changed
- Self-review findings (if any)
- Any issues or concerns

Use DONE_WITH_CONCERNS if you completed the work but have doubts about correctness.
Use BLOCKED if you cannot complete the task. Use NEEDS_CONTEXT if you need
information that wasn't provided. Never silently produce work you're unsure about.
```

#### 1b. Handle Implementer Status

| Status | Action |
|--------|--------|
| **DONE** | Proceed to spec compliance review |
| **DONE_WITH_CONCERNS** | Read concerns before proceeding. If about correctness/scope → address first. If observational (e.g., "file is getting large") → note and proceed to review. |
| **NEEDS_CONTEXT** | Provide missing information and re-dispatch |
| **BLOCKED** | See escalation logic below |

**BLOCKED escalation logic:**
1. Context problem → provide more context and re-dispatch with same model
2. Task requires more reasoning → re-dispatch with more capable model
3. Task too large → break into smaller pieces
4. Plan itself is wrong → escalate to the human

**Never** ignore an escalation or force the same model to retry without changes.

#### 1c. Dispatch Spec Compliance Reviewer Subagent

Only dispatch AFTER implementer status is DONE or DONE_WITH_CONCERNS (concerns resolved).

**Full spec compliance reviewer prompt template:**

```
You are reviewing whether an implementation matches its specification.

## What Was Requested

[FULL TEXT of task requirements]

## What Implementer Claims They Built

[From implementer's report]

## CRITICAL: Do Not Trust the Report

The implementer finished suspiciously quickly. Their report may be incomplete,
inaccurate, or optimistic. You MUST verify everything independently.

**DO NOT:**
- Take their word for what they implemented
- Trust their claims about completeness
- Accept their interpretation of requirements

**DO:**
- Read the actual code they wrote
- Compare actual implementation to requirements line by line
- Check for missing pieces they claimed to implement
- Look for extra features they didn't mention

## Your Job

Read the implementation code and verify:

**Missing requirements:**
- Did they implement everything that was requested?
- Are there requirements they skipped or missed?
- Did they claim something works but didn't actually implement it?

**Extra/unneeded work:**
- Did they build things that weren't requested?
- Did they over-engineer or add unnecessary features?
- Did they add "nice to haves" that weren't in spec?

**Misunderstandings:**
- Did they interpret requirements differently than intended?
- Did they solve the wrong problem?
- Did they implement the right feature but wrong way?

**Verify by reading code, not by trusting report.**

Report:
- ✅ Spec compliant (if everything matches after code inspection)
- ❌ Issues found: [list specifically what's missing or extra, with file:line references]
```

**If spec compliance fails:**
- Have the implementer (same subagent) fix the gaps
- Re-dispatch spec reviewer
- Repeat until ✅

**Never proceed to code quality review while spec compliance has open issues.**

#### 1d. Dispatch Code Quality Reviewer Subagent

Only dispatch AFTER spec compliance is ✅.

Use the code-reviewer template from the requesting-code-review skill with these fields:

```
WHAT_WAS_IMPLEMENTED: [from implementer's report]
PLAN_OR_REQUIREMENTS: Task N from [plan-file]
BASE_SHA: [commit before task]
HEAD_SHA: [current commit]
DESCRIPTION: [task summary]
```

**In addition to standard code quality concerns, the reviewer must check:**
- Does each file have one clear responsibility with a well-defined interface?
- Are units decomposed so they can be understood and tested independently?
- Is the implementation following the file structure from the plan?
- Did this implementation create new files that are already large, or significantly grow existing files? (Do not flag pre-existing file sizes — focus on what this change contributed.)

**Code quality reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment.

**If code quality review fails:**
- Have the implementer fix the issues
- Re-dispatch code quality reviewer
- Repeat until approved

#### 1e. Mark Task Complete

Only after BOTH reviews pass. Mark task done in your tracking list and proceed to next task.

### Phase 2: Final Review

After all tasks complete:
1. Delegate a final code-reviewer subagent covering the entire implementation (all commits from start to HEAD)
2. Proceed to the finishing-a-development-branch skill

## Advantages

**vs. Manual execution:**
- Subagents follow TDD naturally with fresh context per task
- No confusion from accumulated session state
- Parallel-safe: subagents don't interfere with each other
- Subagent can ask questions before AND during work

**vs. Executing Plans (parallel session):**
- Same session — no handoff or context switch
- Continuous progress — no waiting between tasks
- Review checkpoints are automatic

**Efficiency gains:**
- No file-reading overhead: controller provides full task text upfront
- Controller curates exactly what context each subagent needs
- Subagent receives complete information before starting
- Questions are surfaced before work begins, not after

**Quality gates:**
- Implementer self-review catches issues before handoff
- Two-stage review (spec compliance → code quality) prevents over/under-building
- Review loops ensure fixes actually work
- Spec compliance review gates the code quality review

**Cost:**
- More subagent invocations (implementer + 2 reviewers per task)
- Controller does more prep work (extracting all tasks upfront)
- Review loops add iterations
- Tradeoff: catches issues early, which is cheaper than debugging later

## Worked Example

```
[Read plan file once; extract all tasks; create task tracking list]

Task 1: Hook installation script

[Dispatch implementer subagent with full task text + context]

Implementer: "Before I begin — should the hook be installed at user or system level?"

Controller: "User level (~/.config/superpowers/hooks/)"

Implementer: [Implements, tests, self-reviews, commits]
  Status: DONE
  - Implemented install-hook command
  - Added tests: 5/5 passing
  - Self-review: Found I missed --force flag; added it

[Dispatch spec compliance reviewer]
Spec reviewer: ✅ Spec compliant — all requirements met, nothing extra

[Capture BASE_SHA and HEAD_SHA; dispatch code quality reviewer]
Code reviewer:
  Strengths: Good test coverage, clean separation
  Issues: None
  Assessment: Ready to proceed

[Mark Task 1 complete]

---

Task 2: Recovery modes

[Dispatch implementer subagent]

Implementer: [No questions; implements, tests, commits]
  Status: DONE
  - Added verify/repair modes
  - 8/8 tests passing

[Dispatch spec compliance reviewer]
Spec reviewer: ❌ Issues:
  - Missing: Progress reporting (spec says "report every 100 items")
  - Extra: Added --json flag (not requested)

[Implementer fixes]
Implementer: Removed --json flag; added progress reporting

[Spec reviewer re-reviews]
Spec reviewer: ✅ Spec compliant

[Dispatch code quality reviewer]
Code reviewer:
  Issues (Important): Magic number (100) — extract as constant
  
[Implementer fixes]
Implementer: Extracted PROGRESS_INTERVAL constant

[Code reviewer re-reviews]
Code reviewer: ✅ Approved

[Mark Task 2 complete]

...

[After all tasks: dispatch final code reviewer covering entire implementation]
Final reviewer: All requirements met, ready to merge
```

## Quality Gates

**Per-task gates (in order):**
1. Implementer self-review complete
2. Spec compliance ✅ (no missing, no extra)
3. Code quality approved (no Critical or Important issues unresolved)

**Red flags — stop immediately if you observe:**
- Starting implementation on main/master without explicit user consent
- Skipping spec compliance review
- Skipping code quality review
- Starting code quality review before spec compliance is ✅
- Moving to next task while either review has open issues
- Dispatching multiple implementer subagents in parallel (causes conflicts)
- Having subagent read the plan file (provide full text instead)
- Omitting scene-setting context from subagent prompt
- Ignoring subagent questions before implementation
- Accepting "close enough" on spec compliance
- Skipping re-review after fixes
- Letting implementer self-review replace actual review
- Trying to fix manually instead of dispatching a fix subagent (causes context pollution)

## Outputs

- All plan tasks implemented, reviewed, and committed in the isolated worktree
- Final code review report
- Handoff to finishing-a-development-branch

## Feeds Into

- **requesting-code-review** — used for all code quality review subagents
- **finishing-a-development-branch** — REQUIRED after all tasks complete
- **test-driven-development** — subagents should follow TDD for each task

## Harness Notes

The controller (you) provides all context explicitly to each subagent. Subagents never inherit session history and never read the plan file directly — the controller pastes the full task text into the prompt. This preserves the controller's context for coordination and ensures each subagent gets exactly what it needs.
