---
children_hash: b1e67ae062d098c717350d5fff0ffb94b2d9b2e9b7a8b9f1ddaaeb01bdb593d2
compression_ratio: 0.4602941176470588
condensation_order: 3
covers: [ideas/_index.md, skills/_index.md]
covers_token_total: 1360
summary_level: d3
token_count: 626
type: summary
---
### Domain: ideas  
- **Purpose & Scope**: Guides the 62-skill taxonomy reorg, describing the legacy buckets (`meta`, `pa-sdlc`, `specs`, `utils`) and planned four-partition future domain structure (`knowledge`, `dev`, `think`, `spec` with subcategories). Consult `context.md` for overall governance and move exclusion rules.  
- **Skill Reorg Topic**:  
  - Future buckets break down into focused partitions (e.g., `knowledge` for research/vault/memory tooling, `dev` for lifecycle/code/docs utilities, `think` for reasoning/content, `spec` for process/design/score). Key entities like `vault`, `obsidian`, `qaqmd`, and `bynover` anchor each bucket.  
  - Moves table in `skill_reorganization_proposal.md` catalogs every skill’s legacy origin and deterministic destination (e.g., `color-palette` → `dev/docs`, `distill` → `think/distill`, `transcript-sk` → `think/distill`).  
  - Highlights track bucket-level migrations (Meta → `think`, PA-SDLC → `knowledge`/`think`, Utils → `knowledge` or `think/distill`) and preserve relationships between conceptual buckets and specific skills for drill-down.

### Domain: skills  
- **Purpose & Scope**: Serves as the canonical record of skill categories and upcoming taxonomy migrations; includes legacy mapping, new domain coverage, and move tables. See `context.md` for domain-level usage guidance.  
- **Topic: meta_superpowers**:  
  - `superpowers_context.md` defines the superpower meta-skill router, enforcing instruction hierarchy and referencing lifecycle specialists.  
  - `superpowers_workflow.md` details the flow (`user request → SKILL entry → router → references/<skill>/MetaSkill.md → specialist`), includes source files (`.agents/skills/meta/superpowers/SKILL.md`, `references/ROUTER.md`), and documents lifecycle/trigger/routing tables. Highlights emphasize the single entrypoint, 13 specialists, fixed trigger phrases, router-first requirement, and harness-neutral references, enabling precise drill-down.  
- **Topic: organization**:  
  - Overview captures the April 11, 2026 reorganization proposal restructuring legacy groups into future domains.  
  - `context.md` lays out process rationale, while `skill_reorganization_proposal.md` delivers the full narrative, dependencies, and exhaustive 62-skill Moves table (e.g., `changelog` → `dev/docs/`, `council` → `spec/process/`).  
  - Relationships: Moves table enforces legacy-to-future mappings and highlights coordination/dependency expectations with existing owners during migration.