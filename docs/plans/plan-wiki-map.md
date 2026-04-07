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
5. **Add page provenance** — `sources:` frontmatter field lets every synthesized page declare which webclip(s) it derived from.
6. **Add safe deletion** — Delete workflow that finds inbound links and offers redirect/replace/remove options before removing a page.
7. **Make IngestBatch atomic** — read all sources, plan all writes, write once. Eliminates redundant updates and partial-failure inconsistency.
8. **Acknowledge headless mode** — escape hatches in confirmation gates so the skill works in cron, webhook, and batch contexts.
9. **Single source of truth for schema** — consolidate `references/SCHEMA.md` at the meta-skill level. No per-wiki schema files.
10. **Preserve everything that's working** — router architecture, CreateWikiMap read-only guardrail, subdirectory preservation, organize-vs-process distinction, concrete report templates.

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
| D1 | Add session orientation protocol | Prevents cross-session drift, duplicate pages |
| D2 | Add `topic/*` as a fifth tag axis (optional) | Separate work-type from subject; reuse kinds |
| D3 | Tag axis order: `area → kind → topic → status → pty` | Topic sits between kind and status |
| D4 | Add page-creation thresholds: 2+ source mentions OR central to one source | Reproducible LLM behavior |
| D5 | Add page split threshold: 200 lines | Lintable |
| D6 | Add ≥2 outbound wikilinks minimum per page (with kind-based exemptions) | Prevents orphans by construction |
| D7 | Add INDEX scaling: split section at 50 entries, meta map at 200 total | Fixes the flat-INDEX scaling problem |
| D8 | Add LOG rotation at 500 entries → `LOG-YYYY.md` | Bounds orientation read cost |
| D9 | Move contradictions to frontmatter: `contradictions: [page-name]` | Machine-queryable |
| D10 | Add 10-page mass-update confirmation gate | Replace IngestBatch's arbitrary "5 new pages" rule |
| D11 | Keep CreateWikiMap read-only guardrail unchanged | Strongest property in the skill |
| D12 | Keep subdirectory preservation rule unchanged | User-respect property |
| D13 | Keep organize-vs-process hard separation | Prevents body rewrites during organize |
| D14 | Keep router + sub-SKILL architecture | Token-efficient, scales |
| D15 | Closed pages (`status/close`) stay in `INDEX.md`. The **user** manages closed-page entries in INDEX — the AI does not auto-mark, auto-remove, or auto-suffix them | No hidden archive directory; user owns archival semantics |
| D16 | Extract shared schema into `references/SCHEMA.md` at the meta-skill level | Single source of truth; removes 3-way duplication |
| D17 | Slim parent `SKILL.md` by moving schema reference into `references/SCHEMA.md` | Cleaner progressive disclosure |
| D18 | **Keep both** `references/ROUTER.md` AND the parent SKILL routing table — meta-skill will grow more sub-skills | Dual routing surfaces are intentional |
| D19 | Deprecate `kind/relationship` in favor of `topic/relationship` | Relationships are subject-domain, not work-type |
| D20 | Add `sources: [page-name]` frontmatter field for page provenance | Traceability from synthesized pages back to webclips |
| D21 | Add `date_created` alongside `date_updated` | Better stale-detection; provenance for "what's new since X" |
| D22 | Add `kind/query` for filed query answers, distinct from synthesized research | Query answers have different provenance than ingested-source pages |
| D23 | CreateWikiMap detects existing wikis and halts (suggests UpgradeSchema) instead of running destructively | Safe by default |
| D24 | **Drop `references/ORIENTATION.md`** — orientation protocol becomes §9 of `references/SCHEMA.md` | Avoids two-file split for one tightly-coupled concept |
| D25 | Add `Ingest/workflows/Delete.md` — safe-delete workflow with inbound-link cleanup | Closes the deletion loop; preserves link integrity |
| D26 | Add headless/automated mode escape hatches in Ingest sub-SKILL | Insurance for future cron/webhook/batch usage |
| D27 | Rewrite IngestBatch as atomic plan-then-write (read all → plan all → write once) | Eliminates redundant updates, partial-failure inconsistency, LOG noise |
| D28 | INDEX.md gets a header block with stats and self-documenting instruction | Cheap orientation aid |
| D29 | Wikilink minimum exemption list (see §8.2) | Rule must not apply to LOG, INDEX, webclips, etc. |
| D30 | FileAnswer adds a "wiki-worthy" judgment step before filing | Prevents pollution from trivial lookups |

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
kind/query        # Filed query answer (NEW — created by FileAnswer workflow)
kind/tracking     # Ongoing tracking page
kind/random       # Catch-all
```

**Removed in v2:** `kind/relationship` — use `topic/relationship` instead. Relationships are a subject domain, not a work type.

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
date_created: YYYY-MM-DD       # NEW — set on page creation, never changes
date_updated: YYYY-MM-DD       # bumped on every content change
sources:                       # NEW — provenance, optional
  - webclip-page-name
  - another-source
contradictions:                # optional
  - conflicting-page-name
---
```

