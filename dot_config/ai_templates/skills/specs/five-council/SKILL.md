---
name: five-council
description: |
  Run a meaningful decision, tradeoff, plan, or idea through a five-model council inside OpenCode. Use when the user wants multiple independent perspectives, blind peer review, and a final recommendation. Mandatory triggers: "council this", "run the council", "war room this", "pressure-test this", "stress-test this", "debate this". Strong triggers only when paired with a real decision or tradeoff: "should I X or Y", "which option", "what would you do", "is this the right move", "validate this", "get multiple perspectives", "I can't decide", "I'm torn between". Do not trigger on trivia, simple yes or no questions, light preferences, or summarization requests.
metadata:
  author: Pascal Andy
---

# Five Council

Run one meaningful question through five fixed OpenCode advisors, then a blind peer-review round, then a chairman synthesis.

This is the OpenCode-native version of the original LLM Council workflow inspired by Andrej Karpathy's methodology. The goal is the same: multiple independent judgments, anonymous cross-examination, then a final recommendation that is stronger than any single answer.

The method is subject-agnostic. It should work for product questions, strategy, writing, positioning, code decisions, research directions, personal tradeoffs, and other judgment-heavy questions.

## When To Use It

Use the council when the user wants multiple viewpoints on a real question with judgment involved.

Good council prompts:

- `Council this: should I launch a workshop or a course first?`
- `Run the council on these two pricing options.`
- `Pressure-test this positioning before I commit to it.`
- `I'm torn between hiring and automating. Debate this.`
- `Which of these three product directions is strongest?`

Do not use the council for:

- factual lookups
- trivial preferences
- simple yes or no questions with no meaningful tradeoff
- summarization or drafting tasks where the user did not ask for judgment

If the question is too vague to frame responsibly, ask one clarifying question. Then proceed.

Do not start an interview loop. The right level of back-and-forth is:

- zero questions when the user already gave enough context
- one clarifying question when the framing is still too vague

Then convene the council.

## The Five Lenses

These are thinking styles, not job titles. Keep them distinct. The council works because these lenses naturally disagree.

### The Contrarian

Core question: `What fails here, and what is everyone else underestimating?`

- Assume there is a serious flaw. Try to find it.
- Push on hidden assumptions, downside risk, fragility, and self-deception.
- If the idea looks strong, go one level deeper and look for second-order failure modes.
- Do not waste time on upside or elegant theory. That is someone else's job.

### The First Principles Thinker

Core question: `What problem are we actually solving, stripped of inherited assumptions?`

- Ignore the default framing until you verify it deserves to exist.
- Rebuild the decision from goals, constraints, incentives, and underlying reality.
- Say plainly when the user is solving the wrong problem.
- Do not optimize the current plan if the premise itself is weak.

### The Expansionist

Core question: `What upside, leverage, or adjacent opportunity is being undervalued?`

- Look for asymmetric upside and larger plays hidden inside the current decision.
- Name growth paths, leverage points, and opportunities everyone else is discounting.
- Take the upside seriously even when it sounds ambitious.
- Do not spend your time on operational friction or risk management.

### The Outsider

Core question: `How does this read to someone with fresh eyes and no insider context?`

- React only to what is in front of you.
- Catch jargon, hidden context, weak framing, and curse-of-knowledge problems.
- Say what is confusing, unclear, overcomplicated, or unbelievable.
- Do not assume the user's background, audience, or internal context unless the framed question states it explicitly.

### The Executor

Core question: `What would you do on Monday morning, and what is the fastest path to learning?`

- Reduce the decision to action, sequencing, and validation.
- Prefer cheap tests, direct evidence, and the shortest path to reality.
- Call out plans that sound smart but have no crisp first step.
- Do not get lost in grand strategy if the next action is still muddy.

## Why These Five

These lenses create the intended tensions:

- Contrarian versus Expansionist: downside versus upside
- First Principles Thinker versus Executor: rethink the problem versus move the work
- Outsider versus everyone else: fresh eyes versus insider assumptions

If they all agree independently, that is a strong signal. If they clash, the clash itself is useful.

## Fixed OpenCode Roster

Use these exact five agents every time. The roster is fixed.

| OpenCode agent | Council role |
| --- | --- |
| `gpthigh` | The Contrarian |
| `2-opus` | The First Principles Thinker |
| `gemini` | The Expansionist |
| `1-kimi` | The Outsider |
| `1-kimi` | The Executor |

Do not change, add, remove, rename, or reshuffle seats, even if the user suggests alternate agents. If the user wants a different roster, that is a different skill.

## Execution Contract

Use one execution mode for the entire session.

- Primary mode: OpenCode subagents
- Fallback mode: headless `opencode run`

