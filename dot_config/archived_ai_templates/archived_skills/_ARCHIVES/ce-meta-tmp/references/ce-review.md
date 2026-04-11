# ce:review

> Structured code review using tiered persona agents, confidence-gated findings, and a merge/dedup pipeline.

## When to Use

- Before creating a PR
- After completing a task during iterative implementation
- When feedback is needed on any code changes
- Can be invoked standalone
- Can run as a read-only or autofix review step inside larger workflows

## Inputs

- Optional argument: blank to review current branch, PR number, GitHub URL, or branch name
- Optional tokens in the argument:
  - `mode:autofix` — select autofix mode
  - `mode:report-only` — select report-only mode
  - `mode:headless` — select headless mode for programmatic callers
  - `base:<sha-or-ref>` — skip scope detection, use this as the diff base directly
  - `plan:<path>` — load this plan for requirements verification

**Conflicting mode flags:** If multiple mode tokens appear, stop and do not dispatch agents. In headless mode, emit: `Review failed (headless mode). Reason: conflicting mode flags — <mode_a> and <mode_b> cannot be combined.` Otherwise emit: `Review failed. Reason: conflicting mode flags — <mode_a> and <mode_b> cannot be combined.`

**Cannot combine `base:` with a PR number or branch target.** If both are present, stop with an error: "Cannot use `base:` with a PR number or branch target — `base:` implies the current checkout is already the correct branch."

## Methodology

### Mode Detection

| Mode | When | Behavior |
|------|------|----------|
| **Interactive** (default) | No mode token present | Review, apply safe_auto fixes automatically, present findings, ask for policy decisions on gated/manual findings, and optionally continue into fix/push/PR next steps |
| **Autofix** | `mode:autofix` in arguments | No user interaction. Review, apply only policy-allowed `safe_auto` fixes, re-review in bounded rounds, write a run artifact, and emit residual downstream work when needed |
| **Report-only** | `mode:report-only` in arguments | Strictly read-only. Review and report only, then stop with no edits, artifacts, todos, commits, pushes, or PR actions |
| **Headless** | `mode:headless` in arguments | Programmatic mode for skill-to-skill invocation. Apply `safe_auto` fixes silently (single pass), return all other findings as structured text output, write run artifacts, skip todos, and return "Review complete" signal. No interactive prompts. |

**Autofix mode rules:**
- Skip all user questions. Never pause for approval or clarification once scope has been established.
- Apply only `safe_auto -> review-fixer` findings. Leave `gated_auto`, `manual`, `human`, and `release` work unresolved.
- Write a run artifact under `.context/compound-engineering/ce-review/<run-id>/`
- Create durable todo files only for unresolved actionable findings whose final owner is `downstream-resolver`
- Never commit, push, or create a PR from autofix mode

**Report-only mode rules:**
- Skip all user questions.
- Never edit files or externalize work. Do not write `.context` artifacts, do not create todo files, and do not commit, push, or create a PR.
- Safe for parallel read-only verification. The only mode safe to run concurrently with browser testing on the same checkout.
- Do not switch the shared checkout.

**Headless mode rules:**
- Skip all user questions. Never use interactive prompts.
- Require a determinable diff scope. If headless mode cannot determine a diff scope without user interaction, emit `Review failed (headless mode). Reason: no diff scope detected. Re-invoke with a branch name, PR number, or base:<ref>.` and stop.
- Apply only `safe_auto -> review-fixer` findings in a single pass. No bounded re-review rounds.
- Return all non-auto findings as structured text output (see headless output format).
- Write a run artifact under `.context/compound-engineering/ce-review/<run-id>/`
- Do not create todo files.
- Do not switch the shared checkout. If the caller passes an explicit PR or branch target, headless mode must run in an isolated checkout/worktree or stop with: `Review failed (headless mode). Reason: cannot switch shared checkout. Re-invoke with base:<ref> to review the current checkout, or run from an isolated worktree.`
- Not safe for concurrent use on a shared checkout (unlike report-only, headless mutates files).
- Never commit, push, or create a PR.
- End with "Review complete" as the terminal signal. If all reviewers fail or time out, emit `Code review degraded (headless mode). Reason: 0 of N reviewers returned results.` followed by "Review complete".

### Severity Scale

All reviewers use P0–P3:

