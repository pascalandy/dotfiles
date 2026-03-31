# Orchestrating Swarms

> Master multi-agent orchestration using a leader/teammate/task-list model to coordinate parallel specialists, sequential pipelines, and self-organizing worker swarms.

## When to Use

- Coordinating multiple agents working in parallel (e.g., parallel code reviews).
- Creating sequential pipeline workflows with dependency tracking.
- Building self-organizing task queues where workers race to claim work.
- Any divide-and-conquer task that benefits from concurrent execution.
- Running parallel code reviews with specialized reviewer agents.

## Inputs

- A task or feature to decompose into parallelizable or sequential work items.
- A team name for the coordination namespace.
- Access to the TeammateTool and Task system primitives.

## Methodology

### Primitives

| Primitive | What It Is | Storage Location |
|-----------|-----------|------------------|
| **Agent** | A model instance that can use tools. You are an agent. Subagents are agents you spawn. | N/A (process) |
| **Team** | A named group of agents working together. One leader, multiple teammates. | `~/.claude/teams/{name}/config.json` |
| **Teammate** | An agent that joined a team. Has a name, color, and inbox. Spawned via Task with `team_name` + `name`. | Listed in team config |
| **Leader** | The agent that created the team. Receives teammate messages, approves plans/shutdowns. | First member in config |
| **Task** | A work item with subject, description, status, owner, and dependencies. | `~/.claude/tasks/{team}/N.json` |
| **Inbox** | JSON file where an agent receives messages from teammates. | `~/.claude/teams/{name}/inboxes/{agent}.json` |
| **Message** | A JSON object sent between agents. Can be text or structured (shutdown_request, idle_notification, etc.). | Stored in inbox files |
| **Backend** | How teammates run. Auto-detected: `in-process` (same process, invisible), `tmux` (separate panes, visible), `iterm2` (split panes in iTerm2). | Auto-detected based on environment |

---

### How They Connect

```
TEAM:
  Leader (you)
    ↕ messages via inbox ↕
  Teammate 1  ←·→  Teammate 2

TASK LIST:
  #1 completed: Research     (owner: teammate1)
  #2 in_progress: Implement  (owner: teammate2)
  #3 pending: Test           [blocked by #2]

  Teammate 1 → Task #1
  Teammate 2 → Task #2
  Task #2 unblocks → Task #3
```

### Lifecycle

```
1. Create Team
      |
      v
2. Create Tasks
      |
      v
3. Spawn Teammates
      |
      v
4. Work
      |
      v
5. Coordinate
      |
      v
6. Shutdown
      |
      v
7. Cleanup
```

### Message Flow

```
Leader ──TaskCreate(3 tasks)──> Task List
Leader ──spawn──> Teammate 1
Leader ──spawn──> Teammate 2

Teammate 1 ──claim #1──> Task List
Teammate 2 ──claim #2──> Task List

Teammate 1 ──complete #1──> Task List
Teammate 1 ──findings──> Leader inbox

[Task #3 auto-unblocks]

Teammate 2 ──complete #2──> Task List
Teammate 2 ──findings──> Leader inbox

Leader ──requestShutdown──> Teammate 1
Teammate 1 ──approveShutdown──> Leader
Leader ──requestShutdown──> Teammate 2
Teammate 2 ──approveShutdown──> Leader

Leader ──cleanup
```

---

### File Structure

```
~/.claude/teams/{team-name}/
├── config.json              # Team metadata and member list
└── inboxes/
    ├── team-lead.json       # Leader's inbox
    ├── worker-1.json        # Worker 1's inbox
    └── worker-2.json        # Worker 2's inbox

~/.claude/tasks/{team-name}/
├── 1.json                   # Task #1
├── 2.json                   # Task #2
└── 3.json                   # Task #3
```

### Team Config Structure

```json
{
  "name": "my-project",
  "description": "Working on feature X",
  "leadAgentId": "team-lead@my-project",
  "createdAt": 1706000000000,
  "members": [
    {
      "agentId": "team-lead@my-project",
      "name": "team-lead",
      "agentType": "team-lead",
      "color": "#4A90D9",
      "joinedAt": 1706000000000,
      "backendType": "in-process"
    },
    {
      "agentId": "worker-1@my-project",
      "name": "worker-1",
      "agentType": "Explore",
      "model": "haiku",
      "prompt": "Analyze the codebase structure...",
      "color": "#D94A4A",
      "planModeRequired": false,
      "joinedAt": 1706000001000,
      "tmuxPaneId": "in-process",
      "cwd": "/Users/me/project",
      "backendType": "in-process"
    }
  ]
}
```

