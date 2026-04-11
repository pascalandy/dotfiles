---
name: pa-doc-update
description: Universal documentation meta-skill for creating or updating documentation tied to a concrete change, decision, incident, or artifact across repositories, websites, content systems, project-management workspaces, knowledge bases, or personal workflows. USE WHEN update docs for this change, capture what changed, release notes, changelog, sync shipped changes, ADR, decision record, why did we choose this, postmortem, lessons learned, document this module, document this workflow as it works today, update this reference doc to match current state, document this page or board.
---

# Doc

## Routing

| Request Pattern | Route To |
|---|---|
| clean up docs, deduplicate docs, refresh stale docs across the repo, audit documentation, reorganize docs, fix frontmatter, repair routing tables, documentation governance | out of scope -> hand off to `pa-doc-cleaner` or to `ce-compound-refresh`, `docs-cleaner`, `doc-organizer`, or `learned-docs`; if unavailable, state that the request is outside `pa-doc-update` |
| explore this project, figure out what needs to change, define the feature, write the implementation plan, implement the change | out of scope -> hand off to `pa-scout`, `pa-scope`, `pa-vision`, `pa-architect`, or `pa-implement` as appropriate; if unavailable, state that the request is outside `pa-doc-update` |
| update the docs for this change, capture what changed, document this fix, release notes, changelog, sync docs after shipping, post-ship docs, capture the shipped changes, document what we just changed | `ChangeCapture/MetaSkill.md` |
| adr this, record this decision, why did we choose this, capture the rationale, write a postmortem, lessons learned, incident review, tradeoffs and consequences | `RationaleCapture/MetaSkill.md` |
| document this module as it works today, document this component as it exists now, document this workflow as it works today, document this page, explain this artifact in documentation form, write current-state reference docs for this thing, update this reference doc to match current state | `ArtifactDocumenter/MetaSkill.md` |
