# Investigate

> Systematic debugging with root cause investigation -- four phases: investigate, analyze, hypothesize, implement. Iron Law: no fixes without root cause.

## When to Use

- User reports an error, bug, or unexpected behavior
- User asks "why is this broken", "debug this", "fix this bug", "root cause analysis", "investigate this error"
- Tests are failing and the cause is unclear
- Something that used to work stopped working (regression)
- Proactively suggest when the user pastes an error message or stack trace

## Inputs

- Error message, stack trace, or description of unexpected behavior
- Reproduction steps (or help gathering them)
- The codebase (read access to trace the code path)
- Git history to detect regressions

## Methodology

### Iron Law

**No fixes without root cause investigation first.** Fixing symptoms creates whack-a-mole debugging. Every fix that doesn't address root cause makes the next bug harder to find.

### Phase 1: Root Cause Investigation

**Collect symptoms.** Read all error messages, stack traces, and reproduction steps. If the user hasn't provided enough, ask ONE question at a time -- not a list of 5 questions.

**Read the code.** Trace the code path from the symptom back to potential causes. Find all references to the failing function/module, read the logic. Don't just skim the diff -- read the full file.

**Check recent changes.** Run `git log --oneline -20 -- <affected-files>`. Was this working before? What changed? A regression means the root cause is in the diff.

**Reproduce.** Can you trigger the bug deterministically? If not, gather more evidence before forming any hypothesis. An unreproducible bug is not ready for hypothesis testing.

**Search prior learnings.** Check if this project (or other projects on the same machine, if cross-project learnings are enabled) has seen a similar pattern before. When a prior learning applies, surface it explicitly: "Prior learning applied: [key] (confidence N/10, from [date])."

**Output a root cause hypothesis:** a specific, testable claim about what is wrong and why. Not "something in auth.ts is wrong" -- "auth.ts:47, the token check returns undefined when the session expires because the session middleware doesn't handle expired tokens before the route guard runs."

### Scope Lock

After forming the hypothesis, lock edits to the narrowest directory containing the affected files. Tell the user the scope boundary. This prevents accidental changes to unrelated code during the debug session.

If the bug genuinely spans the whole repo or scope is unclear, skip the lock and note why.

### Phase 2: Pattern Analysis

Check if the bug matches a known pattern:

| Pattern | Signature | Where to look |
|---------|-----------|---------------|
| Race condition | Intermittent, timing-dependent | Concurrent access to shared state |
| Nil/null propagation | NoMethodError, TypeError | Missing guards on optional values |
| State corruption | Inconsistent data, partial updates | Transactions, callbacks, hooks |
| Integration failure | Timeout, unexpected response | External API calls, service boundaries |
| Configuration drift | Works locally, fails in staging/prod | Env vars, feature flags, DB state |
| Stale cache | Shows old data, fixes on cache clear | Redis, CDN, browser cache |

Also check `TODOS.md` for related known issues. Recurring bugs in the same files are an architectural smell, not coincidence.

**External pattern search:** If the bug doesn't match a known pattern, search for the error type online. Sanitize first -- strip hostnames, IPs, file paths, SQL fragments, customer identifiers. Search the generic error category and framework context, not the raw message.

### Phase 3: Hypothesis Testing

Before writing any fix, verify the hypothesis.

1. Add a temporary log statement, assertion, or debug output at the suspected root cause. Run the reproduction. Does the evidence match the hypothesis?

2. If the hypothesis is wrong: do not guess the next one. Return to Phase 1. Gather more evidence. Consider searching for the sanitized error type before forming a new hypothesis.

3. **3-strike rule.** If 3 hypotheses fail, STOP. Present:
   ```
   3 hypotheses tested, none match. This may be an architectural issue rather than a simple bug.

   A) Continue investigating -- I have a new hypothesis: [describe]
   B) Escalate for human review -- this needs someone who knows the system
   C) Add logging and wait -- instrument the area and catch it next time
   ```

**Red flags -- slow down if you see:**
- "Quick fix for now" -- there is no "for now." Fix it right or escalate.
- Proposing a fix before tracing data flow -- that's guessing.
- Each fix reveals a new problem elsewhere -- wrong layer, not wrong code.

### Phase 4: Implementation

Once root cause is confirmed:

1. **Fix the root cause, not the symptom.** The smallest change that eliminates the actual problem.

2. **Minimal diff.** Fewest files touched, fewest lines changed. Resist the urge to refactor adjacent code.

3. **Write a regression test** that:
   - Fails without the fix (proves the test is meaningful)
   - Passes with the fix (proves the fix works)

4. **Run the full test suite.** Paste the output. No regressions allowed.

5. **If the fix touches more than 5 files:** flag the blast radius before proceeding:
   ```
   This fix touches N files. That's a large blast radius for a bug fix.
   A) Proceed -- the root cause genuinely spans these files
   B) Split -- fix the critical path now, defer the rest
   C) Rethink -- maybe there's a more targeted approach
   ```

### Phase 5: Verification and Report

Fresh verification: reproduce the original bug scenario and confirm it's fixed. Not optional.

Output a structured debug report:

```
DEBUG REPORT
════════════════════════════════════════
Symptom:         [what the user observed]
Root cause:      [what was actually wrong]
Fix:             [what was changed, with file:line references]
Evidence:        [test output, reproduction showing fix works]
Regression test: [file:line of the new test]
Related:         [TODOS.md items, prior bugs in same area, architectural notes]
Status:          DONE | DONE_WITH_CONCERNS | BLOCKED
════════════════════════════════════════
```

### Capture Learnings

If you discovered a non-obvious pattern, pitfall, or architectural insight during the session, log it. Types: `pattern` (reusable approach), `pitfall` (what NOT to do), `preference` (user stated), `architecture` (structural decision), `tool` (library/framework insight).

Assign confidence 1-10. An observed pattern you verified in the code is 8-9. An inference is 4-5. A user preference explicitly stated is 10. Reference the specific files the learning applies to (enables staleness detection).

Only log genuine discoveries -- things that would save time in a future session.

## Quality Gates

- [ ] Root cause stated as a specific, testable claim before any fix is written
- [ ] Hypothesis verified with evidence (log output, test run, reproduction) before implementing
- [ ] 3-strike rule applied: 3 failed hypotheses triggers escalation, not more guessing
- [ ] Fix addresses root cause (not symptom)
- [ ] Regression test written, confirmed to fail without fix and pass with fix
- [ ] Full test suite run, output pasted
- [ ] Debug report produced with all fields populated

**Completion status:**
- DONE -- root cause found, fix applied, regression test written, all tests pass
- DONE_WITH_CONCERNS -- fixed but cannot fully verify (e.g., intermittent bug, requires staging)
- BLOCKED -- root cause unclear after investigation, escalated

## Outputs

- Code fix (minimal diff, root cause targeted)
- Regression test
- Debug report (structured, with file:line references)
- Learnings logged for future sessions

## Feeds Into

- `>review` -- if the fix is non-trivial, run a pre-landing review before shipping
- `>ship` -- when fix is verified and ready to PR

## Harness Notes

The scope lock mechanism writes to a freeze state file and checks it via a pre-edit hook. In harnesses without hook support, enforce scope boundaries manually: check before each edit that the target file is within the agreed scope. If it isn't, ask the user before proceeding.

See `harness-compat.md`: Hooks/Pre-edit checks.