---

### Two Ways to Spawn Agents

#### Method 1: Subagent (Task Tool, No Team)

Use for **short-lived, focused work** that returns a result:

```javascript
Task({
  subagent_type: "Explore",
  description: "Find auth files",
  prompt: "Find all authentication-related files in this codebase",
  model: "haiku"  // Optional: haiku, sonnet, opus
})
```

- Runs synchronously (blocks until complete) or async with `run_in_background: true`.
- Returns result directly.
- No team membership required.
- Best for: searches, analysis, focused research.

#### Method 2: Teammate (Task Tool + team_name + name)

Use for **persistent, coordinating workers**:

```javascript
// Step 1: Create a team
Teammate({ operation: "spawnTeam", team_name: "my-project" })

// Step 2: Spawn a teammate into that team
Task({
  team_name: "my-project",
  name: "security-reviewer",
  subagent_type: "security-sentinel",
  prompt: "Review all auth code for vulnerabilities. Send findings to team-lead.",
  run_in_background: true
})
```

- Joins team, appears in `config.json`.
- Communicates via inbox messages.
- Can claim tasks from shared task list.
- Persists until shutdown.
- Best for: parallel work, ongoing collaboration, pipeline stages.

#### Comparison

| Aspect | Subagent (Task only) | Teammate (Task + team) |
|--------|---------------------|------------------------|
| Lifespan | Until task complete | Until shutdown requested |
| Communication | Return value | Inbox messages |
| Task access | None | Shared task list |
| Team membership | No | Yes |
| Coordination | One-off | Ongoing |

---

### Built-in Agent Types

#### Bash
- **Tools:** Bash only.
- **Best for:** Git operations, command execution, system tasks.

#### Explore
- **Tools:** All read-only tools (no Edit, Write, or Task delegation).
- **Model:** Haiku (optimized for speed).
- **Best for:** Codebase exploration, file searches, code understanding.
- **Thoroughness levels in prompt:** "quick", "medium", "very thorough".

#### Plan
- **Tools:** All read-only tools.
- **Best for:** Architecture planning, implementation strategies.

#### general-purpose
- **Tools:** All tools.
- **Best for:** Multi-step tasks, research + action combinations, implementation.

#### claude-code-guide
- **Tools:** Read-only + WebFetch + WebSearch.
- **Best for:** Questions about tooling, agent SDKs, API usage.

#### statusline-setup
- **Tools:** Read, Edit only.
- **Model:** Sonnet.
- **Best for:** Configuring status lines and similar configuration tasks.

---

### Plugin Agent Types (compound-engineering)

**Review agents:**
- `agent-native-reviewer` — Ensures features work for agents too.
- `architecture-strategist` — Architectural compliance.
- `code-simplicity-reviewer` — YAGNI and minimalism.
- `data-integrity-guardian` — Database and data safety.
- `data-migration-expert` — Migration validation.
- `deployment-verification-agent` — Pre-deploy checklists.
- `dhh-rails-reviewer` — DHH/37signals Rails style.
- `julik-frontend-races-reviewer` — JavaScript race conditions.
- `kieran-python-reviewer` — Python best practices.
- `kieran-rails-reviewer` — Rails best practices.
- `kieran-typescript-reviewer` — TypeScript best practices.
- `pattern-recognition-specialist` — Design patterns and anti-patterns.
- `performance-oracle` — Performance analysis.
- `security-sentinel` — Security vulnerabilities.

**Research agents:**
- `best-practices-researcher` — External best practices.
- `framework-docs-researcher` — Framework documentation.
- `git-history-analyzer` — Code archaeology.
- `learnings-researcher` — Search `docs/solutions/`.
- `repo-research-analyst` — Repository patterns.

**Design agents:**
- `figma-design-sync` — Compare implementation with Figma design.

**Workflow agents:**
- `bug-reproduction-validator` — Reproduce and validate reported bugs.

---

### TeammateTool Operations

#### `spawnTeam` — Create a Team

```javascript
Teammate({
  operation: "spawnTeam",
  team_name: "feature-auth",
  description: "Implementing OAuth2 authentication"
})
```

