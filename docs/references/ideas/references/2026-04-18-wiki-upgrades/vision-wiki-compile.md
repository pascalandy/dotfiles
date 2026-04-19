---
name: vision-wiki-compile
description: Add a Compile sub-skill to wiki-map that answers "is the wiki complete?" by mining existing pages for missing concept entities, then creating pages and back-edits under user approval.
tags:
  - area/ea
  - kind/doc
  - topic/strategy
  - status/draft
date_created: 2026-04-19
date_updated: 2026-04-19
sources:
  - idea-personal-knowledge-compilation
---

# Vision — Compile Sub-Skill for wiki-map

Mode: `AlignmentDraft`. Direction is settled; this artifact makes the target state explicit before architecting the workflow.

## Request

Extend `dot_config/ai_templates/skills/knowledge/wiki-map` with a new `Compile` sub-skill that answers "is the wiki complete?" — a distinct mental model from Lint's "is the wiki healthy?". Compile mines existing wiki pages for missing concept entities, ranks them, and writes new pages plus back-edits under an explicit approval gate.

## Current State

`wiki-map` exposes three sub-skills — Ingest, Query, Lint — with 11 workflows total. The closest neighbour to the proposed Compile is Lint, but the two differ fundamentally.

What Lint covers today:

- `FullSweep` reports drift across 7 check categories, including "pages over 200 lines", "thin pages", "missing pages implied by repeated references", "orphan pages", "missing cross-references"
- Write surface is capped at "INDEX drift, safe tag corrections, missing cross-references"
- Contradictions, provenance, and stale-content decisions are explicitly deferred to "explicit review"
- Single-agent, read-model, reporting-first

What the wiki cannot do today:

- Promote high-reference entities (2+ source rule already in `SCHEMA.md`) into first-class pages
- Extract concept candidates via parallel subagent fan-out across existing pages
- Flag bare directories as expansion candidates (FullSweep explicitly leaves plain subdirs alone)
- Rank implied-missing entities by reference count to drive a planning pass
- Create net-new pages from the wiki's own content and back-edit siblings with wikilinks

Compile is the name for the gap.

There is also a second naming collision to fix. The bare trigger `wiki-map update` currently routes to `RecursiveUpdate` (Lint), which only rebuilds INDEX routes. That meaning is too narrow for "update," and it blocks Compile from claiming its natural triggers.

## Desired End State

A fourth sub-skill sits alongside Ingest, Query, Lint. It owns the completeness pass. It reuses Lint output as input rather than duplicating scans. It never ingests external sources and never rebuilds INDEX routes.

```text
dot_config/ai_templates/skills/knowledge/wiki-map/
  SKILL.md
  references/
    ROUTER.md
    SCHEMA.md
    Ingest/
    Query/
    Lint/
    Compile/                       # NEW
      MetaSkill.md
      workflows/
        CompileWiki.md              # single atomic workflow, 6 phases
```

`CompileWiki.md` follows the 6-phase orchestration shape already used by `IngestBatch`:

| # | Phase | Output |
|---|---|---|
| 1 | Orientation | SCHEMA, INDEX, last 30 LOG entries, subdir drift check |
| 2 | Lint Gate | Recent `lint | full sweep` or `lint | quick check` in LOG, or halt with "run health check first" |
| 3 | Survey | Lint findings (bloated, thin, implied-missing, orphans) plus bare directories and per-entity ref counts |
| 4 | Mining | Parallel subagents, ~10 pages each, concrete-noun test, per-entity `{source_pages[], ref_count}` |
| 5 | Planning + Approval Gate | Deduped ranked candidate table, halt at Mass-Update threshold (10+ pages) |
| 6 | Creation | Write new pages, back-edit siblings with wikilinks, one INDEX patch, one LOG entry, failure recovery via log marker |

## Key Decisions

