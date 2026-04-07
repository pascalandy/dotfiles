# Plan: wiki-map skill v2

> Refactor of `dot_config/ai_templates/skills/meta/wiki-map` based on cross-analysis with Hermes' `llm-wiki` skill. Adopts the strongest ideas from Hermes while preserving the architectural choices that make `wiki-map` distinct (router-based progressive disclosure, CreateWikiMap read-only guardrail, subdirectory preservation, multi-axis tag model).

**Status:** draft
**Date:** 2026-04-07
**Source skill:** `dot_config/ai_templates/skills/meta/wiki-map/`
**Reference skill:** Hermes `llm-wiki` (analyzed in chat)

---

## 1. Goals

1. **Add session orientation** — every operation in an existing wiki begins by reading SCHEMA + INDEX + recent log, so the LLM never drifts from established conventions across sessions.
2. **Add a fifth tag axis: `topic/*`** — separate the work type (`kind/*`) from the subject domain (`topic/*`), enabling reuse of `kind` semantics across projects.
3. **Make rules numerically checkable** — replace soft guidance ("cross-reference aggressively") with hard, lintable thresholds (≥2 outbound wikilinks, 200-line page split, 50-entry section split, 500-entry log rotation, 10-page mass-update confirmation).
4. **Persist contradictions in frontmatter** — make them machine-queryable instead of buried in prose.
5. **Add a per-wiki `SCHEMA.md`** — store wiki-specific overrides (domain description, custom topic tags) without polluting the global skill schema.
6. **Preserve everything that's working** — router architecture, CreateWikiMap read-only guardrail, subdirectory preservation, organize-vs-process distinction, the four existing kinds of report templates.

## 2. Non-goals

- **No `raw/` directory.** User manages source layout. If sources need a subdirectory, the user creates `references/sources/` themselves and the skill respects it.
- **No `_archive/` directory.** Archiving is handled by `status/close`. Closed pages stay in place.
- **No `related_skills` declarations.** Left null/undefined for now. Cross-skill wiring (defuddle, obsidian, qmd) is out of scope for this revision.
- **No tool-name hardcoding.** Skill stays portable across assistants — no explicit `web_extract`, `search_files`, `execute_code` references in workflow text.
- **No type-based directory hierarchy** (entities/, concepts/, comparisons/). Tag-based classification stays.
- **No version/author frontmatter metadata.** Out of scope.

---

## 3. Decisions Locked In

| # | Decision | Rationale |
|---|---|---|
| D1 | Add session orientation protocol to parent SKILL.md | Prevents cross-session drift, duplicate pages |
| D2 | Add `topic/*` as a fifth tag axis (optional) | Separate work-type from subject; reuse kinds |
| D3 | Tag axis order: `area → kind → topic → status → pty` | Topic sits between kind and status |
| D4 | Add per-wiki `SCHEMA.md` (lightweight) | Allows per-wiki domain notes and custom topics |
| D5 | Add page-creation thresholds: 2+ source mentions OR central to one source | Reproducible LLM behavior |
| D6 | Add page split threshold: 200 lines | Same |
| D7 | Add ≥2 outbound wikilinks minimum per page | Prevents orphans by construction |
| D8 | Add INDEX scaling: split section at 50 entries, meta map at 200 total | Fixes the flat-INDEX scaling problem |
| D9 | Add LOG rotation at 500 entries → `LOG-YYYY.md` | Bounds orientation read cost |
| D10 | Move contradictions to frontmatter: `contradictions: [page-name]` | Machine-queryable |
| D11 | Add 10-page mass-update confirmation gate | Replace IngestBatch's arbitrary "5 new pages" rule |
| D12 | Keep CreateWikiMap read-only guardrail unchanged | Strongest property in the skill |
| D13 | Keep subdirectory preservation rule unchanged | User-respect property |
| D14 | Keep organize-vs-process hard separation | Prevents body rewrites during organize |
| D15 | Keep router + sub-SKILL architecture | Token-efficient, scales |
| D16 | Closed pages (`status/close`) stay in `INDEX.md`. The **user** manages closed-page entries in INDEX — the AI does not auto-mark, auto-remove, or auto-suffix them | No hidden archive directory; user owns archival semantics |
| D17 | Extract shared schema into `references/SCHEMA.md` (skill-side, not per-wiki) | Removes 3-way duplication between parent SKILL, Ingest SKILL, and workflows |
| D18 | Slim parent `SKILL.md` by moving schema reference into `references/SCHEMA.md` | Cleaner progressive disclosure |
| D19 | **Keep both** `references/ROUTER.md` AND the parent SKILL routing table — this is a meta-skill that will grow more sub-skills later, and dual routing surfaces are intentional | Future-proofing for additional sub-skills |
| D20 | Deprecate `kind/relationship` in favor of `topic/relationship` | Relationships are subject-domain, not work-type |
| D21 | The **full schema lives in the meta-skill** at `references/SCHEMA.md`, not per-wiki | Single source of truth at the skill level |

