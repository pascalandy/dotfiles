---
description: chain-it
---
Use the subagent tool with the chain parameter to execute this workflow:

STEP 1: 
- use the @general agent to tell me what I should know about `docs/features/opencode/opencode-configurations.md` within two or three sentences.
- export the answer: `docs/features/feat-0001/{step_id}`

STEP 2: 
- Then use the @general agent to translate the answer in french, using {previous}
- export the answer: `docs/features/feat-0001/{step_id}`

Execute this as a chain, passing output between steps via {previous}