Creates `~/.claude/teams/feature-auth/config.json`, task directory, and makes you team leader.

#### `discoverTeams` — List Available Teams

```javascript
Teammate({ operation: "discoverTeams" })
```

Returns list of teams you can join (not already a member of).

#### `requestJoin` — Request to Join Team

```javascript
Teammate({
  operation: "requestJoin",
  team_name: "feature-auth",
  proposed_name: "helper",
  capabilities: "I can help with code review and testing"
})
```

#### `approveJoin` — Accept Join Request (Leader Only)

When a `join_request` message arrives:
```json
{"type": "join_request", "proposedName": "helper", "requestId": "join-123", ...}
```

Approve:
```javascript
Teammate({
  operation: "approveJoin",
  target_agent_id: "helper",
  request_id: "join-123"
})
```

#### `rejectJoin` — Decline Join Request (Leader Only)

```javascript
Teammate({
  operation: "rejectJoin",
  target_agent_id: "helper",
  request_id: "join-123",
  reason: "Team is at capacity"
})
```

#### `write` — Message One Teammate

```javascript
Teammate({
  operation: "write",
  target_agent_id: "security-reviewer",
  value: "Please prioritize the authentication module."
})
```

**IMPORTANT for teammates:** Your text output is NOT visible to the team. You MUST use `write` to communicate.

#### `broadcast` — Message ALL Teammates

```javascript
Teammate({
  operation: "broadcast",
  name: "team-lead",
  value: "Status check: Please report your progress"
})
```

**WARNING:** Broadcasting is expensive — sends N separate messages for N teammates. Prefer `write` to specific teammates.

**When to broadcast:**
- Critical issues requiring immediate attention from everyone.
- Major announcements affecting the entire team.

**When NOT to broadcast:**
- Responding to one teammate.
- Normal back-and-forth.
- Information relevant to only some teammates.

#### `requestShutdown` — Ask Teammate to Exit (Leader Only)

```javascript
Teammate({
  operation: "requestShutdown",
  target_agent_id: "security-reviewer",
  reason: "All tasks complete, wrapping up"
})
```

#### `approveShutdown` — Accept Shutdown (Teammate Only)

When a `shutdown_request` arrives:
```json
{"type":"shutdown_request","requestId":"shutdown-123","from":"team-lead","reason":"Done"}
```

**MUST** respond:
```javascript
Teammate({
  operation: "approveShutdown",
  request_id: "shutdown-123"
})
```

This sends confirmation and terminates the teammate process.

#### `rejectShutdown` — Decline Shutdown (Teammate Only)

```javascript
Teammate({
  operation: "rejectShutdown",
  request_id: "shutdown-123",
  reason: "Still working on task #3, need 5 more minutes"
})
```

#### `approvePlan` — Approve Teammate's Plan (Leader Only)

When a teammate with `plan_mode_required` sends a plan:
```json
{"type":"plan_approval_request","from":"architect","requestId":"plan-456",...}
```

Approve:
```javascript
Teammate({
  operation: "approvePlan",
  target_agent_id: "architect",
  request_id: "plan-456"
})
```

#### `rejectPlan` — Reject Plan with Feedback (Leader Only)

```javascript
Teammate({
  operation: "rejectPlan",
  target_agent_id: "architect",
  request_id: "plan-456",
  feedback: "Please add error handling and consider rate limiting"
})
```

#### `cleanup` — Remove Team Resources

```javascript
Teammate({ operation: "cleanup" })
```

Removes `~/.claude/teams/{team-name}/` and `~/.claude/tasks/{team-name}/` directories.

**IMPORTANT:** Will fail if teammates are still active. Use `requestShutdown` first and wait for approvals.

---

### Task System Integration

#### `TaskCreate` — Create Work Items

```javascript
TaskCreate({
  subject: "Review authentication module",
  description: "Review all files in app/services/auth/ for vulnerabilities",
  activeForm: "Reviewing auth module..."  // Shown in spinner when in_progress
})
```

#### `TaskList` — See All Tasks

```javascript
TaskList()
```

Returns:
```
#1 [completed] Analyze codebase structure
#2 [in_progress] Review authentication module (owner: security-reviewer)
#3 [pending] Generate summary report [blocked by #2]
```

#### `TaskGet` — Get Task Details

```javascript
TaskGet({ taskId: "2" })
```

Returns full task with description, status, blockedBy, owner, etc.

