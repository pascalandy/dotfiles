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
├── SKILL.md              # Layer 1: Collection (rich docs, invocation scenarios, examples)
└── references/
    ├── ROUTER.md          # Layer 2: Router (pure routing table, ~20 lines)
    ├── [ModeA]/           # Layer 3: Sub-skill 1 (complete, standalone)
    │   ├── SKILL.md       # Classic skill (format specification for Agent Skills)
    │   ├── workflows/     # Discrete workflow files (optional)
    │   ├── references/    # Supporting context (optional)
    │   ├── scripts/       # Scripts (optional)
    │   ├── templates/     # User templates (optional)
    │   └── assets/        # Assets (optional)
    ├── [ModeB]/           # Layer 3: Sub-skill 2
    │   ├── SKILL.md
    │   └── workflows/
    └── [ModeC]/           # Layer 3: Sub-skill 3
        ├── SKILL.md
```

Sub-skills may include any combination of: `workflows/`, `references/`, `scripts/`, `templates/`, `assets/`.

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
| keyword1, keyword2, keyword3 | `[ModeA]/SKILL.md` |
| keyword4, keyword5 | `[ModeB]/SKILL.md` |
| keyword6, keyword7, keyword8 | `[ModeC]/SKILL.md` |
```

The router's `USE WHEN` aggregates ALL keywords from ALL sub-skills. The routing table narrows to the specific one.

## Sub-Skill SKILL.md

Each sub-skill follows Anthropic's skill anatomy and works standalone or via the router:

- YAML frontmatter with name and description (including its own `USE WHEN` scoped to its domain)
- Core concept explaining the methodology
- Workflow routing (maps intent → files in `workflows/`)
- Output format specification
- Examples
- No domain overlap with sibling sub-skills

## Design Rules

1. **Single entry point** -- user invokes the meta-skill name, never a sub-skill directly
2. **Invisible delegation** -- router picks the right specialist automatically
3. **No domain overlap** -- each sub-skill owns distinct territory
4. **Consistent interface** -- all sub-skills follow the same internal structure
5. **Additive scaling** -- adding a sub-skill means one new directory + one new row in the routing table

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
- Here is a great meta-skill example: `/Users/andy16/.local/share/chezmoi/dot_config/ai_templates/skills/meta/thinking`

## Create

A meta-skill named **[NAME]** that [PURPOSE].

Sub-skills:
1. **[ModeA]** -- [what it does, when to use it]
2. **[ModeB]** -- [what it does, when to use it]
3. **[ModeC]** -- [what it does, when to use it]

--

Finally, create a list that is checkable:

- [ ] Sequential go through every steps of these instructions, plan, an create a list of tasks
- [ ] Sequential go through every tasks, execute them carefully
