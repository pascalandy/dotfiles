---
name: scout-planner
description: Gather context then plan implementation
---

## scout
output: context.md

Analyze the codebase for {task}

## planner
reads: context.md
model: anthropic/claude-sonnet-4-5:high
progress: true

Create an implementation plan based on {previous}
