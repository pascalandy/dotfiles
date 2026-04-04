# Absurd Use Case: End-to-End Development Workflow

## Goal

This document shows what a high-level, durable development workflow could look like with Absurd for a very common software-delivery path:

1. read plan and implement with red/green TDD
2. lsp / lint
3. code review
4. qa
5. commit all
6. open pr
7. pr review with Greptile
8. deploy and wait for ci
9. merge to main

The focus here is not code. The focus is:

- what the workflow looks like at a high level
- how prompts are managed across steps
- how model choice is decided per step
- how Absurd helps make the whole thing durable and resumable

## The high-level shape

The cleanest way to model this in Absurd is as one parent task that orchestrates a set of durable phases.

Suggested top-level task name:

- `deliver-change`

Suggested queues:

- `delivery-build` for implementation work
- `delivery-review` for review and qa work
- `delivery-ops` for git, PR, CI, and merge operations

Why split queues:

- implementation and review often want different concurrency profiles
- child-task waits should happen cross-queue, which aligns well with Absurd `0.3.0`
- operations such as PR creation, CI waiting, and merge gating are easier to isolate

## What the parent workflow is responsible for

The parent task is not where all detailed work happens.

The parent task should:

- load the plan and metadata for the change
- decide the execution order
- spawn child tasks on the right queues
- await the terminal result of each child task
- stop early on hard failures
- persist all decision points and artifacts
- wait durably for external events such as CI completion or Greptile feedback

At this level, the parent task is a release manager.

## What the child tasks are responsible for

Each major stage becomes one child task with its own prompt policy, model policy, acceptance criteria, and output contract.

Suggested child tasks:

- `implement-from-plan`
- `run-lsp-and-lint`
- `review-diff`
- `qa-branch`
- `commit-branch`
- `open-pull-request`
- `request-greptile-review`
- `wait-for-ci`
- `merge-when-green`

This is useful because each child task can fail, retry, sleep, or wait independently without losing the whole workflow.

## The workflow as an execution story

Here is what a typical run looks like from the outside.

### Phase 1: Read plan and implement with red/green TDD

The parent task starts by loading:

- the plan document
- branch metadata
- repository context
- acceptance criteria
- risk level

Then it spawns `implement-from-plan` on `delivery-build`.

That child task usually has internal checkpoints like:

- interpret plan
- identify slice 1
- write failing test
- implement minimal fix
- make test pass
- refactor safely
- repeat for remaining slices

What gets persisted:

- plan version used
- implementation strategy chosen
- tests added or changed
- files changed
- unresolved issues or tradeoffs

If the worker dies during implementation, Absurd resumes from the last durable checkpoint instead of restarting from zero.

### Phase 2: LSP / lint

After implementation succeeds, the parent spawns `run-lsp-and-lint` on `delivery-review`.

This phase is mostly deterministic.

Typical behavior:

- run LSP diagnostics
- run lint and formatting
- if fixable mechanically, fix and rerun
- if not fixable mechanically, invoke a model-guided repair substep

What gets persisted:

- tool outputs
- files auto-fixed
- remaining diagnostics
- pass/fail state

### Phase 3: Code review

Then the parent spawns `review-diff` on `delivery-review`.

This phase should behave like a reviewer, not like an implementer.

Expected output shape:

- findings ordered by severity
- impacted files or areas
- open risks
- explicit statement if no findings were found

If findings are found, the parent can either:

- fail the run and require human intervention
- or loop back into a fix-and-rerun branch

That loop is exactly where Absurd helps, because the workflow can re-enter review after a repair without losing the full execution history.

### Phase 4: QA

Then the parent spawns `qa-branch` on 0o0o

This is where you validate user-visible behavior, not just static correctness.

Typical behavior:

- run the app or targeted test surface
- execute a browser or user-flow check
- verify edge cases from the plan
- produce a ship/no-ship result

What gets persisted:

- scenarios tested
- failures found
- screenshots or browser artifacts if applicable
- final QA verdict

### Phase 5: Commit all

Once build, lint, review, and QA are acceptable, the parent spawns `commit-branch` on 0o0o

This phase should:

- inspect staged and unstaged changes
- generate a commit message aligned with repo style
- stage the right files
- create the commit
- verify the branch state afterward

What gets persisted:

- commit SHA
- commit message
- staged file list
- post-commit git status

### Phase 6: Open PR

Then the parent spawns `open-pull-request` on `delivery-ops`.

This phase should:

- inspect branch status relative to base
- decide whether push is needed
- push if needed
- create the PR
- produce the PR URL

What gets persisted:

- base branch
- branch name
- PR title
- PR body summary
- PR URL

### Phase 7: PR review with Greptile

Then the parent spawns `request-greptile-review`.

This is a good example of an external asynchronous system.

The task should:

- submit the PR for Greptile review
- record the request id or tracking metadata
- wait durably for the review result event

In Absurd terms, this is a natural event wait.

