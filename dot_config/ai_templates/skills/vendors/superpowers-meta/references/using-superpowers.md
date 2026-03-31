# Using Superpowers

> Establish how to find and use skills — invoke relevant skills BEFORE any response or action, including clarifying questions.

## When to Use

Applies at the start of every conversation and before every action. If there is even a 1% chance a skill might apply, invoke it. This is non-negotiable.

## Inputs

- The user's message or intended action.
- Access to the skill library (via your platform's skill-loading mechanism).

## Methodology

### Instruction Priority

1. **User's explicit instructions** (CLAUDE.md, GEMINI.md, AGENTS.md, direct requests) — highest priority
2. **Superpowers skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

If user instructions contradict a skill (e.g., user says "don't use TDD" but a skill says "always use TDD"), follow user instructions.

### The Rule

Invoke relevant or requested skills BEFORE any response or action. Even a 1% chance a skill might apply means you should invoke it to check. If an invoked skill turns out to be wrong for the situation, you don't need to use it.

### Decision Flow (text-based)

```
User message received
  └─> About to enter plan/design mode?
        ├─ YES → Already brainstormed?
        │          ├─ NO  → Invoke brainstorming skill
        │          └─ YES → continue to skill check
        └─ NO  → continue to skill check

Skill check: Might any skill apply?
  ├─ YES (even 1%) → Invoke skill via platform mechanism
  │                    └─> Announce: "Using [skill] to [purpose]"
  │                          └─> Skill has checklist?
  │                                ├─ YES → Create a tracked todo per checklist item
  │                                └─ NO  → Follow skill exactly
  └─ DEFINITELY NOT → Respond (including clarifications)
```

### Announcing Skill Usage

When you invoke a skill, announce it:  
`"I'm using [skill name] to [purpose]."`

### Skill Priority (when multiple apply)

1. **Process skills first** (brainstorming, debugging) — these determine HOW to approach the task  
2. **Implementation skills second** (frontend-design, specific builders) — these guide execution

Examples:
- "Let's build X" → brainstorming first, then implementation skills
- "Fix this bug" → debugging first, then domain-specific skills

### Skill Types

| Type | Examples | Behavior |
|------|----------|----------|
| **Rigid** | TDD, debugging | Follow exactly — do not adapt away discipline |
| **Flexible** | patterns | Adapt principles to context |

The skill itself tells you which type it is.

### How to Access Skills

- **Claude Code:** Use the `Skill` tool. Follow its content directly. Never read skill files manually.
- **Gemini CLI:** Use the `activate_skill` tool. Gemini loads metadata at session start and activates full content on demand.
- **Other environments:** Check platform documentation for skill loading.
- **Non-CC platforms:** See `references/codex-tools.md` for tool equivalents.

### Red Flags — STOP, you are rationalizing

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "I can check git/files quickly" | Files lack conversation context. Check for skills. |
| "Let me gather information first" | Skills tell you HOW to gather information. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Read current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Invoke it. |

### User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" does not mean skip workflows.

### Subagent Exception

If you were dispatched as a subagent to execute a specific task, skip this skill.

## Quality Gates

- Skill check performed BEFORE any response (including clarifying questions)
- Relevant skill invoked when ≥1% chance it applies
- Skill usage announced
- Checklist items tracked as todos (if skill has checklist)
- Skill followed exactly (rigid type) or principles adapted (flexible type)

## Outputs

- Correct skill(s) loaded and active before work begins
- Announced skill usage
- Todo list created from any checklists

## Feeds Into

Every other skill — this skill gates entry to all others.

## Harness Notes

Platform tool names differ (Skill tool vs activate_skill vs other mechanisms). The principle is identical across platforms: load skill content before proceeding, never rely on memory of previous skill versions.
