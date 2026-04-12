---
name: Research
description: Surface past solutions from the knowledge base before starting new work. Grep-first filtering against YAML frontmatter, relevance scoring, distilled summaries. USE WHEN search solutions, past fixes, similar problem, before I start, learnings, find related docs, knowledge base lookup, have we seen this before.
---

# Research

Surface past solutions from `docs/solutions/` before new work begins, preventing repeated mistakes and leveraging proven patterns.

## Why Research Before Building?

Every documented solution represents research time already spent. Searching before starting new work:
- Prevents debugging the same problem twice
- Surfaces proven patterns for similar challenges
- Identifies gotchas and edge cases already discovered
- Saves hours of redundant investigation

## Execution

### Step 1: Extract Keywords

From the task description, identify:

- **Module names**: e.g., "BriefSystem", "payments", "authentication"
- **Technical terms**: e.g., "N+1", "caching", "timeout", "memory"
- **Problem indicators**: e.g., "slow", "error", "500", "crash"
- **Component types**: e.g., "model", "controller", "job", "api"

### Step 2: Category-Based Narrowing (Optional)

If the task type is clear, narrow search to relevant category:

| Task Type | Search Directory |
|-----------|-----------------|
| Performance work | `docs/solutions/performance-issues/` |
| Database changes | `docs/solutions/database-issues/` |
| Bug fix | `docs/solutions/runtime-errors/`, `docs/solutions/logic-errors/` |
| Security | `docs/solutions/security-issues/` |
| UI work | `docs/solutions/ui-bugs/` |
| Integration | `docs/solutions/integration-issues/` |
| General / unclear | `docs/solutions/` (all) |

### Step 3: Grep Pre-Filter

Use grep to find candidate files BEFORE reading any content. Run multiple searches in parallel, case-insensitive, targeting frontmatter fields:

```
Grep: pattern="title:.*<keyword>" path=docs/solutions/
Grep: pattern="tags:.*(<keyword1>|<keyword2>)" path=docs/solutions/
Grep: pattern="module:.*<module>" path=docs/solutions/
Grep: pattern="component:.*<component>" path=docs/solutions/
```

Combine results from all grep calls to get candidate files (typically 5-20).

- If >25 candidates: re-run with more specific patterns
- If <3 candidates: broaden to full content search as fallback

### Step 4: Read Frontmatter Only

For each candidate, read frontmatter (first 30 lines). Extract:
- module, problem_type, component, symptoms, root_cause, tags, severity

### Step 5: Score and Rank

Match frontmatter against the task description:

**Strong matches (prioritize):**
- `module` matches the target module
- `tags` contain keywords from the task
- `symptoms` describe similar behaviors
- `component` matches the technical area

**Moderate matches (include):**
- `problem_type` is relevant
- `root_cause` suggests an applicable pattern
- Related modules mentioned

**Weak matches (skip):**
- No overlapping tags, symptoms, or modules

### Step 6: Full Read of Relevant Files

Only for strong and moderate matches, read the complete document.

### Step 7: Return Distilled Summaries

For each relevant document:

```
### [Title]
- File: docs/solutions/[category]/[filename].md
- Module: [module]
- Relevance: [why this matters for current task]
- Key Insight: [the gotcha or pattern to apply]
- Severity: [level]
```

## Output Format

```
## Knowledge Base Search Results

### Search Context
- Task: [description]
- Keywords: [tags, modules, symptoms searched]
- Files scanned: [X total]
- Relevant matches: [Y]

### Relevant Learnings

#### 1. [Title]
[Summary with key insight]

#### 2. [Title]
[Summary with key insight]

### Recommendations
- [Specific actions based on learnings]
- [Patterns to follow]
- [Gotchas to avoid]

### No Matches
[If no relevant learnings found, state this explicitly]
```

## Efficiency Rules

- Always grep before reading -- never scan all files
- Run grep calls in parallel
- Only fully read files that pass the frontmatter filter
- Return distilled summaries, not raw document contents
- Explicitly state when no matches found (this is valuable information)
