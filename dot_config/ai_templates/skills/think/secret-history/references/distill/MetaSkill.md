---
name: secret-history-distill
description: Produce compact summaries of the Secret History corpus at a chosen resolution — one lesson, one thematic arc, or the whole course. USE WHEN summarize lesson N, tldr the course, digest the evil arc, compress the capital arc, the empire arc, the religion arc, high-level overview of the series, thematic summary of X, one-paragraph version of lesson Y, executive summary of the course.
---

# Distill — Summarize at Chosen Resolution

## Concept

Compression, not analysis. Take a chunk of the corpus at one of three resolutions and produce a faithful compact version. Preserve the professor's argument structure and key claims; drop the classroom asides, tangents, and repetitions.

## Three resolutions

| Resolution | Input | Output size |
|---|---|---|
| **Single lesson** | one `follow_along_note.md` | 1 paragraph thesis + bulleted claim spine + 2–4 key quotes |
| **Thematic arc** | 3–8 notes along an arc | 3–5 paragraphs tracing the argument through the arc, with lesson citations |
| **Whole course** | all 28 notes + `CORPUS_INDEX.md` | ~1 page: framework → historical build → synthesis. Hits every major lesson in one sentence. |

## Workflow

### Single-lesson distill

1. Load `references/lessons/NN-slug/references/follow_along_note.md`. The transcript is not needed for summarization.
2. Extract the Overview paragraph → your thesis.
3. Walk the `### Main Idea` / `#### Main Idea` headings → your claim spine.
4. Pick 2–4 blockquotes that best preserve the professor's voice on the load-bearing claims.
5. Write output in the template below.

### Thematic-arc distill

1. Identify the arc. The pre-built arcs in `references/CORPUS_INDEX.md` under "Thematic arcs" are canonical:
   - framework spine, contemporary decline, theory of evil, civilizational origins, ancient world & Homeric-Biblical, religion arc, capital arc, imperial arc, grand synthesis.
2. If the user's theme doesn't match a pre-built arc, construct one by filtering the "Signature concepts index" and thesis table in `CORPUS_INDEX.md`.
3. Load only the `follow_along_note.md` files for the arc's lessons.
4. Write the arc as a narrative: how the argument builds across the lessons. Cite each lesson as you bring it in.

### Whole-course distill

1. Read `references/CORPUS_INDEX.md` in full. It was built for this purpose.
2. Do not re-read all 28 notes for a full-course distill — the index has the thesis per lesson. Only load an individual note when you need to verify a specific claim.
3. Structure the distill by the professor's own meta-structure: framework first (01, 02, 09, 11), then mechanisms of Western decline (03, 07, 08), then civilizational origins (12–15), then ancient world and seed religions (16–22, 24), then the theory-of-evil / capital / faith / empire arc (04, 05, 06, 10, 23, 25, 26, 27), closing on synthesis (28).

## Output formats

### Single lesson

```
## Lesson NN — <Title>

**Thesis.** <one paragraph from the Overview, rewritten tighter>

**Claim spine:**
- <major claim 1>
- <major claim 2>
- <major claim 3>
- <major claim 4>

**Key quotes:**
> "<quote 1>"
> "<quote 2>"
> "<quote 3>"

**Context:** <one line on how this lesson connects to the broader course>
```

### Thematic arc

```
## Arc — <Arc name>
Lessons: NN, NN, NN, …

<3–5 paragraphs of narrative summary. Each major claim carries a (lesson NN) citation. End with a sentence on why the arc matters to the larger course.>
```

### Whole course

```
## The Secret History — Full Course Distill

**Framework** (lessons 01, 02, 09, 11). <paragraph>

**Diagnostic mechanisms of Western decline** (03, 07, 08). <paragraph>

**Civilizational origins** (12–15). <paragraph>

**Ancient world and the seed religions** (16–22, 24). <paragraph>

**The anatomy of evil** (04, 05, 06, 10, 23, 25, 26, 27). <paragraph>

**Synthesis** (28). <paragraph>

**Headline argument.** <one-sentence version of the entire course>
```

## Guardrails

- **No smoothing of hedges.** If the lesson flags something as speculative (especially 04, 06, 10, 19, 27, 28), the distilled version must also flag it.
- **No embellishment.** A distill is compression, not extrapolation. If a claim isn't in the note, it doesn't appear in the distill.
- **Preserve the professor's structure.** Don't reorder his argument into your own preferred order. The course's narrative order is load-bearing — lesson 04 sets up 05, 05 sets up 10, 22 sets up 23, 26 sets up 27, etc.
- **Don't substitute the index for the full course.** Use it to navigate and for whole-course-level structure, but the index's theses are one line each — you owe the user more than concatenating those lines for anything below whole-course resolution.
- **For whole-course distills, don't skip lesson 10.** It sits between the framework and the origins arc (it's one of two places the 33rd-parallel / revelation-of-method material appears; the other is 28) and shapes how the evil arc connects to modernity.
