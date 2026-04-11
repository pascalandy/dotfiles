# Plan: `pa-advisor` — CLI-agnostic executor→advisor skill

## Context

The user is studying Anthropic's new advisor-tool primitive (documented in `docs/ideas/references/1020-advisor/`) and wants the same delegation pattern available outside Claude Code — usable from Codex CLI, Gemini CLI, OpenCode, or anywhere else. Anthropic's native primitive only works inside a single `/v1/messages` call on the Claude API, so it can't be invoked from any other CLI agent.

This plan creates a new skill, **`pa-advisor`**, whose `SKILL.md` *is* the executor prompt. When any CLI agent loads it, that agent behaves as the executor and learns to consult Claude Opus (via `claude -p`) as a read-only advisor at strategic moments. The advisor is invoked by shelling out through the existing `headless-claude` plumbing. The pattern is **dynamic** (multiple advisor calls per task), **stateless** (every call is self-contained — no reliance on Claude Code's local session store, which would break CLI-agnosticism), and **portable** (the shell pipeline is identical regardless of which CLI is reading the skill).

Intended outcome: a single skill file that can be dropped into any CLI agent's instruction-loading path and immediately provides a working advisor-consultation loop with ~3 timing rules, a documented context-packet shape, and a copy-pasteable shell pipeline.

## Deliverables

**Two files:**

```
dot_config/ai_templates/skills/pa-sdlc/pa-advisor/
└── SKILL.md                                            # the new skill

docs/ideas/references/1020-advisor/
└── plan.md                                             # archive of THIS plan, alongside source material
```

1. **`SKILL.md`** — single-file skill (no `references/`, no router, no sub-modes). Matches the shape of sibling orchestration utilities `pa-sdlc/delegate/SKILL.md` and `pa-sdlc/five-council/SKILL.md`.
2. **`plan.md`** — verbatim copy of this plan file exported into the same research folder that sourced the design (`webclip-advisor.md`, `explore.md`). Rationale: the plan was *derived* from those two files; co-locating it preserves the provenance chain so future readers see source → derived plan → implemented skill in one place. No content transformation — straight copy.

## Why this location

- **`pa-sdlc/`** (not `utils/`) — the family already houses cross-cutting orchestration utilities (`delegate`, `five-council`, `hunk-review`) alongside methodology skills. `pa-advisor` is the same shape: a cross-cutting pattern that any phase can invoke. `utils/` is plumbing (`headless-claude`); `pa-sdlc/` is methodology that uses the plumbing.
- **`pa-*` naming** matches the user's `pa-sdlc` family convention.
- **Single-file** matches `delegate/SKILL.md` precedent — no premature router structure for a single primitive.

## `SKILL.md` contents (section-by-section)

### 1. Frontmatter

```yaml
---
name: pa-advisor
description: CLI-agnostic executor→advisor delegation pattern. When loaded, the current CLI agent behaves as an executor that consults Claude Opus as a read-only advisor via `claude -p`. Mimics Anthropic's native advisor-tool primitive client-side. Works in Codex, Gemini, OpenCode, Claude Code, or any CLI with Bash access.
keywords: [pa-advisor, advisor, executor, delegation, opus, planning-oracle, reconcile, headless-claude]
---
```

### 2. Purpose (2 sentences)

One paragraph: "When this skill is loaded, you (the CLI agent reading it) act as an EXECUTOR. At strategic moments, you shell out to `claude -p` with the full task context to consult Claude Opus as a read-only ADVISOR, then resume execution with the advice in hand. This is a client-side simulation of Anthropic's advisor-tool primitive — it works in any CLI that can run shell commands."

### 3. When to call the advisor

Four timing rules, lifted directly from `docs/ideas/references/1020-advisor/webclip-advisor.md:359-370`:

- **Before substantive work.** After orientation (file reads, fetches, exploring) but BEFORE writing, editing, or committing to an interpretation. **"Orientation is not substantive work"** — quote this sentence verbatim; it's the most common mis-timing.
- **When stuck.** Errors recurring, approach not converging, results that don't fit.
- **Before declaring done.** After writes and tests are complete, call the advisor as a final review. **CRITICAL**: make the deliverable durable *before* the final advisor call — write the file, save the result. The call is slow; if the parent CLI dies mid-call, an unwritten result is lost.
- **Before changing approach.** Don't silently switch branches — consult first.

One negative rule: **"Short reactive loops don't need repeat calls."** If the next action is dictated by tool output you just read, don't call the advisor — it adds most of its value on the first call, before the approach crystallizes.

### 4. How to call the advisor (the exact pipeline)

```bash
cat <<'ADVISOR_CONTEXT' | claude --model opus -p \
  --permission-mode plan \
  --no-session-persistence \
  --fallback-model sonnet \
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
<for calls 2+: verbatim advisor responses so far, numbered by call>

<QUESTION>
<one-line: what I specifically need guidance on this call>
ADVISOR_CONTEXT
```

**Every flag justified**:
- `--model opus` — highest available advisor model (verified in `headless-claude/SKILL.md:78`)
- `-p` — print mode, non-interactive (verified in `headless-claude/SKILL.md:46`)
- `--permission-mode plan` — read-only, never hangs, no tools (verified in `headless-claude/SKILL.md:22` as "safe default for audits, summaries, reviews; never hangs"). This enforces the advisor's tool-less semantics from Anthropic's spec.
- `--no-session-persistence` — enforces stateless operation; no leakage into Claude Code's session store (verified in `headless-claude/SKILL.md:255`). **Critical for CLI-agnosticism** — session state would live in a place the calling CLI can't see or manage.
- `--fallback-model sonnet` — Opus 4.6 can get overloaded; fallback beats a hang (verified in `headless-claude/SKILL.md:86`)
- `--output-format text` — explicit even though it's default; prevents future upgrades from surprising us
- `--max-turns 1` — enforces single-shot semantics; the advisor should never loop (verified in `headless-claude/SKILL.md:204`)
- `--append-system-prompt "..."` — injects the advisor role, the conciseness directive (cuts 35-45% of tokens per the webclip), and the conflict-surfacing rule
- Positional `"Produce strategic advice..."` — the user-turn instruction; pairs with the piped stdin context (verified canonical shape in `headless-claude/SKILL.md:53`: `cat logs.txt | claude -p --permission-mode plan "Summarize these errors"`)

**Long-transcript variant** — a documented fallback for when `<TRANSCRIPT>` gets large enough to worry about `ARG_MAX`: write the context to `./.advisor/context.md` and pass it via `--append-system-prompt-file`. Same stateless semantics, disk-backed instead of stdin-backed.

### 5. Context-packet spec (the seven tags)

Tag-by-tag, one line each:

- `<ROLE>` — always identical; anchors the advisor's role
- `<TASK>` — verbatim original user request
- `<CONSTRAINTS>` — non-negotiables the advisor must respect; we can't inherit these from a system prompt the way the native primitive does, so we state them explicitly
- `<TRANSCRIPT>` — chronological log of tool calls and results (the load-bearing one)
- `<CURRENT_STATE>` — current hypothesis, blocker, intended next action
- `<PRIOR_ADVICE>` — for calls 2+; verbatim advisor responses numbered by call, most recent last. **This compensates for losing Anthropic's native multi-turn advisor memory** — since each `claude -p` call is stateless, the executor is responsible for re-passing prior advice.
- `<QUESTION>` — one-line disambiguator for this specific call

### 6. How to treat the advice

Lifted from `docs/ideas/references/1020-advisor/webclip-advisor.md:374-378`:

- **Give the advice serious weight.** Follow unless empirically contradicted by a tool result or primary source (the file says X, the test output shows Y).
- **A passing self-test is NOT evidence the advice is wrong** — it's evidence your test doesn't check what the advice is checking.
- **On conflict, reconcile — don't silently switch.** Quote verbatim: *"I found X, you suggest Y, which constraint breaks the tie?"* — make one more advisor call. A reconcile call is cheaper than committing to the wrong branch.

### 7. Prerequisites / smoke test

```bash
# Check auth (OAuth or ANTHROPIC_API_KEY)
claude auth status --text

# Smoke-test the advisor pipeline end-to-end
claude --model opus -p --permission-mode plan --no-session-persistence \
  "Reply with OK if you received this."
```

Note: advisor responses typically return 400-700 text tokens (1,400-1,800 including thinking, per webclip line 3). Budget context accordingly for `<PRIOR_ADVICE>` accumulation across calls.

### 8. Worked example

One compact walkthrough of a toy task (e.g., "find the bug in X.py") showing:
- Phase 1: executor orients with 2-3 read-only tool calls
- Phase 2: executor calls advisor with the full heredoc template filled in
- Phase 3: executor executes the plan (3 tool calls)
- Phase 4: executor writes the deliverable, THEN calls advisor for review
- Phase 5: executor applies any follow-up and declares done

### 9. Non-goals

- Does NOT spawn parallel sub-agents (unlike `five-council`)
- Does NOT implement retry logic, billing, or rate-limit handling
- Does NOT replace actual tool execution — the executor still does all writes itself
- Does NOT try to preserve session state across parent-CLI invocations
- Does NOT use `--bare` — that breaks OAuth users and is CI-only

### 10. Dependencies

One-line cross-reference: "Uses `$headless-claude` invocation conventions. See `dot_config/ai_templates/skills/utils/headless-claude/SKILL.md` for flag reference and permission-mode semantics."

## Critical files

**To create:**
- `/Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/pa-sdlc/pa-advisor/SKILL.md`
- `/Users/andy16/.local/share/chezmoi/docs/ideas/references/1020-advisor/plan.md` (verbatim copy of `/Users/andy16/.claude/plans/vivid-wishing-adleman.md`)

**To reference (already verified, no changes):**
- `/Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/utils/headless-claude/SKILL.md` — source of flag semantics (`-p`, `--permission-mode plan`, `--no-session-persistence`, `--fallback-model`, `--model opus`, `--append-system-prompt`, `--max-turns`, pipe-stdin+positional pattern, `claude auth status --text`)
- `/Users/andy16/.local/share/chezmoi/docs/ideas/references/1020-advisor/webclip-advisor.md` — source for verbatim timing block (lines 359-370), treatment block (lines 374-378), and durability rule (line 365)
- `/Users/andy16/.local/share/chezmoi/docs/ideas/references/1020-advisor/explore.md` — source for the worked-example pattern (lines 104-198 show the five-phase "Fix failing CI" walkthrough that our worked example will mirror)
- `/Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/pa-sdlc/delegate/SKILL.md` — structural template (single-file, frontmatter + narrative, no router)
- `/Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/pa-sdlc/five-council/SKILL.md` — secondary structural reference

## Reused existing utilities (no duplication)

- **`headless-claude` skill** — all CLI-flag semantics are inherited; `pa-advisor` is the prompt *pattern* that uses `headless-claude` plumbing. No flag docs duplicated in the new skill — cross-reference instead.
- **`pa-sdlc/` family conventions** — frontmatter style, keyword shape, single-file layout, all copied from sibling `delegate/SKILL.md`.

## Decisions locked in (documented here so implementation doesn't drift)

1. **Stateless over stateful** — every advisor call uses `--no-session-persistence`; context is re-packed each call. Rationale: Claude Code's session store is invisible to Codex/Gemini/OpenCode, so relying on it would silently break CLI-agnosticism. The executor accumulates `<PRIOR_ADVICE>` in the context packet instead.
2. **`pa-sdlc/pa-advisor/` over `utils/advisor-bridge/`** — methodology skills live in `pa-sdlc/`; plumbing lives in `utils/`. `pa-advisor` is methodology.
3. **Single `SKILL.md`, no `references/`** — one primitive, no sub-modes; matches `delegate/` and `five-council/` precedent. YAGNI.
4. **Opus 4.6 pinned as advisor** via `--model opus` with `--fallback-model sonnet` — matches Anthropic's native model pairing (executor at any capability → Opus advisor).
5. **`--permission-mode plan`** — enforces the advisor's tool-less read-only semantics from Anthropic's spec; also the only permission mode that's guaranteed not to hang.
6. **Conciseness directive baked in** — "under 100 words, enumerated steps, not explanations" is embedded in `--append-system-prompt`, not left to the executor to remember.
7. **Do NOT use `--bare`** — breaks OAuth users; CI-only variant documented as an aside only.

## Execution order

1. **Export this plan first** — copy `/Users/andy16/.claude/plans/vivid-wishing-adleman.md` verbatim to `/Users/andy16/.local/share/chezmoi/docs/ideas/references/1020-advisor/plan.md`. No edits, no reformatting. Do this before writing the skill so the archived plan reflects the plan-as-approved, not any mid-implementation drift.
2. **Then write the skill** — create `dot_config/ai_templates/skills/pa-sdlc/pa-advisor/SKILL.md` per the section-by-section spec above.
3. **Then verify** — per the steps below.

## Verification

After creating both files, verify end-to-end in four steps:

### Step 0 — Plan archived

```bash
# Exported plan exists and matches source byte-for-byte
diff /Users/andy16/.claude/plans/vivid-wishing-adleman.md \
     /Users/andy16/.local/share/chezmoi/docs/ideas/references/1020-advisor/plan.md

# Sits next to the source material it was derived from
ls /Users/andy16/.local/share/chezmoi/docs/ideas/references/1020-advisor/
# expect: explore.md  plan.md  webclip-advisor.md
```

### Step 1 — File lands where chezmoi expects it

```bash
# Source file exists
ls -la /Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/pa-sdlc/pa-advisor/SKILL.md

# Chezmoi sees it as managed (or pending addition)
chezmoi status | grep pa-advisor

# Dry-run the apply so we know it'll land in the applied runtime path
just cm-apply-dry 2>&1 | grep -i advisor
```

### Step 2 — Advisor pipeline smoke test (the one flag combo the whole skill depends on)

```bash
# Auth is present
claude auth status --text

# The exact pipeline the skill documents, with a trivial context
cat <<'ADVISOR_CONTEXT' | claude --model opus -p \
  --permission-mode plan \
  --no-session-persistence \
  --fallback-model sonnet \
  --output-format text \
  --max-turns 1 \
  --append-system-prompt "You are an advisor. Respond in under 100 words using enumerated steps." \
  "Produce strategic advice for the next step."
<ROLE> I am an executor CLI agent.
<TASK> Print "hello world" in Python.
<TRANSCRIPT> (none yet — I just received the task)
<CURRENT_STATE> Ready to write a one-liner.
<QUESTION> Any gotchas I should know before writing this?
ADVISOR_CONTEXT
```

**Expected**: returns plain text under ~100 words in enumerated steps. Exit code 0. No hang. If it hangs, `--permission-mode plan` isn't being honored — investigate.

### Step 3 — CLI-agnostic load test

Load the skill in at least two CLIs and verify the pipeline runs from each:

- **Claude Code**: `/pa-advisor` (native skill resolution) — should load the `SKILL.md` contents into the session.
- **OpenCode**: load via `/pa-advisor` or the opencode skill-loading mechanism documented in `dot_config/opencode/AGENTS.md`.
- **Codex or Gemini**: paste the SKILL.md contents (or `Read` it as a file) into the session's instructions, then confirm the calling agent can execute the shell pipeline from section 4.

Acceptance: in all three CLIs, the agent (a) recognizes the four timing rules, (b) can construct a filled-in heredoc context packet from its working state, and (c) successfully runs the exact shell pipeline and parses the advisor's text response as guidance for its next step.

### Step 4 — Commit (only after user approval)

Standard chezmoi commit flow:
```bash
just ci                                # local checks
git add dot_config/ai_templates/skills/pa-sdlc/pa-advisor/SKILL.md \
        docs/ideas/references/1020-advisor/plan.md
git commit -m "✨ add: pa-advisor skill — CLI-agnostic executor→advisor delegation pattern"
```
