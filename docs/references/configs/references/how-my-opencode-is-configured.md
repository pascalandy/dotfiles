---
name: OpenCode Configuration Notes
description: Decision-making, naming rules, and routing intent for OpenCode config
tags:
  - area/ea
  - kind/doc
  - status/stable
date_created: 2026-04-07
date_updated: 2026-04-18
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
| 2 | `2-gpt` | GPT-5.4 (high reasoning, low verbosity) | OpenAI |
| 3 | `3-glm` | GLM 5.1 (thinking enabled) | zai-coding-plan |

### Disabled primary agents (parked)

| Key | Model | Provider |
|-----|-------|----------|
| `opus` | Claude Opus 4.6 (adaptive thinking, low effort) | Anthropic |
| `sonnet` | Claude Sonnet 4.6 (adaptive thinking, low effort) | Anthropic |

### Subagent handles

- `@kimi` — Kimi K2.5 Turbo via Fireworks AI
- `@glm` — GLM 5.1 via zai-coding-plan (thinking enabled)
- `@gptmini` — GPT-5.4 Mini (low reasoning, low verbosity)
- `@gpthigh` — GPT-5.4 with high reasoning effort
- `@gptxhigh` — GPT-5.4 with xhigh reasoning effort
- `@worker` — GPT-5.4 general worker (medium reasoning)
- `@worker2` — GLM 5.1 worker (thinking enabled)
- `@worker3` — GPT-5.4 Mini worker
- `@gemini` — Gemini 3.1 Pro via OpenRouter
- `@flash` — Gemini 3 Flash via OpenRouter
- `@minimax` — MiniMax 2.7 via OpenRouter (parked alternative)
- `@grok` — Grok 4.20 Beta via OpenRouter (parked)
- `@mimo` — Xiaomi Mimo V2 Pro via OpenRouter (parked)

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
- Keep OpenRouter (`moonshotai/kimi-k2.5:nitro`) registered as `kimi-or` fallback for when Fireworks is unavailable

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
| `fireworks-ai` | `1-kimi`, `kimi` | Primary Kimi K2.5 Turbo route |
| `openai` | `2-gpt`, `gptmini`, `gpthigh`, `gptxhigh`, `worker`, `worker3` | Native GPT route |
| `zai-coding-plan` | `3-glm`, `glm`, `worker2` | Primary GLM route |
| `anthropic` | `opus`, `sonnet` (disabled) | Native Claude route |
| `openrouter` | `gemini`, `flash`, plus parked `grok`/`mimo`/`minimax`/`kimi-or` | OpenRouter for Gemini and Grok-class fallbacks |
| `lmstudio` | `gemma` (disabled) | Local offline route |
| `opencode` (Zen) | parked `gemini-zen`/`flash-zen`/`glm-zen`/`mini-zen` | Zen fallback pool |

## Updating skills

When we update and/or change these configurations, they impact our skills such as:

- `dot_config/ai_templates/skills/devtools/delegate-to-sub/SKILL.md` — subagent delegation matrix (lineage: `use-subagents` → `delegate` → `delegate-to-sub`)
- `dot_config/ai_templates/skills/devtools/headless/references/opencode/MetaSkill.md` — headless OpenCode invocation reference (lineage: `run-oc` → `headless-opencode` → folded into the `headless` meta-skill)

**IMPORTANT**: Always update these skills in order to avoid drift.

### Checkpoint: Update delegate skill

When primary agents change (enabled/disabled, reordered, or renamed), you **must** update the delegate skill to match:

1. Update the Matrix section with current primary agents and their characteristics
2. Update the Review Workflow section to reference correct agent keys
3. Ensure the 2-pass, 3-pass, and 4-pass review sequences use active agents only

### Checkpoint: Validate justfile QA recipes

The `justfile` contains QA smoke test recipes (`ocqa-*`) that reference agent names. When agents change, validate and update:

1. **Active primary agents** — Ensure `ocqa-<agent>` recipes use correct numbered prefixes (e.g., `ocqa-glm` should use `--agent 3-glm` not `4-glm`)
2. **Disabled agents** — Comment out or remove recipes for disabled agents (e.g., `build` agent is disabled, so `ocqa-build` should not be in the main `opencode-qa` recipe)
3. **Agent name consistency** — Ensure recipe names match actual agent keys (e.g., `flash-or` and `gemini-or` don't exist; use `flash` and `gemini`)
4. **Main QA sweep** — Update the `opencode-qa` recipe to only call active agent tests

Current QA recipes to maintain:
- `ocqa-kimi` → tests `1-kimi`
- `ocqa-gpt` → tests `2-gpt`
- `ocqa-glm` → tests `3-glm`
- `ocqa-gptmini` → tests `gptmini` (small model)
- `ocqa-claude-haiku` → tests Claude via `claude` CLI
- `ocqa-gemini` → tests `gemini` subagent
- `ocqa-flash` → tests `flash` subagent 

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
