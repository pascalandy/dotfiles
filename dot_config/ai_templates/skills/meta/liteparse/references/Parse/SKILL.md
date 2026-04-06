---
name: liteparse-parse
description: Full reference for `lit parse` and `lit batch-parse` -- options, OCR, output formats, page ranges, config files, HTTP OCR servers. USE WHEN parse pdf, parse document, extract text, OCR, convert docx, batch parse, json output, page range, bbox, HTTP OCR server.
---

# LiteParse — Parse

For user defaults, see `../Preferences/SKILL.md`. This file documents the full CLI surface.

**Note on output formats:** LiteParse natively supports only `--format text` and `--format json`. There is no markdown format. The `outputSuffix` field in user configs is a local naming convention applied by post-processing rename, not by `lit` itself.

## Single file

```bash
# Basic text extraction
lit parse document.pdf

# JSON with bounding boxes, saved to file
lit parse document.pdf --format json -o output.json

# Specific page range
lit parse document.pdf --target-pages "1-5,10,15-20"

# Disable OCR (faster, text-only PDFs)
lit parse document.pdf --no-ocr

# External HTTP OCR server
lit parse document.pdf --ocr-server-url http://localhost:8828/ocr

# Higher DPI
lit parse document.pdf --dpi 300
```

## Batch a directory

```bash
lit batch-parse ./input ./output

# Only PDFs, recursively
lit batch-parse ./input ./output --extension .pdf --recursive
```

## OCR options

| Option | Description |
|---|---|
| (default) | Tesseract.js — zero setup |
| `--ocr-language <iso>` | OCR language code (e.g. `en`, `fra`) |
| `--ocr-server-url <url>` | External HTTP OCR server (EasyOCR, PaddleOCR, custom) |
| `--no-ocr` | Disable OCR entirely |

## Output options

| Option | Description |
|---|---|
| `--format json` | Structured JSON with bounding boxes |
| `--format text` | Plain text (default) |
| `-o <file>` | Save output to file |

## Performance / quality

| Option | Description |
|---|---|
| `--dpi <n>` | Rendering DPI (default 150; 300 for high quality) |
| `--max-pages <n>` | Limit pages parsed |
| `--target-pages <pages>` | Parse specific pages, e.g. `"1-5,10"` |
| `--no-precise-bbox` | Disable precise bounding boxes (faster) |
| `--skip-diagonal-text` | Ignore rotated/diagonal text |
| `--preserve-small-text` | Keep very small text |

## Config file

```bash
lit parse document.pdf --config ./liteparse.config.json
```

Example for an HTTP OCR backend:

```json
{
  "ocrServerUrl": "http://localhost:8828/ocr",
  "ocrLanguage": "en",
  "outputFormat": "json"
}
```

## HTTP OCR server API

Custom backends must implement:

- **Endpoint**: `POST /ocr`
- **Accepts**: `file` (multipart) and `language` (string)
- **Returns**:
  ```json
  {
    "results": [
      { "text": "Hello", "bbox": [x1, y1, x2, y2], "confidence": 0.98 }
    ]
  }
  ```

Ready-to-use wrappers exist for EasyOCR and PaddleOCR upstream (see `../Setup/UPSTREAM.md`).
