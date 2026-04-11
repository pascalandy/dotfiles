# Executing Plans

> Load a written implementation plan, review it critically, execute all tasks in order, and complete the branch.

## When to Use

Use when you have a written implementation plan to execute — typically in a separate session from where the plan was written, with review checkpoints throughout.

**Note:** This skill is for environments without subagent support. On platforms that support subagents, use `superpowers:subagent-driven-development` instead — the quality of work will be significantly higher. Check `harness-compat.md` for your platform's subagent capabilities.

## Inputs

- A written implementation plan file
- An isolated git workspace (worktree set up via `superpowers:using-git-worktrees` before starting)
- All dependencies and environment required by the plan

## Methodology

### Announce at Start

State: "I'm using the executing-plans skill to implement this plan."

### Step 1: Load and Review Plan

1. Read the plan file in full
2. Review critically — identify any questions or concerns about the plan
3. **If concerns exist:** Raise them with your human partner before starting. Do not proceed until concerns are resolved.
4. **If no concerns:** Create a task list and proceed to Step 2

### Step 2: Execute Tasks

For each task in the plan:

1. Mark the task as in_progress
2. Follow each step exactly as written (the plan has bite-sized steps)
3. Run verifications as specified in the plan — do NOT skip them
4. Mark the task as completed
5. Move to the next task

### Step 3: Complete Development

After all tasks complete and all verifications pass:

1. Announce: "I'm using the finishing-a-development-branch skill to complete this work."
2. Invoke `superpowers:finishing-a-development-branch`
3. Follow that skill to verify tests, present options, execute choice

---

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

Do NOT force through blockers.

---

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

---

## Rules

- Review plan critically before starting
- Follow plan steps exactly — no improvisation
- Don't skip verifications
- Reference skills when the plan says to invoke them
- Stop when blocked, don't guess
- **Never start implementation on main/master branch without explicit user consent**

## Quality Gates

- [ ] Plan reviewed before any execution begins
- [ ] All concerns raised and resolved before starting
- [ ] Task list created and tracked
- [ ] Each task marked in_progress before starting, completed after finishing
- [ ] Each verification step run (none skipped)
- [ ] Blocked tasks escalated immediately — not guessed through
- [ ] finishing-a-development-branch invoked after all tasks complete

## Outputs

- All plan tasks executed and verified
- Branch completed via `finishing-a-development-branch` (merged, PR, kept, or discarded)

## Feeds Into

- **finishing-a-development-branch** — required sub-skill invoked at the end of Step 3

## Harness Notes

This skill is designed for single-agent execution. If the harness supports subagents, use `superpowers:subagent-driven-development` instead for significantly better results. Requires `superpowers:using-git-worktrees` to be run before this skill to set up an isolated workspace.
