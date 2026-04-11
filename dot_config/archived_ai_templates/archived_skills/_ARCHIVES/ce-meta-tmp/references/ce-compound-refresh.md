# ce:compound-refresh

> Maintain the quality of `docs/solutions/` over time by reviewing, updating, consolidating, replacing, or deleting learning docs against the current codebase.

## When to Use

- After refactors, migrations, renames, or dependency upgrades that likely invalidated existing docs
- When a retrieved learning feels outdated or wrong
- When a recently solved problem contradicts an existing learning
- When pattern docs no longer reflect current code
- When multiple docs seem to cover the same topic and might benefit from consolidation
- When invoked by `ce:compound` with a scope hint (targeted maintenance follow-up)

## Inputs

- Optional scope hint (argument): specific file, module name, component name, category name, or pattern topic
- `docs/solutions/` directory with existing learning docs and pattern docs
- The current codebase (for cross-referencing)
- `MEMORY.md` from the auto memory directory (supplementary drift signals)

## Methodology

### Mode Detection

Check whether arguments contain `mode:autofix`. If present, strip it from arguments (use the remainder as a scope hint) and run in **autofix mode**.

| Mode | When | Behavior |
|------|------|----------|
| **Interactive** (default) | User is present and can answer questions | Ask for decisions on ambiguous cases, confirm actions |
| **Autofix** | `mode:autofix` in arguments | No user interaction. Apply all unambiguous actions. Mark ambiguous cases as stale. Generate a summary report at the end. |

**Autofix mode rules:**
- Skip all user questions. Never pause for input.
- Process all docs in scope. No scope narrowing questions.
- Attempt all safe actions: Keep (no-op), Update (fix references), Consolidate (merge and delete subsumed doc), auto-Delete (unambiguous criteria met), Replace (when evidence is sufficient). If a write succeeds, record it as **applied**. If a write fails, record the action as **recommended** in the report and continue.
- Mark as stale when uncertain. If classification is genuinely ambiguous, mark with `status: stale`, `stale_reason`, and `stale_date` in frontmatter. If even the stale-marking write fails, include it as a recommendation.
- Use conservative confidence. Borderline cases get marked stale, not actioned.
- Always generate a report. The report has two sections: **Applied** (successful writes) and **Recommended** (could not be written). Print it in full.

### Interaction Principles (Interactive Mode Only)

- Ask questions one at a time using a blocking question mechanism when available; otherwise present numbered options in plain text and wait for reply
- Prefer multiple choice when natural options exist
- Start with scope and intent, then narrow only when needed
- Do not ask the user to make decisions before you have evidence
- Lead with a recommendation and explain it briefly

### Refresh Order

1. Review relevant individual learning docs first
2. Note which learnings stayed valid, were updated, were consolidated, were replaced, or were deleted
3. Then review any pattern docs that depend on those learnings

Why: learning docs are primary evidence; pattern docs are derived. Stale learnings can make a pattern look more valid than it really is. If the user starts by naming a pattern doc, you may begin there to understand the concern, but inspect the supporting learning docs before changing the pattern.

### Maintenance Model

For each candidate artifact, classify it into one of five outcomes:

| Outcome | Meaning | Default action |
|---------|---------|----------------|
| **Keep** | Still accurate and still useful | No file edit by default; report that it was reviewed and remains trustworthy |
| **Update** | Core solution is still correct, but references drifted | Apply evidence-backed in-place edits |
| **Consolidate** | Two or more docs overlap heavily but are both correct | Merge unique content into the canonical doc, delete the subsumed doc |
| **Replace** | The old artifact is now misleading, but there is a known better replacement | Create a trustworthy successor, then delete the old artifact |
| **Delete** | No longer useful, applicable, or distinct | Delete the file — git history preserves it if anyone needs to recover it later |

### Core Rules

