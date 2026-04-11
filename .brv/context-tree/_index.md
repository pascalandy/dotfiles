---
children_hash: 3af54f1f41580dc087d4025bee68de639574eda56b7c372459447b67200ae838
compression_ratio: 0.6323119777158774
condensation_order: 3
covers: [ideas/_index.md, skills/_index.md]
covers_token_total: 1077
summary_level: d3
token_count: 681
type: summary
---
# Structural Summary of ByteRover Skill Taxonomy (Level d3)

## Domain: ideas
- **Purpose & Scope** (`ideas/context.md`): Governs ByteRover’s 62-skill catalog reorganization, defining source buckets (`meta`, `pa-sdlc`, `specs`, `utils`) and the new four-partition taxonomy (`knowledge`, `dev`, `think`, `spec` with diacritic sub-buckets). Contains relocation tables for every skill; excludes execution details. Owned by ByteRover context engineering for taxonomy revisions.
- **Topic: skill_reorg**
  - **Current vs. Future Buckets** (`ideas/skill_reorg/_index.md`): Maps existing buckets to four partitions, with each partition covering specific skill domains (e.g., `knowledge` for research/vault/memory tooling; `dev` covering lifecycle/code/docs/headless/diagram/task utilities; `think` for reasoning/content/distillation; `spec` for process/design/score).
  - **Moves Table** (`ideas/skill_reorganization_proposal.md`): Lists deterministic origin-to-target assignments (e.g., `color-palette`→`dev/docs`, `distill`→`think/distill`, `transcript-sk`→`think/distill`). Enables traceable drill-down into how each legacy skill migrates.
  - **Facts & Relationships**: Meta skills largely move into `think`; PA-SDLC skills target `knowledge`/`think`; Utils split between `knowledge` (“pg-memory”, “bynover”) and `think/distill` (“writer-sk”, “edit-note”). Move tables tie bucket concepts directly to target partitions, ensuring precise reassignment logic.

## Domain: skills
- **Purpose & Ownership** (`skills/context.md`): Captures the canonical skill taxonomy, documenting both legacy categories and future domains (knowledge/dev/think/spec) for discovery and migration; maintained by Knowledge Engineering, excluding implementation details.
- **Structural Nodes**
  - **Procedural Overview** (`skills/context.md`): Reiterates included legacy buckets, planned partitions, and rationale for excluding operational content.
  - **Organization Summary** (`skills/organization/_index.md`): Acts as the level-1 hub linking to both the procedural context and the detailed `skill_reorganization_proposal.md`.
  - **Detailed Moves** (`skills/organization/skill_reorganization_proposal.md`): Provides narrative, dependencies, highlights, and the exhaustive Moves table (e.g., `changelog`→`dev/docs/`, `council`→`spec/process/`), ensuring each legacy skill’s future domain and any ownership coordination are explicit.
- **Patterns & Relationships**: Legacy-to-future moves are centralized, enforcing consistent reference points—`skills/context.md` for taxonomy questions and `skills/organization/skill_reorganization_proposal.md` for execution-level assignments—thus preserving ownership and placement rules across the migration effort.