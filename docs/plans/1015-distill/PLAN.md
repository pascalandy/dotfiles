# Plan 1015 — distill + distill-prompt meta-skills

## Goal

Create two new meta-skills that generalize the existing `transcript-sk` workflow so any text — local file, web article, or video/audio URL — can be processed through a growing library of "distill" prompts.

- `meta/distill` — the processor. One unified script handles three input types.
- `meta/distill-prompt` — the prompt library. Each distill style is a folder; grows independently.

`transcript-sk` stays untouched. The media path delegates to it. May be decommissioned later.

## Why

- Today, processing prompts (`follow_along_note`, `short_summary`, `summary_with_quotes`) are locked inside `transcript-sk` and only reachable by going through YouTube → Deepgram first.
- We want to distill **arbitrary text** (local files and web articles) with the same prompt library.
- We want to add new distill styles without touching code.
- We want a single entry point that handles all input types intelligently.

## Cross-skill dependency

```
meta/distill ──reads prompts from──▶ meta/distill-prompt
meta/distill (media path) ──delegates to──▶ utils/transcript-sk (unchanged)
meta/distill (article path) ──shells out to──▶ defuddle (external CLI)
```

`distill-prompt` has zero dependencies. `distill` depends on `distill-prompt`. `transcript-sk` stays standalone.

---

## Meta-skill 1: `meta/distill-prompt/`

Prompt library. Each prompt is its own sub-skill folder so it can grow independently and be documented.

```
dot_config/ai_templates/skills/meta/distill-prompt/
├── SKILL.md                          # Collection: lists all distill prompts, how to add new ones
└── references/
    ├── ROUTER.md                     # prompt name (stem) → prompt folder
    ├── follow-along-note/
    │   ├── SKILL.md                  # When to use, expected output shape, sample
    │   └── prompt.md                 # Canonical prompt text
    ├── short-summary/
    │   ├── SKILL.md
    │   └── prompt.md
    └── summary-with-quotes/
        ├── SKILL.md
        └── prompt.md
```

### Conventions
- Folder name = prompt stem in kebab-case. Both `follow_along_note` and `follow-along-note` resolve to the same folder.
- `prompt.md` = the raw prompt text only. No frontmatter.
- `SKILL.md` = describes intent, when to use it, sample output shape.
- Adding a new distill style = drop a new folder + one row in `ROUTER.md`. No code changes.

### Initial content
Migrate (copy) the 3 existing prompts from `dot_config/ai_templates/skills/utils/transcript-sk/scripts/prompts/` into the new structure. `transcript-sk` keeps its own copy for now.

---

## Meta-skill 2: `meta/distill/`

The processor. **One unified script** handles all three input types. Sub-skills are documentation views, not separate code paths.

```
dot_config/ai_templates/skills/meta/distill/
├── SKILL.md                          # Collection: one entry, three input types
├── scripts/
│   └── distill.py                    # ★ Unified script (shared by all sub-skills)
└── references/
    ├── ROUTER.md                     # Routes by input type → docs sub-skill
    ├── from-file/
    │   └── SKILL.md                  # "distill a local text file"
    ├── from-url/
    │   └── SKILL.md                  # "distill a web article" (defuddle)
    └── from-media/
        └── SKILL.md                  # "distill a video/audio URL" (transcript-sk)
```

### Why one script, three sub-skills

- All three paths converge on the same final step: load prompt → call LLM → write output
- Only **input acquisition** differs (read file / fetch+clean / transcribe)
- One script = single source of truth for flag parsing, prompt loading, output writing
- Sub-skills exist for **documentation discoverability**: when a user asks "how do I distill a YouTube video", they get the media-specific doc with caveats and examples — not buried in a generic page

Script lives at `meta/distill/scripts/distill.py` (one level up from sub-skills) because all three share it.

### Routing logic (`distill/references/ROUTER.md`)

| Request pattern | Route to |
|---|---|
| file path, "distill <file>", local document | `from-file/SKILL.md` |
| article URL, blog post, web page | `from-url/SKILL.md` |
| YouTube URL, video link, audio URL | `from-media/SKILL.md` |

### Auto-detection in the script

