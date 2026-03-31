---
name: use-subagents
description: Use when the main agent needs to delegate tasks to sub-agents. This skill defines which sub-agent to call based on the task type - reviews, batch operations, or general tasks. The main agent (1-kimi) spawns sub-agents according to the matrix.
---

# Using Sub-Agents

When the main agent (`1-kimi`) needs to delegate work, use this skill to determine which sub-agent to call.

## Matrix

- **`1-kimi`** (Kimi K2.5 Turbo via Fireworks AI)
  - **Speed**: Fastest | **Cost**: Lowest | **Intelligence**: High
  - **Use for**: Default for everything. First-pass reviews, commits, quick edits, general tasks, exploration, research.

- **`2-opus`** (Claude Opus 4.6 via Anthropic)
  - **Speed**: Slow | **Cost**: High | **Intelligence**: Highest
  - **Use for**: Second-pass reviews. Complex architecture, hard problems requiring deep reasoning.

- **`gpthigh`** (GPT-5.4 High Reasoning via OpenAI)
  - **Speed**: Medium | **Cost**: Medium-high | **Intelligence**: Very high
  - **Use for**: Third-pass reviews. Different reasoning perspective—catches issues Opus misses.

- **`gemini`** (Gemini 3.1 Pro via OpenRouter)
  - **Speed**: Medium | **Cost**: Medium | **Intelligence**: High
  - **Use for**: Fourth-pass reviews only when user explicitly requests 4 rounds.

- **`glm`** (GLM 5.1 via zai-coding-plan)
  - **Speed**: Medium-fast | **Cost**: Low | **Intelligence**: High (coding-optimized)
  - **Use for**: Batch tasks, bulk operations, large-scale refactoring, heavy tasks where cost matters.

## Review Workflow

When the user requests a review, they explicitly say "do a two pass review", "do a three pass review", or "do a four pass review". The main agent (`1-kimi`) spawns sub-agents accordingly:

**2-Pass Review**:
1. Main agent calls subagent `1-kimi` (fresh instance) for initial review
2. Main agent calls subagent `2-opus` for thorough, deep analysis

**3-Pass Review** (most common):
1. Main agent calls subagent `1-kimi` (fresh instance) for initial review
2. Main agent calls subagent `2-opus` for thorough, deep analysis
3. Main agent calls subagent `3-gpthigh` for different reasoning perspective

**4-Pass Review** (when user explicitly requests):
1. Main agent calls subagent `1-kimi` (fresh instance) for initial review
2. Main agent calls subagent `2-opus` for thorough, deep analysis
3. Main agent calls subagent `3-gpthigh` for different reasoning perspective
4. Main agent calls subagent `gemini` for additional perspective