#### `TaskUpdate` — Update Task Status

```javascript
// Claim a task
TaskUpdate({ taskId: "2", owner: "security-reviewer" })

// Start working
TaskUpdate({ taskId: "2", status: "in_progress" })

// Mark complete
TaskUpdate({ taskId: "2", status: "completed" })

// Set up dependencies
TaskUpdate({ taskId: "3", addBlockedBy: ["1", "2"] })
```

#### Task Dependencies

When a blocking task is completed, blocked tasks automatically unblock:

```javascript
TaskCreate({ subject: "Step 1: Research" })        // #1
TaskCreate({ subject: "Step 2: Implement" })       // #2
TaskCreate({ subject: "Step 3: Test" })            // #3
TaskCreate({ subject: "Step 4: Deploy" })          // #4

TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })   // #2 waits for #1
TaskUpdate({ taskId: "3", addBlockedBy: ["2"] })   // #3 waits for #2
TaskUpdate({ taskId: "4", addBlockedBy: ["3"] })   // #4 waits for #3
// When #1 completes, #2 auto-unblocks, etc.
```

#### Task File Structure

`~/.claude/tasks/{team-name}/1.json`:
```json
{
  "id": "1",
  "subject": "Review authentication module",
  "description": "Review all files in app/services/auth/...",
  "status": "in_progress",
  "owner": "security-reviewer",
  "activeForm": "Reviewing auth module...",
  "blockedBy": [],
  "blocks": ["3"],
  "createdAt": 1706000000000,
  "updatedAt": 1706000001000
}
```

---

### Message Formats

#### Regular Message
```json
{
  "from": "team-lead",
  "text": "Please prioritize the auth module",
  "timestamp": "2026-01-25T23:38:32.588Z",
  "read": false
}
```

#### Shutdown Request
```json
{
  "type": "shutdown_request",
  "requestId": "shutdown-abc123@worker-1",
  "from": "team-lead",
  "reason": "All tasks complete",
  "timestamp": "2026-01-25T23:38:32.588Z"
}
```

#### Shutdown Approved
```json
{
  "type": "shutdown_approved",
  "requestId": "shutdown-abc123@worker-1",
  "from": "worker-1",
  "paneId": "%5",
  "backendType": "in-process",
  "timestamp": "2026-01-25T23:39:00.000Z"
}
```

#### Idle Notification (auto-sent when teammate stops)
```json
{
  "type": "idle_notification",
  "from": "worker-1",
  "timestamp": "2026-01-25T23:40:00.000Z",
  "completedTaskId": "2",
  "completedStatus": "completed"
}
```

#### Task Completed
```json
{
  "type": "task_completed",
  "from": "worker-1",
  "taskId": "2",
  "taskSubject": "Review authentication module",
  "timestamp": "2026-01-25T23:40:00.000Z"
}
```

#### Plan Approval Request
```json
{
  "type": "plan_approval_request",
  "from": "architect",
  "requestId": "plan-xyz789",
  "planContent": "# Implementation Plan\n\n1. ...",
  "timestamp": "2026-01-25T23:41:00.000Z"
}
```

#### Join Request
```json
{
  "type": "join_request",
  "proposedName": "helper",
  "requestId": "join-abc123",
  "capabilities": "Code review and testing",
  "timestamp": "2026-01-25T23:42:00.000Z"
}
```

#### Permission Request (for sandbox/tool permissions)
```json
{
  "type": "permission_request",
  "requestId": "perm-123",
  "workerId": "worker-1@my-project",
  "workerName": "worker-1",
  "workerColor": "#4A90D9",
  "toolName": "Bash",
  "toolUseId": "toolu_abc123",
  "description": "Run npm install",
  "input": {"command": "npm install"},
  "permissionSuggestions": ["Bash(npm *)"],
  "createdAt": 1706000000000
}
```

---

### Orchestration Patterns

#### Pattern 1: Parallel Specialists (Leader Pattern)

Multiple specialists review or analyze simultaneously:

```
1. Create team.
2. Spawn all specialists in parallel (single turn, multiple spawn calls).
3. Wait for results (poll leader inbox or check for idle_notification messages).
4. Synthesize findings.
5. Request shutdown for all teammates; wait for approvals.
6. Cleanup.
```

Example use: parallel security + performance + architecture code review.

#### Pattern 2: Pipeline (Sequential Dependencies)

