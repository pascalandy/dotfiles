# DesignInterface

Generate multiple radically different interface designs for a module using parallel sub-agents. Based on "Design It Twice" from Ousterhout's "A Philosophy of Software Design": your first idea is unlikely to be the best.

## Process

### 1. Gather Requirements

Before designing, understand:

- [ ] What problem does this module solve?
- [ ] Who are the callers? (other modules, external users, tests)
- [ ] What are the key operations?
- [ ] Any constraints? (performance, compatibility, existing patterns)
- [ ] What should be hidden inside vs exposed?

Ask: "What does this module need to do? Who will use it?"

### 2. Generate Designs (Parallel Sub-Agents)

Spawn 3+ sub-agents simultaneously. Each must produce a **radically different** approach -- not minor variations.

Prompt template for each sub-agent:

```
Design an interface for: [module description]

Requirements: [gathered requirements]

Constraints for this design: [one of the constraints below]

Output format:
1. Interface signature (types/methods)
2. Usage example (how caller uses it)
3. What this design hides internally
4. Trade-offs of this approach
```

Assign each agent a different constraint:
- Agent 1: "Minimize method count -- aim for 1-3 methods max"
- Agent 2: "Maximize flexibility -- support many use cases"
- Agent 3: "Optimize for the most common case"
- Agent 4 (optional): "Take inspiration from [specific paradigm/library]"

### 3. Present Designs

Show each design sequentially so the user can absorb each approach before comparison:
1. **Interface signature** -- types, methods, parameters
2. **Usage examples** -- how callers use it in practice
3. **What it hides** -- complexity kept internal

### 4. Compare Designs

After showing all designs, compare on:

- **Interface simplicity** -- fewer methods, simpler params = easier to learn and use correctly
- **General-purpose vs specialized** -- flexibility vs focus
- **Implementation efficiency** -- does the interface shape allow efficient internals?
- **Depth** -- small interface hiding significant complexity (good) vs large interface with thin implementation (bad)
- **Ease of correct use** vs **ease of misuse**

Discuss trade-offs in prose, not tables. Highlight where designs diverge most.

## Evaluation Criteria

From "A Philosophy of Software Design":

**Interface simplicity:** Fewer methods, simpler params = easier to learn and use correctly.

**General-purpose:** Can handle future use cases without changes. But beware over-generalization.

**Implementation efficiency:** Does interface shape allow efficient implementation? Or force awkward internals?

**Depth:** Small interface hiding significant complexity = deep module (good). Large interface with thin implementation = shallow module (avoid).

### 5. Synthesize

Often the best design combines insights from multiple options. Ask:
- "Which design best fits your primary use case?"
- "Any elements from other designs worth incorporating?"

## Anti-Patterns

- Do not let sub-agents produce similar designs -- enforce radical difference
- Do not skip comparison -- the value is in contrast
- Do not implement -- this is purely about interface shape
- Do not evaluate based on implementation effort -- focus on caller experience
