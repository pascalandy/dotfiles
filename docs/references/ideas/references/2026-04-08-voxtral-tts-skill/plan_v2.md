# Review: docs/plans/references/1019-voxtral/plan.md

## Context

The user asked for a review of the existing plan at `docs/plans/references/1019-voxtral/plan.md`, which proposes (1) extending `dot_local/bin/executable_voxtral.tmpl` to a bilingual CLI with a `-l/--lang` flag (en=Paul default, fr=Marie) and (2) creating a new skill at `dot_config/ai_templates/skills/utils/voxtral/SKILL.md`.

I verified the plan's assumptions against the current state of the CLI, the skills directory, and the deployment flow. This review reports what holds, what doesn't, and what needs a decision before execution.

## Verdict

**Approve with minor corrections.** The core design is sound and every structural claim about the current CLI holds. Three things need fixing or confirming before execution; none are blockers.

## What the plan gets right

- **Current CLI state, verified line-by-line against `dot_local/bin/executable_voxtral.tmpl`:**
  - `SCRIPT_VERSION="0.2.0"` today (line 5) — bump to 0.3.0 is appropriate.
  - The four Paul UUID constants exist (lines 102–105 in `fct_emit_voices`, also in `fct_voice_id` lines 136–139).
  - `fct_voice_id` currently takes one arg (line 134) — must become `fct_voice_id <lang_code> <preset>` as the plan says.
  - `fct_parse_arguments` handles `-v`, `--voices`, `--check`, `--json`, `--stdin`, `-o`, `-f`, `--format` (lines 144–199) — no `-l/--lang` exists.
  - `fct_emit_voices`, `fct_history_file_path` (lines 444–453), `--check`, `fct_usage` all exist as the plan claims.
