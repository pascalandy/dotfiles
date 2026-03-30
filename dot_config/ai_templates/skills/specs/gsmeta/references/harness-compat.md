# Harness Compatibility Layer

This document maps GStack concepts (built for Claude Code) to generic primitives and
specific harness implementations. Consult this when a methodology step uses a concept
that doesn't exist natively in your current harness.

## Concept Translation Table

| GStack / Claude Code | Generic Primitive | OpenCode | Codex CLI | Notes |
|---------------------|-------------------|----------|-----------|-------|
| `Agent` tool (subagent) | Delegate subtask to a parallel worker | `Task` tool with subagent_type | `codex exec` subprocess | Use for independent review passes, parallel research |
| `AskUserQuestion` | Prompt the user and wait for response | Output text directly; user responds in chat | stdout prompt | All harnesses support direct prompting |
| `PreToolUse` hooks | Pre-execution safety check | Inline prose guards — check before running | N/A — state the warning in output | Safety skills degrade to advisory mode |
| Plan mode | Structured planning phase | `TodoWrite` tool for task tracking | Planning mode if available | Use whatever structured planning the harness offers |
| `ExitPlanMode` | End planning, begin execution | Mark TodoWrite items, begin executing | Exit planning mode | Transition signal only |
| `Read` tool | Read a file | `Read` tool | File reading capability | Universal — all harnesses have this |
| `Write` tool | Create a file | `Write` tool | File writing capability | Universal |
| `Edit` tool | Edit a file | `Edit` tool | File editing capability | Universal |
| `Bash` tool | Run a terminal command | `Bash` tool | Shell execution | Universal |
| `Glob` tool | Find files by pattern | `Glob` tool | `fd` or `find` | Most harnesses have pattern matching |
| `Grep` tool | Search file contents | `Grep` tool | `rg` or `grep` | Most harnesses have content search |
| `WebSearch` | Search the web | `WebFetch` / `defuddle` skill | Web browsing if available | Capability varies — degrade gracefully |
| `$B` (browse binary) | Headless browser automation | `browse` skill or `agent-browser` CLI | N/A | Browser-dependent skills degrade without this |
| `$D` (design binary) | Design mockup generation | N/A (manual design tools) | N/A | Design skills degrade without this |
| `$CLAUDE_SKILL_DIR` | Directory containing the current skill | Resolve from skill loading context | N/A | Used for script paths — adapt to actual location |
| `$CLAUDE_PLUGIN_DATA` | Persistent plugin data directory | `~/.gstack/` | `~/.gstack/` | Default to `~/.gstack/` on all harnesses |
| `gh` CLI | GitHub operations | `gh` | `gh` | Universal — requires gh auth |

## Browser Capability Detection

Several skills require headless browser access: `>qa`, `>qa-only`, `>design-review`,
`>benchmark`, `>canary`, `>browse`, `>connect-chrome`, `>setup-cookies`.

Detection order:
1. Check if `browse` command exists: `which browse`
2. Check if `agent-browser` exists: `which agent-browser`
3. Check if Playwright is available: `npx playwright --version`
4. If none available: report `BLOCKED` with message "This skill requires browser automation. Install gstack browse binary or agent-browser CLI."

## Subagent Spawning

Skills that use parallel analysis (review, cso, autoplan, ship) benefit from subagent delegation.

| Harness | How to Spawn | Parallelism |
|---------|-------------|-------------|
| OpenCode | `Task` tool with `subagent_type` parameter | Multiple Task calls in single message |
| Codex CLI | `codex exec` with prompt | Sequential only |
| Claude Code | `Agent` tool | Parallel via multiple Agent calls |
| Generic | Run analysis sequentially in main thread | No parallelism — slower but works |

If your harness doesn't support subagents, run all analysis passes sequentially.
This is slower but produces identical results.

## Safety Skill Adaptation

GStack's safety skills (`careful`, `freeze`, `guard`) use Claude Code's `PreToolUse` hook
system to intercept tool calls before execution. This is a Claude Code-specific API.

On harnesses without hooks:
- **careful**: Before running any destructive command (rm -rf, DROP TABLE, force push, git reset --hard, kubectl delete, docker prune), output a warning and ask for explicit confirmation.
- **freeze**: Track the allowed directory in memory. Before any file write/edit, check the path is within the allowed boundary. If not, refuse and explain why.
- **guard**: Apply both careful and freeze behaviors.
- **unfreeze**: Clear the tracked directory boundary.

These become advisory rather than enforced. The agent must self-enforce the constraints.

## Data Directory Convention

All skills that persist data use `~/.gstack/` as the root:

```
~/.gstack/
├── sessions/           # Active session tracking
├── analytics/          # Skill usage telemetry (local JSONL)
├── learnings/          # Per-project learnings (JSONL)
├── contributor-logs/   # Self-improvement field reports
├── freeze-state        # Current freeze boundary
└── config.json         # User preferences (proactive, telemetry, etc.)
```

Create this directory structure on first use if it doesn't exist.
