from this diagram

Use the pa-sdlc ASCII sequence diagram pattern for other process documentation. ASCII diagrams work in terminals, git commits, and anywhere graphical tools are unavailable.

Prefer sequence diagrams over activity diagrams. They show back-and-forth between user and system phases more clearly.

---

## pa-sdlc ASCII Sequence Diagram

```
       ┌─┐
       ║"│
       └┬┘
       ┌┼┐
        │             ┌────────┐           ┌─────────┐          ┌────────────┐           ┌────────┐           ┌────────────┐           ┌─────────────┐
       ┌┴┐            │pa-scout│           │pa-vision│          │pa-architect│           │pa-scope│           │pa-implement│           │pa-doc-update│
      User            └────┬───┘           └────┬────┘          └──────┬─────┘           └────┬───┘           └──────┬─────┘           └──────┬──────┘
        │ Need discovery?  │                    │                      │                      │                      │                        │
        │─────────────────>│                    │                      │                      │                      │                        │
        │                  │                    │                      │                      │                      │                        │
        │    Oriented      │                    │                      │                      │                      │                        │
        │<─ ─ ─ ─ ─ ─ ─ ─ ─│                    │                      │                      │                      │                        │
        │                  │                    │                      │                      │                      │                        │
        │           Need direction?             │                      │                      │                      │                        │
        │──────────────────────────────────────>│                      │                      │                      │                        │
        │                  │                    │                      │                      │                      │                        │
        │               Aligned                 │                      │                      │                      │                        │
        │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │                      │                      │                      │                        │
        │                  │                    │                      │                      │                      │                        │
        │                  │    Need planning?  │                      │                      │                      │                        │
        │─────────────────────────────────────────────────────────────>│                      │                      │                        │
        │                  │                    │                      │                      │                      │                        │
        │                  │        Roadmap     │                      │                      │                      │                        │
        │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                      │                      │                        │
        │                  │                    │                      │                      │                      │                        │
        │                  │                Need scoping?              │                      │                      │                        │
        │────────────────────────────────────────────────────────────────────────────────────>│                      │                        │
        │                  │                    │                      │                      │                      │                        │
        │                  │               Surface defined             │                      │                      │                        │
        │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │                      │                        │
        │                  │                    │                      │                      │                      │                        │
        │                  │                    │          Execute     │                      │                      │                        │
        │───────────────────────────────────────────────────────────────────────────────────────────────────────────>│                        │
        │                  │                    │                      │                      │                      │                        │
        │                  │                    │           Done       │                      │                      │                        │
        │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─│                        │
        │                  │                    │                      │                      │                      │                        │
        │                  │                    │                     Need docs?              │                      │                        │
        │────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────>│
        │                  │                    │                      │                      │                      │                        │
        │                  │                    │                      Updated                │                      │                        │
        │<─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
      User            ┌────┴───┐           ┌────┴────┐          ┌──────┴─────┐           ┌────┴───┐           ┌──────┴─────┐           ┌──────┴──────┐
       ┌─┐            │pa-scout│           │pa-vision│          │pa-architect│           │pa-scope│           │pa-implement│           │pa-doc-update│
       ║"│            └────────┘           └─────────┘          └────────────┘           └────────┘           └────────────┘           └─────────────┘
       └┬┘
       ┌┼┐
        │
       ┌┴┐
```

**Flow Summary:**

| Phase | Purpose |
|-------|---------|
| **pa-scout** | Discovery - Explore & orient in unfamiliar territory |
| **pa-vision** | Direction - Define where work is going |
| **pa-architect** | Planning - Turn direction into a roadmap |
| **pa-scope** | Scoping - Define the touch surface & blast radius |
| **pa-implement** | Execution - Apply bounded changes or fix bugs |
| **pa-doc-update** | Documentation - Update docs for recent changes |
