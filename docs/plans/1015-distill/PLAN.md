# Plan 1015 — distill + distill-prompt meta-skills

## Goal

Create two new meta-skills that generalize the existing `transcript-sk` workflow so any text — local file, web article, or YouTube video — can be processed through a growing library of "distill" prompts.

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
meta/distill (--help) ──renders via──▶ glow (optional, plain fallback)
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
├── help.md                           # ★ Rendered by --help via glow
├── scripts/
│   └── distill.py                    # ★ Unified script (shared by all sub-skills)
└── references/
    ├── ROUTER.md                     # Routes by input type → docs sub-skill
    ├── from-file/
    │   └── SKILL.md                  # "distill a local text file"
    ├── from-url/
    │   └── SKILL.md                  # "distill a web article" (defuddle)
    └── from-media/
        └── SKILL.md                  # "distill a YouTube video" (transcript-sk)
```

### Why one script, three sub-skills

- All three paths converge on the same final step: load prompt → call LLM → write output
- Only **input acquisition** differs (read file / fetch+clean / transcribe)
- One script = single source of truth for flag parsing, prompt loading, output writing
- Sub-skills exist for **documentation discoverability**: when a user asks "how do I distill a YouTube video", they get the media-specific doc with caveats and examples — not buried in a generic page

Script lives at `meta/distill/scripts/distill.py` (one level up from sub-skills) because all three share it. `help.md` lives at the meta root because it's user-facing CLI documentation, not a sub-skill asset.

### Routing logic (`distill/references/ROUTER.md`)

| Request pattern | Route to |
|---|---|
| file path, "distill <file>", local document | `from-file/SKILL.md` |
| article URL, blog post, web page | `from-url/SKILL.md` |
| YouTube URL, `youtube.com`, `youtu.be` | `from-media/SKILL.md` |

### Auto-detection in the script

| Input shape | Resolved type | Acquisition |
|---|---|---|
| not `http(s)://` | `file` | read UTF-8 directly |
| `http(s)://` + `youtube.com` or `youtu.be` | `media` | shell out to `transcript-sk/scripts/transcript.py --no-prompt` |
| `http(s)://` + any other host | `article` | shell out to `defuddle` → clean markdown |

Override with `--source-type {auto,file,article,media}`.

YouTube is the **only** auto-detected media host for v1. Other media hosts require explicit `--source-type media`.

### Output location logic ★ NEW

Default output location depends on input type:

| Input type | Default output parent | Run folder name |
|---|---|---|
| file | parent dir of the input file | `{slug}_{timestamp}_{prompt}/` |
| article URL | `~/Documents/_my_docs/62_distill_exports/` | `{slug}_{timestamp}_{prompt}/` |
| media URL (YouTube) | `~/Documents/_my_docs/62_distill_exports/` | `{slug}_{timestamp}_{prompt}/` |

`--output-dir DIR` always overrides the default.

**Slug derivation:**
- File: input filename stem (`article.md` → `article`)
- Article URL: last non-empty path segment, slugified (`/blog/my-post/` → `my-post`); fallback to hostname
- Media URL: YouTube video ID extracted from `?v=` or `youtu.be/<id>` (`watch?v=2QpXab8z_Gw` → `2QpXab8z_Gw`)

**Timestamp format:** `YYYY-MM-DD_HH-MM-SS`

**Example folder names:**
- `article_2026-04-06_14-32-08_follow_along_note/`
- `my-post_2026-04-06_14-32-08_short_summary/`
- `2QpXab8z_Gw_2026-04-06_14-32-08_summary_with_quotes/`

### `--effort` flag — single canonical vocabulary, internal ETL ★ NEW

User always types canonical values. Script translates per provider.

**Canonical (user-facing):** `low | medium | high | max`
**Default:** `medium`

**Internal ETL:**

| Canonical | Claude CLI value | Codex CLI value |
|---|---|---|
| `low` | `low` | `low` |
| `medium` | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

User never sees the vendor-specific values. If a vendor adds a new effort level later, the ETL absorbs it.

### `--help` rendered via glow ★ NEW

`-h` / `--help` does **not** use argparse's auto-generated help. Instead:

1. Locate `meta/distill/help.md` relative to the script (`Path(__file__).parent.parent / "help.md"`)
2. If `glow` is in PATH → `glow help.md` (rendered terminal markdown)
3. If `glow` not in PATH → print raw markdown to stdout
4. Exit `0`

This means:
- `help.md` is the canonical CLI documentation, version-controlled with the meta-skill
- Help can be richer than argparse allows (sections, code blocks, tables, examples)
- Help renders beautifully in any terminal that has `glow`
- Help still works without `glow` (fallback to plain markdown)
- Argparse parser uses `add_help=False`; we add a custom `-h/--help` action that calls our renderer

