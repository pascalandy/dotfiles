# GithubTriage

Triage GitHub issues through a label-based state machine with interactive grilling sessions. Infer the repo from `git remote`. Use `gh` for all GitHub operations.

## Labels

| Label | Type | Description |
|-------|------|-------------|
| `bug` | Category | Something is broken |
| `enhancement` | Category | New feature or improvement |
| `needs-triage` | State | Maintainer needs to evaluate this issue |
| `needs-info` | State | Waiting on reporter for more information |
| `ready-for-agent` | State | Fully specified, ready for AFK agent |
| `ready-for-human` | State | Requires human implementation |
| `wontfix` | State | Will not be actioned |

Every issue should have exactly **one** state label and **one** category label. If an issue has conflicting state labels, flag the conflict and ask the maintainer which state is correct before doing anything else. Provide a recommendation.

## State Machine

An issue can only move along these transitions. The maintainer can override any state directly (see Quick State Override below), but the skill should flag if the transition is unusual.

| Current State | Can Transition To | Who Triggers | What Happens |
|---------------|-------------------|--------------|-------------|
| `unlabeled` | `needs-triage` | Skill (first look) | Issue needs maintainer evaluation. Skill applies label after presenting recommendation. |
| `unlabeled` | `ready-for-agent` | Maintainer (via skill) | Issue is already well-specified and agent-suitable. Skill writes agent brief. |
| `unlabeled` | `ready-for-human` | Maintainer (via skill) | Issue requires human implementation. Skill applies label. |
| `unlabeled` | `wontfix` | Maintainer (via skill) | Spam, duplicate, or out of scope. Skill closes issue. |
| `needs-triage` | `needs-info` | Maintainer (via skill) | Issue is underspecified. Skill posts triage notes with questions for reporter. |
| `needs-triage` | `ready-for-agent` | Maintainer (via skill) | Grilling session complete, agent-suitable. Skill writes agent brief. |
| `needs-triage` | `ready-for-human` | Maintainer (via skill) | Grilling session complete, needs human. Skill applies label. |
| `needs-triage` | `wontfix` | Maintainer (via skill) | Maintainer decides not to action. Skill closes issue. |
| `needs-info` | `needs-triage` | Skill (detects reply) | Reporter has replied. Skill moves back to triage. |

## Workflows

### Show What Needs Attention

Query GitHub and present a summary grouped into three buckets:
1. **Unlabeled issues** -- new, no labels
2. **`needs-triage` issues** -- maintainer needs to evaluate
3. **`needs-info` issues with new activity** -- reporter has commented since last triage notes

Display counts per group. Within each group, show issues oldest first (longest-waiting gets attention first). For each issue show: number, title, age, and a one-line summary of the issue body.

Let the maintainer pick which issue to dive into.

### Triage a Specific Issue

**Step 1: Gather context.** Read the full issue: body, all comments, all labels, reporter, timestamp. Parse prior triage notes if they exist. Explore the codebase to build context -- understand the domain, relevant interfaces, and existing behavior. Read `.out-of-scope/*.md` files for prior rejections (see `references/OutOfScope.md`).

**Step 2: Present recommendation.** Category (bug/enhancement) with reasoning. State recommendation with reasoning. Surface any matching out-of-scope rejections. Codebase context summary.

The maintainer can:
- Agree and ask you to apply labels -- do it
- Want to flesh it out -- start a grilling session (Step 4)
- Override with a different state -- apply their choice
- Want to discuss -- have a conversation

**Step 3: Bug reproduction (bugs only).**
- Read the reporter's steps to reproduce
- Explore the code path that handles the described scenario
- Try to reproduce the bug
- If reproducible: report findings with specifics (what breaks, where in the flow)
- If not reproducible: report what you tried and what worked
- Note if the reporter's description lacks sufficient detail for reproduction -- this is a signal for `needs-info`
- Reproduction findings inform the agent brief quality

**Step 4: Grilling session (if `ready-for-agent` or `ready-for-human` is the target).**
- Ask questions one at a time
- Provide a recommended answer for each question
- If a question can be answered by exploring the codebase, explore instead of asking
- For bugs: use the reproduction findings to ask targeted questions
- Resume from prior triage notes if they exist -- do not re-ask resolved questions

Grilling goals -- reach:
1. A clear summary of the desired behavior
2. Concrete acceptance criteria
3. Key interfaces that may need to change
4. A clear boundary of what is out of scope

**Step 5: Apply the outcome.** Before posting any comment or applying any label, show the maintainer a preview of exactly what will be posted and which labels will be applied/removed. Only proceed on confirmation.

Outcome-specific actions:
- **`ready-for-agent`:** Post an agent brief comment (see `references/AgentBrief.md`). Apply `ready-for-agent` label. Remove `needs-triage`.
- **`ready-for-human`:** Post a summary of the grilling session outcome. Apply `ready-for-human`. Remove `needs-triage`.
- **`needs-info`:** Post triage notes (see Needs Info Output below). Apply `needs-info`. Remove `needs-triage`.
- **`wontfix` (bug):** Post explanation. Close the issue. Apply `wontfix`. Remove `needs-triage`.
- **`wontfix` (enhancement):** Post explanation. Close the issue. Apply `wontfix`. Write an out-of-scope entry (see `references/OutOfScope.md`). Remove `needs-triage`.
- **Stays `needs-triage`:** Post triage notes capturing progress so far.

### Quick State Override

When the maintainer explicitly requests a state change, trust their judgment and apply directly. Show confirmation of what will happen.

If moving to `ready-for-agent` without a grilling session, ask the maintainer if they want to write a brief agent brief comment or skip it.

## Needs Info Output

Post a comment with triage notes:

```markdown
## Triage Notes

### What we've established so far
- [Summary of what is known from the issue and any investigation]

### What we still need from you (@reporter)
- [Specific, actionable question 1]
- [Specific, actionable question 2]
```

Include everything resolved during the grilling session so that context is preserved for the reporter. The questions for the reporter should be specific and actionable, not vague.

## Resuming Previous Sessions

1. Parse prior triage notes from comments
2. Check for reporter replies since last triage notes
3. Present updated picture showing what is new
4. Do not re-ask resolved questions
5. Continue from where the grilling stopped
