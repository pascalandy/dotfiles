# Napkin Atlas Bootstrap Guide

Complete phase-by-phase guide for creating a project reference map from scratch.
Read this guide fully before starting. Execute phases in order.

The `.napkin/` directory is a curated **project map for AI agents** — not a
note-taking system. Each markdown file is a map entry that describes a specific
aspect of the project (structure, procedure, context, or current state).
Napkin's TF-IDF and BM25 engines generate the navigable index automatically from
these entries, so the quality of your headings, filenames, and wikilinks directly
determines how well agents can find and use the map.

---

## Phase 0 — Discovery

Before writing a single map entry, understand the project deeply. Answer these
questions:

### Identity
- What is this project? What does it do?
- Who is it for? Who works on it?
- What is the domain? What vocabulary does it use?

### Topology
- What are the major areas/sections/components?
- How are files and directories organized?
- What are the boundaries between areas?
- What depends on what?

### Conventions
- What patterns are followed consistently?
- What tools are used? What's the workflow?
- What naming conventions exist?
- What rules (explicit or implicit) govern the project?

### State
- What is actively being worked on?
- What is broken, incomplete, or blocked?
- What was recently changed? What is planned next?

### Fragility
- What breaks easily?
- What do people get wrong repeatedly?
- Where are the undocumented gotchas?

### Discovery strategies by project type

**Software project**: Read config files (package.json, pyproject.toml, Cargo.toml,
Makefile, docker-compose.yml), entry points, directory layout, test structure,
CI/CD pipelines, existing docs. Run the project if possible.

**Product/business**: Read product docs, roadmaps, org charts, process docs,
meeting notes, strategy docs, customer-facing materials, internal wikis.

**Research project**: Read papers, experiment logs, data descriptions, methodology
docs, literature reviews, hypothesis records, analysis scripts.

**Infrastructure/ops**: Read runbooks, architecture diagrams, monitoring configs,
incident reports, deployment procedures, service catalogs.

**Personal knowledge base**: Read existing notes, folder structure, tag usage,
link patterns, daily notes, recurring themes.

**Mixed/unknown**: Start with top-level files and directory listing. Classify
each major area, then apply the appropriate strategy per area.

---

## Phase 1 — Write NAPKIN.md

The single most important file. Loads into every agent session as L0 context.
Every word must earn its place.

**Constraints:**
- Under 250 tokens
- No filler, no boilerplate, no placeholder text
- Only facts that an agent needs in EVERY interaction
- If something only matters sometimes, put it in a deeper map entry

### Template

```markdown
# [Project Name]

## What is this
[1-3 sentences. Precise. What it does, who it's for, what domain.]

## Structure
[The major areas and what lives in each. A mental model of the topology.]

## Key conventions
- [Things that are always true and non-obvious]
- [Rules that agents violate without explicit reminders]

## Current state
- [What's actively happening or blocked]
- [Or "Stable — no active changes" if nothing]

## Atlas guide
- `napkin overview` — map of this atlas with keywords
- `napkin search "<topic>"` — find specific knowledge
- `napkin read "<entry>"` — read a full map entry
```

**Why each section exists:**
- "What is this" — prevents the agent from misunderstanding project scope
- "Structure" — gives the agent a mental model before reading any code
- "Key conventions" — prevents the most common agent mistakes
- "Current state" — orients the agent to what matters now
- "Atlas guide" — teaches the agent how to navigate deeper into the map

---

## Phase 2 — Structure Entries

Create entries in `structure/` that map the project topology. One entry per
major boundary. The filename IS the index entry.

**Scale guide:**
- Small project (< 10 files/components): 1-2 entries
- Medium project (10-50): 3-5 entries
- Large project (50+): 5-10 entries

### Good filenames

- `Frontend Architecture.md`
- `Database Schema.md`
- `API Surface.md`
- `Repository Layout.md`
- `Data Pipeline.md`
- `Infrastructure Topology.md`

### Template

```markdown
---
date: "YYYY-MM-DD"
tags:
  - structure
---
# [Area/Component/Boundary Name]

## What this is
[What does this area contain? What is its purpose?]

## What lives here
[List the key contents — files, modules, processes, teams.]

## Boundaries
[What this area owns vs. what it does NOT own. Where it interfaces
with other areas.]

## Dependencies
[What this depends on. What depends on this.]

## Key details
[Anything non-obvious. Hidden complexity, performance characteristics, gotchas.]

## Related
- [[Other Structure Entry]]
- [[Relevant Guide]]
```

**Use specific language in headings and body.** The TF-IDF engine extracts keywords
from your text. Headings are weighted 3x, filenames 2x, body text 1x.
"Authentication and Session Management" produces useful keywords.
"Component Overview" does not.

---

## Phase 3 — Decisions (not tracked)

Napkin templates may scaffold a `decisions/` directory. **Do not populate it.**
This atlas does not track decisions — they drift too easily and create false
confidence in outdated reasoning.

If the `decisions/` folder was created by `napkin init`, leave it empty or add
a single `_about.md` containing:

```markdown
Decisions are not tracked in this atlas.
```

Do not create decision records during creation or updates.

---

## Phase 4 — Guides

Create entries in `guides/` for recurring procedures that aren't obvious.
One entry per procedure. Filename = what you're trying to do.

### Good filenames

- `Setting up the dev environment.md`
- `Deploying to production.md`
- `Adding a new API endpoint.md`
- `Running the test suite.md`
- `Recovering from a failed migration.md`
- `Debugging payment failures.md`

