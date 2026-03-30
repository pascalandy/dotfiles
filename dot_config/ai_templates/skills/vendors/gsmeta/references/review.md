# Review

> Pre-landing PR review. Analyzes the diff against the base branch for SQL safety, LLM trust boundary violations, race conditions, test gaps, and other structural issues that tests don't catch.

## When to Use

- User says "review this PR", "code review", "pre-landing review", "check my diff"
- User is about to merge or land code changes (proactively suggest)
- Run as part of the ship workflow before creating a PR

## Inputs

- Current branch with commits not yet merged to base
- The diff against the base branch (fetched fresh from origin to avoid stale-state false positives)
- Optionally: a plan file for the current branch (enables plan completion audit)
- Optionally: `TODOS.md` for cross-referencing open work
- Optionally: `DESIGN.md` for design system calibration
- A review checklist file at `.claude/skills/review/checklist.md` (required -- stop if missing)

## Methodology

### Step 0: Detect base branch

Detect the git hosting platform from the remote URL (GitHub, GitLab, or git-native fallback). Determine the branch this PR targets, or the repo's default branch if no PR exists. Use this as "the base branch" in all subsequent steps.

### Step 1: Check branch

If on the base branch or no diff exists against it: output "Nothing to review" and stop.

### Step 1.5: Scope Drift Detection

Before reviewing code quality, check: did they build what was requested, nothing more, nothing less?

**Determine stated intent.** Read `TODOS.md` (if present), PR description (if PR exists), and commit messages.

**Discover plan file.** Check conversation context for an active plan file first. If none, search common plan store locations for a markdown file matching the current branch or repo name. If a plan file is found via search (not conversation context), read its first 20 lines to verify it's for the current branch's work -- discard if it looks like a different project.

**Extract actionable items from the plan.** Look for: checkbox items (`- [ ]` or `- [x]`), numbered implementation steps, imperative statements ("Add X to Y", "Create Z"), file-level specifications, test requirements, data model changes.

Ignore: Context/Background sections, open questions marked with ?, explicitly deferred items ("Out of scope:", "P2:", etc.), and review report sections.

**Cross-reference against the diff.** For each plan item, classify:
- **DONE** -- clear evidence in the diff (cite specific files)
- **PARTIAL** -- some work exists but incomplete
- **NOT DONE** -- no evidence in the diff
- **CHANGED** -- different approach used, same goal achieved (counts as addressed)

Be conservative with DONE (require clear evidence), generous with CHANGED (goal met by different means).

Output a completion audit table:
```
PLAN COMPLETION AUDIT
═══════════════════════════════
Plan: {path}

## Implementation Items
  [DONE]     Create UserService — src/services/user_service.rb (+142 lines)
  [PARTIAL]  Add validation — model validates but missing controller checks
  [NOT DONE] Add caching layer — no cache-related changes in diff

─────────────────────────────────
COMPLETION: 4/7 DONE, 1 PARTIAL, 1 NOT DONE, 1 CHANGED
─────────────────────────────────
```

**NOT DONE items** feed into MISSING REQUIREMENTS detection. **Diff changes not matching any plan item** feed into SCOPE CREEP detection. Both are informational -- do not block the review.

Output scope drift status:
```
Scope Check: [CLEAN / DRIFT DETECTED / REQUIREMENTS MISSING]
Intent: <1-line summary>
Delivered: <1-line summary>
Plan items: N DONE, M PARTIAL, K NOT DONE
```

### Step 2: Read the checklist

Read `.claude/skills/review/checklist.md`. This file defines what to flag, what to suppress, and the Fix-First heuristic. Do not proceed without it.

### Step 2.5: Check for Greptile review comments (if PR exists)

If a PR exists, check for Greptile automated review comments. Classify each as VALID & ACTIONABLE, VALID BUT ALREADY FIXED, FALSE POSITIVE, or SUPPRESSED (known false positives from previous triage). Store these for Step 5 -- do not block the review if Greptile is unavailable.

### Step 3: Get the diff

Fetch the latest base branch state to avoid false positives from a stale local copy. Then get the full diff against origin's base branch (includes both committed and uncommitted changes).

**Search prior learnings.** Check for learnings from previous sessions on this project (and optionally other projects). When a review finding matches a past learning, surface it: "Prior learning applied: [key] (confidence N/10, from [date])."

### Step 4: Two-pass review

