# ce:work-beta

> Execute a plan with optional external delegate support for token-conserving code implementation.

## When to Use

- Same triggers as `ce:work`, plus:
- User says "use codex for this work", "delegate to codex", or "delegate mode".
- A plan implementation unit contains `Execution target: external-delegate` in its Execution note.
- Token conservation matters (e.g., running under a constrained plan quota).

## Inputs

- A file path to an existing plan/spec/todo, OR a plain-language description of the work.
- Access to the project codebase and git repository.
- (Optional) Figma design links for UI work.
- (Optional) External delegate CLI installed (currently: Codex CLI).

## Methodology

This skill is identical to `ce:work` through all phases, with two additions: an **External Delegate Mode** and a **Frontend Design Guidance** step. All ce:work phases and rules apply without exception.

### Phase 0 through Phase 4: Same as ce:work

See `ce-work.md` for the complete methodology for all four phases, the System-Wide Test Check, Test Discovery, Test Scenario Completeness, incremental commits, code review tiers, quality checklist, and Swarm Mode.

---

### Additional Step in Phase 2: Frontend Design Guidance (if applicable)

**Step 7** (insert after Figma Design Sync):

For UI tasks without a Figma design — where the implementation touches view, template, component, layout, or page files, creates user-visible routes, or the plan contains explicit UI/frontend/design language:
- Load the `frontend-design` skill before implementing.
- Follow its detection, guidance, and verification flow.
- If the skill produced a verification screenshot, it satisfies Phase 4's screenshot requirement — no need to capture separately. If the skill fell back to mental review (no browser access), Phase 4's screenshot capture still applies.

---

### External Delegate Mode (Optional)

This mode integrates with Phase 1 Step 4 (Execution Strategy) as a **task-level modifier** — the strategy (inline/serial/parallel) still applies, but the implementation step within each tagged task delegates to the external tool instead of executing directly.

#### When to Use External Delegation

| External Delegation | Standard Mode |
|---------------------|---------------|
| Task is pure code implementation | Task requires research or exploration |
| Plan has clear acceptance criteria | Task is ambiguous or needs iteration |
| Token conservation matters (e.g., Max20 plan) | Unlimited plan or small task |
| Files to change are well-scoped | Changes span many interconnected files |

#### Enabling External Delegation

External delegation activates when any of these conditions are met:
- The user says "use codex for this work", "delegate to codex", or "delegate mode".
- A plan implementation unit contains `Execution target: external-delegate` in its Execution note (set by `ce:plan`).

The specific delegate tool is resolved at execution time. Currently the only supported delegate is Codex CLI.

#### Environment Guard

Before attempting delegation, check whether the current agent is already running inside a delegate's sandbox. Delegation from within a sandbox will fail silently or recurse.

Check for known sandbox indicators:
- `CODEX_SANDBOX` environment variable is set.
- `CODEX_SESSION_ID` environment variable is set.
- The filesystem is read-only at `.git/` (Codex sandbox blocks git writes).

If any indicator is detected, print "Already running inside a delegate sandbox - using standard mode." and proceed with standard execution for that task.

#### External Delegation Workflow

When external delegation is active, follow this workflow for each tagged task. Do not skip delegation because a task seems "small", "simple", or "faster inline". The user or plan explicitly requested delegation.

1. **Check availability** — Verify the delegate CLI is installed. If not found, print "Delegate CLI not installed - continuing with standard mode." and proceed normally.

2. **Build prompt** — For each task, assemble a prompt from the plan's implementation unit (Goal, Files, Approach, Conventions from project AGENTS.md/CLAUDE.md). Include rules: no git commits, no PRs, run `git status` and `git diff --stat` when done. Never embed credentials or tokens in the prompt — pass auth through environment variables.

3. **Write prompt to file** — Save the assembled prompt to a unique temporary file to avoid shell quoting issues and cross-task races. Use a unique filename per task.

4. **Delegate** — Run the delegate CLI, piping the prompt file via stdin (not argv expansion, which hits `ARG_MAX` on large prompts). Omit the model flag to use the delegate's default model, which stays current without manual updates.

5. **Review diff** — After the delegate finishes, verify the diff is non-empty and in-scope. Run the project's test/lint commands. If the diff is empty or out-of-scope, fall back to standard mode for that task.

6. **Commit** — The current agent handles all git operations. The delegate's sandbox blocks `.git/index.lock` writes, so the delegate cannot commit. Stage changes and commit with a conventional message.

7. **Error handling** — On any delegate failure (rate limit, error, empty diff), fall back to standard mode for that task. Track consecutive failures — after **3 consecutive failures**, disable delegation for remaining tasks and print: "Delegate disabled after 3 consecutive failures - completing remaining tasks in standard mode."

#### Mixed-Model Attribution

When some tasks are executed by the delegate and others by the current agent:

- If all tasks used the delegate: attribute to the delegate model.
- If all tasks used standard mode: attribute to the current agent's model.
- If mixed: use `Generated with [CURRENT_MODEL] + [DELEGATE_MODEL] via [HARNESS]` and note which tasks were delegated in the PR description.

---

## Quality Gates

Same as `ce:work` — all checklist items apply:

- [ ] All clarifying questions asked and answered
- [ ] All tasks marked completed
- [ ] Testing addressed — tests pass AND new/changed behavior has corresponding test coverage (or an explicit justification for why tests are not needed)
- [ ] Linting passes
- [ ] Code follows existing patterns
- [ ] Figma designs match implementation (if applicable)
- [ ] Before/after screenshots captured and uploaded (for UI changes)
- [ ] Commit messages follow conventional format
- [ ] PR description includes Post-Deploy Monitoring & Validation section (or explicit no-impact rationale)
- [ ] Code review completed (inline self-review Tier 1 or full `ce:review` Tier 2)
- [ ] PR description includes summary, testing notes, and screenshots

## Outputs

- Implemented feature or fix, committed on a feature branch.
- Passing tests (new and existing).
- Pull request with description, testing notes, monitoring plan, and screenshots (for UI).
- Plan document status updated to `completed` (if applicable).
- Attribution note in PR description when delegation was used.

## Feeds Into

- `ce:review` — full review before or after shipping.
- `changelog` — after merging to main.
- `ce:compound` — capture learnings from execution.
