# Search Workflow

Find relevant wiki pages for a topic and return a curated list with summaries.

## When to Use

- Quick lookup: "what pages cover X?"
- Orientation: "what do we have on topic Y?"
- Before a deep query: identify which pages are relevant

## Steps

### 1. Read INDEX.md

Read the wiki's INDEX.md to scan the page catalog. Identify pages whose name, description, or tags match the query topic.

### 2. Rank Relevance

For each candidate page, assess relevance:
- **Direct match** -- page is specifically about the query topic
- **Related** -- page mentions the topic or covers a related concept
- **Tangential** -- page touches the topic indirectly

### 3. Read Top Pages (Optional)

If the index descriptions are insufficient to judge relevance, read the top candidate pages to confirm they are relevant.

### 4. Present Results

```markdown
## Search Results: {query topic}

**Direct matches:**
- [[page-name]] — {description from INDEX.md}
- [[page-name-2]] — {description}

**Related:**
- [[related-page]] — {description, with note on how it connects}

**Tangential:**
- [[tangential-page]] — {brief note on the connection}

**Pages found:** {count} | **Wiki total:** {count from INDEX.md}
```

### 5. Suggest Next Steps

If the results warrant deeper synthesis:
- "Want me to synthesize across these pages? (DeepQuery)"
- "The wiki has no page specifically on {topic}. Want me to create one? (FileAnswer)"
