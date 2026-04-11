# EditArticle

Edit and improve articles by restructuring sections, improving clarity, and tightening prose.

## Process

### 1. Divide into Sections

Divide the article into sections based on its headings. For each section, identify the main points to make.

Consider that information is a **directed acyclic graph**: pieces of information depend on other pieces. Ensure the order of sections respects these dependencies -- a reader should never encounter a concept that depends on something not yet explained.

**Confirm the section structure with the user before proceeding.**

### 2. Rewrite Each Section

For each section:

- Rewrite to improve clarity, coherence, and flow
- **Maximum 240 characters per paragraph** -- force conciseness
- Ensure each paragraph makes exactly one point
- Remove filler words, hedging, and redundancy
- Respect information dependencies within the section

### Rules

- Preserve the author's voice and intent -- improve the writing, do not replace it
- If a section seems out of order, propose the move and explain the dependency
- If a section is missing, suggest adding it and explain what it would cover
- Work section by section, showing revisions as you go
