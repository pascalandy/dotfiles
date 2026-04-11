# ce:compound

> Document a recently solved problem to compound your team's knowledge into searchable `docs/solutions/` files.

## When to Use

- After a problem is solved and the solution is verified working
- When triggered by phrases like "that worked", "it's fixed", "working now", "problem solved"
- Manually with optional context: `/ce:compound [brief context]`
- Non-trivial problems only (not simple typos or obvious errors)

## Inputs

- A solved, verified problem in the current conversation context
- Support files in the skill's `references/` and `assets/` directories:
  - `references/schema.yaml` — canonical frontmatter fields and enum values (read when validating YAML)
  - `references/yaml-schema.md` — category mapping from problem_type to directory (read when classifying)
  - `assets/resolution-template.md` — section structure for new docs (read when assembling)

## Methodology

### Execution Strategy

**Always run Full Mode by default.** Only switch to Compact-Safe Mode if the user explicitly requests it (e.g., with a `--compact` flag or "use compact mode").

---

### Full Mode

**Critical requirement:** The primary output is ONE file — the final documentation. Phase 1 subagents return TEXT DATA to the orchestrator. They must NOT write any files. Only the orchestrator writes files: the solution doc in Phase 2, and optionally a small edit to a project instruction file for discoverability.

#### Phase 0.5: Auto Memory Scan

Before launching Phase 1 subagents:

1. Read `MEMORY.md` from the auto memory directory (path known from system prompt context)
2. If the file does not exist, is empty, or is unreadable — skip and proceed to Phase 1 unchanged
3. Scan entries for relevance to the problem being documented (semantic judgment, not keyword matching)
4. If relevant entries are found, prepare a labeled excerpt block:

```
## Supplementary notes from auto memory
Treat as additional context, not primary evidence. Conversation history
and codebase findings take priority over these notes.

[relevant entries here]
```

5. Pass this block as additional context to the Context Analyzer and Solution Extractor in Phase 1
6. Tag any memory-sourced content incorporated into the final doc with `(auto memory [claude])`

If no relevant entries are found, proceed to Phase 1 without passing memory context.

#### Phase 1: Parallel Research

Launch these three subagents IN PARALLEL. Each returns text data to the orchestrator.

**1. Context Analyzer**
- Extracts conversation history
- Reads `references/schema.yaml` for enum validation and track classification
- Determines track (bug or knowledge) from the problem_type
- Identifies problem type, component, and track-appropriate fields:
  - **Bug track**: symptoms, root_cause, resolution_type
  - **Knowledge track**: applies_when (symptoms/root_cause/resolution_type optional)
- Incorporates auto memory excerpts (if provided) as supplementary evidence
- Reads `references/yaml-schema.md` for category mapping into `docs/solutions/`
- Suggests a filename using the pattern `[sanitized-problem-slug]-[date].md`
- Returns: YAML frontmatter skeleton (must include `category:` field mapped from problem_type), category directory path, suggested filename, and which track applies
- Does not invent enum values, categories, or frontmatter fields from memory — reads schema and mapping files
- Does not force bug-track fields onto knowledge-track learnings or vice versa

**2. Solution Extractor**
- Reads `references/schema.yaml` for track classification (bug vs knowledge)
- Adapts output structure based on the problem_type track
- Incorporates auto memory excerpts as supplementary evidence (conversation history and the verified fix take priority; if memory notes contradict the conversation, note the contradiction as cautionary context)

**Bug track output sections:**
- **Problem**: 1-2 sentence description of the issue
- **Symptoms**: Observable symptoms (error messages, behavior)
- **What Didn't Work**: Failed investigation attempts and why they failed
- **Solution**: The actual fix with code examples (before/after when applicable)
- **Why This Works**: Root cause explanation and why the solution addresses it
- **Prevention**: Strategies to avoid recurrence, best practices, and test cases. Include concrete code examples where applicable

**Knowledge track output sections:**
- **Context**: What situation, gap, or friction prompted this guidance
- **Guidance**: The practice, pattern, or recommendation with code examples when useful
- **Why This Matters**: Rationale and impact of following or not following this guidance
- **When to Apply**: Conditions or situations where this applies
- **Examples**: Concrete before/after or usage examples showing the practice in action

