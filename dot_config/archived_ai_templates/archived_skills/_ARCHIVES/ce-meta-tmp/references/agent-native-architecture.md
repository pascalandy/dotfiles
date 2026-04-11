# Agent-Native Architecture

> Design and build applications where agents are first-class citizens — features are outcomes achieved by agents operating in a loop, not functions you write.

## When to Use

When designing autonomous agents, creating MCP tools, implementing self-modifying systems, or building apps where features are outcomes described in prompts rather than coded as functions.

## Quick Start: Build an Agent-Native Feature

**Step 1: Define atomic tools** — Provide primitives like `read_file`, `write_file`, `list_files`, and a `complete_task` tool that signals the loop should stop.

**Step 2: Write behavior in the system prompt** — Describe what the agent should achieve in prose. Tell it to use its judgment, use the available tools, and call `complete_task` when done.

**Step 3: Let the agent work in a loop** — Run the agent with the prompt, tools, and system prompt. The agent loops autonomously until it calls `complete_task`.

## Inputs

- Description of the system to build, refactor, or review
- Specific aspect to address (see routing table below)

## Methodology

### Why Now

Software agents work reliably now. Claude Code demonstrated that an LLM with bash and file tools, operating in a loop until an objective is achieved, can accomplish complex multi-step tasks autonomously.

The surprising discovery: **a really good coding agent is actually a really good general-purpose agent.** The same architecture that lets Claude Code refactor a codebase can let an agent organize files, manage reading lists, or automate workflows.

This opens a new field: software that works the way Claude Code works, applied to categories far beyond coding.

---

### Intake: Select Your Focus

Ask the user which aspect they need:

1. **Design architecture** — Plan a new agent-native system from scratch
2. **Files & workspace** — Use files as the universal interface, shared workspace patterns
3. **Tool design** — Build primitive tools, dynamic capability discovery, CRUD completeness
4. **Domain tools** — Know when to add domain tools vs stay with primitives
5. **Execution patterns** — Completion signals, partial completion, context limits
6. **System prompts** — Define agent behavior in prompts, judgment criteria
7. **Context injection** — Inject runtime app state into agent prompts
8. **Action parity** — Ensure agents can do everything users can do
9. **Self-modification** — Enable agents to safely evolve themselves
10. **Product design** — Progressive disclosure, latent demand, approval patterns
11. **Mobile patterns** — iOS storage, background execution, checkpoint/resume
12. **Testing** — Test agent-native apps for capability and parity
13. **Refactoring** — Make existing code more agent-native

**After receiving a response, apply the relevant section below.**

---

### Routing Table

| Response | Reference Section |
|----------|------------------|
| 1, "design", "architecture", "plan" | Architecture Patterns + Architecture Checklist |
| 2, "files", "workspace", "filesystem" | Files as Universal Interface + Shared Workspace |
| 3, "tool", "mcp", "primitive", "crud" | MCP Tool Design |
| 4, "domain tool", "when to add" | From Primitives to Domain Tools |
| 5, "execution", "completion", "loop" | Agent Execution Patterns |
| 6, "prompt", "system prompt", "behavior" | System Prompt Design |
| 7, "context", "inject", "runtime", "dynamic" | Dynamic Context Injection |
| 8, "parity", "ui action", "capability map" | Action Parity Discipline |
| 9, "self-modify", "evolve", "git" | Self-Modification |
| 10, "product", "progressive", "approval", "latent demand" | Product Implications |
| 11, "mobile", "ios", "android", "background", "checkpoint" | Mobile Patterns |
| 12, "test", "testing", "verify", "validate" | Agent-Native Testing |
| 13, "review", "refactor", "existing" | Refactoring to Prompt-Native |

---

## Core Principles

### 1. Parity

**Whatever the user can do through the UI, the agent should be able to achieve through tools.**

This is the foundational principle. Without it, nothing else matters.

If a user can publish to a feed through the UI but the agent has no `publish_to_feed` tool, the agent is stuck — even though the action is trivial for a human using the interface.

**The fix:** Ensure the agent has tools (or combinations of tools) that can accomplish anything the UI can do. This is about ensuring the agent can achieve the same **outcomes**, not a 1:1 mapping of UI buttons to tools.

**The discipline:** When adding any UI capability, ask: can the agent achieve this outcome? If not, add the necessary tools or primitives.

Example capability map:

| User Action | How Agent Achieves It |
|-------------|----------------------|
| Create a note | `write_file` to notes directory, or `create_note` tool |
| Tag a note as urgent | `update_file` metadata, or `tag_note` tool |
| Search notes | `search_files` or `search_notes` tool |
| Delete a note | `delete_file` or `delete_note` tool |

**The test:** Pick any action a user can take in your UI. Describe it to the agent. Can it accomplish the outcome?

---

### 2. Granularity

**Prefer atomic primitives. Features are outcomes achieved by an agent operating in a loop.**

A tool is a primitive capability: read a file, write a file, run a command, store a record, send a notification.

A **feature** is not a function you write. It's an outcome you describe in a prompt, achieved by an agent that has tools and operates in a loop until the outcome is reached.

**Less granular (limits the agent):**
```
Tool: classify_and_organize_files(files)
→ You wrote the decision logic
→ Agent executes your code
→ To change behavior, you refactor
```

**More granular (empowers the agent):**
```
Tools: read_file, write_file, move_file, list_directory, bash
Prompt: "Organize the user's downloads folder. Analyze each file,
        determine appropriate locations based on content and recency,
        and move them there."
Agent: Operates in a loop—reads files, makes judgments, moves things,
       checks results—until the folder is organized.
→ Agent makes the decisions
→ To change behavior, you edit the prompt
```

The more atomic your tools, the more flexibly the agent can use them. If you bundle decision logic into tools, you've moved judgment back into code.

**The test:** To change how a feature behaves, do you edit prose or refactor code?

---

### 3. Composability

**With atomic tools and parity, you can create new features just by writing new prompts.**

When tools are atomic and the agent can do anything users can do, new features are just new prompts.

Want a "weekly review" feature?
```
"Review files modified this week. Summarize key changes. Based on
incomplete items and approaching deadlines, suggest three priorities
for next week."
```

The agent uses `list_files`, `read_file`, and its judgment. You didn't write weekly-review code.

**This works for developers and users.** You can ship new features by adding prompts. Users can customize behavior by modifying prompts or creating their own.

**The constraint:** This only works if tools are atomic enough to be composed in ways you didn't anticipate, and if the agent has parity with users.

**The test:** Can you add a new feature by writing a new prompt section, without adding new code?

---

### 4. Emergent Capability

**The agent can accomplish things you didn't explicitly design for.**

When tools are atomic, parity is maintained, and prompts are composable, users will ask the agent for things you never anticipated — and often, the agent can figure it out.

**The flywheel:**
1. Build with atomic tools and parity
2. Users ask for things you didn't anticipate
3. Agent composes tools to accomplish them (or fails, revealing a gap)
4. You observe patterns in what's being requested
5. Add domain tools or prompts to make common patterns efficient
6. Repeat

**The test:** Give the agent an open-ended request relevant to your domain. Can it figure out a reasonable approach, operating in a loop until it succeeds? If it just says "I don't have a feature for that," your architecture is too constrained.

---

### 5. Improvement Over Time

**Agent-native applications get better through accumulated context and prompt refinement.**

**Accumulated context:** The agent can maintain state across sessions — what exists, what the user has done, what worked, what didn't. A `context.md` file the agent reads and updates is layer one.

