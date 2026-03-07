---
name: council
description: Get second opinions from competing AI models (OpenAI, Google) via OpenRouter, without leaving Claude Code. IMPORTANT — This skill takes priority over gemini-api-dev and claude-developer-platform when the user wants an OPINION from another model, not to BUILD with that model's API. Trigger phrases — "get a second opinion", "ask Gemini", "ask GPT", "ask Codex", "consult Gemini", "consult GPT", "consult Codex", "get a few opinions", "council", "/council", "what would GPT say", "what would Gemini think", "consult [any model name]", or when the user asks to consult, ask, or get a perspective from another AI model on a task. Uses the council.py script via OpenRouter — never call Gemini or OpenAI APIs directly for council consultations.
---

# Council — Multi-Model Second Opinions

Consult competing AI models from inside Claude Code. One OpenRouter API key, every model.

## Setup

Requires `OPENROUTER_API_KEY` in environment or `~/.env` or project `.env`.

Get a key at https://openrouter.ai/keys

## Three Invocation Modes

### 1. "Get a second opinion" — Auto-routed

User says something like "get a second opinion on this bug" without naming a model.

**Workflow:**
1. Analyze the current conversation context
2. Classify the task into a category using the config keywords in [council_config.json](references/council_config.json)
3. Resolve the category to the default model from config
4. **Play back the plan before executing:**

```
Council Plan:
  1. Fix login redirect loop  →  openai/gpt-5.3-codex  [bug_fix]

Proceed?
```

5. Wait for user confirmation, then run:

```bash
python scripts/council.py consult --category bug_fix --context "FULL CONTEXT HERE"
```

6. Present the response, then synthesize: agree, push back, or cherry-pick the best parts

### 2. "Ask Gemini about this" — Explicit override

User names a specific model or provider.

**Trigger phrases:** "ask Gemini", "ask GPT", "ask Codex", "what would Gemini say"

**Provider shortcuts:**
- "Gemini" → `google/gemini-3.1-pro-preview`
- "GPT" / "Codex" / "OpenAI" → `openai/gpt-5.3-codex`
- "Flash" → `google/gemini-3-flash-preview`

```bash
python scripts/council.py consult --model google/gemini-3.1-pro-preview --context "CONTEXT"
```

### 3. "Get a few opinions" — Fan-out

User wants multiple perspectives at once.

**Trigger phrases:** "get a few opinions", "ask everyone", "what do the competitors think"

**Workflow:**
1. Classify each item if there's a laundry list
2. Play back the full plan:

```
Council Plan:
  1. Fix login redirect loop      →  openai/gpt-5.3-codex         [bug_fix]
  2. Redesign settings page       →  google/gemini-3.1-pro-preview [frontend]
  3. Add rate limiting strategy   →  openai/gpt-5.3-codex         [architecture]

Proceed? (y / edit / cancel)
```

3. Wait for confirmation
4. Execute each consultation (parallel where independent)
5. Present each response labeled clearly, then synthesize across all

For a single question fan-out (not a laundry list):

```bash
python scripts/council.py consult --fan-out --context "CONTEXT"
```

This sends to all models in the `fan_out` list and returns each response.

## Category Classification

Infer the category from conversation context using these mappings:

| Category | Routes to | Signals |
|---|---|---|
| `bug_fix` | OpenAI Codex | bug, fix, error, crash, debug, broken, failing |
| `frontend` | Gemini 3.1 Pro | UI, UX, design, CSS, React, component, layout, page |
| `architecture` | Claude Opus 4.6 | architecture, system design, schema, scale, patterns |
| `refactor` | OpenAI Codex | refactor, clean up, optimize, simplify, extract |
| `general` | Gemini 3.1 Pro | Default fallback for anything else |
| `quick_check` | Gemini 3.0 Flash | Quick, fast, simple verification |

## Context Packaging

When sending context to another model, include:
- The specific question or problem statement
- Relevant code snippets (keep it focused, not the entire codebase)
- What approaches have already been tried
- What kind of answer is needed (diagnosis, code fix, design opinion, etc.)

Do NOT send the entire conversation history. Extract and summarize the relevant parts.

## Synthesis Rules

After receiving a response from the council:
1. **Present the raw response** clearly labeled with the model name
2. **State agreement or disagreement** — don't just parrot the response
3. **If disagreeing**, explain why with specific reasoning
4. **If agreeing**, note any additions or refinements
5. **Execute the best approach** — Claude remains the executor

## Model Discovery

To check what's currently available on OpenRouter:

```bash
python scripts/council.py models
python scripts/council.py models --provider openai
python scripts/council.py models --provider google
```

Use this when the user asks "what models are available" or when updating the config with newer models.

## Config

View current config:

```bash
python scripts/council.py config
```

Config lives at [references/council_config.json](references/council_config.json). Edit directly to change default mappings, add providers, or update model IDs.