Rules:

- Prefer OpenCode subagents.
- Dispatch all five advisor seats in parallel in one turn.
- Dispatch all five blind-review seats in parallel in one turn.
- Use these exact `subagent_type` values: `1-kimi`, `2-opus`, `gpthigh`, `gemini`, `glm`.
- Use a fresh `1-kimi` subagent for the Outsider seat. Do not reuse the orchestrator voice as the Outsider.
- Keep one mode for the whole session. Do not mix subagent mode and headless mode across seats unless retrying is impossible otherwise.
- If mixed mode is unavoidable, record the transport mode per seat in the transcript.

Advisor and reviewer seats are packet evaluators only.

- They must not read files.
- They must not browse for additional context.
- They must not call tools.
- They must not search the web.
- They must not write or edit anything.

Each advisor seat receives only:

- its role name
- its seat briefing
- its OpenCode agent identity
- the framed question

Each blind-review seat receives only:

- its role name
- its seat briefing
- the framed question
- anonymized responses `A` through `E`

Do not pass prior transcripts, prior verdicts, or general workspace context into seat prompts unless the framed question explicitly quotes those materials.

## Headless Fallback

If OpenCode subagent dispatch is unavailable, use headless OpenCode CLI.

Use the same fixed roster:

- `opencode run --agent 1-kimi ...`
- `opencode run --agent 2-opus ...`
- `opencode run --agent gpthigh ...`
- `opencode run --agent gemini ...`
- `opencode run --agent glm ...`

Fallback rules:

- Use non-interactive execution.
- Prefer `--format json` when you need reliable capture.
- Pass the same prompt packet to every seat.
- Save one raw output per seat before parsing or summarizing it.
- Check exit codes explicitly.

Do not switch to headless mode for only one seat unless the primary mode failed and a retry in the same mode is impossible.

## Step 1: Gather Context and Frame the Question

Default to user-message-only framing.

Only pull in extra source material when the question clearly depends on it.

Examples of valid extra source material:

- files the user explicitly referenced
- notes, specs, docs, or links the user provided
- one or two clearly relevant files when the question depends on them

Keep extra reading minimal. Do not start a discovery loop if the question can already be framed responsibly from the user's message.

Do not read prior council transcripts by default. Only use a prior transcript when the user is continuing a previous council run or explicitly asks for follow-up on an earlier verdict. Never include a prior verdict in an advisor prompt.

Then write a framed question that includes:

1. the core decision or question
2. the options being weighed, if any
3. key facts from the user's message
4. key facts from the source material, if any were truly needed
5. meaningful constraints
6. what is at stake

Framing guardrails:

- keep it neutral
- add context, not opinion
- do not inject new options unless the user already implied them
- do not narrow the question in a way that hides the real tradeoff
- do not smuggle in a recommendation through phrasing

Save both of these for the transcript:

- the original user question
- the framed question

## Step 2: Convene the Five Advisors

Send the framed question to all five advisors in parallel.

Each advisor should:

- respond only from its assigned lens
- lean fully into that lens
- avoid balancing itself against other viewpoints
- stay between 90 and 180 words
- work only from the prompt packet it received

### Advisor Prompt Template

```text
You are [Council Role] on the Five Council.

Your OpenCode agent identity is [OpenCode agent name].

Seat briefing:
[paste the exact briefing for this role from the skill]

The question brought to the council:

---
[framed question]
---

Rules:
- Work only from this prompt packet.
- Do not inspect files, browse for more context, call tools, or edit anything.
- Do not try to be balanced.
- Do not mention your model name.

Respond from your perspective only. Be direct and specific. If the question is badly framed, say so from your seat's angle.

Keep your response between 90 and 180 words. No preamble. Go straight into the analysis.
```

If all five advisors independently say the question is ill-posed or aimed at the wrong problem, stop here. Report that the council recommends reframing instead of manufacturing a fake verdict.

## Step 3: Run Blind Peer Review

Take the five advisor responses and anonymize them as `Response A` through `Response E`.

Randomization rule:

- use any non-roster permutation
- do not preserve roster order
- do not sort alphabetically
- record the mapping only in the transcript

Then send the anonymized set to the same five agents again in parallel.

Each reviewer keeps its own seat lens during review. That means the Contrarian reviews like a Contrarian, the Executor reviews like an Executor, and so on.

Each reviewer answers:

1. Which response is strongest from your lens, and why?
2. Which response has the biggest blind spot from your lens, and what is it missing?
3. What did all five responses miss that the council should consider?

Keep each review between 60 and 120 words.

### Blind Review Prompt Template

