---
name: BDD Principles for Plan Writing
description: BDD principles for product planning -- concrete examples, domain language, one-behavior-per-criterion, declarative style
tags:
  - area/ea
  - kind/template
  - status/stable
date_updated: 2026-04-04
---

# BDD Principles for Plan Writing

This document defines how the AI assistant should apply BDD thinking when writing plans from the PRD template.

This is for product planning, not test automation, not Gherkin syntax, and not tool worship.

If time is limited, do Tier 1 well. Most of the value is there.

---

## Foundation: Four Axioms

Everything below derives from these four truths:

| # | Axiom | Implication for plan writing |
|---|---|---|
| A1 | Software exists to change observable behavior in the real world | If you cannot describe the observable change, you do not know what you are building. Every FEAT must state what changes, for whom. |
| A2 | All behavior decomposes into context -> trigger -> result | This is the universal structure of every product rule, acceptance criterion, and E2E scenario. |
| A3 | Understanding is verified through concrete examples, never abstract descriptions | A rule without examples is ambiguous by definition. Examples are the disambiguation mechanism. |
| A4 | Shared understanding requires a shared language | Every translation between vocabularies introduces loss. The plan must use domain language, not implementation language. |

---

## Tier 1: 80% of the Value

### 1. Concrete Examples Before Abstract Rules

This is the highest-leverage principle.

A rule without examples is ambiguous by definition.

Whenever the AI assistant writes a product rule, constraint, or acceptance criterion, it should follow it with 2-3 concrete examples using specific data.

Prefer this pattern:
- one normal case
- one negative or non-eligible case
- one boundary case

Bad:
> "Loyal customers get a discount."

Good:
> "Customers with 12+ months of tenure receive 15% off at checkout."
> - Marie, 14 months, $100 cart -> pays $85
> - Paul, 3 months, $100 cart -> pays $100
> - Luc, exactly 12 months, $100 cart -> pays $85

If the assistant cannot generate concrete examples for a rule, the rule is not understood well enough. Treat it as an open question instead of guessing.

### 2. Who + Why Before Feature Shape

Every behavior exists for a specific actor and a real outcome.

Before describing what a FEAT does, establish:
- Who has this problem? Use a specific role, not "user".
- What is the real need? Describe the need, not the solution shape.
- Why does it matter? State the concrete benefit or avoided pain.

The "why" is the reality check. If it cannot be stated clearly, the FEAT is probably weak, premature, or mislabeled as a need when it is really a solution idea.

The classic "As a / I need / so that" frame is useful, but the syntax is optional. The clarity is not.

### 3. Domain Language, One Vocabulary

Use the same words the business domain uses. The plan, examples, acceptance criteria, and E2E tickets should all use one shared vocabulary.

| Do not write | Write instead |
|---|---|
| "The user clicks the submit button" | "The customer confirms the order" |
| "The system sends an event" | "The customer receives a confirmation" |
| "The database is updated" | "The order is recorded" |
| "The record is flagged" | "The account is suspended" |
| "The API returns a 200" | "The request succeeds" |
| "The job is enqueued" | "The report is scheduled" |

Hard rule: if a business stakeholder cannot read and validate a description, it is not a BDD-style spec. It is a technical test disguised as a product spec.

### 4. One Behavior Per Criterion

One criterion, one scenario, or one atomic E2E ticket should verify one behavior:
- one context
- one trigger
- one observable result

Bad:
> "When the customer places an order, the order is recorded, a confirmation email is sent, inventory is updated, and loyalty points are credited."

Better:
> - "When the customer confirms the order, the order appears in their history with status 'confirmed'."
> - "When the order is confirmed, the customer receives a confirmation email with the order number."
> - "When the order is confirmed, the available quantity for each item is reduced accordingly."
> - "When the order is confirmed, the customer's loyalty account is credited with the corresponding points."

If a result clause needs several "and" statements, it is probably bundling multiple behaviors. Split it unless the business would truly treat it as one indivisible outcome.

---

## Tier 2: 15% of the Value

### 5. Declarative Over Imperative

Describe what must happen, not the UI choreography or implementation path.

Bad:
> "The user types 'Montreal' in the search field, clicks the 'Search' button, waits for the page to load, and sees a list of results."

Good:
> "When the customer searches for events in Montreal, the available events in Montreal are displayed."

Declarative language survives UI redesigns, platform changes, and implementation pivots. Imperative language couples the plan to one interface.

### 6. Separate Discovery From Formulation

These are different activities and should not be collapsed into one.

| Phase | Goal | Output |
|---|---|---|
| Discovery | Explore behaviors, examples, unknowns, and tradeoffs | Notes, rough examples, open questions |
| Formulation | Write the structured plan using the template | The plan document |

In this workflow, brainstorming or `ce:brainstorm` is discovery. Writing the PRD is formulation.

Do not force template structure too early. During discovery, rough examples and open questions are more valuable than polished prose.

If useful, use Example Mapping during discovery:
- Story
- Rule
- Example
- Question

If questions dominate the conversation, the item is not ready for clean formulation yet.

### 7. Unresolved Questions Are Valuable Output

Open questions are not plan defects. They are risk discovered early.

The assistant must:
- surface questions explicitly in Section 6 (Open Questions)
- flag questions inline using `0o0o` when they arise inside a FEAT or COMPONENT
- avoid inventing answers to make the document look complete

Treat "5+ unresolved questions" as a heuristic, not a law. The real test is whether ambiguity still blocks build decisions.

---

## Tier 3: 5% of the Value

These patterns help readability, but they are secondary. Do not obsess over them before Tier 1 is solid.

### 8. Shared Context Stated Once

When multiple criteria or scenarios share the same setup, state it once rather than repeating it in every line.

Keep shared context short. If it takes more than 3-4 lines, the FEAT probably covers too much ground and should be split or simplified.

### 9. Tables for Systematic Variations

When a rule changes across combinations of inputs, use a table instead of repetitive prose.

Tables are especially useful for:
- multi-variable rules
- boundary conditions
- spotting missing combinations

---

## Main Anti-Pattern

The biggest anti-pattern is treating the plan as post-facto documentation instead of a discovery tool.

A strong plan does not just restate what was said. It clarifies meaning, pressure-tests assumptions, reveals ambiguity, and records unanswered questions.

A perfectly clean plan with zero open questions is usually a warning sign, not an achievement.

---

## Fast Checklist

Before finalizing a plan, ask:
- Can I name the actor and the benefit?
- Does every important rule have concrete examples?
- Do the examples cover a normal case, a negative case, and a boundary?
- Is the language readable to a business stakeholder?
- Does each criterion express one behavior and one observable result?
- Are open questions visible instead of guessed away?
- Did I spend effort on Tier 1 before formatting tricks?

## Related

- [[plan-template-prd]]
- [[1004-feature-plan-template]]
