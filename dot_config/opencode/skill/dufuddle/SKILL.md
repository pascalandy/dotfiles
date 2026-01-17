---
name: dufuddle
description: "CLI wrapper for Defuddle to extract clean content and metadata (title, author, published date, word count) from any web page as Markdown. Use when you need to: (1) Scrape web page content as clean Markdown, (2) Extract article metadata (title, author, date), (3) Verify URL accessibility with dry-run, (4) Get structured JSON output from web pages."
---

# dufuddle

A CLI wrapper for [Defuddle](https://github.com/kepano/defuddle) that extracts clean content and metadata from any web page.

## Setup

Install dependencies in the scripts folder:

```bash
cd .opencode/skill/dufuddle/scripts && bun install
```

## Usage

```bash
bun run .opencode/skill/dufuddle/scripts/dufuddle.ts [options] <URL>
```

### Options

| Option           | Description                                     |
| ---------------- | ----------------------------------------------- |
| `--help`         | Show help message                               |
| `--dry-run`      | Verify URL is reachable without parsing content |
| `--content`      | Output only clean markdown content              |
| `--json`         | Output full result as JSON                      |
| `--timeout <ms>` | Set request timeout (default: 10000ms)          |

## Examples

### Extract article content as clean Markdown

```bash
bun run .opencode/skill/dufuddle/scripts/dufuddle.ts https://example.com/article
```

By default, outputs only the clean Markdown content (when piped to a file or non-TTY).

### Verify URL accessibility

```bash
bun run .opencode/skill/dufuddle/scripts/dufuddle.ts --dry-run https://example.com
```

### Get JSON output for programmatic use

```bash
bun run .opencode/skill/dufuddle/scripts/dufuddle.ts --json https://example.com/article | jq
```

### Set custom timeout

```bash
bun run .opencode/skill/dufuddle/scripts/dufuddle.ts --timeout 30000 https://slow-site.com
```

## Output Format

### Default Output (clean Markdown)

When running in a terminal (TTY), displays full output with title, content, and metadata. When piping to a file or non-TTY, outputs only the clean Markdown content:

```markdown
# Article Title

Article content in clean Markdown...
```

### Full Output (TTY mode only)

```
--- TITLE ---
Article Title

--- CONTENT (Markdown) ---
# Heading
Article content in clean Markdown...

--- METADATA ---
{
  "author": "Author Name",
  "published": "2025-01-01",
  "site": "Example Site",
  "wordCount": 1500,
  "domain": "example.com"
}
```

### JSON Output (--json)

```json
{
  "title": "Article Title",
  "content": "# Heading\nArticle content...",
  "author": "Author Name",
  "published": "2025-01-01",
  "site": "Example Site",
  "wordCount": 1500,
  "domain": "example.com"
}
```

## Bundled Resources

- `scripts/dufuddle.ts` - Main CLI script
- `scripts/package.json` - Dependencies (defuddle, jsdom)

## Best Practices

- Use `--dry-run` first to verify URL accessibility before full extraction
- Use `--content` for clean markdown exports to files
- Use `--json` when integrating with other tools or scripts
- Increase `--timeout` for slow-loading pages
- The tool uses a browser-like User-Agent to avoid blocking by some sites
