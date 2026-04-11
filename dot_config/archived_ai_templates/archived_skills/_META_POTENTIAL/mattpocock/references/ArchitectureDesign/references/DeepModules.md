# Deep Modules

From John Ousterhout, "A Philosophy of Software Design."

## The Core Idea

A **deep module** has a small interface hiding a large implementation. This is good. Callers interact through a simple API while significant complexity is managed internally.

A **shallow module** has a large interface with little implementation. This is bad. The interface is nearly as complex as what it hides, providing little abstraction value.

## When Designing Interfaces, Ask

- Can I reduce the number of methods?
- Can I simplify the parameters?
- Can I hide more complexity inside?
- Is the interface simpler than the implementation it hides?
- Would a caller need to understand the internals to use this correctly?

## Dependency Categories

When consolidating shallow modules into deep ones, classify dependencies:

### 1. In-Process
Pure computation, in-memory state, no I/O. Always deepenable. Test directly.

### 2. Local-Substitutable
Dependencies with local test stand-ins (e.g., PGLite for Postgres, SQLite for SQL). Deepenable with local substitution in tests.

### 3. Remote but Owned (Ports & Adapters)
Your own services across a network boundary. Define a port (interface), inject the transport. Test through the port with a local adapter.

### 4. True External (Mock)
Third-party services you do not control. Mock at the boundary. This is the ONLY place mocking is appropriate.

## Testing Strategy

**Replace, don't layer.** Old unit tests on shallow modules become waste once boundary tests on the consolidated deep module exist. Delete the old tests -- they test implementation details that no longer exist as separate units.
