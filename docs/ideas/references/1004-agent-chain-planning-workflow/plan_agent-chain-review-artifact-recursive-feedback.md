---
status: proposed
owners:
  - @askpascalandy
created: 2026-03-11
tags:
  - area/ea
  - kind/project
  - status/close
---

# Agent Chain Review Artifact Recursive Feedback

## Abstract

Redesign the `plan-review-3-rounds` workflow so reviewers never edit the plan directly. Each reviewer pass must create a standalone `review_*.md` file next to the plan. The product owner becomes the sole role that mutates the plan: it reads the current plan plus all pending review files in the same feature directory, consolidates the feedback into the plan, updates `## Open Question and Decisions` as the durable decision log, deletes all consumed review files, and then hands off to the commit step.

## Motivation

Current workflow has reviewers editing plans directly, which:
- Creates merge conflicts when multiple reviewers edit simultaneously
- Makes it hard to track who suggested what change
- Loses the context of why changes were made
- Prevents independent parallel review

## Solution

Separate concerns:
1. **Reviewers** write standalone review artifacts
2. **Product Owner** consolidates and edits the plan
3. **Commit agent** implements the approved plan

## Workflow

```
User -> plan-init -> plan-reviewer-1 -> plan-product-manager -> plan-reviewer-2 -> plan-product-manager -> commit
                \              /                    \              /                    \
                 v            v                     v            v                     v
            review_001.md  review_002.md        review_003.md  review_004.md        (implementation)
```

## File Format

### Review File

```markdown
---
name: Review Round N
description: Review feedback for PLAN_FILE
tags:
  - area/ea
  - kind/review
  - status/open
---

# Review Round N

## Concerns

1. **[SEVERITY]** Concern description
   - Location: specific section or line
   - Suggested change: what to do instead

## Questions

1. Question that needs clarification

## Praises

1. What's working well
```

## Handoff Protocol

Each agent prints:
```text
PLAN_FILE: <path>
ROUND: <number>
STEP: <init|review|consolidate|commit>
STATUS: <created|reviewed|updated|implemented>
HANDOFF: <next-agent>
SUMMARY: <one sentence>
```

## Open Questions

1. How many review rounds before forcing a decision?
2. Should we support parallel review (multiple reviewers at once)?
3. What happens if reviewers disagree fundamentally?

## Decision Log

- **2026-03-11**: Reviewers must not edit plan directly (DECIDED)
- **2026-03-11**: Review files are temporary and deleted after consolidation (DECIDED)
- **2026-03-11**: PO is sole plan editor (DECIDED)