---

## 4. Tag Taxonomy v2

### 4.1 Five axes, mandatory order

```
area/* → kind/* → topic/* → status/* → pty/*
```

### 4.2 Required vs optional

| Axis | Required | Notes |
|---|---|---|
| `area/*` | always | Currently hardcoded `area/ea`; left as-is for personal use |
| `kind/*` | always | Work type — what this file *is* |
| `topic/*` | optional | Subject domain — what this file is *about* |
| `status/*` | always | Workflow state |
| `pty/*` | actionable kinds only | Priority — `task`, `bug`, `plan`, `project/*`, `hygiene` |

### 4.3 `kind/*` — the work type

```
kind/task         # Ad-hoc work item
kind/bug          # System failure, broken tool
kind/doc          # Documentation (any form)
kind/plan         # Exploratory plan or idea
kind/log          # Operational log, decision batch, retrospective
kind/wiki         # Wiki root marker (used by INDEX.md)
kind/research     # Synthesized knowledge from sources
kind/webclip      # Source snapshot, never synthesized
kind/relationship # Person, organization (when used as a page kind)
kind/tracking     # Ongoing tracking page
kind/random       # Catch-all
```

### 4.4 `topic/*` — the subject domain (NEW, optional)

```
topic/project/{name}  # Which project this relates to
topic/milestone       # Milestone tracking (was kind/milestone)
topic/playbook        # Reusable procedures
topic/relationship    # People or organizations as a topic
topic/strategy        # Strategic direction
topic/role            # Team functions
topic/template        # Template-related work
topic/reference       # Reference material
```

**Anti-sprawl rule:** New `topic/*` values must be added to the wiki's local `SCHEMA.md` before use. Schema lint flags any `topic/*` tag not declared.

### 4.5 `status/*` — workflow state (UNCHANGED)

```
status/draft     # Structure set, minimal content
status/open      # Active work, partial — default for new tickets
status/stable    # Complete, reliable reference
status/blocked   # Waiting on external input or dependency
status/parked    # Intentionally suspended
status/close     # Resolved, done (replaces "archive")
```

### 4.6 `pty/*` — priority (UNCHANGED)

```
pty/p1   # urgent
pty/p2   # normal
pty/p3   # low
```

---

## 5. New Frontmatter Schema

```yaml
---
name: Page Title
description: One-line summary
tags:
  - area/ea
  - kind/research
  - topic/project/healthwiki   # optional
  - status/open
  - pty/p2                     # optional, actionable kinds only
date_updated: YYYY-MM-DD
contradictions: [page-name]    # NEW, optional
---
```

**Rules:**
- `contradictions` is a YAML list of wikilinked page names (without brackets in YAML — bracket-render in body).
- Empty list omitted entirely (no `contradictions: []` clutter).
- Lint reads this field to surface unresolved contradictions.

---

## 6. Per-wiki `SCHEMA.md`

