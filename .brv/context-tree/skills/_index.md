---
children_hash: ffea8d09d557147698943269521332bf66061565dde600688e2129764976b0cc
compression_ratio: 0.939203354297694
condensation_order: 2
covers: [context.md, organization/_index.md]
covers_token_total: 477
summary_level: d2
token_count: 448
type: summary
---
# skills Domain Structural Summary (Level d2)

## Domain Purpose & Ownership
- **skills/context.md** captures ByteRover’s canonical skill taxonomy, documenting both legacy categories and the planned future domains (knowledge, dev, think, spec) to guide discovery and migration.
- Overseen by the **Knowledge Engineering team**, this domain excludes implementation/operation guides, focusing solely on category structure, migration plans, and placement rules.
- Used whenever stakeholders need the authoritative mapping or placement decisions for skills.

## Key Structural Nodes
- **`context.md`** – Provides the procedural overview of the skill reorganization process, including the scope of included legacy categories (meta, pa-sdlc, specs, utils), planned future subdomains, and the rationale for filtering out implementation details.
- **`organization/_index.md`** – Acts as the d1 summary node that links to the two primary child entries:
  - **`context.md`** for procedural context and high-level mapping rationale.
  - **`skill_reorganization_proposal.md`** for the comprehensive narrative, dependencies, highlights, and the exhaustive Moves table detailing where each of the 62 legacy skills migrates (e.g., `changelog` → `dev/docs/`, `council` → `spec/process/`), preserving ownership coordination requirements.

## Relationships & Patterns
- **Legacy-to-Future Moves** are centralized in `skill_reorganization_proposal.md`, ensuring each legacy category’s target domain (knowledge/dev/think/spec) and ownership dependencies remain traceable.
- **Usage guidance** is enforced by the domain spec: consult `context.md` for taxonomy questions and `skill_reorganization_proposal.md` for execution-level moves, ensuring consistent reference points for planning and discovery activities.