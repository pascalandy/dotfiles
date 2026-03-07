---
name: util-fetch-in-md
description: >
  Fetch public web pages as clean Markdown with markdown.new through a single curl request. Use this whenever a user gives you a URL and wants the page fetched, summarized, analyzed, quoted, rendered in the terminal, or saved as Markdown—especially when they mention markdown.new, Cloudflare Markdown conversion, curl, jq, glow, or token efficiency. Prefer this over downloading raw HTML for single-page fetches.
compatibility: Requires curl and jq. glow is optional for terminal rendering.
---

# Fetch URL content in Markdown

## Goal

Use `https://markdown.new/` as the default way to turn a public web page into clean Markdown. It is lighter than fetching raw HTML and asking the agent to parse it afterward.

## When to use

Use this skill when:
- the user provides a public URL and wants the page content
- the user wants to analyze, summarize, quote, or inspect a webpage as Markdown
- the user wants to save a webpage as a `.md` file
- the user mentions `markdown.new`, Cloudflare Markdown conversion, `curl`, `jq`, `glow`, or token savings

Do not use this skill for:
- web search
- crawling many URLs
- authenticated pages that require login
- APIs that already return structured JSON

## Default workflow

1. Start with `method: "auto"`.
2. Keep the full JSON response for agent workflows. It includes metadata and `.content`.
3. If the result is empty, too short, truncated, or clearly misses client-rendered content, retry once with `method: "browser"`.
4. If the user needs images preserved or richer extraction, use `method: "ai"` with `retain_images: true`.
5. Do not fetch raw HTML first unless the user explicitly asks for HTML.
6. If `browser` fails, stop retrying and report the best available result.

## Core commands

### Agent-friendly JSON (`auto`)

```bash
curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://simonwillison.net/2026/Mar/5/chardet/",
    "method": "auto"
  }' | jq
```

### Retry with browser rendering

Use this only when the `auto` result looks incomplete.

```bash
curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://simonwillison.net/2026/Mar/5/chardet/",
    "method": "browser"
  }' | jq
```

### Keep images when they matter

```bash
curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://simonwillison.net/2026/Mar/5/chardet/",
    "method": "ai",
    "retain_images": true
  }' | jq
```

### Human-friendly terminal reading

```bash
curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://simonwillison.net/2026/Mar/5/chardet/",
    "method": "auto"
  }' | jq -r '.content' | glow
```

### Save the page as Markdown

```bash
curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d '{
    "url": "https://simonwillison.net/2026/Mar/5/chardet/",
    "method": "auto"
  }' | jq -r '.content' > article-chardet.md
```

## Safe scripting pattern

When the URL or method comes from variables, build the JSON body with `jq -nc` so shell quoting stays correct.

```bash
URL='https://simonwillison.net/2026/Mar/5/chardet/'
METHOD='auto'

curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg url "$URL" --arg method "$METHOD" '{url:$url, method:$method}')" | jq
```

With image retention:

```bash
URL='https://www.nasa.gov/image-of-the-day/'

curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg url "$URL" '{url:$url, method:"ai", retain_images:true}')" | jq
```

## Quick validation

Before you summarize a page, inspect a small preview:

```bash
curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg url 'https://example.com' '{url:$url, method:"auto"}')" | \
  jq '{title, method, content_length:(.content|length), preview:(.content|split("\n")[:20]|join("\n"))}'
```

This catches empty or obviously incomplete results early.

For scripts that should fail fast, prefer `jq -e`:

```bash
curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg url 'https://example.com' '{url:$url, method:"auto"}')" | \
  jq -e 'if .success == true and (.content | length) > 0 then {title, method, content_length:(.content|length)} else error(.error // "markdown.new returned no content") end'
```

## Output handling

- For agent workflows, keep the full JSON until you know you only need `.content`.
- To write Markdown to disk, use `jq -r '.content' > file.md`.
- For terminal reading, use `jq -r '.content' | glow`.
- If `glow` is unavailable, fall back to `jq -r '.content'`.
- If the Markdown is large and the user only needs an answer, summarize it instead of dumping the whole page into the conversation.

## Failure handling

- If `curl` exits non-zero, report the error clearly.
- If the JSON response includes an `.error` field, surface it.
- If `browser` rendering fails, explain that the page could not be rendered and continue with the best available `auto` or `ai` result.
- If the page is blocked, private, or heavily dynamic, say so and suggest one fallback method at most.
