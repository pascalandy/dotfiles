---
name: util-fetch-in-markdown
description: >
  Fetch public web pages as clean Markdown through markdown.new using a single curl request, so the agent gets structured content instead of raw HTML. This leans on Cloudflare's native Markdown conversion path rather than making the agent parse the page itself. Use this whenever a user gives you a URL and wants the page fetched, summarized, analyzed, rendered in the terminal, or saved as Markdown—especially when token efficiency matters, when they mention markdown.new, Cloudflare markdown conversion, curl, jq, glow, or saving a page to a .md file. Prefer this over downloading full HTML for single-page fetches.
compatibility: Requires curl and jq. glow is optional for human-friendly terminal rendering.
---

# Fetch URL content in Markdown

## Goal

Use `https://markdown.new/` as the first choice for turning a public URL into clean Markdown. This keeps the workflow lightweight because the agent receives structured content directly, using Cloudflare's Markdown conversion path, instead of downloading raw HTML and trying to parse it afterward.

## When to use

Use this skill when:
- the user provides a public URL and wants the page content
- the user wants to analyze, summarize, quote, or inspect a webpage as Markdown
- the user wants to save a webpage as a `.md` file
- the user mentions `markdown.new`, Cloudflare markdown conversion, `curl`, `jq`, `glow`, or token savings

Do not use this skill for:
- generic web search
- site crawling across many URLs
- authenticated pages that require login
- APIs that already return structured JSON

## Working rules

1. Start with `method: "auto"`. It is the cheapest default and is often enough.
2. Keep the JSON response for agent workflows. It contains metadata plus `.content`.
3. If the result looks empty, suspiciously short, truncated, or misses client-rendered sections, retry with `method: "browser"`.
4. If the user wants images preserved, or richer extraction is needed, use `method: "ai"` with `retain_images: true`.
5. Do not fetch the raw HTML first unless the user explicitly asks for HTML. That defeats the token-saving goal.
6. If `browser` fails, do not loop forever. Report the failure and fall back to the best available `auto` or `ai` result based on the user's goal.

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

## Robust scripting pattern

When the URL or method comes from variables, build the JSON body with `jq -nc` so shell quoting stays safe.

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

## What to inspect before moving on

For agent workflows, check a small preview before summarizing the full page:

```bash
curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg url 'https://example.com' '{url:$url, method:"auto"}')" | \
  jq '{title, method, content_length:(.content|length), preview:(.content|split("\n")[:20]|join("\n"))}'
```

This helps catch empty or obviously incomplete responses early.

For scripts that should fail fast, prefer `jq -e`:

```bash
curl -fsSL 'https://markdown.new/' \
  -H 'Content-Type: application/json' \
  -d "$(jq -nc --arg url 'https://example.com' '{url:$url, method:"auto"}')" | \
  jq -e 'if .success == true and (.content | length) > 0 then {title, method, content_length:(.content|length)} else error(.error // "markdown.new returned no content") end'
```

## Output handling

- For agents, prefer keeping the full JSON until you know only `.content` is needed.
- For downstream Markdown files, use `jq -r '.content' > file.md`.
- For terminal reading, use `jq -r '.content' | glow`.
- If `glow` is unavailable, fall back to `jq -r '.content'` and read the raw Markdown.
- If the fetched Markdown is huge and the user only needs an answer, summarize after the fetch instead of dumping the entire page into the conversation.

## Failure handling

- If `curl` exits non-zero, surface the failure clearly.
- If the JSON response includes an `.error` field, report it instead of pretending the fetch succeeded.
- If `browser` rendering fails, explain that the service could not render the page and continue with the best available `auto` or `ai` output.
- If the target page is blocked, private, or heavily dynamic, say so and suggest another fetch method only once.
