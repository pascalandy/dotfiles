---
name: meta-skill-creator
description: Create hierarchical meta-skills where a minimal router delegates to specialized sub-skills. Use when building skill collections, creating meta-skills, designing router-based skill architectures, organizing multiple related skills under a single entry point, or when the user says "create a meta-skill", "build a skill collection", "make a router skill", or "organize these skills into one".
---

# Meta-Skill Creator

> Create a hierarchical meta-skill where a minimal router delegates to specialized sub-skills.

## Goal

<!-- user must provide:

A) Which skill(s) process. (Assume they are already well made as a skill)
B) where to export meta-skill

If one or the other is missing, stop and ask the user.
-->

Create a hierarchical meta-skill where a minimal router delegates to specialized sub-skills.

## Concept

A meta-skill is a collection of related skills that share a single entry point. The user never picks a sub-skill -- they describe what they need, and the right specialist activates automatically.

Three layers make this work:

1. **Collection** (root `SKILL.md`) -- The user-facing documentation. Explains what the collection does, lists every sub-skill and workflow, shows invocation examples. This is also the entry point the skill system loads. It bridges to the router.

2. **Router** (`ROUTER.md`) -- A minimal dispatch table that maps intent keywords to sub-skill paths. It exists so the collection can stay readable and the routing logic stays isolated. One new row per new sub-skill.

3. **Sub-skills** (one directory each) -- Complete, standalone skills following Anthropic's skill anatomy. Each owns a distinct domain with no overlap. Each works independently if loaded directly, but the normal path is through the router.

This is progressive disclosure applied to sub-skills: the skill system reads the collection, the collection loads the router, the router loads one sub-skill. The user sees a single skill. The AI loads only what's needed.

## Structure

```shell
[MetaSkill]/
├── SKILL.md                  # Layer 1: Collection (the ONLY file the scanner indexes as a skill)
└── references/
    ├── ROUTER.md              # Layer 2: Router (pure routing table, ~20 lines)
    ├── [ModeA]/               # Layer 3: Simple sub-skill — MetaSkill.md is enough
    │   └── MetaSkill.md
    ├── [ModeB]/               # Layer 3: Complex sub-skill — supporting material in references/
    │   ├── MetaSkill.md
    │   └── references/        # ALL supporting material lives here
    │       ├── some-doc.md
    │       ├── prompt-template.md
    │       ├── scripts/
    │       ├── templates/
    │       ├── examples/
    │       └── assets/
    └── [ModeC]/
        └── MetaSkill.md
```

**Sub-skill size rule:** A sub-skill root contains **only** `MetaSkill.md` plus an optional `references/` directory. If a sub-skill is too large or complex to fit cleanly in a single `MetaSkill.md` — it has supporting docs, prompts, scripts, templates, examples, or assets — put ALL of that supporting material under the sub-skill's `references/` directory. Do not scatter `workflows/`, `scripts/`, `templates/`, `assets/` as siblings of `MetaSkill.md`; nest them inside `references/`.

**Link hygiene:** when supporting files live under `references/`, internal links inside `MetaSkill.md` must use the `references/` prefix (e.g. `references/some-doc.md`, not `some-doc.md`).

