# OpenCode Configurations

Source: `dot_config/opencode/opencode.json.tmpl`

## Open Questions & Decisions

## Mental model to select which agent for the task

Main = models I use most

- Reviewers = second opinions
- Small/local = lightweight options
- Parked = documented but not currently in rotation

### Main

- `build` -> GPT-5.4
- `@gpt` -> GPT-5.4
- `@minimax` -> MiniMax M2.7 via OpenRouter (default agent)

### Disabled

- `plan`
- `general`

### Reviewers

- `@grok` -> Grok 4.20 via OpenRouter
- `@gemini-or` -> Gemini 3.1 Pro via OpenRouter
- `@glm-zen` -> GLM 5 via Zen
- `@gemini-zen` -> Gemini 3.1 Pro via Zen
- `@flash-zen` -> Gemini 3 Flash via Zen

### Subagents

- `@agtmini`
- `@agttiny`

Rules:
- subagents and must stay provider agnostic in their names.
- These two are reserved sub-agent handles.
- Their names must stay exactly `agtmini` and `agttiny`.
- If either name changes in config, update this note deliberately and treat it as a breaking workflow change.

### Parked

- `@kimi-zen`
- `@opus`
- `@glm47`
- `@qwen`
- `@mini-zen`
- `@kimi-oc`

## Defaults

- Default agent = `minimax`
  - Why: fast, capable, good daily driver
  - Fallback top-level model = GLM 5 via Zen
- `small_model` = Gemini 3 Flash via Zen

## GPT routing

Use direct OpenAI Plus plan for GPT.
- Do not route GPT through OpenRouter, Zen, or another proxy.
- Keep GPT as the medium default.
- Use separate agents for higher effort levels (`gpthigh`, `gptxhigh`).

## Gemini routing

Two paths available:

- OpenRouter: `@gemini-or`, `@flash-or` (reliable, was the working path)
- Zen: `@gemini-zen`, `@flash-zen` (now enabled and working) `[[2026-03-16]]`

## Grok routing

- Use OpenRouter for Grok. Reason: the latest Grok is not available on Zen. `[[2026-03-14]]`

## GLM routing

- GLM5 used zen because ZAI does not give me GLM 5 `[[2026-03-14]]`
- Keep direct ZAI access (plan) for GLM 4.7.

## Local model usage

- Qwen is my local small-task option.

## Claude usage

Keep Opus documented, but parked for now. Reason: I do not currently have an Anthropic plan `[[2026-03-14]]`