| Level | Meaning | Action |
|-------|---------|--------|
| **P0** | Critical breakage, exploitable vulnerability, data loss/corruption | Must fix before merge |
| **P1** | High-impact defect likely hit in normal usage, breaking contract | Should fix |
| **P2** | Moderate issue with meaningful downside (edge case, perf regression, maintainability trap) | Fix if straightforward |
| **P3** | Low-impact, narrow scope, minor improvement | User's discretion |

### Action Routing

Severity answers **urgency**. Routing answers **who acts next** and **whether this skill may mutate the checkout**.

| `autofix_class` | Default owner | Meaning |
|-----------------|---------------|---------|
| `safe_auto` | `review-fixer` | Local, deterministic fix suitable for the in-skill fixer when the current mode allows mutation |
| `gated_auto` | `downstream-resolver` or `human` | Concrete fix exists, but it changes behavior, contracts, permissions, or another sensitive boundary that should not be auto-applied by default |
| `manual` | `downstream-resolver` or `human` | Actionable work that should be handed off rather than fixed in-skill |
| `advisory` | `human` or `release` | Report-only output such as learnings, rollout notes, or residual risk |

**`autofix_class` calibration examples:**

`safe_auto` examples: extract duplicated helper, add missing nil check, fix off-by-one, add missing test, remove dead code. Do not default to `advisory` when a concrete safe fix exists.

`gated_auto` examples: add auth to unprotected endpoint, change API response shape.

`manual` examples: redesign data model, add pagination strategy, choose between architectural approaches.

`advisory` examples: design asymmetry the PR improves but does not fully resolve, residual risk notes, deployment considerations.

Routing rules:
- Synthesis owns the final route. Persona-provided routing metadata is input, not the last word.
- Choose the more conservative route on disagreement. A merged finding may move from `safe_auto` to `gated_auto` or `manual`, but never the other way without stronger evidence.
- Only `safe_auto -> review-fixer` enters the in-skill fixer queue automatically.
- `requires_verification: true` means a fix is not complete without targeted tests, a focused re-review, or operational validation.

### Reviewer Catalog

**Always-on (4 personas + 2 CE agents) — spawned on every review:**

| Agent | Focus |
|-------|-------|
| `compound-engineering:review:correctness-reviewer` | Logic errors, edge cases, state bugs, error propagation, intent compliance |
| `compound-engineering:review:testing-reviewer` | Coverage gaps, weak assertions, brittle tests, missing edge case tests |
| `compound-engineering:review:maintainability-reviewer` | Coupling, complexity, naming, dead code, premature abstraction |
| `compound-engineering:review:project-standards-reviewer` | CLAUDE.md and AGENTS.md compliance — frontmatter, references, naming, cross-platform portability, tool selection |
| `compound-engineering:review:agent-native-reviewer` | Verify new features are agent-accessible |
| `compound-engineering:research:learnings-researcher` | Search docs/solutions/ for past issues related to this PR |

**Cross-cutting conditional (selected per diff):**

| Agent | Select when diff touches... |
|-------|---------------------------|
| `compound-engineering:review:security-reviewer` | Auth middleware, public endpoints, user input handling, permission checks, secrets management |
| `compound-engineering:review:performance-reviewer` | Database queries, ORM calls, loop-heavy data transforms, caching layers, async/concurrent code |
| `compound-engineering:review:api-contract-reviewer` | Route definitions, serializer/interface changes, event schemas, exported type signatures, API versioning |
| `compound-engineering:review:data-migrations-reviewer` | Migration files, schema changes, backfill scripts, data transformations |
| `compound-engineering:review:reliability-reviewer` | Error handling, retry logic, circuit breakers, timeouts, background jobs, async handlers, health checks |
| `compound-engineering:review:adversarial-reviewer` | Diff >=50 changed non-test/non-generated/non-lockfile lines, OR touches auth, payments, data mutations, external API integrations, or other high-risk domains |
| `compound-engineering:review:previous-comments-reviewer` | **PR-only.** Reviewing a PR that has existing review comments or threads. Skip entirely when no PR metadata was gathered. |

**Stack-specific conditional (selected per diff):**

