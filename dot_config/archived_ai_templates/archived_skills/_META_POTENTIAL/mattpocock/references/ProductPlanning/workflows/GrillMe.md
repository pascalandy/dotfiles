# GrillMe

Relentlessly interview the user about a plan or design until every branch of the decision tree is resolved.

## Process

Interview the user about every aspect of their plan until reaching shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one by one.

### Rules

1. **Ask questions one at a time** -- never batch questions. Wait for an answer before asking the next.

2. **Provide your recommended answer** -- for each question, state what you would recommend and why, then ask if the user agrees or has a different view.

3. **Explore the codebase first** -- if a question can be answered by reading code, exploring the repository, or checking existing patterns, do that instead of asking.

4. **Follow dependency order** -- resolve foundational decisions before dependent ones. If decision B depends on decision A, ask about A first.

5. **Do not stop early** -- continue until every branch of the decision tree is resolved. If you are unsure whether a branch is resolved, ask a clarifying question.

6. **Challenge weak answers** -- if the user gives a vague or hand-wavy answer, push back with a concrete alternative or ask for specifics.

### What to Cover

Systematically walk through:

- **Problem framing** -- Is the problem well-defined? Are there hidden assumptions?
- **Scope boundaries** -- What is explicitly out of scope? Where is scope creep hiding?
- **Key decisions** -- What are the architectural choices? What alternatives exist?
- **Trade-offs** -- What are you giving up with each decision? Is the trade-off worth it?
- **Edge cases** -- What happens when things go wrong? What are the failure modes?
- **Dependencies** -- What does this depend on? What depends on this?
- **Testing strategy** -- How will you verify this works? What makes a good test here?

### Output

No written artifact. The value is the refined, shared understanding produced by the grilling session. The user will use this understanding to inform PRDs, plans, or implementation.
