(recent at the top)

---

# to get: absurd_use_case_v2.md

## context
Read and understand what I'm trying to do.
docs/absurd/absurd_use_case.md

Read and understand what it can do:
docs/absurd/absurd_how_to.md

## problem

Okay, we still need to work on how we have to organize the prompts and the skill required.
and finally the agents that will run these. So based on the use case, we have clear child steps to follow.

I want you to look at these two skills
- compound-engineering
- superpowers

Then I want you to analyze what is the best sub-skill for each childs
Use the best pattern if needed. you can use ideas of one and or the other skills.

Ideally, the prompt for each child will be short. the prompt will say something like
The task at high level is X. load the skill Y and use the sub-skill Z to acomplish the task

## agent
for the actual agents load the skill : run-oc

## Model

When the main agent (`1-kimi`) needs to delegate work, use this skill to determine which sub-agent to call.

### Matrix

- **`1-kimi`** (Kimi K2.5 Turbo via Fireworks AI)
  - **Speed**: Fastest | **Cost**: Lowest | **Intelligence**: High
  - **Use for**: Default for everything. First-pass reviews, commits, quick edits, general tasks, exploration, research.

- **`2-opus`** (Claude Opus 4.6 via Anthropic)
  - **Speed**: Slow | **Cost**: High | **Intelligence**: Highest
  - **Use for**: Second-pass reviews. Complex architecture, hard problems requiring deep reasoning.

- **`gpthigh`** (GPT-5.4 High Reasoning via OpenAI)
  - **Speed**: Medium | **Cost**: Medium-high | **Intelligence**: Very high
  - **Use for**: Third-pass reviews. Different reasoning perspective—catches issues Opus misses.

- **`gemini`** (Gemini 3.1 Pro via OpenRouter)
  - **Speed**: Medium | **Cost**: Medium | **Intelligence**: High
  - **Use for**: Fourth-pass reviews only when user explicitly requests 4 rounds.

- **`glm`** (GLM 5.1 via zai-coding-plan)
  - **Speed**: Medium-fast | **Cost**: Low | **Intelligence**: High (coding-optimized)
  - **Use for**: Batch tasks, bulk operations, large-scale refactoring, heavy tasks where cost matters.

## GOAL:
Create a bonified version of the use case with all the details required
to create the actual absurd workflow. This will act as our specs.

export you work:
docs/absurd/absurd_use_case_v2.md

So before starting the work, let me know if you have any questions.

---

## to get : absurd_use_case-v1-high-level.md
Read and understand what I'm trying to do.
docs/absurd/absurd_use_case.md

Read and understand what it can do:
docs/absurd/absurd_how_to.md

So my goal here is to create a code factory engine so that every time I have a plan, I I can simply trigger my absurd workflow and it will implement a solid solution out of it.

I think I have a great use case but I want you to double check and make sure that it is not overkill and that I'm not forgetting anything. Of course, I know we will have to work on the prompts, but for now, let's think at these levels (delivery-* + childs).

your task is to review my use case.
load skill: "thinking"

Give me suggestions if needed. give me suggestion, make a case to keep or to remove a child step. When you have a suggestion, show me exactly what I have currently. what is your actual suggestion and your justification

use sub-agent @kimi from each thinking patterns


---

# follow up

docs/absurd/absurd_use_case.md

I'm really trying to understand the right lexic to use absurd. So, so far I do understand that.

queues:
delivery-orchestrator   ← task lives here (parent)
    delivery-build          ← implement-from-plan
    delivery-review         ← run-lsp-and-lint, review-diff, qa-branch
    delivery-ops            ← commit-branch, open-pull-request, request-greptile-review,
                            wait-for-ci, merge-when-green

child tasks:
- `implement-from-plan`
- `run-lsp-and-lint`
- `review-diff`
- `qa-branch`
- `commit-branch`
- `open-pull-request`
- `request-greptile-review`
- `wait-for-ci`
- `merge-when-green`

Concretely, a prompt management layer would look like:
prompts/
  implement-from-plan/
    v1.md          # stable system behavior + step-specific instructions
    v2.md
  review-diff/
    v1.md
  qa-branch/
    v1.md
  ...
prompt-config.toml  # maps step -> prompt version + model profile

---

# init to get: absurd_how_to.md

Read and deeply understand what Absurd is and can do:
https://earendil-works.github.io/absurd/

GOAL:
Build a skill markdown document for this release which includes code examples of every feature.

Create a detailed plan

then create a list that is checkable:

- [ ] Sequential go through every steps from the plan, and create a atomic list of tasks
- [ ] Sequential go through every tasks, determine all acceptance criteria for each tasks, make your due diligences, and update the work to get closer to the goal. Do not make mistake!

You can also take a look at the repo as well.
repo: https://github.com/earendil-works/absurd

finally export your work here:
/docs/absurd_draft.md
