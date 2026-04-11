# Verification Before Completion

> Run verification commands and confirm output before making any success, completion, or passing claims — evidence before assertions, always.

## When to Use

**ALWAYS before:**
- Any variation of success or completion claims
- Any expression of satisfaction (e.g., "Great!", "Perfect!", "Done!")
- Any positive statement about work state
- Committing, creating PRs, marking tasks complete
- Moving to the next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion or correctness

## Inputs

- The claim you are about to make (pass/complete/fixed/clean/etc.)
- The specific command that would verify that claim
- Access to run that command

## Methodology

### Core Principle

Claiming work is complete without verification is dishonesty, not efficiency.

**Violating the letter of this rule is violating the spirit of this rule.**

### The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you haven't run the verification command in this message, you cannot claim it passes.

### The Gate Function

Execute ALL five steps before making any claim:

```
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete — not a prior run)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

### Common Failures Table

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

### Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] → "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] → "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

### Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/create PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

### Rationalization Prevention Table

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

### Why This Matters

From documented failure history:
- Trust broken when human partner said "I don't believe you"
- Undefined functions shipped — would crash in production
- Missing requirements shipped — incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## Quality Gates

Before making any claim, confirm:
- [ ] Identified the exact command that proves the claim
- [ ] Ran the FULL command fresh in this message
- [ ] Read full output and checked exit code / failure count
- [ ] Output actually confirms the claim
- [ ] Claim is stated WITH evidence, not without

## Outputs

- Verified claim backed by fresh command output
- Or: honest statement of actual status with evidence

## Feeds Into

- Any commit or PR workflow
- Task completion signaling
- Subagent result reporting

## Harness Notes

"Run verification" means executing a terminal command and reading its output. This is not optional and cannot be replaced with reasoning or recall of prior results.
