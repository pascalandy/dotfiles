# Distill — Architecture decisions

Companion to `PLAN.md`, `FLAGS.md`, and `HELP.md`. Documents the **why** behind structural choices so future changes don't accidentally undo them.

---

## Decision 1: One unified script, three sub-skills

**Choice:** A single `distill.py` handles file, article URL, and media URL inputs. The meta-skill exposes three documentation sub-skills (`from-file`, `from-url`, `from-media`) that all reference the same script.

**Alternatives considered:**

| Alternative | Rejected because |
|---|---|
| Three separate scripts | Triplicates flag parsing, prompt loading, output writing, error handling. Bug fixes happen three times. Drift inevitable. |
| Single sub-skill, no router | Loses progressive disclosure. Users asking "how do I distill a YouTube video" get buried in file/article details. |
| Two sub-skills (`from-file`, `from-url`) collapsing article and media | URL handling has distinct failure modes per type (defuddle vs Deepgram vs paywall). Each deserves its own doc. |
| Script under one sub-skill, others import it | Implies a hierarchy where none exists. All three input types are equal citizens. |

**Implication:** Sub-skill `SKILL.md` files are documentation views, not code modules. They differ in examples, caveats, and external-dep notes — not in flags or output format.

---

## Decision 2: Auto-detect input type, allow override

**Choice:** Default `--source-type auto` inspects the input string. Explicit `--source-type` override available.

**Detection rules:**
1. Not starting with `http(s)://` → `file`
2. Starting with `http(s)://`:
   - YouTube hosts (`youtube.com`, `www.youtube.com`, `m.youtube.com`, `youtu.be`) → `media`
   - Anything else → `article`

**Why:** Pasting a YouTube URL or a blog URL or a file path should "just work". Override exists for edge cases.

**Why YouTube only for v1:** Keep the auto-detection list small and trustworthy. Each new media host needs its own validation that `transcript-sk` actually handles it. Users can force any URL through the media path with `--source-type media`.

---

## Decision 3: Lazy dependency checking

**Choice:** Only check for `defuddle` when source-type resolves to `article`. Only check for `transcript.py` + Deepgram when source-type resolves to `media`. Provider CLI is always required. `glow` is never required.

**Why:** A user who only ever distills local text files should never see "defuddle not found" errors.

**Order of operations:**
1. Parse args (custom `-h/--help` short-circuits to glow renderer)
2. Resolve source-type (auto or explicit)
3. Check dependencies for that type
4. Validate prompt exists
5. Validate output dir writable
6. (If not `--dry-run`) acquire input → distill → write output

---

## Decision 4: Delegate media path to existing `transcript-sk`

**Choice:** Media URL handling shells out to `transcript-sk/scripts/transcript.py --no-prompt <url>` rather than reimplementing yt-dlp + Deepgram.

**Why:**
- `transcript.py` already works, has tests, handles edge cases
- Reimplementing duplicates Deepgram API code, yt-dlp integration, error handling
- `transcript-sk` is the source of truth for "audio → text"; `distill` is the source of truth for "text → distilled output"

**How:** Invoke `transcript.py --no-prompt <url>` to get the raw transcript file, then run the unified distill flow on the result.

**Future:** If `transcript-sk` is decommissioned, the media path internally swaps to direct yt-dlp + Deepgram calls. **The user-facing interface does not change.**

---

## Decision 5: Article extraction via `defuddle`

**Choice:** Use the `defuddle` CLI for HTML → clean markdown.

| Tool | Rejected because |
|---|---|
| `trafilatura` (Python lib) | Adds a Python dep. `defuddle` is already in user's toolchain. |
| Raw `httpx` + BeautifulSoup | Reinventing extraction. Defuddle handles boilerplate, JS-rendered fallbacks. |
| `readability-lxml` | Older, less maintained. |
| `WebFetch` tool | Tool-specific, not portable across harnesses. |

---

## Decision 6: Prompt library as separate meta-skill

**Choice:** Prompts live in `meta/distill-prompt/`, not inside `meta/distill/`.

**Why:**
- Prompts will grow independently of the distill script
- Other skills can read from the same prompt library
- Each prompt is a documented unit (`SKILL.md` + `prompt.md`)

---

## Decision 7: Output location depends on input type ★ NEW

**Choice:**
- File input → output folder created **beside the input file**
- URL input → output folder created in `~/Documents/_my_docs/62_distill_exports/`

**Why:**
- Files have a natural "home" — the directory they live in. Putting outputs there keeps related artifacts together. Easy to find later, easy to grep.
- URLs have no local home. They need a central catalog.
- This matches how a human would organize the work: "the article I distilled lives next to the article I distilled".

**Override:** `--output-dir DIR` always wins, regardless of input type. Use it when you want a centralized dir even for files.