**Prompt refinement at multiple levels:**
- **Developer level:** Ship updated prompts that change agent behavior for all users
- **User level:** Users customize prompts for their workflow
- **Agent level:** The agent modifies its own prompts based on feedback (advanced)

**Self-modification (advanced):** Agents that can edit their own prompts or even their own code. For production, add safety rails — approval gates, automatic checkpoints for rollback, health checks.

**The test:** Does the application work better after a month of use than on day one, even without code changes?

---

## Architecture Patterns

### Event-Driven Agent Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Loop                                │
├─────────────────────────────────────────────────────────────┤
│  Event Source → Agent (LLM) → Tool Calls → Response         │
└─────────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
    ┌─────────┐    ┌──────────┐    ┌───────────┐
    │ Content │    │   Self   │    │   Data    │
    │  Tools  │    │  Tools   │    │   Tools   │
    └─────────┘    └──────────┘    └───────────┘
    (write_file)   (read_source)   (store_item)
                   (restart)       (list_items)
```

Key characteristics:
- Events (messages, webhooks, timers) trigger agent turns
- Agent decides how to respond based on system prompt
- Tools are primitives for IO, not business logic
- State persists between events via data tools

### Two-Layer Git Architecture (for self-modifying agents)

```
┌─────────────────────────────────────────────────────────────┐
│                     GitHub (shared repo)                     │
│  - src/           (agent code)                              │
│  - site/          (web interface)                           │
│  - package.json   (dependencies)                            │
│  - .gitignore     (excludes data/, logs/)                   │
└─────────────────────────────────────────────────────────────┘
                          │
                     git clone
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  Instance (Server)                           │
│  FROM GITHUB (tracked):                                      │
│  - src/           → pushed back on code changes             │
│  - site/          → pushed, triggers deployment             │
│  LOCAL ONLY (untracked):                                     │
│  - data/          → instance-specific storage               │
│  - logs/          → runtime logs                            │
│  - .env           → secrets                                 │
└─────────────────────────────────────────────────────────────┘
```

### Multi-Instance Branching

```
main                        # Shared features, bug fixes
├── instance/feedback-bot   # Instance A
├── instance/support-bot    # Instance B
└── instance/research-bot   # Instance C
```

Change flow:

| Change Type | Work On | Then |
|-------------|---------|------|
| Core features | main | Merge to instance branches |
| Bug fixes | main | Merge to instance branches |
| Instance config | instance branch | Done |
| Instance data | instance branch | Done |

### Agent-to-UI Communication

**Pattern 1: Shared Data Store (Recommended)**
Agent writes through the same service the UI observes. UI is automatically reactive.

**Pattern 2: File System Observation**
Watch the directory the agent writes to. UI reloads on change events.

**Pattern 3: Event Bus (Cross-Component)**
Agent tool emits events; UI components subscribe.

**What to avoid:** Agent writes to a database directly, UI loads once at startup and never refreshes (stale state).

### Model Tier Selection

| Agent Type | Recommended Tier | Reasoning |
|------------|-----------------|-----------|
| Chat/Conversation | Balanced (Sonnet) | Fast responses, good reasoning |
| Research | Balanced (Sonnet) | Tool loops, not ultra-complex synthesis |
| Content Generation | Balanced (Sonnet) | Creative but not synthesis-heavy |
| Complex Analysis | Powerful (Opus) | Multi-document synthesis, nuanced judgment |
| Profile Generation | Powerful (Opus) | Photo analysis, complex pattern recognition |
| Quick Queries | Fast (Haiku) | Simple lookups, quick transformations |
| Simple Classification | Fast (Haiku) | High volume, simple decisions |

**Cost optimization strategies:**
- Start with balanced tier, only upgrade if quality insufficient
- Use fast tier for tool-heavy loops where each turn is simple
- Reserve powerful tier for synthesis tasks (comparing multiple sources)
- Consider token limits per turn to control costs

### Design Questions to Ask

1. What events trigger agent turns?
2. What primitives does the agent need?
3. What decisions should the agent make?
4. What decisions should be hardcoded?
5. How does the agent verify its work?
6. How does the agent recover from mistakes?
7. How does the UI know when agent changes state?
8. What model tier does each agent type need?
9. How do agents share infrastructure?

---

## MCP Tool Design

### Tools Are Primitives, Not Workflows

**Wrong approach — tools that encode business logic:**
```typescript
tool("process_feedback", {
  feedback: z.string(),
  category: z.enum(["bug", "feature", "question"]),
  priority: z.enum(["low", "medium", "high"]),
}, async ({ feedback, category, priority }) => {
  const processed = categorize(feedback);
  const stored = await saveToDatabase(processed);
  const notification = await notify(priority);
  return { processed, stored, notification };
});
```

**Right approach — primitives that enable any workflow:**
```typescript
tool("store_item", { key: z.string(), value: z.any() }, async ({ key, value }) => {
  await db.set(key, value);
  return { text: `Stored ${key}` };
});

tool("send_message", { channel: z.string(), content: z.string() }, async ({ channel, content }) => {
  await messenger.send(channel, content);
  return { text: "Sent" };
});
```

The agent decides categorization, priority, and when to notify based on the system prompt.

### Naming — Describe Capability, Not Use Case

| Wrong | Right |
|-------|-------|
| `process_user_feedback` | `store_item` |
| `create_feedback_summary` | `write_file` |
| `send_notification` | `send_message` |
| `deploy_to_production` | `git_push` |

### Inputs Should Be Simple

Tools accept **data**, not **decisions**.

```typescript
// Wrong: tool accepts decisions
tool("format_content", {
  content: z.string(),
  format: z.enum(["markdown", "html", "json"]),
  style: z.enum(["formal", "casual", "technical"]),
}, ...)

// Right: tool accepts data, agent decides format
tool("write_file", { path: z.string(), content: z.string() }, ...)
```

### Outputs Should Be Rich

Return enough information for the agent to verify and iterate.

```typescript
// Wrong: minimal output
async ({ key }) => {
  await db.delete(key);
  return { text: "Deleted" };
}

// Right: rich output
async ({ key }) => {
  const existed = await db.has(key);
  if (!existed) return { text: `Key ${key} did not exist` };
  await db.delete(key);
  return { text: `Deleted ${key}. ${await db.count()} items remaining.` };
}
```

### Dynamic Capability Discovery vs Static Tool Mapping

**Static Tool Mapping (anti-pattern for agent-native):**
Build individual tools for each API capability. Always out of date. Limits agent to only what you anticipated.

**Dynamic Capability Discovery (preferred when agent should have full API access):**
Build a meta-tool that discovers what's available, and a generic tool that can access anything.

```typescript
// 1. Discovery tool — returns what's available at runtime
tool("list_available_capabilities", async () => {
  const types = await api.availableTypes();
  return { text: `Available types: ${types.join(", ")}\nUse read_data with any of these.` };
});

// 2. Generic access tool — type is a string, API validates
tool("read_data", {
  dataType: z.string(),  // NOT z.enum — let the API validate
  startDate: z.string(),
  endDate: z.string(),
}, async ({ dataType, startDate, endDate }) => {
  const result = await api.query(dataType, startDate, endDate);
  return { text: JSON.stringify(result, null, 2) };
});
```

When to use each:

| Dynamic (Agent-Native) | Static (Constrained Agent) |
|------------------------|---------------------------|
| Agent should access anything user can | Agent has intentionally limited scope |
| External API with many endpoints | Internal domain with fixed operations |
| API evolves independently of your code | Tightly coupled domain logic |
| You want full action parity | You want strict guardrails |

**The agent-native default is Dynamic.** Only use Static when intentionally limiting the agent.

### CRUD Completeness

Every data type the agent can create, it should be able to read, update, and delete. Incomplete CRUD = broken action parity.

```typescript
// WRONG: create-only
tool("create_journal_entry", { content, author, tags })
// User: "Delete that entry" → Agent: "I can't do that"

