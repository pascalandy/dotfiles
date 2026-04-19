---
name: pa-postmortem
description: Multi-mode postmortem skill for reverse-engineering sessions, writing blameless incident reviews, and capturing durable feedback from completed work. USE WHEN postmortem, lessons learned, what should we remember, reverse engineer the session, review what we did together, blameless incident review, incident postmortem, 5 whys, feedback capture, capture lessons from this fix, what went wrong, what did we discover, how should we write this down.
keywords: [postmortem, lessons-learned, session-review, incident-review, feedback-capture, reverse-engineer, blameless, five-whys, root-cause, write-down-postmortem]
---

# Postmortem

Explicit entry point: `pa-postmortem`.

Three distinct postmortem modes in one skill: session review, incident review, and feedback capture. Route to the right mode automatically, then export the final postmortem artifact.

## Route

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

All three modes share one finalization rule: the final postmortem artifact is always written to the resolved export path before the skill returns.

## Internal Modes

| Mode | Owns | Use when |
|---|---|---|
| `SessionReview` | Reverse-engineering a session | Preserve memory types, lessons, fixes, and feedback from a completed conversation |
| `IncidentReview` | Blameless incident review | Real operational or delivery incident needs impact, timeline, causes, and follow-ups |
| `FeedbackCapture` | Durable lessons from completed work | Work is done and only the transferable lessons and feedback should survive |

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

## Boundaries

| If the real need is... | Use instead |
|---|---|
| capturing a rough idea | `pa-idea` |
| deciding whether the direction is right | `pa-vision` |
| designing execution, structure, or sequencing | `pa-architect` |
| building the change or fixing a bug | `pa-implement` |
| documenting an already-made change, decision, or artifact | `pa-doc-update` |
| refreshing, deduplicating, or repairing existing docs | `pa-doc-cleaner` |

## Default Output

Route to one primary mode, then use that mode's output contract. In all modes, make these easy to find:

1. what happened
2. what was learned
3. what should be remembered
4. follow-up actions or feedback
5. recommended next phase or owner

## Export Contract

Create an idea entry in `docs/references/ideas/references/`.

Resolve the export target before running the writing workflow. This contract is separate so the same export pattern can be reused elsewhere by swapping only the destination and naming rules.

- `export_root`: `docs/references/ideas/references/`
- `entry_slug`: a 2-4 word kebab-case title, preferably from a strong user-provided title
- `export_dir`: `YYYY-MM-DD-entry_slug/`
- `export_file`: `postmortem-entry_slug.md`
- Final path: `export_root/export_dir/export_file`

## Workflow

1. Use the user's remaining input as the raw idea text.
2. If the idea is missing or too thin to title, ask one short question.
3. Resolve `entry_slug`, `export_dir`, and `export_file` before editing any text.
4. Start from the raw text.
5. Do a `simple-editor` (skill) pass.
6. Do a `writer-sk` (skill) pass.
7. Write the final text to the resolved export path.
8. Return the folder path, file path, and final slug.

## Rules

- Keep export naming mechanical and separate from the writing pass.
- Prefer a strong user-provided title when resolving `entry_slug`.
- Keep the final artifact aligned with the selected Postmortem mode rather than forcing a single document shape.
- Export is mandatory when `pa-postmortem` produces a session review, incident review, or feedback capture artifact.
- Do not hand off to any later phase before the postmortem artifact has been written to the resolved export path.
- Keep the output proportional to the event size.
- Preserve blameless language for incidents.
- Keep session reviews grounded in what actually happened.
- Capture only durable lessons, not every detail.
- For reuse, change the export contract first and keep the workflow steps unchanged unless the content workflow itself differs.

## Non-Goals

Postmortem does not own discovery, scoping, product direction, execution planning, implementation, or documentation maintenance.
