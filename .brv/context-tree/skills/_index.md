---
children_hash: de2c8f53b5fd8bcc648fe27300ee4d9aef38a9e69cbcf09215177acaaa69ec55
compression_ratio: 0.757607555089192
condensation_order: 2
covers: [context.md, meta_superpowers/_index.md, organization/_index.md]
covers_token_total: 953
summary_level: d2
token_count: 722
type: summary
---
# skills Domain (d2 Structural Summary)

## Domain Purpose & Usage
- **Purpose**: Tracks ByteRover skill categorization and planned taxonomy migrations to ensure canonical references for discovery and planning.
- **Scope**: Includes legacy category membership, future domains (knowledge, dev, think, spec), and complete move mappings; excludes implementation/operation guides.
- **Ownership & Usage**: Owned by Knowledge Engineering; consult when referencing taxonomy or planning skill placements.

## meta_superpowers Topic
- **Entrypoint & Workflow**: `superpowers_context.md` defines the Superpowers meta-skill as a harness-agnostic router that respects workspace/user instructions before applying a fixed rule set; it references the lifecycle (13 specialists) and router dispatch tables that link request patterns to `references/<skill>/MetaSkill.md` nodes.
- **Workflow Details** (`superpowers_workflow.md`):
  - Flow: `User request → Superpowers SKILL entry → Router selection → Delegate to references/<skill>/MetaSkill.md → Specialist workflow`.
  - Raw concept metadata lists the task focus, recent routing additions, related source files (`.agents/skills/meta/superpowers/SKILL.md`, `references/ROUTER.md`), and timestamp/author.
  - Narrative structure:
    - Lifecycle table: 13 specialists covering Design through Skill Authoring phases.
    - Invocation table: maps trigger phrases to specialist routes.
    - Routing table: connects request patterns to specific `references/<skill>/MetaSkill.md` documents for drill-down.
    - Dependencies: router table as workflow node requiring referenced sub-skill artifacts.
    - Highlights & Rules: emphasize single prioritized entrypoint, 13 specialists, exact trigger phrases, instructions to load router first, obey instruction hierarchy, add specialists via directories/router entries, and keep references harness-neutral using local paths.
  - Facts preserved: router usage pattern, instruction priority, existence of a 13-row router table.

## organization Topic
- **Overview** (`_index.md`):
  - **Purpose**: Documents April 11, 2026 Skill Reorganization proposal moving legacy groups (meta, pa-sdlc, specs, utils) into future domains (knowledge, dev, think, spec).
  - **Content Structure**:
    - `context.md`: procedural summary and high-level legacy-to-future mapping.
    - `skill_reorganization_proposal.md`: full narrative, dependencies, highlights, and exhaustive Moves table covering all 62 skills.
  - **Key Relationships**:
    - Moves table preserves legacy→future mappings (e.g., `changelog` → `dev/docs/`, `council` → `spec/process/`).
    - Dependencies underline coordination with existing owners to maintain knowledge links during migration.
  - **Drill-Down Nodes**:
    - `context.md`: overview process and mapping.
    - `skill_reorganization_proposal.md`: detailed narrative and Moves table for each skill.