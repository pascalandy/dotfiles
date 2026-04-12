---
children_hash: fcfa1401f2ed9c3e426297346c8668461772e4628a837e6d99dcdee2e4642313
compression_ratio: 0.2568858909499719
condensation_order: 1
covers: [context.md, superpowers_workflow.md]
covers_token_total: 1779
summary_level: d1
token_count: 457
type: summary
---
### meta_superpowers (context.md)
- Describes the Superpowers meta-skill entrypoint that routes harness-agnostic requests through a shared router ledger, prioritizing direct user/workspace instructions before the Superpowers rule set.
- Contains the lifecycle table (13 specialists with purposes) and router dispatch table mapping request patterns to `references/<skill>/MetaSkill.md`.
- Points to the organizational context in `skills/organization/skill_reorganization_proposal.md` for broader taxonomy.

### Superpowers Workflow (superpowers_workflow.md)
- Documents the entryflow: `User request → Superpowers SKILL entry → Router selection → Delegate to references/<skill>/MetaSkill.md → Specialist workflow`.
- Raw concept details include task focus, recent additions (harness-agnostic routing, 13 specialists, router mappings), related source files (`.agents/skills/meta/superpowers/SKILL.md`, `references/ROUTER.md`), timestamp, and author.
- Narrative structure:
  - Lifecycle table enumerates specialists, purposes, and phases (Design through Skill Authoring).
  - Invocation table lists trigger phrases and the corresponding specialist routes.
  - Routing table mirrors request patterns to specific `references/<skill>/MetaSkill.md` files, referencing each skill entry for drill-down details.
  - Dependencies highlight that the router table is the workflow node and requires the referenced sub-skill artifacts.
  - Highlights emphasize the single prioritized entrypoint, the 13 specialists, and exact trigger phrases.
  - Rules preserve exact instructions: load the router first, obey instruction priority, add specialists by creating directories/router entries, and keep references harness-neutral with local paths.
- Facts recorded cover router usage, instruction priority, and existence of the 13-row router table.