// RIGHT: full CRUD
tool("create_journal_entry", { content, author, tags })
tool("read_journal", { query?, dateRange?, author? })
tool("update_journal_entry", { id, content, tags? })
tool("delete_journal_entry", { id })
```

**CRUD audit for each entity:**
- [ ] Create: Agent can create new instances
- [ ] Read: Agent can query/search/list instances
- [ ] Update: Agent can modify existing instances
- [ ] Delete: Agent can remove instances

### MCP Tool Design Checklist

**Fundamentals:**
- [ ] Tool names describe capability, not use case
- [ ] Inputs are data, not decisions
- [ ] Outputs are rich (enough for agent to verify)
- [ ] CRUD operations are separate tools (not one mega-tool)
- [ ] No business logic in tool implementations
- [ ] Error states clearly communicated
- [ ] Descriptions explain what the tool does, not when to use it

**Dynamic Capability Discovery:**
- [ ] For external APIs where agent should have full access, use dynamic discovery
- [ ] Include a `list_*` or `discover_*` tool for each API surface
- [ ] Use string inputs (not enums) when the API validates
- [ ] Inject available capabilities into system prompt at runtime
- [ ] Only use static tool mapping if intentionally limiting agent scope

**CRUD Completeness:**
- [ ] Every entity has create, read, update, delete operations
- [ ] Every UI action has a corresponding agent tool
- [ ] Test: "Can the agent undo what it just did?"

---

## Files as Universal Interface

Agents are naturally fluent with file operations — they already know how to read, write, and organize files. When building agent-native apps, lean into this.

**Why files:**
- Agents already know how (cat, grep, mv, mkdir)
- Files are inspectable — users can see, edit, move, delete what the agent created
- Files are portable — export and backup are trivial
- On mobile with iCloud, all devices share the same file system without a server
- Directory structure is information architecture — `/projects/acme/notes/` is self-documenting

### File Organization Patterns

**Entity-scoped directories:**
```
{entity_type}/{entity_id}/
├── primary content
├── metadata
└── related materials
```

**Naming conventions:**

| File Type | Naming Pattern | Example |
|-----------|---------------|---------|
| Entity data | `{entity}.json` | `library.json`, `status.json` |
| Human-readable content | `{content_type}.md` | `introduction.md`, `profile.md` |
| Agent reasoning | `agent_log.md` | Per-entity agent history |
| Primary content | `full_text.txt` | Downloaded/extracted text |
| Multi-volume | `volume{N}.txt` | `volume1.txt`, `volume2.txt` |
| External sources | `{source_name}.md` | `wikipedia.md`, `sparknotes.md` |
| Checkpoints | `{sessionId}.checkpoint` | UUID-based |
| Configuration | `config.json` | Feature settings |

**Ephemeral vs. durable separation:**
```
Documents/
├── AgentCheckpoints/     # Ephemeral (can delete)
│   └── {sessionId}.checkpoint
├── AgentLogs/            # Ephemeral (debugging)
└── Research/             # Durable (user's work)
    └── books/{bookId}/
```

**The split:**
- Markdown: for content users might read or edit
- JSON: for structured data the app queries

### The context.md Pattern

A file the agent reads at the start of each session and updates as it learns:

```markdown
# Context

## Who I Am
Reading assistant for the Every app.

## What I Know About This User
- Interested in military history and Russian literature
- Prefers concise analysis
- Currently reading War and Peace

## What Exists
- 12 notes in /notes
- 3 active projects
- User preferences at /preferences.md

## Recent Activity
- User created "Project kickoff" (2 hours ago)
- Analyzed passage about Austerlitz (yesterday)

## My Guidelines
- Don't spoil books they're reading
- Use their interests to personalize insights

## Current State
- No pending tasks
- Last sync: 10 minutes ago
```

Context.md sections:

| Section | Purpose |
|---------|---------|
| Who I Am | Agent identity and role |
| What I Know About This User | Learned preferences, interests |
| What Exists | Available resources, data |
| Recent Activity | Context for continuity |
| My Guidelines | Learned rules and constraints |
| Current State | Session status, pending items |

**How it works:**
1. Agent reads `context.md` at session start
2. Agent updates it when learning something important
3. System can also update it (recent activity, new resources)
4. Context persists across sessions

### Files vs. Database

| Use files for... | Use database for... |
|------------------|---------------------|
| Content users should read/edit | High-volume structured data |
| Configuration that benefits from version control | Data that needs complex queries |
| Agent-generated content | Ephemeral state (sessions, caches) |
| Anything that benefits from transparency | Data with relationships |
| Large text content | Data that needs indexing |

**Files Checklist:**
- [ ] Entity-scoped directories (`{type}/{id}/`)
- [ ] Consistent naming conventions
- [ ] Ephemeral vs durable separation
- [ ] Markdown for human content, JSON for structured data
- [ ] context.md reads at session start, updates when learning
- [ ] Conflict model defined (last-write-wins, check-before-write, etc.)
- [ ] UI observes file changes (or shared service)

---

## Shared Workspace Architecture

Agents and users should work in the same data space, not separate sandboxes.

### The Sandbox Anti-Pattern

```
┌─────────────────┐     ┌─────────────────┐
│   User Space    │     │   Agent Space   │
├─────────────────┤     ├─────────────────┤
│ Documents/      │     │ agent_output/   │
│ user_files/     │  ←→ │ temp_files/     │
│ settings.json   │sync │ cache/          │
└─────────────────┘     └─────────────────┘
```

Problems: need sync layer, users can't inspect agent work, duplication of state, complexity.

### The Shared Workspace Pattern

```
┌─────────────────────────────────────────┐
│           Shared Workspace              │
├─────────────────────────────────────────┤
│ Documents/                              │
│ ├── Research/                           │
│ │   └── {bookId}/        ← Agent writes │
│ │       ├── full_text.txt               │
│ │       ├── introduction.md  ← User can edit │
│ │       └── sources/                    │
│ ├── Chats/               ← Both read/write │
│ └── profile.md           ← Agent generates, user refines │
└─────────────────────────────────────────┘
         ↑                    ↑
       User                 Agent
       (UI)               (Tools)
