# Document Review

> Review requirements or plan documents through multi-persona analysis: dispatch specialized reviewer agents in parallel, auto-fix quality issues, and surface strategic questions for user decision.

## When to Use

- A requirements document (in `docs/brainstorms/`) or plan document (in `docs/plans/`) exists and needs improvement before the next stage
- User wants feedback on a document before implementing or planning
- Invoked headlessly by other skills (ce:brainstorm, ce:plan) to validate output

## Inputs

- Path to a requirements or plan document (optional in interactive mode; required in headless mode)
- Optional flag: `mode:headless` to suppress interactive prompts and return structured text output

## Methodology

### Phase 0: Detect Mode

Check arguments for `mode:headless`. Tokens starting with `mode:` are flags — strip them and use any remaining token as the document path.

**Headless mode** changes interaction model only. Classification boundaries and synthesis pipeline are identical. Differences:
- `auto` fixes applied silently (same as interactive)
- `present` findings returned as structured text — no interactive prompts
- Phase 5 returns "Review complete" immediately

**Interactive mode** (default): full interactive prompts, AskUserQuestion calls, refinement loop.

---

### Phase 1: Get and Analyze Document

**Path provided:** Read the file, proceed.

**No path, interactive mode:** Ask which document to review, or find the most recent file in `docs/brainstorms/` or `docs/plans/` using file search.

**No path, headless mode:** Output error: `"Review failed: headless mode requires a document path. Re-invoke with: Skill("compound-engineering:document-review", "mode:headless <path>")"` — do not dispatch agents.

#### Classify Document Type

- **requirements** — from `docs/brainstorms/`, focuses on what to build and why
- **plan** — from `docs/plans/`, focuses on how to build it with implementation details

#### Select Conditional Personas

Analyze document content to determine which conditional personas to activate:

**product-lens** — activate when document contains:
- User-facing features, user stories, or customer-focused language
- Market claims, competitive positioning, or business justification
- Scope decisions, prioritization language, or priority tiers with feature assignments
- Requirements with user/customer/business outcome focus

**design-lens** — activate when document contains:
- UI/UX references, frontend components, or visual design language
- User flows, wireframes, screen/page/view mentions
- Interaction descriptions (forms, buttons, navigation, modals)
- Responsive behavior or accessibility references

**security-lens** — activate when document contains:
- Auth/authorization, login flows, session management
- API endpoints exposed to external clients
- Data handling, PII, payments, tokens, credentials, encryption
- Third-party integrations with trust boundary implications

**scope-guardian** — activate when document contains:
- Multiple priority tiers (P0/P1/P2, must-have/should-have/nice-to-have)
- Large requirement count (>8 distinct requirements or implementation units)
- Stretch goals, nice-to-haves, or "future work" sections
- Goals that don't clearly connect to requirements

**adversarial** — activate when document contains:
- More than 5 distinct requirements or implementation units
- Explicit architectural or scope decisions with stated rationale
- High-stakes domains (auth, payments, data migrations, external integrations)
- Proposals of new abstractions, frameworks, or significant architectural patterns

---

### Phase 2: Announce and Dispatch Personas

#### Announce Review Team

Tell the user which personas will review and why. For conditional personas, include justification:

```
Reviewing with:
- coherence-reviewer (always-on)
- feasibility-reviewer (always-on)
- scope-guardian-reviewer -- plan has 12 requirements across 3 priority levels
- security-lens-reviewer -- plan adds API endpoints with auth flow
```

#### Always-On Personas

- `coherence-reviewer`
- `feasibility-reviewer`

#### Conditional Personas (added if activated above)

- `product-lens-reviewer`
- `design-lens-reviewer`
- `security-lens-reviewer`
- `scope-guardian-reviewer`
- `adversarial-document-reviewer`

#### Dispatch

Delegate all personas **in parallel** as subagents. Each agent receives:

| Variable | Value |
|----------|-------|
| `{persona_file}` | Full content of the agent's persona definition |
| `{schema}` | Findings schema (see below) |
| `{document_type}` | "requirements" or "plan" |
| `{document_path}` | Path to the document |
| `{document_content}` | Full text of the document |

Pass each agent the **full document** — do not split into sections.

**Error handling:** If an agent fails or times out, proceed with findings from agents that completed. Note the failed agent in the Coverage section. Do not block the entire review on a single agent failure.

**Dispatch limit:** Even at maximum (7 agents), use parallel dispatch.

#### Subagent Prompt Template

Each agent receives this prompt with variables filled in:

```
You are a specialist document reviewer.

<persona>
{persona_file}
</persona>

<output-contract>
Return ONLY valid JSON matching the findings schema below. No prose, no markdown,
no explanation outside the JSON object.

{schema}

Rules:
- Suppress any finding below your stated confidence floor.
- Every finding MUST include at least one evidence item — a direct quote from the document.
- You are operationally read-only. Do not edit the document, create files, or make changes.
  You may use non-mutating tools (file reads, glob, grep, git log) to gather context.
- Use your suppress conditions. Do not flag issues that belong to other personas.
- Set `finding_type` for every finding:
  - `error`: Something the document says that is wrong — contradictions, incorrect statements,
    design tensions, incoherent tradeoffs.
  - `omission`: Something the document forgot to say — missing mechanical steps, absent list
    entries, undefined thresholds, forgotten cross-references.
- Set `autofix_class` based on whether there is one clear correct fix, not on severity:
  - `auto`: One clear correct fix. Two categories:
    - Internal reconciliation: one part of the document is authoritative over another —
      reconcile toward the authority. (summary/detail mismatches, wrong counts, stale
      cross-references, terminology drift, prose/diagram contradictions where prose is
      authoritative)
    - Implied additions: the correct content is mechanically obvious from the document's
      own context. (missing implied step, unstated threshold, completeness gap)
    Always include `suggested_fix` for auto findings.
    NOT auto (the gap is clear but more than one reasonable fix exists): choosing an
    implementation approach when the document states a need without constraining how
    (e.g., "support offline mode" could mean service workers, local-first database,
    or queue-and-sync — there is no single obvious answer), changing scope or priority
    where the author may have weighed tradeoffs the reviewer can't see (e.g., promoting
    a P2 to P1, or cutting a feature the document intentionally keeps at a lower tier).
  - `present`: Requires judgment — strategic questions, tradeoffs, design tensions.
- `suggested_fix` required for `auto`. For `present`, include only when fix is obvious;
  frame as a question when right action is unclear.
- If no issues found, return empty findings array. Still populate residual_risks and
  deferred_questions if applicable.
</output-contract>

<review-context>
Document type: {document_type}
Document path: {document_path}

Document content:
{document_content}
</review-context>
```

---

### Phase 3: Synthesize Findings

Process in order — each step depends on the previous.

#### 3.1 Validate

Check each agent's returned JSON against the findings schema:
- Drop findings missing any required field
- Drop findings with invalid enum values
- Note agent name for malformed output in Coverage section

#### 3.2 Confidence Gate

Suppress findings below **0.50 confidence**. Store as residual concerns for potential promotion in 3.4.

Confidence thresholds:
- **Below 0.50** — suppress; finding is speculative noise
- **0.50–0.69** — include only when the persona's calibration says actionable at that confidence
- **0.70+** — report with full confidence

#### 3.3 Deduplicate

Fingerprint each finding using `normalize(section) + normalize(title)`.
Normalization: lowercase, strip punctuation, collapse whitespace.

When fingerprints match across personas:
- If findings recommend **opposing actions** — do not merge; preserve both for contradiction resolution in 3.5
- Otherwise **merge**: keep highest severity, highest confidence, union all evidence arrays, note all agreeing reviewers
- **Coverage attribution:** Attribute merged finding to persona with highest confidence. Decrement losing persona's Findings count and corresponding route bucket so `Findings = Auto + Present` stays exact.

#### 3.4 Promote Residual Concerns

Scan residual concerns (suppressed in 3.2) for:
- **Cross-persona corroboration**: residual from Persona A overlaps with above-threshold finding from Persona B → promote at P2 with confidence 0.55–0.65, `finding_type` inherited from corroborating finding
- **Concrete blocking risks**: specific risk that would block implementation → promote at P2 with confidence 0.55, `finding_type: omission`

#### 3.5 Resolve Contradictions

When personas disagree on the same section:
- Create a **combined finding** presenting both perspectives
- Set `autofix_class: present`
- Set `finding_type: error`
- Frame as a tradeoff, not a verdict

Specific conflict patterns:
- Coherence "keep for consistency" + scope-guardian "cut for simplicity" → combined, let user decide
- Feasibility "this is impossible" + product-lens "this is essential" → P1 framed as tradeoff
- Multiple personas flag same issue → merge, note consensus, increase confidence

#### 3.6 Route by Autofix Class

**Severity and autofix_class are independent.** A P1 finding can be `auto` if the correct fix is obvious. The test: is there **one clear correct fix**, or does this require judgment?