**3. Related Docs Finder**
- Searches `docs/solutions/` for related documentation
- Identifies cross-references and links
- Finds related GitHub issues (use `gh issue list --search "<keywords>" --state all --limit 5`; if `gh` is not installed, fall back to GitHub MCP tools if available; otherwise skip and note it was skipped)
- Flags any related learning or pattern docs that may now be stale, contradicted, or overly broad
- **Assesses overlap** with the new doc being created across five dimensions: problem statement, root cause, solution approach, referenced files, and prevention rules. Score as:
  - **High**: 4–5 dimensions match — essentially the same problem solved again
  - **Moderate**: 2–3 dimensions match — same area but different angle or solution
  - **Low**: 0–1 dimensions match — related but distinct
- Returns: Links, relationships, refresh candidates, and overlap assessment (score + which dimensions matched)

**Search strategy (grep-first filtering for efficiency):**
1. Extract keywords from the problem context: module names, technical terms, error messages, component types
2. If the problem category is clear, narrow search to the matching `docs/solutions/<category>/` directory
3. Use content search to pre-filter candidate files BEFORE reading any content. Run multiple searches in parallel, case-insensitive, targeting frontmatter fields:
   - `title:.*<keyword>`
   - `tags:.*(<keyword1>|<keyword2>)`
   - `module:.*<module name>`
   - `component:.*<component>`
4. If search returns >25 candidates, re-run with more specific patterns. If <3, broaden to full content search
5. Read only frontmatter (first 30 lines) of candidate files to score relevance
6. Fully read only strong/moderate matches
7. Return distilled links and relationships, not raw file contents

#### Phase 2: Assembly & Write

**WAIT for all Phase 1 subagents to complete before proceeding.**

1. Collect all text results from Phase 1 subagents
2. **Check the overlap assessment** from the Related Docs Finder before deciding what to write:

| Overlap | Action |
|---------|--------|
| **High** — existing doc covers the same problem, root cause, and solution | **Update the existing doc** with fresher context (new code examples, updated references, additional prevention tips) rather than creating a duplicate. The existing doc's path and structure stay the same. |
| **Moderate** — same problem area but different angle, root cause, or solution | **Create the new doc** normally. Flag the overlap for Phase 2.5 to recommend consolidation review. |
| **Low or none** | **Create the new doc** normally. |

When updating an existing doc, preserve its file path and frontmatter structure. Update the solution, code examples, prevention tips, and any stale references. Add a `last_updated: YYYY-MM-DD` field to the frontmatter. Do not change the title unless the problem framing has materially shifted.

3. Assemble complete markdown file from collected pieces, reading `assets/resolution-template.md` for section structure of new docs
4. Validate YAML frontmatter against `references/schema.yaml`
5. Create directory if needed: `mkdir -p docs/solutions/[category]/`
6. Write the file: `docs/solutions/[category]/[filename].md`

When creating a new doc, preserve section order from `assets/resolution-template.md` unless the user explicitly asks for a different structure.

#### Phase 2.5: Selective Refresh Check

After writing the new learning, decide whether this new solution is evidence that older docs should be refreshed. `ce:compound-refresh` is **not** a default follow-up — use it selectively.

**Invoke `ce:compound-refresh` when one or more of these are true:**
1. A related learning or pattern doc recommends an approach that the new fix now contradicts
2. The new fix clearly supersedes an older documented solution
3. The current work involved a refactor, migration, rename, or dependency upgrade that likely invalidated references in older docs
4. A pattern doc now looks overly broad, outdated, or no longer supported by the refreshed reality
5. The Related Docs Finder surfaced high-confidence refresh candidates in the same problem space
6. The Related Docs Finder reported **moderate overlap** with an existing doc

**Do NOT invoke `ce:compound-refresh` when:**
1. No related docs were found
2. Related docs still appear consistent with the new learning
3. The overlap is superficial and does not change prior guidance
4. Refresh would require a broad historical review with weak evidence

**Scoping rules:**
- If there is **one obvious stale candidate** → invoke `ce:compound-refresh` with a narrow scope hint after the new learning is written
- If there are **multiple candidates in the same area** → ask the user whether to run a targeted refresh for that module, category, or pattern set
- If context is already tight or you are in compact-safe mode → do not expand into a broad refresh automatically; instead recommend `ce:compound-refresh` as the next step with a scope hint

**When invoking or recommending, be explicit about the argument. Prefer the narrowest useful scope:**
- Specific file (one learning or pattern doc is the likely stale artifact)
- Module or component name (several related docs may need review)
- Category name (the drift is concentrated in one solutions area)
- Pattern filename or pattern topic (the stale guidance lives in `docs/solutions/patterns/`)

