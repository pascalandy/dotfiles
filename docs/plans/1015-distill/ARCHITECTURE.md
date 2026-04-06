# Distill — Architecture decisions

Companion to `PLAN.md` and `FLAGS.md`. Documents the **why** behind structural choices so future changes don't accidentally undo them.

---

## Decision 1: One unified script, three sub-skills

**Choice:** A single `distill.py` handles file, article URL, and media URL inputs. The meta-skill exposes three documentation sub-skills (`from-file`, `from-url`, `from-media`) that all reference the same script.

**Alternatives considered:**

| Alternative | Rejected because |
|---|---|
| Three separate scripts (`distill_file.py`, `distill_url.py`, `distill_media.py`) | Triplicates flag parsing, prompt loading, output writing, error handling. Bug fixes happen three times. Drift inevitable. |
| Single sub-skill, no router | Loses progressive disclosure. Users asking "how do I distill a YouTube video" get buried in file/article details and unrelated caveats. |
| Two sub-skills (`from-file`, `from-url`) collapsing article and media into one URL doc | URL handling has distinct failure modes per type (defuddle missing vs Deepgram missing vs paywall vs media transcoding). Each deserves its own doc with its own caveats and external-dep notes. |
| Script under one sub-skill, others import it | Implies a hierarchy where none exists. All three input types are equal citizens. Script lives at `meta/distill/scripts/` (one level up from sub-skills) to make this explicit. |

**Implication:** The three sub-skill `SKILL.md` files are documentation views, not code modules. They differ in:
- Example invocations
- External dependency callouts
- Common pitfalls (paywalls, age-gated videos, encoding issues)
- When to use `--source-type` override

They do **not** differ in flags, output format, or exit codes. Those are defined once in `FLAGS.md`.

---

## Decision 2: Auto-detect input type, allow override

**Choice:** Default `--source-type auto` inspects the input string. Explicit `--source-type` override available.

**Detection rules:**
1. Not starting with `http(s)://` → `file`
2. Starting with `http(s)://`:
   - Known media hosts → `media`
   - Anything else → `article`

**Why:** Users shouldn't have to think about input types for the common case. Pasting a YouTube URL or a blog URL or a file path should "just work". Override exists for edge cases (YouTube transcript page treated as article, non-standard media host, ambiguous URL).

**Why not require explicit type:** Adds friction for the 95% case. Goes against agent-friendly CLI principles (auto-detect with override, not mandatory mode flags).

**Why include override:** Auto-detection will be wrong sometimes. Without override, users hit a wall. Per coding-standards CliAudit guidance: "agents need explicit overrides for every auto-detected behavior".

---

## Decision 3: Lazy dependency checking

**Choice:** Only check for `defuddle` when source-type resolves to `article`. Only check for `transcript.py` + Deepgram when source-type resolves to `media`. Provider CLI is always required.

**Why:** A user who only ever distills local text files should never see "defuddle not found" errors. Each path's dependencies are isolated.

**Implication:** The script must do source-type resolution **before** dependency checks. Order of operations:
1. Parse args
2. Resolve source-type (auto or explicit)
3. Check dependencies for that type
4. Validate prompt exists
5. Validate output dir writable
6. (If not `--dry-run`) acquire input → distill → write output

---

## Decision 4: Delegate media path to existing `transcript-sk`

**Choice:** Media URL handling shells out to `transcript-sk/scripts/transcript.py` rather than reimplementing yt-dlp + Deepgram.

**Why:**
- `transcript.py` already works, has tests, handles edge cases (long videos, retries, context limits)
- Reimplementing duplicates Deepgram API code, yt-dlp integration, error handling
- `transcript-sk` is the source of truth for "audio → text"; `distill` is the source of truth for "text → distilled output"
- Clean separation of concerns

**How:** `distill.py` invokes `transcript.py --no-prompt <url>` to get the raw transcript, then runs the unified distill flow on the result. The `--no-prompt` flag tells `transcript.py` to skip its own summary step.