| Agent | Select when diff touches... |
|-------|---------------------------|
| `compound-engineering:review:dhh-rails-reviewer` | Rails architecture, service objects, authentication/session choices, Hotwire-vs-SPA boundaries, or abstractions that may fight Rails conventions |
| `compound-engineering:review:kieran-rails-reviewer` | Rails controllers, models, views, jobs, components, routes, or other application-layer Ruby code where clarity and conventions matter |
| `compound-engineering:review:kieran-python-reviewer` | Python modules, endpoints, services, scripts, or typed domain code |
| `compound-engineering:review:kieran-typescript-reviewer` | TypeScript components, services, hooks, utilities, or shared types |
| `compound-engineering:review:julik-frontend-races-reviewer` | Stimulus/Turbo controllers, DOM event wiring, timers, async UI flows, animations, or frontend state transitions with race potential |

**CE conditional (migration-specific):**

| Agent | Select when diff includes migration files |
|-------|------------------------------------------|
| `compound-engineering:review:schema-drift-detector` | Cross-references schema.rb against included migrations to catch unrelated drift |
| `compound-engineering:review:deployment-verification-agent` | Produces deployment checklist with SQL verification queries and rollback procedures |

**Selection rules:**
1. Always spawn all 4 always-on personas plus the 2 CE always-on agents.
2. For each cross-cutting conditional persona, read the diff and decide whether the persona's domain is relevant. This is a judgment call, not a keyword match.
3. For each stack-specific conditional persona, use file types and changed patterns as a starting point, then decide whether the diff actually introduces meaningful work for that reviewer. Do not spawn language-specific reviewers just because one config or generated file happens to match the extension.
4. For CE conditional agents, spawn when the diff includes migration files (`db/migrate/*.rb`, `db/schema.rb`) or data backfill scripts.
5. `previous-comments` is PR-only. Only select this persona when Stage 1 gathered PR metadata.

**Review scope right-sizing:** A small config change triggers 0 conditionals = 6 reviewers. A Rails auth feature might trigger security + reliability + kieran-rails + dhh-rails = 10 reviewers.

### Protected Artifacts

The following paths are pipeline artifacts and must never be flagged for deletion, removal, or gitignore by any reviewer:
- `docs/brainstorms/*` — requirements documents created by ce:brainstorm
- `docs/plans/*.md` — plan files created by ce:plan
- `docs/solutions/*.md` — solution documents

If a reviewer flags any file in these directories for cleanup or removal, discard that finding during synthesis.

---

### Stage 1: Determine Scope

Compute the diff range, file list, and diff.

**If `base:` argument is provided (fast path):**
```
BASE_ARG="{base_arg}"
BASE=$(git merge-base HEAD "$BASE_ARG" 2>/dev/null) || BASE="$BASE_ARG"
echo "BASE:$BASE" && echo "FILES:" && git diff --name-only $BASE && echo "DIFF:" && git diff -U10 $BASE && echo "UNTRACKED:" && git ls-files --others --exclude-standard
```

**If a PR number or GitHub URL is provided:**
- If `mode:report-only` or `mode:headless` is active, do NOT run `gh pr checkout` on the shared checkout. For report-only, tell the caller to run it from an isolated worktree. For headless, emit the headless cannot-switch-checkout error and stop.
- Verify worktree is clean first (`git status --porcelain`). If non-empty, inform the user and do not proceed until the worktree is clean.
- Check out the PR branch: `gh pr checkout <number-or-url>`
- Fetch PR metadata: `gh pr view <number-or-url> --json title,body,baseRefName,headRefName,url`
- Use the repository portion of the PR URL as `<base-repo>` (e.g., `EveryInc/compound-engineering-plugin` from `https://github.com/EveryInc/compound-engineering-plugin/pull/348`)
- Resolve the base ref from the PR's actual base repository (not by assuming `origin` points at that repo). Compute:
```
PR_BASE_REMOTE=$(git remote -v | awk 'index($2, "github.com:<base-repo>") || index($2, "github.com/<base-repo>") {print $1; exit}')
if [ -n "$PR_BASE_REMOTE" ]; then PR_BASE_REMOTE_REF="$PR_BASE_REMOTE/<base>"; else PR_BASE_REMOTE_REF=""; fi
PR_BASE_REF=$(git rev-parse --verify "$PR_BASE_REMOTE_REF" 2>/dev/null || git rev-parse --verify <base> 2>/dev/null || true)
if [ -z "$PR_BASE_REF" ]; then
  if [ -n "$PR_BASE_REMOTE_REF" ]; then
    git fetch --no-tags "$PR_BASE_REMOTE" <base>:refs/remotes/"$PR_BASE_REMOTE"/<base> 2>/dev/null || git fetch --no-tags "$PR_BASE_REMOTE" <base> 2>/dev/null || true
    PR_BASE_REF=$(git rev-parse --verify "$PR_BASE_REMOTE_REF" 2>/dev/null || git rev-parse --verify <base> 2>/dev/null || true)
  else
    if git fetch --no-tags https://github.com/<base-repo>.git <base> 2>/dev/null; then
      PR_BASE_REF=$(git rev-parse --verify FETCH_HEAD 2>/dev/null || true)
    fi
    if [ -z "$PR_BASE_REF" ]; then PR_BASE_REF=$(git rev-parse --verify <base> 2>/dev/null || true); fi
  fi
fi
if [ -n "$PR_BASE_REF" ]; then BASE=$(git merge-base HEAD "$PR_BASE_REF" 2>/dev/null) || BASE=""; else BASE=""; fi
```
- If BASE is resolved: `echo "BASE:$BASE" && echo "FILES:" && git diff --name-only $BASE && echo "DIFF:" && git diff -U10 $BASE && echo "UNTRACKED:" && git ls-files --others --exclude-standard`
- If BASE cannot be resolved, stop — do not fall back to `git diff HEAD`.

