   ╭───────────────────────────────────────────────────────────────────────────────────────╮
     │ Plan: Voxtral skill + bilingual CLI (Paul / Marie)                                    │
     │                                                                                       │
     │ Context                                                                               │
     │                                                                                       │
     │ The user wants to convert their draft Voxtral usage instructions                      │
     │ (docs/plans/references/draft.md) into a proper skill at                               │
     │ dot_config/ai_templates/skills/utils/voxtral/. The draft already worked               │
     │ fine in conversation — they're locking it in as a reusable skill so                   │
     │ every agent picks it up.                                                              │
     │                                                                                       │
     │ The new requirement: by default the agent speaks English using Paul,                  │
     │ but when it must speak French it should switch to Marie.                              │
     │                                                                                       │
     │ Constraint discovered while planning: the existing                                    │
     │ dot_local/bin/executable_voxtral.tmpl CLI only knows the four English                 │
     │ Paul UUIDs (neutral / confident / cheerful / frustrated). It has no                   │
     │ language flag and no Marie voice. So the skill alone cannot make French               │
     │ work — the CLI must be extended in the same change.                                   │
     │                                                                                       │
     │ A live GET /v1/audio/voices against the user's Mistral account                        │
     │ confirmed Marie exists with 6 emotion variants (no "Confident", no                    │
     │ "Frustrated" — closest matches will be used).                                         │
     │                                                                                       │
     │ Approach                                                                              │
     │                                                                                       │
     │ One change, two files:                                                                │
     │                                                                                       │
     │ 1. Extend dot_local/bin/executable_voxtral.tmpl with a -l/--lang                      │
     │ flag (en default → Paul, fr → Marie). Keep the four existing                          │
     │ tone presets (neutral / confident / cheerful / frustrated) and map                    │
     │ them per language. Bump version to 0.3.0.                                             │
     │ 2. Create dot_config/ai_templates/skills/utils/voxtral/SKILL.md                       │
     │ from the draft, adding the language-switching rule.                                   │
     │                                                                                       │
     │ Rejected alternative: two separate scripts (voxtral + voxtral-fr).                    │
     │ Would duplicate ~500 lines of bash for 4 UUIDs. One script with a -l                  │
     │ flag is simpler, keeps the history dir unified, and lets the skill stay               │
     │ small ("add -l fr when speaking French").                                             │
     │                                                                                       │
     │ Marie voice mapping                                                                   │
     │                                                                                       │
     │ Preset (shorthand): neutral                                                           │
     │ Paul (en, current): Paul - Neutral c69964a6-…                                         │
     │ Marie (fr, new): Marie - Neutral 5a271406-039d-46fe-835b-fbbb00eaf08d                 │
     │ Notes: exact                                                                          │
     │ ────────────────────────────────────────                                              │
     │ Preset (shorthand): confident                                                         │
     │ Paul (en, current): Paul - Confident 98559b22-…                                       │
     │ Marie (fr, new): Marie - Neutral 5a271406-039d-46fe-835b-fbbb00eaf08d                 │
     │ Notes: fallback — Marie has no Confident voice; Neutral is the safest stand-in        │
     │ ────────────────────────────────────────                                              │
     │ Preset (shorthand): cheerful                                                          │
     │ Paul (en, current): Paul - Cheerful 01d985cd-…                                        │
     │ Marie (fr, new): Marie - Happy 49d024dd-981b-4462-bb17-74d381eb8fd7                   │
     │ Notes: semantic match                                                                 │
     │ ────────────────────────────────────────                                              │
     │ Preset (shorthand): frustrated                                                        │
     │ Paul (en, current): Paul - Frustrated 1f017bcb-…                                      │
     │ Marie (fr, new): Marie - Angry a7c07cdc-1c35-4d87-a938-c610a654f600                   │
     │ Notes: closest affect; stronger than Paul's Frustrated                                │
     │                                                                                       │
     │ The four-preset surface stays identical so the draft tone guide still                 │
     │ works. The language flag is orthogonal: agent picks the preset by                     │
     │ tone, picks the language by what it's about to say.                                   │
     │                                                                                       │
     │ Switch trigger (skill instruction)                                                    │
     │                                                                                       │
     │ Recommended: match the language of the sentence the agent is about                    │
     │ to speak — not the user's typing language.                                            │
     │                                                                                       │
     │ Why: Pascal often writes in English but might ask for a French summary,               │
     │ or vice-versa. Detecting from the spoken text is the only signal that's               │
     │ always right. The agent already knows what it's about to say, so this is              │
     │ free.                                                                                 │
     │                                                                                       │
     │ Default = English/Paul. Switch to -l fr only when the gist itself is                  │
     │ in French.                                                                            │
     │                                                                                       │
     │ File 1 — CLI extension                                                                │
     │                                                                                       │
     │ /Users/andy16/.local/share/chezmoi/dot_local/bin/executable_voxtral.tmpl              │
     │                                                                                       │
     │ Changes:                                                                              │
     │                                                                                       │
     │ - SCRIPT_VERSION → 0.3.0                                                              │
     │ - Add global LANG_CODE="en" default (avoid clashing with the                          │
     │ environment LANG variable)                                                            │
     │ - New 4 Marie UUID constants alongside the existing Paul ones                         │
     │ - Replace fct_voice_id <preset> with                                                  │
     │ fct_voice_id <lang_code> <preset> — case-of-case lookup                               │
     │ - Add -l|--lang parsing in fct_parse_arguments; accept en|fr                          │
     │ - Validation: reject any --lang other than en or fr                                   │
     │ - fct_emit_voices lists both Paul and Marie sets (tab-aligned and                     │
     │ in --json mode)                                                                       │
     │ - fct_history_file_path includes lang in the filename                                 │
     │ (..._en_paul_neutral.mp3 / ..._fr_marie_neutral.mp3)                                  │
     │ - --check JSON adds default_lang field                                                │
     │ - fct_usage documents -l with one example per language                                │
     │                                                                                       │
     │ File 2 — New skill                                                                    │
     │                                                                                       │
     │ /Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/utils/voxtral/SKILL │
     │ .md                                                                                   │
     │                                                                                       │
     │ Structure (one file, ~80–100 lines, well under the 500-line guidance                  │
     │ from single-skill-creator):                                                           │
     │                                                                                       │
     │ - Frontmatter                                                                         │
     │   - name: voxtral                                                                     │
     │   - description: short imperative sentence + explicit triggers                        │
     │ ("after completing a task or answering a question, speak the gist                     │
     │ aloud", "switch to Marie when the spoken sentence is in French")                      │
     │   - metadata.ref: Mistral TTS docs URL                                                │
     │ - Core rules (verbatim from draft.md): max one sentence, never read                   │
     │ the full answer, never read options/lists, never narrate, don't speak                 │
     │ on every reply, never read git commit results                                         │
     │ - Tone guide table (the 4 presets — same as draft)                                    │
     │ - Language section (NEW):                                                             │
     │   - Default = English / Paul. No flag needed.                                         │
     │   - Switch to -l fr (Marie) when the sentence the agent is about to                   │
     │ speak is in French. Detect from the spoken text, not the user's                       │
     │ typing language.                                                                      │
     │   - Mention the Marie preset mapping caveat:                                          │
     │ cheerful → Happy, frustrated → Angry, confident → Neutral fallback.                   │
     │ - Patterns — examples for both languages                                              │
     │ - What not to do (verbatim from draft)                                                │
     │                                                                                       │
     │ Files                                                                                 │
     │                                                                                       │
     │ ┌───────────────────────────────────────────────────────┬──────────────────────────── │
     │ ────┐                                                                                 │
     │ │                         File                          │             Action          │
     │     │                                                                                 │
     │ ├───────────────────────────────────────────────────────┼──────────────────────────── │
     │ ────┤                                                                                 │
     │ │ dot_local/bin/executable_voxtral.tmpl                 │ edit (extend with           │
     │ -l/--lang,   │                                                                        │
     │ │                                                       │ bump to v0.3.0)             │
     │     │                                                                                 │
     │ ├───────────────────────────────────────────────────────┼──────────────────────────── │
     │ ────┤                                                                                 │
     │ │ dot_config/ai_templates/skills/utils/voxtral/SKILL.md │ create                      │
     │     │                                                                                 │
     │ └───────────────────────────────────────────────────────┴──────────────────────────── │
     │ ────┘                                                                                 │
     │                                                                                       │
     │ The empty docs/plans/references/1019-voxtral file (zero bytes,                        │
     │ named-like-a-dir but actually a file) is left alone — out of scope.                   │
     │ docs/plans/references/draft.md and docs/plans/references/doc.md                       │
     │ also stay; the skill consumes the draft but doesn't need to delete it.                │
     │                                                                                       │
     │ Verification                                                                          │
     │                                                                                       │
     │ After chezmoi apply -v:                                                               │
     │                                                                                       │
     │ voxtral --version                                    # → voxtral v0.3.0               │
     │ voxtral --check                                      # → status: ok, default_lang: en │
     │ voxtral --voices                                     # → 8 rows (4 Paul + 4 Marie)    │
     │ voxtral --voices --json | jq '. | length'            # → 8                            │
     │                                                                                       │
     │ # English (default, Paul)                                                             │
     │ voxtral "Build passed. No type errors."                                               │
     │                                                                                       │
     │ # French (Marie - Neutral)                                                            │
     │ voxtral -l fr "Le build est passé. Pas d'erreur de type."                             │
     │                                                                                       │
     │ # French + cheerful (Marie - Happy)                                                   │
     │ voxtral -l fr -v cheerful "Tout est prêt."                                            │
     │                                                                                       │
     │ # French + frustrated (Marie - Angry)                                                 │
     │ voxtral -l fr -v frustrated "Le déploiement a encore échoué."                         │
     │                                                                                       │
     │ # Invalid lang → friendly error                                                       │
     │ voxtral -l es "hola"                                 # → error: -l accepts en|fr      │
     │                                                                                       │
     │ History dir check:                                                                    │
     │                                                                                       │
     │ ls -lt /Users/andy16/Documents/_my_docs/63-voxtral/ | head -5                         │
     │ # Filenames should now contain en_paul_* or fr_marie_*                                │
     │                                                                                       │
     │ Skill discovery check (Claude Code reads                                              │
     │ ~/.config/ai_templates/skills/... after chezmoi apply):                               │
     │                                                                                       │
     │ ls ~/.config/ai_templates/skills/utils/voxtral/SKILL.md                               │
     │ chezmoi managed | grep voxtral                                                        │
     │                                                                                       │
     │ Open question for confirmation                                                        │
     │                                                                                       │
     │ The Marie confident → Neutral fallback is the only soft spot. If                      │
     │ you'd rather, I can either (a) drop confident from the French preset                  │
     │ list entirely (so voxtral -l fr -v confident errors out), or (b) map                  │
     │ it to Marie - Curious instead of Marie - Neutral. Default plan is                     │
     │ (c) silent fallback to Neutral so the agent never has to think about it.              │
     ╰───────────────────────────────────────────────────────────────────────────────────────╯