1. **Evidence informs judgment.** The signals below are inputs, not a mechanical scorecard. Use engineering judgment to decide whether the artifact is still trustworthy.
2. **Prefer no-write Keep.** Do not update a doc just to leave a review breadcrumb.
3. **Match docs to reality, not the reverse.** When current code differs from a learning, update the learning to reflect the current code. Do not ask the user whether code changes were "intentional" or "a regression" — that is outside this workflow.
4. **Be decisive, minimize questions.** When evidence is clear (file renamed, class moved, reference broken), apply the update. In interactive mode, only ask when the right action is genuinely ambiguous. In autofix mode, mark ambiguous cases as stale.
5. **Avoid low-value churn.** Do not edit a doc just to fix a typo, polish wording, or make cosmetic changes that do not materially improve accuracy or usability.
6. **Use Update only for meaningful, evidence-backed drift.** Paths, module names, related links, category metadata, code snippets, and clearly stale wording are fair game when fixing them materially improves accuracy.
7. **Use Replace only when there is a real replacement.** That means either:
   - the current conversation contains a recently solved, verified replacement fix, or
   - the user has provided enough concrete replacement context, or
   - the codebase investigation found the current approach and can document it as the successor, or
   - newer docs, pattern docs, PRs, or issues provide strong successor evidence.
8. **Delete when the code is gone.** If the referenced code, controller, or workflow no longer exists in the codebase and no successor can be found, delete the file. A learning about a deleted feature misleads readers. Missing referenced files with no matching code is **not** a doubt case — it is strong, unambiguous Delete evidence. Auto-delete it.
9. **Evaluate document-set design, not just accuracy.** In addition to checking whether each doc is accurate, evaluate whether it is still the right unit of knowledge. If two or more docs overlap heavily, determine whether they should remain separate, be cross-scoped more clearly, or be consolidated.
10. **Delete, don't archive.** There is no `_archived/` directory. When a doc is no longer useful, delete it. Git history is the archive. If someone needs a deleted doc, `git log --diff-filter=D -- docs/solutions/` will find it.

### Scope Selection

Start by discovering learnings and pattern docs under `docs/solutions/`.

**Exclude:**
- `README.md` files
- `docs/solutions/_archived/` (legacy — if this directory exists, flag it for cleanup in the report)

If arguments are provided, narrow scope using these matching strategies in order, stopping at the first that produces results:
1. **Directory match** — check if the argument matches a subdirectory name under `docs/solutions/`
2. **Frontmatter match** — search `module`, `component`, or `tags` fields in learning frontmatter
3. **Filename match** — match against filenames (partial matches are fine)
4. **Content search** — search file contents for the argument as a keyword

If no matches are found, report that and ask the user to clarify. In autofix mode, report the miss and stop.

If no candidate docs are found at all, report:
```text
No candidate docs found in docs/solutions/.
Run ce:compound after solving problems to start building your knowledge base.
```

### Phase 0: Assess and Route

Before asking the user to classify anything:
1. Discover candidate artifacts
2. Estimate scope
3. Choose the lightest interaction path that fits

**Route by Scope:**

| Scope | When to use it | Interaction style |
|-------|----------------|-------------------|
| **Focused** | 1-2 likely files or user named a specific doc | Investigate directly, then present a recommendation |
| **Batch** | Up to ~8 mostly independent docs | Investigate first, then present grouped recommendations |
| **Broad** | 9+ docs, ambiguous, or repo-wide stale-doc sweep | Triage first, then investigate in batches |

**Broad Scope Triage** (when 9+ candidate docs):
1. **Inventory** — read frontmatter of all candidate docs, group by module/component/category
2. **Impact clustering** — identify areas with the densest clusters of learnings + pattern docs
3. **Spot-check drift** — for each cluster, check whether the primary referenced files still exist
4. **Recommend a starting area** — present the highest-impact cluster with a brief rationale and ask the user to confirm or redirect. In autofix mode, skip the question and process all clusters in impact order.

