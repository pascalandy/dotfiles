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

Use agent names as workflow handles, not as a changelog.

### Primary workflow handles

- `build` — main build-oriented preset
- `@gpt` — standard GPT subagent
- `@gpthigh` — higher-effort GPT subagent
- `@gptxhigh` — highest-effort GPT subagent
- `@minimax` — daily-driver general-purpose agent
- `@kimi` — Kimi-based alternative for comparison
- `@gemini-or` — Gemini via OpenRouter
- `@grok` — Grok via OpenRouter
- `@glm` — GLM-based general-purpose handle

### Reserved subagent handles

- `@agtmini`
- `@agttiny`

Rules:
- These names are reserved workflow handles.
- They must stay provider-agnostic.
- They must remain exactly `agtmini` and `agttiny` unless a deliberate workflow-breaking change is made.
- If they ever change, update this document because that affects how the system is operated, not just how it is configured.

## Defaults

- Default agent: `minimax`
- Top-level model fallback: `opencode/glm-5`
- Small model: `minimax`

Why `minimax` is the default:
- fast enough for daily use
- capable enough to act as the general driver
- good balance between quality and responsiveness

## Provider routing decisions

### GPT routing

Use direct OpenAI for GPT.

Rules:
- keep GPT on the native OpenAI path
- do not treat OpenRouter or Zen as the primary GPT route
- use separate handles for increased reasoning effort instead of overloading one GPT agent

### Gemini routing

Gemini may be accessed through more than one provider path.

Guideline:
- keep provider-specific Gemini handles explicit in the config
- prefer documenting the routing pattern here, not temporary provider health

### Grok routing

Use OpenRouter for Grok when the newest Grok models are only available there.

### GLM routing

Use Zen for GLM 5.
Keep direct ZAI access available when needed for GLM 4.7-specific workflows.

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
