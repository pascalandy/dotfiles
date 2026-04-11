---
name: pa-advisor
description: CLI-agnostic executor→advisor delegation pattern. When loaded, the current CLI agent behaves as an executor that consults Claude Opus as a read-only advisor via `claude -p`. Mimics Anthropic's native advisor-tool primitive client-side. Works in Codex, Gemini, OpenCode, Claude Code, or any CLI with shell access.
keywords: [pa-advisor, advisor, executor, delegation, opus, planning-oracle, reconcile, headless-claude]
---

# pa-advisor

When this skill is loaded, **you act as an EXECUTOR**. At strategic moments, you shell out to `claude -p` with the full task context to consult Claude Opus as a read-only **ADVISOR**, then resume execution with the advice in hand. This is a client-side simulation of Anthropic's advisor-tool primitive — it works in any CLI that can run shell commands.

Depends on `$headless-claude` invocation conventions. See `dot_config/ai_templates/skills/utils/headless-claude/SKILL.md` for flag reference.

## When to call the advisor

Four timing rules. Follow them.

1. **Before substantive work.** After orientation (file reads, fetches, exploring) but BEFORE writing, editing, or committing to an interpretation. **Orientation is not substantive work.** Writing, editing, and declaring an answer are.
2. **When stuck.** Errors recurring, approach not converging, results that don't fit the evidence.
3. **Before declaring done.** After writes and tests are complete, call the advisor as a final review.
   - **CRITICAL**: make your deliverable durable BEFORE this call — write the file, save the result, commit the change. The advisor call is slow; if the parent CLI dies during it, an unwritten result is lost and a durable one persists.
4. **Before changing approach.** Don't silently switch branches. Consult first.

**Negative rule:** On short reactive loops where the next action is dictated by a tool output you just read, don't call the advisor. It adds most of its value on the first call, before the approach crystallizes.

Default cadence for a non-trivial task: **at least one call before committing to an approach, and one before declaring done.**

## How to call the advisor

Run this exact shell pipeline. Fill in the tagged context block.

```bash
cat <<'ADVISOR_CONTEXT' | claude --model opus -p \
  --permission-mode plan \
  --no-session-persistence \
  --fallback-model sonnet \
  --effort medium \
  --output-format text \
  --max-turns 1 \
  --append-system-prompt "You are an advisor consulted mid-task. You have no tools and cannot take actions. Read the full context above, then produce a strategic plan or course correction. Respond in under 100 words using enumerated steps, not explanations. If you detect a conflict between the executor's current plan and evidence in the context, name it explicitly." \
  "Produce strategic advice for the next step based on the context above."
<ROLE>
I am an executor CLI agent working on a task. I am consulting you for strategic guidance.

<TASK>
<paste the original user request, verbatim>

<CONSTRAINTS>
<non-negotiables: language, style guide, files to not touch, budget, deadline>

<TRANSCRIPT>
<chronological log of tool calls and their results so far>

<CURRENT_STATE>
<current working hypothesis, blockers, intended next step>

<PRIOR_ADVICE>
<for calls 2+: verbatim advisor responses so far, numbered by call, most recent last>

<QUESTION>
<one-line: what I specifically need guidance on this call>
ADVISOR_CONTEXT
```

### Flag rationale (do not strip)

