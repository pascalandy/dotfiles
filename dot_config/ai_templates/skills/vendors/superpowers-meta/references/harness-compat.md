# Harness Compatibility Layer

Superpowers methodologies use generic language. This file maps generic capabilities to specific harness primitives.

## Concept Translation Table

| Generic Capability | OpenCode | Codex | Gemini CLI | Claude Code | Cursor | Generic Fallback |
|-------------------|----------|-------|------------|-------------|--------|------------------|
| Read a file | `Read` tool | `read_file` | `read_file` | `Read` tool | file read | `cat <path>` in terminal |
| Write/create a file | `Write` tool | `write_file` | `write_file` | `Write` tool | file write | redirect in terminal |
| Edit a file | `Edit` tool | `patch_file` | `replace` | `Edit` tool | file edit | `sed`/manual in terminal |
| Search file contents | `Grep` tool | `grep` in shell | `grep_search` | `Grep` tool | search | `rg <pattern>` in terminal |
| Find files by pattern | `Glob` tool | `glob` in shell | `glob` | `Glob` tool | file search | `fd <pattern>` in terminal |
| List directory | `Bash ls` | `shell` tool | `list_directory` | `Bash ls` | terminal | `ls` in terminal |
| Run terminal command | `Bash` tool | `shell` tool | `run_shell_command` | `Bash` tool | terminal | native shell |
| Delegate to subagent | `Task` tool | `spawn_agent` (see below) | **No equivalent** | `Task` tool | background agent | Run sequentially |
| Wait for subagent result | (implicit) | `wait` | N/A | (implicit) | N/A | N/A |
| Close subagent slot | (implicit) | `close_agent` | N/A | (implicit) | N/A | N/A |
| Track tasks/progress | `TodoWrite` tool | `update_plan` | `write_todos` | `TodoWrite` tool | task list | Numbered list in response |
| Prompt the user | Direct text output | Direct text output | `ask_user` | Direct text output | Direct text output | Direct text output |
| Load a skill | `Skill` tool | fetch URL + follow | `activate_skill` | `Skill` tool | read rule file | Read reference file directly |
| Web search | `WebSearch` tool | shell `curl`/browse | `google_web_search` | `WebSearch` tool | search | manual |
| Fetch web page | `WebFetch` tool | shell `curl` | `web_fetch` | `WebFetch` tool | browser | manual |
| Persist memory across sessions | session context | session context | `save_memory` | session context | N/A | notes file |
| Rich task management | `TodoWrite` | `update_plan` | `tracker_create_task` | `TodoWrite` | task list | Numbered list |
| Read-only research mode | (none) | (none) | `enter_plan_mode` / `exit_plan_mode` | (none) | (none) | no-write discipline |
| Agent config file | `AGENTS.md` | `AGENTS.md` | `GEMINI.md` | `CLAUDE.md` | `.cursorrules` | `AGENTS.md` or equivalent |

## Capability Detection

Some methodologies reference tools that may not be available in all environments.

**Git CLI** (required by: >worktree, >finish, >request-review):
```bash
command -v git >/dev/null 2>&1 || echo "BLOCKED: git not found"
```

**GitHub CLI** (required by: >finish option 2, >receive-review thread replies):
```bash
command -v gh >/dev/null 2>&1 || echo "gh CLI not available -- manual PR creation required"
```

**Visual companion** (optional for: >brainstorm):
The visual brainstorming companion requires a Node.js HTTP server and browser access. If unavailable, degrade to text-only brainstorming. All visual companion functionality is optional -- the core brainstorming methodology works without it.

## Subagent Spawning

Several methodologies dispatch parallel or sequential subagents. Here is how each harness handles delegation:

| Harness | Parallel Subagents | Sequential Subagents | Model Selection |
|---------|-------------------|---------------------|-----------------|
| OpenCode | Multiple `Task` calls in one response | Sequential `Task` calls | `subagent_type` parameter |
| Codex | Multiple `spawn_agent` calls | Sequential `spawn_agent` calls | `--model` flag |
| Gemini CLI | **Not supported** | Run in main thread | N/A |
| Claude Code | Multiple `Task` calls in one response | Sequential `Task` calls | Agent type in `Task` tool |
| Cursor | Background agent (limited) | Sequential in main thread | Not configurable |
| Generic | **Not available** | Run in main thread | N/A |