| Autofix Class | Route |
|---------------|-------|
| `auto` | Apply automatically — one clear correct fix |
| `present` | Present for user judgment |

Demote any `auto` finding that lacks a `suggested_fix` to `present`.

**Auto-eligible patterns:** summary/detail mismatch (body authoritative over overview), wrong counts, missing list entries derivable from elsewhere, stale internal cross-references, terminology drift, prose/diagram contradictions where prose is more detailed, missing steps mechanically implied by other content, unstated thresholds implied by surrounding context, completeness gaps where correct addition is obvious.

If the fix requires judgment about *what* to do (not just *what to write*), it belongs in `present`.

#### 3.7 Sort

Sort findings: P0 → P1 → P2 → P3, then by finding type (errors before omissions), then by confidence (descending), then by document order.

---

### Phase 4: Apply and Present

#### Apply Auto-fixes

Apply all `auto` findings to the document in a **single pass**:
- Edit the document inline
- Track what was changed for the "Auto-fixes Applied" section
- Do not ask for approval
- List every auto-fix in output with enough detail (section, what changed, reviewer attribution)

#### Present Remaining Findings

**Headless mode** — structured text output:

```
Document review complete (headless mode).

Applied N auto-fixes:
- <section>: <what was changed> (<reviewer>)

Findings (requires judgment):

[P0] Section: <section> — <title> (<reviewer>, confidence <N>)
  Why: <why_it_matters>
  Suggested fix: <suggested_fix or "none">

[P1] Section: <section> — <title> (<reviewer>, confidence <N>)
  Why: <why_it_matters>
  Suggested fix: <suggested_fix or "none">

Residual concerns:
- <concern> (<source>)

Deferred questions:
- <question> (<source>)
```

Omit any section with zero items.

**Interactive mode** — use the review output template:

```markdown
## Document Review Results

**Document:** docs/plans/2026-03-15-feat-user-auth-plan.md
**Type:** plan
**Reviewers:** coherence, feasibility, security-lens, scope-guardian
- security-lens -- plan adds public API endpoint with auth flow
- scope-guardian -- plan has 15 requirements across 3 priority levels

Applied 5 auto-fixes. 4 findings to consider (2 errors, 2 omissions).

### Auto-fixes Applied

- Standardized "pipeline"/"workflow" terminology to "pipeline" throughout (coherence)
- Fixed cross-reference: Section 4 referenced "Section 3.2" which is actually "Section 3.1" (coherence)
- Updated unit count from "6 units" to "7 units" to match listed units (coherence)
- Added "update API rate-limit config" step to Unit 4 -- implied by Unit 3's rate-limit introduction (feasibility)
- Added auth token refresh to test scenarios -- required by Unit 2's token expiry handling (security-lens)

### P0 -- Must Fix

#### Errors

| # | Section | Issue | Reviewer | Confidence |
|---|---------|-------|----------|------------|
| 1 | Requirements Trace | Goal states "offline support" but technical approach assumes persistent connectivity | coherence | 0.92 |

### P1 -- Should Fix

#### Errors

| # | Section | Issue | Reviewer | Confidence |
|---|---------|-------|----------|------------|
| 2 | Scope Boundaries | 8 of 12 units build admin infrastructure; only 2 touch stated goal | scope-guardian | 0.80 |

#### Omissions

| # | Section | Issue | Reviewer | Confidence |
|---|---------|-------|----------|------------|
| 3 | Implementation Unit 3 | Plan proposes custom auth but does not mention existing Devise setup or migration path | feasibility | 0.85 |

### P2 -- Consider Fixing

#### Omissions

| # | Section | Issue | Reviewer | Confidence |
|---|---------|-------|----------|------------|
| 4 | API Design | Public webhook endpoint has no rate limiting mentioned | security-lens | 0.75 |

### Residual Concerns

| # | Concern | Source |
|---|---------|--------|
| 1 | Migration rollback strategy not addressed for Phase 2 data changes | feasibility |

### Deferred Questions

| # | Question | Source |
|---|---------|--------|
| 1 | Should the API use versioned endpoints from launch? | feasibility, security-lens |

### Coverage

| Persona | Status | Findings | Auto | Present | Residual |
|---------|--------|----------|------|---------|----------|
| coherence | completed | 4 | 3 | 1 | 0 |
| feasibility | completed | 2 | 1 | 1 | 1 |
| security-lens | completed | 2 | 1 | 1 | 0 |
| scope-guardian | completed | 1 | 0 | 1 | 0 |
| product-lens | not activated | -- | -- | -- | -- |
| design-lens | not activated | -- | -- | -- | -- |
```

