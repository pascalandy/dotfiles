---
children_hash: 2cfb5c32791b8fef8bb30360463aa6ea0a18c2dd8634d25fa0949045cee38816
compression_ratio: 0.4357142857142857
condensation_order: 1
covers: [context.md, skill_reorganization_proposal.md]
covers_token_total: 1120
summary_level: d1
token_count: 488
type: summary
---
## skill_reorg Overview
- **Current structure (context.md / skill_reorganization_proposal.md)**: Four buckets—`meta`, `pa-sdlc`, `specs`, `utils`—cover the existing 62-skill landscape. Each bucket lists its skills in single-bullet format to feed the move analysis.
- **Future structure definition**: Reframes the taxonomy into four partitions (`knowledge`, `dev`, `think`, `spec`), with `dev` further subdivided into lifecycle/code/review/docs/headless/browser/system/media/research/diagram/task/util and `think` covering reasoning/content/doc/distill. `knowledge` and `spec` capture medium- to long-term research, documentation, and process/design/score concerns.

## Moves Table (skill_reorganization_proposal.md)
- **Purpose**: Maps every skill from its current bucket to a precise destination partition/subcategory without altering the underlying table entries.
- **Key migrations**:
  - `specs` skills like `changelog`, `eval-rubric`, `color-palette` move into `dev/docs`, `dev/review`, `spec/design`, etc.
  - `meta` skills (`thinking`, `creative`, `marketing`, `ContentAnalysis`, `investigation`, `liteparse`) migrate to `think` subcategories (reasoning/content/doc).
  - `pa-sdlc` skills (`obsidian`, `wiki-map`, `qmd`, `distill`, `distill-prompt`) refocus into `knowledge` (vault) or `think/distill`.
  - `utils` (e.g., `pg-memory`, `byterover`, `nia-docs`, `map-filesystem-abstract`, `cass`, `writer-sk`, `simple-editor`, `transcript-sk`) split across `knowledge` (memory/fs/browse) and `think/distill`.

## Facts Highlight (skill_reorganization_proposal.md)
- **Current meta skills**: `thinking`, `creative`, `marketing`, `ContentAnalysis`, `investigation`, `liteparse`.
- **Future knowledge bucket contents**: `vault`, `obsidian`, `wiki-map`, `qmd`, `pg-memory`, `byterover`, `nia-docs`, `map-filesystem-abstract`, `cass`.
- **Moves mapping**: Provides deterministic origin→destination assignments for each skill, supporting the new taxonomy.