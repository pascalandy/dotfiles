---
name: five-council
description: |
  Run a meaningful decision, tradeoff, plan, or idea through a five-model council inside OpenCode. Use when the user wants multiple independent perspectives, blind peer review, and a final recommendation. Mandatory triggers: "council this", "run the council", "war room this", "pressure-test this", "stress-test this", "debate this". Strong triggers when paired with a real decision or tradeoff: "should I X or Y", "which option", "what would you do", "is this the right move", "validate this", "get multiple perspectives", "I can't decide", "I'm torn between". Do not trigger on trivial facts, simple yes/no questions, summarization requests, or low-stakes choices.
metadata:
  author: Pascal Andy
---

# Five Council

Pressure-test consequential questions through five fixed OpenCode advisors, then run a blind peer-review round, then synthesize a clear recommendation.

This is the OpenCode-native version of LLM Council. It uses OpenCode subagents first. If subagent dispatch is unavailable or the user explicitly wants headless execution, fall back to `opencode run --agent ...`.

## Use It For

Use the council when the user is making a decision where bad judgment is expensive.

Good council prompts:

- `Council this: should I launch a workshop or a course first?`
- `Run the council on these two pricing options.`
- `Pressure-test this positioning before I commit to it.`
- `I'm torn between hiring and automating. Debate this.`
- `Which of these three product directions is strongest?`

Skip the council for:

- factual lookups
- trivial preferences
- simple yes or no questions with no real tradeoff
- writing or summarization tasks where the user did not ask for judgment

If the question is too vague to frame responsibly, ask one clarifying question. Then proceed.

## Fixed Advisor Roster

Use these exact five agents every time unless the user explicitly changes the roster.

| OpenCode agent | Council role | Thinking style |
| --- | --- | --- |
| `gpthigh` | The Contrarian | hunts for fatal flaws, hidden assumptions, and downside risk |
| `2-opus` | The First Principles Thinker | strips the problem to fundamentals and rebuilds it from scratch |
| `gemini` | The Expansionist | looks for upside, leverage, and bigger adjacent opportunities |
| `1-kimi` | The Outsider | reacts with fresh eyes and catches confusion, jargon, and blind spots |
| `glm` | The Executor | reduces everything to what can actually be done next |

Keep this mapping fixed so outputs stay comparable across sessions.

## OpenCode Dispatch Rules

- Prefer OpenCode subagents.
- Dispatch all five advisor passes in parallel in one turn.
- Dispatch all five peer-review passes in parallel in one turn.
- Use these exact `subagent_type` values: `1-kimi`, `2-opus`, `gpthigh`, `gemini`, `glm`.
- Do not substitute `3-gpt`, `4-sonnet`, `worker`, `worker1`, `worker2`, or `worker3` unless the user explicitly changes the council roster.
- Use a fresh `1-kimi` subagent for the Outsider seat. Do not reuse the current conversation voice as that advisor.
- Keep the initial advisor responses independent. No advisor sees any other advisor output before the peer-review round.
- During peer review, anonymize the initial responses as `Response A` through `Response E` and randomize the mapping each session.
- Reveal the anonymization mapping only in the transcript, never in the blind review prompt.

## Headless Fallback

If OpenCode subagent dispatch is unavailable, use headless OpenCode CLI.

- Run `opencode run --agent ...` once per advisor.
- Run the five advisor calls in parallel.
- Save each advisor result to a separate scratch file or variable before the peer-review round.
- Repeat the same pattern for the blind review round.

Use the same fixed roster in headless mode:

- `opencode run --agent 1-kimi ...`
- `opencode run --agent 2-opus ...`
- `opencode run --agent gpthigh ...`
- `opencode run --agent gemini ...`
- `opencode run --agent glm ...`

## Step 1: Gather Context and Frame the Question

Before dispatching the council, do a fast context pass.

Look for the 2-5 files that would materially improve the advisors' judgment:

- `AGENTS.md`
- `CLAUDE.md` or `claude.md`
- `README.md`
- `memory/` notes
- relevant docs under `docs/`
- files the user referenced or attached
- recent `five-council-transcript-*.md` or `council-transcript-*.md` files
- any obviously relevant project artifacts for the decision at hand

Use `Glob` and `Read` for this. Move quickly. Do not spend more than about 30 seconds gathering context.

Then write a framed question that includes:

1. the core decision or question
2. the options being weighed, if any
3. key facts from the user message
4. key facts from the workspace
5. meaningful constraints
6. what is at stake

Keep the framed question neutral. Add context. Do not add your opinion.

Save both of these for the transcript:

- the user's original question
- the framed question