```text
You are [Council Role] conducting blind peer review for a Five Council session.

Seat briefing:
[paste the exact briefing for this role from the skill]

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

Rules:
- Review from your seat's lens.
- Work only from this prompt packet.
- Do not inspect files, browse for more context, call tools, or edit anything.
- Do not guess authorship.

Answer these three questions:
1. Which response is strongest from your lens? Why?
2. Which response has the biggest blind spot from your lens? What is it missing?
3. What did all five responses miss that the council should consider?

Keep your review between 60 and 120 words. Be direct.
```

## Step 4: Synthesize the Verdict

The orchestrating assistant is the chairman by default.

Read:

- the framed question
- all five named advisor responses
- all five blind reviews

Then produce the final synthesis using this exact structure:

```markdown
## Where the Council Agrees

## Where the Council Clashes

## Blind Spots the Council Caught

## The Recommendation

## The One Thing to Do First
```

Synthesis rules:

- use evidence from the advisor seats and blind reviews
- cite supporting seats inline where useful
- do not drift into your own unsupported opinion
- surface real agreement where multiple seats converged independently
- surface real disagreement without smoothing it over
- let blind-review insights influence the verdict
- make a real recommendation
- do not end with `it depends`
- give exactly one concrete first action

The chairman may disagree with the majority if the minority reasoning is stronger.

## Step 5: Optional Artifacts

By default, return the verdict inline in the conversation.

Generate saved artifacts only when one of these is true:

- the user explicitly asks for a report or transcript
- the decision is important enough that a durable artifact is clearly useful

If artifacts are not needed, stop after the chairman synthesis.

If artifacts are needed, write them in the current working directory unless the user asked for a different path.

### Optional HTML Report

File name:

`five-council-report-[YYYYMMDD-HHMMSS].html`

Requirements:

- self-contained HTML
- inline CSS only
- system font stack
- white background
- subtle borders
- mobile-friendly layout
- collapsible sections using native `details` and `summary`

Use this structure:

1. original question
2. framed question
3. chairman verdict
4. agreement and disagreement visual
5. advisor responses
6. blind-review highlights
7. footer with timestamp and roster

Define agreement as two or more advisors independently reaching the same conclusion on the core decision. Define disagreement as materially different recommendations or materially different explanations of what matters most.

Use this minimal styling baseline:

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Five Council Report</title>
  <style>
    :root { --ink:#111827; --muted:#6b7280; --line:#e5e7eb; --panel:#ffffff; --bg:#f8fafc; --accent:#2563eb; }
    * { box-sizing:border-box; }
    body { margin:0; font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:var(--ink); background:var(--bg); }
    main { max-width:1040px; margin:0 auto; padding:32px 20px 64px; }
    .card { background:var(--panel); border:1px solid var(--line); border-radius:14px; padding:20px; margin:16px 0; }
    .grid { display:grid; gap:12px; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); }
    .muted { color:var(--muted); }
    summary { cursor:pointer; font-weight:600; }
  </style>
</head>
<body>
  <main>
    <!-- Fill with the required sections in the specified order -->
  </main>
</body>
</html>
```

Do not open the report automatically. Return the path. Only attempt local opening if the user explicitly asks.

### Optional Transcript

Write the transcript beside the HTML report when both are requested. If only a transcript is requested, write just the transcript.

File name:

`five-council-transcript-[YYYYMMDD-HHMMSS].md`

Use this structure:

```markdown
# Five Council Transcript

## Original Question

## Framed Question

## Roster

## Execution Mode

## Anonymization Mapping

## Advisor Responses

## Blind Reviews

## Council Verdict

## Failed Seats
```

`## Failed Seats` can say `None` when everything succeeded.

## Failure Handling

Treat any of these as failure:

- tool or transport error
- non-zero exit in headless mode
- empty response
- advisor response under 70 words
- blind review under 40 words
- response that clearly ignores the framed question or assigned seat

Suggested timeout budgets:

- advisors: 120 seconds each
- blind reviews: 90 seconds each

Retry policy:

- retry the same seat once with the same prompt packet and same execution mode
- if that still fails, record the failure in the transcript
- if one seat fails twice, continue with four seats and call out the missing seat in the verdict
- if two or more seats fail twice, stop and report the failure instead of pretending the council is complete

## Output Contract

Every council run must return:

- the council verdict inline
- whether any seat failed or retried

If artifacts were generated, also return:

- the artifact paths

Optional artifact filenames:

- `five-council-report-[timestamp].html`
- `five-council-transcript-[timestamp].md`

## Quality Bar

- Do not council trivia.
- Do not confuse number of voices with quality of reasoning.
- Do not let eloquence outrank substance.
- Do not skip the anonymized review round.
- Do not let old council verdicts leak into new advisor prompts.
- Keep the whole process pointed at helping the user decide what to do.
