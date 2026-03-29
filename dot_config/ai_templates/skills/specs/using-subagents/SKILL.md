---
name: using-subagents
description: Use when the main agent needs to delegate tasks to sub-agents. This skill defines which sub-agent to call based on the task type - reviews, batch operations, or general tasks. The main agent (1-kimi) spawns sub-agents according to the matrix.
---

# Using Sub-Agents

When the main agent (`1-kimi`) needs to delegate work, use this skill to determine which sub-agent to call.

## Matrix

- **Default / General / exploration / Commits / research (local / web)** → `1-kimi`
- **Code Review** → `1-kimi` → `2-opus` → `3-gpt` → `gemini`
- **Batch Tasks** → `glm`

## Agent Profiles

### `1-kimi` (Kimi K2.5 Turbo via Fireworks AI)
- **Speed**: Fastest
- **Cost**: Lowest  
- **Intelligence**: High
- **Use for**: Everything by default. First-pass reviews, commits, quick edits, general tasks.

### `2-opus` (Claude Opus 4.6 via Anthropic)
- **Speed**: Slow (adaptive thinking)
- **Cost**: High
- **Intelligence**: Highest available
- **Use for**: Second-pass reviews, complex architecture, hard problems requiring deep reasoning.

### `3-gpt` (GPT-5.4 via OpenAI)
- **Speed**: Medium
- **Cost**: Medium-high
- **Intelligence**: Very high with high reasoning effort
- **Use for**: Third-pass reviews. Catches issues Opus misses due to different training.

### `gemini` (Gemini 3.1 Pro via OpenRouter)
- **Speed**: Medium
- **Cost**: Medium
- **Intelligence**: High with different architectural strengths
- **Use for**: Fourth-pass reviews only when user explicitly requests 4 rounds.

### `glm` (GLM 5.1 via zai-coding-plan)
- **Speed**: Medium-fast
- **Cost**: Low
- **Intelligence**: High, coding-optimized
- **Use for**: Bulk operations, large-scale refactoring, heavy tasks where cost matters.

### `4-sonnet` (Claude Sonnet 4.6 via Anthropic)
- **Speed**: Medium-fast (faster than Opus)
- **Cost**: Medium
- **Intelligence**: High
- **Use for**: When you need Claude capabilities but Opus is too slow.

## Review Workflow

When the user requests a review, they explicitly say "do a two pass review", "do a three pass review", or "do a four pass review". The main agent (`1-kimi`) spawns sub-agents accordingly:

**2-Pass Review**:
1. Main agent calls subagent `1-kimi` (fresh instance) for initial review
2. Main agent calls subagent `2-opus` for thorough, deep analysis

**3-Pass Review** (most common):
1. Main agent calls subagent `1-kimi` (fresh instance) for initial review
2. Main agent calls subagent `2-opus` for thorough, deep analysis
3. Main agent calls subagent `3-gpt` for different reasoning perspective

**4-Pass Review** (when user explicitly requests):
4. Main agent calls subagent `gemini` for additional perspective
