---
name: mistral-ocr
description: OCR-based PDF/image to Markdown using Mistral AI. Best for scanned documents and images. Requires MISTRAL_API_KEY.
---

# Mistral OCR

OCR conversion using Mistral AI API. Excellent for scanned documents, images with text, and complex layouts.

## Prérequis

1. Copy `.env.example` to `.env`
2. Add your `MISTRAL_API_KEY` to `.env`

## Usage

```bash
# From the mistral-ocr directory
cd .opencode/skill/convert-to-md/converters/mistral-ocr

# Basic usage
uv run scripts/mistral_ocr.py input.pdf -o output_mistral.md

# With options
uv run scripts/mistral_ocr.py input.pdf -o output_mistral.md --table-format html
uv run scripts/mistral_ocr.py input.pdf -o output_mistral.md --no-images
```

## Options

| Option           | Description                                      |
| ---------------- | ------------------------------------------------ |
| `-o, --output`   | Output file path (default: `{input}_mistral.md`) |
| `--table-format` | `markdown` (default) or `html`                   |
| `--no-images`    | Exclude base64 images from output                |

## Supported Formats

- PDF (.pdf)
- Images: PNG, JPG, JPEG, GIF, WEBP

## Notes

- Best results for scanned documents and images
- Preserves table structure
- Can extract text from images within PDFs
- API usage incurs costs based on Mistral pricing