Example:
```text
Found 24 learnings across 5 areas.

The auth module has 5 learnings and 2 pattern docs that cross-reference
each other — and 3 of those reference files that no longer exist.
I'd start there.

1. Start with auth (recommended)
2. Pick a different area
3. Review everything
```

Do not ask action-selection questions yet. First gather evidence.

### Phase 1: Investigate Candidate Learnings

For each learning in scope, read it, cross-reference its claims against the current codebase, and form a recommendation.

**Dimensions that can independently go stale:**
- **References** — do file paths, class names, and modules still exist or have they moved?
- **Recommended solution** — does the fix still match how the code actually works today?
- **Code examples** — if the learning includes code snippets, do they still reflect the current implementation?
- **Related docs** — are cross-referenced learnings and patterns still present and consistent?
- **Auto memory** — read `MEMORY.md` from the auto memory directory if it exists. A memory note describing a different approach than what the learning recommends is a supplementary drift signal.
- **Overlap** — while investigating, note when another doc in scope covers the same problem domain, references the same files, or recommends a similar solution. For each overlap, record: the two file paths, which dimensions overlap (problem, solution, root cause, files, prevention), and which doc appears broader or more current. These signals feed Phase 1.75.

Match investigation depth to the learning's specificity — a learning referencing exact file paths and code snippets needs more verification than one describing a general principle.

#### Drift Classification: Update vs Replace

- **Update territory** — file paths moved, classes renamed, links broke, metadata drifted, but the core recommended approach is still how the code works.
- **Replace territory** — the recommended solution conflicts with current code, the architectural approach changed, or the pattern is no longer the preferred way.

**The boundary:** if you find yourself rewriting the solution section or changing what the learning recommends, stop — that is Replace, not Update.

**Memory-sourced drift signals are supplementary, not primary.** A memory note describing a different approach does not alone justify Replace or Delete. Use memory signals to corroborate codebase-sourced drift or prompt deeper investigation. In autofix mode, memory-only drift (no codebase corroboration) should result in stale-marking, not action.

#### Judgment Guidelines

1. **Contradiction = strong Replace signal.** If the learning's recommendation conflicts with current code patterns or a recently verified fix, the learning is actively misleading. Classify as Replace.
2. **Age alone is not a stale signal.** A 2-year-old learning that still matches current code is fine.
3. **Check for successors before deleting.** Before recommending Replace or Delete, look for newer learnings, pattern docs, PRs, or issues. If successor evidence exists, prefer Replace over Delete.

### Phase 1.5: Investigate Pattern Docs

After reviewing the underlying learning docs, investigate any relevant pattern docs under `docs/solutions/patterns/`.

Pattern docs are high-leverage — a stale pattern is more dangerous than a stale individual learning because future work may treat it as broadly applicable guidance. A pattern doc with no clear supporting learnings is a stale signal.

### Phase 1.75: Document-Set Analysis

After investigating individual docs, step back and evaluate the document set as a whole.

**Overlap Detection** — for docs sharing the same module, component, tags, or problem domain, compare across:
- Problem statement — do they describe the same underlying problem?
- Solution shape — do they recommend the same approach?
- Referenced files — do they point to the same code paths?
- Prevention rules — do they repeat the same prevention bullets?
- Root cause — do they identify the same root cause?

High overlap across 3+ dimensions is a strong Consolidate signal.

**Supersession Signals:**
- A newer doc covers the same files, same workflow, and broader runtime behavior than an older doc
- An older doc describes a specific incident that a newer doc generalizes into a pattern
- Two docs recommend the same fix but the newer one has better context, examples, or scope

**Canonical Doc Identification** — for each topic cluster, identify the doc that is the canonical source of truth. All other docs in the cluster are either:
- **Distinct** — cover a meaningfully different sub-problem. Keep separate.
- **Subsumed** — their unique content fits as a section in the canonical doc. Consolidate.
- **Redundant** — add nothing the canonical doc doesn't already say. Delete.

