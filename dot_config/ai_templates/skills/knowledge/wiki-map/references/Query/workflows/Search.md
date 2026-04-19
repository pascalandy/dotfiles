# Search Workflow

Find relevant wiki pages for a topic and return a curated list with short summaries.

## When to Use

- Quick lookup: "what pages cover X?"
- Orientation: "what do we have on topic Y?"
- Before a deep query

## Steps

### 1. Orientation

- Read the meta-skill `references/SCHEMA.md`
- Read the wiki's `INDEX.md`
- Read the last 30 entries of `references/LOG.md`
- If `references/_meta/topic-map.md` exists, read it too
- Check for subdirectory drift against the recent log; note it, do not normalize it, and ask whether `INDEX.md` should reflect it if drift is detected

### 2. Rank Relevance

Identify candidate pages whose name, description, or tags match the query topic.

Use three buckets:
- direct match
- related
- tangential

### 3. Read Top Pages When Needed

If `INDEX.md` descriptions are not enough, read the strongest candidates to confirm relevance.

### 4. Present Results

```markdown
## Search Results: {query topic}

**Direct matches:**
- [[page-name]] -- {description}

**Related:**
- [[related-page]] -- {description and connection}

**Tangential:**
- [[tangential-page]] -- {brief note}

**Pages found:** {count} | **Wiki total:** {count from INDEX.md}
```

### 5. Suggest Next Steps

If the results warrant deeper synthesis:
- suggest `DeepQuery`
- if there is no dedicated page yet, suggest creating or filing one only if the result would be substantial
