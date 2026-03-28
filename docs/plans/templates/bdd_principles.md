# BDD Principles for Plan Writing

This document defines the principles the AI assistant must follow when writing plans using the PRD template. These principles are derived from Behavior-Driven Development (BDD) but adapted for product planning — not test automation, not Gherkin syntax, not tooling.

Read this document before drafting any plan.

---

## Foundation: Four Axioms

Everything below derives from these four truths:

| # | Axiom | Implication for plan writing |
|---|---|---|
| A1 | Software exists to **change observable behavior in the real world** | If you cannot describe the observable change, you do not know what you are building. Every FEAT must state what changes for whom. |
| A2 | All behavior decomposes into **context → trigger → result** | This is the universal structure of every product rule, acceptance criterion, and E2E scenario. |
| A3 | Understanding is verified through **concrete examples**, never abstract descriptions | A rule without an example is ambiguous by definition. Examples are the disambiguation mechanism. |
| A4 | Shared understanding requires a **shared language** | Every translation between vocabularies introduces loss. The plan must use domain language, not implementation language. |

---

## Principle 1: Concrete Examples Before Abstract Rules

Derived from A3. This is the single highest-leverage principle.

A rule without examples is ambiguous by definition.

When the AI assistant writes a product rule, constraint, or acceptance criterion, it must follow the rule with 2-3 concrete examples using specific data. The examples are what eliminate ambiguity — the rule alone never does.

Bad — rule only:
> "Loyal customers get a discount."

Loyal how? What discount? On what? Since when?

Good — rule + examples:
> "Customers with 12+ months of tenure receive 15% off at checkout."
> - Marie, 14 months, 100$ cart → pays 85$
> - Paul, 3 months, 100$ cart → pays 100$
> - Luc, exactly 12 months, 100$ cart → pays 85$

If the AI assistant cannot generate concrete examples for a rule, the rule is not understood well enough. Flag it as an open question.

---

## Principle 2: Who + Why Before What

Derived from A1. Every behavior serves a specific actor for a specific reason.

Before describing what a feature does, the plan must establish:
- **Who** has this problem? (a specific role, not "user")
- **What** is the real need? (not the solution)
- **Why** does it matter? (the concrete benefit — the ultimate test of relevance)

If the "why" cannot be articulated, the need is probably not real.

---

## Principle 3: Domain Language, Not Implementation Language

Derived from A4. The plan must use the same words the business domain uses. Every translation between vocabularies introduces loss and ambiguity.

| Do not write | Write instead |
|---|---|
| "The user clicks the submit button" | "The customer confirms the order" |
| "The system sends an event" | "The customer receives a confirmation" |
| "The database is updated" | "The order is recorded" |
| "The record is flagged" | "The account is suspended" |
| "The API returns a 200" | "The request succeeds" |
| "The job is enqueued" | "The report is scheduled" |

The test: if a business stakeholder cannot read and validate a description, it is implementation disguised as product spec.

This applies to every section of the plan — feature descriptions, rules, acceptance criteria, E2E tickets. No exceptions.

---

## Principle 4: One Behavior Per Criterion

Derived from A2. One criterion = one context → one trigger → one result.

Each acceptance criterion, each E2E ticket, each scenario must verify one behavior. Not two, not three.

Bad — multiple behaviors bundled:
> "When the customer places an order: the order is recorded, a confirmation email is sent, inventory is updated, and loyalty points are credited."

Good — one behavior each:
> - "When the customer confirms the order, the order appears in their history with status 'confirmed'."
> - "When the order is confirmed, the customer receives a confirmation email with the order number."
> - "When the order is confirmed, the available quantity for each item is reduced accordingly."
> - "When the order is confirmed, the customer's loyalty account is credited with the corresponding points."

The signal: if a criterion needs "and" more than twice in its result, it is probably bundling distinct behaviors.

---

## Principle 5: Declarative Over Imperative

Describe **what** happens, not **how** it happens. This is the boundary between a need and a solution.

Bad — imperative (describes the UI interaction sequence):
> "The user types 'Montreal' in the search field, clicks the 'Search' button, waits for the page to load, and sees a list of results."

Good — declarative (describes the need):
> "When the customer searches for events in Montreal, the available events in Montreal are displayed."

Why this matters: imperative descriptions are coupled to a specific interface. Declarative descriptions survive UI redesigns, platform changes, and implementation pivots. A plan should describe the behavior the product must deliver, not the specific interaction path.

This applies to feature descriptions, acceptance criteria, and E2E ticket steps.

