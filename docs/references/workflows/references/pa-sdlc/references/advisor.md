---
name: Advisor
description: `pa-advisor` is the executor→advisor delegation pattern — use it to consult Claude Opus as a read-only strategic advisor mid-task via `claude -p`
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - pa-sdlc
---

Advisor is the eighth skill in the `pa-sdlc` family. Load it with the explicit entry point `pa-advisor`.

Unlike the other stages, Advisor is **not a phase** in the lifecycle — it is a **pattern** that applies *during* any phase. When loaded, the executor CLI (Codex, Gemini, OpenCode, Claude Code, or any shell-capable agent) behaves as an executor that shells out to `claude -p` to consult Claude Opus as a read-only advisor at strategic moments, then resumes work with the advice in hand.

This page is a short workflow-level summary. The full invocation playbook — the exact shell pipeline, all the flags and their rationale, the context-packet tag schema, the long-transcript variant — lives in `dot_config/ai_templates/skills/pa-sdlc/pa-advisor/SKILL.md`. Read the skill file when you are about to actually invoke the advisor.

## What the pattern does

Anthropic's API has a native "advisor-tool" primitive: a read-only, tool-less second model consulted mid-task for strategic guidance. CLI agents running against the chat API — or running without that primitive at all — cannot use it directly. `pa-advisor` simulates the primitive client-side, in any CLI that can run shell commands, by:

1. Building a structured context packet (role, task, constraints, transcript, current state, prior advice, question).
2. Piping the packet into `claude -p` with flags that enforce read-only, stateless, single-turn semantics.
3. Reading the advisor's short enumerated response back into the executor's context.
4. Resuming work with the advice treated as strong guidance.

The pattern works because `claude --permission-mode plan` is read-only and tool-less — the advisor cannot take actions, only reason about them. It is CLI-agnostic because the call happens through a plain shell pipeline, not through any particular agent harness.

## When to call the advisor

Four timing rules from the SKILL.md. Follow them.

1. **Before substantive work.** After orientation but BEFORE writing, editing, or committing to an interpretation. Orientation is not substantive work; writing and declaring an answer are.
2. **When stuck.** Errors recurring, approach not converging, results that do not fit the evidence.
3. **Before declaring done.** After writes and tests are complete, as a final review. Make your deliverable **durable before this call** — write the file, save the result, commit the change — because the advisor call is slow and a parent-CLI death mid-call loses unwritten results.
4. **Before changing approach.** Do not silently switch branches. Consult first.

**Negative rule:** On short reactive loops where the next action is dictated by a tool output you just read, do not call the advisor. Value is highest on the first call, before the approach crystallizes.

Default cadence for a non-trivial task: **at least one call before committing to an approach, and one before declaring done.**

## How to call the advisor

The call is a `cat <<'ADVISOR_CONTEXT' | claude ...` heredoc pipeline with a specific set of flags. Do not paraphrase or abbreviate — the flag set is load-bearing. Read the skill file for the exact invocation.

Required flags (summary):

| Flag | Purpose |
|---|---|
| `--model opus` | Highest-capability advisor model. |
| `-p` | Print mode, non-interactive. |
| `--permission-mode plan` | Read-only, tool-less. Never hangs. |
| `--no-session-persistence` | Stateless. Keeps the call CLI-agnostic. |
| `--fallback-model sonnet` | Opus can get overloaded; fallback beats a hang. |
| `--effort medium` | Documented cost/quality sweet spot. |
| `--output-format text` | Explicit default. |
| `--max-turns 1` | Single-shot advisor. |
| `--append-system-prompt "..."` | Injects the advisor role and the `<100 words, enumerated steps` rule. |

Required context-packet tags:

| Tag | Contents |
|---|---|
| `<ROLE>` | Always identical; anchors the advisor's role. |
| `<TASK>` | The original user request, verbatim. |
| `<CONSTRAINTS>` | Non-negotiables: language, style guide, files to not touch, budget, deadline. |
| `<TRANSCRIPT>` | Chronological log of tool calls and their results so far. |
| `<CURRENT_STATE>` | Current hypothesis, blocker, or intended next action. |
| `<PRIOR_ADVICE>` | For calls 2+: verbatim prior advisor responses. |
| `<QUESTION>` | One line: what you specifically need guidance on this call. |

Missing tags degrade advice quality sharply. The `<TRANSCRIPT>` tag is the load-bearing one — the advice is bounded by how complete it is.

## How to treat the advice

- **Give it serious weight.** Follow it unless empirically contradicted by a tool result or primary source.
- **A passing self-test is NOT evidence the advice is wrong.** It is evidence your test does not check what the advice is checking.
- **On conflict, reconcile — do not silently switch.** If your retrieved data points one way and the advisor points another, make a second advisor call: *"I found X, you suggest Y, which constraint breaks the tie?"*

## How Advisor interacts with the rest of `pa-sdlc`

Advisor is orthogonal to the other stages. It is useful at every one of them:

- **During Scout**, to decide whether a map is thorough enough or needs deeper passes.
- **During Scope**, to verify that the change surface is correct before committing to it.
- **During Vision**, to pressure-test the direction before writing the alignment draft.
- **During Architect**, to stress-test the slice sequence before handing off to Implement.
- **During Implement**, to get a second opinion before a non-obvious fix, and before declaring done.
- **During Doc-update**, to verify that the chosen canonical placement makes sense.
- **During Doc-cleaner**, to classify ambiguous pages where the keep/update/replace/consolidate/remove judgment is unclear.

In every case the call is the same shape. Only the `<QUESTION>` tag changes.

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

Advisor responses are typically 400–700 text tokens. Budget parent-CLI context accordingly for `<PRIOR_ADVICE>` accumulation across calls.

## Non-goals

- Does NOT spawn parallel sub-agents (see `five-council` for that pattern).
- Does NOT implement retry, billing tracking, or rate-limit handling.
- Does NOT replace actual tool execution — the executor still does all writes itself.
- Does NOT attempt to preserve session state across parent-CLI invocations.
- Does NOT use `--bare` — that breaks OAuth users.

## Related

- [[scout]], [[scope]], [[vision]], [[architect]], [[implement]], [[doc-update]], [[doc-cleaner]] — the stages Advisor supports
- source: `dot_config/ai_templates/skills/pa-sdlc/pa-advisor/SKILL.md`
- related skill: `dot_config/ai_templates/skills/devtools/headless/references/claude/MetaSkill.md` for the `claude -p` flag reference (via the `headless` meta-skill)