```

**Organize by domain, not by actor.** Don't create `user_created/` vs `agent_created/` directories.

**Agent-user collaboration patterns:**
1. **Agent Drafts, User Refines** — Agent generates, user edits, future agent work builds on refinements
2. **User Seeds, Agent Expands** — User creates initial notes, agent adds research and related files
3. **Append-Only Collaboration** — For logs/activity streams, neither actor overwrites the other

**Security:** Scope the workspace to the app's documents directory. Reject absolute paths that could escape the sandbox. Protect sensitive files (`.env`, `credentials.json`). Audit agent read/write actions.

**iCloud Documents for iOS** (free multi-device sync):
- Use `FileManager.default.url(forUbiquityContainerIdentifier: nil)?.appendingPathComponent("Documents")`
- Fallback to local Documents if iCloud unavailable
- Handle `.icloud` placeholder files (trigger download)
- Use `NSFileCoordinator` for conflict-safe writes

**Shared Workspace Checklist:**
- [ ] Single shared directory for agent and user data
- [ ] Organized by domain, not by actor
- [ ] File tools scoped to workspace (no escape)
- [ ] `read_file`, `write_file`, `list_files` tools provided
- [ ] UI observes same files agent writes (file watching or shared store)
- [ ] Agent reads user modifications before overwriting
- [ ] System prompt acknowledges user may edit files

---

## Agent Execution Patterns

### Completion Signals

**Anti-pattern: Heuristic Detection**
- Consecutive iterations without tool calls
- Checking for expected output files
- Tracking "no progress" states
- Time-based timeouts

These break in edge cases and create unpredictable behavior.

**Pattern: Explicit Completion Tool**

```typescript
tool("complete_task", {
  summary: z.string().describe("Summary of what was accomplished"),
  status: z.enum(["success", "partial", "blocked"]).optional(),
}, async ({ summary, status = "success" }) => {
  return { text: summary, shouldContinue: false };  // Key: signals loop should stop
});
```

**The ToolResult Pattern — three common cases:**
```
Tool succeeded, keep going:    { success: true,  output: "...", shouldContinue: true  }
Tool failed but recoverable:   { success: false, output: "...", shouldContinue: true  }
Task done, stop the loop:      { success: true,  output: "...", shouldContinue: false }
```

**Key insight:** `success/failure` is orthogonal to `continue/stop`. A tool can succeed AND signal stop. A tool can fail AND signal continue.

**System prompt guidance:**
```markdown
## Completing Tasks
When you've accomplished the user's request:
1. Verify your work (read back files you created, check results)
2. Call `complete_task` with a summary of what you did
3. Don't keep working after the goal is achieved

If you're blocked and can't proceed:
- Call `complete_task` with status "blocked" and explain why
- Don't loop forever trying the same thing
```

### Partial Completion

Track task-level progress for resume capability:

```
Task Statuses: pending | inProgress | completed | failed | skipped
```

**UI Progress Display:**
```
Progress: 3/5 tasks complete (60%)
✅ [1] Find source materials
✅ [2] Download full text
✅ [3] Extract key passages
❌ [4] Generate summary - Error: context limit exceeded
⏳ [5] Create outline - Pending
```

**Partial completion scenarios:**
- Agent hits max iterations: some tasks completed, some pending → checkpoint saved → resume continues from where left off
- Agent fails on one task: task marked `.failed` with notes → other tasks may continue → orchestrator doesn't auto-abort entire session
- Network error mid-task: checkpoint preserves messages → resume possible

**Checkpoint structure:**
```
sessionId, agentType, messages (full conversation history),
iterationCount, tasks (task state), customState, timestamp
```

Checkpoints expire (default 1 hour). On app launch, scan for valid checkpoints and offer resume.

### Context Limits

Agents can extend indefinitely, but context windows don't. Design for bounded context from the start.

**1. Tools should support iterative refinement:**
```typescript
tool("read_file", {
  path: z.string(),
  preview: z.boolean().default(true),  // Return first 1000 chars by default
  full: z.boolean().default(false),    // Opt-in to full content
}, ...);
```

**2. Provide consolidation tools:**
```typescript
tool("summarize_and_continue", {
  keyPoints: z.array(z.string()),
  nextSteps: z.array(z.string()),
}, async ({ keyPoints, nextSteps }) => {
  await saveSessionSummary({ keyPoints, nextSteps });
  return { text: "Summary saved. Continuing with focus on: " + nextSteps.join(", ") };
});
```

**3. Design for truncation:** Important context should be in the system prompt (always present), in files (can be re-read), or summarized in context.md.

**System prompt guidance:**
```markdown
## Managing Context
For long tasks, periodically consolidate what you've learned:
1. If you've gathered a lot of information, summarize key points
2. Save important findings to files (they persist beyond context)
3. Use `summarize_and_continue` if the conversation is getting long

Don't try to hold everything in memory. Write it down.
```

**Agent Execution Checklist:**
- [ ] `complete_task` tool provided (explicit completion)
- [ ] No heuristic completion detection
- [ ] Tool results include `shouldContinue` flag
- [ ] System prompt guides when to complete
- [ ] Tasks tracked with status (pending, in_progress, completed, failed)
- [ ] Checkpoints saved for resume
- [ ] Progress visible to user
- [ ] Tools support iterative refinement (preview vs full)
- [ ] Consolidation mechanism available
- [ ] Important context persisted to files

---

## System Prompt Design

### Features Are Prompt Sections

**Traditional approach:** Feature = function in codebase

**Prompt-native approach:** Feature = section in system prompt

```markdown
## Feedback Processing

When someone shares feedback:
1. Read the message to understand what they're saying
2. Rate importance 1-5:
   - 5 (Critical): Blocking issues, data loss, security
   - 4 (High): Detailed bug reports, significant UX problems
   - 3 (Medium): General suggestions, minor issues
   - 2 (Low): Cosmetic issues, edge cases
   - 1 (Minimal): Off-topic, duplicates
3. Store using feedback.store_feedback
4. If importance >= 4, let the channel know you're tracking it

Use your judgment. Context matters.
```

### System Prompt Structure

```markdown
# Identity
You are [Name], [brief identity statement].

## Core Behavior
[What you always do, regardless of specific request]

## Feature: [Feature Name]
[When to trigger]
[What to do]
[How to decide edge cases]

## Tool Usage
[Guidance on when/how to use available tools]

## Tone and Style
[Communication guidelines]

## What NOT to Do
[Explicit boundaries]
```

### Guide, Don't Micromanage

Tell the agent what to **achieve**, not exactly how to do it.

**Micromanaging (bad):**
```markdown
When creating a summary:
1. Use exactly 3 bullet points
2. Each bullet under 20 words
3. Use em-dashes for sub-points
4. Bold the first word of each bullet
```

**Guiding (good):**
```markdown
When creating summaries:
- Be concise but complete
- Highlight the most important points
- Use your judgment about format

The goal is clarity, not consistency.
```

### Define Judgment Criteria, Not Rules

**Rules (rigid):**
```
If the message contains "bug", set importance to 4.
If the message contains "crash", set importance to 5.
```

**Judgment criteria (flexible):**
```markdown
## Importance Rating
Rate importance based on:
- **Impact**: How many users affected? How severe?
- **Urgency**: Is this blocking? Time-sensitive?
- **Actionability**: Can we actually fix this?
- **Evidence**: Video/screenshots vs vague description

