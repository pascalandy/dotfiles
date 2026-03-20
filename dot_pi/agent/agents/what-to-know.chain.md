---
name: what-to-know
description: Gather context then plan implementation
---

## scout
output: context.md
model: openai/gpt-5.4:low 
progress: true

Analyze the codebase for {task}

## general
reads: context.md
model: openai/gpt-5.4:high
progress: true
output: what-to-know.md

Tell me what I should know about this project within two or three sentences {previous}
