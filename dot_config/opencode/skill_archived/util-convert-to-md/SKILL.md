---
name: convert-to-md
description: Convert documents to Markdown. Supports specific converter selection ("convert with Mistral", "convert with markitdown", "convert with pdftotext", "convert with Docker") or automatic mode using all converters to select the best result. Use for PDF, DOCX, PPTX, XLSX, HTML, images, audio, and other file formats.
---

# Convert to Markdown

Document conversion with single-converter or multi-converter mode.

## Mode Selection

Determine the conversion mode based on user request:

| User says                                      | Mode   | Action                          |
| ---------------------------------------------- | ------ | ------------------------------- |
| "convert with Mistral" / "using Mistral"       | Single | Use Mistral OCR only            |
| "convert with markitdown" / "using markitdown" | Single | Use uvx markitdown only         |
| "convert with Docker" / "using Docker"         | Single | Use Docker markitdown only      |
| "convert with pdftotext" / "using pdftotext"   | Single | Use pdftotext only              |
| "convert this PDF" (no method specified)       | Auto   | Run all converters, select best |

## Single Converter Mode

Use only the specified converter:

### markitdown (uvx)

```bash
uvx --from 'markitdown[all]' markitdown input.pdf -o output.md
```

See [converters/markitdown/SKILL.md](converters/markitdown/SKILL.md) for options.

### Docker

```bash
docker run --rm -v "$(pwd):/data" -w /data markitdown:latest input.pdf -o output.md
```

See [converters/docker/SKILL.md](converters/docker/SKILL.md) for setup.

### pdftotext

```bash
pdftotext -layout input.pdf output.txt
```

See [converters/pdftotext/SKILL.md](converters/pdftotext/SKILL.md) for options.

### Mistral OCR

```bash
cd .opencode/skill/convert-to-md/converters/mistral-ocr
uv run scripts/mistral_ocr.py /path/to/input.pdf -o /path/to/output.md
```

See [converters/mistral-ocr/SKILL.md](converters/mistral-ocr/SKILL.md) for setup.

## Auto Mode (All Converters)

When no specific converter is requested, run all available converters and select the best result.

### Step 1: Run all converters

```bash
# 1. uvx markitdown
uvx --from 'markitdown[all]' markitdown input.pdf -o input_uvx.md

# 2. Docker markitdown (if image available)
docker run --rm -v "$(pwd):/data" -w /data markitdown:latest input.pdf -o input_docker.md

# 3. pdftotext (PDF only)
pdftotext -layout input.pdf input_pdftotext.txt

# 4. Mistral OCR (if API key available)
cd .opencode/skill/convert-to-md/converters/mistral-ocr
uv run scripts/mistral_ocr.py /path/to/input.pdf -o /path/to/input_mistral.md
```

### Step 2: Compare and select

1. Read all generated files
2. Compare file sizes (character count)
3. Select the longest output as the best result
4. Copy the best result to `{basename}.md`

### Step 3: Report results

Inform the user:

- Which method produced the best result
- Character count for each output
- Any methods that failed or were skipped

## Quick Reference

| Converter           | Output suffix    | Best For                              |
| ------------------- | ---------------- | ------------------------------------- |
| markitdown (uvx)    | `_uvx.md`        | Most documents, preserves structure   |
| markitdown (Docker) | `_docker.md`     | Isolated execution, same as uvx       |
| pdftotext           | `_pdftotext.txt` | Fast text extraction, large PDFs      |
| Mistral OCR         | `_mistral.md`    | Scanned docs, images, complex layouts |

## Notes

- **Auto mode**: Skip unavailable converters (no Docker image, no API key) and inform user
- **pdftotext**: Only works with PDF files
- **Non-PDF files**: Only markitdown methods (uvx/Docker) apply
- **Mistral OCR**: Requires `MISTRAL_API_KEY` in `.env`