**Rules:**
- `date_created` is set once at page creation by CreateWikiMap, IngestSingle, IngestBatch, or FileAnswer. It is never modified after creation.
- `date_updated` is bumped on any content change. For organize-only operations (CreateWikiMap adding frontmatter), `date_updated == date_created`.
- `sources` lists wiki page names (no brackets, kebab-case) of the `kind/webclip` or other source pages this page derived from. Required for `kind/research`, `kind/doc`, `kind/query`. Empty list omitted.
- `contradictions` is a YAML list of wiki page names. Empty list omitted entirely (no `contradictions: []` clutter).
- Lint reads `sources` and `contradictions` to detect orphan webclips, broken provenance, and unresolved conflicts.

---

## 6. Schema location: meta-skill only

**There is no per-wiki `SCHEMA.md`.** The full schema lives in exactly one place: `references/SCHEMA.md` inside the meta-skill. Every wiki built with this skill inherits the same schema.

This is a deliberate constraint:
- One source of truth, no drift between wikis
- New `topic/*` values are added to the meta-skill SCHEMA.md, not per-wiki
- A wiki built last year and a wiki built today follow identical conventions
- The user manages the meta-skill schema directly when they need to extend it

**What this means in practice:**
- CreateWikiMap does **not** generate a SCHEMA.md inside the wiki
- Orientation reads only INDEX.md and LOG.md (not a wiki-local SCHEMA.md)
- Adding a new `topic/*` value is a meta-skill edit, not a per-wiki edit
- Wiki contents remain self-describing through frontmatter; conventions live with the skill

If, later, a use case emerges for genuinely wiki-specific conventions (e.g. domain-specific staleness thresholds), they get added to the meta-skill SCHEMA.md as a section keyed by wiki name — not as a separate file in each wiki.

---

## 7. Session Orientation Protocol (NEW)

Add to parent `SKILL.md` immediately after the Routing section. Every operation on an **existing** wiki must execute this before any read/write workflow.

### 7.1 Protocol steps

```
Before any wiki operation in an existing wiki:

1. Read the meta-skill's references/SCHEMA.md (canonical conventions, tag enums)
2. Read the wiki's INDEX.md (page catalog, recent additions)
3. Read the last 30 entries of the wiki's LOG.md (recent activity, current state)
4. For wikis with 100+ pages, also search for the topic of the current request
   before creating any new page
```

Note: step 1 reads the **meta-skill's** SCHEMA.md, not a per-wiki file (there is none). This ensures every wiki operation starts from identical canonical conventions.

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

Pages of the **content kinds** must contain **≥2 outbound `[[wikilinks]]`** (counting wikilinks in `## Related` and in body text together).

**Content kinds (rule applies):**
- `kind/research` — synthesized knowledge must integrate with existing pages
- `kind/doc` — documentation must reference related concepts
- `kind/plan` — exploratory plans must reference what they're planning around
- `kind/query` — filed query answers reference the pages they synthesized from (often many)

**Operational kinds (rule applies softly — ≥1 wikilink, not ≥2):**
- `kind/task` — should link to the parent project or related pages
- `kind/bug` — should link to the broken component or related context
- `kind/tracking` — should link to what it's tracking

**Exempt entirely (rule does not apply):**
- `kind/wiki` — INDEX.md links to everything by design; rule is moot
- `kind/log` — LOG.md is chronological events, not content
- `kind/webclip` — immutable source snapshots; **must not be edited to add wikilinks**
- `kind/random` — unstructured catch-all

A content-kind page that cannot meet ≥2 signals one of:
- The page covers something out of scope (delete or move)
- Related pages are missing (create them, or mark this page `status/draft`)
- The page should be merged into an existing page

Lint flags violations as **warnings** for content kinds, **info** for operational kinds, and **never** for exempt kinds.

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

Pages with `status/close` remain in `INDEX.md`. **The user manages closed-page entries in INDEX manually** — the AI must not:
- Auto-suffix descriptions with `(closed)`
- Auto-remove closed pages from INDEX
- Reformat or reorder closed entries
- "Tidy up" the closed section in any way

The AI's only obligation regarding closed pages is to not break them: don't delete, don't rename, don't strip frontmatter.

Closed pages are excluded from these **lint** checks:
- Orphan checks (closed pages may legitimately have no inbound links)
- Stale-content checks
- Cross-reference minimum rule

They are still included in:
- Contradiction checks (a closed contradiction should still surface)
- Tag/frontmatter validation

### 8.8 Interactive vs automated mode

The Ingest workflows have user-confirmation gates designed for interactive use (typing in OpenCode, Claude Code, etc.). When the skill is invoked in **automated mode** — cron jobs, webhooks, batch scripts, headless pipelines — the gates that wait for human input must be skipped.

**Skip in automated mode:**
- IngestSingle step 2 (user discussion of takeaways)
- IngestBatch step 1 (batch confirmation)
- DeepQuery's "Suggest filing" prompt
- Delete workflow's per-link confirmation (use the default action: replace with plain text + "(deleted)")

**Always honor in automated mode (these gates protect data integrity):**
- The 10-page mass-update gate. If triggered, the operation must halt, write a `kind/log` entry to LOG.md noting the gate trigger and exit non-zero. A human must re-run the operation interactively.
- CreateWikiMap's directory-scan confirmation. Never run destructively without confirmation, even in automated mode. If automated mode encounters this, halt and log.
- The "existing wiki detected" halt in CreateWikiMap. Never auto-upgrade.