**Critical naming rule:** the root file is `SKILL.md` (so the scanner discovers exactly one skill per meta-skill). Every sub-skill file is `MetaSkill.md` (so recursive `SKILL.md` scanners do not register sub-skills as independent top-level skills). See [Why Sub-Skills Use `MetaSkill.md`](#why-sub-skills-use-metaskillmd) below.

## Root SKILL.md (Collection)

IMPORTANT: At the root, we should only see a `SKILL.md` file and a `/references` directory.

The entry point the skill system loads. Contains:

- Frontmatter with name, description, all keywords
- Problem/solution framing for the collection
- "What's Included" table listing all sub-skills and their workflows
- Invocation scenarios table (trigger phrase → what happens)
- Usage examples showing representative inputs/outputs
- Customization options (if any)

**Must include this bridge to the router:**

```markdown
## Routing

Load `references/ROUTER.md` to determine which sub-skill handles this request.
```

Without this line, the router never gets read.

## ROUTER.md (Dispatcher)

Minimal file. Contains ONLY frontmatter + a routing table.

```yaml
---
name: [MetaSkill]
description: [What it does]. USE WHEN [all trigger keywords from all sub-skills merged into one flat list].
---
```

```markdown
# [MetaSkill]

## Routing

| Request Pattern | Route To |
|---|---|
| keyword1, keyword2, keyword3 | `[ModeA]/MetaSkill.md` |
| keyword4, keyword5 | `[ModeB]/MetaSkill.md` |
| keyword6, keyword7, keyword8 | `[ModeC]/MetaSkill.md` |
```

The router's `USE WHEN` aggregates ALL keywords from ALL sub-skills. The routing table narrows to the specific one.

## Sub-Skill MetaSkill.md

Each sub-skill follows Anthropic's skill anatomy but lives in a file named `MetaSkill.md` (not `SKILL.md`) so the scanner ignores it. It is only loaded explicitly through the router:

- YAML frontmatter with name and description (including its own `USE WHEN` scoped to its domain)
- Core concept explaining the methodology
- Workflow routing (maps intent → files in `workflows/`)
- Output format specification
- Examples
- No domain overlap with sibling sub-skills

Sub-skills are NOT directly invocable by name. The user always enters through the parent meta-skill (e.g. `gstack, plan-ceo`) and the router dispatches to the correct `MetaSkill.md`.

## Why Sub-Skills Use `MetaSkill.md`

Skill scanners (including Claude Code's native scanner) discover skills by walking the filesystem and indexing every `SKILL.md` they find. If sub-skills were named `SKILL.md`, the scanner would treat each one as an independent top-level skill. That breaks the meta-skill design in three ways:

1. **It defeats the single entry point.** A meta-skill exists so the user invokes ONE name (`gstack`) and the router dispatches internally. Indexing sub-skills as standalone skills creates multiple competing entry points.
2. **It causes name conflicts.** Generic sub-skill names (`review`, `qa`, `ship`, `plan`) collide with other skills in the registry, and the wrong one can win.
3. **It allows unintended auto-activation.** Sub-skills are designed to run only inside their parent's context. If the scanner indexes them, they can auto-trigger on keywords outside that context.

Renaming sub-skills to `MetaSkill.md` makes them invisible to the scanner. They keep the same content, frontmatter, and standalone format — they are simply loaded explicitly via the router instead of being discovered. The parent `SKILL.md` is the only file the scanner registers.

## Design Rules

1. **Single entry point** -- user invokes the meta-skill name, never a sub-skill directly
2. **Invisible delegation** -- router picks the right specialist automatically
3. **No domain overlap** -- each sub-skill owns distinct territory
4. **Consistent interface** -- all sub-skills follow the same internal structure
5. **Additive scaling** -- adding a sub-skill means one new directory + one new row in the routing table
6. **Scanner hygiene** -- only the root `SKILL.md` is named `SKILL.md`; every sub-skill file is `MetaSkill.md`
7. **Clean sub-skill roots** -- a sub-skill root holds only `MetaSkill.md` (+ optional `references/`). All supporting files (docs, prompts, scripts, templates, examples, assets) live under that sub-skill's `references/` directory, never as siblings of `MetaSkill.md`

## Harness Agnostic

A skill is a folder of markdown files and optional scripts. It runs on any coding assistant -- Claude Code, Codex, Gemini, No harness-specific dependencies. Concretely:

- **No harness-specific paths** -- Do not reference `~/.claude/`, or any assistant's internal directories. Skills reference their own files via relative paths (`references/`, `workflows/`, `scripts/`).
- **No assumed tools** -- Do not require specific tool from Claude Code like `hooks`, `present_files`, etc. Describe the action needed ("run this script", "read this file", "search the codebase") and let the harness map it to its own tooling.
- **Portable by default** -- One folder, copied into any assistant's skill directory, works immediately. No installation scripts, no adapter layers, no harness detection logic.

## Reference

- **Skills** are folders of instructions, scripts, and resources that loads dynamically to improve performance on specialized tasks. Skills teach an AI assistant how to complete specific tasks in a repeatable way, whether that's creating documents with your company's brand guidelines, analyzing data using your organization's specific workflows, or automating personal tasks.
- Format specification for Agent Skills:
	- https://agentskills.io/specification
	- https://agentskills.io/skill-creation/best-practices
	- https://agentskills.io/skill-creation/optimizing-descriptions
	- https://agentskills.io/skill-creation/using-scripts
- Here is a great meta-skill example: `/Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/think/thinking`

## Create

A meta-skill named **[NAME]** that [PURPOSE].

Sub-skills:
1. **[ModeA]** -- [what it does, when to use it]
2. **[ModeB]** -- [what it does, when to use it]
3. **[ModeC]** -- [what it does, when to use it]
