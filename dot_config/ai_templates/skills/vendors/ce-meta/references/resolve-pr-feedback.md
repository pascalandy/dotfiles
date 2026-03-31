# Resolve PR Review Feedback

> Evaluate and fix PR review feedback, then reply and resolve threads — spawning parallel subagents for each thread.

> **Agent time is cheap. Tech debt is expensive.**
> Fix everything valid — including nitpicks and low-priority items. If we're already in the code, fix it rather than punt it.

## When to Use

- Addressing PR review comments
- Resolving review threads in bulk or targeting a single comment
- Fixing code review feedback after a reviewer has submitted changes requested

## Inputs

| Argument | Mode |
|----------|------|
| No argument | **Full** — all unresolved threads on the current branch's PR |
| PR number (e.g., `123`) | **Full** — all unresolved threads on that PR |
| Comment/thread URL | **Targeted** — only that specific thread |

## Methodology

---

## Full Mode

### 1. Fetch Unresolved Threads

If no PR number was provided, detect it from the current branch:
```bash
gh pr view --json number -q .number
```

Then fetch all feedback via GraphQL (see Scripts section). The query returns a JSON object with three keys:

| Key | Contents | Has file/line? | Resolvable? |
|-----|----------|---------------|-------------|
| `review_threads` | Unresolved, non-outdated inline code review threads | Yes | Yes (GraphQL) |
| `pr_comments` | Top-level PR conversation comments (excludes PR author) | No | No |
| `review_bodies` | Review submission bodies with non-empty text (excludes PR author) | No | No |

**Fallback if GraphQL script fails:**
```bash
gh pr view PR_NUMBER --json reviews,comments
gh api repos/{owner}/{repo}/pulls/PR_NUMBER/comments
```

---

### 2. Triage: Separate New from Pending

Classify each piece of feedback as **new** or **already handled** before processing.

**Review threads:** Read the thread's comments. Rules:
- If there is a substantive reply that acknowledges the concern but defers action (e.g., "need to align on this", "going to think through this", or a reply presenting options without resolving) → **pending decision** — do not re-process
- If there are only the original reviewer comment(s) with no substantive response → **new**

**PR comments and review bodies:** These have no resolve mechanism and reappear every run.
- Check the PR conversation for an existing reply that quotes and addresses the feedback
- If a reply already exists → skip
- If not → **new**

The distinction is about content, not who posted. A deferral from a teammate, a previous skill run, or a manual reply all count as already handled.

**If there are no new items across all feedback types**, skip steps 3–8 and go directly to step 9.

---

### 3. Cluster Analysis (Gated)

This step only runs when at least one gate signal fires. Skip to step 4 if neither fires.

| Gate signal | Check |
|---|---|
| **Volume** | 4+ new items from triage |
| **Verify-loop re-entry** | This is the 2nd+ pass through the workflow (new feedback appeared after a previous fix round) |

The common case (1–3 unrelated comments) skips this step entirely with zero overhead.

**If the gate fires**, analyze feedback for thematic clusters:

**Step 3a — Assign concern categories.** Use exactly this fixed list: `error-handling`, `validation`, `type-safety`, `naming`, `performance`, `testing`, `security`, `documentation`, `style`, `architecture`, `other`. Each new item gets exactly one category based on what the feedback is about.

**Step 3b — Group by category + spatial proximity.** Two items form a potential cluster when they share a concern category AND are spatially proximate:

| Thematic match | Spatial proximity | Action |
|---|---|---|
| Same category | Same file | Cluster |
| Same category | Same directory subtree | Cluster |
| Same category | Unrelated locations | No cluster |
| Different categories | Any | No cluster (same-file grouping still applies for conflict avoidance) |

**Step 3c — Synthesize a cluster brief** for each cluster of 2+ items. Pass briefs to subagents using a `<cluster-brief>` XML block:

```xml
<cluster-brief>
  <theme>[concern category]</theme>
  <area>[common directory path]</area>
  <files>[comma-separated file paths]</files>
  <threads>[comma-separated thread/comment IDs]</threads>
  <hypothesis>[one sentence: what the individual comments collectively suggest about a deeper issue]</hypothesis>
</cluster-brief>
```

On verify-loop re-entry, add context about the previous cycle:
```xml
<cluster-brief>
  ...
  <just-fixed-files>[files modified in the previous fix cycle]</just-fixed-files>
</cluster-brief>
```

**Step 3d — Items not in any cluster** remain as individual items and are dispatched normally in step 5.

**Step 3e — If no clusters are found** after analysis (gate fired but items don't form thematic+spatial groups), proceed with all items as individual. The gate was a false positive — only cost was the analysis.

---

### 4. Plan

Create a task list of all **new** unresolved items grouped by type:
- Code changes requested
- Questions to answer
- Style/convention fixes
- Test additions needed

If step 3 produced clusters, include them in the task list alongside individual items.

---

### 5. Implement (PARALLEL)

Process all three feedback types. Review threads are primary; PR comments and review bodies are secondary but must not be ignored.

#### Individual dispatch (default)

**For `review_threads`:** Delegate a `pr-comment-resolver` subagent for each thread NOT assigned to a cluster. Clustered threads are handled by cluster dispatch — do not dispatch them individually.

Each subagent receives:
- The thread ID
- The file path and line number
- The full comment text (all comments in the thread)
- The PR number (for context)
- The feedback type (`review_thread`)

**For `pr_comments` and `review_bodies`:** These lack file/line context. Delegate a `pr-comment-resolver` subagent for each actionable non-clustered item. The subagent receives the comment ID, body text, PR number, and feedback type (`pr_comment` or `review_body`). The subagent must identify relevant files from the comment text and the PR diff.

#### Cluster dispatch

For each cluster identified in step 3, delegate ONE `pr-comment-resolver` subagent that receives:
- The `<cluster-brief>` XML block
- All thread details for threads in the cluster (IDs, file paths, line numbers, comment text)
- The PR number
- The feedback types

The cluster subagent reads the broader area before making targeted fixes. It returns one summary per thread it handled (same structure as individual subagents), plus a `cluster_assessment` field.

#### Subagent return format

Each subagent returns:
- **verdict**: `fixed`, `fixed-differently`, `replied`, `not-addressing`, or `needs-human`
- **feedback_id**: the thread ID or comment ID it handled
- **feedback_type**: `review_thread`, `pr_comment`, or `review_body`
- **reply_text**: the markdown reply to post (quoting the relevant part of the original feedback)
- **files_changed**: list of files modified (empty if replied/not-addressing)
- **reason**: brief explanation of what was done or why it was skipped

Cluster subagents additionally return:
- **cluster_assessment**: what the broader investigation found, whether a holistic or individual approach was taken

**Verdict meanings:**
- `fixed` — code change made as requested
- `fixed-differently` — code change made, but with a better approach than suggested
- `replied` — no code change needed; answered a question, acknowledged feedback, or explained a design decision
- `not-addressing` — feedback is factually wrong about the code; skip with evidence
- `needs-human` — cannot determine the right action; needs user decision

#### Batching and conflict avoidance

**Batching:** Clusters count as 1 dispatch unit regardless of how many threads they contain.
- 1–4 dispatch units total: dispatch all in parallel
- 5+ dispatch units: batch in groups of 4

**Conflict avoidance:** No two dispatch units that touch the same file should run in parallel. Before dispatching, check for file overlaps across all dispatch units (clusters and individual items).
- If a cluster's file list overlaps with an individual item's file, or with another cluster's files → serialize those units (dispatch one, wait for completion, then dispatch the next)
- Non-overlapping units can still run in parallel
- Within a single dispatch unit handling multiple threads on the same file, the subagent addresses them sequentially

**Sequential fallback:** Platforms that do not support parallel dispatch should run subagents sequentially. Dispatch cluster units first (higher-leverage), then individual items.

Fixes can occasionally expand beyond their referenced file (e.g., renaming a method updates callers elsewhere). The verification step (step 8) catches this — if re-fetching shows unresolved threads or the commit reveals inconsistent changes, re-run the affected subagents sequentially.

---

### 6. Commit and Push

After all subagents complete, check whether any files were actually changed. If all verdicts are `replied`, `not-addressing`, or `needs-human` (no code changes), skip this step and proceed to step 7.

If there are file changes:

1. Stage only files reported by subagents and commit:
```bash
git add [files from subagent summaries]
git commit -m "Address PR review feedback (#PR_NUMBER)

- [list changes from subagent summaries]"
```

2. Push to remote:
```bash
git push
```

---

### 7. Reply and Resolve

After push succeeds, post replies and resolve where applicable.

#### Reply format

All replies must quote the relevant part of the original feedback. Quote the specific sentence or passage being addressed, not the entire comment if it's long.

**For fixed items:**
```markdown
> [quoted relevant part of original feedback]

Addressed: [brief description of the fix]
```

**For items not addressed:**
```markdown
> [quoted relevant part of original feedback]

Not addressing: [reason with evidence, e.g., "null check already exists at line 85"]
```

For `needs-human` verdicts: post the reply but do NOT resolve the thread. Leave it open for human input.

#### Review threads

**Reply** (body read from stdin to avoid shell escaping issues):
```bash
echo "REPLY_TEXT" | gh api graphql -f threadId="$THREAD_ID" -f body="$(cat)" -f query='
mutation ReplyToReviewThread($threadId: ID!, $body: String!) {
  addPullRequestReviewThreadReply(input: {
    pullRequestReviewThreadId: $threadId
    body: $body
  }) {
    comment { id url }
  }
}'
```

**Resolve:**
```bash
gh api graphql -f threadId="$THREAD_ID" -f query='
mutation ResolveReviewThread($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { id isResolved path line }
  }
}'
```

#### PR comments and review bodies

These cannot be resolved via GitHub's API. Reply with a top-level PR comment referencing the original:

```bash
gh pr comment PR_NUMBER --body "REPLY_TEXT"
```

Include enough quoted context in the reply so the reader can follow which comment is being addressed without scrolling.

---

### 8. Verify

Re-fetch feedback to confirm resolution:

```bash
# Re-run the get-pr-comments GraphQL query for PR_NUMBER
```

The `review_threads` array should be empty (except `needs-human` items).

**If new threads remain**, check the iteration count:

- **First or second fix-verify cycle:** Record which files were modified and which concern categories were addressed in this cycle. Repeat from step 2 for remaining threads. The cluster analysis gate (step 3) will fire on re-entry because verify-loop re-entry is a gate signal, enabling broader investigation of recurring patterns.

- **After the second fix-verify cycle (3rd pass would begin):** Stop looping. Surface remaining issues to the user with context: *"Multiple rounds of feedback on [area/theme] suggest a deeper issue. Here's what we've fixed so far and what keeps appearing."* Use the `needs-human` escalation pattern — leave threads open and present the pattern for the user to decide.

PR comments and review bodies have no resolve mechanism, so they will still appear in output. Verify they were replied to by checking the PR conversation.

---

### 9. Summary

Present a concise summary of all work done. Group by verdict, one line per item describing *what was done*, not just *where*.

```
Resolved N of M new items on PR #NUMBER:

Fixed (count): [brief description of each fix]
Fixed differently (count): [what was changed and why the approach differed]
Replied (count): [what questions were answered]
Not addressing (count): [what was skipped and why]
```

**If clusters were investigated**, append:
```
Cluster investigations (count):

1. [theme] in [area]: [cluster_assessment from the subagent —
   what was found, whether a holistic or individual approach was taken]
```

**If any subagent returned `needs-human`**, append a decisions section. Each `needs-human` subagent returns a `decision_context` field with: what the reviewer said, what the subagent investigated, why it needs a decision, concrete options with tradeoffs, and the subagent's lean if it has one. Present it directly:

```
Needs your input (count):

1. [decision_context from the subagent — includes quoted feedback,
   investigation findings, why it needs a decision, options with
   tradeoffs, and the subagent's recommendation if any]
```

The `needs-human` threads already have a natural-sounding acknowledgment reply posted and remain open on the PR.

**If there are pending decisions from a previous run** (threads detected in step 2 as already responded to but still unresolved), surface them after the new work:

```
Still pending from a previous run (count):

1. [Thread path:line] — [brief description of what's pending]
   Previous reply: [link to the existing reply]
   [Re-present the decision options if the original context is available,
   or summarize what was asked]
```

If a blocking question mechanism is available, use it to ask about all pending decisions (both new `needs-human` and previous-run pending) together. After the user decides, process the remaining items: fix the code, compose the reply, post it, and resolve the thread.

If no blocking question mechanism is available, present the decisions in the summary and wait for the user to respond in conversation. If they don't respond, the items remain open on the PR for later handling.

---

## Targeted Mode

When a specific comment or thread URL is provided, ONLY address that feedback. Do not fetch or process other threads.

### 1. Extract Thread Context

Parse the URL to extract OWNER, REPO, PR number, and comment REST ID:
```
https://github.com/OWNER/REPO/pull/NUMBER#discussion_rCOMMENT_ID
```

**Step 1 — Get comment details and GraphQL node ID via REST:**
```bash
gh api repos/OWNER/REPO/pulls/comments/COMMENT_ID \
  --jq '{node_id, path, line, body}'
```

**Step 2 — Map comment to its thread ID via GraphQL:**

Query all review threads for the PR (fetching thread IDs, first comment IDs, and full comment details). Filter to find the thread whose `comments.nodes` array contains the comment matching `COMMENT_NODE_ID`.

```bash
# GraphQL query sketch:
gh api graphql -f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUMBER" -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes {
          id isResolved path line
          comments(first: 100) {
            nodes { id author { login } body createdAt url }
          }
        }
      }
    }
  }
}' | jq -e --arg cid "$COMMENT_NODE_ID" '
  [.data.repository.pullRequest.reviewThreads.nodes[]
  | select(.comments.nodes | map(.id) | index($cid))]
  | if length == 0 then error("No thread found") else .[0] end
'
```

### 2. Fix, Reply, Resolve

Delegate a single `pr-comment-resolver` subagent for the thread. Then follow the same commit → push → reply → resolve flow as Full Mode steps 6–7.

---

## Scripts Reference

The following GraphQL scripts are used internally:

| Script | Purpose |
|--------|---------|
| `get-pr-comments PR_NUMBER [OWNER/REPO]` | Fetch all unresolved review threads, PR comments, and review bodies in one GraphQL query. Returns JSON with keys `review_threads`, `pr_comments`, `review_bodies`. |
| `get-thread-for-comment PR_NUMBER COMMENT_NODE_ID [OWNER/REPO]` | Map a PR review comment node ID to its parent thread ID with full comment details. |
| `echo "BODY" \| reply-to-pr-thread THREAD_ID` | GraphQL mutation to add a reply within a review thread. Body passed via stdin. |
| `resolve-pr-thread THREAD_ID` | GraphQL mutation to mark a review thread as resolved. |

## Quality Gates

- All unresolved review threads evaluated
- Valid fixes committed and pushed
- Each thread replied to with quoted context
- Review threads resolved via GraphQL (except `needs-human`)
- Re-fetch of `review_threads` returns empty (or only `needs-human` open threads)
- `needs-human` items surfaced to user with full `decision_context`
- No more than 2 fix-verify cycles before escalating recurring patterns to user

## Outputs

- Code fixes committed and pushed to the PR branch
- Reply posted to each review thread, PR comment, and review body
- Review threads resolved (or left open with explanation for `needs-human`)
- Summary report grouped by verdict
- Cluster assessment (if cluster analysis ran)
- Pending decisions presented for user input

## Feeds Into

- `ce:review` (for a fresh review pass after fixes)
- `ship` (once all feedback is resolved and PR is ready to merge)