**Mode detection** is the assistant's responsibility, not the skill's. The skill only declares which gates can be skipped. Assistants may detect mode via:
- Interactive TTY check
- An `--automated` or `--non-interactive` flag from the caller
- Environment variable (e.g., `WIKI_MODE=automated`)
- Configuration

**When in doubt, default to interactive mode.** Skipping a gate that should have run is worse than blocking an automated job that needs adjustment.

---

## 9. Workflow Changes

### 9.1 CreateWikiMap (Ingest)

**Changes:**
- No SCHEMA.md generation. Schema lives in the meta-skill, not per wiki.
- **New step 0 — detect existing wiki:** Before scanning, check for an existing INDEX.md at the target path:
  - Empty dir → proceed normally
  - Has files but no INDEX.md → proceed normally (organize mode)
  - Has INDEX.md lacking v2 features (no `date_created`, no `sources:`, has `kind/relationship` tags) → **halt**, report "this looks like a v1 wiki, run UpgradeSchema instead"
  - Has INDEX.md with v2 features → **halt**, report "wiki already exists, nothing to do"
- Step 4 (frontmatter add) uses the v2 frontmatter template: `date_created` and `date_updated` both set to today; `topic/*` slot present but empty; no `kind/relationship`.
- INDEX.md template now includes a header block (see §11 SCHEMA skeleton and the updated INDEX format).

**Unchanged:**
- Body-content read-only rule
- Move-and-rename behavior
- LOG and INDEX creation (structure)
- Subdirectory preservation

### 9.2 IngestSingle (Ingest)

**Changes:**
- Step 1 prepended with **orientation protocol** (read SCHEMA, INDEX, last 30 LOG entries) when wiki already exists.
- Step 2 (user discussion) is now conditional on interactive mode — skipped in automated mode per §8.8.
- Step 4 references the new page-creation thresholds (≥2 sources or central) before creating any page.
- Step 4 enforces the ≥2 outbound wikilinks rule **only for content kinds** (see §8.2 exemptions).
- Step 4 sets `date_created` and `date_updated` on new pages; only bumps `date_updated` on existing pages.
- Step 4 populates the `sources:` frontmatter field on any new/updated page that derives from a webclip.
- New step 4.5: if the operation would touch ≥10 pages, halt and ask for confirmation (or halt-and-log in automated mode).
- Step on contradictions: when one is detected, write to **frontmatter** (`contradictions: [page]`) on both pages, in addition to the `## Contradictions` body section.
- URL handling tightened: if the source is a URL, the assistant fetches it with whatever capability is available (defuddle, WebFetch, manual save) and saves it as a webclip file before ingestion. The skill processes files, not URLs. If no fetch capability exists, ask the user to save locally and provide the path.

### 9.3 IngestBatch (Ingest) — full rewrite as atomic plan-then-write

**Motivation.** The old IngestBatch processed sources sequentially, fully completing each before starting the next. For 5 sources touching overlapping topics, this produced ~15 file writes, 5 INDEX updates, and 5 LOG entries. Cross-references between pages created in earlier iterations had to be retrofitted in later iterations. A crash mid-batch left the wiki in an inconsistent state.

The new IngestBatch is **atomic**: read everything, plan everything in memory, write once.

**New workflow structure:**

```
Phase 1 — Orientation
  1.1 Run the orientation protocol (SCHEMA.md + INDEX.md + last 30 LOG entries)
  1.2 Inventory the sources to be processed (no writes yet)
  1.3 Confirm scope with user (skipped in automated mode)

Phase 2 — Read all sources
  2.1 Read every source file
  2.2 Extract entities, concepts, claims, and relationships from each
  2.3 Build a unified "discovery map" in memory:
      - All entities mentioned (across all sources)
      - All concepts mentioned (across all sources)
      - All cross-source relationships

Phase 3 — Plan all writes
  3.1 ONE search pass: which entities/concepts already exist in the wiki?
  3.2 For each unique entity/concept, decide: CREATE new page OR UPDATE existing
  3.3 For each existing page that needs updates, compute the full merged update
      (not per-source — the final state after all sources are applied)
  3.4 Resolve all cross-references at planning time, including links between
      newly-created pages
  3.5 Resolve all `sources:` frontmatter entries at planning time
  3.6 Build the write plan:
      - List of pages to CREATE with full final content
      - List of pages to UPDATE with full final content
      - INDEX.md patch (one atomic update)
      - LOG.md entry (one atomic entry)

Phase 4 — Mass-update gate
  4.1 If total pages touched (CREATE + UPDATE) ≥ 10, halt and present the plan
  4.2 In interactive mode: ask for confirmation
  4.3 In automated mode: halt, log, exit non-zero

Phase 5 — Write once
  5.1 Write all CREATE pages
  5.2 Write all UPDATE pages
  5.3 Update INDEX.md once with all new entries
  5.4 Append ONE LOG entry:
      `- [[YYYY-MM-DD]] ingest | batch-{N-sources} | created: [page-a, page-b], updated: [page-c, page-d], sources: [src-1, src-2]`
  5.5 Report to user: list of all changes

Phase 6 — Failure handling
  6.1 If any write in Phase 5 fails, the batch is in an undefined state
  6.2 The LOG entry serves as the recovery marker: it lists what the operation
      intended to do
  6.3 Lint can detect post-crash inconsistency by cross-referencing the LOG
      entry against filesystem state
```