### Template

```markdown
---
date: "YYYY-MM-DD"
tags:
  - guide
---
# [What You're Trying To Do]

## Prerequisites
- [What must be true before starting]

## Steps
1. [Step 1 — be specific, not vague]
2. [Step 2]
3. [Step 3]

## Common problems
- **[Problem]** — [Cause and fix]
- **[Problem]** — [Cause and fix]

## Related
- [[Relevant Structure Entry]]
- [[Relevant Guide]]
```

**What deserves a guide:**
- Anything someone asked how to do more than once
- Procedures with non-obvious steps or gotchas
- Recovery procedures for known failure modes
- Onboarding steps that can't be automated

---

## Phase 5 — Context Entries

Create entries in `context/` for knowledge that doesn't fit structure or
guides — but that an agent needs to work effectively. This is institutional
knowledge: things that live in people's heads and chat history.

### Examples

- `Third-party API quirks.md`
- `Performance bottlenecks.md`
- `Customer segments.md`
- `Historical incidents.md`
- `Known technical debt.md`
- `Glossary.md`

No rigid template. Freeform entries with good headings, tags, and wikilinks.
Every context entry must have frontmatter with `date` and `tags`.

---

## Phase 6 — Active State

Create entries in `active/` for the current state of work. These are the most
volatile entries — they change frequently.

### Examples

- `Current sprint.md`
- `Open questions.md`
- `Blocked items.md`
- `Recent changes.md`

Update at the end of every significant work session. Move stale active entries
to `context/` or delete them.

---

## Phase 7 — Wiring (Wikilinks + Tags)

After writing all entries, go back and add connections.

### Wikilinks

Every entry should link to at least one other entry using `[[Entry Name]]` syntax.

**Link patterns:**
- Structure entries -> related guide entries
- Guides -> structure entries they operate on
- Context entries -> structure and guides they relate to
- Active entries -> everything they touch

The search engine boosts results by backlink count. An entry with 5 inbound links
ranks higher than an orphan with the same text match. Wikilinks are ranking signals,
not decoration.

### Tags

Use a small, consistent vocabulary. Keep total under 15 tags.

**Base tags:**
- `#structure` — topology and map entries
- `#guide` — how-to procedures
- `#context` — institutional knowledge
- `#active` — current work state

Add domain-specific tags as needed.

---

## Phase 8 — Verification

### Test L1 (overview)

Run `napkin overview`. Check:
- [ ] NAPKIN.md content appears at the top
- [ ] Each folder shows distinct, meaningful keywords
- [ ] Keywords are specific to the folder (not generic words)
- [ ] The overview gives a clear picture of what knowledge exists where

If keywords are weak, rewrite headings and content with more specific language.

### Test L2 (search)

Run `napkin search` for 5 different queries an agent might ask:
- [ ] Architecture query -> finds structure entries
- [ ] "How to" query -> finds guide entries
- [ ] Current state query -> finds active entries
- [ ] Domain-specific query -> finds the right context entry

If results are poor, check filenames, headings, body text specificity,
and wikilink density.

### Test L3 (read)

Read each entry. Check:
- [ ] No placeholder text ("TBD", "fill in later", empty sections)
- [ ] Every entry has frontmatter with `date` and `tags`
- [ ] Every entry has at least one `[[wikilink]]` to another entry
- [ ] Entries are concise — no entry over 200 lines unless justified

### Wiring check

```bash
napkin link orphans      # Should return empty or near-empty
napkin link deadends     # Should return empty or near-empty
napkin link unresolved   # Must return empty (no broken links)
```

### AGENTS.md check

Verify the project's `AGENTS.md` starts with:

```markdown
## Project overview using progressive disclosure

1. Read and understand: `.napkin/NAPKIN.md`
2. run `napkin overview --json`
```

If missing, add it. If `AGENTS.md` does not exist, create it with this content.

---

## Phase 9 — Maintenance Protocol

| Event | Action |
|-------|--------|
| Architecture changes | Update or create `structure/` entry |
| Someone asks "how do I..." twice | Create `guides/` entry |
| Bug took >30min to diagnose | Create troubleshooting guide |
| New institutional knowledge surfaces | Create `context/` entry |
| Work focus changes | Update `active/` entries |
| Old active entry is stale | Move to `context/` or delete |
| Conversation produced valuable insight | Distill into the appropriate category |

Do not create decision records. The `decisions/` folder is intentionally left empty.

### Manual distill

At the end of a significant session, ask: "What did I learn that should
outlive this conversation?" Write it down in the appropriate folder.

---

## Output Checklist

After completing all phases, the atlas should contain:

- [ ] `NAPKIN.md` — filled, under 250 tokens, no placeholders
- [ ] `structure/` — 2-5 entries mapping major project boundaries
- [ ] `decisions/` — empty (not tracked in this atlas)
- [ ] `guides/` — 2-3 entries for recurring procedures
- [ ] `context/` — 1-3 entries for institutional knowledge
- [ ] `active/` — 1 entry capturing current state
- [ ] All entries have frontmatter (`date`, `tags`)
- [ ] All entries have at least one `[[wikilink]]`
- [ ] `napkin overview` produces meaningful, distinct keywords per folder
- [ ] `napkin search` returns relevant results for 4 test queries
- [ ] No placeholder text anywhere in the atlas
- [ ] `AGENTS.md` has progressive disclosure section at the top
