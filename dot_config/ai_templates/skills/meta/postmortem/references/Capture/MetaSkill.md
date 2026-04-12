---
name: Capture
description: Document a recently solved problem into structured knowledge with YAML frontmatter. USE WHEN document fix, capture solution, that worked, it's fixed, compound, capture learning, solved problem, write up fix, record solution.
---

# Capture

Document a solved problem while context is fresh, creating structured documentation in `docs/solutions/` with YAML frontmatter for searchability and future reference.

## Why "Capture"?

Each documented solution compounds team knowledge. The first time a problem is solved takes research. Document it, and the next occurrence takes minutes. Knowledge compounds.

## Preconditions

- Problem has been solved (not in-progress)
- Solution has been verified working
- Non-trivial problem (not simple typo or obvious error)

## Mode Selection

Present two options before proceeding:

1. **Full** (recommended) -- complete workflow with cross-referencing, overlap detection, and specialized review. Better quality, more tokens.
2. **Lightweight** -- same documentation, single pass. Faster, no duplicate detection. Best for simple fixes or long sessions near context limits.

Do not pre-select a mode. Wait for user's choice.

## Execution

### Full Mode

#### Phase 1: Research

Launch research in parallel:

**Context Analyzer:**
- Extract problem context from conversation history
- Read `references/schema.md` for classification
- Determine category and filename using pattern `[sanitized-problem-slug]-[date].md`
- Return: YAML frontmatter skeleton, category directory, suggested filename

**Solution Extractor:**
- Read `references/schema.md` for track classification (bug vs knowledge)
- Adapt output based on track:
  - **Bug track:** Problem, Symptoms, What Didn't Work, Solution, Why This Works, Prevention
  - **Knowledge track:** Context, Guidance, Why This Matters, When to Apply, Examples

**Related Docs Finder:**
- Search `docs/solutions/` for related documentation using grep-first filtering
- Extract keywords from problem context (module names, error messages, component types)
- Read frontmatter of candidates to score relevance
- Assess overlap across five dimensions: problem statement, root cause, solution, referenced files, prevention rules
- Return: links, relationships, overlap assessment (High/Moderate/Low)

#### Phase 2: Assembly and Write

1. Collect all Phase 1 results
2. **Check overlap assessment:**

   | Overlap | Action |
   |---------|--------|
   | High | Update existing doc with fresher context |
   | Moderate | Create new doc, flag for cross-reference |
   | Low or none | Create new doc normally |

3. Assemble complete markdown from collected pieces, reading `references/resolution-template.md` for section structure
4. Validate YAML frontmatter against `references/schema.md`
5. Create directory if needed: `mkdir -p docs/solutions/[category]/`
6. Write file: `docs/solutions/[category]/[filename].md`

#### Phase 3: Post-Write

Present "What's next?" options:
1. Continue workflow (recommended)
2. Link related documentation
3. View documentation

### Lightweight Mode

Single-pass, no subagents. The orchestrator performs all work sequentially:

1. **Extract from conversation** -- identify problem and solution
2. **Classify** -- read `references/schema.md`, determine category and filename
3. **Write minimal doc** -- create `docs/solutions/[category]/[filename].md` using appropriate track template
4. **Skip specialized reviews** to conserve context

## What It Captures

- Problem symptom (exact error messages, observable behavior)
- Investigation steps tried (what didn't work and why)
- Root cause analysis (technical explanation)
- Working solution (step-by-step fix with code examples)
- Prevention strategies (how to avoid recurrence)
- Cross-references (links to related issues and docs)

## Success Output

```
Documentation complete

File created:
- docs/solutions/[category]/[filename].md

Cross-references: [N related docs found]
Overlap: [none | moderate | high (updated existing doc)]
```

## Anti-Patterns

| Wrong | Correct |
|-------|---------|
| Research and assembly run in parallel | Research completes, then assembly runs |
| Creating new doc when existing covers same problem | Check overlap; update existing when high |
| Vague descriptions ("something was wrong") | Exact error messages, file:line references |
| No code examples in solution | Before/after code snippets when applicable |
| Missing prevention guidance | Concrete strategies to avoid recurrence |

## Auto-Invoke

Triggers:
- "that worked"
- "it's fixed"
- "working now"
- "problem solved"

Manual override: invoke Capture directly to document without waiting for auto-detection.
