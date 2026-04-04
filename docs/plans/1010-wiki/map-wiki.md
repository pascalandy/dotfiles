# LLM Wiki

A pattern for building personal knowledge bases using LLMs.

This is an idea file, it is designed to be copy pasted to your own LLM Agent (e.g. OpenAI Codex, Claude Code, OpenCode / Pi, or etc.). Its goal is to communicate the high level idea, but your agent will build out the specifics in collaboration with you.

# The core idea

Most people's experience with LLMs and documents looks like RAG: you upload a collection of files, the LLM retrieves relevant chunks at query time, and generates an answer. This works, but the LLM is rediscovering knowledge from scratch on every question. There's no accumulation. Ask a subtle question that requires synthesizing five documents, and the LLM has to find and piece together the relevant fragments every time. Nothing is built up. NotebookLM, ChatGPT file uploads, and most RAG systems work this way.

The idea here is different. Instead of just retrieving from raw documents at query time, the LLM **incrementally builds and maintains a persistent wiki** — a structured, interlinked collection of markdown files that sits between you and the raw sources. When you add a new source, the LLM doesn't just index it for later retrieval. It reads it, extracts the key information, and integrates it into the existing wiki — updating entity pages, revising topic summaries, noting where new data contradicts old claims, strengthening or challenging the evolving synthesis. The knowledge is compiled once and then *kept current*, not re-derived on every query.

This is the key difference: **the wiki is a persistent, compounding artifact.** The cross-references are already there. The contradictions have already been flagged. The synthesis already reflects everything you've read. The wiki keeps getting richer with every source you add and every question you ask.

You never (or rarely) write the wiki yourself — the LLM writes and maintains all of it. You're in charge of sourcing, exploration, and asking the right questions. The LLM does all the grunt work — the summarizing, cross-referencing, filing, and bookkeeping that makes a knowledge base actually useful over time. In practice, I have the LLM agent open on one side and Obsidian open on the other. The LLM makes edits based on our conversation, and I browse the results in real time — following links, checking the graph view, reading the updated pages. Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase.

This can apply to a lot of different contexts. A few examples:

- **Personal**: tracking your own goals, project management, health, psychology, self-improvement — filing journal entries, articles, podcast notes, and building up a structured picture of yourself over time.
- **Business/team**: an internal wiki maintained by LLMs, a federation of "Personal" wiki. It can be fed by Slack threads, meeting transcripts, project documents, customer calls. Possibly with humans in the loop reviewing updates. The wiki stays current because the LLM does the maintenance that no one on the team wants to do.
- **Research**: going deep on a topic over weeks or months — reading papers, articles, reports, and incrementally building a comprehensive wiki with an evolving thesis.
- **Competitive analysis, due diligence, trip planning, course notes, hobby deep-dives** — anything where you're accumulating knowledge over time and want it organized rather than scattered.
- **Reading a book**: filing each chapter as you go, building out pages for characters, themes, plot threads, and how they connect. By the end you have a rich companion wiki. Think of fan wikis like [Tolkien Gateway](https://tolkiengateway.net/wiki/Main_Page) — thousands of interlinked pages covering characters, places, events, languages, built by a community of volunteers over years. You could build something like that personally as you read, with the LLM doing all the cross-referencing and maintenance.

## Architecture

There are two layers:

**The wiki** — all markdown files live in `/references/`. This includes source material (`kind/webclip`), synthesized pages (research, relationships, concepts), operational records (LOG.md), and everything else. The `kind/` tag distinguishes what each file is. INDEX.md at the root catalogs them. The LLM creates pages, updates them when new sources arrive, maintains cross-references, and keeps everything consistent. You read it; the LLM writes it.

**The schema** — a global document (AGENTS.md) that tells the LLM how wikis are structured, what the conventions are, and what workflows to follow when ingesting sources, answering questions, or maintaining the wiki. This is not per-wiki — it's a single set of instructions shared across all wiki instances. This is the key configuration file — it's what makes the LLM a disciplined wiki maintainer rather than a generic chatbot. You and the LLM co-evolve this over time as you figure out what works.

## Operations

**Ingest.** You add a new source to `/references/` as a webclip and tell the LLM to process it. An example flow: the LLM reads the source, discusses key takeaways with you, writes a summary page in the wiki, updates the index, updates relevant entity and concept pages across the wiki, and appends an entry to the log. A single source might touch 10-15 wiki pages. Personally I prefer to ingest sources one at a time and stay involved — I read the summaries, check the updates, and guide the LLM on what to emphasize. But you could also batch-ingest many sources at once with less supervision. It's up to you to develop the workflow that fits your style and document it in the schema for future sessions.

**New page vs update.** If the new source covers an entity or concept that already has a page, update the existing page with the new information. If it covers a distinct subtopic, create a new page and cross-link it. Webclips (`kind/webclip`) always get their own page — they're source snapshots, not synthesized content.

**Query.** You ask questions against the wiki. The LLM searches for relevant pages, reads them, and synthesizes an answer with citations. Answers can take different forms depending on the question — a markdown page, a comparison table, a slide deck (Marp), a chart (matplotlib), a canvas. The important insight: **good answers can be filed back into the wiki as new pages.** A comparison you asked for, an analysis, a connection you discovered — these are valuable and shouldn't disappear into chat history. This way your explorations compound in the knowledge base just like ingested sources do.

**Lint.** Periodically, ask the LLM to health-check the wiki. Look for: contradictions between pages, stale claims that newer sources have superseded, orphan pages with no inbound links, important concepts mentioned but lacking their own page, missing cross-references, data gaps that could be filled with a web search. The LLM is good at suggesting new questions to investigate and new sources to look for. This keeps the wiki healthy as it grows.

## Indexing and logging

Two special files help the LLM (and you) navigate the wiki as it grows. They serve different purposes:

**INDEX.md** is content-oriented. It's a catalog of everything in the wiki — a table with a link and a one-line description per page. The LLM updates it on every ingest. When answering a query, the LLM reads the index first to find relevant pages, then drills into them. This works surprisingly well at moderate scale (~100 sources, ~hundreds of pages) and avoids the need for embedding-based RAG infrastructure.

Example:

```md
## wiki map

| File | Description |
|------|-------------|
| `references/vitamin-d-and-sleep.md` | Research on vitamin D's effect on sleep quality |
| `references/dr-smith-profile.md` | Dr. Smith — endocrinologist, author of sleep study |
| `references/supplement-comparison.md` | Side-by-side comparison of vitamin D brands |
```

**LOG.md** lives in `/references/` (`kind/log`). It's an append-only record of what happened and when. Each entry is a markdown list item with a fixed format for easy parsing:

```md
- [[2026-04-04]] ingest | vitamin-d-and-sleep | Ingested article, created entity page for Dr. Smith, updated supplement comparison
- [[2026-04-03]] query | magnesium-vs-zinc | Generated comparison table, filed as new page
- [[2026-04-02]] lint | full sweep | Found 3 orphan pages, added cross-references
```

Retrieve the latest entries with: `grep "^- \[\[" references/LOG.md | tail -10`

The log gives you a timeline of the wiki's evolution and helps the LLM understand what's been done recently.

## Tips and tricks

- **Obsidian Web Clipper** is a browser extension that converts web articles to markdown. Very useful for quickly getting sources into your raw collection.
- **Download images locally.** In Obsidian Settings → Files and links, set "Attachment folder path" to a fixed directory (e.g. `assets/`). Then in Settings → Hotkeys, search for "Download" to find "Download attachments for current file" and bind it to a hotkey (e.g. Ctrl+Shift+D). After clipping an article, hit the hotkey and all images get downloaded to local disk. This is optional but useful — it lets the LLM view and reference images directly instead of relying on URLs that may break. Note that LLMs can't natively read markdown with inline images in one pass — the workaround is to have the LLM read the text first, then view some or all of the referenced images separately to gain additional context. It's a bit clunky but works well enough.
- **Obsidian's graph view** is the best way to see the shape of your wiki — what's connected to what, which pages are hubs, which are orphans.
- **Marp** is a markdown-based slide deck format. Obsidian has a plugin for it. Useful for generating presentations directly from wiki content.
- **Bases** is an Obsidian core plugin that manages queries within Obsidian.
- if needed check skill `obsidian`
- The wiki is just a git repo of markdown files. You get version history, branching, and collaboration for free.

## Why this works

The tedious part of maintaining a knowledge base is not the reading or the thinking — it's the bookkeeping. Updating cross-references, keeping summaries current, noting when new data contradicts old claims, maintaining consistency across dozens of pages. Humans abandon wikis because the maintenance burden grows faster than the value. LLMs don't get bored, don't forget to update a cross-reference, and can touch 15 files in one pass. The wiki stays maintained because the cost of maintenance is near zero.

The human's job is to curate sources, direct the analysis, ask good questions, and think about what it all means. The LLM's job is everything else.

The idea is related in spirit to Vannevar Bush's Memex (1945) — a personal, curated knowledge store with associative trails between documents. Bush's vision was closer to this than to what the web became: private, actively curated, with the connections between documents as valuable as the documents themselves. The part he couldn't solve was who does the maintenance. The LLM handles that.

---

# Implementation

<!-- CEO / Validated [[2026-04-02]] -->

## File structure

```txt
{dir_name}/
  INDEX.md            # content catalog (area/ea, kind/wiki)
  /references/        # all wiki md pages: sources, logs, entities, concepts, etc.
  /scripts/           # scripts (optional)
  /assets/            # non-md files: images, PDFs, etc. (optional)
```

All content lives in `/references/` — flat, no subdirectories. Webclips (`kind/webclip`), LOG.md (`kind/log`), entity pages, concept pages, summaries, and everything else. Tags handle categorization; the filesystem stays simple. INDEX.md sits at the root and catalogs them.

The schema (conventions, workflows, structure rules) is defined globally in AGENTS.md, not per-wiki.

Each `{dir_name}/` is self-contained with its own INDEX.md and LOG.md. All wikis live in the same Obsidian vault, so `[[wikilinks]]` resolve across wikis naturally.

## Frontmatter and metadata

### General rule

- Every markdown file must include a YAML frontmatter with at minimum: `name`, `description`, `tags`, and `date_updated`.
- Non-markdown files (code, images, PDF, etc.) are exempt from frontmatter.
- Tags are lowercase only, no spaces.
- Bump `date_updated` on any content change — new sections, revised claims, new cross-references, fixes during lint.

Example:

```yaml
---
name: Vitamin D and Sleep
description: Research on vitamin D's effect on sleep quality
tags:
  - area/ea
  - kind/research
  - status/open
date_updated: 2026-04-04
---
```

### File naming and cross-references

- Filenames use **kebab-case**: `vitamin-d-and-sleep.md`, `dr-smith-profile.md`.
- Cross-references between pages use **Obsidian wikilinks**: `[[vitamin-d-and-sleep]]`.

### Page structure

Every wiki page follows this structure:

```yaml
---
name: Short human-readable title
description: One-line summary of what this page covers
tags:
  - area/ea
  - kind/research
  - status/open
date_updated: 2026-04-04
---
```

Body starts with a summary paragraph, then sections as needed, ending with:

```md
## Related

- [[other-page]]
- [[another-page]]
```

INDEX.md uses the same frontmatter convention:

```yaml
---
name: Health Wiki
description: Personal wiki tracking nutrition, supplements, sleep, and exercise
tags:
  - area/ea
  - kind/wiki
date_updated: 2026-04-04
---
```

### Label model — 4 orthogonal axes

Tags are distributed across 4 independent axes. Each axis answers a distinct question.

`ea` = executive assistant — marks files managed by the AI assistant.

**Axis 1 — AREA: which system component?** (required on every markdown file)

- INDEX.md     # content catalog (`area/ea`, `kind/wiki`)
- `area/ea`    # Apply to each and every note under any given wiki including INDEX.md

**Axis 2 — KIND: what is this file?** (required on every wiki note)

- `kind/wiki`  # apply only to INDEX.md at {dir_name}
- `kind/playbook` — reusable procedure or prompt
- `kind/relationship` — person or organization
- `kind/plan` — plan for something you intend to build or execute, may include strategic analysis
- `kind/research` — research
- `kind/blog` — draft or published blog post, content intended for external publication
- `kind/idea` — brainstorm or early-stage thinking, not tied to something you intend to build
- `kind/webclip` — source, scrap from the web
- `kind/tracking` — status/progress page that monitors something over time (projects, goals, personal metrics). Not tied to a single managed project — a dashboard you keep updated. (e.g. ACV4 status, health goals, quarterly OKRs)
- `kind/project/{name}` — artifact within a project. `{name}` matches the project root directory name (e.g. `kind/project/cass`, `kind/project/ccl`)
- `kind/log` — operational log, batch of historical decisions, retrospective
- `kind/task` — ad-hoc work
- `kind/template` — reusable scaffold
- `kind/hygiene` — drift sweep, metadata cleanup, structural maintenance
- `kind/bug` — system failure, broken tool, unexpected behavior
- `kind/role` — team role description (`TEAM_*.md` files)
- `kind/random` — for anything else

**Axis 3 — STATUS: where in the workflow?** (required on every wiki note, except `kind/project/*`)

- `status/draft` — structure laid out, minimal content
- `status/open` — in progress, partial. Default for new wiki pages.
- `status/stable` — complete, reliable reference (blog post)
- `status/blocked` — waiting on external input or a dependency
- `status/parked` — intentionally suspended
- `status/closed` — closed

Knowledge kinds (research, relationship, webclip, etc.) typically flow `draft` → `open` → `stable`. Actionable kinds (task, bug, plan, hygiene) use the full range including `blocked`, `parked`, `closed`.

**Axis 4 — PRIORITY: how urgent?** (only for actionable kinds: `kind/task`, `kind/bug`, `kind/plan`, `kind/hygiene`)

- `pty/p1` — urgent
- `pty/p2` — normal. Default when not specified.
- `pty/p3` — low priority

Knowledge kinds (`kind/wiki`, `kind/research`, `kind/relationship`, `kind/webclip`, `kind/idea`, `kind/tracking`, `kind/playbook`, `kind/blog`, `kind/role`, `kind/log`, `kind/random`, `kind/template`, `kind/project/{name}`) do not get priority tags.

### Tag order

Tags in the frontmatter always follow this order: `area` → `kind` → `status` → `pty`.

---

# use cases

tbd