# Session brief — distill meta-skill design

A self-contained summary of the design conversation that produced the `distill` plan. Read this to understand the proposal without needing to read the four companion docs first.

---

## 1. Starting point

The user has an existing skill, `transcript-sk`, that does this:

```
YouTube URL → yt-dlp (download audio) → Deepgram API (transcribe) → prompt.md (run via claude/codex) → distilled output
```

It supports three "prompts" today:
- `follow_along_note` — detailed notes
- `short_summary` — concise summary
- `summary_with_quotes` — summary with verbatim quotes

The script lives at `dot_config/ai_templates/skills/utils/transcript-sk/scripts/transcript.py`. Prompts live in `transcript-sk/scripts/prompts/`.

**The constraint:** the prompt library is locked inside `transcript-sk` and only reachable by going through YouTube → Deepgram first. There's no way to apply these prompts to a local text file or a web article.

---

## 2. What the user wants

1. **Generalize the workflow.** Any text — local file, web article, or YouTube video — should be processable through the same prompt library.
2. **Don't call it "summary".** The processing is more general than summarization. The chosen verb: **distill**.
3. **Prompts as a separate, growing library.** New distill styles should be addable without touching code.
4. **A new meta-skill.** Built using the `meta-skill-creator` pattern (router + sub-skills under a single entry point).
5. **Don't break `transcript-sk`.** It stays untouched. The new design delegates to it for the YouTube path.

---

## 3. Naming decisions