| Decision | Choice | Reasoning |
|---|---|---|
| Name | `Compile` | Matches "is the wiki complete?" and "Personal Knowledge Compilation" framing; `Breakdown` reads as destructive |
| Sub-skill vs workflow-under-Lint | New sub-skill | Compile is write-heavy and parallel; Lint is read-only, single-agent, reporting-first — mixing them violates Lint's "report before fixing" principle |
| Phase count | 6, not 4 | The original idea listed 4 novel phases; two orchestration phases (Orient, Gate) are already the convention in `IngestBatch` and every Lint workflow |
| Workflow file count | 1 atomic `CompileWiki.md` | Matches `IngestBatch` precedent; forces atomic thinking; survey-only can be added later as `Survey.md` if needed |
| Lint coupling | Require prior Lint report | User decision. Compile does not re-scan. Phase 2 halts if no recent Lint entry in LOG |
| Trigger for `wiki-map update` | Strip from `RecursiveUpdate`, treat as ambiguous and ask the user | "Update" today silently means "rebuild INDEX routes" — too narrow and blocks Compile |
| Subagent portability | Abstract pattern in MetaSkill.md, `delegate-to-sub` referenced as optional harness-specific dispatcher | wiki-map is harness-agnostic by design |
| Schema changes | None | The 2+ sources rule and Mass-Update 10-page gate already exist in `SCHEMA.md` |
| Ontology coupling | Deferred | Per user instruction; shared mining phase extraction is a later refactor when Ontology lands |
| Boundary with Ingest | Compile writes from wiki itself, Ingest writes from external sources | Stated in MetaSkill.md as hard rule |
| Boundary with Refresh (RecursiveUpdate) | Compile never rebuilds INDEX routes | Stated in MetaSkill.md as hard rule |

## Success Signals

- A wiki with 50+ pages and at least one `lint | full sweep` LOG entry can run Compile end-to-end and produce a ranked candidate table.
- Phase 2 halts cleanly when no recent Lint report exists and instructs the user to run health check first.
- Phase 5 halts at the 10-page Mass-Update threshold and shows the candidate table; user approves or revises before any write.
- Phase 6 produces one write pass, one INDEX patch, one LOG entry — no per-page loops.
- Mining phase completes with parallel subagent fan-out when the harness supports it and degrades to sequential when it does not, without changing the output shape.
- Router disambiguation for `wiki-map update` surfaces three options (Lint, Refresh, Compile) rather than silently running RecursiveUpdate.
- A new reader lands in `CompileWiki.md` and recognizes the 6-phase shape from `IngestBatch` immediately.

## Risks and Review Points

| Risk | Mitigation |
|---|---|
| Compile duplicates FullSweep's scanning | Phase 2 Lint Gate is a hard requirement; Phase 3 consumes Lint output rather than re-walking the tree |
| Mining cost explodes on large wikis | Subagent batches capped at ~10 pages each; prioritize bloated pages (>200 lines) as quarries first |
| Concrete-noun test produces garbage candidates | SCHEMA's "2+ sources or central subject" rule filters Phase 5; low-ref entities drop out of the approval table |
| User bypasses Lint Gate and runs Compile blind | Phase 2 halts with explicit instruction; no silent fallback |
| Router change breaks existing `wiki-map update` muscle memory | Disambiguation row asks the user once per ambiguous invocation; documented in SKILL.md Invocation Scenarios |
| Harness lacks parallel subagent support | Mining described abstractly; reference to `delegate-to-sub` optional; sequential fallback preserves the output shape |
| Sub-skill root violates meta-skill-creator's "references/ nesting" rule | Follow existing wiki-map convention (workflows as sibling of MetaSkill.md) for consistency; note as repo-wide refactor for a separate pass |
| Failure mid-Phase-6 leaves wiki in undefined state | LOG entry written first as recovery marker, matching `IngestBatch` Phase 6 pattern |

## Success Is Not

- A standalone generic "create missing pages" tool. Compile is tightly coupled to wiki-map's schema, LOG, INDEX, and Lint.
- A replacement for Ingest. External sources never enter Compile.
- A replacement for Lint. Health reporting stays with Lint.
- A full rewrite of Lint's overlapping checks. Compile imports Lint output; it does not re-implement it.

## Recommended Next Phase

`pa-architect` on `CompileWiki.md` — design the 6-phase internal logic in detail, specify the subagent batch contract, spell out the Phase 5 candidate table format, lock in the Phase 6 write-order, and enumerate the precise Router/SKILL.md/MetaSkill.md edits.

## Related

- [[idea-personal-knowledge-compilation]]
