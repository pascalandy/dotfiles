---
name: obsidian
description: Obsidian vault management -- notes, markdown, Bases database views, JSON Canvas visual maps, and CLI automation. USE WHEN obsidian, vault, notes, wikilinks, embeds, callouts, frontmatter, tags, properties, create note, search vault, organize notes, obsidian markdown, index notes, aliases, block IDs, base files, bases, table view, card view, list view, map view, filters, formulas, summaries, database view, .base, groupBy, computed properties, canvas, mind map, flowchart, nodes, edges, groups, visual map, .canvas, json canvas, project board, research canvas, obsidian cli, plugin development, reload plugin, screenshot, dom inspect, eval, daily note, append note, search command, tasks command, backlinks command, dev errors, console output.
---

# Obsidian

> Four specialized modes for working with Obsidian vaults -- from creating notes with wikilinks to building database views with Bases, composing visual canvases, and automating via CLI, routed automatically based on what you need.

---

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.

---

## The Problem

Obsidian vaults involve several distinct file formats and interaction modes. A note with wikilinks and callouts is not the same task as building a `.base` database view with formulas, which is not the same as laying out a `.canvas` visual map, which is not the same as scripting vault operations through the CLI. When you bring these tasks to an AI, you get generic Markdown help that misses Obsidian-specific syntax, or Base files with broken YAML, or Canvas JSON with dangling edge references. You end up:

- **Getting broken syntax** -- the AI produces standard Markdown but misses Obsidian extensions like wikilinks, callouts, block IDs, and embeds
- **Writing invalid Bases** -- duration math without field access, unguarded null properties, formulas referencing undefined names
- **Generating bad Canvas JSON** -- duplicate node IDs, edges referencing non-existent nodes, overlapping layouts
- **Missing CLI capabilities** -- manually editing files when `obsidian` CLI commands could search, create, append, and manage properties directly
- **Mixing concerns** -- asking for a Base view but getting a Markdown table, or asking for a Canvas but getting a Mermaid diagram

The fundamental issue: Obsidian vault work spans four distinct domains, each with its own file format, validation rules, and gotchas.

---

## The Solution

The Obsidian skill provides four specialized modes, each with its own format knowledge, validation rules, and workflows:

1. **obsidian-sk** -- Create, search, edit, and organize vault notes using Obsidian Flavored Markdown. Handles wikilinks, embeds, callouts, properties (frontmatter), tags, and index notes. Knows the naming conventions, gotchas (aliases must be lists, frontmatter must be first line), and when to use wikilinks vs standard links.

2. **bases-sk** -- Create and edit Obsidian Bases (`.base` files) with YAML-based views, filters, formulas, and summaries. Covers table, cards, list, and map view types. Knows filter syntax, formula functions, duration math, null guards, and YAML quoting rules.

3. **canva-sk** -- Create and edit JSON Canvas files (`.canvas`) with text, file, link, and group nodes plus edges. Follows the JSON Canvas Spec 1.0. Handles ID generation, layout spacing, edge anchoring, color presets, and validation of referential integrity.

4. **obsidian-cli** -- Interact with a running Obsidian instance via the `obsidian` CLI. Read, create, append, search notes. Manage properties, tasks, tags, backlinks. Supports plugin development workflows: reload, screenshot, DOM inspection, eval, error capture.

The collection `SKILL.md` loads `references/ROUTER.md`, which routes requests to the right mode based on keyword matching. Each mode has its own `SKILL.md` and supporting reference documents.

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Skill router | `references/ROUTER.md` | Dispatches requests to the correct Obsidian mode |
| obsidian-sk skill | `references/obsidian-sk/SKILL.md` | Vault notes, Obsidian Flavored Markdown |
| obsidian-sk references | `references/obsidian-sk/references/` | PROPERTIES, EMBEDS, CALLOUTS, MARKDOWN docs |
| bases-sk skill | `references/bases-sk/SKILL.md` | Obsidian Bases (.base files) |
| bases-sk references | `references/bases-sk/references/` | Complete functions reference |
| canva-sk skill | `references/canva-sk/SKILL.md` | JSON Canvas (.canvas files) |
| canva-sk references | `references/canva-sk/references/` | Full canvas examples |
| obsidian-cli skill | `references/obsidian-cli/SKILL.md` | CLI automation and plugin development |