Each stage depends on the previous completing:

```
1. Create team.
2. Create all tasks (research, plan, implement, test, review).
3. Set dependencies: each task blocked by the previous.
4. Spawn workers that poll TaskList and claim unblocked tasks.
5. Dependencies auto-unblock as stages complete.
```

Example use: research → plan → implement → test → review feature pipeline.

#### Pattern 3: Swarm (Self-Organizing)

Workers race to claim tasks from a pool of independent work items:

```
1. Create team.
2. Create many independent tasks (no dependencies between them).
3. Spawn N workers with a loop prompt:
   a. Call TaskList to find pending, unowned, unblocked tasks.
   b. Claim one: set owner and status to in_progress.
   c. Do the work.
   d. Mark completed; send findings to team-lead.
   e. Repeat until no tasks remain.
   f. If no tasks remain after retries, send idle notification and exit.
4. Workers self-organize; naturally load-balance.
```

Example use: reviewing N files simultaneously.

Worker loop prompt template:
```
You are a swarm worker. Your job:
1. Call TaskList() to see available tasks
2. Find a task with status 'pending' and no owner
3. Claim it: TaskUpdate({ taskId: "X", owner: "YOUR_NAME" })
4. Start it: TaskUpdate({ taskId: "X", status: "in_progress" })
5. Do the work
6. Complete it: TaskUpdate({ taskId: "X", status: "completed" })
7. Send findings to team-lead via write
8. Repeat until no tasks remain
If no tasks after 3 retries (30s wait each), exit.
Replace YOUR_NAME with $CLAUDE_CODE_AGENT_NAME.
```

#### Pattern 4: Research + Implementation

Synchronous research phase feeds implementation:

```
1. Run a research subagent (no team needed) — blocks until complete.
2. Use research result content to construct implementation prompt.
3. Run implementation agent with enriched prompt.
```

#### Pattern 5: Plan Approval Workflow

Require explicit plan review before implementation:

```
1. Create team.
2. Spawn architect with plan_mode_required / mode: "plan".
3. Wait for plan_approval_request message in inbox.
4. Review plan content.
5. approvePlan or rejectPlan with feedback.
6. Architect proceeds (or revises) based on response.
```

#### Pattern 6: Coordinated Multi-File Refactoring

```
1. Create team.
2. Create tasks with clear file/module boundaries.
3. Set dependencies: shared downstream tasks (e.g., spec updates) blocked by
   all upstream refactors.
4. Spawn one worker per independent task.
5. Shared downstream worker waits for its task to unblock, then proceeds.
```

---

### Environment Variables (Auto-Injected into Teammates)

```bash
CLAUDE_CODE_TEAM_NAME="my-project"
CLAUDE_CODE_AGENT_ID="worker-1@my-project"
CLAUDE_CODE_AGENT_NAME="worker-1"
CLAUDE_CODE_AGENT_TYPE="Explore"
CLAUDE_CODE_AGENT_COLOR="#4A90D9"
CLAUDE_CODE_PLAN_MODE_REQUIRED="false"
CLAUDE_CODE_PARENT_SESSION_ID="session-xyz"
```

Reference in prompts: `"Your name is $CLAUDE_CODE_AGENT_NAME. Use it when messaging team-lead."`

---

### Spawn Backends

A backend determines how teammate instances actually run. Auto-detected based on environment.

| Backend | How It Works | Visibility | Persistence | Speed |
|---------|-------------|------------|-------------|-------|
| **in-process** | Same process as leader | Hidden (background) | Dies with leader | Fastest |
| **tmux** | Separate terminal in tmux session | Visible in tmux panes | Survives leader exit | Medium |
| **iterm2** | Split panes in iTerm2 window (macOS only) | Visible side-by-side | Dies with window | Medium |

#### Auto-Detection Logic

```
Is $TMUX set?
  Yes → use tmux backend (native pane split)
  No  →
    Is $TERM_PROGRAM === "iTerm.app" or $ITERM_SESSION_ID set?
      No →
        Is tmux available (which tmux)?
          Yes → use tmux (external session)
          No  → use in-process
      Yes →
        Is it2 CLI installed (which it2)?
          Yes → use iterm2 backend
          No  →
            Is tmux available?
              Yes → use tmux (prompt to install it2)
              No  → Error: install tmux or it2
```