**If a branch name is provided:**
- If `mode:report-only` or `mode:headless` is active, do NOT run `git checkout <branch>` on the shared checkout.
- Verify worktree is clean first. If non-empty, inform the user.
- Check out the branch: `git checkout <branch>`
- Run `references/resolve-base.sh` to detect the review base branch with fork-safe multi-fallback detection. If the script outputs an error, stop — do not fall back to `git diff HEAD`.
- On success: `echo "BASE:$BASE" && echo "FILES:" && git diff --name-only $BASE && echo "DIFF:" && git diff -U10 $BASE && echo "UNTRACKED:" && git ls-files --others --exclude-standard`

**If no argument (standalone on current branch):**
- Run `references/resolve-base.sh` to detect the review base branch.
- If the script outputs an error, stop.
- On success, produce the diff as above.

Using `git diff $BASE` (without `..HEAD`) diffs the merge-base against the working tree, including committed, staged, and unstaged changes.

**Untracked file handling:** Always inspect the `UNTRACKED:` list. Untracked files are outside review scope until staged. If the list is non-empty, tell the user which files are excluded. If any of them should be reviewed, stop and tell the user to `git add` them first and rerun. Only continue when the user is intentionally reviewing tracked changes only. In `mode:headless` or `mode:autofix`, proceed with tracked changes only and note excluded untracked files in the Coverage section.

### Stage 2: Intent Discovery

Write a 2–3 line intent summary from diff context:
```
Intent: Simplify tax calculation by replacing the multi-tier rate lookup
with a flat-rate computation. Must not regress edge cases in tax-exempt handling.
```

Pass this to every reviewer in their spawn prompt.

- **PR/URL mode:** Use PR title, body, and linked issues from `gh pr view` metadata. Supplement with commit messages if the body is sparse.
- **Branch mode:** Run `git log --oneline ${BASE}..<branch>` using the resolved merge-base.
- **Standalone:** Run `echo "BRANCH:" && git rev-parse --abbrev-ref HEAD && echo "COMMITS:" && git log --oneline ${BASE}..HEAD`

**When intent is ambiguous:**
- **Interactive mode:** Ask one question: "What is the primary goal of these changes?" Do not spawn reviewers until intent is established.
- **Autofix/report-only/headless modes:** Infer intent conservatively from available metadata. Note the uncertainty in Coverage or Verdict reasoning.

### Stage 2b: Plan Discovery (Requirements Verification)

Locate the plan document so Stage 6 can verify requirements completeness. Check these sources in priority order:

1. **`plan:` argument** — if the caller passed a plan path, use it directly. `plan_source: explicit`
2. **PR body** — scan the body for paths matching `docs/plans/*.md`. If exactly one match, use it as `plan_source: explicit`. If multiple matches, use most recent match that exists as `plan_source: inferred`. Always verify the selected file exists.
3. **Auto-discover** — extract 2–3 keywords from the branch name. Glob `docs/plans/*` and filter filenames containing those keywords. If exactly one unambiguous match, use it as `plan_source: inferred`. If multiple/ambiguous matches or generic keywords, skip.

If a plan is found, read its **Requirements Trace** (R1, R2, etc.) and **Implementation Units** (checkbox items). Store the requirements list and `plan_source` for Stage 6.

