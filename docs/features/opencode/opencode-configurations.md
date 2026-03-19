# Open Questions & Decisions (OpenCode)

Source: `dot_config/opencode/opencode.json.tmpl`

## Mental model to select which agent for the task

Main = models I use most

Reviewers = second opinions

Small/local = lightweight options

Parked = documented but not currently in rotation

### Main

- `build` -> GPT-5.4
- `@gpt` -> GPT-5.4
- `@minimax` -> MiniMax M2.7 via OpenRouter (default agent)

### Disabled

- `general` -> built-in catch-all subagent
- `plan` -> GPT-5.4 planning preset

### Reviewers

- `@grok` -> Grok 4.20 via OpenRouter
- `@gemini-or` -> Gemini 3.1 Pro via OpenRouter
- `@flash-or` -> Gemini 3 Flash via OpenRouter
- `@glm-zen` -> GLM 5 via Zen
- `@gemini-zen` -> Gemini 3.1 Pro via Zen
- `@flash-zen` -> Gemini 3 Flash via Zen

### Also configured

- `@kimi` -> Kimi 2.5 Turbo via Fireworks

### Subagents

- `@agtmini`
- `@agttiny`

Rules:
- These are subagents and must stay provider agnostic in their names.
- These two are reserved sub-agent handles.
- Their names must stay exactly `agtmini` and `agttiny`.
- If either name changes in config, update this note deliberately and treat it as a breaking workflow change.

### Parked

- `@kimi-zen`
- `@opus`
- `@qwen`
- `@mini-zen`
- `@kimi-oc`

## Defaults

- Default agent = `minimax` `[[2026-03-18]]`
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

- Use Zen for GLM 5. Reason: direct ZAI does not give me GLM 5 `[[2026-03-14]]`
- Keep direct ZAI access (plan) for GLM 4.7.

## Local model usage

- Keep one local LM Studio model.
- Qwen is my local small-task option.

## Claude usage

Keep Opus documented, but parked for now. 
Reason: I do not currently have an Anthropic plan `[[2026-03-14]]`

## Issues with Gemini zen

Hi there!

I'm running into an issue with Gemini models in OpenCode. When I try to use gemini-3-flash, gemini-3-pro through the Zen integration, I keep getting "Unauthorized" message errors — even though they're ENABLED on my Zen account.

The weird part is that other models like Minimax and GLM5 work fine. It's only the Gemini family that seems to have this problem. actually on day one I configured Gemini 3 it worked. And then when I tried with Gemini 3.1 Pro, I started to have this error. and since then the Gemini models do not work.

I also check your FAQ and there's nothing about this subject. 

Any idea what's going on?

Thanks!
Pascal