Each wiki gets a lightweight `SCHEMA.md` at its root, alongside `INDEX.md`. This is **not** the global skill schema (which lives in `references/SCHEMA.md` inside the skill). It is the wiki's local override.

### 6.1 Template

```markdown
---
name: Wiki Schema
description: Local schema and conventions for {Wiki Name}
tags:
  - area/ea
  - kind/doc
  - status/stable
date_updated: YYYY-MM-DD
---

# Schema

## Domain

{One paragraph on what this wiki covers and why it exists.}

## Custom Topic Tags

The following `topic/*` values are valid in this wiki (in addition to the global ones):

- `topic/project/healthwiki` — anything tied to the health-tracking project
- `topic/{custom}` — {description}

## Local Conventions

{Any wiki-specific rules: e.g. "all webclips must include the source URL in frontmatter",
 or "this wiki uses status/parked for any drug-related notes pending FDA review".}

## Contradiction Handling Notes

{Domain-specific guidance, e.g. "research papers from before 2020 are considered stale"}
```

### 6.2 What lives where

| Concern | Global skill `references/SCHEMA.md` | Per-wiki `SCHEMA.md` |
|---|---|---|
| Tag axis order | ✓ | — |
| Required `kind/*` enum | ✓ | — |
| Required `status/*` enum | ✓ | — |
| Required `pty/*` enum | ✓ | — |
| Page templates | ✓ | — |
| INDEX/LOG formats | ✓ | — |
| Domain description | — | ✓ |
| Custom `topic/*` values | — | ✓ |
| Wiki-specific conventions | — | ✓ |

---

## 7. Session Orientation Protocol (NEW)

Add to parent `SKILL.md` immediately after the Routing section. Every operation on an **existing** wiki must execute this before any read/write workflow.

### 7.1 Protocol steps

```
Before any wiki operation in an existing wiki:

1. Read the wiki's SCHEMA.md (local domain conventions, custom topics)
2. Read INDEX.md (page catalog, recent additions)
3. Read the last 30 entries of LOG.md (recent activity, current state)
4. For wikis with 100+ pages, also search for the topic of the current request
   before creating any new page
```

### 7.2 When to skip orientation

- New wiki initialization (CreateWikiMap on empty directory) — there's nothing to orient on.
- Pure routing decisions made by the parent SKILL — no file I/O yet.

### 7.3 Subdirectory preservation cross-check

During orientation, if the LLM detects that the wiki's directory structure has changed since the last LOG entry (new subdirectories, moved files), it must:
- Note the change in the orientation summary
- **Not** attempt to "fix" or normalize the structure
- Ask the user if the structure change should be reflected in INDEX.md

This preserves the existing rule: the user manages directory layout, the skill processes files wherever they are.

---

## 8. New & Changed Hard Rules

### 8.1 Page creation thresholds

**Create a new page when:**
- An entity, concept, or topic appears in **2 or more sources**, OR
- It is the central subject of one source

**Do not create a page for:**
- Passing mentions
- Footnote references
- Things outside the wiki's stated domain (per local SCHEMA.md)

**Update an existing page instead when:**
- Any of the above already has a page

### 8.2 Cross-reference minimum

Every wiki page must contain **≥2 outbound `[[wikilinks]]`** (excluding `## Related` section to count, and excluding INDEX.md and LOG.md from this rule).

A page that cannot meet this rule signals one of:
- The page covers something out of scope (delete or move)
- Related pages are missing (create them or merge this page in)
- The page is a stub (mark `status/draft`)

Lint flags pages with <2 outbound wikilinks as warnings.

### 8.3 Page splitting

**Split a page when it exceeds 200 lines** (excluding frontmatter and `## Related`). Sub-topics become their own pages, cross-linked from the original.

Lint flags pages over 200 lines as info-level.

### 8.4 INDEX.md scaling

- When any single section (by `kind/*`) exceeds **50 entries**, split it into sub-sections by first letter or by `topic/*`.
- When INDEX.md exceeds **200 total entries**, create `references/_meta/topic-map.md` grouping pages by `topic/*` for faster navigation.
- Lint flags both thresholds.

### 8.5 LOG rotation

When LOG.md exceeds **500 entries**, rename it to `LOG-{YYYY}.md` and start a fresh `LOG.md`. The orientation protocol reads only the active `LOG.md`.

Lint checks log size on every run.

### 8.6 Mass-update confirmation gate

If an ingest operation would create or modify **10 or more** existing pages, the LLM must:
1. Stop after planning the changes
2. List every page that would be created/updated
3. Ask the user to confirm before writing

This replaces the old IngestBatch "pause at 5 new pages" rule, which was per-source. The new rule is per-operation, regardless of single vs batch ingest.

### 8.7 Closed pages

Pages with `status/close` remain in `INDEX.md`. Their description in the table is suffixed with `(closed)`. They are excluded from:
- Orphan checks (closed pages may legitimately have no inbound links)
- Stale-content checks
- Cross-reference minimum rule

They are still included in:
- Contradiction checks (a closed contradiction should still surface)
- Tag/frontmatter validation

---

## 9. Workflow Changes

### 9.1 CreateWikiMap (Ingest)

**Changes:**
- Step 6 also creates `SCHEMA.md` from the new local-schema template (asks user for domain description and any initial `topic/*` tags).
- Step 7 report mentions the new SCHEMA.md.
- No changes to the read-only guardrail or subdirectory preservation.

**Unchanged:**
- Body-content read-only rule
- Move-and-rename behavior
- LOG and INDEX creation

### 9.2 IngestSingle (Ingest)

**Changes:**
- Step 1 prepended with **orientation protocol** (read SCHEMA, INDEX, last 30 LOG entries) when wiki already exists.
- Step 4 references the new page-creation thresholds (≥2 sources or central) before creating any page.
- Step 4 enforces ≥2 outbound wikilinks on every new/updated page.
- New step 4.5: if the operation would touch ≥10 pages, halt and ask for confirmation.
- Step on contradictions: when one is detected, write to **frontmatter** (`contradictions: [page]`) on both pages, in addition to the `## Contradictions` body section.

### 9.3 IngestBatch (Ingest)

**Changes:**
- Same orientation protocol prepended.
- Same ≥10-page confirmation gate (replaces the old "5 new pages" rule).
- Cross-reference pass at end now also verifies the ≥2 outbound wikilinks rule.

### 9.4 Search (Query)

**Changes:**
- Orientation protocol prepended.
- Search now also reads `references/_meta/topic-map.md` if it exists (for wikis past the 200-page threshold).

### 9.5 DeepQuery (Query)

**Changes:**
- Orientation protocol prepended.
- Contradictions section now reads from frontmatter `contradictions:` field directly, instead of grepping bodies.

### 9.6 FileAnswer (Query)

**Changes:**
- New page must satisfy ≥2 outbound wikilinks rule.
- New page count toward the ≥10-page confirmation gate (rare for FileAnswer but possible if the answer cites many sources).

### 9.7 FullSweep (Lint)

**New checks:**
- LOG size — flag if approaching 500 entries.
- INDEX section size — flag if any section exceeds 50 entries.
- INDEX total size — flag if exceeds 200 entries (suggest creating `_meta/topic-map.md`).
- Outbound wikilink minimum — flag pages with <2 outbound wikilinks (excluding closed pages).
- Page size — flag pages over 200 lines.
- Frontmatter `contradictions:` field — surface unresolved contradictions across the wiki.
- `topic/*` tag validation against local SCHEMA.md.
- Closed-page exclusion in orphan and staleness checks.

**Removed:**
- "3x average updated date" staleness rule (was fragile). Replaced by **absolute threshold: pages with `date_updated` more than 180 days old** AND `status/open` or `status/stable`.

### 9.8 QuickCheck (Lint)

**Changes:**
- Add new check types matching the new FullSweep checks.
- New request mappings:
  - "log size", "rotate log" → log size check
  - "index size", "huge index" → INDEX scaling checks
  - "thin links", "underlinked", "few links" → outbound wikilink minimum
  - "big pages", "long pages", "split" → page size check
  - "topic tags" → topic/* validation

---

## 10. Skill File Structure (After Refactor)

```
wiki-map/
├── SKILL.md                          # ~120 lines (down from 245)
└── references/
    ├── ROUTER.md                     # KEEP — single source of routing truth
    ├── SCHEMA.md                     # NEW — global schema, single source of truth
    ├── ORIENTATION.md                # NEW — orientation protocol (loaded by sub-SKILLs)
    ├── Ingest/
    │   ├── SKILL.md                  # ~100 lines (drops duplicated schema)
    │   └── workflows/
    │       ├── CreateWikiMap.md      # +SCHEMA.md creation step
    │       ├── IngestSingle.md       # +orientation, +thresholds, +frontmatter contradictions
    │       └── IngestBatch.md        # +orientation, +10-page gate
    ├── Query/
    │   ├── SKILL.md                  # ~70 lines
    │   └── workflows/
    │       ├── Search.md             # +orientation, +topic-map.md fallback
    │       ├── DeepQuery.md          # +orientation, +frontmatter contradictions
    │       └── FileAnswer.md         # +wikilink minimum
    └── Lint/
        ├── SKILL.md                  # ~80 lines (+severity rewrite)
        └── workflows/
            ├── FullSweep.md          # +6 new checks, -3x avg rule
            └── QuickCheck.md         # +5 new check mappings
```

### 10.1 Routing duplication resolution (D19)

**Decision:** Keep `references/ROUTER.md` as the single source of truth. Remove the routing table from parent `SKILL.md`'s "Invocation Scenarios" section. The parent SKILL keeps a one-line pointer: *"For routing, see `references/ROUTER.md`."*

The parent SKILL becomes a philosophy/architecture document; ROUTER.md becomes the dispatch logic.

### 10.2 Schema duplication resolution (D17, D18)

**Move into `references/SCHEMA.md`:**
- Wiki architecture diagram
- Frontmatter schema
- Tag axis order and enums
- Page template
- INDEX.md format
- LOG.md format
- Naming convention

**Remove from `wiki-map/SKILL.md`:** all of the above. Replace with: *"For the full schema, see `references/SCHEMA.md`."*

**Remove from `Ingest/SKILL.md`:** wiki structure reference, page template, INDEX format, LOG format, tag reference, naming convention. Replace with: *"For the full schema, see `../SCHEMA.md`."*

**Net effect:** schema lives in exactly one place. Workflows can be shorter because they no longer need to repeat conventions.

---

## 11. New `references/SCHEMA.md` Skeleton

```markdown
# Wiki Schema (Global)

> The single source of truth for wiki conventions. All sub-SKILLs and
> workflows reference this file. Per-wiki overrides live in each wiki's
> own SCHEMA.md.

## Wiki Architecture

{wiki-name}/
  SCHEMA.md           # Per-wiki local overrides (NEW)
  INDEX.md            # Page catalog (kind/wiki)
  references/
    LOG.md            # Append-only operational log
    {page}.md         # Wiki pages
    _meta/
      topic-map.md    # Created when INDEX exceeds 200 entries
  assets/             # Optional, for non-markdown files

## Tag Axes

Order: area → kind → topic → status → pty

### area/*  (always required)
- area/ea  (default for all pages in personal wikis)

### kind/*  (always required)
{full enum from §4.3}

### topic/*  (optional)
{full enum from §4.4, plus per-wiki extensions in local SCHEMA.md}

### status/*  (always required)
{full enum from §4.5}

### pty/*  (actionable kinds only)
{full enum from §4.6}

## Frontmatter Template
{from §5}

## Page Template
{body structure: summary paragraph, sections, ## Related, optional ## Contradictions}

## INDEX.md Format
{table format, scaling rules from §8.4}

## LOG.md Format
{append-only entry format, rotation rule from §8.5}

## Naming Convention
- kebab-case filenames
- Obsidian-style [[wikilinks]]

## Hard Rules
- ≥2 outbound wikilinks per page (§8.2)
- 200-line page split threshold (§8.3)
- 50/200 INDEX scaling (§8.4)
- 500-entry LOG rotation (§8.5)
- 10-page mass-update confirmation (§8.6)
- Closed-page handling (§8.7)
```

---

## 12. New `references/ORIENTATION.md`

A small loadable file referenced from every sub-SKILL:

```markdown
# Orientation Protocol

Before any operation on an existing wiki, perform these reads:

1. Read `{wiki}/SCHEMA.md` — local conventions and custom topics
2. Read `{wiki}/INDEX.md` — current page catalog
3. Read last 30 entries of `{wiki}/references/LOG.md` — recent activity
4. For wikis with 100+ pages, search the wiki for the request topic
   before creating any new page

## Skip orientation when:
- Initializing a brand new wiki (no SCHEMA/INDEX/LOG yet)
- The current request is pure routing (no file I/O)

## Subdirectory drift detection:
If the directory structure has changed since the last LOG entry,
note it in the orientation summary but do not attempt to normalize
or "fix" the structure. Ask the user if the change should be reflected
in INDEX.md.

## Output

After orientation, emit a one-line summary:
`Oriented: {wiki-name} | {N} pages | {M} recent log entries | {drift status}`
```

---

## 13. Migration Plan for Existing Wikis

When this v2 lands, existing wikis built with v1 need a one-time upgrade. Add a new workflow:

### 13.1 New workflow: `Ingest/workflows/UpgradeSchema.md`

**Purpose:** Upgrade an existing v1 wiki to v2 conventions.

**Steps:**
1. Detect v1 wiki (no `SCHEMA.md` at wiki root, no `topic/*` tags in any frontmatter).
2. Ask user for domain description and any custom `topic/*` tags they want to add.
3. Create `SCHEMA.md` at wiki root from the local-schema template.
4. Scan all pages and report:
   - Pages with <2 outbound wikilinks
   - Pages over 200 lines
   - INDEX section sizes (flag if any >50)
   - LOG size (flag if approaching 500)
   - Pages without `status/*` tag (assign `status/open` after confirmation)
5. Do **not** auto-add `topic/*` tags to existing pages — that requires content judgment. List candidates by `kind/*` for the user to apply manually.
6. Append to LOG.md: `[YYYY-MM-DD] upgrade | wiki | Schema upgraded to v2`

**Triggers:** "upgrade wiki", "upgrade schema", "migrate wiki to v2"

---

## 14. Open Questions

1. **Tag axis order with topic/* — confirm `area → kind → topic → status → pty`?** (Plan assumes yes.)
2. **`status/close` visibility in INDEX.md — keep visible with `(closed)` marker?** (Plan assumes yes.)
3. **`area/*` taxonomy — stay hardcoded `area/ea`, or open up?** (Plan keeps hardcoded for personal use.)
4. **Webclip handling — still kind/webclip in flat references/, or adopt your suggestion of optional `references/sources/` subdirectory?** (Plan: user manages, skill respects whatever exists.)
5. **Should `kind/relationship` be deprecated in favor of `topic/relationship`?** They overlap. (Plan: keep both for now; document overlap in SCHEMA.md.)
6. **Stale threshold — 180 days the right default?** Could be per-wiki via local SCHEMA.md. (Plan: 180 days global, overridable per wiki.)
7. **Drop `references/ROUTER.md` or drop the parent SKILL routing table?** (Plan picks: keep ROUTER.md, drop the table.)
8. **`_meta/topic-map.md` — generated by lint, or hand-maintained?** (Plan: generated by lint, regenerated on threshold breach.)

---

## 15. Validation Plan

How to verify this refactor works:

1. **Unit-style:** load each new workflow file and check that every cross-reference (`SCHEMA.md`, `ORIENTATION.md`, peer workflows) resolves.
2. **Schema lint:** the global `references/SCHEMA.md` must validate against itself — every example frontmatter in workflows must use only declared tag values.
3. **Existing wiki upgrade:** run UpgradeSchema against any existing v1 wiki (or a synthetic test fixture) and verify it produces a valid v2 wiki without modifying any page bodies.
4. **Round-trip test:** CreateWikiMap on an empty dir → IngestSingle a fake source → DeepQuery the source → FileAnswer the result → FullSweep. Should produce zero critical lint issues on a clean run.
5. **Orientation read-cost:** measure orientation token cost for a 50-page wiki and a synthetic 500-page wiki. Should stay under 10% of operation context budget.

---

## 16. Implementation Order

Suggested commit sequence:

1. **Commit 1 — extract schema:** create `references/SCHEMA.md`, remove duplicated content from parent SKILL and Ingest SKILL. Pure refactor, no behavior change.
2. **Commit 2 — orientation:** create `references/ORIENTATION.md`, prepend orientation step to all sub-SKILLs. Behavior change.
3. **Commit 3 — tag taxonomy v2:** add `topic/*` axis to SCHEMA.md, update frontmatter template, document optional usage.
4. **Commit 4 — hard rules:** add §8 rules to SCHEMA.md, update workflows to enforce them.
5. **Commit 5 — frontmatter contradictions:** update IngestSingle, DeepQuery, FullSweep to read/write `contradictions:` field.
6. **Commit 6 — lint v2:** add new checks to FullSweep and QuickCheck, remove the 3x-average staleness rule.
7. **Commit 7 — UpgradeSchema workflow:** add the migration workflow.
8. **Commit 8 — routing dedup:** drop the parent SKILL routing table, slim parent SKILL to ~120 lines.
9. **Commit 9 — per-wiki SCHEMA.md:** update CreateWikiMap to generate it; document local-schema template.
10. **Commit 10 — validation:** run round-trip test on a fixture wiki, fix any issues.

Each commit should be independently revertable. Commit 1 carries no risk. Commits 2-6 are the substantive behavior changes.

---

## 17. What Stays the Same

For the record, this refactor explicitly preserves:

- Router + sub-SKILL architecture
- CreateWikiMap read-only-on-bodies guardrail
- Subdirectory preservation rule (never flatten, never reorganize)
- Organize-vs-process hard separation
- Concrete report templates with realistic numbers
- Four-axis tag model (now five with `topic/*`)
- Status enum (`status/close` instead of archive)
- `area/ea` hardcoding (personal wiki use)
- All existing kinds (`kind/research`, `kind/webclip`, `kind/log`, etc.)
- Append-only LOG model (now with rotation)
- INDEX.md as the navigational entry point (now with scaling rules)
- Tool-portability — no hardcoded `web_extract`, `read_file`, `search_files` references

---

## 18. Summary

This plan adopts ten high-leverage ideas from Hermes' `llm-wiki` (orientation protocol, page-creation thresholds, wikilink minimum, INDEX scaling, log rotation, mass-update gate, frontmatter contradictions, page split threshold, per-wiki SCHEMA, schema dedup) while rejecting the structural choices that conflict with `wiki-map`'s identity (raw/ separation, type-based hierarchy, archive directory, hardcoded tool calls, integration ecosystem). It introduces one genuinely new axis (`topic/*`) that emerged from the conversation. The result is a tighter, more checkable, more session-resilient version of the existing skill — without losing the properties that make it good at organizing existing messy notes.

The single biggest behavioral change is the **orientation protocol**: every operation in an existing wiki now begins by re-reading the wiki's own conventions, which prevents the silent drift that destroys long-lived knowledge bases.

The single biggest structural change is **schema deduplication**: pulling the schema into `references/SCHEMA.md` so it lives in exactly one place. Every other improvement compounds off that foundation.
