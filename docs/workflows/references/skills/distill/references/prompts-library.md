---
name: Prompts Library
description: How the sibling `distill-prompt` skill feeds distill, stem normalization, and how to add a new prompt
tags:
  - area/ea
  - kind/doc
  - status/open
date_created: 2026-04-11
date_updated: 2026-04-11
sources:
  - distill
---

distill is the runner. The prompts it runs live in a separate skill called `distill-prompt`, one directory level up at `dot_config/ai_templates/skills/pa-sdlc/distill-prompt/references/`. The two skills are a tight pair: distill treats `distill-prompt` as its prompt database, and `distill-prompt` is only useful to distill. This page documents how they connect and how to add a new prompt without breaking anything.

## The physical layout

`distill-prompt` stores one prompt per folder. The current inventory is three folders at `dot_config/ai_templates/skills/pa-sdlc/distill-prompt/references/`:

```text
distill-prompt/references/
├── ROUTER.md
├── follow-along-note/
│   ├── MetaSkill.md
│   └── prompt.md
├── short-summary/
│   ├── MetaSkill.md
│   └── prompt.md
└── summary-with-quotes/
    ├── MetaSkill.md
    └── prompt.md
```

Each prompt folder has exactly two files:

- **`prompt.md`** — the actual prompt text distill feeds to the provider. This is the file distill reads at runtime.
- **`MetaSkill.md`** — a short description of what the prompt does and when to reach for it. distill never reads this file; it is there for humans and for the `distill-prompt` skill's own router.

`ROUTER.md` at the top of the library is a dispatch table used by `distill-prompt`'s own meta-skill. distill does not consult it — distill resolves prompts by directory lookup, not by routing.

## How distill resolves a prompt stem

The resolution path runs through two functions near the top of `scripts/distill.py`:

### Step 1: normalize the user input

`normalize_prompt_stem` at `scripts/distill.py:471-477`:

```python
def normalize_prompt_stem(raw: str) -> str:
    """Normalize a user-facing prompt stem to canonical underscore form."""
    stem = raw.strip().lower()
    if stem.endswith(".md"):
        stem = stem[:-3]
    stem = stem.replace("-", "_")
    return stem
```

This makes the following user-facing inputs equivalent:

| User types | Normalized |
|---|---|
| `follow_along_note` | `follow_along_note` |
| `follow-along-note` | `follow_along_note` |
| `FOLLOW_ALONG_NOTE` | `follow_along_note` |
| `follow_along_note.md` | `follow_along_note` |
| `Follow-Along-Note` | `follow_along_note` |

The canonical form uses underscores. That canonical form is what gets written to `meta.yml`'s `prompt` field and appears in the run folder name, regardless of what the user typed.

### Step 2: map the canonical stem to a folder

`resolve_prompt` at `scripts/distill.py:480-496`:

```python
prompt_name = normalize_prompt_stem(raw)
prompt_dir = PROMPTS_DIR / prompt_name.replace("_", "-")
prompt_path = prompt_dir / "prompt.md"
```

`PROMPTS_DIR` is computed once at `scripts/distill.py:47` as the sibling skill's references directory:

```python
PROMPTS_DIR = SKILL_DIR.parent / "distill-prompt" / "references"
```

The directory lookup is kebab-case — the canonical underscore stem is flipped back to hyphens for the filesystem path. `follow_along_note` becomes `follow-along-note/prompt.md`. This lets the on-disk folder names stay kebab-case (which is the chezmoi and wiki-map convention for filenames) while the canonical in-memory form stays underscore (which is the Python identifier convention for the script's internal state).

If `prompt.md` does not exist at the computed path, `resolve_prompt` raises `PromptFileError` with exit code `EXIT_PROMPT_NOT_FOUND = 4` and the error message tells the operator to run `--list-prompts`.

## `--list-prompts` discovery

`--list-prompts` (implemented at `scripts/distill.py:697`-ish in the discovery section) scans `PROMPTS_DIR` for any subdirectory that contains a `prompt.md` file and prints the list. The scan is a pure filesystem walk — no allowlist, no configuration. This means:

- Adding a new prompt is zero-config: create a new folder with a `prompt.md` inside and `--list-prompts` will pick it up immediately.
- Removing a prompt is similarly zero-config: delete the folder and the stem becomes unresolvable.
- There is no way to have a "hidden" or "disabled" prompt. Anything on disk with a `prompt.md` in the right place is live.

## Adding a new prompt

The happy path for adding a new prompt named `action-items`:

1. Create the folder under the chezmoi source path:

   ```text
   dot_config/ai_templates/skills/pa-sdlc/distill-prompt/references/action-items/
   ```

2. Write `prompt.md` inside it. No frontmatter required — the file is read as raw text and handed to the provider's system-prompt flag verbatim.

3. Write `MetaSkill.md` alongside it. This is the human-readable companion file; distill does not read it, but `distill-prompt`'s own meta-skill router expects one per prompt folder.

4. Run `chezmoi apply -v` to fan out the new prompt to every agent home. See [[how-ai-templates-are-distributed]] for the pipeline.

5. Verify the prompt is live: `distill.py --list-prompts`.

6. Smoke-test: `distill.py some-small-file.md --prompt action-items --dry-run`. Then run it against a real file once the dry-run looks right.

## What prompts can and cannot do

Prompts are simple strings. distill feeds them to the provider as the system prompt (for claude at `scripts/distill.py:830-831`; similar for codex; opencode receives it as an inline agent instruction). Prompts do not have access to:

- Variables from the invocation — no template substitution, no `{filename}` interpolation
- The input text — the prompt is the *system* message; the input is a separate *user* message framed as `"Based on this content:\n\n{input}"` at `scripts/distill.py:130`
- Other prompts — no composition, no chaining
- File I/O, shell commands, or network calls

If the operator wants conditional behavior — "summarize technical content one way, narrative content another" — the answer is two separate prompts, not one conditional prompt.

## Why `distill-prompt` is a separate skill

The two-skill split exists so that the prompt library can grow independently of the runner. Adding a new prompt should not require editing distill's Python source; changing distill's argument parsing should not touch any prompt text. The split also means `distill-prompt` could plausibly be reused by a future runner (a browser extension, a vim plugin, etc.) without dragging distill's CLI dependencies along.

## Related

- [[overview]]
- [[output-layout]]
- [[how-ai-templates-are-distributed]]
