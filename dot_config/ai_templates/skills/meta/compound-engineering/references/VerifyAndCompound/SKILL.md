---
name: VerifyAndCompound
description: "Verify compound-engineering work after or around implementation by reviewing changes, validating behavior, resolving feedback, and capturing reusable knowledge. USE WHEN the request is to review, test, harden, document, or compound what was learned."
---

# VerifyAndCompound

VerifyAndCompound owns post-implementation quality and compounding. It works standalone or via the meta-skill router. Use it when the code exists or the branch is active and the main job is to review code, validate behavior, resolve follow-up work, or preserve reusable knowledge.

## Core Concept

Treat validation and compounding as first-class work. Reviewing a branch, reproducing a bug, resolving PR feedback, and documenting the learning are related but distinct steps, and each already has a focused skill in the pack.

## Workflow Routing

| User Intent | Load |
|---|---|
| Need code review, QA, browser validation, platform validation, or bug reproduction | `workflows/ReviewAndValidate.md` |
| Need to resolve review comments, manage todos, or report workflow issues | `workflows/ResolveFeedbackAndTrack.md` |
| Need changelogs, videos, copy polish, or reusable solution docs | `workflows/CaptureAndShare.md` |

## Output Format

Return a short routing decision with:

1. Selected workflow
2. Downstream skill path
3. Why this route fits the request
4. Expected artifact or next handoff

## Examples

```text
User: run a full review of this branch before I open the PR

Route:
- Workflow: `ReviewAndValidate`
- Downstream skill: `../ce-review/SKILL.md`
- Why: the branch exists and the priority is structured validation
- Expected artifact: findings report, safe autofixes where allowed, and residual risks
```

```text
User: write up the fix so the team does not rediscover it next month

Route:
- Workflow: `CaptureAndShare`
- Downstream skill: `../ce-compound/SKILL.md`
- Why: the implementation is done and the request is about preserving knowledge
- Expected artifact: solution document in `docs/solutions/`
```
