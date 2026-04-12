---
name: Workflows
description: Planning, subagents, and repeatable workflow patterns
tags:
  - area/ea
  - kind/doc
  - status/stable
date_created: 2025-04-11
date_updated: 2025-04-11
---

# Workflows

Use this file when the task is about how to operate OpenCode well.

## Default workflow

1. Understand the request.
2. Decide whether to stay in planning or make changes.
3. Gather context from files before editing config or prompts.
4. Make targeted changes.
5. Run a smoke check or audit when practical.

## Subagents

Use subagents when the task benefits from separation of concerns:
- narrow research
- parallel exploration
- specialized review
- contained background work

When creating a subagent:
- define a narrow job
- set clear trigger phrases
- keep permissions tight
- avoid turning a general-purpose agent into a vague catch-all

## Commands vs skills vs agents

- **Command**: a user-triggered shortcut for a repeatable prompt
- **Skill**: reusable instructions or operating procedure
- **Agent**: a routed worker with its own prompt, mode, and permissions

Choose the smallest abstraction that solves the problem.
