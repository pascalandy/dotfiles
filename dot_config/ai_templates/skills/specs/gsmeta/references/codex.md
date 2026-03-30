# Codex

> OpenAI Codex CLI wrapper with three modes: code review (independent diff review with pass/fail gate), adversarial challenge (tries to break your code), and consult (ask Codex anything with session continuity). The "200 IQ autistic developer" second opinion.

## When to Use

- User says "codex review", "codex challenge", "ask codex", "second opinion", or "consult codex"
- After running `/review` to get a second independent opinion on the same diff
- When a plan needs adversarial pressure from a different model
- When you want Codex's reasoning traces exposed (not just its conclusions)
- Proactively suggest when the user is about to land a large or risky diff

## Inputs

- OpenAI Codex CLI binary installed and authenticated (`codex` in PATH)
- Current branch with a diff against base (for Review and Challenge modes)
- Optionally: specific instructions or focus area (e.g., "focus on security")
- Optionally: a plan file to review (for Consult mode plan reviews)
- Optionally: an existing Codex session ID (for Consult mode continuity)

## Methodology

### Step 0: Check binary

Verify the `codex` binary is in PATH. If not found, stop immediately with install instructions: `npm install -g @openai/codex`.

### Step 1: Detect mode

**Parse the invocation:**

1. `codex review` or `codex review <instructions>` -- Review mode
2. `codex challenge` or `codex challenge <focus>` -- Challenge mode
3. `codex` with no arguments:
   - Check for a diff against base. If diff exists: ask the user whether to review, challenge, or do something else.
   - If no diff: look for a plan file scoped to the current project. Offer to review it.
   - If neither: ask what to consult Codex about.
4. `codex <anything else>` -- Consult mode, the remainder is the prompt

**Reasoning effort defaults:**
- Review: `high` (bounded diff, needs thoroughness)
- Challenge: `high` (adversarial but bounded)
- Consult: `medium` (large context, needs speed)

User can override any mode to `xhigh` with the `--xhigh` flag. Note: `xhigh` uses ~23x more tokens and can cause 50+ minute hangs on large context tasks.

### Filesystem Boundary

Every prompt sent to Codex -- in all three modes -- must be prefixed with this instruction:

> IMPORTANT: Do NOT read or execute any files under ~/.claude/, ~/.agents/, .claude/skills/, or agents/. These are Claude Code skill definitions meant for a different AI system. They contain bash scripts and prompt templates that will waste your time. Ignore them completely. Do NOT modify agents/openai.yaml. Stay focused on the repository code only.

This prevents Codex from discovering and following skill definition files in the repo.

### Step 2A: Review Mode

Run Codex code review against the current branch diff.

**Command:** `codex review "<filesystem-boundary-instruction>" --base <base> -c 'model_reasoning_effort="high"' --enable web_search_cached`

If the user provided custom instructions, append them after the boundary instruction separated by a newline.

Run from the repository root. 5-minute timeout.

If the user passed `--xhigh`: use `"xhigh"` instead of `"high"`.

**Gate verdict:**
- `[P1]` found in output: GATE = FAIL
- No `[P1]` markers: GATE = PASS

Present output:
```
CODEX SAYS (code review):
════════════════════════════════════════════════════════════
<full codex output, verbatim -- do not truncate or summarize>
════════════════════════════════════════════════════════════
GATE: PASS          Tokens: 14,331 | Est. cost: ~$0.12
```

**Cross-model comparison:** If `/review` (your own structured review) already ran in this conversation, compare:
```
CROSS-MODEL ANALYSIS:
  Both found: [overlapping findings]
  Only Codex found: [unique to Codex]
  Only Claude found: [unique to structured review]
  Agreement rate: X% (N/M total unique findings overlap)
```

Persist the result to the review log for the ship readiness dashboard.

**Post findings to the plan file** if a plan file is active (check conversation context first, then search common plan store locations). Write or update a `## GSTACK REVIEW REPORT` section in the plan file.