Examples:
- "App crashes when I tap submit" → 4-5 (critical, reproducible)
- "The button color seems off" → 2 (cosmetic, non-blocking)
- "Video walkthrough with 15 timestamped issues" → 5 (high-quality evidence)
```

### Iterating on System Prompts

1. **Observe** agent behavior in production
2. **Identify** gaps: "It's not rating video feedback high enough"
3. **Add guidance**: "Video walkthroughs are gold — always rate them 4-5"
4. **Deploy** (just edit the prompt file)
5. **Repeat**

No code changes. No recompilation. Just prose.

**System Prompt Checklist:**
- [ ] Clear identity statement
- [ ] Core behaviors that always apply
- [ ] Features as separate sections
- [ ] Judgment criteria instead of rigid rules
- [ ] Examples for ambiguous cases
- [ ] Explicit boundaries (what NOT to do)
- [ ] Tone guidance
- [ ] Tool usage guidance (when to use each)
- [ ] Memory/context handling

---

## Dynamic Context Injection

A static system prompt tells the agent what it CAN do. Dynamic context tells it what it can do RIGHT NOW with the user's actual data.

**The failure case:**
```
User: "Write a little thing about Catherine the Great in my reading feed"
Agent: "What system are you referring to? I'm not sure what reading feed means."
```

The agent failed because it didn't know what books exist, what the "reading feed" is, or what tools it has to publish there.

**The fix:** Inject runtime context about app state into the system prompt.

### What Context to Inject

**1. Available Resources** — What data/files exist that the agent can access?
```
## Available in User's Library
Books:
- "Moby Dick" by Herman Melville (id: book_123)
- "1984" by George Orwell (id: book_456)
```

**2. Current State** — What has the user done recently?
```
## Recent Activity
- 2 hours ago: Highlighted passage in "1984" about surveillance
- Yesterday: Completed research on "Moby Dick" whale symbolism
```

**3. Capabilities Mapping** — What tool maps to what UI feature?
```
## What You Can Do
| User Says | You Should Use | Result |
|-----------|----------------|--------|
| "my feed" / "reading feed" | publish_to_feed | Creates insight in Feed tab |
| "my library" / "my books" | read_library | Shows their book collection |
```

**4. Domain Vocabulary** — Explain app-specific terms.
```
## Vocabulary
- **Feed**: The Feed tab showing reading insights and analyses
- **Research folder**: Documents/Research/{bookId}/
```

### Context Freshness

- Inject fresh context at agent initialization (not cached from app launch)
- For long sessions, provide a `refresh_context` tool
- What NOT to do: use stale context from app launch — books may have been added, activity may have changed

**Context Injection Checklist:**
Before launching an agent:
- [ ] System prompt includes current resources (books, files, data)
- [ ] Recent activity is visible to the agent
- [ ] Capabilities are mapped to user vocabulary
- [ ] Domain-specific terms are explained
- [ ] Context is fresh (gathered at agent start, not cached)

When adding new features:
- [ ] New resources are included in context injection
- [ ] New capabilities are documented in system prompt
- [ ] User vocabulary for the feature is mapped

---

## Action Parity Discipline

### The Capability Map

Maintain a structured map of UI actions to agent tools:

| UI Action | UI Location | Agent Tool | System Prompt Reference |
|-----------|-------------|------------|-------------------------|
| View library | Library tab | `read_library` | "View books and highlights" |
| Add book | Library → Add | `add_book` | "Add books to library" |
| Publish insight | Analysis view | `publish_to_feed` | "Create insights for Feed tab" |

Status meanings:
- ✅ Done: Tool exists and is documented in system prompt
- ⚠️ Missing: UI action exists but no agent equivalent
- 🚫 N/A: User-only action (e.g., biometric auth, camera capture)

### The Action Parity Workflow

When adding a new feature, before merging any PR:

```
1. What action is this?
   → "User can publish an insight to their reading feed"

2. Does an agent tool exist for this?
   → Check tool definitions
   → If NO: Create the tool

3. Is it documented in the system prompt?
   → If NO: Add documentation

4. Is the context available?
   → Does agent know what "feed" means?
   → Does agent see available books?
   → If NO: Add to context injection

5. Update the capability map
```

### PR Checklist for Agent-Native

- [ ] Every new UI action has a corresponding agent tool
- [ ] System prompt updated to mention new capability
- [ ] Agent has access to same data UI uses
- [ ] Capability map updated
- [ ] Tested with natural language request

### The Parity Audit

**Step 1: Walk through every screen and list what users can do**

**Step 2: Check tool coverage for each action**
```
✅ View list of books      → read_library
⚠️ Filter by category     → MISSING (add filter param to read_library)
⚠️ Add new book           → MISSING (need add_book tool)
✅ Delete book             → delete_book
```

**Step 3: Prioritize gaps**
- High priority: Add new book, create/edit/delete content, core workflow actions
- Medium priority: Filter/search variations, export functionality
- Low priority: Theme changes, settings that are UI-preference only

**Action Parity Checklist:**
For every PR with UI changes:
- [ ] Listed all new UI actions
- [ ] Verified agent tool exists for each action
- [ ] Updated system prompt with new capabilities
- [ ] Added to capability map
- [ ] Tested with natural language request

For periodic audits:
- [ ] Walked through every screen
- [ ] Listed all possible user actions
- [ ] Checked tool coverage for each
- [ ] Prioritized gaps by likelihood of user request
- [ ] Created issues for high-priority gaps

---

## From Primitives to Domain Tools

### Start with Pure Primitives

Begin every agent-native system with the most atomic tools possible:
- `read_file` / `write_file` / `list_files`
- `bash` (for everything else)
- Basic storage (`store_item` / `get_item`)
- HTTP requests (`fetch_url`)

Why start here:
1. **Proves the architecture** — If it works with primitives, your prompts are doing their job
2. **Reveals actual needs** — You'll discover what domain concepts matter
3. **Maximum flexibility** — Agent can do anything, not just what you anticipated
4. **Forces good prompts** — You can't lean on tool logic as a crutch

### When to Add Domain Tools

| Reason | When to add |
|--------|-------------|
| **Vocabulary Anchoring** | Agent needs to understand domain concepts (e.g., `create_note` teaches what "note" means) |
| **Guardrails** | Operations need validation the agent shouldn't decide (e.g., enforce headline length, check content policies) |
| **Efficiency** | Common operations would take many primitive calls |

### The Rule for Domain Tools

**Domain tools should represent one conceptual action from the user's perspective.** They can include mechanical validation, but judgment about what to do or whether to do it belongs in the prompt.

**Wrong — bundles judgment:**
```typescript
tool("analyze_and_publish", async ({ input }) => {
  const analysis = analyzeContent(input);      // Tool decides how to analyze
  const shouldPublish = analysis.score > 0.7;  // Tool decides whether to publish
  if (shouldPublish) await publish(analysis.summary);  // Tool decides what to publish
});
```

**Right — one action, agent decides:**
```typescript
tool("analyze_content", { content: z.string() }, ...);  // Returns analysis
tool("publish", { content: z.string() }, ...);          // Publishes what agent provides
// Prompt: "Analyze the content. If it's high quality, publish a summary."
```

**The test:** Ask "Who is making the decision here?" If the answer is "the tool code" → refactor. If "the agent based on the prompt" → good.

### Keep Primitives Available

Domain tools are **shortcuts, not gates.** Unless there's a specific reason (security, data integrity), the agent should still be able to use underlying primitives for edge cases.

**When to gate (make domain tool the only way):**
- Security: user authentication, payment processing
- Data integrity: operations that must maintain invariants
- Audit requirements: actions that must be logged in specific ways

**The default is open.**

### Graduating to Code

```
Stage 1: Agent uses primitives in a loop
         → Flexible, proves the concept
         → Slow, potentially expensive

Stage 2: Add domain tools for common operations
         → Faster, still agent-orchestrated
         → Agent still decides when/whether to use

Stage 3: For hot paths, implement in optimized code
         → Fast, deterministic
         → Agent can still trigger, but execution is code
