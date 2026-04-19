---
name: distill-prompt
description: Library of named "distill" prompts for transforming long-form text into structured notes, summaries, quote-based outlines, or content-adaptive wisdom reports. Each sub-skill is one prompt style (follow-along-note, short-summary, summary-with-quotes, extract-wisdom). USE WHEN picking a distill prompt, choosing a summary style, selecting a note-taking template, deciding which distill prompt fits this content, listing available distill prompts.
keywords: [distill, distill-prompt, prompt-library, summary, notes, follow-along, short-summary, quotes, extract-wisdom, wisdom, insights, transcript, article]
---

# distill-prompt

> A library of reusable prompts for distilling long-form text. Each sub-skill is a single named prompt style, ready to be passed to the `distill` tool.

---

## Routing

Load `references/ROUTER.md` to determine which prompt sub-skill fits the request.

---

## The Problem

Prompts that transform long content into notes, summaries, or outlines are usually buried inside a specific tool (a transcription script, a note-taker, an agent harness). They are hard to reuse, hard to inventory, and hard to grow. New styles get invented instead of extended because nobody knows what already exists.

- **Prompts locked inside tools** -- a summary prompt living inside a YouTube transcriber cannot be used on a local article
- **No central inventory** -- it is unclear what prompts exist, who owns them, or how they differ
- **Growth is awkward** -- adding a new style means touching code in the consuming tool
- **Duplication** -- similar prompts drift across tools because nobody consolidates them

The fundamental issue: prompts are content, not code, and they should live in their own versioned library.

---

## The Solution

`distill-prompt` is a plain prompt library. Each prompt is a sub-skill folder under `references/` with:

- A `SKILL.md` describing when to use it and what shape of output to expect
- A `prompt.md` containing the raw prompt text, no frontmatter, no wrapping

A consumer (like the `distill` tool) receives the path to a specific `prompt.md` and feeds it to an LLM.

**Core capabilities:**

1. **Named prompt styles** -- each folder is one clearly-scoped prompt
2. **Raw prompt files** -- `prompt.md` is plain text, ready to pipe into any LLM CLI
3. **Self-documenting** -- every prompt has its own `SKILL.md` explaining intent and output shape
4. **Grows without code changes** -- add a new folder, add a row to `ROUTER.md`, done
5. **Consumer-agnostic** -- any skill or tool can read from this library

---

## What's Included

| Component | Path | Purpose |
|-----------|------|---------|
| Router | `references/ROUTER.md` | Routing table that maps request patterns to prompt sub-skills |
| follow-along-note | `references/follow-along-note/` | Detailed follow-along notes preserving structure and nuance |
| short-summary | `references/short-summary/` | Concise 2-3 sentence overview with key bullet points |
| summary-with-quotes | `references/summary-with-quotes/` | Structured outline with the best verbatim quotes |
| extract-wisdom | `references/extract-wisdom/` | Content-adaptive wisdom report with dynamic sections and depth levels |

**Summary:**
- **Prompts:** 4 (follow-along-note, short-summary, summary-with-quotes, extract-wisdom)
- **Dependencies:** None (works standalone)
- **Consumers:** `meta/distill` (primary), any future skill that needs a prompt by name

---

## Invocation Scenarios

| Trigger | What Happens |
|---------|--------------|
| "use the follow-along prompt" | Routes to `follow-along-note/MetaSkill.md` |
| "short summary" / "TL;DR" / "quick overview" | Routes to `short-summary/MetaSkill.md` |
| "summary with quotes" / "include quotes" / "quote-based outline" | Routes to `summary-with-quotes/MetaSkill.md` |
| "extract wisdom" / "what's interesting" / "key takeaways" / "analyze this video" | Routes to `extract-wisdom/MetaSkill.md` |
| "list available distill prompts" | Lists all sub-skills under `references/` |

---

## Using a Prompt

Each prompt sub-skill has exactly two files:

```
references/<prompt-name>/
├── SKILL.md      # intent, when to use, expected output shape
└── prompt.md     # raw prompt text, piped to LLMs as-is
```

A consumer reads `prompt.md` and passes it to an LLM. The `distill` tool does this by resolving a prompt stem via `--prompt`:

```
uv run ~/.config/opencode/skill/meta/distill/scripts/distill.py <input-file> \
    --prompt follow_along_note
```

---

## Adding a New Prompt

1. Create `references/<new-prompt>/` with kebab-case folder name
2. Add `SKILL.md` with proper frontmatter (`name`, `description`), when-to-use notes, and expected output shape
3. Add `prompt.md` with the raw prompt text (no frontmatter)
4. Add one row to `references/ROUTER.md` mapping request patterns to the new folder
5. No code changes required. The `distill` tool consumes any prompt at a given path.

---

## Configuration

No configuration required. The library is a static collection of prompt files.

---

## Related Work

- **`meta/distill`** -- the processor that applies these prompts to local files
- **`utils/transcript-sk`** -- older YouTube transcription skill that bundles its own prompts (not migrated to this library)
