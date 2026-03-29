# OpenCode configuration notes

Source of truth: `dot_config/opencode/opencode.json.tmpl`

This document captures decision-making, naming rules, and routing intent.
It is **not** a status board for what is enabled, disabled, active, or parked. For the current live configuration, check the source file directly.

## Purpose of this note

Use this file to record:
- why an agent or provider exists
- how agent names should be interpreted
- routing decisions between providers
- workflow constraints that should survive future config edits

Do not use this file to track:
- which agents are currently enabled or disabled
- temporary experiments
- day-to-day toggles
- provider availability snapshots

## Agent mental model

Agent names use a numbered prefix (`1-` through `6-`) to control display order in the Tab picker. The number is the sort key; the suffix is the workflow handle.

### Primary agents (Tab cycling order)

| # | Key | Model | Provider |
|---|-----|-------|----------|
| 1 | `1-opus` | Claude Opus 4.6 | Anthropic |
| 2 | `2-gpt` | GPT-5.4 (medium reasoning) | OpenAI |
| 3 | `3-gptmini` | GPT-5.4 Mini (low reasoning) | OpenAI |
| 4 | `4-glm` | GLM 5.1 | zai-coding-plan |
| 5 | `5-sonnet` | Claude Sonnet 4.6 (low effort) | Anthropic |
| 6 | `6-kimi` | Kimi K2.5 | OpenCode Zen |

### Subagent handles

- `@gpthigh` — GPT-5.4 with high reasoning effort
- `@gptxhigh` — GPT-5.4 with xhigh reasoning effort
- `@worker` — GPT-5.4 general worker
- `@worker1` — Claude Sonnet 4.6 worker
- `@worker2` — GLM 5.1 worker
- `@worker3` — GPT-5.4 Mini worker
- `@gemini` — Gemini 3.1 Pro via OpenRouter
- `@flash` — Gemini 3 Flash via OpenRouter
- `@minimax` — MiniMax 2.7 via OpenRouter

### Naming rules

- Numbered prefixes (`1-` to `6-`) control Tab order. OpenCode sorts agents alphabetically by key; numbers sort before letters.
- Subagents and disabled agents do not use number prefixes.
- Names are workflow handles, not provider labels. They must stay provider-agnostic.
- If a primary agent is reordered, renumber all affected keys and update this document.

## Defaults

- Default agent: `1-opus`
- Small model: `3-gptmini`

Why `1-opus` is the default:
- Claude Opus 4.6 is the most capable model available
- Adaptive thinking with low effort setting balances quality and cost
- Pinned to position 1 in the Tab picker

## Provider routing decisions

### GPT routing

Use direct OpenAI for GPT.

Rules:
- keep GPT on the native OpenAI path
- do not treat OpenRouter or Zen as the primary GPT route
- use separate handles for increased reasoning effort instead of overloading one GPT agent

### Gemini routing

Gemini is available as a subagent only (not in the main Tab picker).

Guideline:
- `@gemini` (Gemini 3.1 Pro) and `@flash` (Gemini 3 Flash) route through OpenRouter
- keep provider-specific Gemini handles explicit in the config
- prefer documenting the routing pattern here, not temporary provider health

### Grok routing

Use OpenRouter for Grok when the newest Grok models are only available there.

### GLM routing

Primary GLM 5.1 access via `zai-coding-plan` provider (coding-optimized endpoint) as `4-glm`.
Keep Zen (`opencode/glm-5.1`) available as `glm-zen` fallback when needed (currently disabled).

### Local model usage

Keep at least one local LM Studio option available for small or offline-friendly tasks.

## Documentation boundary

When updating this note in the future:
- record durable decisions
- record naming rules
- record workflow conventions
- record routing intent

Do not add sections like:
- "currently enabled"
- "disabled"
- "parked"
- "working today"
- support transcripts or temporary outage notes

If something is a live config fact, it belongs in `dot_config/opencode/opencode.json.tmpl`, not here.
