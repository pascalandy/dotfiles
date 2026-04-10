---
title: Add OpenCode CLI Provider Support to distill
type: feat
  - status/close
date: 2026-04-07
---

# Add OpenCode CLI Provider Support to distill

## Overview

Add support for the OpenCode CLI (`opencode`) as a third LLM provider alongside Claude and Codex. OpenCode uses curated agent selection (e.g., `1-kimi`, `2-opus`) and will default to `1-kimi` for fast, economical distillation.

## Problem Frame

The `distill` tool currently supports Claude and Codex. Users want to use OpenCode's agents (particularly the fast/cheap `1-kimi` for routine distillation tasks). Without OpenCode support, users must manually craft shell pipelines or use OpenCode directly, breaking the unified workflow.

## Requirements Trace

- R1. Add `opencode` as a valid `--provider` option
- R2. Support the current curated OpenCode agents: `1-kimi`, `2-opus`, `3-gpt`, `4-sonnet`, `worker`, `worker1`, `worker2`, `worker3`, `glm`, `gemini`, `gpthigh`, `gptxhigh`, `gptmini`, `flash`
- R3. Default model for OpenCode: `1-kimi`
- R4. Context limit: 250,000 tokens for OpenCode
- R5. Input via stdin pipe (not `--file` flag)
- R6. Output via `--format json` event stream, parsed from emitted `text` events
- R7. Do not add OpenCode-specific `--thinking` support
- R8. Reject `--effort` for OpenCode; reasoning remains defined by the selected agent
- R9. Update help.md with OpenCode documentation
- R10. Update `--list-models` to include OpenCode agents

## Scope Boundaries

- Out: Server mode (`opencode serve`) - use direct `opencode run` only
- Out: Session management (`--continue`, `--fork`) - each call is independent
- Out: File attachments beyond stdin pipe

## Key Technical Decisions

- **Agent naming**: Use full curated agent names (`1-kimi`, `2-opus`) as the canonical model identifiers. No short aliases to avoid confusion.
- **Effort handling**: OpenCode agent configuration already encodes reasoning behavior. `distill` will reject `--effort` for `--provider opencode` rather than mapping it to `--variant` or silently ignoring it.
- **Thinking flag**: Do not expose provider-specific OpenCode thinking controls in `distill`. `opencode --thinking` changes output shape by emitting reasoning events, which is a poor fit for clean markdown distillation.
- **Output parsing**: `opencode run --format json` emits a stream of JSON events (`step_start`, `text`, `step_finish`, and optionally `reasoning`), not a single JSON object. Parse and concatenate emitted `text` events only.
- **stdin contract**: `opencode run --agent <agent> -` correctly reads the prompt body from stdin, so `distill` can keep its current piped-input architecture.

## Implementation Units

- [ ] **Unit 1: Add OpenCode constants and configuration**

**Goal:** Add OpenCode provider constants, model list, and context limits to the script.

**Requirements:** R1, R2, R3, R4

**Dependencies:** None

**Files:**
- Modify: `dot_config/ai_templates/skills/meta/distill/scripts/distill.py`

**Approach:**
- Add `PROVIDER_OPENCODE = "opencode"` constant
- Add `VALID_OPENCODE_MODELS` tuple with the 14 curated agent names
- Add `DEFAULT_OPENCODE_MODEL = "1-kimi"`
- Update `VALID_PROVIDERS` to include `PROVIDER_OPENCODE`
- Add `CONTEXT_LIMITS` entry for opencode: 250_000
- Do not add OpenCode provider entries to `EFFORT_ETL`

**Test scenarios:**
- Happy path: Import script successfully with new constants
- Edge case: Verify all 14 curated agent names are in `VALID_OPENCODE_MODELS`

**Verification:**
- Script imports without errors
- `VALID_OPENCODE_MODELS` contains all expected curated agents

---

- [ ] **Unit 2: Define OpenCode argument behavior**

**Goal:** Make OpenCode behavior explicit in argument resolution without adding provider-specific thinking flags.

**Requirements:** R7, R8

**Dependencies:** Unit 1

**Files:**
- Modify: `dot_config/ai_templates/skills/meta/distill/scripts/distill.py`

**Approach:**
- Keep the existing CLI surface unchanged for OpenCode
- When `provider == opencode`, reject `--effort` with a clear usage error
- Update `ResolvedPlan` handling so OpenCode paths do not require a provider-specific effort translation

**Test scenarios:**
- Happy path: `--provider opencode` resolves without provider-specific flags
- Edge case: `--effort` with OpenCode returns a clear usage error

**Verification:**
- Dry-run shows OpenCode without `--variant` or `--thinking`
- Help text matches actual OpenCode behavior

---

- [ ] **Unit 3: Implement run_opencode() function**

**Goal:** Add OpenCode CLI invocation function with stdin pipe and JSON event parsing.

**Requirements:** R5, R6, R8

**Dependencies:** Unit 1, Unit 2

**Files:**
- Modify: `dot_config/ai_templates/skills/meta/distill/scripts/distill.py`