- **Existing slug convention already aligns.** `fct_emit_voices` already prints slugs like `en_paul_neutral`, `en_paul_confident`, etc. (lines 93–96, 102–105). The original author clearly anticipated multi-language/multi-speaker — the plan's Marie additions land naturally on top of this existing scheme. Worth noting: the plan doesn't call this out, but it's a point in favor of the single-script approach over the rejected two-script alternative.
- **`LANG_CODE` naming** is the right call to avoid colliding with the shell `LANG` environment variable.
- **Single-script over two-script** rationale is correct: duplicating ~500 lines for 4 UUIDs is worse than one `case` branch.
- **Skill scope (~80–100 lines)** is well within the 500-line guidance at `dot_config/ai_templates/skills/utils/single-skill-creator/SKILL.md:26`.
- **Skill frontmatter convention** — other skills under `dot_config/ai_templates/skills/utils/` use `name` + `description`, with optional `metadata` (the `ref` URL field the plan proposes is consistent with `single-skill-creator`'s example).
- **Switch trigger rule** ("detect from the sentence the agent is about to speak, not the user's typing language") is the right call — Pascal routinely mixes languages in a single conversation.
- **Marie voice existence** confirmed in `doc.md`: Marie has 6 emotion variants, no Confident, no Frustrated — Happy/Angry/Neutral fallbacks are the honest mapping.

## Issues to fix before execution

### 1. Factually wrong statement about the `1019-voxtral` path (cosmetic, but fix it)

The plan says:

> The empty docs/plans/references/1019-voxtral file (zero bytes, named-like-a-dir but actually a file) is left alone — out of scope.

That was true at some point but is now stale: `docs/plans/references/1019-voxtral/` is a **directory** containing `plan.md` (this file), `doc.md`, and `draft.md`. Nothing needs to be deleted, but the paragraph should be removed from the plan so the execution step doesn't trip on it. Also: `draft.md` and `doc.md` now live inside `1019-voxtral/`, not directly under `docs/plans/references/`.

### 2. Verification `ls` path is wrong for Claude Code discovery (medium)

The plan's post-apply check is:

```bash
ls ~/.config/ai_templates/skills/utils/voxtral/SKILL.md
```

That path is the chezmoi-applied source tree. **Claude Code does not read from `~/.config/ai_templates/skills/`.** Skills are propagated by `.chezmoiscripts/run_after_backup.sh` (lines ~75–111), which copies from `~/.config/ai_templates/skills/` into the per-agent homes. The relevant destination for Claude Code is:

```bash
ls ~/.claude/skills/utils/voxtral/SKILL.md
```

Keep the `~/.config/…` check if you want to confirm the chezmoi source landed, but add the `~/.claude/skills/…` check as the real "Claude Code can see it" gate. Same note applies if the skill also needs to reach OpenCode / Codex / Pi / Amp / Factory / Gemini homes — `run_after_backup.sh` fans out to all of them.

### 3. History filename change is a breaking rename — say so explicitly

Current format (line 447–452):

```
YYYY_MM_DD_HHhMmsS_<dirname>_<preset>.<format>
```

Plan proposes:

```
…_<dirname>_<lang>_<speaker>_<preset>.<format>
```

This is fine, but old files at `/Users/andy16/Documents/_my_docs/63-voxtral/` won't match the new pattern and any grep/glob tooling the user has (if any) will miss them. Two options:

- **(a) Accept the break.** Old files remain searchable manually; new files follow the new scheme. Zero code to write.
- **(b) Keep the old format when lang=en to preserve backward compatibility**, and only add the lang/speaker segment when `LANG_CODE != "en"`. Uglier but strictly additive.

Plan currently implies (a) without saying so. Just name the choice in the plan.

## Open question for the user

The plan already flags the `confident → Marie Neutral` fallback as the only soft spot and proposes three options: (a) drop `confident` from French (error), (b) map to Marie-Curious, (c) silent fallback to Marie-Neutral (default).

Worth a user decision before execution. My weak preference is **(c) silent fallback** — the agent shouldn't have to context-switch on language when picking a tone preset, and Neutral is the safest "don't make things worse" choice. But this is a taste call.

## Files to modify (unchanged from the plan)

| File | Action |
|---|---|
| `dot_local/bin/executable_voxtral.tmpl` | Edit — add `-l/--lang`, `LANG_CODE` default, 4 Marie UUID constants, two-arg `fct_voice_id`, update `fct_emit_voices` / `fct_history_file_path` / `--check` / `fct_usage`, bump to v0.3.0 |
| `dot_config/ai_templates/skills/utils/voxtral/SKILL.md` | Create |

## Updated verification block (replaces the one in the plan)

```bash
# After: just cm-apply-verbose  (or chezmoi apply -v)

voxtral --version                                    # → voxtral v0.3.0
voxtral --check                                      # → status: ok, default_lang: en
voxtral --voices                                     # → 8 rows (4 Paul + 4 Marie)
voxtral --voices --json | jq 'length'                # → 8

# English (default, Paul)
voxtral "Build passed. No type errors."

# French (Marie - Neutral)
voxtral -l fr "Le build est passé. Pas d'erreur de type."

# French + cheerful (Marie - Happy)
voxtral -l fr -v cheerful "Tout est prêt."

# French + frustrated (Marie - Angry)
voxtral -l fr -v frustrated "Le déploiement a encore échoué."

# Invalid lang → friendly error
voxtral -l es "hola"                                 # → error: -l accepts en|fr

# History dir — filenames should now contain en_paul_* or fr_marie_*
ls -lt /Users/andy16/Documents/_my_docs/63-voxtral/ | head -5

# Skill landed in chezmoi source AND in Claude Code's discovery path
ls ~/.config/ai_templates/skills/utils/voxtral/SKILL.md   # chezmoi target
ls ~/.claude/skills/utils/voxtral/SKILL.md                # Claude Code reads from here
chezmoi managed | grep voxtral
```

## TL;DR

Plan is 95% ready. Three edits before execution:

1. Drop the stale "empty 1019-voxtral file" paragraph.
2. Fix the verification `ls` path to `~/.claude/skills/…` (or add it alongside the existing one).
3. State explicitly whether the history-filename rename is a clean break (recommended) or gated on `lang != en`.

Plus one decision from the user: how to handle `-l fr -v confident` (my pick: silent fallback to Marie-Neutral, as the plan already defaults to).
