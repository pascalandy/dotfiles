---
name: distill-router
description: Routes distill requests to the right input sub-skill based on what the user is feeding in. USE WHEN distill a local file, summarize this file, notes from article.md, process a markdown file, read this text file, distill this URL, summarize a web page, fetch and distill, distill this video, summarize a YouTube URL, podcast audio.
---

# distill Router

## Routing Table

| Request Pattern | Route To |
|---|---|
| distill `<local-file>`, summarize this file, notes from article.md, process a markdown file, read this text file | `from-file/SKILL.md` |
| distill this URL, summarize a web page, fetch and distill | **Out of scope in v1.** Deferred to a future `from-url/SKILL.md`. |
| distill this video, summarize a YouTube URL, podcast audio | **Out of scope.** Use `utils/transcript-sk` for YouTube. `from-media/SKILL.md` is future work. |

## Default

If the input is a path to a file on disk, route to `from-file/SKILL.md`.

## Why a Router for One Sub-Skill?

`meta/distill` is intentionally a meta-skill even though v1 ships with a single input path (`from-file`). Future expansion (`from-url`, `from-media`) will add rows here without requiring callers to change how they invoke the top-level `distill` skill.
