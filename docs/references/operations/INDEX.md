---
name: Operations Wiki
description: Documentation and notes about how the chezmoi repository itself runs, applies, and distributes assets
tags:
  - area/ea
  - kind/wiki
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-19
---

# Operations Wiki

> Content catalog. Every wiki page is listed here with a one-line summary.
> Read this first to find relevant pages for any query.
> **Parent index:** [`../INDEX.md`](../INDEX.md) | **Total pages:** 2 | **Last updated:** 2026-04-19

This category covers how the repo itself operates: what runs on `chezmoi apply`, how `dot_config/ai_templates/` fans out to the eight agent homes, how VS Code and the Brewfile sync back, and how to debug the pipeline.

Category follows the **generic guide + personal preferences** pattern from [`docs/INDEX.md`](../INDEX.md). Operations pages today are generic — they describe what the scripts in `.chezmoiscripts/` do, not one operator's preferred cadence — so every page here is a `how-to-*` page. Personal preferences about operations (e.g. "I apply twice a day", "I forbid the brewfile dump") would go into a `how-my-operations-are-run.md` sibling, not added today.

## Wiki Map

### kind/log

| File | Description |
|------|-------------|
| `references/LOG.md` | Operational log |

### kind/wiki

| File | Description |
|------|-------------|
| [`references/how-ai-templates-are-distributed/INDEX.md`](references/how-ai-templates-are-distributed/INDEX.md) | The post-apply fan-out: how `dot_config/ai_templates/` renders through chezmoi and rsyncs into eight agent homes |
| [`references/how-vscode-and-brewfile-sync-back/INDEX.md`](references/how-vscode-and-brewfile-sync-back/INDEX.md) | The pre-apply reverse sync: VS Code settings/keybindings/extensions and the rate-limited Brewfile dump |

## Related

- [[docs/INDEX.md]] — root catalog
- [[configs/INDEX.md]] — individual config files and tools
- [[skills/INDEX.md]] — per-skill wikis organized by 8 workflow-arc buckets
