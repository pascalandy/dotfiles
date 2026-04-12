- Document defines the Superpowers meta-skill entry point and harness-agnostic routing for 13 lifecycle specialists, each tied to a purpose and example invocation.
- Lifecycle and invocation tables map request intentions (e.g., “help me think through this feature”) to specialist skills.
- Router table in `references/ROUTER.md` links request patterns to `references/<skill>/MetaSkill.md`, enforcing that those sub-skill artifacts exist.
- Core rules emphasize loading the router before acting, honoring instruction priority (user > workspace/repo > workflow collection), and keeping references harness-neutral.
- Highlights include single entry point, prioritized instructions, and explicit trigger phrases per specialist.

### Structure / Sections Summary
1. **Reason & Raw Concept** – Motivations, changes, key files, flow, timestamp, and author.
2. **Narrative**
   - **Structure** – Lifecycle table with 13 specialists, invocation scenarios mapped to skills, and router table detailing request patterns → `MetaSkill` documents.
   - **Dependencies** – Router table is central; each route requires corresponding sub-skill artifact.
   - **Highlights** – Emphasizes single entry, instruction priority, and trigger phrases.
   - **Rules** – Core operating principles for using the workflow collection.
3. **Facts** – Key conventions on router usage, instruction priority, and router table contents.

### Notable Entities / Patterns / Decisions
- **Entities:** Lifecycle specialists (`brainstorming`, `writing-plans`, `using-git-worktrees`, etc.) with specific purposes and trigger phrases.
- **Patterns/Decisions:** Router-driven dispatch ensures deterministic handling; additions require new subdirectories and router entries; instructions must remain harness-agnostic and reference local paths.
- **Decisions:** Prioritize direct user instructions, then workspace-level instructions, then workflow collection rules; router must be loaded before action.