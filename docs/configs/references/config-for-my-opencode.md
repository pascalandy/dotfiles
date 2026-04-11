---
name: OpenCode Configuration Notes
description: Decision-making, naming rules, and routing intent for OpenCode config
tags:
  - area/ea
  - kind/doc
  - status/stable
date_created: 2026-04-07
date_updated: 2026-04-11
---

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
| 1 | `1-kimi` | Kimi K2.5 Turbo | Fireworks AI |
| 2 | `2-opus` | Claude Opus 4.6 (adaptive thinking, low effort) | Anthropic |
| 3 | `3-gpt` | GPT-5.4 (high reasoning, low verbosity) | OpenAI |
| 4 | `4-sonnet` | Claude Sonnet 4.6 (adaptive thinking, low effort) | Anthropic |

### Subagent handles

- `@gptmini` — GPT-5.4 Mini (low reasoning, low verbosity)
- `@glm` — GLM 5.1 via zai-coding-plan (thinking enabled)
- `@gpthigh` — GPT-5.4 with high reasoning effort
- `@gptxhigh` — GPT-5.4 with xhigh reasoning effort
- `@worker` — GPT-5.4 general worker (medium reasoning)
- `@worker1` — Claude Sonnet 4.6 worker (adaptive thinking, high effort)
- `@worker2` — GLM 5.1 worker
- `@worker3` — GPT-5.4 Mini worker
- `@gemini` — Gemini 3.1 Pro via OpenRouter
- `@flash` — Gemini 3 Flash via OpenRouter
- `@minimax` — MiniMax 2.7 via OpenRouter (parked alternative)

### Naming rules

- Numbered prefixes (`1-` to `6-`) control Tab order. OpenCode sorts agents alphabetically by key; numbers sort before letters.
- Subagents and disabled agents do not use number prefixes.
- Names are workflow handles, not provider labels. They must stay provider-agnostic.
- If a primary agent is reordered, renumber all affected keys and update this document.

## Defaults

- Default agent: `1-kimi`
- Small model: `gptmini`

Why `1-kimi` is the default:
- Kimi K2.5 Turbo via Fireworks AI provides fast, capable responses
- Positioned as the primary agent (slot 1) for quick access via Tab cycling
- Routes through Fireworks AI for optimized inference

## Provider routing decisions

### Kimi routing

Primary Kimi K2.5 access via Fireworks AI provider as `1-kimi`.

Guideline:
- `1-kimi` routes through Fireworks AI (`fireworks-ai/accounts/fireworks/routers/kimi-k2p5-turbo`)
- This is the default agent and primary entry point
- Keep OpenRouter (`moonshotai/kimi-k2.5:nitro`) registered as `kimi-oc` fallback for when Fireworks is unavailable

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

GLM 5.1 is available as a subagent via the `zai-coding-plan` provider:
- `@glm` — primary GLM subagent (thinking enabled)
- `worker2` — secondary GLM worker

Keep Zen (`opencode/glm-5.1`) registered as `glm-zen` fallback for when the coding plan is unavailable.

### Local model usage

Keep at least one local LM Studio option available for small or offline-friendly tasks.
Current handle: `gemma` → `lmstudio/mlx-community/gemma-4-31b-6bit` (mode `all`, not number-prefixed).

## Provider inventory

Providers currently wired in `opencode.json.tmpl` and their role:

| Provider | Used by | Role |
|----------|---------|------|
| `fireworks-ai` | `1-kimi` | Primary Kimi K2.5 Turbo route |
| `anthropic` | `2-opus`, `4-sonnet`, `worker1` | Native Claude route |
| `openai` | `3-gpt`, `gptmini`, `gpthigh`, `gptxhigh`, `worker`, `worker3` | Native GPT route |
| `zai-coding-plan` | `glm`, `worker2` | Primary GLM route |
| `openrouter` | `gemini`, `flash`, plus parked `grok`/`mimo`/`minimax`/`kimi-oc` | OpenRouter for Gemini and Grok-class fallbacks |
| `lmstudio` | `gemma` | Local offline route |
| `opencode` (Zen) | parked `gemini-zen`/`flash-zen`/`glm-zen`/`mini-zen` | Zen fallback pool |

## Updating skills

When we update and/or change these configurations, they impact our skills such as:

- `dot_config/ai_templates/skills/specs/use-subagents`
- `dot_config/ai_templates/skills/specs/run-oc`

**IMPORTANT**: Always update these skills in order to avoid drift. 

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
