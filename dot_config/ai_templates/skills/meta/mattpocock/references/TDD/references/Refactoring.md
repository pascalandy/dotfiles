# Refactoring Candidates

After the TDD cycle (all tests GREEN), look for these refactoring opportunities:

## Patterns to Refactor

- **Duplication** -- Extract into a shared function or class. If two places do the same thing, one change should fix both.

- **Long methods** -- Break into private helpers. Keep tests on the public interface -- private helpers are implementation details.

- **Shallow modules** -- Combine tightly-coupled small modules into a deep module with a smaller total interface.

- **Feature envy** -- Logic that mostly uses data from another module. Move the logic to where the data lives.

- **Primitive obsession** -- Using raw strings, numbers, or booleans where a value object would add clarity and safety.

- **SOLID principles** -- Apply where natural. Single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion.

- **Existing code revealed as problematic** -- New code often exposes weaknesses in code it touches. If the new tests reveal that existing code is fragile, refactor it now while the context is fresh.

## Rules

- Never refactor while RED -- only after all tests pass
- Each refactoring step must be small enough that failure is easy to diagnose
- Run all tests after each step
- If a test fails after a refactoring step, undo and try a smaller step
- Commit after each successful refactoring step