**Detection checks:**
1. `$TMUX` environment variable → inside tmux.
2. `$TERM_PROGRAM === "iTerm.app"` or `$ITERM_SESSION_ID` → in iTerm2.
3. `which tmux` → tmux available.
4. `which it2` → it2 CLI installed.

#### in-process

Teammates run as async tasks within the same process.

```
┌─────────────────────────────────────────┐
│           Node.js Process               │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐ │
│  │ Leader  │  │Worker 1 │  │Worker 2 │ │
│  │ (main)  │  │ (async) │  │ (async) │ │
│  └─────────┘  └─────────┘  └─────────┘ │
└─────────────────────────────────────────┘
```

- Pros: Fastest startup, lowest overhead, works everywhere.
- Cons: Can't see teammate output in real-time; all die if leader dies; harder to debug.
- Force: `export CLAUDE_CODE_SPAWN_BACKEND=in-process`

#### tmux

Each teammate gets its own tmux pane.

Inside tmux (native — splits current window):
```
┌─────────────────┬─────────────────┐
│                 │    Worker 1     │
│     Leader      ├─────────────────┤
│   (your pane)   │    Worker 2     │
│                 ├─────────────────┤
│                 │    Worker 3     │
└─────────────────┴─────────────────┘
```

Outside tmux (external session named `claude-swarm`):
```bash
# View workers:
tmux attach -t claude-swarm
```

- Pros: Real-time output visibility; teammates survive leader exit; CI-compatible.
- Cons: Slower startup; requires tmux installed; more resource usage.
- Force: `export CLAUDE_CODE_SPAWN_BACKEND=tmux`

Useful tmux commands when debugging:
```bash
tmux list-panes
tmux select-pane -t 1
tmux kill-pane -t %5
tmux attach -t claude-swarm
tmux select-layout tiled
```

#### iterm2 (macOS only)

Uses iTerm2's Python API via `it2` CLI. Splits window into side-by-side panes.

```
┌─────────────────┬─────────────────┐
│                 │    Worker 1     │
│     Leader      ├─────────────────┤
│   (your pane)   │    Worker 2     │
│                 ├─────────────────┤
│                 │    Worker 3     │
└─────────────────┴─────────────────┘
```

- Pros: Visual debugging, native macOS, automatic pane management.
- Cons: macOS + iTerm2 + it2 CLI + Python API enabled required. Panes die with window.

Setup:
```bash
# Install it2
uv tool install it2  # or pipx install it2

# Enable Python API in iTerm2:
# Settings → General → Magic → Enable Python API

# Verify
it2 --version
it2 session list
```

If setup fails, Claude Code prompts: install it2 now / use tmux instead / cancel.

#### Backend in Team Config

The backend is recorded per-teammate:
```json
{
  "members": [
    {"name": "worker-1", "backendType": "in-process", "tmuxPaneId": "in-process"},
    {"name": "worker-2", "backendType": "tmux", "tmuxPaneId": "%5"}
  ]
}
```

#### Backend Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| "No pane backend available" | Neither tmux nor iTerm2 available | Install tmux: `brew install tmux` |
| "it2 CLI not installed" | In iTerm2 but missing it2 | Run `uv tool install it2` |
| "Python API not enabled" | it2 can't communicate with iTerm2 | Enable in iTerm2 Settings → General → Magic |
| Workers not visible | Using in-process backend | Start inside tmux or iTerm2 |
| Workers dying unexpectedly | Outside tmux, leader exited | Use tmux for persistence |

Checking current backend:
```bash
cat ~/.claude/teams/{team}/config.json | jq '.members[].backendType'
echo $TMUX
echo $TERM_PROGRAM
which tmux
which it2
```

---

### Error Handling

#### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Cannot cleanup with active members" | Teammates still running | `requestShutdown` all, wait for approval |
| "Already leading a team" | Team already exists | `cleanup` first, or use different team name |
| "Agent not found" | Wrong teammate name | Check `config.json` for actual names |
| "Team does not exist" | No team created | Call `spawnTeam` first |
| "team_name is required" | Missing team context | Provide `team_name` parameter |
| "Agent type not found" | Invalid subagent_type | Check available agents with proper prefix |

#### Graceful Shutdown Sequence

Always follow this order:

```
1. requestShutdown for all teammates.
2. Wait for shutdown_approved messages from each.
3. Verify no active members remain (read team config.json).
4. Only then call cleanup.
```

#### Crashed Teammates

