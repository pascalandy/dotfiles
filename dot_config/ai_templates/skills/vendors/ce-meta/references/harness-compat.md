# Harness Compatibility Layer

> Translation table and adaptation rules for running Compound Engineering methodologies across AI coding assistants.

## Concept Translation Table

| Generic Primitive | OpenCode | Codex | Claude Code | Cursor | Generic / Fallback |
|---|---|---|---|---|---|
| Read a file | `Read` tool | `read_file` | `Read` tool | built-in file read | `cat <path>` in terminal |
| Write a file | `Write` tool | `write_file` | `Write` tool | built-in file write | `cat > <path>` in terminal |
| Edit a file | `Edit` tool | `apply_diff` / `edit_file` | `Edit` tool | built-in file edit | manual write of full file |
| Search file contents | `Grep` tool | `grep` / `rg` in terminal | `Grep` tool | built-in search | `rg <pattern>` in terminal |
| Find files by pattern | `Glob` tool | `find` / `fd` in terminal | `Glob` tool | built-in file find | `fd <pattern>` in terminal |
| Run terminal command | `Bash` tool | `shell` tool | `Bash` tool | terminal tool | shell execution |
| Delegate to subagent | `Task` tool (with `subagent_type`) | `codex exec` (headless) | `Task` / `Agent` tool | N/A -- run sequentially | Run sequentially in main thread |
| Prompt the user (blocking) | `AskUserQuestion` | `request_user_input` | `AskUserQuestion` | present options in chat | Print numbered options, wait for response |
| Track tasks | `TodoWrite` tool | `update_plan` | `TodoWrite` tool | N/A | Print checklist in output |
| Web fetch | `WebFetch` tool | `curl` in terminal | `WebFetch` tool | N/A | `curl` in terminal |
| Create tasks for agents | `Task` tool | `codex exec` | `TaskCreate` / `Task` tool | N/A | Run sequentially |
| Team/swarm operations | N/A | N/A | `Teammate` tool | N/A | Not available -- run sequentially |

## Capability Detection

Some skills require external binaries. Before using them, verify availability:

| Capability | Binary | Detection | If Missing |
|---|---|---|---|
| Browser automation | `agent-browser` | `which agent-browser` | BLOCKED: "Install agent-browser: `npm install -g agent-browser`" |
| Video encoding | `ffmpeg` | `which ffmpeg` | BLOCKED: "Install ffmpeg: `brew install ffmpeg`" |
| GitHub CLI | `gh` | `which gh` | BLOCKED: "Install gh: `brew install gh && gh auth login`" |
| Cloud storage sync | `rclone` | `which rclone` | BLOCKED: "Install rclone: `brew install rclone`" |
| Xcode build tools | `xcodebuildmcp` | `which xcodebuildmcp` | BLOCKED: "Install: `brew tap getsentry/xcodebuildmcp && brew install xcodebuildmcp`" |
| Image generation | `python` + `google-genai` | `python -c "import google.genai"` | BLOCKED: "Install: `pip install google-genai`" |
| Node.js scripts | `node` | `which node` | BLOCKED: "Install Node.js" |
| Python runtime | `python` / `uv` | `which python || which uv` | BLOCKED: "Install Python or uv" |

## Subagent Spawning

Skills that dispatch parallel agents must adapt to the harness:

| Harness | Parallel Dispatch Method | Max Concurrency | Notes |
|---|---|---|---|
| OpenCode | `Task` tool with `subagent_type` param | Limited by config | Multiple `Task` calls in single message for parallelism |
| Codex | `codex exec` in parallel shell commands | OS-limited | Each delegate runs headless in separate process |
| Claude Code | `Task` / `Agent` tool, or `Teammate` for swarms | ~5-8 concurrent | Supports `model` param for cost control (e.g., `model: "haiku"`) |
| Cursor | Not supported | 1 | Run all agent work sequentially in main thread |
| Generic | Not supported | 1 | Run all agent work sequentially in main thread |

**Fallback rule**: If parallel subagent dispatch is unavailable, run each agent's work sequentially in the main thread. Results are identical; execution is slower.

## Safety and Hook Adaptation

The source skills use Claude Code hook systems (`PreToolUse`, `PostToolUse`, `allowed-tools`, `disable-model-invocation`). In other harnesses:

| Hook Concept | Adaptation |
|---|---|
| `allowed-tools` (restrict tool access) | Advisory: skill lists which operations it uses. Harness enforces if capable; otherwise trust the methodology. |
| `disable-model-invocation` | The skill is a fixed procedure. Follow it literally step-by-step. Do not improvise or riff. |
| `PreToolUse` / `PostToolUse` guards | Inline the check before/after the operation. E.g., "before writing a file, verify the path is within the project directory." |
| `context: fork` | If available, run in an isolated context/worktree. Otherwise, warn user that the skill modifies files in the current working directory. |

## Data Directory Convention

Skills that persist artifacts use these directories (created on first use):

| Directory | Purpose | Used By |
|---|---|---|
| `docs/brainstorms/` | Requirements documents from brainstorming | brainstorm, plan, work |
| `docs/plans/` | Implementation plan documents | plan, work, lfg, slfg |
| `docs/solutions/` | Compounded knowledge from solved problems | compound, compound-refresh, todo-resolve |
| `docs/solutions/patterns/` | Pattern documentation | compound, compound-refresh |
| `docs/ideation/` | Ideation session outputs | ideate |
| `.context/compound-engineering/todos/` | File-based todo items | todo-create, todo-resolve, todo-triage |
| `.context/compound-engineering/ce-review/<run-id>/` | Review run artifacts | review |
| `.context/compound-engineering/feature-video/<run-id>/` | Video screenshots and output | feature-video |
| `.context/compound-engineering/todo-resolve/<run-id>/` | Resolve session scratch | todo-resolve |

## Platform Question Tool Pattern

Many skills need to ask the user blocking questions. Use the appropriate primitive:

```
OpenCode / Claude Code:  AskUserQuestion  (or present numbered options)
Codex:                   request_user_input
Gemini:                  ask_user
Cursor / Generic:        Print numbered options in output, wait for user response
```

If the harness has no blocking question mechanism, present the options clearly and pause for user input before proceeding.
