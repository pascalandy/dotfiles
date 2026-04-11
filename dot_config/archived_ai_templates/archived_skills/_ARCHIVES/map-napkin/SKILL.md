---
name: map-napkin
description: >
  Use only when the user explicitly says "map-napkin". Create and update project
  reference maps using Napkin. Use when the user wants to bootstrap a new .napkin/
  atlas, update an existing atlas, audit atlas quality, or run atlas maintenance.
  Also use when user mentions napkin init, napkin overview, napkin search, or
  project reference map.
---

# Map Napkin

Build and maintain a **project reference map** for AI agents using
[Napkin](https://github.com/Michaelliv/napkin). The atlas lives in `.napkin/`
at the project root. Its purpose is to give agents a structured, searchable
map of the project — what exists, why it exists, how things connect, and what
to watch out for.

This is not a note-taking system or file manager. The `.napkin/` directory is
a curated map that agents consume through progressive disclosure. Napkin
auto-generates a navigable index from the map's structure using TF-IDF keyword
extraction and BM25 search ranking.

Install: `bun install -g napkin-ai`

## When to use this skill

| User intent | Action |
|-------------|--------|
| "Create a napkin atlas" / "map-napkin" | Run the **Create** workflow |
| "Update the napkin" / "refresh the atlas" | Run the **Update** workflow |
| "Audit the atlas" / "check atlas quality" | Run the **Verify** workflow |

## Progressive Disclosure (how agents consume the atlas)

| Level | Command | Token cost | Purpose |
|-------|---------|-----------|---------|
| L0 | `NAPKIN.md` | ~200 | Always-loaded project context anchor |
| L1 | `napkin overview --json` | ~1-2k | Atlas map: folders, TF-IDF keywords, tags, counts |
| L2 | `napkin search "<query>"` | ~2-5k | BM25 ranked results with snippets |
| L3 | `napkin read "<file>"` / `rg`, `fd` | variable | Full content of a specific map entry |

**Rule: Start at L0. Descend only when the current level doesn't answer.**

## AGENTS.md Integration

On every **Create** or **Update** run, check the project's `AGENTS.md` file.
Ensure it starts with this section (add it if missing, preserve everything else below):

```markdown
## Project overview using progressive disclosure

1. Read and understand: `.napkin/NAPKIN.md`
2. run `napkin overview --json`
```

If `AGENTS.md` does not exist, create it with this section as the starting content.

## Workflow: Create a new atlas

Read the full guide before starting: [references/bootstrap-guide.md](references/bootstrap-guide.md)

### Step 0 — Initialize

Pick the template that matches the project type:

```bash
napkin init --template coding     # Software project
napkin init --template company    # Team/org knowledge
napkin init --template product    # Product development
napkin init --template personal   # Personal knowledge
napkin init --template research   # Research/academic
napkin init --list                # See all templates
```

### Step 1 — Discover

Explore the project deeply before writing any map entries. Understand identity,
topology, conventions, current state, and fragility points. See the Discovery
section in `references/bootstrap-guide.md` for strategies by project type.

### Step 2 — Write NAPKIN.md

The single most important file. Under 250 tokens. No filler. Only facts an agent
needs in EVERY interaction. Use the template in `references/bootstrap-guide.md#phase-1`.

### Step 3 — Create map entries by category

Follow the templates in `references/bootstrap-guide.md`:

| Folder | Purpose | How many |
|--------|---------|----------|
| `structure/` | Map project topology and boundaries | 2-5 entries |
| `guides/` | How-to procedures for recurring tasks | 2-3 entries |
| `context/` | Institutional knowledge, gotchas, debt | 1-3 entries |
| `active/` | Current work state, open questions | 1 entry |

**`decisions/` folder** — Napkin templates may scaffold this directory. Do not
populate it. This atlas does not track decisions. If the folder exists, leave it
empty or add a single `_about.md` stating: "Decisions are not tracked in this atlas."

Every map entry MUST have:
- Frontmatter with `date` and `tags`
- At least one `[[wikilink]]` to another entry
- Specific language in headings (not generic words like "overview")

### Step 4 — Wire connections

Add wikilinks between entries. Wikilinks are ranking signals for search — an
entry with 5 inbound links ranks higher than an orphan with the same text match.
Use `napkin link orphans` to find unlinked entries.

### Step 5 — Update AGENTS.md

Ensure the progressive disclosure section is at the top of `AGENTS.md` (see
AGENTS.md Integration above).

### Step 6 — Verify

Run the verification checklist from `references/bootstrap-guide.md#phase-8`.

## Workflow: Update an existing atlas

1. Run `napkin overview` to see current state
2. Run `napkin link orphans` and `napkin link deadends` to find disconnected entries
3. Check for stale `active/` entries — move to `context/` or delete
4. Apply maintenance triggers:

| Event | Action |
|-------|--------|
| Architecture changes | Update or create `structure/` entry |
| Someone asks "how do I..." twice | Create `guides/` entry |
| Bug took >30min to diagnose | Create troubleshooting guide |
| New institutional knowledge | Create `context/` entry |
| Work focus changes | Update `active/` entries |

Do not create decision records. The `decisions/` folder is intentionally left empty.

5. Verify with `napkin overview` — each folder should show distinct, meaningful keywords
6. Ensure `AGENTS.md` still has the progressive disclosure section at the top

## Workflow: Verify atlas quality

```bash
napkin overview                    # Check keyword quality per folder
napkin link orphans                # Entries with no incoming links
napkin link deadends               # Entries with no outgoing links
napkin link unresolved             # Broken wikilinks
napkin search "architecture"       # Test retrieval for structure
napkin search "conventions"         # Test retrieval for context
napkin search "how to"             # Test retrieval for guides
```

Checklist:
- [ ] NAPKIN.md under 250 tokens, no placeholders
- [ ] Each folder shows distinct TF-IDF keywords in overview
- [ ] No orphan entries (every entry has at least one inbound link)
- [ ] No unresolved links
- [ ] Search returns relevant results for 5 different query types
- [ ] No placeholder text ("TBD", empty sections) in any entry
- [ ] `AGENTS.md` has progressive disclosure section at the top

## CLI Quick Reference

```bash
napkin init --template <name>        # Scaffold atlas
napkin overview                      # TF-IDF keyword map (human-readable)
napkin overview --json               # TF-IDF keyword map (structured)
napkin overview --depth 3            # Limit folder depth
napkin vault                         # Atlas info (path, size)
```

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON (for programmatic access) |
| `--vault <path>` | Override atlas path (napkin CLI flag name) |

## References

| File | Contents |
|------|----------|
| `references/bootstrap-guide.md` | Full phase-by-phase creation guide with templates, quality principles, and verification checklists |

## Quality Principles

These principles drive how the map is written. They matter because Napkin's
TF-IDF and BM25 engines derive keyword quality and search relevance directly
from the text you write — headings are weighted 3x, filenames 2x, body 1x.

1. **Specific over generic** — "PostgreSQL pooling is 20 because 3 serverless functions share one RDS instance" beats "database is configured." Specific language produces distinct TF-IDF keywords.
2. **Short over long** — 15 useful lines > 150 skipped lines. Agents have token budgets.
3. **Why over what** — the project itself shows what exists; the atlas explains why it exists and what to watch out for.
4. **Linked over isolated** — orphan entries are invisible to the ranking engine. Every entry must be reachable through at least one wikilink.
5. **Current over historical** — a wrong entry is worse than no entry. Stale entries mislead agents.
6. **Selective over exhaustive** — document the 20% of knowledge that covers 80% of what agents need. The rest stays in source code where it belongs.