| Input shape | Resolved type | Acquisition |
|---|---|---|
| not `http(s)://` | `file` | read UTF-8 directly |
| `http(s)://` + youtube.com / youtu.be / vimeo.com / known media host | `media` | shell out to `transcript-sk/scripts/transcript.py` (transcribe-only) |
| `http(s)://` + any other host | `article` | shell out to `defuddle` → clean markdown |

Override with `--source-type {auto,file,article,media}`.

### External dependency matrix

| Path | Required tools | Detected when |
|---|---|---|
| file | provider CLI (`claude` or `codex`) | always |
| article | `defuddle` in PATH + provider CLI | only when source-type resolves to `article` |
| media | `transcript.py` from `transcript-sk` + Deepgram keyring + provider CLI | only when source-type resolves to `media` |

Lazy checking — file-only users don't need defuddle or Deepgram installed.

### Invocation examples

```
distill ~/Documents/article.md                              → from-file, default prompt
distill follow_along_note ~/notes.txt                       → from-file + follow_along_note
distill short_summary ./meeting.md                          → from-file + short_summary
distill https://example.com/blog/post                       → from-url, default prompt (defuddle)
distill summary_with_quotes https://example.com/article     → from-url + summary_with_quotes
distill https://youtube.com/watch?v=...                     → from-media, default prompt
distill summary_with_quotes https://youtube.com/...         → from-media + summary_with_quotes
distill --list-prompts                                      → reads from distill-prompt
distill --source-type article https://youtu.be/xyz          → force article path on a media URL
```

---

## Build order

1. **Create `meta/distill-prompt/`**
   - Root `SKILL.md` (collection)
   - `references/ROUTER.md`
   - Three prompt sub-folders, each with `SKILL.md` + `prompt.md`
   - Copy prompt text from `transcript-sk/scripts/prompts/*.md`

2. **Create `meta/distill/` skeleton**
   - Root `SKILL.md` (collection) with invocation scenarios for all three input types
   - `references/ROUTER.md` with input-type routing table
   - `references/from-file/SKILL.md`
   - `references/from-url/SKILL.md`
   - `references/from-media/SKILL.md`

3. **Build `scripts/distill.py`** (per `FLAGS.md` and `ARCHITECTURE.md`)
   - PEP 723 inline metadata, `uv run` shebang
   - Argparse with all flags from `FLAGS.md`
   - Auto-detection of input type
   - Lazy dependency checking per path
   - Three acquisition paths converging on unified distill+output flow
   - Type hints, ruff/pyright clean

4. **Test paths**
   - `distill --list-prompts` → enumerates from `distill-prompt`
   - `distill --dry-run ~/some-file.md` → resolves all flags, prints plan
   - `distill ~/some-file.md` → file path
   - `distill https://some-blog.com/post` → article path (defuddle)
   - `distill https://youtube.com/...` → media path (transcript-sk delegation)
   - `distill --source-type article https://youtu.be/xyz` → override

5. **Apply via chezmoi**
   - `chezmoi apply -v` to sync to `~/.config/opencode/skill/meta/distill*`

---

## Acceptance criteria

- [ ] `meta/distill-prompt/` exists with 3 migrated prompts, each in its own sub-folder
- [ ] `meta/distill/` exists with `from-file`, `from-url`, `from-media` sub-skills + shared `scripts/distill.py`
- [ ] `distill.py` accepts file paths AND URLs, auto-detects input type
- [ ] `--source-type` flag overrides auto-detection
- [ ] `distill --list-prompts` lists all prompts from `distill-prompt`
- [ ] File path works without `defuddle` or Deepgram installed
- [ ] Article URL works via `defuddle`
- [ ] Media URL still works via `transcript-sk` delegation
- [ ] `transcript-sk` is unchanged and still works on its own
- [ ] All meta-skills follow the meta-skill-creator structure
- [ ] Script passes `ruff check` and `pyright`

---

## Open questions deferred

- Whether to eventually delete prompts from `transcript-sk/scripts/prompts/` and have `transcript-sk` read from `distill-prompt`. Out of scope.
- Stdin support for piped input. Deferred — file path or URL only for v1.
- Multiple inputs in one run (`distill *.md`). Deferred — single input for v1.
- Caching of fetched URLs / extracted text. Deferred.

---

## Companion documents

- `FLAGS.md` — complete CLI surface, every flag, exit codes, full `--help` text
- `ARCHITECTURE.md` — design decisions, why one script, dependency model