**Approach:**
- Create `run_opencode(plan: ResolvedPlan, output_file: Path)` function
- Build command: `opencode run --agent <model> --format json -`
- Pass input via stdin (pipe)
- Parse newline-delimited JSON events from stdout
- Concatenate `text` event payloads in emission order
- Ignore `reasoning` events and lifecycle events (`step_start`, `step_finish`)
- Write result to output_file
- Return usage stats dict

**Command structure:**
```python
[
    "opencode",
    "run",
    "--agent", plan.model,
    "--format", "json",
    "-",  # stdin
]
```

**Test scenarios:**
- Happy path: OpenCode CLI is invoked with correct arguments
- Happy path: JSON event stream is parsed and `text` content is written to file
- Error path: Handle JSON parse errors
- Error path: Handle OpenCode CLI failures
- Edge case: Ignore `reasoning` events if they appear in future output streams

**Verification:**
- Dry-run shows correct OpenCode command
- Actual run produces output file with distilled content

---

- [ ] **Unit 4: Update run_llm() dispatcher**

**Goal:** Add OpenCode to the provider dispatcher.

**Requirements:** R1

**Dependencies:** Unit 3

**Files:**
- Modify: `dot_config/ai_templates/skills/meta/distill/scripts/distill.py`

**Approach:**
- Update `run_llm()` function to handle `PROVIDER_OPENCODE`
- Call `run_opencode(plan, output_file)` when provider is opencode

**Test scenarios:**
- Happy path: Provider dispatch routes to correct function

**Verification:**
- `--provider opencode` triggers `run_opencode()`

---

- [ ] **Unit 5: Update print_list_models()**

**Goal:** Include OpenCode agents in model listing.

**Requirements:** R10

**Dependencies:** Unit 1

**Files:**
- Modify: `dot_config/ai_templates/skills/meta/distill/scripts/distill.py`

**Approach:**
- Add OpenCode section to `print_list_models()`
- List all 14 curated agents with default marked
- Do not show an OpenCode effort translation table, since reasoning is agent-defined

**Test scenarios:**
- Happy path: `--list-models` shows OpenCode agents
- Happy path: `--list-models --provider opencode` filters correctly

**Verification:**
- `distill.py --list-models` displays OpenCode agents section

---

- [ ] **Unit 6: Update help.md documentation**

**Goal:** Document OpenCode provider in user-facing help.

**Requirements:** R9

**Dependencies:** Unit 1, Unit 2

**Files:**
- Modify: `dot_config/ai_templates/skills/meta/distill/help.md`

**Approach:**
- Add OpenCode to `--provider` section
- Add OpenCode models to `--model` section
- Update defaults table with OpenCode row
- Clarify that OpenCode uses curated agents and stdin piping
- Clarify that `--format json` is parsed from emitted text events
- Clarify that OpenCode does not use `--thinking` or provider-specific effort mapping in `distill`

**Test scenarios:**
- Happy path: `distill.py --help` renders updated help.md

**Verification:**
- Help text includes OpenCode provider information

---

- [ ] **Unit 7: End-to-end testing**

**Goal:** Verify complete OpenCode integration works.

**Requirements:** All

**Dependencies:** Units 1-6

**Files:**
- Test only, no file changes

**Approach:**
- Test dry-run: `distill.py file.md --provider opencode --dry-run`
- Test list-models: `distill.py --list-models --provider opencode`
- Test actual minimal run against `opencode run --format json`

**Test scenarios:**
- Happy path: OpenCode provider selected, default model is 1-kimi
- Happy path: Context size check uses 250k limit
- Happy path: JSON event parsing extracts final text output cleanly
- Edge case: Event stream contains non-text events

**Verification:**
- All dry-run outputs show expected configuration
- No errors in any test scenario

## System-Wide Impact

- **Interaction graph:** None - this is an additive feature
- **Error propagation:** OpenCode errors follow same pattern as Claude/Codex
- **State lifecycle risks:** None
- **API surface parity:** New provider option added to CLI
- **Unchanged invariants:** Claude and Codex behavior unchanged

## Risks & Dependencies

| Risk | Mitigation |
|------|------------|
| OpenCode CLI not installed | Same handling as Claude/Codex - clear error message |
| OpenCode JSON event schema changes | Parse only stable `type == "text"` events and fail loudly on malformed JSON |
| Kimi token count approximation | Use tiktoken (same as other providers), note it's approximate |
| OpenCode agent limits differ under the hood | Start with a conservative provider-wide limit and tighten later if per-agent limits become necessary |

## Sources & References

- **Origin:** User request for OpenCode support
- **Validated locally:** `opencode run --format json --agent 1-kimi "Reply with exactly OK and nothing else."` emitted `step_start`, `text`, and `step_finish` events; `opencode run --format json --agent 1-kimi -` successfully consumed stdin and returned the stdin payload
- **Skills:** `headless-opencode`, `delegate`
- **Related:** Existing Claude and Codex implementations in distill.py
