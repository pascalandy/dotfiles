# Deep Modules in TDD

From John Ousterhout, "A Philosophy of Software Design."

## The Principle

A **deep module** has a small interface hiding a large implementation. This is the goal during TDD design decisions.

A **shallow module** has a large interface with little implementation. Avoid creating these during TDD.

```
Deep module:            Shallow module:
┌─────────┐            ┌──────────────────────┐
│Interface│            │     Interface         │
├─────────┤            ├──────────────────────┤
│         │            │   Implementation     │
│  Impl.  │            └──────────────────────┘
│         │
│         │
│         │
└─────────┘
Small interface,        Large interface,
lots of functionality   little functionality
```

## During TDD, Ask

When designing the interface for the code you are about to test:

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?

## TDD Implication

Deep modules are naturally more testable:
- Fewer methods = fewer tests needed to cover the interface
- Simpler parameters = simpler test setup
- Hidden complexity = tests focus on behavior, not internals
- Clean interface = tests read like specifications

Shallow modules create testing friction:
- Many small methods each needing their own test
- Complex wiring between modules requiring mocks
- Tests coupled to internal structure that break on refactor
