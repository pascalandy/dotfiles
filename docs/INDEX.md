---
name: Dotfiles Docs
description: Root router for the chezmoi dotfiles documentation tree
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-18
---

# Dotfiles Docs

> Root router for `~/.local/share/chezmoi/docs/`.
> This page points to child wiki maps. Do not treat it as the place where leaf content lives.
> **Child wikis:** 4 | **Last updated:** 2026-04-18

This root index exists to route humans and agents into the right child `INDEX.md`.

Each directory under `docs/references/` is its own wiki map with its own catalog, local conventions, and `references/LOG.md`. Traverse one layer at a time:

1. Start here.
2. Open the matching child wiki `INDEX.md`.
3. From there, open the nested wiki or page you actually need.

## How To Use This Index

Use the child wiki indexes as the real entry points:

- `configs/` for configuration files, tools, and machine-specific setup notes
- `skills/` for per-skill narrative wikis, organized by the 8 workflow-arc buckets (`pa-sdlc`, `devtools`, `think`, `knowledge`, `web`, `distill`, `diagram`, `media`)
- `operations/` for how this repo runs, applies, syncs, and distributes assets
- `ideas/` for brainstorms and early-stage material

Root-level policy stays light on purpose. Detailed conventions belong in the child wiki that owns them.

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| [`references/LOG.md`](references/LOG.md) | Operational log for the root docs wiki |

### kind/wiki

| File | Description |
|------|-------------|
| [`references/configs/INDEX.md`](references/configs/INDEX.md) | Child wiki map for configuration references, generic guides, and personal setup docs |
| [`references/skills/INDEX.md`](references/skills/INDEX.md) | Child wiki map for per-skill narrative wikis, organized by 8 workflow-arc buckets |
| [`references/operations/INDEX.md`](references/operations/INDEX.md) | Child wiki map for repository operations, apply flow, and distribution mechanics |
| [`references/ideas/INDEX.md`](references/ideas/INDEX.md) | Child wiki map for brainstorms, drafts, and exploratory material |

## Related

- [[configs/INDEX.md]]
- [[skills/INDEX.md]]
- [[operations/INDEX.md]]
- [[ideas/INDEX.md]]
