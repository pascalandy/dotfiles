# Project Analysis Prompt

Agent: L1 (fallback: L2)

## Template

```
Analyze project <PATH>

Context:
- Type: <directory|file>
- Hints: <hints object or null>

IF DIRECTORY:
1. Read 0o0o.md (if exists)
2. Read latest session file: <latest_session>
3. Read README.md (if exists)
4. Assess maturity 1-5

IF FILE:
1. Read content
2. Type = ideation
3. Assess maturity 1-5

Return JSON:
{
  "path": "<path>",
  "name": "<name>",
  "type": "active|ideation",
  "purpose": "<description>",
  "current_state": "<summary>",
  "maturity": <1-5>,
  "next_step": "<action>",
  "blocker": "<description|null>",
  "priority": "high|medium|low"
}
```

## Classification

- TYPE: active (code) | ideation (docs only)
- PRIORITY: high (0o0o/blocker) | medium (incomplete) | low (refinement)
- MATURITY: 1 (idea) → 5 (production)