**Summary:**
- **Modes:** 4 (obsidian-sk, bases-sk, canva-sk, obsidian-cli)
- **Reference documents:** 6 supporting files
- **Dependencies:** Obsidian app (for CLI mode); none for file-based modes

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "create a note about project X with tags and wikilinks" | Routes to obsidian-sk -- creates note with frontmatter, tags, and `[[wikilinks]]` |
| "search the vault for notes about machine learning" | Routes to obsidian-sk -- searches by filename and content |
| "add a callout block to this note" | Routes to obsidian-sk -- inserts `> [!type]` callout syntax |
| "create a Base view that shows all tasks grouped by status" | Routes to bases-sk -- generates `.base` YAML with filters, formulas, and views |
| "add a formula to calculate days until due date" | Routes to bases-sk -- writes duration math with proper null guards |
| "build a mind map canvas for this project" | Routes to canva-sk -- generates `.canvas` JSON with nodes, edges, and layout |
| "add a new node to this canvas and connect it" | Routes to canva-sk -- appends node, generates edge with valid IDs |
| "read today's daily note" | Routes to obsidian-cli -- runs `obsidian daily:read` |
| "append a task to my daily note" | Routes to obsidian-cli -- runs `obsidian daily:append` |
| "reload my plugin and check for errors" | Routes to obsidian-cli -- runs plugin dev workflow |

---

## Example Usage

### Creating a Note with Wikilinks

```
User: create a note about Docker Compose with related links

AI responds:
Routing to obsidian-sk...

Creates "Docker Compose.md" with:
- Frontmatter: title, tags (docker, devops), aliases
- Content with Obsidian-specific syntax
- [[Docker]] and [[Container Orchestration]] wikilinks
- Verifies linked notes exist in vault
```

### Building a Base View

```
User: create a reading tracker base that shows books grouped by status

AI responds:
Routing to bases-sk...

Creates "reading-tracker.base" with:
- Filters: file.hasTag("book")
- Formulas: status_icon, reading_time with null guards
- Cards view for library browsing
- Table view for reading list
- Validates all formula references and YAML syntax
```

### Composing a Canvas

```
User: create a project planning canvas with three phases

AI responds:
Routing to canva-sk...

Creates "project-plan.canvas" with:
- 3 group nodes (Phase 1, Phase 2, Phase 3)
- Text nodes for deliverables inside each group
- Edges connecting phases left-to-right
- Validates all IDs unique, all edge references resolve
```

### CLI Automation

```
User: search the vault for notes tagged "meeting" from this week

AI responds:
Routing to obsidian-cli...

Runs: obsidian search query="#meeting" limit=20
Returns matching notes with paths and excerpts
```

---

## Configuration

No configuration required for file-based modes (obsidian-sk, bases-sk, canva-sk).

The obsidian-cli mode requires a running Obsidian instance.

| Configuration | Location | Purpose |
|--------------|----------|---------|
| Vault path | `chezmoi secret keyring get --service=OBSIDIAN_VAULT --user=path` | Resolves vault location for file operations |

---

## Customization

### Optional Customization

| Customization | Location | Impact |
|--------------|----------|--------|
| Property conventions | `references/obsidian-sk/references/PROPERTIES.md` | Adjust frontmatter field types and defaults |
| Callout types | `references/obsidian-sk/references/CALLOUTS.md` | Add custom callout types with CSS |
| Formula functions | `references/bases-sk/references/FUNCTIONS_REFERENCE.md` | Complete function reference for Base formulas |
| Canvas examples | `references/canva-sk/references/EXAMPLES.md` | Reference layouts for mind maps, boards, flowcharts |
