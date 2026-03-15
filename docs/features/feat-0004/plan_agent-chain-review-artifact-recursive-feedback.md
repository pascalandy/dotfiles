---
status: proposed
owners:
  - @askpascalandy
created: 2026-03-11
---

# Agent Chain Review Artifact Recursive Feedback

## Participants

- **CEO (User)** — Initiates ideas, reviews final plans, approves or requests additional rounds.
- **Product Manager (PM)** — Strategic ownership across the product lifecycle. Defines vision, roadmap, market positioning, and business outcomes. Works across engineering, design, marketing, sales, and executives. Sole role that mutates the plan.
- **Reviewer A/B/C** — Independent reviewers that provide feedback via review files. Never edit the plan directly.

## Abstract

Redesign the `plan-review-3-rounds` workflow so reviewers never edit the plan directly. Each reviewer pass must create a standalone `review-{reviewer}-r{round}-{timestamp}-{suffix}.md` file next to the plan. The Product Manager (PM) becomes the sole role that mutates the plan: it reads the current plan plus all pending review files in the same feature directory, consolidates the feedback into the plan, updates `## Open Question and Decisions` as the durable decision log, clears the review file content and signs it with "Plan updated [date/time]", and then hands off to the commit step.

## Motivation

The current workflow stores reviewer feedback inline inside the plan. That works for a few rounds, but it mixes temporary critique with durable decisions and makes recursive feedback harder to control. Over many rounds, the same ideas can resurface repeatedly because the workflow does not cleanly separate:

- temporary review artifacts
- durable product decisions
- canonical plan state

The new design makes the plan the only durable memory. Reviewer outputs become temporary files that are consumed and cleared by the Product Manager. This should make the loop more deterministic, reduce repeated issues, and make `## Open Question and Decisions` the canonical record of what was considered, accepted, or rejected.

## Non-Goals

- **NG_01:** Do not change the overall round structure of `plan-review-3-rounds`.
- **NG_02:** Do not let reviewers edit the plan directly anymore.
- **NG_03:** Do not introduce cross-feature review discovery; review collection stays local to the active feature directory.
- **NG_04:** Do not keep review files after PM consolidation; delete them (git history is the audit trail).
- **NG_05:** Do not move durable reviewer memory into subagent session state; the plan remains the durable memory.

## Use Cases

### UC_01 — Reviewer produces independent critique artifact

**Actor:** Reviewer agent

**Scenario:** A review pass is executed for a plan in `docs/features/feat-0004/`.

**Expected Outcome:** The reviewer reads the plan from disk, creates a new `review-{reviewer}-r{round}-{timestamp}-{suffix}.md` file in `docs/features/feat-0004/`, and returns a handoff that identifies both the plan and review file.

### UC_02 — Reviewer has no material feedback

**Actor:** Reviewer agent

**Scenario:** The reviewer finds no additional issues.

**Expected Outcome:** The reviewer still creates a new review file and records a minimal no-op message such as `Nothing to add. Looks good to me.`.

### UC_03 — Product Manager consolidates multiple review files

**Actor:** Product Manager agent

**Scenario:** The feature directory contains several pending review files.

**Expected Outcome:** The PM reads the plan and all review files in that directory, consolidates all useful feedback into the plan, updates `## Open Question and Decisions`, clears each review file content and signs with "Plan updated [date/time]", and returns a consolidation handoff.

### UC_04 — Durable decision log prevents repeated feedback churn

**Actor:** Future reviewer agent

**Scenario:** A future reviewer evaluates a plan after multiple earlier review rounds were already consolidated by the PM.

**Expected Outcome:** The current plan state, especially `## Open Question and Decisions`, already reflects prior considered ideas so the reviewer works from the latest durable decisions rather than reintroducing already-processed feedback.

### UC_05 — Commit captures consolidation plus cleared review files

**Actor:** Commit agent

**Scenario:** The PM has updated the plan and cleared/signed review files.

**Expected Outcome:** The commit includes the updated plan and the cleared review files together as one audit snapshot.

### UC_06 — CEO provides review feedback

**Actor:** CEO (User)

**Scenario:** The CEO reviews the plan and provides feedback.

**Expected Outcome:** The CEO creates a `review-ceo-r{round}.md` file with feedback. The PM processes it like any other review.