**Output format rules:**
- Summary line always present after reviewer list: "Applied N auto-fixes. K findings to consider (X errors, Y omissions)." Omit any zero clause.
- Only include P0–P3 sections that have findings. Within each severity, separate Errors and Omissions sub-headers.
- Coverage table always included. Findings = Auto + Present exactly (post-deduplication).
- Residual column = count of `residual_risks` from each persona's raw output (not just promoted ones).
- Use pipe-delimited markdown tables — NOT ASCII box-drawing characters.

#### Protected Artifacts

During synthesis, discard any finding that recommends deleting or removing files in:
- `docs/brainstorms/`
- `docs/plans/`
- `docs/solutions/`

---

### Phase 5: Next Action

**Headless mode:** Return "Review complete" immediately.

**Interactive mode:** Ask (via interactive question tool):

1. **Refine again** — Address the findings above, then re-review
2. **Review complete** — Next step based on document type:
   - requirements document: "Create technical plan with ce:plan"
   - plan document: "Implement with ce:work"

After 2 refinement passes, recommend completion (diminishing returns). Allow continuation if user requests.

Return "Review complete" as terminal signal for callers.

---

### What NOT to Do

- Do not rewrite the entire document
- Do not add new sections or requirements the user didn't discuss
- Do not over-engineer or add complexity
- Do not create separate review files or add metadata sections
- Do not modify caller skills

### Iteration Guidance

On subsequent passes, re-dispatch personas and re-synthesize. The auto-fix mechanism and confidence gating prevent the same findings from recurring once fixed. If findings are repetitive across passes, recommend completion.

---

## Findings Schema

```json
{
  "type": "object",
  "required": ["reviewer", "findings", "residual_risks", "deferred_questions"],
  "properties": {
    "reviewer": { "type": "string" },
    "findings": {
      "type": "array",
      "items": {
        "required": ["title","severity","section","why_it_matters","finding_type","autofix_class","confidence","evidence"],
        "properties": {
          "title": { "type": "string", "description": "Short, specific issue title. 10 words or fewer.", "maxLength": 100 },
          "severity": { "enum": ["P0","P1","P2","P3"] },
          "section": { "type": "string", "description": "Document section where the issue appears (e.g., 'Requirements Trace', 'Implementation Unit 3', 'Overview')" },
          "why_it_matters": { "type": "string", "description": "Impact statement — not 'what is wrong' but 'what goes wrong if not addressed'" },
          "autofix_class": { "enum": ["auto","present"] },
          "finding_type": { "enum": ["error","omission"] },
          "suggested_fix": { "type": ["string","null"] },
          "confidence": { "type": "number", "minimum": 0.0, "maximum": 1.0 },
          "evidence": { "type": "array", "items": { "type": "string" }, "minItems": 1 }
        }
      }
    },
    "residual_risks": { "type": "array", "items": { "type": "string" } },
    "deferred_questions": { "type": "array", "items": { "type": "string" } }
  }
}
```

Severity definitions:
- **P0** — Contradictions or gaps that would cause building the wrong thing. Must fix before proceeding.
- **P1** — Significant gap likely hit during planning or implementation. Should fix.
- **P2** — Moderate issue with meaningful downside. Fix if straightforward.
- **P3** — Minor improvement. User's discretion.

## Quality Gates

- All activated personas return valid JSON before synthesis
- Confidence gate applied before deduplication (0.50 threshold)
- `Findings = Auto + Present` exactly in Coverage table
- Auto-fixes have `suggested_fix` populated; those without are demoted to `present`
- Protected artifacts (`docs/brainstorms/`, `docs/plans/`, `docs/solutions/`) never flagged for removal

## Outputs

- Auto-fixes applied directly to the document
- Structured findings report (interactive or headless format)
- Terminal signal "Review complete" for callers

## Feeds Into

- `ce:plan` (after requirements document review)
- `ce:work` (after plan document review)
- `deepen-plan` / `deepen-plan-beta` (for plans needing depth)

## Harness Notes

Interactive question tool varies by harness:
- Claude Code: `AskUserQuestion`
- Codex: `request_user_input`
- Gemini: `ask_user`
- Fallback (no question tool): present numbered options and wait for next message

Subagent dispatch varies by harness:
- Claude Code: Agent tool
- Codex: spawn
- Others: platform-specific task delegation mechanism