### External dependency matrix

| Path | Required tools | Detected when |
|---|---|---|
| file | provider CLI (`claude` or `codex`) | always |
| article | `defuddle` in PATH + provider CLI | only when source-type resolves to `article` |
| media | `transcript.py` from `transcript-sk` + Deepgram keyring + provider CLI | only when source-type resolves to `media` |
| `--help` | `glow` (optional, falls back to plain print) | only on `--help` |

Lazy checking — file-only users don't need defuddle, Deepgram, or even glow.

### Invocation examples

```
distill ~/Documents/article.md                              → output beside input file
distill --prompt short_summary ~/notes.txt                  → from-file + short_summary
distill https://example.com/blog/post                       → from-url, default prompt (defuddle)
distill --prompt summary_with_quotes https://example.com/x  → from-url + summary_with_quotes
distill https://youtube.com/watch?v=2QpXab8z_Gw             → from-media, default prompt
distill --source-type article https://youtu.be/xyz          → force article path on a media URL
distill --effort high --provider codex ./meeting.md         → codex with high effort
distill --list-prompts                                      → reads from distill-prompt
distill --help                                              → renders help.md via glow
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
   - `help.md` (rich markdown CLI documentation, see `FLAGS.md`)
   - `references/ROUTER.md` with input-type routing table
   - `references/from-file/SKILL.md`
   - `references/from-url/SKILL.md`
   - `references/from-media/SKILL.md`

3. **Build `scripts/distill.py`** (per `FLAGS.md` and `ARCHITECTURE.md`)
   - PEP 723 inline metadata, `uv run` shebang
   - Argparse with `add_help=False` + custom `-h/--help` action
   - Auto-detection of input type (YouTube hosts only for media)
   - Lazy dependency checking per path
   - Output location logic (alongside file vs central exports)
   - Effort ETL (canonical → vendor-specific)
   - Three acquisition paths converging on unified distill+output flow
   - Type hints, ruff/pyright clean

4. **Test paths**
   - `distill --help` → renders help.md via glow
   - `distill --help` (without glow) → prints raw markdown
   - `distill --list-prompts` → enumerates from `distill-prompt`
   - `distill --dry-run ~/some-file.md` → resolves all flags, prints plan
   - `distill ~/some-file.md` → file path, output beside input
   - `distill https://some-blog.com/post` → article path (defuddle)
   - `distill https://youtube.com/...` → media path (transcript-sk delegation)
   - `distill --source-type article https://youtu.be/xyz` → override
   - `distill --effort max ~/file.md` → claude gets `max`
   - `distill --effort max --provider codex ~/file.md` → codex gets `xhigh`

5. **Apply via chezmoi**
   - `chezmoi apply -v` to sync to `~/.config/opencode/skill/meta/distill*`

---

## Acceptance criteria

- [ ] `meta/distill-prompt/` exists with 3 migrated prompts, each in its own sub-folder
- [ ] `meta/distill/` exists with `help.md`, `from-file`, `from-url`, `from-media` sub-skills + shared `scripts/distill.py`
- [ ] `distill.py` accepts file paths AND URLs, auto-detects input type
- [ ] `--source-type` flag overrides auto-detection
- [ ] `--help` renders `help.md` via glow (or plain fallback)
- [ ] File input writes output beside the input file
- [ ] URL input writes output to `~/Documents/_my_docs/62_distill_exports/`
- [ ] Run folder naming follows `{slug}_{timestamp}_{prompt}/`
- [ ] `--effort` accepts canonical `low|medium|high|max` and ETLs per provider
- [ ] YouTube is the only auto-detected media host
- [ ] `distill --list-prompts` lists all prompts from `distill-prompt`
- [ ] File path works without `defuddle`, Deepgram, or `glow` installed
- [ ] Article URL works via `defuddle`
- [ ] YouTube URL still works via `transcript-sk` delegation
- [ ] `transcript-sk` is unchanged and still works on its own
- [ ] All meta-skills follow the meta-skill-creator structure
- [ ] Script passes `ruff check` and `pyright`

---

## Open questions deferred

- Whether to eventually delete prompts from `transcript-sk/scripts/prompts/` and have `transcript-sk` read from `distill-prompt`. Out of scope.
- Stdin support for piped input. Deferred — file path or URL only for v1.
- Multiple inputs in one run (`distill *.md`). Deferred — single input for v1.
- Caching of fetched URLs / extracted text. Deferred.
- Additional media hosts (Vimeo, SoundCloud, etc.). Deferred — YouTube only for v1.

---

## Companion documents

- `FLAGS.md` — complete CLI surface, every flag, exit codes
- `HELP.md` — the rendered `help.md` content (canonical user-facing help)
- `ARCHITECTURE.md` — design decisions, why one script, dependency model