```

Even when an operation graduates to code, the agent should be able to trigger the optimized operation and fall back to primitives for edge cases.

### Decision Frameworks

**Should I add a domain tool?**

| Question | If Yes |
|----------|--------|
| Is the agent confused about what this concept means? | Add for vocabulary anchoring |
| Does this operation need validation the agent shouldn't decide? | Add with guardrails |
| Is this a common multi-step operation? | Add for efficiency |
| Would changing behavior require code changes? | Keep as prompt instead |

**Should I graduate to code?**

| Question | If Yes |
|----------|--------|
| Is this operation called very frequently? | Consider graduating |
| Does latency matter significantly? | Consider graduating |
| Are token costs problematic? | Consider graduating |
| Do you need deterministic behavior? | Graduate to code |

**Should I gate access?**

| Question | If Yes |
|----------|--------|
| Is there a security requirement? | Gate appropriately |
| Must this operation maintain data integrity? | Gate appropriately |
| Is it just "safer" with no specific risk? | Keep primitives available |

---

## Self-Modification

Self-modification is the advanced tier of agent-native engineering: agents that can evolve their own code, prompts, and behavior.

### What Self-Modification Enables

- **Code modification:** Read source files, write fixes/features, commit/push, trigger builds, verify builds pass
- **Prompt evolution:** Edit system prompt based on feedback, add new feature sections, refine judgment criteria
- **Infrastructure control:** Pull latest code, merge from branches, restart after changes, roll back if something breaks
- **Site/output generation:** Generate and maintain websites, create documentation, build dashboards

### Required Guardrails

**Approval gates for code changes:**
```typescript
tool("write_file", async ({ path, content }) => {
  if (isCodeFile(path)) {
    pendingChanges.set(path, content);
    const diff = generateDiff(path, content);
    return { text: `Requires approval:\n\n${diff}\n\nReply "yes" to apply.` };
  }
  // Non-code files apply immediately
  writeFileSync(path, content);
  return { text: `Wrote ${path}` };
});
```

**Auto-commit before changes:**
```typescript
tool("self_deploy", async () => {
  runGit("stash");           // Save current state first
  runGit("fetch origin");
  runGit("merge origin/main --no-edit");
  runCommand("npm run build");  // Build and verify
  scheduleRestart();             // Only then restart
});
```

**Build verification:** Don't restart unless build passes. Rollback the merge if build fails.

**Health checks after restart:**
```typescript
tool("health_check", async () => {
  return { text: JSON.stringify({ status: "healthy", uptime, build, git }, null, 2) };
});
```

### Git-Based Self-Modification

```
main                      # Shared code
├── instance/bot-a       # Instance A's branch
├── instance/bot-b       # Instance B's branch
└── instance/bot-c       # Instance C's branch
```

**Essential git tools:**
```
status, diff, log, commit_code, git_push, pull, rollback
```

### When to Implement Self-Modification

Good candidates:
- Long-running autonomous agents
- Agents that need to adapt to feedback
- Systems where behavior evolution is valuable
- Internal tools where rapid iteration matters

Not necessary for:
- Simple single-task agents
- Highly regulated environments
- Systems where behavior must be auditable
- One-off or short-lived agents

Start with a non-self-modifying prompt-native agent. Add self-modification when you need it.

**Self-Modification Checklist:**
- [ ] Git-based version control set up
- [ ] Approval gates for code changes
- [ ] Build verification before restart
- [ ] Rollback mechanism available
- [ ] Health check endpoint
- [ ] Agent can read all project files
- [ ] Agent can write files (with appropriate approval)
- [ ] Agent can commit and push
- [ ] Agent can pull updates
- [ ] Agent can restart itself
- [ ] Agent can roll back if needed

---

## Product Implications

### Progressive Disclosure of Complexity

The best agent-native applications are simple to start but endlessly powerful (the Excel analogy).

**Simple entry:** Basic requests work immediately with no configuration needed
```
User: "Organize my downloads"
Agent: [Does it immediately]
```

**Discoverable depth:** Users find they can do more as they explore
```
User: "Organize my downloads by project"
Agent: [Adapts]
User: "Every Monday, review last week's downloads"
Agent: [Sets up recurring workflow]
```

**No ceiling:** Power users can push the system in ways you didn't anticipate

**Design implications:**
- Don't force configuration upfront — let users start immediately
- Don't hide capabilities — make them discoverable through use
- Don't cap complexity — if the agent can do it, let users ask for it
- Do provide hints — help users discover what's possible

### Latent Demand Discovery

**Traditional approach:** Imagine what users want → build it → hope you guessed right

**Agent-native approach:**
1. Build capable foundation (atomic tools, parity)
2. Ship
3. Users ask agent for things
4. Observe what they're asking for
5. Patterns emerge
6. Formalize patterns into domain tools or prompts
7. Repeat

**What you learn:**
- When users ask and agent succeeds → real need, architecture supports it, consider optimizing
- When users ask and agent fails → real need, capability gap, fix the gap
- When users don't ask → maybe they don't need it, or maybe capability is hidden

**Implementation:** Log agent requests and track success/failure to observe patterns.

### Approval and User Agency

Applies to unsolicited agent actions (not explicit user requests).

**Stakes/Reversibility Matrix:**

| Stakes | Reversibility | Pattern | Example |
|--------|---------------|---------|---------|
| Low | Easy | **Auto-apply** | Organizing files |
| Low | Hard | **Quick confirm** | Publishing to a private feed |
| High | Easy | **Suggest + apply** | Code changes with undo |
| High | Hard | **Explicit approval** | Sending emails, payments |

**Patterns in detail:**

**Auto-apply:** Agent does it, then tells user. Easy to undo, low stakes.

**Quick confirm:** One-tap approval because stakes are low but hard to un-publish.

**Suggest + apply:** Shows what will happen, makes reversal clear. "Changes can be reverted with git."

**Explicit approval:** Requires explicit action, makes consequences clear. "This will send immediately and cannot be unsent. Type 'send' to confirm."

**Self-modification considerations:** When agents can modify their own behavior — changing prompts, adjusting workflows — the goals are: (1) Visibility: user can see what changed, (2) Understanding: user understands the effects, (3) Rollback: user can undo changes.

### Capability Visibility

Users need to discover what the agent can do. Hidden capabilities lead to underutilization.

- **Onboarding hints:** Proactively list key capabilities
- **Contextual suggestions:** After a user action, suggest related agent capabilities
- **Progressive revelation:** After user uses basic features, reveal advanced ones

**Balance:** Don't overwhelm with all capabilities upfront. Do reveal naturally through use. Don't assume users will discover on their own.

**Product Design Checklist:**
- [ ] Basic requests work immediately (no config)
- [ ] Depth is discoverable through use
- [ ] No artificial ceiling on complexity
- [ ] Agent requests are logged
- [ ] Success/failure is tracked
- [ ] Patterns are reviewed regularly
- [ ] Stakes assessed for each action type
- [ ] Reversibility assessed for each action type
- [ ] Approval pattern matches stakes/reversibility
- [ ] Onboarding reveals key capabilities

---

## Agent-Native Testing

### Testing Philosophy

**Test outcomes, not procedures.** Agents may solve problems differently each time. Verify the end state, not the path. Accept reasonable ranges, not exact values.

**Wrong (procedure-focused):**
```typescript
expect(mockProcessFeedback).toHaveBeenCalledWith({ message: "Great app!", category: "praise", priority: 2 });
```

**Right (outcome-focused):**
```typescript
const storedFeedback = await db.feedback.getLatest();
expect(storedFeedback.content).toContain("Great app");
expect(storedFeedback.importance).toBeGreaterThanOrEqual(1);
expect(storedFeedback.importance).toBeLessThanOrEqual(5);
```

### The "Can Agent Do It?" Test

For each UI feature, write a test prompt and verify the agent can accomplish it.

```typescript
test('Agent can add a book to library', async () => {
  await agent.chat("Add 'Moby Dick' by Herman Melville to my library");
  const library = await libraryService.getBooks();
  expect(library.find(b => b.title.includes("Moby Dick"))).toBeDefined();
});
```

### The "Surprise Test"

Give open-ended requests that require creative composition:

```typescript
test('Agent can handle open-ended requests', async () => {
  const result = await agent.chat("Help me organize my reading for next month");
  expect(result.toolCalls.length).toBeGreaterThan(0);
  // The agent should do SOMETHING useful — we don't specify exactly what
});
```

**What failure looks like:**
```typescript
// FAILURE: Agent can only say it can't do that
expect(result.response).not.toContain("I can't");
expect(result.response).not.toContain("I don't have a tool");
```

### Automated Parity Testing

```typescript
// capability-map.ts
export const capabilityMap = {
  "View library": "read_library",
  "Add book": "add_book",
  "Publish insight": "publish_to_feed",
  "Export data": "N/A",  // UI-only action
};

