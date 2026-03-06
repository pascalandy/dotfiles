---
name: pdftotext
description: Extract text from PDF using pdftotext CLI (poppler-utils). Fast, reliable, plain text output.
---

# pdftotext

Extract plain text from PDF files using the `pdftotext` command-line utility.

## When to Use

- For very large PDFs where speed is a priority
- When you only need raw text without markdown formatting
- For scanned PDFs with embedded text layers

## Basic Usage

```bash
# Extract text to a file
pdftotext input.pdf output_pdftotext.txt

# Extract text to stdout
pdftotext input.pdf -

# Maintain original physical layout (useful for tables/columns)
pdftotext -layout input.pdf output_pdftotext.txt
```

## Options

| Option          | Description                            |
| --------------- | -------------------------------------- |
| `-f <int>`      | First page to convert                  |
| `-l <int>`      | Last page to convert                   |
| `-layout`       | Maintain original physical layout      |
| `-raw`          | Keep strings in content stream order   |
| `-nopgbrk`      | Don't insert page breaks between pages |
| `-enc <string>` | Output text encoding (e.g., UTF-8)     |

## Examples

```bash
# Extract pages 1-5 only
pdftotext -f 1 -l 5 input.pdf output_pdftotext.txt

# Preserve layout for tables
pdftotext -layout input.pdf output_pdftotext.txt

# UTF-8 encoding
pdftotext -enc UTF-8 input.pdf output_pdftotext.txt
```

## Notes

- Part of `poppler-utils` package
- Install: `brew install poppler` (macOS) or `apt install poppler-utils` (Linux)
- Output is plain text (.txt), not markdown
