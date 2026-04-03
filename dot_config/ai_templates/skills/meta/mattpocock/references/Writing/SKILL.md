---
name: Writing
description: Technical writing workflows -- edit articles for clarity and information dependency ordering, and create new agent skills with proper structure and progressive disclosure. USE WHEN edit article, revise article, improve article, restructure sections, tighten prose, write skill, create skill, build skill, skill structure, agent skill.
---

## Status Update

When beginning a workflow, emit:
`Running the **[WorkflowName]** workflow in the **Writing** skill to [ACTION]...`

# Writing

Two workflows for structured technical writing: article editing and skill creation.

## Workflow Routing

| Intent | Workflow |
|--------|----------|
| Edit or improve an article draft | `workflows/EditArticle.md` |
| Create a new agent skill with proper structure | `workflows/WriteASkill.md` |

## Output Format

- **EditArticle** -- Revised article with sections reordered for information dependency, paragraphs capped at 240 characters, improved clarity and flow
- **WriteASkill** -- Skill directory with SKILL.md, optional reference files, and optional scripts following progressive disclosure structure
