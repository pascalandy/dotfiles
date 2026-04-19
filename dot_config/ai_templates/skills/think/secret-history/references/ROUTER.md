---
name: secret-history
description: Dispatch table for the secret-history meta-skill. USE WHEN applying the Secret History framework, analyzing current events with the professor's lens, looking up corpus claims or quotes, finding which lesson covers a topic, summarizing a lesson or thematic arc, distilling the course, or re-explaining concepts in the professor's voice (bank thought experiment, three illusions, Monkey Island, Asha, Gospel of Thomas, Paul's paterfamilias franchise, gerontocracy, meritocracy critique, bureaucratic rent-seeking, Sabbatean-Frankist, Pax Judaica, four eschatologies, 33rd parallel, Khazar theory).
---

# Secret History — Router

Before dispatching, load `CORPUS_INDEX.md` if the request names a lesson, theme, concept, or historical figure — the index resolves slugs and identifies which files the chosen sub-skill should load.

## Routing table

| Request pattern | Route to |
|---|---|
| analyze X through secret history, apply the framework to Y, what would the professor say about Z, secret history lens on, run this through the three-illusions lens, diagnose via gerontocracy / meritocracy / bureaucracy, evil-mechanics read on this, capital-extraction read on this, empire-vs-borderlands read on this | `lens/MetaSkill.md` |
| find the quote about, what did the professor say about, which lesson covers, cite the passage on, locate the reference to, does he mention, where does he discuss, pull the exact wording of, who does he cite on Y | `lookup/MetaSkill.md` |
| summarize lesson N, tldr the course, give me the evil arc, the capital arc, the empire arc, the religion arc, thematic summary of X, compress these lessons, high-level overview of the series, digest the whole course | `distill/MetaSkill.md` |
| explain like the professor, teach me X the way he teaches it, walk me through the bank thought experiment, onboard someone to Asha, re-explain the Monkey Island thought experiment, Paradise Lost breakdown, Priam and Achilles the way he tells it, Frank's pear garden story, pedagogical version of | `teach/MetaSkill.md` |

## Fallback

If intent is genuinely ambiguous, ask the user one short question to disambiguate:

> Do you want me to (a) apply the framework to something external, (b) find a specific claim in the corpus, (c) give you a summary, or (d) re-explain it in the professor's voice?

Do not default-route. Guessing wrong wastes corpus loading.
