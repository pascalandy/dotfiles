# DeepQuery Workflow

Synthesize an answer across multiple wiki pages with full citations.

## When to Use

- Questions that span multiple pages
- "Synthesize everything we know about X"
- "Compare A and B based on the wiki"
- "What's the current understanding of X?"

## Steps

### 1. Find Relevant Pages

Follow the Search workflow (steps 1-3) to identify all relevant pages. Read each one.

### 2. Follow Cross-References

For each page read, check its `## Related` section and `[[wikilinks]]` in the body. If a linked page is relevant to the query, read it too. Continue until no new relevant pages are found (typically 1-2 hops).

### 3. Synthesize

Combine the knowledge from all pages into a coherent answer. Structure depends on the question type:

**Factual question** -- prose summary with inline citations:

```markdown
## {Question}

{Synthesized answer with [[page]] citations for each claim.}

### Sources
- [[page-1]] — {what it contributed}
- [[page-2]] — {what it contributed}
```

**Comparison** -- structured table:

```markdown
## Comparison: {A} vs {B}

| Dimension | {A} | {B} | Source |
|-----------|-----|-----|--------|
| {dim 1} | {value} | {value} | [[page]] |
| {dim 2} | {value} | {value} | [[page]] |
```

**Timeline** -- chronological:

```markdown
## Timeline: {Topic}

| Date | Event | Source |
|------|-------|--------|
| {date} | {event} | [[page]] |
```

### 4. Surface Contradictions

If pages disagree on a claim, report both positions:

```markdown
### Contradictions

- **{claim}**: [[page-a]] states {position A} (based on {evidence}).
  [[page-b]] states {position B} (based on {evidence}).
  No resolution in the wiki.
```

### 5. Identify Gaps

Note what the wiki does not cover that would help answer the question:

```markdown
### Gaps

- No page covers {missing topic}
- {Page} mentions {concept} but lacks detail
- No data on {specific dimension}
```

### 6. Suggest Filing

If the synthesized answer is substantive (more than a few sentences), suggest:

```
This answer synthesizes {N} pages. Want me to save it as a wiki page? (FileAnswer)
```

### 7. Log the Query

Append to LOG.md:

```markdown
- [[{today}]] query | {query-topic} | Synthesized from {N} pages, {contradictions} contradictions
```
