---
name: great-books
description: Curated reference library of great-books lecture notes — each sub-skill holds the long-form follow-along note for one book or lecture. USE WHEN the user cites a great book by name or theme (Homer, Iliad, Odyssey, Aeneid, Virgil, Dante, Divine Comedy, Inferno, Plato, Kant, consciousness, noumena, Greek civilization, aretē, eudaimonia, Achilles, Patroclus, Priam, Odysseus, Penelope, Aeneas, Dido, Beatrice, archetypes, love, soul, reincarnation, poets as prophets, piety vs love, empire, trauma, homecoming, great books, predictive history, lecture notes on a book).
---

# Great Books

## Purpose

A library of detailed lecture notes on individual great books (and their themes) so that future conversations can pull in accurate, structured context on demand. Each sub-skill is **one lecture / one book focus**. Triggered when the user names the book, its author, or a distinctive theme (e.g. "what does the Aeneid say about piety", "remind me what Kant's noumena means in the consciousness lecture", "Dante's Inferno circle of lust notes").

Source for all notes: Predictive History, *Great Books* series (YouTube).

## What's Included

| # | Lecture focus | Sub-skill |
|---|---|---|
| 1 | Secrets of the Universe — consciousness, Kant, Plato's cave, soul | `01-secrets-of-the-universe/MetaSkill.md` |
| 2 | Homer and the Invention of the Human — Iliad, Achilles, archetypes | `02-homer-invention-of-the-human/MetaSkill.md` |
| 3 | Poets and Prophets — aretē, eudaimonia, Shelley, poetry | `03-poets-and-prophets/MetaSkill.md` |
| 4 | The Conscious Universe — Iliad conclusion, Priam, Shield of Achilles | `04-conscious-universe/MetaSkill.md` |
| 5 | The Odyssey — trauma, soul, journey home | `05-odyssey/MetaSkill.md` |
| 6 | The Intimacy of Love — Odyssey, Penelope, reunion | `06-intimacy-of-love/MetaSkill.md` |
| 7 | The Anti-Homer — Aeneid, Virgil, inversion of Homer | `07-antihomer/MetaSkill.md` |
| 8 | The Poetry of Empire — Aeneid conclusion, Dido, piety | `08-poetry-of-empire/MetaSkill.md` |
| 9 | Dante — Divine Comedy, Inferno, shadowed forest | `09-dante/MetaSkill.md` |

## Invocation Scenarios

| Trigger | What happens |
|---|---|
| "pull the notes on the Iliad lecture" | Router routes to `02-` or `04-` depending on whether the focus is introduction (Achilles/Homer) or conclusion (Priam/Shield) |
| "what did Virgil invert from Homer" | Routes to `07-antihomer/` |
| "Dante's view of Virgil as a guide" | Routes to `09-dante/` |
| "Penelope and the bow" | Routes to `06-intimacy-of-love/` |
| "Kant's noumena / phenomena" | Routes to `01-secrets-of-the-universe/` |

## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request, then load that sub-skill's `MetaSkill.md`. Each sub-skill's `MetaSkill.md` provides an overview and pointer to its full `references/follow_along_note.md`.

## Adding a new book

To add book #10+ (or any new lecture), replicate the pattern:

1. Create `references/NN-kebab-title/references/` under this skill.
2. Drop the follow-along note at `references/NN-kebab-title/references/follow_along_note.md`.
3. Author `references/NN-kebab-title/MetaSkill.md` with:
   - YAML frontmatter: `name`, `description` (the `description` ends with `USE WHEN …` listing distinctive keywords for that book).
   - An overview paragraph, 4–8 key themes, and a pointer line: `Full note: references/follow_along_note.md`.
4. Append one row to `references/ROUTER.md` mapping its keywords to `NN-kebab-title/MetaSkill.md`.
5. Append one row to the **What's Included** table above and, if useful, one row to **Invocation Scenarios**.
6. Merge the new keywords into this root `SKILL.md` `USE WHEN` list (so the scanner surfaces the collection on those triggers).

No other file needs to change.
