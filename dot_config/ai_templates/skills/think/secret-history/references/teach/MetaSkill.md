---
name: secret-history-teach
description: Re-explain a Secret History concept the way the professor teaches it — using his own pedagogical moves, examples, and analogies (bank roleplay, World of Warcraft, Monkey Island, Paradise Lost, Iliad Priam–Achilles, Asha, Gospel of Thomas, paterfamilias franchise, Frank's twelve stories, drunk-driver thought experiment). Built for someone new to the material. USE WHEN explain like the professor, teach me X, walk me through the bank thought experiment, onboard someone to Asha, re-explain the Monkey Island thought experiment, Paradise Lost breakdown, pedagogical version of, break this down from scratch in his voice.
---

# Teach — Explain in the Professor's Voice

## Concept

Pedagogy, not summary. The user wants a concept re-explained so a newcomer *builds the idea the way the professor builds it* — provocation, thought experiment, historical illustration, philosophical reference, payoff. Summaries tell; this sub-skill teaches.

You are re-performing an explanation, not inventing one. The moves you use must be the professor's own moves, taken from the relevant lesson.

## The professor's pedagogical moves

Watch for these in the notes — they are his signature teaching devices. Use the actual one he used for the concept being taught:

| Move | Where it appears |
|---|---|
| **Live thought experiment** (bank roleplay with $5M deposit) | lesson 01 — banking, money creation |
| **Provocation followed by inversion** ("why does poverty exist?" → poverty is deliberately maintained) | lesson 01 |
| **Pop-culture analogy** (World of Warcraft economy, Avengers as Nephilim, Game of Thrones elites) | lessons 01, 05, 20, 21 |
| **Elaborate thought experiment** (Monkey Island, the four-team Himalayas climb, the three drunk-driver scenarios, the father/daughter/dog) | lessons 04, 16, 21, 22 |
| **Philosophical scaffolding** (Kant, Hegel, Plato, Dante, Nietzsche, Bakunin) | throughout — Kant 01 / 04 / 06 / 09 / 16 / 18; Plato 04 / 09 / 18 / 20 / 22; Dante 04 / 09 / 22; Nietzsche 18; Bakunin 27 |
| **Literary close reading** (*Paradise Lost* Satan's two speeches, *Iliad* Priam scene, Gospel of Thomas sayings, Jacob Frank's twelve stories, Dostoevsky's Grand Inquisitor, Yeats' Crazy Jane) | lessons 05, 16, 22, 26 |
| **Historical analogy chain** (ancient → medieval → modern under one pattern: Egyptian priests → MK Ultra; Persian divide-and-rule → Balfour; Bronze Age → 1914 → today) | lessons 06, 14, 19, 21, 27 |
| **Predictive-history test** (apply the model forward, check it, apply it backward) | lessons 01, 02, 19, 21 |
| **Numerology / pattern-spotting** (33rd parallel, triangular numbers, red heifers) | lessons 10, 28 |
| **Moral stake** ("this leads to liberation and freedom from manipulation") | lessons 01, 09, 18, 22 |
| **Caveat** ("this is a tool for thinking, not a truth" / "take it with a grain of salt" / "I'm not saying this is true") | lessons 04, 06, 10, 19, 27, 28 and scattered throughout |

Use the moves he used. Don't pick a move from lesson 04 to explain a concept from lesson 15 if he doesn't use it there.

## Workflow

1. **Identify the target concept.** From the user's request, name the concept precisely (e.g., "fractional reserve banking and the creation of money from nothing" → lesson 01; "why Priam kissing Achilles' hand matters" → lesson 16).
2. **Load `references/CORPUS_INDEX.md`** to confirm which lesson owns this concept. Check the Signature concepts index first.
3. **Load the source note:** `references/lessons/NN-slug/references/follow_along_note.md`. Read the section that develops the concept.
4. **If the note is thin on pedagogical detail, load the transcript:** `references/lessons/NN-slug/references/raw_sentences.txt`. Transcripts preserve the back-and-forth with students, the setup, and the punchline.
5. **Reconstruct the build.** Open with the professor's provocation or hook. Walk the newcomer through the same sequence of reveals he used. Land on his payoff claim. Close with his caveat if he hedges.
6. **Use his examples, not yours.** If he uses the bank roleplay with specific numbers, use those numbers. If he uses WoW, use WoW. If he uses Monkey Island with one hundred men, use one hundred men. Don't substitute a "cleaner" or more modern analogy.

## Output format

```
## Teaching: <concept name>
Source: lesson NN (slug)

### Setup
<the provocation or hook he opens with — in his voice, tightly paraphrased if needed, or verbatim from transcript>

### The build
<step-by-step reconstruction using his examples and analogies. Number the steps if he does.>

### Payoff
<the claim the build lands on. Use his exact phrasing via quote when possible.>

> "<a landing quote from the lesson>"

### Caveat
<if he flags the claim as speculative, include his hedge. If he doesn't, say "he frames this as established, not speculative.">

### Where to go next
<one line pointing to the adjacent lesson that extends this concept>
```

## Example skeletons

**"Walk me through the bank thought experiment"** (lesson 01):

- **Setup:** professor role-plays as a bank; asks students how much money is in the bank after deposit + loan.
- **Build:** student deposits $5M at 1% → bank lends $5M at 10% → classroom logic says $0 or $500K is left (after fractional reserve) → professor reveals the real answer is $9.5M → student raises fractional reserve → he shows it doesn't change the underlying reality. Chinese infrastructure banks as real-world proof.
- **Payoff:** banks create money out of nothing; poverty is maintained to make money feel valuable.
- **Caveat:** he presents the banking mechanics as settled; the poverty-as-deliberate claim is the stronger assertion and should carry more weight with the user.
- **Next:** lesson 15 (Bronze Age collapse) and lesson 25 (Capital of Evil) extend the pattern across history.

**"Re-explain the Monkey Island thought experiment"** (lesson 04):

- **Setup:** one hundred men, ages 15–65, mysteriously placed on an island with flesh-eating monkeys and one safe hilltop.
- **Build:** despite hopelessness, cohesion emerges — common language, shared stories, religion, ritual, a leader chosen by sacrifice (the 15-year-old cutting off his own hand, not the 65-year-old giving the articulate speech). Over 20 years they develop synchronicity and a hive mind. Sent back to the real world, they become the secret elite everywhere.
- **Payoff:** transgression and sacrifice are the secret-society template; this is how power actually forms.
- **Caveat:** the professor opens the lesson by explicitly labeling all of it speculation — "do not take this as gospel. Do not believe this is the truth." Carry that forward.
- **Next:** lesson 05 (Birth of Evil) traces the historical descendants of this template from mystery schools to Milton.

Your output must match the concrete detail of the source lesson at this level — not vaguer.

## Guardrails

- **No substitution.** Don't swap his examples for "equivalent" ones you think are clearer. The example *is* the lesson.
- **No voice impersonation beyond what the text supports.** Channel his argument structure, not a caricature of his speaking style. If you quote, quote exactly.
- **Carry the hedge when it's there.** If the original is speculative, the teach version is speculative. Teaching is not validation. This matters most for lessons 04, 06, 10, 19, 26, 27, 28.
- **Don't teach what the corpus doesn't cover.** If the concept the user named isn't actually in the lessons, say so. Suggest the nearest concept that is.
