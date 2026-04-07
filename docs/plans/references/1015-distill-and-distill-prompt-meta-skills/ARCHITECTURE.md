---
name: Distill Architecture
description: Architecture documentation for distill meta-skills
tags:
  - area/ea
  - kind/project
  - status/stable
date_created: 2026-04-07
date_updated: 2026-04-07
---

# Distill - Architecture decisions

Companion to `PLAN.md`, `FLAGS.md`, and `HELP.md`. Documents the why behind
structural choices so future changes do not accidentally undo them.

---

## Decision 1: One unified script, one current sub-skill

**Choice:** A single `distill.py` handles local file input. The meta-skill
currently exposes one documentation sub-skill, `from-file`, which references the
shared script.

**Alternatives considered:**

| Alternative | Rejected because |
|---|---|
| Plain skill instead of meta-skill | The user wants `meta/distill` to remain the stable top-level entry point for future URL and media expansion. |
| Separate scripts for future source types now | Premature. Adds complexity before those paths are approved. |
| Build URL and media now and adapt `transcript-sk` | Conflicts with the requirement to leave `transcript-sk` untouched. |

**Implication:** The structure reserves room for future `from-url` and
`from-media` docs, but v1 implements only `from-file`.

---

## Decision 2: File-only scope for v1

**Choice:** `distill` supports local file input only.

**Why:**

- This directly solves the user's immediate need: apply the prompt library to
  local text without going through `transcript-sk`.
- It keeps `transcript-sk` untouched.
- It removes the need for URL fetching, article extraction, and media
  orchestration in v1.
- It keeps the CLI and implementation minimal.

**Explicitly out of scope:** article URLs, YouTube URLs, other media hosts,
auto-detection between source types.

---

## Decision 3: Prompt library as separate meta-skill

**Choice:** Prompts live in `meta/distill-prompt/`, not inside `meta/distill/`.

**Why:**

- Prompts will grow independently of the distill script.
- Other skills can read from the same prompt library later.
- Each prompt is a documented unit (`SKILL.md` + `prompt.md`).

---

## Decision 4: Output folder lives beside the input file

**Choice:** File input creates the output folder beside the source file, unless
`--output-dir` overrides it.

**Why:**

- Files have a natural home: their parent directory.
- This keeps source material and derived artifacts together.
- It avoids inventing a central export location for a file-based workflow.

**Run folder naming:** `{slug}_{timestamp}_{prompt}/`

---

## Decision 5: `--effort` is canonical, ETL inside script

**Choice:** `--effort` accepts a single canonical vocabulary
`{low, medium, high, max}`. The script translates per provider before invoking
the CLI.

**ETL table:**

| Canonical | Claude | Codex |
|---|---|---|
| `low` | `low` | `low` |
| `medium` | `med` | `medium` |
| `high` | `high` | `high` |
| `max` | `max` | `xhigh` |

**Why:**

- Users should not memorize vendor-specific values.
- One vocabulary across providers keeps the CLI stable.
- Vendor quirks live in one table, not scattered through docs or code.

---

## Decision 6: `--help` renders `help.md` via glow

**Choice:** `-h` / `--help` does not use argparse's auto-generated help.
Instead, the script reads `meta/distill/help.md` and pipes it to `glow`. If
`glow` is not in PATH, it prints raw markdown.

**Why:**

- Argparse help is rigid.
- `help.md` is version-controlled with the skill.
- Help can include examples, tables, and richer explanation.
- The user explicitly requested glow rendering.

**Implementation:**

- Argparse parser uses `add_help=False`
- Custom action handles `-h` / `--help`:
  1. Locate `help.md` via `Path(__file__).parent.parent / "help.md"`
  2. If `shutil.which("glow")` → `subprocess.run(["glow", str(help_path)])`
  3. Else → `sys.stdout.write(help_path.read_text())`
  4. `sys.exit(0)`

---

## Decision 7: Per coding-standards (CliSpec + CliImpl + Python)

The script will:

- Use PEP 723 inline metadata + `uv run` shebang
- Type hints throughout, pyright-clean
- Be ruff-formatted and ruff-checked
- Use argparse for parsing
- Use a custom `-h/--help` action overriding argparse default
- Use distinct exit codes per failure class
- Include `--dry-run` and `--quiet`
- Use actionable error messages that resolve in one attempt
- Include `--list-*` discovery commands
- Avoid interactive prompts; everything via flags
- Be idempotent through timestamped output folders

---

## What this design does NOT include (and why)

| Feature | Why deferred |
|---|---|
| URL input | Out of scope for v1. |
| Media input | Out of scope for v1. |
| Stdin input | Out of scope for v1. |
| Multiple inputs (`distill *.md`) | Out of scope for v1. |
| URL fetch caching | Not needed for file-only scope. |
| Custom prompts via flag | Use the prompt library. |
| `--temperature` / `--max-tokens` | Provider CLIs handle these. |
| Prompt chaining | Out of scope. |
| Web UI / TUI | CLI only. |
| MCP tool wrapping | Future. CLI works in any harness today. |

---

## Invariants to preserve in future changes

1. **`meta/distill` stays the top-level container.** Future input modes should
   extend it, not replace it.
2. **Prompts remain external.** Do not move prompts back into the script.
3. **File outputs go beside the input by default.** Do not centralize file
   outputs without explicit `--output-dir`.
4. **`--effort` is canonical.** Do not expose vendor-specific values to users.
5. **`help.md` is the canonical help.** Do not add a parallel argparse help
   string.
6. **Harness-agnostic.** No harness-specific tooling in the implementation.