Apply the checklist against the diff:

**Pass 1 (CRITICAL):**
- SQL & Data Safety (injection, mass assignment, missing validation)
- Race Conditions & Concurrency (shared state, TOCTOU, missing transactions)
- LLM Output Trust Boundary (LLM output used in SQL, shell commands, evals, or written to DB without validation)
- Enum & Value Completeness

For Enum & Value Completeness: when the diff adds a new enum value, status, tier, or type constant, search the codebase for all files that reference sibling values, then read those files to check if the new value is handled everywhere. This is the one category where within-diff review is insufficient.

**Pass 2 (INFORMATIONAL):**
- Conditional Side Effects (side effects inside conditionals that look like guards)
- Magic Numbers & String Coupling (hardcoded values that should be constants)
- Dead Code & Consistency (unreachable code, inconsistent patterns)
- LLM Prompt Issues
- Test Gaps (partial -- expanded in Step 4.75)
- View/Frontend
- Performance & Bundle Impact

**Confidence scoring.** Every finding gets a confidence score:

| Score | Meaning | Display |
|-------|---------|---------|
| 9-10 | Verified by reading specific code. Concrete bug demonstrated. | Show normally |
| 7-8 | High confidence pattern match. | Show normally |
| 5-6 | Moderate, could be false positive. | Show with caveat: "Medium confidence, verify" |
| 3-4 | Low confidence, pattern is suspicious. | Appendix only |
| 1-2 | Speculation. | Only report if P0 severity |

Finding format: `[SEVERITY] (confidence: N/10) file:line -- description`

**Search before recommending fixes.** When recommending a pattern for concurrency, caching, auth, or framework-specific behavior: verify the pattern is current for the framework version in use. Check if a built-in solution exists. Verify API signatures. Takes seconds, prevents recommending outdated patterns.

### Step 4.5: Design Review (conditional)

Check if the diff touches frontend files. If not, skip silently.

If frontend files are changed:
1. Read `DESIGN.md` or `design-system.md` if present -- patterns blessed there are not flagged
2. Read the design checklist file
3. Read each changed frontend file in full (not just diff hunks)
4. Apply 7 litmus checks (YES/NO each): brand unmistakable, one strong visual anchor, scannable by headlines only, each section has one job, cards actually necessary, motion improves hierarchy, would feel premium without decorative shadows
5. Check for hard rejections: generic SaaS card grid as first impression, beautiful image with weak brand, strong headline with no clear action, busy imagery behind text, sections repeating same mood, carousel with no narrative, app UI made of stacked cards
6. Classify findings: mechanical CSS fixes (outline:none, !important, font-size < 16px) as AUTO-FIX; judgment calls as ASK

### Step 4.75: Test Coverage Diagram

Detect the test framework (read `CLAUDE.md` first, then auto-detect from project files).

**Trace every code path changed** in the diff. For each changed file: read the full file, trace data flow from every entry point (route handler, exported function, component render), follow through every branch, identify every error path.

**Map user flows.** For each changed feature, think through:
- User flows spanning the change (full journey, not just the function)
- Interaction edge cases: double-click, navigate-away mid-operation, submit with stale data, slow connection, concurrent actions
- Error states the user can see: clear error message or silent failure, can they recover?
- Empty/zero/boundary states

**Build an ASCII coverage diagram** showing both code paths and user flows:

```
CODE PATH COVERAGE
===========================
[+] src/services/billing.ts
    ├── processPayment()
    │   ├── [★★★ TESTED] Happy path — billing.test.ts:42
    │   ├── [GAP]         Network timeout — NO TEST
    │   └── [GAP]         Invalid currency — NO TEST
    └── refundPayment()
        ├── [★★  TESTED] Full refund — billing.test.ts:89
        └── [★   TESTED] Partial refund (smoke only) — billing.test.ts:101

USER FLOW COVERAGE
===========================
[+] Payment checkout flow
    ├── [★★★ TESTED] Complete purchase — checkout.e2e.ts:15
    ├── [GAP] [→E2E] Double-click submit
    └── [★   TESTED] Form validation (checks render only) — checkout.test.ts:40

─────────────────────────────────
COVERAGE: 5/13 paths tested (38%)
GAPS: 8 paths need tests (2 need E2E, 1 needs eval)
─────────────────────────────────
```

Quality rating: ★★★ = behavior + edge cases + error paths, ★★ = correct behavior happy path only, ★ = smoke test / existence check.

