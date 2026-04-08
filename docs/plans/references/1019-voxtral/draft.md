## Voice (Voxtral TTS)

After completing a task or answering a question, speak the core gist aloud using `voxtral`. This is not a transcript of your written answer — it's a short, spoken takeaway. The user reads the full answer on screen; the voice adds a human punctuation mark.

For a long task, it's a good idea to tell the user where we are in certain milestones.

### Rules

- **Max one sentence.** Two if absolutely necessary. The user cannot pause or skip you — respect that.
- **Never read your full answer.** Distill it to what matters most.
- **Never read options or lists.** If you have a question with choices, just say you have a question. The user will read the options.
- **Never narrate what you're doing.** No "I'm going to run the build now." Just do it.
- **Don't speak on every reply.** Only when there's something worth hearing: a decision made, a result delivered, a question asked, a warning given. Skip voice on routine confirmations.
- **Never read results of git commits.**

### Tone guide

| Shorthand | When to use | Example |
|-----------|------------|---------|
| `neutral` | Default. Facts, status updates, questions. | `voxtral "The migration is done. Three tables updated."` |
| `confident` | Decisions, recommendations, good results. | `voxtral -v confident "Revenue is up thirty percent this quarter."` |
| `cheerful` | Welcomes, completions, good news. | `voxtral -v cheerful "All tests passing. Ready to ship."` |
| `frustrated` | Failures, repeated problems, blockers. | `voxtral -v frustrated "Deploy failed again. Same timeout on staging."` |

### Patterns

```bash
# Task completed
voxtral -v cheerful "Done. The report is in your inbox."

# Question for the user (don't read the options)
voxtral "I have a question about the export format."

# Warning
voxtral -v frustrated "Three broken links found. Check the plan."

# Decision or recommendation
voxtral -v confident "I'd go with option two. Lower risk, same outcome."

# Status update
voxtral "Build passed. No type errors."
```

### What not to do

```bash
# Too long — user will hate this
voxtral "I've completed the refactoring of the database migration scripts and updated all three configuration files and also ran the test suite which passed with no errors"

# Reading a list — annoying
voxtral "Your options are one use PostgreSQL two use SQLite three use MySQL"

# Narrating actions — pointless
voxtral "Let me go ahead and check the git status for you"

# Parroting the written answer — redundant
voxtral "The function is defined at line 42 of src/utils/helpers.ts and it takes two parameters"
```