// parity.test.ts
for (const [uiAction, toolName] of Object.entries(capabilityMap)) {
  if (toolName === 'N/A') continue;
  test(`"${uiAction}" has agent tool: ${toolName}`, () => {
    expect(agentTools.map(t => t.name)).toContain(toolName);
  });
  test(`${toolName} is documented in system prompt`, () => {
    expect(systemPrompt).toContain(toolName);
  });
}
```

### Manual Testing Checklist

**Natural Language Variation Test** — Try multiple phrasings for the same request. All should work if context injection is correct.

**Edge Case Prompts:**
```
"What can you do?" → Agent should describe capabilities
"Help me with my books" → Should engage with library, not ask what "books" means
"Delete everything" → Agent should confirm before destructive actions
```

**Confusion Test:**
```
"What's in my research folder?" → Should list files, not ask "what research folder?"
"Show me my recent reading" → Should show activity, not ask "what do you mean?"
```

### CI Integration

Add agent-native tests to your CI pipeline:
- Run parity tests on every PR (fast, no API key needed)
- Run capability tests with API key on main branch
- Check system prompt completeness
- Detect capability map drift

**Cost-Aware Testing:** Use smaller models for basic tests. Cache responses for deterministic tests. Run expensive tests only on main branch.

**Testing Checklist:**
Automated:
- [ ] "Can Agent Do It?" tests for each UI action
- [ ] Location awareness tests ("write to my feed")
- [ ] Parity tests (tool exists, documented in prompt)
- [ ] Context parity tests (agent sees what UI shows)
- [ ] End-to-end flow tests
- [ ] Failure recovery tests

Manual:
- [ ] Natural language variation (multiple phrasings work)
- [ ] Edge case prompts (open-ended requests)
- [ ] Confusion test (agent knows app vocabulary)
- [ ] Surprise test (agent can be creative)

---

## Mobile Patterns (iOS)

### Why Mobile Matters

- **A file system:** Agents work with files naturally, same primitives that work everywhere
- **Rich context:** Health data, location, photos, calendars — context that doesn't exist on desktop
- **Cross-device sync:** With iCloud, all devices share the same file system without a server

**The challenge:** Agents are long-running. Mobile apps are not. iOS will background your app after seconds of inactivity. This means mobile agent apps need checkpointing, resuming, background execution, and on-device vs. cloud decisions.

### iOS Storage (iCloud-First)

Use iCloud Drive's Documents folder for the shared workspace:

| Approach | Cost | Complexity | Offline | Multi-Device |
|----------|------|------------|---------|--------------|
| Custom backend + sync | $$$ | High | Manual | Yes |
| CloudKit database | Free tier limits | Medium | Manual | Yes |
| **iCloud Documents** | Free (user's storage) | Low | Automatic | Automatic |

**When NOT to use iCloud Documents:**
- Sensitive data (use Keychain instead)
- High-frequency writes (iCloud sync has latency)
- Large media files (use CloudKit Assets)
- Shared between users (use CloudKit for sharing)

### Checkpoint/Resume Pattern

```
Agent States: idle → running → waitingForUser / backgrounded → completed / failed
```

On app backgrounding: save checkpoints for all active sessions. On foreground: scan for valid checkpoints, offer resume.

Background Task Extension: Request extra time (30-second window) when backgrounded during critical operations.

**Checkpoint structure:** sessionId, agentType, messages (full conversation history), iterationCount, tasks (task state), customState, timestamp. Checkpoints expire (default 1 hour).

### Permission Handling

- Request permissions **only when needed**, not at app launch
- Graceful degradation when permissions denied — offer alternatives
- Clear error messages with Settings deep links

### Cost-Aware Design

- Match model tier to task complexity (Haiku for quick queries, Opus for complex analysis)
- Token budgets per session
- Defer heavy operations to WiFi (warn if on cellular)
- Cache expensive operations (24-hour expiry)
- Show users estimated costs

### Offline Graceful Degradation

Identify which tools work offline (read_file, write_file, list_files, read_library) vs. online-only (web_search, web_fetch) vs. hybrid (publish_to_feed — works offline, syncs later). Queue online actions and process when connectivity returns.

**Mobile Checklist:**
- [ ] iCloud Documents as primary storage (or conscious alternative)
- [ ] Local Documents fallback when iCloud unavailable
- [ ] Handle `.icloud` placeholder files (trigger download)
- [ ] Use NSFileCoordinator for conflict-safe writes
- [ ] Checkpoint/resume for all agent sessions
- [ ] State machine for agent lifecycle
- [ ] Background task extension for critical saves
- [ ] Permissions requested only when needed
- [ ] Graceful degradation when permissions denied
- [ ] Model tier matched to task complexity
- [ ] Token budgets per session
- [ ] Network-aware (defer heavy work to WiFi)
- [ ] Caching for expensive operations
- [ ] Action queue for sync when online

---

## Refactoring to Prompt-Native

### Diagnosing Non-Prompt-Native Code

**Red flags:**

1. Tools that contain business logic (categorize, calculate, decide)
2. Prompts that tell the agent to "use process_feedback to handle messages" (agent as function caller, not decision maker)
3. Artificial limits on agent capability (allowed paths list, restricted operations)
4. Prompts that specify HOW (exactly 3 bullet points, under 20 words each)

### Step-by-Step Refactoring

**Step 1:** List all tools. Mark any with business logic, orchestration, or decision-making.

**Step 2:** Extract the hidden primitives.

| Workflow Tool | Hidden Primitives |
|---------------|-------------------|
| `process_feedback` | `store_item`, `send_message` |
| `generate_report` | `read_file`, `write_file` |
| `deploy_and_notify` | `git_push`, `send_message` |

**Step 3:** Move business logic from tool code to system prompt as natural language.

**Step 4:** Simplify tools to primitives (1 workflow tool → 2 primitive tools).

**Step 5:** Remove artificial limits. Use approval gates for writes, not artificial limits on reads.

**Step 6:** Test with outcomes, not procedures.

### Common Refactoring Challenges

**"But the agent might make mistakes!"**
Yes, and you can iterate. Change the prompt to add guidance:
```
# Before
Rate importance 1-5.

