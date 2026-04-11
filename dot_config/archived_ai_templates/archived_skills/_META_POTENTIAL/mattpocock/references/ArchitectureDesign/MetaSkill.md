---
name: ArchitectureDesign
description: Module interface design and codebase architecture improvement -- generate radically different interface designs, find deep-module refactoring opportunities, plan refactors as tiny commits, and extract DDD ubiquitous language. USE WHEN design interface, design it twice, module interface, API design, deep modules, shallow modules, improve architecture, testability, refactor plan, refactoring RFC, tiny commits, ubiquitous language, DDD, domain model, glossary, canonical terms.
---

## Status Update

When beginning a workflow, emit:
`Running the **[WorkflowName]** workflow in the **ArchitectureDesign** skill to [ACTION]...`

# Architecture Design

Four workflows for designing, improving, and documenting software architecture. Grounded in Ousterhout's deep module philosophy, Fowler's tiny-commit refactoring, and Evans' domain-driven design.

## Core Principles

- **Design it twice** -- Your first idea is unlikely to be the best. Generate multiple radically different options, then compare. (Ousterhout, "A Philosophy of Software Design")
- **Deep over shallow** -- A deep module has a small interface hiding significant complexity (good). A shallow module has a large interface with thin implementation (avoid). See `references/DeepModules.md`.
- **Tiny commits** -- Each refactoring step as small as possible (Fowler). Every commit leaves the codebase in a working state.
- **Durable decisions** -- Describe modules, interfaces, and architectural decisions. No file paths or line numbers -- they go stale.

## Workflow Routing

| Intent | Workflow |
|--------|----------|
| Design a module interface, compare API options | `workflows/DesignInterface.md` |
| Find architectural improvements, deepen shallow modules | `workflows/ImproveArchitecture.md` |
| Plan a refactor with tiny commits | `workflows/RequestRefactor.md` |
| Extract domain terminology into a ubiquitous language glossary | `workflows/UbiquitousLanguage.md` |

## Output Format

- **DesignInterface** -- 3+ interface designs with signatures, usage examples, hidden complexity analysis, and trade-off comparison
- **ImproveArchitecture** -- Candidate list of deepening opportunities, followed by a GitHub issue RFC for the selected candidate
- **RequestRefactor** -- GitHub issue with: Problem Statement, Solution, Tiny Commit Plan, Decision Document, Testing Decisions, Out of Scope
- **UbiquitousLanguage** -- `UBIQUITOUS_LANGUAGE.md` with grouped term tables, relationships with cardinality, example dialogue, and flagged ambiguities