**Fallback when subagents unavailable:** Run tasks sequentially in the main thread. Results are identical but slower. The methodologies note this explicitly where subagent dispatch is referenced.

**Subagent prompt templates:** The methodologies reference prompt templates for implementer, spec-reviewer, and code-quality-reviewer subagents. These templates are embedded in the relevant reference files (`subagent-driven-development.md`, `requesting-code-review.md`). Adapt the dispatch mechanism to your harness but preserve the prompt content.

---

## Codex-Specific Adaptations

### Multi-agent config requirement

Subagent dispatch requires explicitly enabling multi-agent support. Add to `~/.codex/config.toml`:

```toml
[features]
multi_agent = true
```

This enables `spawn_agent`, `wait`, and `close_agent` for skills like `dispatching-parallel-agents` and `subagent-driven-development`. Without this flag, subagent dispatch is unavailable and tasks must run sequentially.

### Named agent dispatch

Claude Code skills reference named agent types like `superpowers:code-reviewer`. Codex does not have a named agent registry — `spawn_agent` creates generic agents from built-in roles (`default`, `explorer`, `worker`).

When a skill says to dispatch a named agent type:

1. Find the agent's prompt file (e.g., the skill's local prompt template like `code-quality-reviewer-prompt.md`, or the prompt embedded in `references/requesting-code-review.md`)
2. Read the prompt content
3. Fill any template placeholders (`{BASE_SHA}`, `{WHAT_WAS_IMPLEMENTED}`, etc.)
4. Spawn a `worker` agent with the filled content as the `message`

| Skill instruction | Codex equivalent |
|-------------------|-----------------|
| `Task(superpowers:code-reviewer)` | `spawn_agent(agent_type="worker", message=...)` with prompt from `requesting-code-review.md` |
| `Task` with inline prompt | `spawn_agent(message=...)` with the same prompt |

### Message framing for Codex agents

The `message` parameter is user-level input, not a system prompt. Structure it for maximum instruction adherence:

```
Your task is to perform the following. Follow the instructions below exactly.

<agent-instructions>
[filled prompt content from the agent's .md file]
</agent-instructions>

Execute this now. Output ONLY the structured response following the format
specified in the instructions above.
```

Rules:
- Use **task-delegation framing** (`"Your task is..."`) rather than persona framing (`"You are..."`)
- Wrap instructions in **XML tags** — the model treats tagged blocks as authoritative
- End with an **explicit execution directive** to prevent the agent from summarizing the instructions instead of executing them

### Environment detection for worktrees

Skills that create worktrees or finish branches should detect their environment with read-only git commands before proceeding:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

Signals:
- `GIT_DIR != GIT_COMMON` → already in a linked worktree (skip creation)
- `BRANCH` empty → detached HEAD (cannot branch/push/PR from sandbox)

See `using-git-worktrees` Step 0 and `finishing-a-development-branch` Step 1 for how each skill uses these signals.

### Codex App finishing flow

When the sandbox blocks branch/push operations (detached HEAD in an externally managed worktree), the agent:

1. Commits all staged work
2. Outputs the suggested branch name, commit message, and PR description for the user to copy
3. Instructs the user to use the Codex App's native controls:
   - **"Create branch"** — names the branch, then commit/push/PR via App UI
   - **"Hand off to local"** — transfers work to the user's local checkout

The agent can still run tests and stage files even when branch/push is blocked.

---

## Gemini CLI-Specific Adaptations

### No subagent support

Gemini CLI has no equivalent to Claude Code's `Task` tool. Skills that rely on subagent dispatch (`subagent-driven-development`, `dispatching-parallel-agents`) fall back to single-session execution via `executing-plans`. No configuration can enable this — it is a platform limitation.

### Additional Gemini CLI tools

These tools are available in Gemini CLI but have no Claude Code equivalent. Use them when available to improve the experience:

| Tool | Purpose | When to use |
|------|---------|-------------|
| `list_directory` | List files and subdirectories | Alternative to `glob` for directory inspection |
| `save_memory` | Persist facts to `GEMINI.md` across sessions | Store project context, user preferences |
| `ask_user` | Request structured input from the user | Replace direct text prompts for structured responses |
| `tracker_create_task` | Rich task management (create, update, list, visualize) | Replaces `write_todos` for more complex tracking |
| `enter_plan_mode` / `exit_plan_mode` | Switch to read-only research mode before making changes | Use before planning phases that should not modify files |

### Gemini CLI skill loading

`activate_skill` is the Gemini CLI equivalent of the `Skill` tool. When a methodology says to load a skill or cross-reference, use `activate_skill` rather than reading files manually.

---

## Safety/Hook Adaptation

The original Superpowers project uses Claude Code hooks (SessionStart) to auto-load skills. In this meta-skill package:

- **No hooks are used.** All invocation is explicit via `>command`.
- If your harness supports session-start hooks and you want auto-loading, configure your harness to load this SKILL.md at session start. The `>intro` command provides the equivalent of the original session-start behavior.
- Skill cross-references in methodologies (e.g., "use superpowers:test-driven-development") mean: read the corresponding reference file from this package's `references/` directory.

## Data Directory Convention

Some methodologies persist artifacts:

| Artifact | Default Path | Purpose |
|----------|-------------|---------|
| Design specs | `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` | Brainstorming output |
| Implementation plans | `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` | Planning output |
| Worktree directory | `.worktrees/` or project preference | Isolated workspaces |
| Visual companion | `.superpowers/brainstorm/` | Browser mockup sessions |

These directories are created on first use. User preferences (from agent config files) override defaults.

---

## Cross-Reference Resolution

When a methodology says `superpowers:X` or "use superpowers:X", it resolves as follows. These are **NOT** external skills — they are reference files within this package.

| Cross-reference | Resolves to | Notes |
|----------------|-------------|-------|
| `superpowers:brainstorm` | `references/brainstorming.md` | Full brainstorming methodology |
| `superpowers:plan` | `references/planning.md` | Implementation planning methodology |
| `superpowers:tdd` / `superpowers:test-driven-development` | `references/test-driven-development.md` | TDD cycle |
| `superpowers:sdd` / `superpowers:subagent-driven-development` | `references/subagent-driven-development.md` | Parallel subagent dispatch |
| `superpowers:executing-plans` | `references/executing-plans.md` | Sequential plan execution (subagent fallback) |
| `superpowers:worktree` / `superpowers:using-git-worktrees` | `references/using-git-worktrees.md` | Worktree creation and management |
| `superpowers:finish` / `superpowers:finishing-a-development-branch` | `references/finishing-a-development-branch.md` | Branch finish, PR creation |
| `superpowers:request-review` / `superpowers:requesting-code-review` | `references/requesting-code-review.md` | Review dispatch (also contains code-reviewer agent prompt) |
| `superpowers:receive-review` / `superpowers:receiving-a-code-review` | `references/receiving-a-code-review.md` | Review response methodology |
| `superpowers:code-reviewer` | Prompt embedded in `references/requesting-code-review.md` | Agent prompt, NOT a separate skill file |
| `superpowers:dispatching-parallel-agents` | `references/dispatching-parallel-agents.md` | General parallel agent patterns |

**Important:** `superpowers:code-reviewer` refers to the **agent prompt template** embedded inside `requesting-code-review.md`, not to a standalone skill file. When dispatching this agent in Codex, extract the prompt from that reference file and use the message framing pattern described above.

Do NOT attempt to load external skill files or use harness-specific skill loading mechanisms for cross-references within this package.

## Skill Cross-References

When a reference file says "use superpowers:X", translate as:

1. Identify the target from the Cross-Reference Resolution table above
2. Read `references/<target>.md` from this package
3. Follow its methodology
4. Return to the calling methodology when complete

For agent-type cross-references (e.g., `superpowers:code-reviewer`), extract the embedded prompt from the listed reference file rather than looking for a separate file.