**Future:** If `transcript-sk` is decommissioned, the media path internally swaps to direct yt-dlp + Deepgram calls. **The user-facing interface does not change.** That's the value of having one entry point.

---

## Decision 5: Article extraction via `defuddle`

**Choice:** Use the `defuddle` CLI (already in user's toolchain per `AGENTS.md`) for HTML → clean markdown.

**Alternatives:**

| Tool | Rejected because |
|---|---|
| `trafilatura` (Python lib) | Would add a Python dependency. `defuddle` is a CLI already installed and trusted. |
| Raw `httpx` + BeautifulSoup | Reinventing extraction. Defuddle handles boilerplate removal, paywalls, JS-rendered content fallbacks. |
| `readability-lxml` | Older, less maintained. Defuddle is the user's existing standard. |
| `WebFetch` tool | Tool-specific, not portable across harnesses. Skills must be harness-agnostic. |

**Implication:** `defuddle` becomes a hard dependency for the article path. Documented in `from-url/SKILL.md`. Lazy-checked at runtime.

---

## Decision 6: Prompt library as separate meta-skill

**Choice:** Prompts live in `meta/distill-prompt/`, not inside `meta/distill/`.

**Why:**
- Prompts will grow (user explicitly mentioned this). Independent versioning and discovery.
- Other skills can read from the same prompt library (future: `transcript-sk` migrates to it; other distill-like tools can reuse).
- Separation of "what to do with text" (prompts) from "how to acquire and process text" (distill).
- Each prompt is a documented unit with its own `SKILL.md` describing intent and sample output.

**Why not a flat folder of `.md` files:** Loses room for per-prompt documentation. A folder per prompt allows `SKILL.md` (when to use, sample output) + `prompt.md` (canonical text). Future additions (per-prompt examples, test inputs, output schemas) have a place to live.

---

## Decision 7: Output folder convention matches `transcript-sk`

**Choice:** Timestamped run folders under `~/Documents/_my_docs/62_distill_exports/` with `{prompt}.md`, `source.txt`, `meta.txt`. Optional `extracted.txt` when `--keep-extracted`.

**Why:** Consistency with existing user workflow. `transcript-sk` exports to `61_transcription_exports_yt`. `distill` follows the same numbering scheme (`62_*`) and same internal structure. Muscle memory transfers.

---

## Decision 8: Per coding-standards (CliSpec + CliImpl + Python)

The script will:

- Use PEP 723 inline metadata + `uv run` shebang (per `Python` standards)
- Type hints throughout, pyright-clean
- ruff-formatted, ruff-checked
- Argparse for parsing (stdlib, no extra deps for the core)
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
| Stdin input | v1 scope. File or URL only. Easy to add later (`-` as input). |
| Multiple inputs (`distill *.md`) | v1 scope. Single input only. Shell loops handle this. |
| URL fetch caching | Premature optimization. Add when re-runs become a pain point. |
| Custom prompts via flag | Use the prompt library. Adding a one-off prompt = adding a folder. |
| `--temperature` / `--max-tokens` | Provider CLIs handle these. Not exposed in v1. Add if needed. |
| Prompt chaining (multi-step distill) | Out of scope. Run distill twice if needed. |
| Web UI / TUI | CLI only. Skills are CLI-first. |
| MCP tool wrapping | Future. CLI works in any harness today. |

---

## Invariants to preserve in future changes

1. **One script, three sub-skills.** Don't split the script. Don't merge the sub-skills.
2. **Auto-detection with explicit override.** Don't make `--source-type` required.
3. **Lazy dependency checking.** Don't make file-only users install defuddle.
4. **Prompts external.** Don't move prompts back into the script or into `distill/`.
5. **`transcript-sk` is the audio-to-text source of truth.** Don't reimplement Deepgram inside `distill.py`.
6. **Output folder convention matches `transcript-sk`.** Don't change the layout without updating both.
7. **Harness-agnostic.** No Claude Code-specific paths, no MCP-specific tooling. Pure CLI.
