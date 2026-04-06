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

## User configs

`~/.config/liteparse/config.en.json` and `config.fr.json` are managed by chezmoi (`dot_config/liteparse/` in source). Run `chezmoi apply` to install/update.

## Supported input formats

| Category | Formats |
|---|---|
| PDF | `.pdf` |
| Word | `.doc`, `.docx`, `.docm`, `.odt`, `.rtf` |
| PowerPoint | `.ppt`, `.pptx`, `.pptm`, `.odp` |
| Spreadsheets | `.xls`, `.xlsx`, `.xlsm`, `.ods`, `.csv`, `.tsv` |
| Images | `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.webp`, `.svg` |

Office documents auto-convert via LibreOffice; images via ImageMagick.
