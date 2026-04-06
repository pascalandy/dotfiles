---
name: liteparse-setup
description: Install LiteParse and its optional dependencies (LibreOffice, ImageMagick). USE WHEN install liteparse, setup, lit not found, libreoffice, imagemagick, supported formats.
---

# LiteParse — Setup

Provenance and upstream links: see [`UPSTREAM.md`](./UPSTREAM.md).

## Install LiteParse

```bash
bun i -g @llamaindex/liteparse
lit --version
```

## Optional dependencies

Office documents (DOCX, PPTX, XLSX) — requires LibreOffice:

```bash
# macOS
brew install --cask libreoffice
# Ubuntu/Debian
apt-get install libreoffice
```

Images — requires ImageMagick:

```bash
# macOS
brew install imagemagick
# Ubuntu/Debian
apt-get install imagemagick
```

## User configs and wrapper

Managed by chezmoi (run `chezmoi apply` to install/update):

- `~/.config/liteparse/config.en.json` / `config.fr.json` — language configs (source: `dot_config/liteparse/`)
- `~/.local/bin/lykra-parse` — wrapper script that calls `lit` with defaults and applies the `_lykra.txt` naming (source: `dot_local/bin/executable_lykra-parse`)

Ensure `~/.local/bin` is in `PATH`.

## Tesseract OCR models

Tesseract.js downloads `*.traineddata` files (e.g. `eng.traineddata`, ~10 MB) on first OCR run. The wrapper `cd`s into `~/.cache/liteparse/tessdata/` before invoking `lit`, so models cache there once and stay out of your working directories. Safe to keep; deleting forces re-download.

## Supported input formats

| Category | Formats |
|---|---|
| PDF | `.pdf` |
| Word | `.doc`, `.docx`, `.docm`, `.odt`, `.rtf` |
| PowerPoint | `.ppt`, `.pptx`, `.pptm`, `.odp` |
| Spreadsheets | `.xls`, `.xlsx`, `.xlsm`, `.ods`, `.csv`, `.tsv` |
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg` |

Office documents auto-convert via LibreOffice; images via ImageMagick.