**E2E vs unit decision:**
- E2E: common user flows spanning 3+ components/services, integration points where mocking hides real failures, auth/payment/data-destruction flows
- Eval: LLM calls where prompt changed and quality bar must be verified
- Unit: pure functions, internal helpers, single-function edge cases

**Regression rule (mandatory):** When the coverage audit identifies a regression (existing code path broken by the diff, not covered by existing tests), write the regression test immediately. No asking. Commit as `test: regression test for {what broke}`.

**Coverage warning:** If AI-assessed coverage is below the minimum (default 60%, or the `Minimum:` field in `CLAUDE.md`'s `## Test Coverage` section), output a prominent warning before findings. Informational -- does not block review.

**Generate tests for gaps:** If a test framework is detected and gaps exist, classify each gap as AUTO-FIX (simple unit tests for pure functions, edge cases of tested functions) or ASK (E2E tests, tests requiring new infrastructure, tests for ambiguous behavior). Apply AUTO-FIX tests directly. Include ASK tests in the Fix-First batch question.

### Greptile Comment Resolution (after Step 4 findings)

If Greptile comments were classified in Step 2.5, include a header: `+ N Greptile comments (X valid, Y fixed, Z FP)`.

Run the Escalation Detection algorithm from greptile-triage.md to determine Tier 1 (friendly) or Tier 2 (firm) reply template before replying to any comment.

- **VALID & ACTIONABLE:** Included in findings and Follow the Fix-First flow. If fixed: reply using the Fix reply template (inline diff + explanation). If user marks false positive: reply using the False Positive reply template (evidence + suggested re-rank), save to per-project and global greptile-history.
- **FALSE POSITIVE:** Present each via question to the user -- show file:line, body summary, permalink URL, why it's a false positive. Options: A) Reply to Greptile explaining why it's wrong (recommended), B) Fix it anyway (low-effort), C) Ignore. If A: use False Positive reply template, save to history.
- **VALID BUT ALREADY FIXED:** Reply automatically using the Already Fixed reply template -- include what was done and the fixing commit SHA. Save to history. No user question needed.
- **SUPPRESSED:** Skip silently (known false positives from previous triage).

### Step 5: Fix-First Review

**Every finding gets action -- not just critical ones.**

Output header: `Pre-Landing Review: N issues (X critical, Y informational)`

**Step 5a: Classify.** For each finding, classify as AUTO-FIX or ASK per the Fix-First heuristic in the checklist. Critical findings lean toward ASK; informational findings lean toward AUTO-FIX.

**Step 5b: Auto-fix all AUTO-FIX items.** Apply each fix directly. One-line summary per fix: `[AUTO-FIXED] [file:line] Problem → what you did`

**Step 5c: Batch-ask about ASK items.** Present all ASK items in ONE question (not one per item). For each, show severity, problem, recommended fix, and options (Fix or Skip). Include an overall RECOMMENDATION. If 3 or fewer ASK items, individual questions are acceptable.

**Step 5d: Apply approved fixes.**

**Verification of claims:** Before producing the final output:
- "This pattern is safe" requires citing the specific line proving safety
- "This is handled elsewhere" requires reading and citing the handling code
- "Tests cover this" requires naming the test file and method
- Never say "likely handled" or "probably tested" -- verify or flag as unknown
- "This looks fine" is not a finding: either cite evidence it IS fine, or flag as unverified

### Step 5.5: TODOS cross-reference

If `TODOS.md` exists: note which TODOs this PR closes, flag work that should become a new TODO, and reference related TODOs when discussing findings.

### Step 5.6: Documentation staleness check

For each `.md` file in the repo root (README, ARCHITECTURE, CONTRIBUTING, CLAUDE.md): if the code it describes changed in this diff but the doc wasn't updated, flag as INFORMATIONAL: "Documentation may be stale: [file] describes [feature] but code changed in this branch."

### Step 5.7: Adversarial review (auto-scaled)

Scale based on diff size. No configuration needed.