## Functional Requirements

- **REQ_01:** The system must require `plan-reviewer` to create a new standalone review file in the same feature directory as `PLAN_FILE` instead of editing the plan directly. (covers: UC_01)
- **REQ_02:** The reviewer must always create a new review file, even when there are no material issues. (covers: UC_02)
- **REQ_03:** Review filenames must follow this pattern:
  - Reviewer: `review-{reviewer}-r{round}-{timestamp}-{suffix}.md`
    - Example: `review-a-r1-2026-03-15_12h30_abc.md`
  - CEO: `review-ceo-r{round}.md`
    - Example: `review-ceo-r1.md`, `review-ceo-r2.md`
  The resulting file must be written as `<feature-dir>/<generated>.md`. (covers: UC_01, UC_02)
- **REQ_04:** The Product Manager must treat the plan on disk as the source of truth and must read all review files currently present in the same feature directory as that plan. Review discovery must come from scanning that directory, not from trusting review paths listed in prior handoff text. (covers: UC_03)
- **REQ_05:** The Product Manager must process pending review files in deterministic lexicographic filename order. (covers: UC_03)
- **REQ_06:** The Product Manager must be the only role in this workflow allowed to modify the plan after initialization. (covers: UC_03, UC_04)
- **REQ_07:** The Product Manager must consolidate relevant feedback into the plan and keep `## Open Question and Decisions` as the durable decision log for chosen directions with concise inline rationale. (covers: UC_03, UC_04)
- **REQ_08:** After consolidation, the Product Manager must delete each review file (git history serves as the audit trail). (covers: UC_03, UC_05)
- **REQ_09:** The commit step must commit the updated plan and the cleared review files together, rather than committing only the plan file. (covers: UC_05)
- **REQ_10:** Review discovery and cleanup scope must be limited to the feature directory containing `PLAN_FILE`. (covers: UC_03)
- **REQ_11:** The workflow must preserve the existing rule that prior handoff text is locator metadata only and that agents must reread the current plan from disk before acting. (covers: UC_01, UC_03, UC_04)

## Acceptance Criteria

- **ACC_01:** When a review step runs for a plan in `docs/features/feat-0004/plan_*.md`, a new review file is created in `docs/features/feat-0004/` and the plan file itself is not modified by the reviewer. (validates: REQ_01, REQ_03)
- **ACC_02:** When the reviewer has no material issues, it still creates a new review file containing a minimal no-op review message. (validates: REQ_02, REQ_03)
- **ACC_03:** When the feature directory contains multiple pending review files, the PM discovers them by scanning the directory, processes them in lexicographic filename order, updates the plan accordingly, and clears/signs all those review files before handoff. (validates: REQ_04, REQ_05, REQ_07, REQ_08, REQ_10)
- **ACC_04:** After PM consolidation, the durable outcomes of review feedback are reflected in the plan's `## Open Question and Decisions` section using the chosen direction plus concise inline rationale, and consumed review files are cleared and signed. (validates: REQ_06, REQ_07, REQ_08)
- **ACC_05:** The commit step can create a commit that includes both the modified plan and the cleared review files from that feature directory. (validates: REQ_09)
- **ACC_06:** Agents continue to use handoff text only to locate `PLAN_FILE` and reread the current plan from disk before acting. (validates: REQ_11)

## Open Question and Decisions

**QST_01:** Should the workflow later support multiple plan files per feature directory?
- **DECISION:** No for this redesign. Scope review collection and cleanup to the active feature directory that contains the single current plan file. RATIONALE: The intended workflow assumes one canonical plan per feature directory. Supporting multiple plan files would complicate review routing and is unnecessary for this iteration. (2026-03-15)

**QST_02:** Should the PM trust handoff-listed review paths or discover reviews from disk?
- **DECISION:** The PM must ignore handoff-listed review paths and discover pending reviews by scanning the feature directory that contains `PLAN_FILE`. RATIONALE: Handoff text is locator metadata only. Directory-local discovery keeps the on-disk state authoritative and avoids stale or partial handoff data becoming a second source of truth. (2026-03-15)

**QST_03:** What should happen to review files after PM consolidation?
- **DECISION:** The PM should delete each review file after consolidation. Git history serves as the audit trail. RATIONALE: Deleting keeps the feature directory clean. Git history preserves the audit trail of what was reviewed and when. (2026-03-15)