Examples: `ce:compound-refresh plugin-versioning-requirements`, `ce:compound-refresh payments`, `ce:compound-refresh performance-issues`, `ce:compound-refresh critical-patterns`

Do not invoke `ce:compound-refresh` without an argument unless the user explicitly wants a broad sweep. Always capture the new learning first.

#### Discoverability Check

After the learning is written and the refresh decision is made, check whether the project's instruction files would lead an agent to discover and search `docs/solutions/` before starting work in a documented area.

1. Identify which root-level instruction files exist (AGENTS.md, CLAUDE.md, or both). Read them and determine which holds substantive content — one may be a shim that includes the other. The substantive file is the assessment and edit target; ignore shims. If neither file exists, skip this check entirely.
2. Assess whether an agent reading the instruction files would learn three things:
   - That a searchable knowledge store of documented solutions exists
   - Enough about its structure to search effectively (category organization, YAML frontmatter fields like `module`, `tags`, `problem_type`)
   - When to search it (before implementing features, debugging issues, or making decisions in documented areas)
   
   This is a semantic assessment, not a string match. Use judgment — if an agent would reasonably discover and use the knowledge store after reading the file, the check passes.

3. If the spirit is already met, no action needed.
4. If not:
   a. Identify where a mention fits naturally in the file's existing structure. A line added to an existing section is almost always better than a new headed section.
   b. Draft the smallest addition that communicates the three things. Match the file's existing style and density. Keep the tone informational, not imperative — express timing as description, not instruction ("relevant when implementing or debugging in documented areas" rather than "check before implementing or debugging").
   
   Examples of calibration (adapt to the file, not copy-paste):
   
   When there's an existing directory listing or architecture section — add a line:
   ```
   docs/solutions/  # documented solutions to past problems (bugs, best practices, workflow patterns), organized by category with YAML frontmatter (module, tags, problem_type)
   ```
   
   When nothing in the file is a natural fit — a small headed section is appropriate:
   ```
   ## Documented Solutions
   
   `docs/solutions/` — documented solutions to past problems (bugs, best practices, workflow patterns), organized by category with YAML frontmatter (`module`, `tags`, `problem_type`). Relevant when implementing or debugging in documented areas.
   ```
   
   c. Explain to the user why this matters — agents without the plugin won't know to check `docs/solutions/` unless the instruction file surfaces it. Show the proposed change and where it would go, then ask for consent before making the edit. If no question tool is available, present the proposal and wait for the user's reply.

#### Phase 3: Optional Enhancement

**WAIT for Phase 2 to complete before proceeding.**

Based on problem type, optionally delegate to specialized agents to review the documentation (run in parallel):

- **performance_issue** → `performance-oracle`
- **security_issue** → `security-sentinel`
- **database_issue** → `data-integrity-guardian`
- **test_failure** → `cora-test-reviewer`
- Any code-heavy issue → `kieran-rails-reviewer` + `code-simplicity-reviewer` + `pattern-recognition-specialist`

---

### Compact-Safe Mode

**Single-pass alternative for context-constrained sessions.** When context budget is tight, this mode skips parallel subagents entirely. The orchestrator performs all work in a single sequential pass, producing a minimal but complete solution document.

The orchestrator performs ALL of the following in one sequential pass:

1. **Extract from conversation**: Identify the problem and solution from conversation history. Also read `MEMORY.md` from the auto memory directory if it exists — use relevant notes as supplementary context. Tag any memory-sourced content with `(auto memory [claude])`
2. **Classify**: Read `references/schema.yaml` and `references/yaml-schema.md`, then determine track (bug vs knowledge), category, and filename
3. **Write minimal doc**: Create `docs/solutions/[category]/[filename].md` using the appropriate track template from `assets/resolution-template.md`, with:
   - YAML frontmatter with track-appropriate fields
   - Bug track: Problem, root cause, solution with key code snippets, one prevention tip
   - Knowledge track: Context, guidance with key examples, one applicability note
4. **Skip specialized agent reviews** (Phase 3) to conserve context

In compact-safe mode, the overlap check is skipped. This means a doc may be created that overlaps with an existing one — that is acceptable; `ce:compound-refresh` will catch it later.

**Compact-safe output:**
```
✓ Documentation complete (compact-safe mode)

File created:
- docs/solutions/[category]/[filename].md

[If discoverability check found instruction files don't surface the knowledge store:]
Tip: Your AGENTS.md/CLAUDE.md doesn't surface docs/solutions/ to agents —
a brief mention helps all agents discover these learnings.

Note: This was created in compact-safe mode. For richer documentation
(cross-references, detailed prevention strategies, specialized reviews),
re-run /compound in a fresh session.
```

