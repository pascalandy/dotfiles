---
name: TDD
description: Test-driven development with red-green-refactor vertical slices. Integration-style tests through public interfaces, boundary-only mocking, deep module design for testability. USE WHEN TDD, test-driven development, red-green-refactor, test-first, integration tests, write tests, tracer bullet, build feature with tests, fix bug with tests.
---

## Status Update

When beginning a workflow, emit:
`Running the **RedGreenRefactor** workflow in the **TDD** skill to [ACTION]...`

# Test-Driven Development

Vertical-slice red-green-refactor loops that build features or fix bugs one thin slice at a time. Tests verify behavior through public interfaces, not implementation details.

## Core Philosophy

**Good tests** are integration-style: exercise real code paths through public APIs. They describe _what_ the system does, not _how_.

**Bad tests** are coupled to implementation: mock internal collaborators, test private methods, verify call counts. They break when you refactor without changing behavior.

## Anti-Pattern: Horizontal Slices

DO NOT write all tests first, then all implementation. This produces tests disconnected from design. Correct approach: vertical slices via tracer bullets. One test, one implementation, repeat.

## Workflow Routing

| Intent | Workflow |
|--------|----------|
| Build a feature or fix a bug using TDD | `workflows/RedGreenRefactor.md` |

## Supporting References

| Reference | Purpose |
|-----------|---------|
| `references/TestPhilosophy.md` | Good vs bad tests, integration over unit, behavior over implementation |
| `references/InterfaceDesign.md` | Designing interfaces for natural testability |
| `references/Mocking.md` | When to mock (system boundaries only) and when not to |
| `references/Refactoring.md` | What to look for in the refactor phase |
| `references/DeepModules.md` | Deep module philosophy for design decisions during TDD |

## Checklist Per Cycle

Every RED-GREEN cycle must satisfy:

- [ ] Test describes behavior, not implementation
- [ ] Test uses public interface only
- [ ] Test would survive an internal refactor
- [ ] Code is minimal for this test (no speculative features)
- [ ] No refactoring while RED -- only after GREEN