**QST_04:** In what order should the PM process multiple pending review files?
- **DECISION:** Process them in lexicographic filename order. RATIONALE: The timestamp-based filename convention already gives a natural stable order, and lexicographic sorting is easy to explain and implement. (2026-03-15)

**QST_05:** Should the commit step verify that review-file clearing actually happened before committing?
- **DECISION:** No additional clearing verification is required in the commit step for this iteration. RATIONALE: The commit step should stay simple and commit the resulting git state rather than adding extra workflow policing that is not needed right now. (2026-03-15)

## Assumptions / Dependencies

- The workflow continues to use one feature directory per plan, such as `docs/features/feat-0004/`.
- `plan-review-3-rounds` remains a sequential chain.
- `plan-init`, `plan-reviewer`, `plan-product-manager`, and `plan-commit` continue to communicate by structured handoff blocks.
- The PM treats the feature directory containing `PLAN_FILE` as the sole discovery scope for pending reviews.
- Review file generation may rely on `bash` because the filename command is shell-based.

## File Contract

### Plan file

- Lives in a feature directory such as `docs/features/feat-0004/`
- Remains the canonical durable artifact
- Contains `## Open Question and Decisions` as the durable decision ledger

### Review file

- Must live in the same feature directory as the plan
- Must be named `review-{reviewer}-r{round}-{timestamp}-{suffix}.md` (reviewers) or `review-ceo-r{round}.md` (CEO)
- Must always be created by the reviewer, even for no-op reviews
- Is part of the PM's local input queue regardless of whether it is substantive, stale, empty, or malformed
- Is deleted by the PM after consolidation (git history is the audit trail)

## Handoff Contract *(add-on)*

### Reviewer handoff

The reviewer should return a block shaped like:

```text
PLAN_FILE: <repo-relative path>
REVIEW_FILE: <repo-relative path>
ROUND: <number from the prompt>
STEP: review
REVIEW_STATUS: created
HANDOFF: pm
SUMMARY: <one concise sentence>
```

### Product Manager handoff

The Product Manager should return a block shaped like:

```text
PLAN_FILE: <repo-relative path>
ROUND: <number from the prompt>
STEP: pm
PLAN_STATUS: revised | unchanged
REVIEWS_CONSUMED: <number>
HANDOFF: commit
SUMMARY: <one concise sentence>
```

### Commit handoff

The commit agent should return a block shaped like:

```text
PLAN_FILE: <repo-relative path>
ROUND: <number from the prompt>
STEP: commit
PLAN_STATUS: committed | skipped
HANDOFF: <exact value requested in the prompt>
COMMIT_MESSAGE: <message used, or none>
COMMIT_SHA: <short sha, or none>
SUMMARY: <one concise sentence>
```

## Solution Approach

**Target Files:**
- `extensions/agent-chain.ts`
- `.pi/agents/agent-chain.yaml`
- `.pi/agents/plan-reviewer.md`
- `.pi/agents/plan-product-manager.md`
- `.pi/agents/plan-commit.md`
- `docs/features/feat_template.md`

**Architecture & Flow:**
- Keep the current chain executor model in `extensions/agent-chain.ts`.
- Redesign the planning workflow contracts so reviewer output becomes a file artifact, not an inline plan edit.
- Treat the plan as the only durable memory layer.
- Treat all review files in the active feature directory as the PM input queue.
- After PM consolidation, delete each review file (git history is the audit trail).

**Key Changes:**
- Update reviewer persona instructions to create standalone review files and never edit the plan.
- Update PM persona instructions to gather all directory-local review files, consolidate them into the plan, then clear and sign each file.
- Update commit persona instructions so it commits plan changes plus cleared review files.
- Update `agent-chain.yaml` prompts to pass the right expectations and handoff fields.
- Tighten the feature template language so `Open Question and Decisions` records the chosen direction with concise inline rationale.

**Risks & Sequencing:**
- First lock the workflow contract in docs so persona changes stay aligned.
- Then update reviewer and PM personas together; changing only one side would break the loop.
- Update commit behavior after PM clearing behavior is defined, otherwise the audit step will still assume plan-only commits.
- Only after persona/prompt alignment should any extension-level observability or polish be considered.