Do not block the review if no plan is found — requirements verification is additive, not required.

### Stage 3: Select Reviewers

Read the diff and file list from Stage 1. The 4 always-on personas and 2 CE always-on agents are automatic. For each cross-cutting and stack-specific conditional persona, decide whether the diff warrants it. This is agent judgment, not keyword matching.

Before spawning, discover project standards paths:
1. Find all `**/CLAUDE.md` and `**/AGENTS.md` in the repo
2. Filter to those whose directory is an ancestor of at least one changed file
3. Pass the resulting path list to the `project-standards` persona inside a `<standards-paths>` block

Announce the team before spawning (progress reporting, not a blocking confirmation):
```
Review team:
- correctness (always)
- testing (always)
- maintainability (always)
- project-standards (always)
- agent-native-reviewer (always)
- learnings-researcher (always)
- security -- new endpoint in routes.rb accepts user-provided redirect URL
- kieran-rails -- controller and Turbo flow changed in app/controllers and app/views
```

### Stage 4: Spawn Sub-Agents

**Model tiering:** Use the platform's cheapest capable model for all persona and CE sub-agents. The orchestrator stays on the default (most capable) model.

**Spawn each selected persona reviewer as a parallel sub-agent.** Each persona sub-agent receives:
1. Their persona file content
2. Diff scope rules
3. The JSON output contract (findings schema)
4. PR metadata: title, body, and URL when reviewing a PR (empty string otherwise) in a `<pr-context>` block
5. Review context: intent summary, file list, diff
6. **For `project-standards` only:** the standards file path list in a `<standards-paths>` block

Persona sub-agents are **read-only** (non-mutating). They may use non-mutating inspection commands (read-oriented git/gh usage such as `git diff`, `git show`, `git blame`, `git log`, `gh pr view`). They must not edit files, change branches, commit, push, create PRs, or otherwise mutate state.

**Each persona sub-agent returns JSON matching this schema:**
```json
{
  "reviewer": "<persona name>",
  "findings": [
    {
      "title": "Short specific issue title (10 words or fewer)",
      "severity": "P0|P1|P2|P3",
      "file": "relative/file/path",
      "line": 42,
      "why_it_matters": "Impact and failure mode — not 'what is wrong' but 'what breaks'",
      "autofix_class": "safe_auto|gated_auto|manual|advisory",
      "owner": "review-fixer|downstream-resolver|human|release",
      "requires_verification": true,
      "suggested_fix": "Concrete minimal fix or null",
      "confidence": 0.85,
      "evidence": ["code-grounded evidence item 1", "code-grounded evidence item 2"],
      "pre_existing": false
    }
  ],
  "residual_risks": ["risk description"],
  "testing_gaps": ["missing test coverage description"]
}
```

**Confidence thresholds:**
- Below 0.60: suppress (exception: P0 at 0.50+ may survive)
- 0.60–0.69: include only when clearly actionable with concrete evidence
- 0.70–0.84: real and important. Report with full evidence.
- 0.85–1.00: verifiable from the code alone. Report.

**CE always-on agents** (agent-native-reviewer, learnings-researcher) are dispatched as standard Agent calls in parallel with persona agents. Give them the same review context bundle. Their output is unstructured and synthesized separately in Stage 6.

**CE conditional agents** (schema-drift-detector, deployment-verification-agent) are also dispatched as standard Agent calls when applicable. Pass the same review context bundle plus the applicability reason. For schema-drift-detector specifically, pass the resolved review base branch explicitly.

### Stage 5: Merge Findings

Convert multiple reviewer JSON payloads into one deduplicated, confidence-gated finding set:

1. **Validate.** Check each output against the schema. Drop malformed findings. Record the drop count.
2. **Confidence gate.** Suppress findings below 0.60 confidence. Exception: P0 findings at 0.50+ confidence survive. Record the suppressed count.
3. **Deduplicate.** Compute fingerprint: `normalize(file) + line_bucket(line, +/-3) + normalize(title)`. When fingerprints match, merge: keep highest severity, keep highest confidence with strongest evidence, union evidence, note which reviewers flagged it.
4. **Cross-reviewer agreement.** When 2+ independent reviewers flag the same issue (same fingerprint), boost the merged confidence by 0.10 (capped at 1.0). Note the agreement in the Reviewer column.
5. **Separate pre-existing.** Pull out findings with `pre_existing: true` into a separate list.
6. **Resolve disagreements.** When reviewers flag the same code region but disagree on severity, autofix_class, or owner, record the disagreement in the finding's evidence.
7. **Normalize routing.** For each merged finding, set the final `autofix_class`, `owner`, and `requires_verification`. If reviewers disagree, keep the most conservative route. Synthesis may narrow a finding from `safe_auto` to `gated_auto` or `manual`, but must not widen it without new evidence.
8. **Partition the work.** Build three sets:
   - in-skill fixer queue: only `safe_auto -> review-fixer`
   - residual actionable queue: unresolved `gated_auto` or `manual` findings whose owner is `downstream-resolver`
   - report-only queue: `advisory` findings plus anything owned by `human` or `release`
9. **Sort.** Order by severity (P0 first) → confidence (descending) → file path → line number.
10. **Collect coverage data.** Union residual_risks and testing_gaps across reviewers.
11. **Preserve CE agent artifacts.** Keep the learnings, agent-native, schema-drift, and deployment-verification outputs alongside the merged finding set.

### Stage 6: Synthesize and Present

Assemble the final report using **pipe-delimited markdown tables for findings**. The table format is mandatory for finding rows in interactive mode.

**Report sections:**

1. **Header.** Scope, intent, mode, reviewer team with per-conditional justifications.
2. **Findings.** Rendered as pipe-delimited tables grouped by severity (`### P0 -- Critical`, `### P1 -- High`, `### P2 -- Moderate`, `### P3 -- Low`). Each finding row shows `#`, file, issue, reviewer(s), confidence, and synthesized route. Omit empty severity levels. Never render findings as freeform text blocks or numbered lists.
3. **Requirements Completeness.** Include only when a plan was found in Stage 2b. For each requirement (R1, R2, etc.) and implementation unit, report: met / not addressed / partially addressed.
   - `plan_source: explicit`: Flag unaddressed requirements as P1 findings with `autofix_class: manual`, `owner: downstream-resolver`. These enter the residual actionable queue and can become todos.
   - `plan_source: inferred`: Flag unaddressed requirements as P3 findings with `autofix_class: advisory`, `owner: human`. Report only — no todos.
   - Omit this section entirely when no plan was found.
4. **Applied Fixes.** Include only if a fix phase ran in this invocation.
5. **Residual Actionable Work.** Include when unresolved actionable findings were handed off or should be handed off.
6. **Pre-existing.** Separate section, does not count toward verdict.
7. **Learnings & Past Solutions.** Surface learnings-researcher results: if past solutions are relevant, flag them as "Known Pattern" with links to docs/solutions/ files.
8. **Agent-Native Gaps.** Surface agent-native-reviewer results. Omit section if no gaps found.
9. **Schema Drift Check.** If schema-drift-detector ran, summarize whether drift was found.
10. **Deployment Notes.** If deployment-verification-agent ran, surface key Go/No-Go items.
11. **Coverage.** Suppressed count, residual risks, testing gaps, failed/timed-out reviewers, and any intent uncertainty.
12. **Verdict.** Ready to merge / Ready with fixes / Not ready. Fix order if applicable. When an `explicit` plan has unaddressed requirements, the verdict must reflect it — a code-clean PR missing planned requirements is "Not ready" unless the omission is intentional. When an `inferred` plan has unaddressed requirements, note it in the verdict reasoning but do not block on it alone.

Do not include time estimates.

**Format verification:** Before delivering the report, verify the findings sections use pipe-delimited table rows (`| # | File | Issue | ... |`) not freeform text.

**Findings table example:**
```
| # | File | Issue | Reviewer | Confidence | Route |
|---|------|-------|----------|------------|-------|
| 1 | `orders_controller.rb:42` | User-supplied ID in account lookup without ownership check | security | 0.92 | `gated_auto -> downstream-resolver` |
```

**Diff scope rules for reviewers** — findings fall into three tiers:
- **Primary** (directly changed code) — lines added or modified in the diff. Main focus. Report at full confidence.
- **Secondary** (immediately surrounding code) — unchanged code within the same function/method as a changed line. If a change introduces a bug only visible by reading surrounding context, report it — but note the issue exists in the interaction between new and existing code.
- **Pre-existing** (unrelated to this diff) — issues in unchanged code the diff didn't touch and doesn't interact with. Mark as `"pre_existing": true`. Reported separately and don't count toward the review verdict. Rule: if you'd flag the same issue on an identical diff that didn't include the surrounding file, it's pre-existing.