| Flag | Purpose |
|---|---|
| `--model opus` | Highest-capability advisor model. |
| `-p` | Print mode, non-interactive. |
| `--permission-mode plan` | Read-only, tool-less, **never hangs**. Enforces the advisor's read-only semantics from Anthropic's native spec. |
| `--no-session-persistence` | Stateless. Prevents leakage into Claude Code's local session store — load-bearing for CLI-agnosticism, since that store is invisible to Codex/Gemini/OpenCode. |
| `--fallback-model sonnet` | Opus 4.6 can get overloaded; fallback beats a hang. |
| `--effort medium` | Default. Medium is the documented cost/quality sweet spot for an Opus advisor paired with any executor. Raise to `high` or `max` for truly hard problems; `max` requires Opus 4.6. |
| `--output-format text` | Explicit default; prevents future CLI upgrades from surprising the pipeline. |
| `--max-turns 1` | Enforces single-shot advisor semantics — the advisor should never loop. |
| `--append-system-prompt "..."` | Injects the advisor role + the conciseness directive (the `<100 words, enumerated steps` rule cuts 35-45% of tokens with no quality loss per Anthropic's benchmarks) + the conflict-surfacing rule. |
| Positional `"Produce strategic advice..."` | User-turn instruction; concatenates with the piped stdin context into the advisor's user message. |

### Context-packet tags

Every call must include all tags. Missing tags degrade advice quality sharply.

| Tag | Contents |
|---|---|
| `<ROLE>` | Always identical; anchors the advisor's role. |
| `<TASK>` | The original user request, verbatim. |
| `<CONSTRAINTS>` | Non-negotiables: language, style guide, files to not touch, budget, deadline. (We can't inherit these from a system prompt the way the native primitive does, so state them explicitly.) |
| `<TRANSCRIPT>` | Chronological log of tool calls and their results so far. The load-bearing tag — the advisor's advice quality is bounded by how complete this is. |
| `<CURRENT_STATE>` | Your current hypothesis, blocker, or intended next action. |
| `<PRIOR_ADVICE>` | For calls 2+ only: verbatim prior advisor responses, numbered by call, most recent last. This compensates for losing Anthropic's native multi-turn advisor memory — since each `claude -p` call is stateless, you are responsible for re-passing prior advice. |
| `<QUESTION>` | One line: what you specifically need guidance on this call. |

### Long-transcript variant

When `<TRANSCRIPT>` gets large (approaching shell `ARG_MAX` limits or hard to read in-place), write the context to a file and pass it via `--append-system-prompt-file`:

```bash
mkdir -p .advisor
# ... write the full context packet to .advisor/context-N.md ...
claude --model opus -p \
  --permission-mode plan --no-session-persistence \
  --fallback-model sonnet --effort medium \
  --output-format text --max-turns 1 \
  --append-system-prompt-file .advisor/context-N.md \
  "Produce strategic advice for the next step based on the context above."
```

Same stateless semantics, disk-backed instead of stdin-backed.

## How to treat the advice

- **Give the advice serious weight.** Follow it unless empirically contradicted by a tool result or primary source (the file says X, the test output shows Y).
- **A passing self-test is NOT evidence the advice is wrong.** It's evidence your test doesn't check what the advice is checking.
- **On conflict, reconcile — don't silently switch.** If you've already retrieved data pointing one way and the advisor points another, make one more advisor call: *"I found X, you suggest Y, which constraint breaks the tie?"* A reconcile call is cheaper than committing to the wrong branch.

## Prerequisites

```bash
# Verify auth (OAuth or ANTHROPIC_API_KEY)
claude auth status --text

# Smoke-test the advisor pipeline end-to-end
claude --model opus -p \
  --permission-mode plan --no-session-persistence \
  --fallback-model sonnet --effort medium \
  "Reply with OK if you received this."
```

Advisor responses are typically 400-700 text tokens (1,400-1,800 including discarded thinking). Budget your parent-CLI context accordingly for `<PRIOR_ADVICE>` accumulation across calls.

## Worked example — "Fix the failing test in payments/handler_test.go"

**Phase 1 — orient (no advisor yet)**

```
read_file("payments/handler.go")
read_file("payments/handler_test.go")
bash("go test ./payments/ -run TestPaymentFlow -v")  → AssertionError, nil pointer at handler.go:142
```

**Phase 2 — call advisor (before writing any fix)**

```bash
cat <<'ADVISOR_CONTEXT' | claude --model opus -p \
  --permission-mode plan --no-session-persistence \
  --fallback-model sonnet --effort medium \
  --output-format text --max-turns 1 \
  --append-system-prompt "You are an advisor consulted mid-task. You have no tools and cannot take actions. Read the full context above, then produce a strategic plan or course correction. Respond in under 100 words using enumerated steps, not explanations. If you detect a conflict between the executor's current plan and evidence in the context, name it explicitly." \
  "Produce strategic advice for the next step based on the context above."
<ROLE>
I am an executor CLI agent working on a task. I am consulting you for strategic guidance.

<TASK>
Fix the failing test in payments/handler_test.go.

<CONSTRAINTS>
Go 1.22. Do not touch the test file itself. Do not add new dependencies.

<TRANSCRIPT>
1. Read payments/handler.go — handler dereferences req.Metadata unconditionally at line 142.
2. Read payments/handler_test.go — test sends a request without the optional Metadata field.
3. Ran `go test ./payments/ -run TestPaymentFlow -v` — fails with nil pointer dereference at handler.go:142.

<CURRENT_STATE>
My hypothesis: add a nil check before dereferencing req.Metadata at line 141. Planning to apply that and re-run the test.

<QUESTION>
Is the nil check at the handler the right fix, or should I push the validation elsewhere?
ADVISOR_CONTEXT
```

**Phase 3 — execute the plan**

```
read_file("payments/validator.go")
write_file("payments/handler.go", <nil check at 141>)
bash("go test ./payments/ -v")  → all PASS
```

**Phase 4 — durable deliverable, then call advisor again for review**

Commit or save the fix FIRST, then:

```bash
cat <<'ADVISOR_CONTEXT' | claude --model opus -p \
  --permission-mode plan --no-session-persistence \
  --fallback-model sonnet --effort medium \
  --output-format text --max-turns 1 \
  --append-system-prompt "You are an advisor consulted mid-task. You have no tools and cannot take actions. Read the full context above, then produce a strategic plan or course correction. Respond in under 100 words using enumerated steps, not explanations. If you detect a conflict between the executor's current plan and evidence in the context, name it explicitly." \
  "Produce strategic advice for the next step based on the context above."
<ROLE>
I am an executor CLI agent working on a task. I am consulting you for strategic guidance.

<TASK>
Fix the failing test in payments/handler_test.go.

<CONSTRAINTS>
Go 1.22. Do not touch the test file itself. Do not add new dependencies.

<TRANSCRIPT>
1. Orient: read handler, test, ran test, saw nil pointer at handler.go:142.
2. Read payments/validator.go — validator allows nil metadata (optional field).
3. Wrote nil check at handler.go:141.
4. Ran `go test ./payments/ -v` — all PASS.

<CURRENT_STATE>
Fix applied and committed. About to declare done.

<PRIOR_ADVICE>
Call 1: "1. Nil check at handler.go:141 is correct — validator confirms metadata is optional. 2. Also check refund_handler.go, dispute_handler.go, webhook_handler.go for the same pattern. 3. Run the specific test then the full suite."

<QUESTION>
Anything I'm missing before I declare this task done?
ADVISOR_CONTEXT
```

**Phase 5 — apply any follow-up the advisor surfaced, then declare done.**

## Non-goals

- Does NOT spawn parallel sub-agents (see `$five-council` for that pattern).
- Does NOT implement retry logic, billing tracking, or rate-limit handling.
- Does NOT replace actual tool execution — the executor still does all writes itself.
- Does NOT attempt to preserve session state across parent-CLI invocations.
- Does NOT use `--bare` — that breaks OAuth users. `--bare` is a CI-only variant, not the default.
