---
name: pa-postmortem
description: Multi-mode postmortem skill for reverse-engineering sessions, writing blameless incident reviews, and capturing durable feedback from completed work. USE WHEN postmortem, lessons learned, what should we remember, reverse engineer the session, review what we did together, blameless incident review, incident postmortem, 5 whys, feedback capture, capture lessons from this fix, what went wrong, what did we discover, how should we write this down.
keywords: [postmortem, lessons-learned, session-review, incident-review, feedback-capture, reverse-engineer, blameless, five-whys, root-cause, write-down-postmortem]
---

# Postmortem

> Three distinct postmortem modes in one skill: session review, incident review, and feedback capture. Route to the right mode automatically, then save the final result in the active project with `write-down-postmortem`.

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

## The Problem

"Postmortem" can mean different things.

- Sometimes the user wants to reverse-engineer a conversation and preserve what matters.
- Sometimes they need a blameless incident review with impact, timeline, causes, and follow-up actions.
- Sometimes they already finished the work and only want the durable lessons and feedback.

Without routing, these use cases collapse into one vague template. That creates heavy writeups for small sessions, weak structure for real incidents, or noisy lesson capture that misses what should actually be remembered.

## The Solution

This meta-skill provides three focused modes.

1. `SessionReview` for reverse-engineering a completed session or conversation into memory types, lessons, fixes, and feedback.
2. `IncidentReview` for blameless operational or delivery incidents using standard, quick, or 5 Whys workflows.
3. `FeedbackCapture` for turning completed work, fixes, or decisions into durable lessons.

All three modes share one finalization rule: when the content is final and should be saved, use the utility skill `write-down-postmortem`, which writes into the current project's `docs/references/postmortem/references/` path.

## What's Included

| Component | Path | Purpose |
|---|---|---|
| Skill router | `references/ROUTER.md` | Minimal routing table for postmortem requests |
| SessionReview skill | `references/SessionReview/MetaSkill.md` | Reverse-engineer conversations and work sessions |
| SessionReview references | `references/SessionReview/references/` | Workflows, template, rubric, and example |
| IncidentReview skill | `references/IncidentReview/MetaSkill.md` | Blameless incident review and root-cause analysis |
| IncidentReview references | `references/IncidentReview/references/` | Workflows, template, and example |
| FeedbackCapture skill | `references/FeedbackCapture/MetaSkill.md` | Capture durable lessons and feedback from completed work |
| FeedbackCapture references | `references/FeedbackCapture/references/` | Workflows, template, and example |

## Invocation Scenarios

| Trigger | What Happens |
|---|---|
| "reverse engineer what we did together" | Routes to `SessionReview` |
| "what is worth remembering from this session" | Routes to `SessionReview` |
| "write a blameless postmortem for this outage" | Routes to `IncidentReview` |
| "do a quick postmortem on this incident" | Routes to `IncidentReview` |
| "run 5 whys on this failure" | Routes to `IncidentReview` |
| "capture lessons from this fix" | Routes to `FeedbackCapture` |
| "what feedback should the agent remember next time" | Routes to `FeedbackCapture` |
| "save the final postmortem in the project" | Stay in the active sub-skill and finish with `write-down-postmortem` |

## Example Usage

### Session Review

```text
User: Reverse engineer what we did together and keep only what is worth remembering.

AI routes to SessionReview and returns:
- Elements worth remembering
- Memory type for each element
- What we learned
- What went wrong
- What we discovered
- The fix
- Feedback for the agent
- Feedback for the user
```

### Incident Review

```text
User: Write a blameless postmortem for the deploy rollback.

AI routes to IncidentReview and returns:
- Summary
- Impact
- Timeline
- Root cause
- Contributing factors
- Fixes applied
- Follow-up actions
```

### Feedback Capture

```text
User: Capture the lessons from this fix and save it in the project.

AI routes to FeedbackCapture, writes the lesson set, then uses `write-down-postmortem`
to save it under `docs/references/postmortem/references/`.
```

## Configuration

No configuration is required.

Optional conventions:

- Keep the output proportional to the event size.
- Prefer the user's own vocabulary when writing lessons or feedback.
- Save final content with `write-down-postmortem` only after the postmortem itself is complete.

## Design Rules

1. Keep the output proportional to the event.
2. Preserve blameless language for incidents.
3. Keep session reviews grounded in what actually happened.
4. Capture only durable lessons, not every detail.
5. Use `write-down-postmortem` for persistence inside the active project.