- **Small (< 50 lines changed):** Skip. Print "Small diff -- adversarial review skipped."
- **Medium (50-199 lines):** Run one adversarial pass. If the OpenAI Codex CLI is available, use it with adversarial prompt. Otherwise, delegate to a fresh subagent with no checklist context (genuine independence). Present findings under `ADVERSARIAL REVIEW:` header. These follow the Fix-First flow -- FIXABLE findings go into the pipeline, INVESTIGATE findings are informational.
- **Large (200+ lines):** Run all three additional passes: Codex structured review (with pass/fail gate on P1 findings), Claude adversarial subagent, Codex adversarial challenge. If Codex is unavailable, note that 2 of 4 passes ran.

For medium and large diffs, synthesize findings across all passes after they complete:
```
ADVERSARIAL REVIEW SYNTHESIS (auto: TIER, N lines):
════════════════════════════════════════════════════════════
  High confidence (found by multiple sources): [findings agreed on by >1 pass]
  Unique to Claude structured review: [from earlier step]
  Unique to Claude adversarial: [from subagent, if ran]
  Unique to Codex: [from codex adversarial or code review, if ran]
  Models used: Claude structured ✓  Claude adversarial ✓/✗  Codex ✓/✗
════════════════════════════════════════════════════════════
```

High-confidence findings (agreed on by multiple independent sources) get priority.

For large diffs: if Codex P1 findings found, ask the user -- A) Investigate and fix now (recommended), B) Continue. If A, address findings then re-run Codex review to verify.

**User override:** If the user explicitly asks for a specific tier ("full adversarial", "run all passes", "paranoid review"), honor it regardless of diff size.

### Step 5.8: Persist Review Result

After all review passes complete, persist the final review outcome so ship can recognize that Eng Review was run on this branch:

```
gstack-review-log '{"skill":"review","timestamp":"TIMESTAMP","status":"STATUS","issues_found":N,"critical":N,"informational":N,"commit":"COMMIT"}'
```

STATUS = "clean" if no remaining unresolved findings after Fix-First and adversarial review, otherwise "issues_found". issues_found = total remaining unresolved, critical = remaining critical, informational = remaining informational.

If the review exits early (no diff against base), do NOT write this entry.

### Capture Learnings

If you discovered a non-obvious pattern, pitfall, or architectural insight during the session, log it for future reviews. Types: `pattern`, `pitfall`, `preference`, `architecture`, `tool`. Confidence 1-10. Reference specific files.

Only log genuine discoveries. Do not log obvious patterns or things the user already knows. Test: would this save time in a future session?

If the review exits early before a real review completes, do not log.

## Quality Gates

- [ ] Checklist read before any analysis begins
- [ ] Full diff fetched fresh from origin (not stale local state)
- [ ] Every finding includes confidence score
- [ ] Claims verified: "safe" findings cite the specific safe line, "tested" findings cite the test file
- [ ] Enum completeness checked outside the diff (search for sibling values in other files)
- [ ] Coverage diagram produced for all changed code paths and user flows
- [ ] Regression tests written immediately (no asking) for any identified regressions
- [ ] All findings actioned via Fix-First (auto-fixed or batch-asked, not just listed)
- [ ] Adversarial review tier applied based on diff size (or user override honored)

## Outputs

- Code fixes applied (AUTO-FIX items) and user-approved fixes
- Test additions for gaps and regressions
- ASCII coverage diagram
- Scope drift / plan completion audit (if plan file found)
- Review result persisted for downstream skills (ship's readiness dashboard)

## Feeds Into

- `>ship` -- review result is checked by ship's readiness gate before creating the PR

## Important Rules

- **Read the FULL diff before commenting.** Do not flag issues already addressed in the diff.
- **Fix-first, not read-only.** AUTO-FIX items are applied directly. ASK items are only applied after user approval. Never commit, push, or create PRs -- that's ship's job.
- **Be terse.** One line problem, one line fix. No preamble.
- **Only flag real problems.** Skip anything that's fine. "This looks fine" is not a finding -- either cite evidence it IS fine, or flag as unverified.
- **Use Greptile reply templates from greptile-triage.md.** Every Greptile reply includes evidence. Never post vague replies.

## Harness Notes

The adversarial review passes (medium/large tier) delegate to independent subagents and optionally invoke the OpenAI Codex CLI. In single-agent harnesses: skip Codex passes, run only the Claude adversarial subagent pass by treating it as a second sequential analysis pass with fresh context (no checklist loaded).

The Greptile integration (Step 2.5) requires PR existence and the `gh` CLI to fetch comments. Skip silently if either is unavailable.

See `harness-compat.md`: Subagents, External CLIs (Codex), Git/GitHub CLI.
