---
children_hash: c2f3bd3c778a99e0d8ee12e24d47780d5479c0ef49b20b5ff23b53afbd15b83f
compression_ratio: 0.6879334257975035
condensation_order: 2
covers: [context.md, skill_reorg/_index.md]
covers_token_total: 721
summary_level: d2
token_count: 496
type: summary
---
## Domain: ideas
- **Purpose & Scope (context.md)**: Governs the reorganization proposals for ByteRover’s 62-skill catalog, detailing current buckets (`meta`, `pa-sdlc`, `specs`, `utils`) and planned expanded partitions (`knowledge`, `dev`, `think`, `spec` with diacritic sub-buckets). Includes move tables for relocating each skill; excludes execution notes or unrelated feature discussions. Owned by ByteRover context engineering; consult this domain when evaluating future taxonomy revisions.

## Topic: skill_reorg (overview / context)
- **Current vs. Future Buckets (skill_reorg/_index.md)**: The existing single-level buckets are reinterpreted into a four-partition taxonomy:
  - `knowledge`: Research, vault, memory, and filesystem tooling.
  - `dev`: Lifecycle/code/review/docs/headless/browser/system/media/research/diagram/task/util subdivisions.
  - `think`: Reasoning, content, documentation, and distillation expertise.
  - `spec`: Process/design/score-focused areas.
  Key entities include `vault`, `obsidian`, `qaqmd`, `pg-memory`, `bynover`, `nia-docs`, etc.
- **Moves Table (skill_reorganization_proposal.md)**: Each skill’s origin bucket and deterministic destination partition/subcategory are cataloged, mapping current skills (e.g., `color-palette`, `eval-rubric`, `distill`, `transcript-sk`) into their new homes such as `dev/docs`, `think/distill`, or `knowledge/memory`.
- **Facts Highlights**:
  - Meta → `think` (e.g., `thinking`, `creative`, `marketing`, `ContentAnalysis`, `investigation`, `liteparse`).
  - PA-SDLC → `knowledge` or `think` (`obsidian`, `wiki-map`, `qmd`, `distill*`).
  - Utils → `knowledge` (`pg-memory`, `byterover`, `nia-docs`, `map-filesystem-abstract`, `cass`) or `think/distill` (`writer-sk`, `simple-editor`, `transcript-sk`).
- **Relationships**: The document ties the conceptual buckets to specific skills via structured move tables, enabling drill-down into `skill_reorganization_proposal.md` for precise per-skill reassignment logic.