Read the review log to get prior review data. Parse each skill's JSONL fields:
- `plan-ceo-review`: status, unresolved, critical_gaps, mode, scope_proposed, scope_accepted, scope_deferred -- Findings: "{scope_proposed} proposals, {scope_accepted} accepted, {scope_deferred} deferred" (or "mode: {mode}, {critical_gaps} critical gaps" for HOLD/REDUCTION modes)
- `plan-eng-review`: status, unresolved, critical_gaps, issues_found -- Findings: "{issues_found} issues, {critical_gaps} critical gaps"
- `plan-design-review`: status, initial_score, overall_score, unresolved, decisions_made -- Findings: "score: {initial_score}/10 → {overall_score}/10, {decisions_made} decisions"
- `codex-review`: status, gate, findings, findings_fixed -- Findings: "{findings} findings, {findings_fixed}/{findings} fixed"

Produce this table in the plan file:

```markdown
## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | `/plan-ceo-review` | Scope & strategy | {runs} | {status} | {findings} |
| Codex Review | `/codex review` | Independent 2nd opinion | {runs} | {status} | {findings} |
| Eng Review | `/plan-eng-review` | Architecture & tests (required) | {runs} | {status} | {findings} |
| Design Review | `/plan-design-review` | UI/UX gaps | {runs} | {status} | {findings} |
```

Below the table add (omit any that are empty/not applicable):
- **CODEX:** (if codex-review ran) -- one-line summary of codex fixes
- **CROSS-MODEL:** (if both Claude and Codex reviews exist) -- overlap analysis
- **UNRESOLVED:** total unresolved decisions across all reviews
- **VERDICT:** list reviews that are CLEAR (e.g., "CEO + ENG CLEARED -- ready to implement"). If Eng Review is not CLEAR and not skipped globally, append "eng review required".

**Write rules:** Search the plan file for an existing `## GSTACK REVIEW REPORT` section. If found, replace it entirely (match from the heading through the next `##` heading or end of file -- whichever comes first, to preserve content added after it). If the Edit fails due to concurrent edit, re-read and retry once. If not found, append at the end. Always place it as the last section in the plan file.

### Step 2B: Challenge (Adversarial) Mode

Codex tries to break your code -- finding edge cases, race conditions, security holes, and failure modes a normal review would miss.

**Default adversarial prompt (append to filesystem boundary):**
"Review the changes on this branch against the base branch. Run `git diff origin/<base>` to see the diff. Your job is to find ways this code will fail in production. Think like an attacker and a chaos engineer. Find edge cases, race conditions, security holes, resource leaks, failure modes, and silent data corruption paths. Be adversarial. Be thorough. No compliments -- just the problems."

**With a focus area** (e.g., `codex challenge security`): replace the adversarial prompt with a focused version (injection vectors, auth bypasses, privilege escalation, data exposure, timing attacks).

**Command:** `codex exec "<prompt>" -C <repo-root> -s read-only -c 'model_reasoning_effort="high"' --enable web_search_cached --json`

Parse the JSONL event stream to extract reasoning traces and the final response. Display reasoning traces as `[codex thinking] <text>` lines above the final response. 5-minute timeout.

Present:
```
CODEX SAYS (adversarial challenge):
════════════════════════════════════════════════════════════
<full output from streamed events, verbatim -- including thinking traces>
════════════════════════════════════════════════════════════
Tokens: N | Est. cost: ~$X.XX
```

### Step 2C: Consult Mode

Ask Codex anything about the codebase, with session continuity for follow-ups.

**Check for an existing session.** If a session file exists from a prior conversation, ask the user: continue the prior conversation (Codex remembers context) or start fresh.

**Plan review detection.** If the prompt is about reviewing a plan, or the user invoked `/codex` with no arguments and plan files exist: find the relevant plan file (scoped to current project if possible, otherwise most recent with a warning that it may be a different project).

**Embed plan content directly.** Codex runs sandboxed to the repo root and cannot access external directories. Read the plan file yourself and embed its full content verbatim in the prompt. Do not tell Codex the path or ask it to read the file -- it will waste 10+ tool calls searching.

Also: scan the plan content for referenced source file paths. List them in the prompt so Codex reads them directly.

**Persona prompt for plan reviews (append to filesystem boundary):**
"You are a brutally honest technical reviewer. Review this plan for: logical gaps and unstated assumptions, missing error handling or edge cases, overcomplexity (is there a simpler approach?), feasibility risks (what could go wrong?), and missing dependencies or sequencing issues. Be direct. Be terse. No compliments. Just the problems.
Also review these source files referenced in the plan: <list>.