---

## Principle 6: Separate Discovery From Formulation

Two distinct activities, two distinct moments.

| Phase | What happens | Artifact |
|---|---|---|
| **Discovery** | Explore behaviors, find gray areas, surface unknowns | Brainstorm notes, rough examples, open questions |
| **Formulation** | Write the structured plan using the PRD template | The plan document |

In the AI-assisted workflow: brainstorming (ce:brainstorm) is discovery. Writing the plan from the template is formulation. Do not formalize too early. During discovery, use rough examples, sketches, and questions — not template structure. Premature formulation kills the conversation.

The AI assistant should not start filling in template sections during a brainstorm. When the user says "now plan this," that is the transition from discovery to formulation.

---

## Principle 7: Unresolved Questions Are a Readiness Signal

During plan writing, every question the AI assistant cannot answer is a risk removed early.

The AI assistant must:
- Surface questions explicitly in Section 6 (Open Questions).
- Flag questions inline using `0o0o` when they arise within a FEAT or COMPONENT.
- Not invent answers to fill gaps. Uncertainty must be visible, not buried.

Readiness threshold: if a FEAT or COMPONENT accumulates 5+ unresolved questions, it is not ready to build. This is a signal, not a failure. The plan should flag it explicitly so the PM can resolve the questions before committing to delivery.

---

## Principle 8: Shared Context Stated Once

When multiple acceptance criteria or scenarios within a FEAT share the same setup, state it once rather than repeating it in every criterion.

Bad — context repeated:
> - "Given a catalog with Widget A at 25$ (100 in stock) and Widget B at 50$ (0 in stock), when the customer adds Widget A to cart, the cart shows Widget A."
> - "Given a catalog with Widget A at 25$ (100 in stock) and Widget B at 50$ (0 in stock), when the customer adds Widget B to cart, the customer sees 'Out of stock.'"

Good — shared context established once:
> Context for all criteria below: catalog contains Widget A (25$, 100 in stock) and Widget B (50$, 0 in stock).
> - "When the customer adds Widget A to cart, the cart shows Widget A."
> - "When the customer adds Widget B to cart, the customer sees 'Out of stock.'"

Keep shared context to 3-4 lines. If it grows beyond that, the FEAT probably covers too much ground and should be split.

---

## Principle 9: Tables for Systematic Variations

When a rule produces different results based on different input combinations, use a table instead of writing separate scenarios for each case.

Bad — repetitive individual scenarios:
> - "A 50$ order shipped locally costs 5$ shipping."
> - "A 50$ order shipped nationally costs 12$ shipping."
> - "A 100$ order shipped locally costs 0$ shipping."
> - "A 100$ order shipped nationally costs 0$ shipping."

Good — table showing all variations:
> Shipping cost by order amount and zone:
>
> | Order amount | Zone | Shipping cost |
> |---|---|---|
> | 50$ | local | 5$ |
> | 50$ | national | 12$ |
> | 100$ | local | 0$ |
> | 100$ | national | 0$ |

Tables make it easy to spot missing combinations and verify boundary conditions. Use them whenever a rule has 2+ input dimensions.

---

## The Anti-Pattern to Avoid

The biggest anti-pattern: **treating the plan as post-facto documentation rather than a discovery tool.**

The plan does not document what the system will do — it captures decisions about what the system *should* do, and why. If the AI assistant is merely transcribing what the user said without challenging assumptions, surfacing ambiguity, or generating disambiguating examples, the plan is not doing its job.

A plan full of clean, confident statements with zero open questions is not a sign of clarity — it is a sign that hard questions were not asked.

---

## Summary

| # | Principle | One-line test |
|---|---|---|
| 1 | Concrete examples before abstract rules | Can a reviewer look at specific data and say "yes, that is correct" or "no, that is wrong"? |
| 2 | Who + Why before What | Can you name the role and articulate the benefit? |
| 3 | Domain language, not implementation language | Can a business stakeholder read and validate every description? |
| 4 | One behavior per criterion | Does each criterion have exactly one pass/fail condition? |
| 5 | Declarative over imperative | Would this description survive a complete UI redesign? |
| 6 | Separate discovery from formulation | Was there a brainstorm phase before the plan was written? |
| 7 | Unresolved questions are a readiness signal | Are open questions visible, and is there a threshold for "not ready"? |
| 8 | Shared context stated once | Is repeated setup extracted so criteria stay focused on behavior? |
| 9 | Tables for systematic variations | Are multi-dimension rules shown as tables, not repeated prose? |
