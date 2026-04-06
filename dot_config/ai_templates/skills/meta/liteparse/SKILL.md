---
name: liteparse
description: Parse, convert, or extract text from unstructured documents (PDF, DOCX, PPTX, XLSX, images) locally with the LiteParse CLI -- no cloud, no LLM. USE WHEN parse pdf, parse document, extract text, OCR pdf, OCR image, convert docx, convert pptx, convert xlsx, batch parse, page screenshot, render pdf pages, lit cli, liteparse, install liteparse, libreoffice, imagemagick, my parse preferences, LYKRA.
---

# LiteParse

Local, fast, dependency-light document parsing via the `lit` CLI. This meta-skill bundles user preferences, parsing commands, page screenshots, and install steps.

## Auto-detect rule (do not ask, just run)

When the user provides a path:

- **File** → `lit parse` with the user's config (see `Preferences`).
- **Directory** → `lit batch-parse` with the user's config (see `Preferences`).

Do not prompt for format, language, DPI, or confirmation when a path is given. Execute immediately using `Preferences/config.json`. Output is markdown (`.md`) by default. Only ask if the path is missing or ambiguous.

## What's Included

| Sub-skill | Purpose |
|---|---|
| `Preferences` | User defaults (lang, dpi, format, output suffix) stored in `config.json` |
| `Parse` | Full `lit parse` / `lit batch-parse` reference and options |
| `Screenshot` | `lit screenshot` for rendering pages as images |
| `Setup` | Install LiteParse + LibreOffice + ImageMagick; upstream provenance |

## Invocation Scenarios

| Trigger | Routes to |
|---|---|
| user gives a file or directory path | `Preferences` (execute immediately) |
| "json output", "page range", "bbox", "HTTP OCR server" | `Parse` |
| "screenshot pages", "render pages" | `Screenshot` |
| "install liteparse", "lit not found", "libreoffice", "imagemagick" | `Setup` |

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.