---

### Headless Output Format

In `mode:headless`, replace the interactive pipe-delimited table report with a structured text envelope:

```
Code review complete (headless mode).

Scope: <scope-line>
Intent: <intent-summary>
Reviewers: <reviewer-list with conditional justifications>
Verdict: <Ready to merge | Ready with fixes | Not ready>
Artifact: .context/compound-engineering/ce-review/<run-id>/

Applied N safe_auto fixes.

Gated-auto findings (concrete fix, changes behavior/contracts):

[P1][gated_auto -> downstream-resolver][needs-verification] File: <file:line> -- <title> (<reviewer>, confidence <N>)
  Why: <why_it_matters>
  Suggested fix: <suggested_fix or "none">
  Evidence: <evidence[0]>
  Evidence: <evidence[1]>

Manual findings (actionable, needs handoff):

[P1][manual -> downstream-resolver] File: <file:line> -- <title> (<reviewer>, confidence <N>)
  Why: <why_it_matters>
  Evidence: <evidence[0]>

Advisory findings (report-only):

[P2][advisory -> human] File: <file:line> -- <title> (<reviewer>, confidence <N>)
  Why: <why_it_matters>

Pre-existing issues:
[P2][gated_auto -> downstream-resolver] File: <file:line> -- <title> (<reviewer>, confidence <N>)
  Why: <why_it_matters>

Residual risks:
- <risk>

Learnings & Past Solutions:
- <learning>

Agent-Native Gaps:
- <gap description>

Schema Drift Check:
- <drift status>

Deployment Notes:
- <deployment note>

Testing gaps:
- <gap>

Coverage:
- Suppressed: <N> findings below 0.60 confidence (P0 at 0.50+ retained)
- Untracked files excluded: <file1>, <file2>
- Failed reviewers: <reviewer>

Review complete
```

**Headless formatting rules:**
- `[needs-verification]` marker appears only on findings where `requires_verification: true`
- Findings with `owner: release` appear in the Advisory section
- Findings with `pre_existing: true` appear in the Pre-existing section regardless of autofix_class
- Verdict appears in the metadata header (first, so programmatic callers get it immediately)
- Omit any section with zero items
- End with "Review complete" as the terminal signal

---

### After Review: Mode-Driven Post-Review Flow

#### Step 1: Build the Action Sets

- **Clean review**: zero findings after suppression and pre-existing separation. Skip the fix/handoff phase.
- **Fixer queue:** final findings routed to `safe_auto -> review-fixer`
- **Residual actionable queue:** unresolved `gated_auto` or `manual` findings whose final owner is `downstream-resolver`
- **Report-only queue:** `advisory` findings and any outputs owned by `human` or `release`
- **Never convert advisory-only outputs into fix work or todos.**

#### Step 2: Choose Policy by Mode

**Interactive mode:**
- Apply `safe_auto -> review-fixer` findings automatically without asking.
- Ask a policy question using the platform's blocking question tool only when `gated_auto` or `manual` findings remain after safe fixes.

  **When `gated_auto` findings are present (with or without `manual`):**
  ```
  Safe fixes have been applied. What should I do with the remaining findings?
  1. Review and approve specific gated fixes (Recommended)
  2. Leave as residual work
  3. Report only -- no further action
  ```

  **When only `manual` findings remain (no `gated_auto`):**
  ```
  Safe fixes have been applied. The remaining findings need manual resolution. What should I do?
  1. Leave as residual work (Recommended)
  2. Report only -- no further action
  ```

  If no blocking question tool is available, present the applicable numbered options as text and wait for the user's selection.
- If no `gated_auto` or `manual` findings remain after safe fixes, skip the policy question entirely.
- Only include `gated_auto` findings in the fixer queue after the user explicitly approves the specific items.

**Autofix mode:**
- Ask no questions.
- Apply only the `safe_auto -> review-fixer` queue.
- Leave `gated_auto`, `manual`, `human`, and `release` items unresolved.

**Report-only mode:**
- Ask no questions.
- Do not build a fixer queue.
- Do not create residual todos or `.context` artifacts.
- Stop after Stage 6.