**Retrieval-Value Test** — before recommending that two docs stay separate, ask: "If a maintainer searched for this topic six months from now, would having these as separate docs improve discoverability, or just create drift risk?"

Separate docs earn their keep only when:
- They cover genuinely different sub-problems that someone might search for independently
- They target different audiences or contexts
- Merging them would create an unwieldy doc

**Cross-Doc Conflict Check** — look for outright contradictions between docs. Contradictions are more urgent than individual staleness.

### Subagent Strategy

| Approach | When to use |
|----------|-------------|
| **Main thread only** | Small scope, short docs |
| **Sequential subagents** | 1-2 artifacts with many supporting files to read |
| **Parallel subagents** | 3+ truly independent artifacts with low overlap |
| **Batched subagents** | Broad sweeps — narrow scope first, then investigate in batches |

**Two subagent roles:**
1. **Investigation subagents** — read-only. They must not edit files, create successors, or delete anything. Each returns: file path, evidence, recommended action, confidence, and open questions. Can run in parallel when artifacts are independent.
2. **Replacement subagents** — write a single new learning to replace a stale one. These run **one at a time, sequentially**. The orchestrator handles all deletions and metadata updates after each replacement completes.

When spawning any subagent, include this instruction in its task prompt:
> Use dedicated file search and read tools for all investigation. Do NOT use shell commands (ls, find, cat, grep, test, bash) for file operations.
> Also read MEMORY.md from the auto memory directory if it exists. Report any memory-sourced drift signals separately, tagged with "(auto memory [claude])". If MEMORY.md does not exist or is empty, skip this check.

The orchestrator merges investigation results, detects contradictions, coordinates replacement subagents, and performs all deletions/metadata edits centrally.

### Phase 2: Classify the Right Maintenance Action

#### Keep
The learning is still accurate and useful. Do not edit the file. Report that it was reviewed and remains trustworthy.

#### Update
The core solution is still valid but references have drifted. Apply the fixes directly.

**Valid in-place updates:**
- Rename file path references (e.g., `app/models/auth_token.rb` → `app/models/session_token.rb`)
- Update module names
- Fix outdated links to related docs
- Refresh implementation notes after a directory move

**NOT in-place updates (require Replace instead):**
- Rewording prose for style alone
- The old fix is now an anti-pattern
- The system architecture changed enough that the old guidance is misleading
- The troubleshooting path is materially different

#### Consolidate
Choose **Consolidate** when Phase 1.75 identified docs that overlap heavily but are both materially correct.

**When to consolidate:**
- Two docs describe the same problem and recommend the same (or compatible) solution
- One doc is a narrow precursor and a newer doc covers the same ground more broadly
- The unique content from the subsumed doc can fit as a section or addendum in the canonical doc
- Keeping both creates drift risk without meaningful retrieval benefit

**When NOT to consolidate** (apply the Retrieval-Value Test from Phase 1.75):
- The docs cover genuinely different sub-problems that someone would search for independently
- Merging would create an unwieldy doc

**Consolidate vs Delete:** If the subsumed doc has unique content worth preserving, use Consolidate to merge that content first. If the subsumed doc adds nothing, skip straight to Delete.

**Consolidate action:**
1. Confirm the canonical doc (broader, more current, more accurate)
2. Extract unique content from the subsumed doc
3. Merge unique content into the canonical doc in a natural location
4. Update cross-references — if any other docs reference the subsumed doc, update those references to point to the canonical doc
5. Delete the subsumed doc. Not archive — delete.

If a doc cluster has 3+ overlapping docs, process pairwise: consolidate the two most overlapping docs first, then evaluate the merged result against the next.

**Structural edits:** Consolidate also covers splitting an unwieldy doc that covers multiple distinct problems into separate docs — only when the sub-topics are genuinely independent.

#### Replace
Choose **Replace** when the learning's core guidance is now misleading.