## Step 2: Convene the Five Advisors

Send the framed question to all five advisors in parallel.

Each advisor should:

- answer from its assigned thinking style
- lean fully into that style
- stay direct and specific
- avoid balancing itself against other viewpoints
- keep the response between 150 and 300 words

### Advisor Prompt Template

```text
You are [Council Role] on the Five Council.

Your OpenCode agent identity is [OpenCode agent name].
Your thinking style: [thinking style from the roster above]

A user has brought this question to the council:

---
[framed question]
---

Respond from your perspective only. Be direct and specific. Lean fully into your assigned angle. Do not try to be balanced. Do not mention your model name. The synthesis happens later.

Keep your response between 150 and 300 words. No preamble. Go straight into the analysis.
```

## Step 3: Run Blind Peer Review

Collect the five advisor responses. Randomize them as `Response A` through `Response E`.

Then send the anonymized set to the same five OpenCode agents again in parallel.

Each reviewer answers three questions:

1. Which response is strongest, and why?
2. Which response has the biggest blind spot, and what is it missing?
3. What did all five responses miss that the council should consider?

Each review should stay under 200 words.

### Peer Review Prompt Template

```text
You are conducting blind peer review for a Five Council session.

The question brought to the council:

---
[framed question]
---

Five advisors answered independently. Their responses are anonymized below.

**Response A**
[response]

**Response B**
[response]

**Response C**
[response]

**Response D**
[response]

**Response E**
[response]

Evaluate the responses on reasoning quality, specificity, usefulness, and what they miss. Do not guess authorship.

Answer these three questions:
1. Which response is the strongest? Why?
2. Which response has the biggest blind spot? What is it missing?
3. What did all five responses miss that the council should consider?

Keep your review under 200 words. Be direct.
```

## Step 4: Synthesize the Verdict

The orchestrating assistant is the chairman by default. Read:

- the framed question
- all five named advisor responses
- all five peer reviews

Then produce a final synthesis using this exact structure:

```markdown
## Where the Council Agrees

## Where the Council Clashes

## Blind Spots the Council Caught

## The Recommendation

## The One Thing to Do First
```

Rules for the synthesis:

- Surface genuine agreement where multiple advisors converged independently.
- Surface genuine disagreements without smoothing them over.
- Pull blind spots from the peer-review round, not just the initial takes.
- Make a real recommendation. Do not end with `it depends`.
- Give one concrete first action, not a backlog.

If the reasoning supports it, the synthesis can side with a minority view.

## Step 5: Generate the HTML Report

Write a self-contained HTML report in the workspace root by default.

File name:

`five-council-report-[YYYYMMDD-HHMMSS].html`

Requirements:

- inline CSS only
- clean white background
- system font stack
- subtle borders and soft accent colors
- easy to scan on desktop and mobile
- collapsible sections implemented with native `details` and `summary`

The report should contain:

1. the original question
2. the framed question
3. the chairman verdict prominently near the top
4. an agreement and disagreement visual
5. collapsible sections for the five advisor responses
6. a collapsible section for peer-review highlights
7. a footer with timestamp and council roster

For the agreement and disagreement visual, keep it simple. A compact table or card grid is enough. Show:

- advisor
- role
- primary takeaway
- stance or emphasis

If local file opening is available, open the HTML report after generating it. Otherwise, return the path clearly.

## Step 6: Save the Full Transcript

Write the full transcript beside the HTML report.

File name:

`five-council-transcript-[YYYYMMDD-HHMMSS].md`

Include:

- original question
- framed question
- the roster mapping
- anonymization mapping for `Response A` through `Response E`
- all five advisor responses
- all five peer reviews
- the final synthesis

This transcript is the durable artifact for future follow-up runs.

## Output Contract

Every council session should produce two files unless the user explicitly asks for a lighter run:

- `five-council-report-[timestamp].html`
- `five-council-transcript-[timestamp].md`

After generating them, give the user:

- the verdict in a short summary
- the file paths
- whether the report was opened locally

## Failure Handling

- If one advisor fails, retry that seat once with the same agent.
- If that retry fails, continue with four responses and clearly mark the missing seat in the transcript and verdict.
- If two or more advisors fail, stop and report the failure instead of pretending the council is complete.
- If a peer-review pass fails, retry once. If it still fails, continue and note the missing review.

## Quality Bar

- Do not council trivia.
- Do not confuse number of voices with quality of reasoning.
- Do not let the most eloquent response dominate if the argument is weak.
- Do not skip the anonymized review round. That is where many of the best insights appear.
- Keep the council focused on helping the user decide what to do.