| Question | Decision |
|---|---|
| What to call the verb? | `distill` (rejected: summary, transform, render, reshape, process) |
| Split prompts into a separate skill? | Yes — `meta/distill-prompt` |
| What to call the processing meta-skill? | `meta/distill` |
| Where do file outputs go? | Beside the input file (not centralized) |
| Where do URL outputs go? | `~/Documents/_my_docs/62_distill_exports/` (matches `transcript-sk`'s `61_*` numbering convention) |
| Run folder name format? | `{slug}_{timestamp}_{prompt}/` (slug first, single underscores) |

---

## 4. Architecture in one picture

```
Two new meta-skills + one untouched existing skill:

dot_config/ai_templates/skills/
├── meta/
│   ├── distill/                    ★ NEW — the processor
│   │   ├── SKILL.md
│   │   ├── help.md                 ← rendered via glow on --help
│   │   ├── scripts/
│   │   │   └── distill.py          ← one script, three input types
│   │   └── references/
│   │       ├── ROUTER.md
│   │       ├── from-file/SKILL.md  ← docs view: local file workflow
│   │       ├── from-url/SKILL.md   ← docs view: web article workflow
│   │       └── from-media/SKILL.md ← docs view: YouTube workflow
│   │
│   └── distill-prompt/             ★ NEW — the prompt library
│       ├── SKILL.md
│       └── references/
│           ├── ROUTER.md
│           ├── follow-along-note/
│           │   ├── SKILL.md        ← when to use, expected output
│           │   └── prompt.md       ← canonical prompt text
│           ├── short-summary/
│           │   ├── SKILL.md
│           │   └── prompt.md
│           └── summary-with-quotes/
│               ├── SKILL.md
│               └── prompt.md
│
└── utils/
    └── transcript-sk/              UNCHANGED — still works standalone
        └── scripts/
            ├── transcript.py
            └── prompts/            (kept for now, may migrate later)
```

### Data flow

```
USER INPUT
    │
    ▼
distill <input> [flags]
    │
    ├── Auto-detect source type (or --source-type override)
    │      │
    │      ├── not http(s)://        → file
    │      ├── youtube.com / youtu.be → media
    │      └── any other URL         → article
    │
    ├── Lazy dependency check (only for the resolved type)
    │
    ├── ACQUIRE TEXT
    │      │
    │      ├── file:    read UTF-8 directly
    │      ├── article: shell out to `defuddle` → clean markdown
    │      └── media:   shell out to `transcript-sk/scripts/transcript.py --no-prompt` → raw transcript
    │
    ├── LOAD PROMPT (from meta/distill-prompt/references/<stem>/prompt.md)
    │
    ├── CALL LLM (claude or codex CLI, with effort ETL applied)
    │
    └── WRITE OUTPUT
           │
           ├── file input  → folder created BESIDE input file
           └── URL input   → folder created in ~/Documents/_my_docs/62_distill_exports/

Output folder: {slug}_{timestamp}_{prompt}/
Contents: {prompt}.md, source.txt, meta.txt, [extracted.txt if --keep-extracted]
```

---

## 5. The 10 architectural decisions

| # | Decision | Why |
|---|---|---|
| 1 | One unified script, three documentation sub-skills | All paths converge on the same final step. Three scripts = triplicated bug fixes. Three sub-skills = progressive disclosure for users. |
| 2 | Auto-detect input type, allow `--source-type` override | "Just paste the input and it works." Override exists for edge cases. |
| 3 | Lazy dependency checking | File-only users shouldn't need `defuddle` or Deepgram installed. |
| 4 | Media path delegates to existing `transcript-sk` | `transcript.py` already works. Don't reimplement Deepgram. |
| 5 | Article extraction via `defuddle` | Already in user's toolchain. Handles boilerplate, paywalls, JS. |
| 6 | Prompts as a separate meta-skill | Prompts grow independently. Other skills can reuse the library. |
| 7 | File output beside input; URL output centralized | Files have a "home" (their parent dir). URLs don't. Keeps related artifacts together. |
| 8 | `--effort` is canonical (`low/medium/high/max`); ETL inside script | One vocabulary. Vendor quirks (`med` vs `medium`, `max` vs `xhigh`) hidden. |
| 9 | `--help` renders `help.md` via `glow` (with plain fallback) | Argparse help is rigid. `help.md` is version-controlled markdown, rich and rendered. |
| 10 | Per coding-standards: PEP 723 + uv + ruff + pyright + lazy deps + distinct exit codes | User's standard Python conventions. |

---

## 6. CLI surface (summary)

```
distill <input> [--prompt STEM] [--source-type TYPE] [--provider PROVIDER]
                [--model MODEL] [--effort LEVEL] [--output-dir DIR]
                [--keep-extracted] [--no-open] [--dry-run] [--quiet]
distill --list-prompts
distill --list-models [--provider PROVIDER]
distill --help     ← renders meta/distill/help.md via glow
distill --version
```

### Defaults (everything you get with no flags)

| Setting | Default |
|---|---|
| Source type | `auto` |
| Prompt | `follow_along_note` |
| Provider | `claude` |
| Model (claude) | `claude-opus-4-6` |
| Model (codex) | `gpt-5.4` |
| Effort | `medium` |
| Output dir (file) | parent dir of input |
| Output dir (URL) | `~/Documents/_my_docs/62_distill_exports` |
| Run folder | `{slug}_{timestamp}_{prompt}/` |
| Open in Finder | yes (macOS) |
| Keep extracted | no |

### Effort ETL (canonical → vendor)

| Canonical | Claude | Codex |
|---|---|---|
| `low` | `low` | `low` |
| `medium` (default) | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 1 | Generic error |
| 2 | Invalid arguments |
| 3 | Input file not found / not readable |
| 4 | Unknown prompt stem |
| 5 | Provider CLI not found in PATH |
| 6 | LLM call failed |
| 7 | Output directory not writable |
| 8 | URL fetch failed |
| 9 | `defuddle` not found in PATH |
| 10 | `transcript.py` not found or failed |

### Example invocations

```bash
# Local file (output beside the file)
distill ~/Documents/article.md
distill --prompt short_summary ~/notes.txt

# Web article (defuddle, output to central exports)
distill https://example.com/blog/post

# YouTube video (transcript-sk delegation)
distill https://youtube.com/watch?v=2QpXab8z_Gw
distill --prompt summary_with_quotes https://youtube.com/...

# Override auto-detection
distill --source-type article https://youtube.com/watch?v=...

# Use codex with max effort
distill --provider codex --effort max ./meeting.md

# Discovery
distill --list-prompts
distill --list-models --provider claude

# Verify without running
distill --dry-run --prompt summary_with_quotes https://example.com/post
```

---

## 7. External dependencies

| Path | Required tools | Lazy-checked? |
|---|---|---|
| `file` | `claude` or `codex` CLI | always required |
| `article` | `defuddle` + provider CLI | only when source-type resolves to `article` |
| `media` | `transcript.py` (from transcript-sk) + Deepgram keyring + provider CLI | only when source-type resolves to `media` |
| `--help` | `glow` (optional, plain fallback) | only on `--help` |

A user who only ever distills local text files needs nothing beyond `claude` or `codex` in PATH.

---

## 8. Cross-skill relationships

```
meta/distill ──reads prompts from──▶ meta/distill-prompt
meta/distill (media path) ──delegates to──▶ utils/transcript-sk (unchanged)
meta/distill (article path) ──shells out to──▶ defuddle (external CLI)
meta/distill (--help) ──renders via──▶ glow (optional, plain fallback)
```

- `distill-prompt` has zero dependencies.
- `distill` depends on `distill-prompt`.
- `transcript-sk` stays standalone and unchanged.
- Future migration: `transcript-sk` could read prompts from `distill-prompt` to eliminate duplication. **Out of scope for this plan.**

---

## 9. What's deliberately NOT in scope

| Feature | Why deferred |
|---|---|
| Stdin / piped input | v1 takes file or URL only |
| Multiple inputs (`distill *.md`) | Single input only; shell loops handle batching |
| URL fetch caching | Premature optimization |
| Custom prompts via inline flag | Use the prompt library; add a folder |
| `--temperature` / `--max-tokens` | Provider CLIs handle these |
| Prompt chaining (multi-step distill) | Run distill twice if needed |
| Web UI / TUI | CLI only |
| MCP tool wrapping | CLI works in any harness today |
| Auto-detect for non-YouTube media hosts | YouTube only for v1; use `--source-type media` for others |
| Video title as media slug | Requires extra API call; video ID is faster + deterministic |
| Migrating `transcript-sk` to read from `distill-prompt` | Future cleanup |

---

## 10. Open questions (still pending review)

From `FLAGS.md`:

- (a) URL output dir `~/Documents/_my_docs/62_distill_exports` — agree?
- (b) Slug max length 60 chars — agree?
- (c) For media URLs, slug = video ID (fast, deterministic) vs video title (extra API call). Current choice: video ID.
- (d) Any flags missing? (e.g., `--max-tokens`, `--temperature`, `--no-source-copy`, `--timeout`)

---

## 11. Build order (when approved)

1. **Create `meta/distill-prompt/`**
   - Root `SKILL.md` + `references/ROUTER.md`
   - 3 prompt sub-folders, each with `SKILL.md` + `prompt.md`
   - Copy prompt text from `transcript-sk/scripts/prompts/*.md`

2. **Create `meta/distill/` skeleton**
   - Root `SKILL.md` + `help.md`
   - `references/ROUTER.md`
   - 3 sub-skill folders (`from-file`, `from-url`, `from-media`), each with `SKILL.md`

3. **Build `scripts/distill.py`**
   - PEP 723 inline metadata, `uv run` shebang
   - Argparse with `add_help=False` + custom `-h/--help` action
   - Auto-detection, lazy dependency checks, output location logic, effort ETL
   - Three acquisition paths converging on unified distill+output flow
   - Type hints, ruff/pyright clean

4. **Test** the matrix of input types × prompts × providers, including dry-run and override paths

5. **Apply via chezmoi**: `chezmoi apply -v`

---

## 12. Artifacts produced in this session

All files live in `docs/plans/1015-distill/`:

| File | Purpose | Audience |
|---|---|---|
| `PLAN.md` | The full implementation plan: structure, build order, acceptance criteria | Engineer building this |
| `FLAGS.md` | Machine-readable flag spec: every flag, validation rules, exit codes | Engineer building this |
| `HELP.md` | Final user-facing help text. Becomes `meta/distill/help.md` verbatim. Rendered by `glow` at runtime. | End user running `distill --help` |
| `ARCHITECTURE.md` | Design decisions with rationale + invariants to preserve | Future maintainer making changes |
| `BRIEF.md` (this file) | Self-contained session summary for review | External reviewer |

**Reading order for review:**
1. `BRIEF.md` (this doc) — full context
2. `HELP.md` — see exactly what the end user will see
3. `FLAGS.md` — verify the flag spec matches the help
4. `ARCHITECTURE.md` — understand why each decision was made
5. `PLAN.md` — see how it gets built

---

## 13. Things to push back on (review checklist)

If I were reviewing this plan, I'd specifically question:

- **Is "one script, three sub-skills" actually simpler than three scripts?** Yes per the rationale, but worth challenging — the sub-skills share zero code, so the "DRY" argument is purely about flag parsing and output writing. Is that enough payoff?
- **Is the alongside-output convention surprising for file inputs?** Some users expect a centralized export dir. Counter: `--output-dir` always overrides.
- **Is YouTube-only auto-detection too restrictive?** Vimeo, SoundCloud, podcast hosts are common. Counter: explicit `--source-type media` works; auto-detection list can grow.
- **Is glow-rendered help worth the implementation complexity?** It requires `add_help=False` + custom action + path resolution + fallback logic. Counter: it makes `help.md` version-controlled and rich.
- **Why 11 exit codes when most CLIs use 3?** Agent-friendly CLIs benefit from distinct codes per failure class. Counter: collapse 3, 4, 7 into "input/output errors" if simpler is better.
- **Should the effort ETL live in the script or in `transcript-sk`?** It currently lives in `distill.py` but `transcript-sk` could benefit from the same translation. Counter: `transcript-sk` is unchanged in this plan; future refactor.
- **Why is `distill-prompt` a meta-skill instead of just a folder of `.md` files?** Each prompt has room for `SKILL.md` (intent, sample output) + `prompt.md` (canonical text). Counter: maybe overkill for v1 with only 3 prompts.

---

## 14. TL;DR for the reviewer

> Build two new meta-skills: `meta/distill` (one script, three input types: file/article/YouTube, with auto-detection and override) and `meta/distill-prompt` (a growing library of prompts, each in its own folder). The script delegates the YouTube path to existing `transcript-sk` so it stays untouched. File inputs export beside the source file; URL inputs export to a central dir. Help is rendered via `glow` from a version-controlled `help.md`. Effort levels are canonical (`low/medium/high/max`) with internal ETL to vendor-specific values. Lazy dependency checks mean file-only users don't need `defuddle` or Deepgram installed.
>
> Five docs in `docs/plans/1015-distill/`: BRIEF (this), PLAN, FLAGS, HELP, ARCHITECTURE.
>
> Nothing has been built yet. This is design + spec only, awaiting review and approval.
