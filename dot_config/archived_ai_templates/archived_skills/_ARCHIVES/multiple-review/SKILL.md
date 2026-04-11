---
name: multiple-review
description: Use this skill whenever the user wants multiple AI assistants consulted from the current session. Trigger on requests like "use council," "get more opinions," "cross-check this plan," "compare what other assistants think," "ask Codex and Kilo Code," or any request to reconcile advice from more than one external assistant. Council packages one question, sends it to the selected CLI assistants in headless mode, then returns a synthesis. If the user names specific assistants, use those. Otherwise use the currently configured runners.
compatibility: Requires working local CLI runners for the assistants you choose. Start with Codex CLI and Kilo Code CLI. Use local headless workflows, not provider SDKs or the archived Python workflow.
---

# Council (multiple-review)

Use Council when the user wants outside opinions, not outside ownership. The invoking agent still decides what to trust, what to reject, and what to do next.

Council is about the method: ask several assistants the same focused question, compare the answers, and return one recommendation. It is not defined by a permanent list of assistant names.

## Purpose

Use Council to:
- gather several viewpoints on one question
- surface blind spots, risks, and tradeoffs
- compare disagreement before taking action
- keep the human in one session while consulting other assistants

## Default behavior

If the user names assistants, use those assistants.

If the user asks for Council in general terms, use the currently configured runners. Today, the default runners are:
- Codex CLI
- Kilo Code CLI

Treat those runners as the current setup, not the definition of Council.
Keep assistant-specific setup brief. Council should explain the comparison pattern first and the current runners second.

If the user explicitly asks for one assistant, respect that. If only one runner is available, continue with one and say so.

Examples:
- "Use council to review this plan."
- "Cross-check this refactor with other assistants."
- "Ask Codex and Kilo Code what they think."
- "Get more opinions on this refactor."
- "Cross-check my approach with the council."
- "Ask Codex only."
- "Ask Kilo Code only."

## Workflow

1. Generate a prompt that will generate the most optimal review
  - Use the same prompt for each reviewers
2. Choose the assistants based on the user's request and the available runners
3. Build one focused context package
4. Use runner-specific instructions when they exist
5. Send the same package to each selected assistant headlessly
6. Present each response under a clear label
7. Reconcile the answers
8. State the invoking agent's recommendation

Keep the workflow simple. Council is a comparison tool, not a routing system

## Context packaging

Send the smallest useful context

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

## Runner guidance

### Codex CLI

```bash
codex -m gpt-5.4 -c 'model_reasoning_effort="xhigh"' -a never exec -s read-only \
  "Tell me what I should know about this repo within two or three sentences."
```

See all detail by loading the skill: `headless-codex`

### Gemini (via kilo)

```bash
kilo run "Tell me what I should know about this repo within two or three sentences." \
-m kilo/google/gemini-3.1-pro-preview --variant high
```

## Prompt framing

Use wording like:

> Give a precise engineering second opinion. Focus on likely root cause, hidden risks, and the safest next step. Be concise.
> Review this plan as an independent coding assistant. Focus on tradeoffs, blind spots, and the most defensible next action. Be direct and actionable.

## Output format

Use this structure:

```text
## Council question
- What we asked

## Assistant opinions
### Codex CLI
<summary or quoted answer>

### Kilo Code CLI
<summary or quoted answer>

## Reconciliation
- Where they agree
- Where they differ
- What matters most

## Recommendation
- What I recommend next
```

If the user asked for one model only, omit the other section.

## Reliability rules

- Default to the currently configured runners unless the user specifies otherwise.
- Stay read-only unless the user explicitly wants more than advice.
- If one runner fails, continue with the other and say what failed.
- If both succeed, compare substance, not tone.
- Do not force agreement. If the assistants disagree, explain the disagreement.
- Call out weak reasoning, missing context, or likely hallucinations.
- Keep the final recommendation short and specific.