---

### Common Mistakes to Avoid

| Wrong | Correct |
|-------|---------|
| Subagents write files like `context-analysis.md`, `solution-draft.md` | Subagents return text data; orchestrator writes one final file |
| Research and assembly run in parallel | Research completes → then assembly runs |
| Multiple files created during workflow | One solution doc written or updated: `docs/solutions/[category]/[filename].md` (plus optional small edit to a project instruction file for discoverability) |
| Creating a new doc when an existing doc covers the same problem | Check overlap assessment; update the existing doc when overlap is high |

## Quality Gates

- Problem has been solved (not in-progress)
- Solution has been verified working
- Non-trivial problem (not simple typo or obvious error)
- YAML frontmatter validated against `references/schema.yaml`
- Section order from `assets/resolution-template.md` preserved
- Only one file written (or one existing file updated) — no intermediate draft files

## Outputs

**Primary output:** `docs/solutions/[category]/[filename].md`

**Auto-detected categories:**
- `build-errors/`
- `test-failures/`
- `runtime-errors/`
- `performance-issues/`
- `database-issues/`
- `security-issues/`
- `ui-bugs/`
- `integration-issues/`
- `logic-errors/`

**Success output (new doc):**
```
✓ Documentation complete

Auto memory: 2 relevant entries used as supplementary evidence

Subagent Results:
  ✓ Context Analyzer: Identified performance_issue in brief_system, category: performance-issues/
  ✓ Solution Extractor: 3 code fixes, prevention strategies
  ✓ Related Docs Finder: 2 related issues

Specialized Agent Reviews (Auto-Triggered):
  ✓ performance-oracle: Validated query optimization approach
  ✓ kieran-rails-reviewer: Code examples meet Rails standards
  ✓ code-simplicity-reviewer: Solution is appropriately minimal

File created:
- docs/solutions/performance-issues/n-plus-one-brief-generation.md
```

**Success output (existing doc updated due to high overlap):**
```
✓ Documentation updated (existing doc refreshed with current context)

Overlap detected: docs/solutions/performance-issues/n-plus-one-queries.md
  Matched dimensions: problem statement, root cause, solution, referenced files
  Action: Updated existing doc with fresher code examples and prevention tips

File updated:
- docs/solutions/performance-issues/n-plus-one-queries.md (added last_updated: 2026-03-24)
```

After displaying the success output, present "What's next?" options and wait for the user's selection before proceeding:
1. Continue workflow (recommended)
2. Link related documentation
3. Update other references
4. View documentation
5. Other

## Compounding Philosophy

Each documented solution compounds your team's knowledge. The first time you solve a problem takes research. Document it, and the next occurrence takes minutes.

The feedback loop:
```
Build → Test → Find Issue → Research → Improve → Document → Validate → Deploy
    ↑                                                                      ↓
    └──────────────────────────────────────────────────────────────────────┘
```

**Each unit of engineering work should make subsequent units of work easier — not harder.**

## Auto-Invoke

This skill can be auto-invoked when trigger phrases are detected: "that worked", "it's fixed", "working now", "problem solved". Use `/ce:compound [context]` to document immediately without waiting for auto-detection.

## Applicable Specialized Agents

Based on problem type, these agents can enhance documentation:

### Code Quality & Review
- **kieran-rails-reviewer**: Reviews code examples for Rails best practices
- **code-simplicity-reviewer**: Ensures solution code is minimal and clear
- **pattern-recognition-specialist**: Identifies anti-patterns or repeating issues

### Specific Domain Experts
- **performance-oracle**: Analyzes performance_issue category solutions
- **security-sentinel**: Reviews security_issue solutions for vulnerabilities
- **cora-test-reviewer**: Creates test cases for prevention strategies
- **data-integrity-guardian**: Reviews database_issue migrations and queries

### Enhancement & Documentation
- **best-practices-researcher**: Enriches solution with industry best practices
- **every-style-editor**: Reviews documentation style and clarity
- **framework-docs-researcher**: Links to framework/gem documentation references

## Feeds Into

- `ce:compound-refresh` — for targeted maintenance when new learning suggests older docs may be stale
- `ce:plan` — planning workflow that references documented solutions

## Related Commands

- `/research [topic]` — Deep investigation (searches docs/solutions/ for patterns)
- `/ce:plan` — Planning workflow (references documented solutions)
