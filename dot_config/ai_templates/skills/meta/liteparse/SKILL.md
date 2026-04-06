---
name: liteparse
description: Parse, convert, or extract text from unstructured documents (PDF, DOCX, PPTX, XLSX, images) locally with the LiteParse CLI -- no cloud, no LLM. USE WHEN parse pdf, parse document, extract text, OCR pdf, OCR image, convert docx, convert pptx, convert xlsx, batch parse, page screenshot, render pdf pages, lit cli, liteparse, install liteparse, libreoffice, imagemagick, my parse preferences, LYKRA.
---

# LiteParse

Local, fast, dependency-light document parsing via the `lit` CLI. This meta-skill bundles user preferences, parsing commands, page screenshots, and install steps.

## Canonical entry point: `lykra-parse`

When the user provides a path, run **one command**:

```bash
lykra-parse <file-or-dir>          # English (default)
lykra-parse <file-or-dir> --fr     # French
```

`lykra-parse` is a wrapper at `~/.local/bin/lykra-parse` (chezmoi-managed) that:
- auto-detects file vs directory
- loads `~/.config/liteparse/config.{en,fr}.json`
- runs `lit parse` or `lit batch-parse`
- atomically renames outputs to `_lykra.txt`

**Do not call `lit` directly** unless the user asks for a non-default option (json output, page range, screenshots, etc.) — those go through `Parse` or `Screenshot`.

Do not prompt for format, language, DPI, or confirmation when a path is given. Run `lykra-parse` immediately. Only ask if the path is missing.

## What's Included

| Sub-skill | Purpose |
|---|---|
| `Preferences` | User defaults (lang, dpi, format, output suffix) stored in `config.en.json` / `config.fr.json` |
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