**Headless mode:**
- Ask no questions.
- Apply only the `safe_auto -> review-fixer` queue in a single pass. Do not enter the bounded re-review loop.
- Leave `gated_auto`, `manual`, `human`, and `release` items unresolved.
- Output the headless output envelope.
- Write a run artifact but do not create todo files.
- Stop after the structured text output and "Review complete" signal.

#### Step 3: Apply Fixes with One Fixer and Bounded Rounds

- Spawn exactly one fixer subagent for the current fixer queue. That fixer applies all approved changes and runs the relevant targeted tests in one pass.
- Do not fan out multiple fixers against the same checkout.
- Re-review only the changed scope after fixes land.
- Bound the loop with `max_rounds: 2`. If issues remain after the second round, stop and hand them off as residual work.
- If any applied finding has `requires_verification: true`, the round is incomplete until the targeted verification runs.
- Do not start a mutating review round concurrently with browser testing on the same checkout.

#### Step 4: Emit Artifacts and Downstream Handoff

- In interactive, autofix, and headless modes, write a per-run artifact under `.context/compound-engineering/ce-review/<run-id>/` containing: synthesized findings, applied fixes, residual actionable work, advisory-only outputs.
- In autofix mode, create durable todo files only for unresolved actionable findings whose final owner is `downstream-resolver`. Map finding severity to todo priority: `P0`/`P1` → `p1`, `P2` → `p2`, `P3` → `p3`. Set `status: ready`.
- Do not create todos for `advisory` findings, `owner: human`, `owner: release`, or protected-artifact cleanup suggestions.

#### Step 5: Final Next Steps (Interactive Mode Only)

After the fix-review cycle completes, offer next steps based on the entry mode. Reuse the resolved review base/default branch from Stage 1:

- **PR mode** (entered via PR number/URL):
  - **Push fixes** — push commits to the existing PR branch
  - **Exit** — done for now

- **Branch mode** (feature branch with no PR, and not the resolved review base/default branch):
  - **Create a PR (Recommended)** — push and open a pull request
  - **Continue without PR** — stay on the branch
  - **Exit** — done for now

- **On the resolved review base/default branch:**
  - **Continue** — proceed with next steps
  - **Exit** — done for now

If "Create a PR": first publish the branch with `git push --set-upstream origin HEAD`, then use `gh pr create` with a title and summary derived from the branch changes.
If "Push fixes": push the branch with `git push` to update the existing PR.

Autofix, report-only, and headless modes: stop after the report, artifact emission, and residual-work handoff.

## Language-Aware Conditionals

This skill uses stack-specific reviewer agents when the diff clearly warrants them. Keep those agents opinionated. They are not generic language checkers; they add a distinct review lens on top of the always-on and cross-cutting personas.

Do not spawn them mechanically from file extensions alone. The trigger is meaningful changed behavior, architecture, or UI state in that stack.

## Fallback

If the platform doesn't support parallel sub-agents, run reviewers sequentially. Everything else (stages, output format, merge pipeline) stays the same.

## Quality Gates

Before delivering the review, verify:

1. **Every finding is actionable.** If a finding says "consider", "might want to", or "could be improved" without a concrete fix, rewrite it with a specific action.
2. **No false positives from skimming.** For each finding, verify the surrounding code was actually read. Check that the "bug" isn't handled elsewhere in the same function, that the "unused import" isn't used in a type annotation, that the "missing null check" isn't guarded by the caller.
3. **Severity is calibrated.** A style nit is never P0. A SQL injection is never P3. Re-check every severity assignment.
4. **Line numbers are accurate.** Verify each cited line number against the file content.
5. **Protected artifacts are respected.** Discard any findings that recommend deleting or gitignoring files in `docs/brainstorms/`, `docs/plans/`, or `docs/solutions/`.
6. **Findings don't duplicate linter output.** Don't flag things the project's linter/formatter would catch. Focus on semantic issues.

**Anti-pattern check:** Before delivering the report, verify the findings sections use pipe-delimited table rows, not freeform text blocks separated by horizontal rules.

## Outputs

- Pipe-delimited markdown review report (interactive mode) or structured text envelope (headless mode)
- Applied safe_auto fixes (when mode allows mutation)
- Run artifact under `.context/compound-engineering/ce-review/<run-id>/`
- Optional: todo files for unresolved actionable findings (autofix mode only)
- Optional: pushed branch or new PR (interactive mode only)

## Feeds Into

- `ce:compound` — for documenting any bugs discovered during review
- `ce:work` — for implementing gated or manual fixes
