# Specification-Driven Development (SDD)

## Core Idea

Specs are the source of truth. Code serves specs, not the other way around.

Traditional: code is king, specs are scaffolding discarded after coding.
SDD: specs generate code. Implementation plan derives from spec. Code is output.

## Why Now

1. **AI capability threshold**: natural language → working code is reliable
2. **Complexity growth**: dozens of services/deps need systematic alignment
3. **Pace of change**: pivots happen; regenerating from spec beats manual rewrites

## Core Principles

- **Specs as lingua franca**: primary artifact; code is expression in a language
- **Executable specs**: precise, complete, unambiguous → generate working systems
- **Continuous refinement**: AI analyzes specs for gaps, contradictions, ambiguity
- **Research-driven context**: agents gather tech options, constraints, best practices
- **Bidirectional feedback**: production metrics/incidents inform spec evolution
- **Branching for exploration**: same spec → multiple implementation approaches

## The Workflow

1. **Idea → Spec**: iterative dialogue with AI; clarify, define acceptance criteria
2. **Research**: agents investigate libraries, performance, security, org constraints
3. **Spec → Plan**: map requirements to tech decisions; every choice has rationale
4. **Plan → Tasks**: break down into executable, parallelizable work items
5. **Generate Code**: as soon as specs are stable enough (not necessarily complete)
6. **Feedback Loop**: production reality updates specs for next iteration

## Key Differentiators

- **Gap elimination**: no gap between intent and implementation
- **Requirement changes = normal workflow**: not disruptions
- **What-if experiments**: simulate business pivots before committing
- **Living documentation**: specs stay in sync because they generate code

## Template Power

Templates constrain LLM output toward quality:

- Prevent premature implementation details (focus on WHAT, not HOW)
- Force explicit uncertainty markers `[NEEDS CLARIFICATION]`
- Structured checklists catch gaps systematically
- Constitution gates prevent over-engineering
- Test-first thinking baked in

## Constitution

Immutable principles governing how specs become code:

- Library-first: features start as standalone libraries
- CLI interface: every library exposes text I/O
- Test-first (non-negotiable): tests before implementation
- Simplicity: max 3 projects initially; justify complexity
- Integration-first testing: real environments over mocks

## The Transformation

Not replacing developers. Amplifying capability by automating mechanical translation.
Tight feedback loop: specs, research, code evolve together.
Each iteration brings deeper understanding and better alignment.