**Run folder naming:** `{slug}_{timestamp}_{prompt}/` — single underscores, slug first for at-a-glance recognition, timestamp middle for sorting, prompt last for filtering.

---

## Decision 8: `--effort` is canonical, ETL inside script ★ NEW

**Choice:** `--effort` accepts a single canonical vocabulary `{low, medium, high, max}`. The script translates per provider before invoking the CLI.

**ETL table:**

| Canonical | Claude | Codex |
|---|---|---|
| `low` | `low` | `low` |
| `medium` | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

**Why:**
- Users shouldn't memorize vendor-specific values (`med` vs `medium`, `max` vs `xhigh`)
- One vocabulary across providers means switching `--provider` doesn't require relearning effort levels
- Vendor quirks live in one ETL table, not scattered across docs and user habits
- When a vendor adds a new effort level, only the ETL table changes

**Why not split into `--claude-effort` / `--codex-effort`:** User explicitly rejected this. Single flag, ETL inside the script.

**Default:** `medium` (translates to `med` for Claude, `medium` for Codex).

---

## Decision 9: `--help` renders `help.md` via glow ★ NEW

**Choice:** `-h` / `--help` does not use argparse's auto-generated help. Instead, the script reads `meta/distill/help.md` and pipes it to `glow`. If `glow` is not in PATH, it prints raw markdown.

**Why:**
- Argparse help is rigid and ugly. `glow`-rendered markdown is rich, sectioned, includes tables and examples.
- `help.md` is version-controlled with the meta-skill — same source of truth as the docs.
- Help can include things argparse can't: example output, dependency matrices, "see also" sections, design rationale links.
- The user explicitly requested glow rendering.

**Why not just use argparse:**
- Argparse output is constrained to flag descriptions. Can't include rich examples or rationale.
- Argparse text wraps awkwardly in narrow terminals.
- Maintaining help in code (argparse) and docs (markdown) leads to drift.

**Implementation:**
- Argparse parser uses `add_help=False`
- Custom action handles `-h` / `--help`:
  1. Locate `help.md` via `Path(__file__).parent.parent / "help.md"`
  2. If `shutil.which("glow")` → `subprocess.run(["glow", str(help_path)])`
  3. Else → `sys.stdout.write(help_path.read_text())`
  4. `sys.exit(0)`

**Fallback graceful:** No glow = no error. Just plain markdown.

**Argparse still useful:** It still validates flag types, shows usage errors, parses `--list-*` etc. We just override the help action.

---

## Decision 10: Per coding-standards (CliSpec + CliImpl + Python)

The script will:

- Use PEP 723 inline metadata + `uv run` shebang (per `Python` standards)
- Type hints throughout, pyright-clean
- ruff-formatted, ruff-checked
- Argparse for parsing (stdlib, no extra deps for the core)
- Custom `-h/--help` action overriding argparse default (for glow rendering)
- All inputs via flags (per `CliAudit`)
- Distinct exit codes per failure class (per `CliSpec`)
- `--dry-run` and `--quiet` (per `CliAudit` agent-friendliness)
- Actionable error messages that resolve in one attempt
- `--list-*` discovery commands (per `transcript-sk` precedent + agent-friendly conventions)
- No interactive prompts; everything via flags
- Idempotent: timestamped output folders, no overwrites

---

## What this design does NOT include (and why)

| Feature | Why deferred |
|---|---|
| Stdin input | v1 scope. File or URL only. |
| Multiple inputs (`distill *.md`) | v1 scope. Single input only. Shell loops handle this. |
| URL fetch caching | Premature optimization. |
| Custom prompts via flag | Use the prompt library. |
| `--temperature` / `--max-tokens` | Provider CLIs handle these. Not exposed in v1. |
| Prompt chaining | Out of scope. |
| Web UI / TUI | CLI only. |
| MCP tool wrapping | Future. CLI works in any harness today. |
| Auto-detect for non-YouTube media hosts | v1 keeps the list small. Use `--source-type media` for others. |
| Video title as media slug (vs ID) | Requires extra API call. Video ID is faster, deterministic. |

---

## Invariants to preserve in future changes

1. **One script, three sub-skills.** Don't split the script. Don't merge the sub-skills.
2. **Auto-detection with explicit override.** Don't make `--source-type` required.
3. **Lazy dependency checking.** Don't make file-only users install defuddle.
4. **Prompts external.** Don't move prompts back into the script or into `distill/`.
5. **`transcript-sk` is the audio-to-text source of truth.** Don't reimplement Deepgram inside `distill.py`.
6. **File outputs go beside the input.** Don't centralize file outputs without explicit `--output-dir`.
7. **`--effort` is canonical.** Don't expose vendor-specific values to users.
8. **`help.md` is the canonical help.** Don't add a parallel argparse help string.
9. **Harness-agnostic.** No Claude Code-specific paths, no MCP-specific tooling. Pure CLI.