Teammates have a **5-minute heartbeat timeout**. If a teammate crashes:
1. Automatically marked inactive after timeout.
2. Their tasks remain in the task list.
3. Another teammate can claim their tasks.
4. `cleanup` works after timeout expires.

#### Debugging Commands

```bash
# Check team config
cat ~/.claude/teams/{team}/config.json \
  | jq '.members[] | {name, agentType, backendType}'

# Check teammate inboxes
cat ~/.claude/teams/{team}/inboxes/{agent}.json | jq '.'

# List all teams
ls ~/.claude/teams/

# Check task states
cat ~/.claude/tasks/{team}/*.json \
  | jq '{id, subject, status, owner, blockedBy}'

# Watch for new messages
tail -f ~/.claude/teams/{team}/inboxes/team-lead.json
```

---

### Best Practices

1. **Always cleanup** — Don't leave orphaned teams. Always call `cleanup` when done.

2. **Use meaningful names:**
   ```
   Good: "security-reviewer", "oauth-implementer", "test-writer"
   Bad:  "worker-1", "agent-2"
   ```

3. **Write clear prompts** — Tell workers exactly what to do, including how to communicate results:
   ```
   1. Review app/models/user.rb for N+1 queries
   2. Check all ActiveRecord associations have proper includes
   3. Document any issues found
   4. Send findings to team-lead via Teammate write
   ```

4. **Use task dependencies** — Let the system manage unblocking rather than manual polling.

5. **Check inboxes for results** — Workers send results to the leader's inbox.

6. **Handle worker failures** — Build retry logic into worker prompts (e.g., retry up to 3 times with 30s waits before exiting).

7. **Prefer `write` over `broadcast`** — `broadcast` sends N messages for N teammates.

8. **Match agent type to task:**
   - `Explore` for searching/reading.
   - `Plan` for architecture design.
   - `general-purpose` for implementation.
   - Specialized reviewers for specific review types.

---

### Quick Reference

```javascript
// Spawn subagent (no team)
Task({ subagent_type: "Explore", description: "Find files", prompt: "..." })

// Spawn teammate (with team)
Teammate({ operation: "spawnTeam", team_name: "my-team" })
Task({ team_name: "my-team", name: "worker",
       subagent_type: "general-purpose", prompt: "...",
       run_in_background: true })

// Message a teammate
Teammate({ operation: "write", target_agent_id: "worker-1", value: "..." })

// Create task pipeline
TaskCreate({ subject: "Step 1", description: "..." })
TaskCreate({ subject: "Step 2", description: "..." })
TaskUpdate({ taskId: "2", addBlockedBy: ["1"] })

// Shutdown team
Teammate({ operation: "requestShutdown", target_agent_id: "worker-1" })
// Wait for approval...
Teammate({ operation: "cleanup" })
```

## Quality Gates

- [ ] Team created with `spawnTeam` before spawning any teammates.
- [ ] All teammates shut down with `requestShutdown` → `approveShutdown` before `cleanup`.
- [ ] `cleanup` called when work is complete (no orphaned teams).
- [ ] Task dependencies set with `addBlockedBy` (not manual polling in prompts).
- [ ] Worker prompts include explicit instructions for communicating results to team-lead.
- [ ] `write` used for targeted communication, not `broadcast`.
- [ ] Retry logic included in worker prompts for failure resilience.

## Outputs

- Completed work distributed across multiple agents.
- Findings aggregated in the leader's inbox.
- Synthesized report or result from the leader.
- Clean team teardown (no orphaned processes or task files).

## Feeds Into

- `ce:review` — parallel multi-perspective code review.
- `slfg` — swarm-based full engineering workflow.
- Any workflow that benefits from parallelized or pipelined execution.

## Harness Notes

This skill describes the Claude Code TeammateTool and Task system API precisely. The `Teammate({...})` and `Task({...})` calls are Claude Code-specific primitives. In other harnesses:
- Adapt `spawnTeam` / `requestShutdown` / `cleanup` to equivalent team-lifecycle operations.
- The inbox and task file patterns (`~/.claude/teams/`, `~/.claude/tasks/`) are Claude Code filesystem conventions; other harnesses may use different persistence mechanisms.
- Spawn backend auto-detection (`$TMUX`, `$TERM_PROGRAM`, `which it2`) is Claude Code-specific but the concepts (in-process vs. separate-process workers) apply universally.