**Evidence assessment:**
- **Sufficient evidence** — you understand both what the old learning recommended AND what the current approach is → Proceed to write the replacement
- **Insufficient evidence** — the drift is so fundamental you cannot confidently document the current approach → Mark as stale in place:
  - Add `status: stale`, `stale_reason: [what you found]`, `stale_date: YYYY-MM-DD` to frontmatter
  - Report what evidence was found and what is missing
  - Recommend the user run `ce:compound` after their next encounter with that area

**Replace Flow** (process one at a time, sequentially):
When evidence is sufficient, delegate to a single replacement subagent. Pass it:
- The old learning's full content
- A summary of the investigation evidence
- The target path and category
- Contents of `references/schema.yaml`, `references/yaml-schema.md`, and `assets/resolution-template.md`

After the subagent completes, the orchestrator deletes the old learning file. The new learning's frontmatter may optionally include `supersedes: [old learning filename]`.

#### Delete
Choose **Delete** when:
- The code or workflow no longer exists and the problem domain is gone
- The learning is obsolete and has no modern replacement worth documenting
- The learning is fully redundant with another doc
- There is no meaningful successor evidence suggesting it should be replaced instead

**Before deleting: check if the problem domain is still active.** When a learning's referenced files are gone, that is strong evidence the implementation is gone — but not necessarily the problem domain:
- Implementation gone + problem domain gone → **Delete**
- Implementation gone + problem domain still active (app still does auth, still processes payments) → **Replace** not Delete

**Auto-delete only when both the implementation AND the problem domain are gone:**
- the referenced code is gone AND the application no longer deals with that problem domain
- the learning is fully superseded by a clearly better successor AND the old doc adds no distinct value
- the document is plainly redundant and adds nothing the canonical doc doesn't already say

Do not keep a learning just because its general advice is "still sound" — if the specific code it references is gone, the learning misleads readers.

### Phase 3: Ask for Decisions

#### Autofix mode
Skip this entire phase. Proceed directly to Phase 4.

#### Interactive mode
Most Updates and Consolidations should be applied directly without asking. Only ask the user when:
- The right action is genuinely ambiguous (Update vs Replace vs Consolidate vs Delete)
- You are about to Delete a document and the evidence is not unambiguous
- You are about to Consolidate and the choice of canonical doc is not clear-cut
- You are about to create a successor via Replace

Always present choices using a blocking question mechanism when available; otherwise present numbered options in plain text and wait for the user's reply.

**Question rules:**
- Ask one question at a time
- Prefer multiple choice
- Lead with the recommended option
- Explain the rationale in one concise sentence
- Avoid asking the user to choose from actions that are not actually plausible

**Focused Scope question format:**
```text
This [learning/pattern] looks like a [Keep/Update/Consolidate/Replace/Delete].

Why: [one-sentence rationale based on the evidence]

What would you like to do?

1. [Recommended action]
2. [Second plausible action]
3. Skip for now
```

**Batch Scope questions:**
1. Confirm grouped Keep/Update recommendations
2. Then handle Consolidate groups
3. Then handle Replace one at a time
4. Then handle Delete one at a time unless strong auto-delete criteria are met

**Broad Scope:**
- Narrow scope first
- Investigate a manageable batch
- Present recommendations
- Ask whether to continue to the next batch

### Phase 4: Execute the Chosen Action

(See Maintenance Model section above for Keep, Update, Consolidate, Replace, and Delete flows.)

### Pattern Guidance

Apply the same five outcomes (Keep, Update, Consolidate, Replace, Delete) to pattern docs, but evaluate them as **derived guidance** rather than incident-level learnings. Key differences:
- **Keep**: the underlying learnings still support the generalized rule and examples remain representative
- **Update**: the rule holds but examples, links, scope, or supporting references drifted
- **Consolidate**: two pattern docs generalize the same set of learnings or cover the same design concern
- **Replace**: the generalized rule is now misleading, or the underlying learnings support a different synthesis. Base the replacement on the refreshed learning set — do not invent new rules from guesswork
- **Delete**: the pattern is no longer valid, no longer recurring, or fully subsumed by a stronger pattern doc

