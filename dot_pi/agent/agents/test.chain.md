---
name: chain-test
description: Gather context then plan implementation
---

## scout
output: context.md
model: openai/gpt-5.4:low 

Analyze the codebase for {task}

## planner
reads: context.md
model: openai/gpt-5.4:low 
progress: true

Create an implementation plan based on {previous}