# After (if agent keeps rating too high)
Rate importance 1-5. Be conservative—most feedback is 2-3.
Only use 4-5 for truly blocking or critical issues.
```

**"We need deterministic behavior!"**
Some operations should stay in code. Prompt-native isn't all-or-nothing.
- Keep in code: security validation, rate limiting, audit logging, exact format requirements
- Move to prompts: categorization decisions, priority judgments, content generation, workflow orchestration

**Refactoring Checklist:**
Diagnosis:
- [ ] Listed all tools with business logic
- [ ] Identified artificial limits on agent capability
- [ ] Found prompts that micromanage HOW

Refactoring:
- [ ] Extracted primitives from workflow tools
- [ ] Moved business logic to system prompt
- [ ] Removed artificial limits
- [ ] Simplified tool inputs to data, not decisions

Validation:
- [ ] Agent achieves same outcomes with primitives
- [ ] Behavior can be changed by editing prompts
- [ ] New features could be added without new tools

---

## Architecture Review Checklist

When designing an agent-native system, verify these **before implementation**:

### Core Principles
- [ ] **Parity:** Every UI action has a corresponding agent capability
- [ ] **Granularity:** Tools are primitives; features are prompt-defined outcomes
- [ ] **Composability:** New features can be added via prompts alone
- [ ] **Emergent Capability:** Agent can handle open-ended requests in your domain

### Tool Design
- [ ] **Dynamic vs Static:** For external APIs where agent should have full access, use Dynamic Capability Discovery
- [ ] **CRUD Completeness:** Every entity has create, read, update, AND delete
- [ ] **Primitives not Workflows:** Tools enable capability, don't encode business logic
- [ ] **API as Validator:** Use `z.string()` inputs when the API validates, not `z.enum()`

### Files & Workspace
- [ ] **Shared Workspace:** Agent and user work in same data space
- [ ] **context.md Pattern:** Agent reads/updates context file for accumulated knowledge
- [ ] **File Organization:** Entity-scoped directories with consistent naming

### Agent Execution
- [ ] **Completion Signals:** Agent has explicit `complete_task` tool (not heuristic detection)
- [ ] **Partial Completion:** Multi-step tasks track progress for resume
- [ ] **Context Limits:** Designed for bounded context from the start

### Context Injection
- [ ] **Available Resources:** System prompt includes what exists (files, data, types)
- [ ] **Available Capabilities:** System prompt documents tools with user vocabulary
- [ ] **Dynamic Context:** Context refreshes for long sessions (or provide `refresh_context` tool)

### UI Integration
- [ ] **Agent → UI:** Agent changes reflect in UI (shared service, file watching, or event bus)
- [ ] **No Silent Actions:** Agent writes trigger UI updates immediately
- [ ] **Capability Discovery:** Users can learn what agent can do

### Mobile (if applicable)
- [ ] **Checkpoint/Resume:** Handle iOS app suspension gracefully
- [ ] **iCloud Storage:** iCloud-first with local fallback for multi-device sync
- [ ] **Cost Awareness:** Model tier selection matched to task complexity

---

## Anti-Patterns

### Common Approaches That Aren't Fully Agent-Native

**Agent as router** — Agent figures out what user wants, then calls the right function. Uses a fraction of agent capability.

**Build the app, then add agent** — Features built as code, then exposed to agent. Agent can only do what features already do. No emergent capability.

**Request/response thinking** — Agent gets input, does one thing, returns output. Misses the loop.

**Defensive tool design** — Over-constrained inputs (strict enums, validation at every layer). Prevents agent from doing unanticipated things.

**Happy path in code, agent just executes** — Code handles all edge cases; agent is just a caller.

### Specific Anti-Patterns

**THE CARDINAL SIN: Agent executes your code instead of figuring things out**

```typescript
// WRONG - You wrote the workflow, agent just executes it
tool("process_feedback", async ({ message }) => {
  const category = categorize(message);      // Your code decides
  const priority = calculatePriority(message); // Your code decides
  if (priority > 3) await notify();           // Your code decides
});

// RIGHT - Agent figures out how to process feedback
tools: store_item, send_message  // Primitives
prompt: "Rate importance 1-5 based on actionability, store feedback, notify if >= 4"
```

**Context starvation** — Agent doesn't know what resources exist in the app.
Fix: Inject available resources, capabilities, and vocabulary into system prompt.

**Orphan UI actions** — User can do something through the UI that the agent can't achieve.
Fix: Maintain parity.

**Silent actions** — Agent changes state but UI doesn't update.
Fix: Use shared data stores with reactive binding, or file system observation.

**Heuristic completion detection** — Detecting completion through heuristics is fragile.
Fix: Require agents to explicitly signal completion through a `complete_task` tool.

**Static tool mapping for dynamic APIs** — Building N tools for N API endpoints.
Fix: Use `discover` + `access` pattern with string inputs.

**Incomplete CRUD** — Agent can create but not update or delete.
Fix: Every entity needs full CRUD.

**Sandbox isolation** — Agent works in separate data space from user.
Fix: Use shared workspace where both operate on same files.

**Workflow-shaped tools** — `analyze_and_organize` bundles judgment into the tool. Break it into primitives and let the agent compose them.

**Gates without reason** — Domain tool is the only way to do something, and you didn't intend to restrict access. The default is open. Keep primitives available unless there's a specific reason to gate.

**Artificial capability limits** — Restricting what the agent can do out of vague safety concerns rather than specific risks. Be thoughtful about restricting capabilities. The agent should generally be able to do what users can do.

---

## Success Criteria

You've built an agent-native application when:

### Architecture
- [ ] The agent can achieve anything users can achieve through the UI (parity)
- [ ] Tools are atomic primitives; domain tools are shortcuts, not gates (granularity)
- [ ] New features can be added by writing new prompts (composability)
- [ ] The agent can accomplish tasks you didn't explicitly design for (emergent capability)
- [ ] Changing behavior means editing prompts, not refactoring code

### Implementation
- [ ] System prompt includes dynamic context about app state
- [ ] Every UI action has a corresponding agent tool (action parity)
- [ ] Agent tools are documented in system prompt with user vocabulary
- [ ] Agent and user work in the same data space (shared workspace)
- [ ] Agent actions are immediately reflected in the UI
- [ ] Every entity has full CRUD (Create, Read, Update, Delete)
- [ ] Agents explicitly signal completion (no heuristic detection)
- [ ] context.md or equivalent for accumulated knowledge

### Product
- [ ] Simple requests work immediately with no learning curve
- [ ] Power users can push the system in unexpected directions
- [ ] You're learning what users want by observing what they ask the agent to do
- [ ] Approval requirements match stakes and reversibility

### Mobile (if applicable)
- [ ] Checkpoint/resume handles app interruption
- [ ] iCloud-first storage with local fallback
- [ ] Background execution uses available time wisely
- [ ] Model tier matched to task complexity

### The Ultimate Test

**Describe an outcome to the agent that's within your application's domain but that you didn't build a specific feature for.**

Can it figure out how to accomplish it, operating in a loop until it succeeds?

If yes, you've built something agent-native. If it says "I don't have a feature for that" — your architecture is still too constrained.

## Quality Gates

- Architecture checklist passes before implementation
- All 8 principles addressed in design
- Parity verified for every UI action
- Context injection covers all user-visible data

## Outputs

- Architecture designs with explicit checklist sign-offs
- Tool definitions (primitives with rich outputs)
- System prompt templates (features as sections, judgment criteria)
- Capability maps (UI actions → agent tools)
- Refactored agent code from workflow-shaped to primitive-shaped

## Feeds Into

- `agent-native-audit` — Scored review of compliance with these principles
- `ce:plan` — Implementation planning incorporating these patterns
