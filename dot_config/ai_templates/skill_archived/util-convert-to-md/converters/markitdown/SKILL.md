---
name: markitdown
description: Convert documents to Markdown using uvx markitdown. Supports PDF, DOCX, PPTX, XLSX, HTML, CSV, JSON, XML, images, audio, YouTube URLs, EPubs.
---

# markitdown (uvx)

Convert files to Markdown using `uvx` with `markitdown` — no installation required.

## Basic Usage

For formats requiring optional dependencies (PDF, DOCX, PPTX, XLSX, audio, etc.), use `--from` with the appropriate extra:

```bash
# PDF files
uvx --from 'markitdown[pdf]' markitdown input.pdf -o output_uvx.md

# Word documents
uvx --from 'markitdown[docx]' markitdown input.docx -o output_uvx.md

# PowerPoint presentations
uvx --from 'markitdown[pptx]' markitdown input.pptx -o output_uvx.md

# Excel spreadsheets (.xlsx)
uvx --from 'markitdown[xlsx]' markitdown input.xlsx -o output_uvx.md

# Excel spreadsheets (.xls - older format)
uvx --from 'markitdown[xls]' markitdown input.xls -o output_uvx.md

# Audio transcription
uvx --from 'markitdown[audio-transcription]' markitdown audio.mp3 -o output_uvx.md

# YouTube transcription
uvx --from 'markitdown[youtube-transcription]' markitdown "https://youtube.com/watch?v=..." -o output_uvx.md

# All features (when unsure or multiple formats)
uvx --from 'markitdown[all]' markitdown input.pdf -o output_uvx.md
```

For simple formats (HTML, CSV, JSON, XML, plain text), no extras needed:

```bash
uvx markitdown input.html -o output_uvx.md
uvx markitdown data.csv -o output_uvx.md
```

## Optional Dependency Groups

| Extra                     | File Types                  |
| ------------------------- | --------------------------- |
| `[pdf]`                   | PDF files                   |
| `[docx]`                  | Word documents (.docx)      |
| `[pptx]`                  | PowerPoint (.pptx)          |
| `[xlsx]`                  | Excel (.xlsx)               |
| `[xls]`                   | Older Excel (.xls)          |
| `[outlook]`               | Outlook messages (.msg)     |
| `[audio-transcription]`   | Audio files (wav, mp3)      |
| `[youtube-transcription]` | YouTube URLs                |
| `[az-doc-intel]`          | Azure Document Intelligence |
| `[all]`                   | All of the above            |

## Options

```bash
-o OUTPUT      # Output file
-x EXTENSION   # Hint file extension (for stdin)
-m MIME_TYPE   # Hint MIME type
-c CHARSET     # Hint charset (e.g., UTF-8)
-d             # Use Azure Document Intelligence
-e ENDPOINT    # Document Intelligence endpoint
--use-plugins  # Enable 3rd-party plugins
--list-plugins # Show installed plugins
```

## Notes

- Use single quotes around `'markitdown[extra]'` to prevent shell interpretation of brackets
- Output preserves document structure: headings, tables, lists, links
- First run caches dependencies; subsequent runs are faster
