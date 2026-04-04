---
name: query
description: Search the wiki and synthesize answers with citations -- find relevant pages via the index, combine knowledge across pages, and optionally file answers back as new wiki pages. USE WHEN query wiki, search wiki, ask wiki, synthesize, deep query, what does the wiki say, find in wiki, compare, file answer, save answer, save as wiki page, compound answer.
---

## Customization

If the current assistant supports user-specific overrides, apply them before execution. Otherwise, use the defaults in this folder.

## Status Update

Before executing, emit a brief text status update such as:
`Running the **WorkflowName** workflow in the **Query** skill to ACTION...`

# Query

Search the wiki and synthesize answers from its accumulated knowledge. The LLM reads INDEX.md to find relevant pages, drills into them, and produces an answer with citations. Valuable answers can be filed back into the wiki so explorations compound alongside ingested sources.

## Core Concept

The wiki is not a search engine. It is a pre-synthesized knowledge base. When you query it, the LLM is reading structured, cross-referenced pages -- not re-deriving answers from raw chunks. The INDEX.md serves as the entry point: the LLM scans it to identify relevant pages, reads those pages, follows cross-references to related pages, and synthesizes across all of them.

Answers can take different forms depending on the question:
- A prose summary with citations
- A comparison table
- A timeline
- A list of contradictions or open questions

The key insight: **good answers are wiki-worthy.** A comparison you asked for, an analysis, a connection you discovered -- these should not disappear into chat history. File them back as wiki pages so they compound.

## When to Use

- **Finding information** -- "what does the wiki say about X?"
- **Synthesizing across pages** -- "compare A and B based on the wiki"
- **Deep analysis** -- "synthesize everything we know about X"
- **Preserving discoveries** -- "save that answer as a wiki page"

## Workflow Routing

Route to the appropriate workflow based on the request.

**When executing a workflow, output this notification directly:**

```
Running the **WorkflowName** workflow in the **Query** skill to ACTION...
```

- Find relevant pages for a topic -> `workflows/Search.md`
- Synthesize an answer across multiple pages -> `workflows/DeepQuery.md`
- Save an answer back into the wiki as a new page -> `workflows/FileAnswer.md`

## Query Process

```
INDEX.md ──> Scan for relevant pages
    |
    v
Read pages ──> Follow [[wikilinks]] to related pages
    |
    v
Synthesize ──> Combine knowledge, cite sources
    |
    v
Answer ──> Present to user (optionally file back)
```

## Citation Format

Always cite wiki pages in answers:

```markdown
Vitamin D deficiency correlates with poor sleep quality ([[vitamin-d-and-sleep]]),
though Dr. Jones disputes the mechanism ([[dr-jones-review]]).
```

## Principles

1. **Index-first navigation** -- always start from INDEX.md, not by scanning the filesystem
2. **Follow cross-references** -- if a page links to related pages, read those too
3. **Cite everything** -- every claim in an answer must reference the wiki page it came from
4. **Surface contradictions** -- if pages disagree, report both positions with citations
5. **Suggest filing** -- if an answer is substantive, suggest saving it as a wiki page
6. **Scope to the wiki** -- answer from wiki content, not from general knowledge. If the wiki lacks information, say so.