**Changes from old IngestBatch:**
- Removed per-source progress reporting (replaced with Phase 5 summary)
- Removed the cross-reference sweep at end (now resolved at planning time)
- Removed per-source LOG entries (now one entry)
- Removed per-source INDEX updates (now one update)
- Added explicit mass-update gate check in Phase 4
- Added explicit failure-handling notes

**What stays:**
- Orientation protocol prepended
- User confirmation in interactive mode (Phase 1.3)
- Automated-mode escape hatch (from §8.8)
- All the schema rules (wikilink minimums, tag axis order, etc.) still apply to each page in the plan

### 9.4 Delete (Ingest) — NEW workflow

**Purpose:** Safely remove a page from the wiki with full inbound-link cleanup.

**File:** `references/Ingest/workflows/Delete.md`

**When to use:**
- User says "delete", "remove", "get rid of" a specific page
- A page is superseded, wrong, off-topic, or duplicative
- Note: closure of completed work uses `status/close`, not deletion. Delete is for pages that shouldn't exist at all.

**Workflow structure:**

```
Step 1 — Orientation
  Run the orientation protocol (SCHEMA + INDEX + last 30 LOG entries)

Step 2 — Identify the target
  Confirm the page to delete (by name or by path).
  Refuse to delete:
    - INDEX.md
    - LOG.md (or rotated LOG-YYYY.md files)
    - Any page with kind/wiki or kind/log
  These require manual intervention.

Step 3 — Find inbound links
  Scan all wiki pages for [[target-page-name]]
  Build a list of inbound references with:
    - Source page
    - Line number / section
    - Link context (the surrounding sentence)

Step 4 — Present findings and proposed actions
  For each inbound link, present options:
    [a] Replace with plain text: "target-page-name (deleted)"
    [b] Redirect to another page: ask which
    [c] Remove the link entirely (delete the sentence/bullet if it becomes empty)
    [d] Leave broken (not recommended; lint will flag)

  Also ask the user:
    - Reason for deletion (recorded in LOG)
    - Confirm or cancel

  In automated mode, default to [a] "replace with plain text" and halt if
  the user would be asked anything else.

Step 5 — Apply
  5.1 Apply the chosen action to each inbound link
  5.2 Remove the page from INDEX.md
  5.3 Delete the page file using `trash` (not `rm`) when available,
      fallback to `rm` only if trash is unavailable
  5.4 Append LOG entry:
      `- [[YYYY-MM-DD]] delete | {page-name} | reason: {user-provided} | fixed inbound links in {N} pages: [list]`

Step 6 — Report
  - Page deleted
  - N inbound links fixed (with actions taken)
  - INDEX.md and LOG.md updated

## Guardrails

- **Never delete without inbound-link analysis.** Even if the user says "just delete it",
  run the scan and report what will break. The deletion still proceeds, but the user sees
  the impact.
- **Never delete webclips without extra confirmation.** Webclips are source snapshots.
  Deleting one means losing the provenance trail for any page that cites it in `sources:`.
  Require explicit "yes, delete the webclip and its provenance" confirmation.
- **Never batch-delete.** This workflow handles one page at a time. If the user asks to
  delete multiple pages, run the workflow multiple times with explicit confirmation each time.
- **`trash` over `rm`.** Use `trash` (from the user's global tools list) when available,
  so deletions are recoverable.
```

### 9.5 Search (Query)

**Changes:**
- Orientation protocol prepended.
- Search now also reads `references/_meta/topic-map.md` if it exists (for wikis past the 200-page threshold).

### 9.6 DeepQuery (Query)

**Changes:**
- Orientation protocol prepended.
- Contradictions section now reads from frontmatter `contradictions:` field directly, instead of grepping bodies.
- When synthesizing, the workflow reads `sources:` frontmatter to trace claims back to original webclips for stronger citations.
- The "Suggest filing" prompt is now conditional on the wiki-worthy judgment (see §9.7) — if the answer doesn't meet the threshold, don't suggest filing.

### 9.7 FileAnswer (Query)

**Changes:**
- New pages are created with `kind/query` (not `kind/research`) to preserve provenance.
- New pages satisfy the ≥2 outbound wikilinks rule by definition (they cite the pages they synthesized from) — but the rule is still enforced.
- New pages populate `sources:` frontmatter with the list of wiki pages the answer synthesized from.
- New pages set `date_created` and `date_updated` to today.
- **New step — wiki-worthy judgment:** before filing, assess whether the answer is substantive enough to preserve:
  - File when re-deriving the answer would require reading 3+ pages
  - File when the answer is a novel synthesis, comparison, or timeline
  - File when the user explicitly requests it
  - **Do not** file simple lookups answerable from a single page
  - **Do not** file answers that just restate existing wiki content
  If filing is declined, still offer to add a short cross-reference note to the most relevant existing page.