The task sleeps until one of these happens:

- Greptile returns no issues
- Greptile returns findings
- the request times out

What gets persisted:

- Greptile request metadata
- returned findings
- review disposition

### Phase 8: Deploy and wait for CI

Then the parent either triggers deploy directly or waits for the normal CI/deploy pipeline after PR creation or merge approval.

The child task `wait-for-ci` should:

- wait for about two minutes 
- fetch the current check state
- decide what checks matter
- wait for the terminal CI result
- If the CI needs more time, check every 30 seconds. 

This is also a durable wait problem.

Instead of polling in memory for hours, the task can:

- wake periodically
- or suspend until a GitHub webhook event is emitted into Absurd

What gets persisted:

- required checks
- latest CI state
- timestamps
- final green or red outcome

### Phase 9: Merge to main

Finally the parent spawns `merge-when-green`.

This phase should only run if all gates passed:

- implementation complete
- lint clean
- review acceptable
- QA acceptable
- PR open
- Greptile acceptable
- CI green

This phase should:

- verify the merge gate one last time
- merge the PR
- persist the merge commit or merge reference

At the end, the parent task can return a compact delivery summary.

---

## How prompt management should work

This is the part that matters most for your question.

The main mistake would be to treat prompts as ad hoc strings assembled at runtime with no versioning.

A better approach is:

- treat prompts as versioned workflow assets
- give each step a prompt contract
- persist which prompt version was used
- persist which model was selected
- persist the important artifacts that were fed into the prompt

## A practical prompt model

Each step should have three layers of prompt material.

### 1. Stable system behavior

This is the durable role definition for the phase.

Examples:

- implementation phase: act as a TDD implementer
- review phase: act as a strict reviewer focused on findings
- QA phase: act as a user-flow validator
- PR phase: act as a summarizer for reviewers

This layer changes rarely.

### 2. Step-specific instructions

This is where you say what the current step must do.

Examples:

- read this plan and implement the smallest red/green slice
- run lint and resolve only the concrete diagnostics
- review the current diff and return findings only
- review this PR and summarize actionable findings

This layer is specific to the workflow stage.

### 3. Runtime context

This is the concrete payload for the step.

Examples:

- plan content
- affected files
- test failures
- diff summary
- QA target URL
- PR URL
- CI check list

This layer changes every run.

## What should be versioned

For every AI-backed step, you want durable provenance.

Persist at least:

- prompt family name
- prompt version
- model profile name
- concrete model name
- important input artifacts
- expected output schema version

That way, months later, you can answer:

- which prompt produced this commit
- which model reviewed this diff
- why did the QA step decide to pass

## What a good prompt contract looks like

Each workflow phase should define four things.

### Input contract

What must be present before the step starts.

Examples:

- plan path
- repo status
- diff summary
- PR URL
- target environment URL

### Behavior contract

What the model is allowed to do.

Examples:

- implementation can edit code and run tests
- reviewer cannot modify code and must only produce findings
- PR summarizer cannot change code, only write title/body

### Output contract

What shape the step must return.

Examples:

- implementation summary plus changed files
- list of lint issues fixed and remaining
- review findings with severity and file references
- QA verdict and evidence

### Escalation contract

When the step must stop and ask for human input.

Examples:

- ambiguous plan
- conflicting review findings
- CI failure that looks environmental
- deploy gate blocked by missing approval

## How to choose models per step

The best pattern is to separate model policy from workflow logic.

Do not hardcode model names directly into the task logic.

Instead, define model profiles and let each phase choose a profile.

## Recommended model profiles

Suggested profiles:

- `builder-strong`
- `builder-fast`
- `reviewer-strong`
- `reviewer-cheap`
- `qa-browser`
- `ops-safe`
- `summarizer-fast`

Then map each profile to a concrete model in configuration.

That gives you two levers:

- workflow code chooses a profile by task type
- environment config resolves the profile to a real model

This is much easier to change than editing workflow logic everywhere.

## Example routing by phase

### Read plan and implement with TDD

Goal:

- deep reasoning
- repo awareness
- good code changes
- strong test judgment

Best profile:

- `builder-strong`

Typical concrete model choice:

- strongest coding model available in your stack

Why:

- this step has the highest complexity and the highest downstream blast radius

### LSP / lint

Goal:

- deterministic cleanup
- cheap iteration

Best profile:

- `builder-fast`

Typical concrete model choice:

- small or medium coding model only when auto-fix cannot handle it

Why:

- most of this step should be tooling-first, not model-first

### Code review

Goal:

- high-signal findings
- low false positives
- reviewer mindset

Best profile:

- `reviewer-strong`

Typical concrete model choice:

- strongest review-oriented model available

Why:

- bad review quality either blocks good code or misses bad code

### QA

Goal:

- tool use
- browser or user-flow reliability
- evidence production

Best profile:

- `qa-browser`

Typical concrete model choice:

- model that works well with browser/tool loops and concise reporting

Why:

- this is usually less about deep architecture and more about observation and execution

### Commit all

Goal:

- concise accurate summarization
- low creativity

Best profile:

- `summarizer-fast`

Typical concrete model choice:

- cheap, fast summarization model

Why:

- the hard work is already done

### Open PR

Goal:

- clear reviewer-facing communication
- branch-awareness

Best profile:

- `summarizer-fast`

or, if the change is risky:

- `reviewer-cheap` plus a stronger summarizer fallback

### PR review with Greptile

Goal:

- external second opinion

Model choice:

- not your concern inside the workflow if Greptile is the service doing the review
- your workflow should only manage submission, waiting, ingestion, and gating

### Deploy and wait for CI

Goal:

- safe operational decisions
- minimal hallucination risk

Best profile:

- `ops-safe`

Typical concrete model choice:

- conservative tool-using model, or no model at all if purely deterministic

Why:

- this phase should be mostly state-machine logic and tool checks

### Merge to main

Goal:

- strict gate enforcement

Best profile:

- `ops-safe`

Why:

- ideally this is mostly deterministic and policy-driven

## A good model selection rule

Choose the model based on the job, not based on a global favorite model.

Three questions are enough:

1. Is this step creative or mostly deterministic?
2. Is the cost of a bad answer high or low?
3. Does this step need deep reasoning, tool use, or just summarization?

That gives you the routing logic:

- deep code change: strongest builder
- deterministic cleanup: cheap fast builder or no model
- review: strongest reviewer
- browser validation: tool-centric QA model
- PR and commit copy: fast summarizer
- deploy and merge: conservative ops model or deterministic logic

## Recommended prompt and model matrix

| Phase | Prompt style | Output style | Best model profile | Retry posture |
|---|---|---|---|---|
| Read plan and implement | TDD implementer | changed files, tests, residual risks | `builder-strong` | retry with same profile, escalate on ambiguity |
| LSP / lint | diagnostics fixer | fixed issues, remaining blockers | `builder-fast` | retry automatically after fixes |
| Code review | findings-first reviewer | severity-ordered findings | `reviewer-strong` | retry on transient tool failure only |
| QA | user-flow validator | pass/fail plus evidence | `qa-browser` | retry on flaky environment, escalate on product failure |
| Commit all | concise summarizer | commit message and git result | `summarizer-fast` | retry on hook or staging failure |
| Open PR | reviewer-facing summarizer | PR title/body and URL | `summarizer-fast` | retry on network or auth failure |
| Greptile review | external review orchestrator | findings ingested and normalized | `ops-safe` | wait durably for event |
| Wait for CI | operational gate checker | check matrix and final gate | `ops-safe` | sleep and retry, or event wait |
| Merge to main | strict gate enforcer | merge result | `ops-safe` | retry only on transient platform failure |

## How Absurd helps with prompts specifically

Absurd is not choosing prompts for you. That is your policy layer.

What Absurd gives you is durable execution around prompt-driven work.

That means:

- if an implementation run crashes after writing tests, you do not lose that checkpoint
- if Greptile takes 20 minutes, you wait durably
- if CI takes an hour, you wait durably
- if QA needs to be rerun after a fix, the workflow can loop back cleanly
- if you later change a prompt family, you can version the step or normalize the returned artifact shape

In other words, Absurd does for prompt-driven engineering workflows what it already does for business workflows: it turns long, failure-prone, multi-stage processes into resumable state machines.

## How this should look operationally

At a human level, you would see something like this:

- one delivery task starts for a plan
- implementation runs and checkpoints each TDD slice
- lint runs and cleans up
- review runs and either passes or sends the workflow back for repair
- QA runs and records evidence
- commit and PR steps produce durable metadata
- Greptile review is submitted and awaited
- CI is awaited without a long-lived in-memory worker
- merge runs only if all gates are green

Everything important has a durable trail:

- which prompt family was used
- which model profile and concrete model were used
- which artifacts were fed in
- which findings were returned
- which gates passed or failed

## Recommended design decisions

If you wanted this to work well in practice, I would recommend:

1. Keep prompts versioned outside the workflow code.
2. Route by model profile, not concrete model name, inside workflow logic.
3. Persist prompt version and model metadata with every AI-backed step.
4. Keep review, QA, and ops phases separate from implementation.
5. Use cross-queue child waits for major phases.
6. Make deploy and merge mostly deterministic, not model-driven.
7. Treat external systems such as Greptile and CI as event sources, not synchronous calls.
8. Version step names when prompt output shape or artifact meaning changes.

## Final takeaway

At high level, the use case is not “Absurd writes code.”

The use case is:

- Absurd coordinates a classic dev workflow as a durable multi-phase delivery pipeline
- prompts are first-class workflow assets with versions and contracts
- model choice is a policy decision per phase
- long waits, retries, review loops, and external gates become durable instead of fragile

That is what this style of workflow should look like if you want it to stay understandable and operable over time.