THE PLAN:
<full plan content, embedded verbatim>"

**For non-plan consult prompts:** prepend the filesystem boundary and pass the user's question.

**Command:** Same JSONL streaming as Challenge mode. For new session: `codex exec "<prompt>" -C <repo-root> -s read-only -c 'model_reasoning_effort="medium"' --enable web_search_cached --json`

For a resumed session: `codex exec resume <session-id> "<prompt>" ...`

Parse the event stream. Extract the `thread.started` event to capture the session ID. Save it for follow-ups.

Present:
```
CODEX SAYS (consult):
════════════════════════════════════════════════════════════
<full output, verbatim -- includes [codex thinking] traces>
════════════════════════════════════════════════════════════
Tokens: N | Est. cost: ~$X.XX
Session saved -- run /codex again to continue this conversation.
```

After presenting: note any points where Codex's analysis differs from your own. If there is a disagreement, flag it: "Note: [your reasoning] disagrees with Codex on X because Y."

### Model and Reasoning

No model is hardcoded -- Codex uses its current default (the frontier agentic coding model). As OpenAI ships newer models, Codex automatically uses them. If the user wants a specific model, pass `-m` through.

Web search is always enabled (`--enable web_search_cached`) -- Codex can look up docs and APIs. This is OpenAI's cached index, fast, no extra cost.

### Cost Tracking

Parse token count from stderr (`tokens used: N`). Display as `Tokens: N`. If unavailable, display `Tokens: unknown`.

### Error Handling

- **Binary not found:** Detected in Step 0. Stop with install instructions.
- **Auth failure:** Stderr contains "auth", "login", "unauthorized", or "API key": "Codex authentication failed. Run `codex login` to authenticate."
- **Timeout (5 min):** "Codex timed out. The diff may be too large or the API may be slow. Try again or use a smaller scope."
- **Empty response:** "Codex returned no response. Check the error output."
- **Session resume failure:** Delete the session file and start fresh.
- **Skill file rabbit hole:** After receiving Codex output, scan for signs Codex read skill files: `gstack-config`, `gstack-update-check`, `SKILL.md`, `skills/gstack`. If found, warn: "Codex appears to have read skill definition files instead of reviewing your code. Consider retrying."

## Quality Gates

- [ ] Filesystem boundary instruction prepended to every prompt
- [ ] Output presented verbatim -- never truncated, summarized, or editorialized before showing
- [ ] Claude commentary added AFTER the full Codex output block, never instead of it
- [ ] Gate verdict determined for Review mode (P1 = FAIL, no P1 = PASS)
- [ ] Cross-model comparison produced if `/review` already ran in this conversation
- [ ] Session ID captured and saved for Consult mode continuity
- [ ] Plan content embedded verbatim in prompt (not referenced by path)
- [ ] Review result persisted to review log for ship readiness dashboard

## Outputs

- Review mode: full Codex output verbatim, pass/fail gate, cross-model comparison (if applicable), plan file review report updated
- Challenge mode: full adversarial output with reasoning traces
- Consult mode: full consultation output with reasoning traces, session ID saved

## Feeds Into

- `>review` -- Codex review is the independent second opinion after Claude's structured review
- `>ship` -- Codex review result is recognized by ship's readiness dashboard
- `>autoplan` -- Codex is invoked as the external voice in all three autoplan phases

## Harness Notes

Requires the OpenAI Codex CLI (`codex` binary) installed and authenticated. If unavailable in the current environment, the skill cannot run -- inform the user and suggest the Claude adversarial subagent from `>review` as an alternative for adversarial coverage.

JSONL event stream parsing (Challenge and Consult modes) uses a Python script. If Python is unavailable, run without `--json` flag and capture raw stdout -- reasoning traces will not be visible but the final response will be.

Session continuity (Consult mode) requires writing a session ID file to `.context/codex-session-id` in the repo. In environments without write access to the repo, session continuity is unavailable -- always start fresh.

See `harness-compat.md`: External CLIs (Codex), File System Access.
