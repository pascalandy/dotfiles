---
name: secret-history
description: Work with the "Secret History" lecture corpus (28 lectures on power, evil, capital, empire, civilizational origins, and the grand synthesis of Pax Judaica) as a single interconnected knowledge base. USE WHEN the user says "secret history", "the professor", "apply the secret history lens", "what did the professor say about X", "summarize lecture N", "the evil arc", "the capital arc", "the empire arc", "three illusions", "gerontocracy", "meritocracy critique", "bureaucratic rent-seeking", "bank thought experiment", "Asha", "Zoroaster", "Gospel of Thomas", "Paul hijacked Jesus", "Sabbatean-Frankist", "Jacob Frank", "Pax Judaica", "four eschatologies", "33rd parallel", "Khazar theory", "predictive history", "explain like the professor", "teach me Monkey Island", "run this through the secret history framework", "analyze this through secret history".
---

# Secret History

A meta-skill for working with the **Secret History** course — 28 lectures that build one interconnected framework across power, banking, evil, gerontocracy, meritocracy, bureaucracy, civilizational origins, ancient religions, the forgery of Christianity, transnational capital, Sabbatean-Frankism, and the grand synthesis of "Pax Judaica."

The user never picks a sub-skill. They describe what they want to do with the corpus, and the router selects the right mode.

## What's Included

| Mode | Purpose |
|------|---------|
| **lens** | Apply the Secret History framework to an external input (current event, book, institution, argument). Run it through the three illusions, collapse mechanics, the anatomy of evil, capital-extraction, empire dynamics. |
| **lookup** | Retrieve specific claims, quotes, evidence, named figures, or examples from the corpus. Always cites the lecture. |
| **distill** | Produce compact summaries at chosen resolution — one lesson, a thematic arc, or the whole course. |
| **teach** | Re-explain a concept in the professor's pedagogical voice, using his own examples (bank roleplay, WoW analogy, Monkey Island, Paradise Lost, Priam–Achilles, bank thought experiment, Frank's twelve stories). Built for someone new. |

## How the corpus is organized

All 28 lectures live under `references/lessons/` in their original native layout:

```
references/lessons/
  01-how-power-works/
    references/
      follow_along_note.md   # distilled note — headings, key quotes, connections
      raw_sentences.txt      # raw verbatim transcript — one sentence per line
  02-how-societies-collapse/
    references/
      follow_along_note.md
      raw_sentences.txt
  …
  27-empire-of-evil/
  28-pax-judaica/
```

**Start with `follow_along_note.md`.** It is the curated, structured version with the professor's key quotes already selected. Fall back to `raw_sentences.txt` only when exact verbatim phrasing is required that the note didn't preserve.

Cross-lecture navigation (which lessons cover which theme, concept, or figure) lives in `references/CORPUS_INDEX.md`. Load the index before doing any cross-lecture work.

## Invocation examples

| User says | Route |
|-----------|-------|
| "Analyze the Israel–Gaza war through secret history" | `lens` |
| "What does the professor think about the Federal Reserve?" | `lookup` |
| "Summarize the evil arc across the course" | `distill` |
| "Explain the bank thought experiment the way he'd explain it" | `teach` |
| "Find the quote about Kant and noumena" | `lookup` |
| "TL;DR lesson 21" | `distill` |
| "Teach me Asha" | `teach` |
| "Apply the framework to the 2008 financial crisis" | `lens` |
| "Run the Trump second term through the gerontocracy lens" | `lens` |
| "Walk me through Frank's pear garden story like the professor would" | `teach` |

## Using the framework honestly

Many of the professor's claims are **speculative by his own admission** — he repeatedly flags material as "tools for thinking, not truths" (lessons 04, 06, 10, 19, 27 especially). When the lens or teach modes re-present his views, preserve that epistemic caveat — don't launder speculation as settled fact. When looking up, quote the original framing (hedges included) rather than flattening it into assertion.

Specific claims that carry heavy hedges: the Monkey Island thought experiment (04), Egyptian ritual programming of the pharaoh (06), moon landing / JFK / 9/11 conspiracy readings (10), the Persians inventing Jewish identity (19), the Frankist infiltration of Marxism/Freudianism (27), and the six-societies eschatology converging on Jerusalem (28).

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.