- New page count toward the ≥10-page confirmation gate (rare but possible if the answer cites many sources and triggers cross-reference updates).

### 9.8 FullSweep (Lint)

**New checks:**
- **LOG size** — flag if approaching 500 entries; recommend rotation.
- **INDEX section size** — flag if any section exceeds 50 entries; recommend sub-section split.
- **INDEX total size** — flag if exceeds 200 entries; recommend creating or regenerating `_meta/topic-map.md`.
- **Outbound wikilink minimum** — apply per the exemption list in §8.2: warnings for content kinds, info for operational kinds, no check for exempt kinds. Always exclude closed pages.
- **Page size** — flag pages over 200 lines (info-level; recommend split).
- **Frontmatter `contradictions:` field** — surface unresolved contradictions across the wiki (critical).
- **Frontmatter `sources:` field** — verify every listed source page exists; flag broken provenance (critical). Also flag any content-kind page (`kind/research`, `kind/doc`, `kind/query`) with no `sources:` field at all (warning).
- **Orphan webclips** — flag `kind/webclip` pages that no other page cites in their `sources:` field (warning; webclips that were ingested but produced no synthesis).
- **`topic/*` tag validation** against the SCHEMA.md enum.
- **Tag axis order** — must be `area → kind → topic → status → pty`. Missing axes are allowed (topic and pty are optional); out-of-order axes are errors. This update matters now that `topic/*` is inserted between kind and status.
- **`date_created` validation** — must be present on every page (was required in v2), must not be in the future, must be ≤ `date_updated`.
- **Closed-page exclusion** — `status/close` pages are excluded from orphan, stale, and wikilink-minimum checks; still included in contradiction and frontmatter validation.
- **Post-crash batch inconsistency** — cross-reference LOG.md batch entries against filesystem state. If a batch LOG entry lists pages that don't exist on disk, or if pages exist that aren't in INDEX.md, flag as critical.
- **LOG rotation sanity** — if `LOG.md` exists alongside `LOG-YYYY.md` files, verify no date-range overlap.

**Severity ordering in reports** (within each severity tier, order issues as):
1. Broken wikilinks
2. Broken `sources:` provenance
3. Contradictions
4. Orphan pages / orphan webclips
5. Missing pages (red links)
6. Stale content
7. Missing cross-references
8. Tag issues
9. Thin/long pages

**Removed:**
- "3x average updated date" staleness rule (was fragile). Replaced by **absolute threshold: pages with `date_updated` more than 180 days old** AND `status/open` or `status/stable`.

### 9.9 QuickCheck (Lint)

