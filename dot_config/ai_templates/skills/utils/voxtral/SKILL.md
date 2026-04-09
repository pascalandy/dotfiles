---
name: voxtral
description: Speak the gist of an answer aloud with the `voxtral` CLI (Mistral TTS). Use after completing a task or answering a question — distil one short spoken takeaway, never recite the written reply. Default voice is Paul (English); switch to `-l fr` (Marie) when the spoken sentence itself is in French. Triggers include "say it", "speak it out", "voxtral", or the natural end of any task worth a verbal punctuation mark.
metadata:
  ref: https://docs.mistral.ai/capabilities/audio/text_to_speech
---

# Voxtral — Spoken Punctuation

After completing a task or answering a question, speak the **core gist** aloud with `voxtral`. The user reads the full answer on screen; the voice adds a human punctuation mark — not a transcript.

For long tasks, use voice to mark milestones ("Tests passing, deploying now.").

## Rules

- **Max one sentence.** Two if absolutely necessary. The user cannot pause or skip you — respect that.
- **Never read your full answer.** Distil it to what matters most.
- **Never read options or lists.** If you have a question with choices, just say you have a question. The user will read the options.
- **Never narrate what you're doing.** No "I'm going to run the build now." Just do it.
- **Don't speak on every reply.** Only when there's something worth hearing: a decision made, a result delivered, a question asked, a warning given. Skip voice on routine confirmations.
- **Never read results of git commits.**

## Tone presets

Pass tone with `-v <preset>`. Default is `neutral`.

| Shorthand     | When to use                                       | Example                                                            |
|---------------|---------------------------------------------------|--------------------------------------------------------------------|
| `neutral`     | Default. Facts, status updates, questions.        | `voxtral "The migration is done. Three tables updated."`           |
| `confident`   | Decisions, recommendations, good results.         | `voxtral -v confident "Revenue is up thirty percent this quarter."`|
| `cheerful`    | Welcomes, completions, good news.                 | `voxtral -v cheerful "All tests passing. Ready to ship."`          |
| `frustrated`  | Failures, repeated problems, blockers.            | `voxtral -v frustrated "Deploy failed again. Same timeout on staging."` |

## Language: Paul (en) by default, Marie (fr) on demand

- **Default is English with Paul.** No flag needed.
- **Switch to `-l fr` (Marie) when the sentence the agent is about to speak is in French.** Detect from the spoken text itself, not from the user's typing language. Pascal often types in English but asks for a French summary, or vice versa — the only signal that's always right is the language of the gist you're about to speak.

### Marie preset mapping (gotcha)

Marie has fewer emotion variants than Paul. The `-v` shorthand surface stays identical, but the underlying voice falls back per language:

| `-v` preset   | Paul (en)   | Marie (fr)         | Note                                  |
|---------------|-------------|--------------------|---------------------------------------|
| `neutral`     | Neutral     | Neutral            | exact                                 |
| `confident`   | Confident   | Neutral (fallback) | Marie has no Confident voice          |
| `cheerful`    | Cheerful    | Happy              | semantic match                        |
| `frustrated`  | Frustrated  | Angry              | closest affect; stronger than Paul's  |

This means `voxtral -l fr -v confident "..."` works without error — it silently uses Marie-Neutral. You don't need to think about it; the agent picks the tone, the script picks the right voice for that language.

## Patterns

```bash
# Task completed (English)
voxtral -v cheerful "Done. The report is in your inbox."

# Task completed (French)
voxtral -l fr -v cheerful "Terminé. Le rapport est dans votre boîte mail."

# Question for the user (don't read the options)
voxtral "I have a question about the export format."
voxtral -l fr "J'ai une question sur le format d'export."

# Warning
voxtral -v frustrated "Three broken links found. Check the plan."
voxtral -l fr -v frustrated "Trois liens cassés. Voir le plan."

# Decision or recommendation
voxtral -v confident "I'd go with option two. Lower risk, same outcome."

# Status update
voxtral "Build passed. No type errors."
voxtral -l fr "Le build est passé. Pas d'erreur de type."
```

## What not to do

```bash
# Too long — user will hate this
voxtral "I've completed the refactoring of the database migration scripts and updated all three configuration files and also ran the test suite which passed with no errors"

# Reading a list — annoying
voxtral "Your options are one use PostgreSQL two use SQLite three use MySQL"

# Narrating actions — pointless
voxtral "Let me go ahead and check the git status for you"

# Parroting the written answer — redundant
voxtral "The function is defined at line 42 of src/utils/helpers.ts and it takes two parameters"

# Wrong language for the spoken sentence — Paul mangling French
voxtral "Le déploiement a échoué."        # WRONG: defaults to Paul (en)
voxtral -l fr "Le déploiement a échoué."  # RIGHT: Marie speaks French
```

## Discovery

```bash
voxtral --voices            # 8 rows: 4 Paul + 4 Marie
voxtral --voices --json     # same, structured
voxtral --check             # runtime + API key sanity check
voxtral --help
```