### Discoverability Check

After the refresh report is generated, check whether the project's instruction files would lead an agent to discover and search `docs/solutions/`. (Same check as in `ce:compound` — see that skill for the full procedure.)

In interactive mode, show the proposed change and ask for consent before editing.
In autofix mode, include as a "Discoverability recommendation" line in the report — do not attempt to edit instruction files.

If the check produces edits, amend or create a follow-up commit after Phase 5.

### Phase 5: Commit Changes

Skip this phase if no files were modified.

**Detect git context before offering options:**
1. Which branch is currently checked out (main/master vs feature branch)
2. Whether the working tree has other uncommitted changes beyond what compound-refresh modified
3. Recent commit messages to match the repo's commit style

**Autofix mode defaults:**

| Context | Default action |
|---------|---------------|
| On main/master | Create a branch named for what was refreshed (e.g., `docs/refresh-auth-and-ci-learnings`), commit, attempt to open a PR. If PR creation fails, report the branch name. |
| On a feature branch | Commit as a separate commit on the current branch |
| Git operations fail | Include recommended git commands in the report and continue |

Stage only the files that compound-refresh modified — not other dirty files in the working tree.

**Interactive mode options:**

If the current branch is main/master/default:
1. Create a branch, commit, and open a PR (recommended) — branch name should be specific (e.g., `docs/refresh-auth-learnings` not `docs/compound-refresh`)
2. Commit directly to `{current branch name}`
3. Don't commit — I'll handle it

If the current branch is a feature branch, clean working tree:
1. Commit to `{current branch name}` as a separate commit (recommended)
2. Create a separate branch and commit
3. Don't commit

If the current branch is a feature branch, dirty working tree (other uncommitted changes):
1. Commit only the compound-refresh changes to `{current branch name}` (selective staging — other dirty files stay untouched)
2. Don't commit

**Commit message:** Summarize what was refreshed (e.g., "update 3 stale learnings, consolidate 2 overlapping docs, delete 1 obsolete doc"). Follow the repo's existing commit conventions.

## Quality Gates

Before declaring done, verify the full report has been printed in markdown output (not summarized internally). The report is the deliverable — print every section in full.

**Report format:**
```text
Compound Refresh Summary
========================
Scanned: N learnings

Kept: X
Updated: Y
Consolidated: C
Replaced: Z
Deleted: W
Skipped: V
Marked stale: S
```

Then for EVERY file processed, list:
- The file path
- The classification (Keep/Update/Consolidate/Replace/Delete/Stale)
- What evidence was found (tag memory-sourced findings with "(auto memory [claude])")
- What action was taken (or recommended)
- For Consolidate: which doc was canonical, what unique content was merged, what was deleted

For **Keep** outcomes, list them under a reviewed-without-edits section.

**Autofix mode report sections:**

**Applied** (writes that succeeded):
- For each Updated file: file path, what references were fixed, and why
- For each Consolidated cluster: canonical doc, what unique content was merged from each subsumed doc, and the subsumed docs that were deleted
- For each Replaced file: what the old learning recommended vs what the current code does, and the path to the new successor
- For each Deleted file: file path and why it was removed
- For each Marked stale file: file path, what evidence was found, and why it was ambiguous

**Recommended** (actions that could not be written — e.g., permission denied):
- Same detail as above, framed as recommendations for a human to apply

**Legacy cleanup** (if `docs/solutions/_archived/` exists): list archived files found and recommend disposition.

## Outputs

- Updated, consolidated, replaced, or deleted docs in `docs/solutions/`
- Full refresh summary report (markdown)
- Optional discoverability edit to project instruction files
- Optional commit/PR on the modified docs

## Feeds Into

- `ce:compound` — run `ce:compound` after the next encounter with any area marked as stale (when evidence was insufficient for Replace)