**Changes:**
- Add new check types matching the new FullSweep checks.
- New request mappings:
  - "log size", "rotate log" → log size check
  - "index size", "huge index" → INDEX scaling checks
  - "thin links", "underlinked", "few links" → outbound wikilink minimum
  - "big pages", "long pages", "split" → page size check
  - "topic tags" → topic/* validation
  - "provenance", "sources", "orphan webclips" → sources-field validation + orphan-webclip check
  - "axis order", "tag order" → tag axis order check
  - "inconsistent batch", "recovery" → post-crash batch inconsistency check

---

## 10. Skill File Structure (After Refactor)

```
wiki-map/
├── SKILL.md                          # ~150 lines (down from 245)
└── references/
    ├── ROUTER.md                     # KEPT — routing dispatch
    ├── SCHEMA.md                     # NEW — global schema, single source of truth
    │                                 #   (includes §9 Session Orientation Protocol;
    │                                 #    no separate ORIENTATION.md file)
    ├── Ingest/
    │   ├── SKILL.md                  # ~100 lines (drops duplicated schema)
    │   └── workflows/
    │       ├── CreateWikiMap.md      # +existing-wiki detection, v2 frontmatter
    │       ├── IngestSingle.md       # +orientation, +thresholds, +sources field, +mode
    │       ├── IngestBatch.md        # FULL REWRITE — atomic plan-then-write
    │       ├── Delete.md             # NEW — safe delete with inbound-link cleanup
    │       └── UpgradeSchema.md      # NEW — v1 → v2 migration
    ├── Query/
    │   ├── SKILL.md                  # ~70 lines
    │   └── workflows/
    │       ├── Search.md             # +orientation, +topic-map.md fallback
    │       ├── DeepQuery.md          # +orientation, +frontmatter contradictions, +sources
    │       └── FileAnswer.md         # +wiki-worthy judgment, +kind/query
    └── Lint/
        ├── SKILL.md                  # ~80 lines (+severity ordering)
        └── workflows/
            ├── FullSweep.md          # +11 new checks, -3x avg rule
            └── QuickCheck.md         # +8 new check mappings
```

**File count change:** 13 files → 15 files (+Delete, +UpgradeSchema, +SCHEMA.md; -ORIENTATION.md).

### 10.1 Routing — keep both surfaces (D19)

**Decision:** Keep both `references/ROUTER.md` and the parent `SKILL.md` "Invocation Scenarios" routing table. This is intentional for a meta-skill that will accumulate more sub-skills over time.

- **Parent SKILL routing table** = human-readable scenarios with example trigger phrases
- **ROUTER.md** = dispatch logic loaded by the assistant at routing time

When new sub-skills are added later, both surfaces get updated together. The duplication is the price of having a meta-skill entry point that's also human-browsable.

### 10.2 Schema duplication resolution (D17, D18)

**The full schema lives in `references/SCHEMA.md` at the meta-skill level.** This is where any sub-skill (current or future) reads the canonical conventions.

**Move into `references/SCHEMA.md`:**
- Wiki architecture diagram
- Frontmatter schema
- Tag axis order and full enums (area, kind, topic, status, pty)
- Page template
- INDEX.md format
- LOG.md format
- Naming convention
- All hard rules from §8

**Remove from `wiki-map/SKILL.md`:** all of the above. Replace with a one-line pointer: *"For the full schema, see `references/SCHEMA.md`."* The parent SKILL becomes a philosophy/problem/solution document; SCHEMA.md becomes the rules document.

**Remove from `Ingest/SKILL.md`:** wiki structure reference, page template, INDEX format, LOG format, tag reference, naming convention. Replace with: *"For the full schema, see `../SCHEMA.md`."*

**Net effect:** schema lives in exactly one place at the meta-skill root. Sub-skills and workflows reference it. When a new sub-skill is added later, it points at the same SCHEMA.md and inherits all conventions for free.

---

## 11. New `references/SCHEMA.md` Skeleton

```markdown
# Wiki Schema (Global)

> The single source of truth for wiki conventions. All sub-SKILLs and
> workflows reference this file. Per-wiki overrides live in each wiki's
> own SCHEMA.md.

## Wiki Architecture

{wiki-name}/
  INDEX.md            # Page catalog (kind/wiki)
  references/
    LOG.md            # Append-only operational log
    {page}.md         # Wiki pages
    {subdir}/         # User-managed subdirectories preserved as-is
    _meta/
      topic-map.md    # Generated by lint when INDEX exceeds 200 entries
  assets/             # Optional, for non-markdown files

Note: there is no per-wiki SCHEMA.md. The full schema lives in the
meta-skill at `wiki-map/references/SCHEMA.md`.

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
- ≥2 outbound wikilinks per content-kind page, with exemption list (§8.2)
- 200-line page split threshold (§8.3)
- 50/200 INDEX scaling (§8.4)
- 500-entry LOG rotation (§8.5)
- 10-page mass-update confirmation (§8.6)
- Closed-page handling (§8.7)
- Interactive vs automated mode gates (§8.8)

## Session Orientation Protocol
(Formerly planned as a separate ORIENTATION.md file — now lives here as §9 of SCHEMA.md.)

Before any operation on an existing wiki, perform these reads:

1. Read this `references/SCHEMA.md` — canonical conventions, tag enums, hard rules
2. Read `{wiki}/INDEX.md` — current page catalog and header stats
3. Read last 30 entries of `{wiki}/references/LOG.md` — recent activity
4. For wikis with 100+ pages, search the wiki for the current request topic
   before creating any new page

### Skip orientation when:
- Initializing a brand new wiki (no INDEX/LOG yet — but SCHEMA is still read)
- The current request is pure routing (no file I/O)

### Subdirectory drift detection:
If the directory structure has changed since the last LOG entry, note it in the
orientation summary but do not attempt to normalize or "fix" the structure.
Ask the user if the change should be reflected in INDEX.md.

### Orientation output:
After orientation, emit a one-line summary:
`Oriented: {wiki-name} | {N} pages | {M} recent log entries | {drift status}`
```

---

## 12. INDEX.md header block (NEW)

Every v2 INDEX.md starts with a header block before the table. This is a cheap orientation aid and self-documenting instruction.

```markdown
---
name: {Wiki Name}
description: {One-line description}
tags:
  - area/ea
  - kind/wiki
date_created: YYYY-MM-DD
date_updated: YYYY-MM-DD
---

# {Wiki Name}

> Content catalog. Every wiki page is listed here with a one-line summary.
> Read this first to find relevant pages for any query.
> **Total pages:** N | **Last updated:** YYYY-MM-DD

## Wiki Map

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |
| `references/{page}.md` | {description from frontmatter} |
```

**Scaling rules (from §8.4) apply to the table section:**
- When any `kind/*` section exceeds 50 entries, split into sub-sections
- When total exceeds 200 entries, generate `references/_meta/topic-map.md` grouped by `topic/*`

The **header blockquote** line ("Read this first...") is literal — it appears in every INDEX.md as self-documentation for any LLM that loads the file without the skill context.

The **stats line** ("Total pages: N | Last updated: YYYY-MM-DD") is maintained by whichever workflow last touched INDEX.md.

---

## 13. Migration Plan for Existing Wikis

When this v2 lands, existing wikis built with v1 need a one-time upgrade. Add a new workflow:

### 13.1 New workflow: `Ingest/workflows/UpgradeSchema.md`

**Purpose:** Upgrade an existing v1 wiki to v2 conventions.

**Detection (idempotent):** a v1 wiki is one that exhibits **any** of these markers:
- Presence of `kind/relationship` tags anywhere
- Absence of `date_created` frontmatter on any page
- Absence of `sources:` frontmatter on any content-kind page
- INDEX.md without the v2 header block (no blockquote line, no stats line)

Running UpgradeSchema twice is a no-op: the second run finds no markers and reports "already at v2".

**Steps:**

1. **Detect** — scan the wiki for v1 markers. Report which markers are present.

2. **Report** (no writes yet) — list all issues found:
   - Pages with `kind/relationship` → will be rewritten to `topic/relationship`
   - Pages missing `date_created` → will be set to `date_updated` value (best-effort backfill)
   - Pages missing `sources:` → cannot auto-infer; list for manual review
   - INDEX.md needing header block → will be prepended with v2 header
   - Pages with <2 outbound wikilinks (content kinds only) → report, do not auto-fix
   - Pages over 200 lines → report, do not auto-split
   - INDEX section sizes (flag any >50)
   - LOG size (flag if approaching 500)
   - Pages without `status/*` tag → will assign `status/open` after confirmation

3. **Confirm** — user confirms the auto-fixes (non-auto items are advisory).

4. **Apply auto-fixes** (in interactive mode with confirmation; in automated mode this whole workflow halts before writing — upgrades are never automated):
   - Rewrite `kind/relationship` → `topic/relationship` (tag-only edit; bodies untouched)
   - Backfill `date_created` from `date_updated` where missing
   - Prepend v2 header block to INDEX.md (preserve existing table)
   - Assign `status/open` to pages missing a status tag

5. **Never auto-do:**
   - Add `sources:` to existing pages (requires content judgment)
   - Add `topic/*` tags beyond the relationship migration
   - Fix wikilink-minimum violations (requires content judgment)
   - Split long pages

6. **Log** — append to LOG.md:
   `- [[YYYY-MM-DD]] upgrade | wiki | Schema upgraded to v2: {N} kind→topic rewrites, {N} date_created backfills, INDEX header added`

**Triggers:** "upgrade wiki", "upgrade schema", "migrate wiki to v2"

---

## 14. Resolved Decisions (was Open Questions)

### From first review round
1. ✅ Tag axis order: `area → kind → topic → status → pty`
2. ✅ Closed pages stay in INDEX.md; **user manages closed entries manually, AI does not touch them**
3. ✅ `area/*` stays hardcoded as `area/ea` (personal use)
4. ✅ Webclips: user manages source layout. If they want a `references/sources/` subdirectory, they create it; the skill respects whatever exists.
5. ✅ `kind/relationship` removed; use `topic/relationship` instead
6. ✅ Stale threshold: 180 days, global default
7. ✅ Keep both ROUTER.md and the parent SKILL routing table (meta-skill will grow more sub-skills)
8. ✅ `_meta/topic-map.md` generated by lint when INDEX exceeds 200 entries; regenerated on threshold breach. **Once generated, the user may edit it; the AI must not overwrite user edits without confirmation.**

### From second review round
9. ✅ **A1: `sources: [page-name]` frontmatter field** — adopted for traceability
10. ✅ **A2: `date_created` alongside `date_updated`** — adopted
11. ✅ **B1: `kind/query`** — adopted for filed query answers
12. ✅ **A4: IngestBatch atomic rewrite** (read all → plan all → write once) — adopted
13. ✅ **B8: scoped topic tags** — **REJECTED as overkill**; keep `topic/{name}` flat with project exception
14. ✅ **D2: drop ORIENTATION.md** — orientation becomes §9 of SCHEMA.md
15. ✅ **C4: Delete workflow** — adopted; added as `Ingest/workflows/Delete.md`
16. ✅ **A6: automated-mode escape hatches** — adopted as §8.8
17. ✅ **D3: wikilink minimum exemption list** — see §8.2
18. ✅ **B7: CreateWikiMap detects existing wikis and halts** — adopted
19. ✅ **A3: INDEX.md header block** — adopted; see §12
20. ✅ **A5: FileAnswer wiki-worthy judgment** — adopted; see §9.7
21. ✅ **A7: severity ordering convention in lint reports** — adopted; see §9.8
22. ✅ **B2: URL handoff language tightened** in IngestSingle — adopted

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

Each commit should be independently revertable. Commits 1 and 2 are zero-risk refactors. Commits 3-11 are the substantive behavior changes.

### Phase A — Foundation (zero-risk refactors)

1. **Commit 1 — extract SCHEMA.md:** create `references/SCHEMA.md` with the full skeleton from §11 (including §9 orientation section). Remove duplicated schema content from parent SKILL and Ingest SKILL. No behavior change.
2. **Commit 2 — slim parent SKILL:** move remaining schema references into SCHEMA.md pointers. Keep both routing surfaces (ROUTER.md + parent table).

### Phase B — Frontmatter v2 (new fields)

3. **Commit 3 — tag taxonomy v2:** add `topic/*` axis to SCHEMA.md, remove `kind/relationship`, add `kind/query`. Update frontmatter template.
4. **Commit 4 — date_created and sources:** add `date_created` and `sources:` fields to SCHEMA.md frontmatter. Update workflows to populate them on create/update.
5. **Commit 5 — contradictions frontmatter:** update IngestSingle, DeepQuery, FullSweep to read/write `contradictions:` field.

### Phase C — Hard rules and behavior changes

6. **Commit 6 — hard rules:** add §8 rules to SCHEMA.md (≥2 wikilinks with exemption list, 200-line split, 50/200 INDEX scaling, 500-entry LOG rotation, 10-page mass-update gate, closed-page handling, interactive vs automated mode). Update workflows to enforce them.
7. **Commit 7 — orientation prepend:** prepend orientation protocol to every sub-SKILL and workflow. Behavior change in all operations on existing wikis.
8. **Commit 8 — CreateWikiMap v2:** add existing-wiki detection, INDEX.md header block, `date_created` population, `topic/*` slot in templates.

### Phase D — New workflows

9. **Commit 9 — IngestBatch atomic rewrite:** full rewrite per §9.3 (read all → plan all → write once). Single LOG entry per batch. This is the highest-complexity commit.
10. **Commit 10 — Delete workflow:** new `Ingest/workflows/Delete.md` per §9.4. Safe-delete with inbound-link cleanup.
11. **Commit 11 — FileAnswer v2:** add wiki-worthy judgment, `kind/query` creation, `sources:` population.

### Phase E — Lint and migration

12. **Commit 12 — lint v2:** add 11 new checks to FullSweep per §9.8, add QuickCheck mappings per §9.9, replace 3x-average staleness rule with 180-day absolute threshold.
13. **Commit 13 — UpgradeSchema workflow:** add `Ingest/workflows/UpgradeSchema.md` per §13. Idempotent v1 → v2 migration.

### Phase F — Validation

14. **Commit 14 — validation:** run round-trip test per §15 on a fixture wiki. Fix any issues found. Update the skill's own INDEX/LOG examples in SCHEMA.md if reality diverged from templates.

---

## 17. What Stays the Same

For the record, this refactor explicitly preserves:

- Router + sub-SKILL architecture
- **Both routing surfaces** (ROUTER.md AND parent SKILL routing table) — meta-skill will grow more sub-skills
- CreateWikiMap read-only-on-bodies guardrail
- Subdirectory preservation rule (never flatten, never reorganize)
- Organize-vs-process hard separation
- Concrete report templates with realistic numbers
- Four-axis tag model (now five with `topic/*`)
- Status enum (`status/close` instead of archive); user-managed closed entries in INDEX
- `area/ea` hardcoding (personal wiki use)
- All existing kinds **except `kind/relationship`** (now `topic/relationship`), **plus `kind/query`** (new)
- Append-only LOG model (now with rotation)
- INDEX.md as the navigational entry point (now with header block and scaling rules)
- Tool-portability — no hardcoded `web_extract`, `read_file`, `search_files` references
- **No per-wiki SCHEMA.md** — full schema lives at the meta-skill level only
- Flat `topic/{name}` tags (no scoped `topic/{wiki}/{name}`) — rejected as overkill

---

## 18. Summary

This plan adopts twelve high-leverage ideas from Hermes' `llm-wiki` (orientation protocol, page-creation thresholds, wikilink minimum, INDEX scaling, log rotation, mass-update gate, frontmatter contradictions, page split threshold, `sources` provenance, `date_created`, atomic bulk-ingest, INDEX header block) while rejecting the structural choices that conflict with `wiki-map`'s identity (`raw/` separation, type-based hierarchy, archive directory, per-wiki schema files, hardcoded tool calls, integration ecosystem). It introduces two genuinely new elements — the `topic/*` tag axis and the `kind/query` work type — and removes one redundant kind (`kind/relationship`). It adds two new workflows: `Delete` for safe page removal and `UpgradeSchema` for v1→v2 migration.

The result is a tighter, more checkable, more session-resilient version of the existing skill — without losing the properties that make it good at organizing existing messy notes.

The three biggest behavioral changes:
1. **Orientation protocol** — every operation in an existing wiki now begins by re-reading the wiki's own conventions, preventing the silent drift that destroys long-lived knowledge bases.
2. **Atomic IngestBatch** — batch ingestion becomes read-all → plan-all → write-once, eliminating redundant updates, partial-failure inconsistency, and LOG noise.
3. **Provenance via `sources:` frontmatter** — every synthesized page declares which webclip(s) it derived from, making the wiki traceable and enabling lint checks for orphan webclips and broken provenance.

The biggest structural change is **schema deduplication**: pulling the schema into `references/SCHEMA.md` (with orientation as §9 rather than a separate ORIENTATION.md file) so conventions live in exactly one place. Every other improvement compounds off that foundation.

**New capabilities (not in v1):**
- Safe deletion with inbound-link cleanup (`Delete.md`)
- v1→v2 migration path (`UpgradeSchema.md`)
- Headless/automated-mode support for future cron/webhook usage
- Machine-queryable contradictions in frontmatter
- Filed query answers distinct from ingested-source synthesis (`kind/query`)
- INDEX.md self-documentation via header block

**New lint coverage (14 checks added or enhanced):**
LOG size, INDEX scaling, wikilink minimum with exemptions, page size, `sources:` integrity, orphan webclips, `contradictions:` field, `topic/*` validation, tag axis order, `date_created` validation, closed-page exclusion, post-crash batch inconsistency, LOG rotation sanity, severity ordering.
