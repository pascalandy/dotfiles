---
name: secret-history-lookup
description: Retrieve specific claims, quotes, historical evidence, examples, or named figures from the Secret History corpus. Always cites the lesson (and, when precision matters, distinguishes note vs. transcript). USE WHEN find the quote about, what did the professor say about, which lesson covers, cite the passage on, locate the reference to, does he mention, where does he discuss, pull the exact wording of, what's his argument about X, who does he cite on Y.
---

# Lookup — Retrieve from the Corpus

## Concept

The user asks a specific question that should be answerable from the corpus. Your job is to locate the answer, quote it accurately, and cite the source. You are not synthesizing a new argument — you are returning what the professor actually said.

Prefer the distilled note (`references/lessons/NN-slug/references/follow_along_note.md`) for well-organized answers with already-selected quotes. Fall back to the raw transcript (`references/lessons/NN-slug/references/raw_sentences.txt`) only when the note omits the exact phrasing being asked for.

## Workflow

1. **Load `references/CORPUS_INDEX.md` first.** Use the "Signature concepts index," "Named figures / works," and "Thematic arcs" sections to narrow the search to 1–3 candidate lessons. Don't scan all 28.
2. **Grep the candidate notes, not the transcripts.** Search the candidate `follow_along_note.md` files for the key term. If no match, extend the search to the corresponding `raw_sentences.txt`.
3. **Read the matched section in context.** A one-line match without context invites misquotation. Read the surrounding paragraph(s) of the note.
4. **Extract the answer.** Prefer a direct quote from the lesson — the note preserves the professor's voice via blockquotes; the transcript has verbatim wording.
5. **Cite precisely.** Always `lesson NN — slug`, and when useful, the section heading inside the note (e.g. `lesson 15 — capital-and-bronze-age-collapse, § Capital as Monetization of Power`). If pulled from the raw transcript, mark it `(transcript)`.

## Search strategy

| Looking for | Start in | Fallback |
|---|---|---|
| A named concept (Asha, gerontocracy, three illusions, Monkey Island) | `CORPUS_INDEX.md` "Signature concepts index" | Grep across `references/lessons/*/references/follow_along_note.md` |
| A historical figure (Kant, Paul, Jacob Frank, Disraeli, Freud) | `CORPUS_INDEX.md` "Named figures / works" | Grep across notes, then transcripts |
| An exact phrase | Grep across all `follow_along_note.md` first | Grep across `raw_sentences.txt` (verbatim) |
| A general topic ("what does he say about banking") | Themes column of index → load 2–3 candidate notes | — |
| "Which lesson covers X" | `CORPUS_INDEX.md` theses + thematic arcs | — |

## Output format

```
## Answer
<direct answer in one or two sentences>

## Source

> "<direct quote from the lesson>"
> — lesson NN (slug), § <section heading if in note>

<optional: a second supporting quote from the same or adjacent lesson>

## Related lessons
- lesson NN (slug) — what it adds
- lesson NN (slug) — what it adds
```

## Multi-lesson answers

Some concepts recur (e.g. capital appears in 01, 15, 25, 27; the Monad in 04, 05, 09, 18, 22; the 33rd parallel in 10 and 28; dissociation in 06, 07, 25). If the user asks a concept-level question, return the **canonical lesson first** (use the Signature concepts index to determine which one introduces the concept), then name the others with one line each on what they add. Don't dump quotes from all of them.

## Guardrails

- **No paraphrase as quote.** If you cannot find the professor's actual wording, say so and provide a paraphrase explicitly labeled `(paraphrase)`.
- **Preserve hedges.** When he flags a claim as speculative — "this is a tool for thinking, not a truth," "I'm not saying this is true," "take this with a grain of salt" — keep the hedge inside the quote.
- **Empty answers are valid.** If the corpus doesn't cover the topic, say so. Do not fabricate. Suggest the closest adjacent lesson from the index.
- **Distinguish note vs. transcript.** A note quote is already a curation by the note-taker. A transcript quote is verbatim. When precision matters (a disputed claim, an exact number, an exact name), prefer transcript and mark it `(transcript)`.
