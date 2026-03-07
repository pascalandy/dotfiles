---
name: council
description: Use this skill whenever the user wants a second opinion from another AI without leaving the current coding session. Trigger on requests like "use council," "ask Gemini and Codex," "get more opinions," "cross-check this plan," "what do Gemini and Codex think," or any request to reconcile Claude's view with other models. By default, consult both Gemini CLI and Codex CLI in headless mode, then synthesize the results. Use a single model only when the user asks for one on purpose.
compatibility: Requires working local `gemini` and `codex` CLIs. Run them headlessly. Do not use OpenRouter, provider SDKs, or the archived Python workflow.
---

# Council

Use Council when the user wants outside opinions, not outside ownership. Claude still decides what to trust, what to reject, and what to do next.

## Default behavior

By default, run both:
- kilo CLI
- codex CLI

Then compare their answers and give Claude's synthesis.

If the user explicitly asks for only one model, respect that.

Examples:
- "Use council to review this plan."
- "Ask Gemini and Codex what they think."
- "Get more opinions on this refactor."
- "Cross-check my approach with the council."
- "Ask Codex only."
- "Ask Gemini only."

## Workflow

1. Distill the real question.
2. Build one focused context package.
3. Send that package to Gemini and Codex headlessly.
4. Present each response under a clear label.
5. Reconcile the answers.
6. State Claude's recommendation.

Keep the workflow simple. Council is a comparison tool, not a routing system.

## Context packaging

Send the smallest useful context.

Include:
- the exact question
- relevant constraints
- the key snippet, command, error, or plan
- what has already been tried
- what kind of answer is wanted

Avoid:
- dumping the full conversation
- dumping the whole repo unless clearly needed
- vague prompts like "thoughts?"

A strong context package usually produces better answers than a broad repo scan.

## Command patterns

### Codex

load skill: $headless-codex

## Prompt framing


Use wording like:

> Give a precise engineering second opinion. Focus on likely root cause, hidden risks, and the safest next step. Be concise.
> Give a strategic second opinion. Focus on tradeoffs, blind spots, and whether the current direction seems sound. Be direct and actionable.

## Output format

Use this structure:

```text
## Council question
- What we asked

## Codex opinion
<summary or quoted answer>

## Gemini opinion
<summary or quoted answer>

## Reconciliation
- Where they agree
- Where they differ
- What matters most

## Claude recommendation
- What I recommend next
```

If the user asked for one model only, omit the other section.

## Reliability rules

- Default to both Gemini and Codex.
- Stay read-only unless the user explicitly wants more than advice.
- If one runner fails, continue with the other and say what failed.
- If both succeed, compare substance, not tone.
- Do not force agreement. If the models disagree, explain the disagreement.
- Keep the final recommendation short and specific.

## When not to use Council

Do not use Council when:
- the user wants Claude's answer only
- the user wants to build against Gemini, OpenAI, or OpenRouter APIs
- the user wants Codex or Gemini to become the primary executor
- another-model consultation adds no value
